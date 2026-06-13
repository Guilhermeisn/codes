import sys
import socket

def recv_line(sock):
    line = b""

    while not line.endswitch(b"\r\n"):
        line += sock.recv(1)

    return line

def get_data(site, resource, output):
    my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_sock.connect((site, 80))

    my_sock.send (("GET "+resource+" HTTP/1.1\r\n"+
                   "Host: "+site+"\r\n"+
                   "\r\n").encode())

    data = my_sock.recv(4096)
    pos2NL = data.find(b"\r\n\r\n")
    headers = data[:pos2NL].split(b'\r\n')

    len_data = -1
    for header in headers[1:]:
        header = header.split(b":")
        if header[0] == b"Content-Length":
            len_data = int(header[1])

    if len_data != -1:
        print (f"tamanho dos dados: {len_data}")
        data = data[pos2NL+4:]
        while len(data) < len_data:
            data += my_sock.recv(4096)

        fd = open(output, "wb")
        fd.write(data)
        fd.close()
        print (f"Arquivo salvo em {output}")
    else:
        print ("Content-Length não encontrado!")
        
        transfer_chunked = False

        for header in headers[1:]:
            header = header.lower()

            if header.startswith(b"transfer-encoding"):
                if b"chunked" in header:
                    transfer_chunked = True
                    
        if transfer_chunked:
            print("Transfer-encoding: chunk detectado.")

            body = data[pos2NL+4:]

            arquivo = b""

            while True:

                while b"\r\n" not in body:
                    body += my_sock.recv(4096)

                pos = body.find(b"\r\n")

                tamanho_hex = body[:pos]
                body = body[pos+2:]

                tamanho_chunk = int(tamanho_hex, 16)

                print(f"Chunk recebeido: {tamanho_chunk} bytes. ")

                if tamanho_chunk == 0:
                    break

                while len(body) < tamanho_chunk + 2:
                    body += my_sock.recv(4096)

                arquivo += body[:tamanho_chunk]

                body = body[tamanho_chunk+2:]

            fd = open(output, "wb")
            fd.write(arquivo)
            fd.close()

            print(f"Arquivo salvo em {output}")
        else:
            print(f"[ERRO]: Tipo de transferência não suportado. ")

    my_sock.close()

if len(sys.argv) == 4:
    get_data(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print ("uso: python site resource output_filename")
    print ("Exemplos:")
    print (" python htppclient3.py httpbin.org /image/png porco.png")
    print (" python htppclient3.py viacep.com.br /ws/59062570/json/ meucep.json")
    print (" python htppclient3.py httpbin.org /image/jpeg lobo.jpg")
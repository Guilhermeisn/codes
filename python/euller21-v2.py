def soma_div (n):
    soma = 0
    for i in range (1, n//2 + 1):
        if n % i == 0:
            soma += i
    return soma

LIMITE = 10000
soma = 0
for a in range (1, LIMITE+1):
    b = soma_div(a)
    if (a < b) and (soma_div(b) == a):
        soma += a+b    
        print (a, b)
print (soma)


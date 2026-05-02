def sd (n):
    soma = 0
    for i in range (1, n//2 + 1):
        if n % i == 0:
            soma += i
    return soma

def amigos (a,b):
    if sd (a) == b and sd (b) == a:
        return True
    else:
        return False

LIMITE = 1000
soma = 0
for a in range (1, LIMITE+1):
    for b in range (a+1, LIMITE+1):
        if amigos (a,b):
            soma += a + b
    if a % 10 == 0: print (a)
print (soma)


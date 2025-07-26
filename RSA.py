#Author: João Victor Lima da Silva
import random
import math

CHAVE_PUBLICA = [7990271, 5] #default encryption key
CHAVE_PRIVADA = [7990271, 1596269] #default decryption key

EXTRAS = '\n§áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ'
ALFABETO = {EXTRAS[i]: (abs((len(EXTRAS) + 94)) - i) for i in range(len(EXTRAS))} | {chr(32 + i): (94 - i) for i in range(95)} #Alphabet dict
INVERSO = {num: letra for letra, num in ALFABETO.items()} #Alphabet dict inverse

def ehPrimo(n): #Is Prime function
    if n == 2 or n == 3: 
        return True
    if n % 2 == 0 or n < 2: 
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False    
    return True
def fatoresPrimos(n): #Prime factorization function
    if ehPrimo(n):
        return [n]
    for i in range(2, n+1):
        if n % i == 0 and ehPrimo(i):
            return [i] + fatoresPrimos(n // i)
def eulerPhi(n): #Totient function
    if n == 1:
        return 1
    fatores = fatoresPrimos(n)
    resultado = 1
    for p in set(fatores):
        k = fatores.count(p)
        resultado *= p**(k-1) * (p - 1)
    return resultado
def decimal4Base(num, base): #Converts a number from base 10 to base x
    quociente = num // base
    resto = num % base
    if quociente == 0:
        return [resto]
    return  decimal4Base(quociente, base) + [resto]
def base4Decimal(numLista, base): #Converts a number from base x to base 10 
    listaNum = numLista[::-1]
    decimal = 0
    for i in range(len(listaNum)):
        decimal += listaNum[i] * base**(i)
    return decimal
def geraChaves(p, q): #Generates encryption/decryption keys from 2 prime numbers
    n = p * q
    nPhi = (p - 1) * (q - 1)

    while True: #Chooses e randomly, where 1 < e < phi(n) and gcd(e, phi(n)) == 1
        e = random.randrange(2, nPhi)
        if math.gcd(e, nPhi) == 1:
            break
    d = pow(e, -1, nPhi) #Computes d, where 1 < d =< phi(n) and d*e == 1(mod phi(n))       
    return[[n, e] ,[n, d]]
def checaChavePub(chavePublica): #Checks if public key is valid
    n = chavePublica[0]
    e = chavePublica[1]
    nPhi = eulerPhi(n)
    return (e > 1 and e < nPhi) and (math.gcd(e, nPhi) == 1)
def encriptNum(m, chavePublica): #RSA Encryption
    n = chavePublica[0]
    e = chavePublica[1]
    c = pow(m, e, n) #c = (m**e) % n
    return c
def decriptNum(c, chavePrivada): #RSA Decryption
    n = chavePrivada[0]
    d = chavePrivada[1]
    m = pow(c, d, n)
    return m
def cifraDeBlocosE(texto, chavePublica): #RSA based block cipher encryption
    Mensagem = []
    n = chavePublica[0]
    N = len(ALFABETO)
    compTexto = len(texto) 
    k = int(math.log(n, N))
    
    while len(texto) % k != 0: #Completes the text whith characters if necessary
        #texto += chr(random.randint(97, 122))
        texto += '§'
    compTexto = len(texto)
    for i in range(compTexto): #Converts the text characters into a list of numbers
        if not(texto[i] in  ALFABETO): raise Exception(f"the character '{texto[i]}' at position '{(i+1)}' is not present in the alphabet (char code: {ord(texto[i])}).")
        Mensagem.append(ALFABETO[texto[i]])
    c = []
    for i in range(0, compTexto, k): #List of numbers encryption
        bloco = decimal4Base(encriptNum(base4Decimal(Mensagem[i:i+k], N), chavePublica), N)
        bloco.reverse()
        while len(bloco) != k+1:
            bloco.append(0)
        bloco.reverse()
        c += bloco
    for i in range(len(c)): #Converts the list of numbers into a text
        c[i] = INVERSO[c[i]]
    return ''.join(c)
def cifraDeBlocosD(texto, chavePrivada): #RSA based block cipher decryption
    Mensagem = []
    n = chavePrivada[0]
    N = len(ALFABETO)
    compTexto = len(texto) 
    k = int(math.log(n, N))
    for i in range(compTexto): #Converts the text characters into a list of numbers
        if not (texto[i] in  ALFABETO): raise Exception(f"the character '{texto[i]}' at position '{(i+1)}' is not present in the alphabet (char code: {ord(texto[i])}).")
        Mensagem.append(ALFABETO[texto[i]])
    m = []
    for i in range(0, compTexto, k+1): #List of numbers decryption
        bloco = decimal4Base(decriptNum(base4Decimal(Mensagem[i:i+(k+1)], N), chavePrivada), N)    
        bloco.reverse()
        if len(bloco) > k: raise ValueError("Message undecodable by the key.")
        while len(bloco) != k:
            bloco.append(0)
        bloco.reverse()
        m += bloco 
    for i in range(len(m)): #Converts the list of numbers into a text
        m[i] = INVERSO[m[i]]
    return ''.join(m).replace("§", "") #Removes addtional character if exists
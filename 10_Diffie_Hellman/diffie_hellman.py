import sys
import random

# returns (k, m) such that n = 2^k * m
def decompose(n):
    k = 0
    m = n
    while (m % 2 == 0):
        k += 1
        m = m // 2
    return (k, m)

#return True if n is prime, else False
def millerRabin(n):
    (k, m) = decompose(n-1)
    a = random.randint(2, n-1)
    b = pow(a, m, n)
    if b % n == 1:
        return True
    for _ in range(k):
        if b % n == n-1:
            return True
        b = pow(b, 2, n)
    return False

# repeatdly check if n is prime with millerRabin
# P(FalsePositive) < 1/4^rounds
def isPrime(n, rounds):
    for _ in range(rounds):
        if (not millerRabin(n)):
            return False
    return True

iList = [1,7,11,13,17,19,23,29]

# generates a prime number
def generatePrime(length):
    z = random.randint(2**(length-1), 2**length-1)
    iIndex = 0
    while(True):
        n = 30*(z+iIndex//len(iList)) + iList[iIndex % len(iList)]
        # check multiple times if prime
        # P(FalsePositive) < 1/4^100 = 6.223015 × 10^-61
        # if length > 26 then n>10^9 and P(FalsePositive) < (10^-6)^100 = 10^-600 see https://core.ac.uk/download/pdf/197479038.pdf
        if (isPrime(n,100)):
            return n
        iIndex += 1

# generates p = 2*q + 1 with q and p prime
def generateP(keylength):
    while True:
        q = generatePrime(keylength-1)
        p = 2*q + 1
        if (isPrime(p,100)):
            return p

# Berechnung eines Erzeugers von Zp für p = 2q + 1
def getGenerator(p):
    q = (p - 1) // 2
    while True:
        a = random.randint(2, p-1)
        if (pow(a, (p-1)//2, p) != 1 and pow(a, (p-1)//q, p) != 1):
            return a

# main 
if (len(sys.argv) != 2 and len(sys.argv) != 3):
    print("Usage: python3 diffie_hellman.py keylength [output_file]") # output_file for testing
    exit(1)

keylength = int(sys.argv[1])
output_file = sys.argv[2] if len(sys.argv) == 3 else None

p = generateP(keylength)
g = getGenerator(p)
a = random.randint(2, p-1)
b = random.randint(2, p-1)

# calculate secret
A = pow(g, a, p)
B = pow(g, b, p)
# key exchange would happen here
S = pow(B, a, p)

if(output_file):
    with open(output_file, "w") as f:
        f.write(str(p) + "\n" + str(g) + "\n" + str(a) + "\n" + str(b) + "\n" + str(A) + "\n" + str(B) + "\n" + str(S))
print(p)
print(g)
print(A)
print(B)
print(S)
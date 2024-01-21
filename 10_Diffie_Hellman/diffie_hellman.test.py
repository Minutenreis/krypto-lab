import subprocess
import os
import random

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
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
    # you could deterministicly test this if n < 3,317,044,064,679,887,385,961,981 was known see https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    a = random.randint(2, n-1) # todo: sollte es nicht n-2 sein?
    b = pow(a, m, n) # todo: sollen wir hier die RSA funktion verwenden?
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

run("diffie_hellman.py", "100", "temp.txt")

with open("temp.txt", "r") as f:
    (p,g,a,b,A,B,S) = f.read().split()

expect("diffie_hellman.py p prime", True, isPrime(int(p),1000))
expect("diffie_hellman.py g generator", True, pow(int(g), (int(p)-1)//2, int(p)) != 1 and pow(int(g), (int(p)-1)//2,int(p)) != 1)
expect("diffie_hellman.py same secret", pow(int(A), int(b), int(p)), pow(int(B), int(a), int(p)))
expect("diffie_hellman.py S = g**(a*b)", pow(int(g), int(a)*int(b), int(p)), int(S))

os.remove("temp.txt")
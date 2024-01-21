import sys
import random

# calculates phi(n = p * q) of 2 primes p and q
def phi(prime1, prime2):
    return (prime1 - 1) * (prime2 - 1)

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

# returns (gcd(a,b), p, q) such that a*p + b*q = gcd(a,b)
def expandedEuclid(a, b):
    n = 0
    rn_1 = a
    rn = b
    pn_1 = 1
    pn = 0
    qn_1 = 0
    qn = 1
    while(True):
        n += 1
        d = rn_1 // rn
        # assign "last" values the k+1 values
        rn_1 = rn_1 - d * rn
        pn_1 = pn_1 - d * pn
        qn_1 = qn_1 - d * qn
        if (rn_1 == 0):
            break
        # swap into correct order
        rn_1, rn = rn, rn_1
        pn_1, pn = pn, pn_1
        qn_1, qn = qn, qn_1
    return (rn, pn, qn)

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

# generate public and private key as ((e,n),(d,n))
def genKeys(p,q):
    n = p * q
    phiN = phi(p, q)
    e = 2**16 + 1 # todo: sollte es tatsächlich zufällig sein?
    while (expandedEuclid(e, phiN)[0] != 1):
        e = random.randint(3, phiN-1)
    d = expandedEuclid(e, phiN)[1] % phiN
    return ((e,n), (d,n))

# main
if (len(sys.argv) != 5):
    print("Usage: python3 RSA_keygen.py length output_private_key output_public_key output_primes")
    exit(1)
    
length = int(sys.argv[1])
output_private_key = sys.argv[2]
output_public_key = sys.argv[3]
output_primes = sys.argv[4]

# generate two primes
p = generatePrime(length)
q = generatePrime(length)
(e, n), (d, n) = genKeys(p,q)
with open(output_private_key, "w") as f:
    f.write(str(d) + "\n" + str(n))
with open(output_public_key, "w") as f:
    f.write(str(e) + "\n" + str(n))
with open(output_primes, "w") as f:
    f.write(str(p) + "\n" + str(q))
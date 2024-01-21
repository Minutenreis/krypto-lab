import subprocess
import os

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
run ("RSA_Keygen.py", "100", "tempPrivate.txt", "tempPublic.txt", "tempPrimes.txt")

with open("tempPrivate.txt", "r") as f:
    (d,dn) = f.read().split()
with open("tempPublic.txt", "r") as f:
    (e,en) = f.read().split()
with open("tempPrimes.txt", "r") as f:
    (p,q) = f.read().split()

expect("RSA_Keygen.py n same across keys", dn, en)
expect("RSA_Keygen.py ed = 1", int(d)*int(e)%((int(p)-1)*(int(q)-1)), 1)
expect("RSA_Keygen.py primes form n", int(p)*int(q), int(dn))

os.remove("tempPrivate.txt")
os.remove("tempPublic.txt")
os.remove("tempPrimes.txt")

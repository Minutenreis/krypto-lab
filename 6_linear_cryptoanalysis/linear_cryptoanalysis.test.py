import subprocess
import os

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

run("generateExampleTexts.py", "plaintexts.txt", "4000")

with open("plaintexts.txt", 'r') as f:
    plaintexts = f.readlines()

expect("generateExampleTexts.py length", 4000, len(plaintexts))

run("SPN.py", "plaintexts.txt", "key.txt", "ciphertexts.txt")

with open("ciphertexts.txt", 'r') as f:
    ciphertexts = f.read().split(" ")

expect("SPN.py length", 4000, len(ciphertexts))

# default this to false because this test both takes up a lot of compute time and is by nature not deterministic
runLinApproxTest = False
if runLinApproxTest:
    run("LinApprox.py", "plaintexts.txt", "ciphertexts.txt", "temp.txt")

    with open("temp.txt", 'r') as f:
        approxKey = f.read()
    with open("key.txt", 'r') as f:
        key = f.read()

    expect("LinApprox.py", approxKey, key[1]+key[3])

os.remove("plaintexts.txt")
os.remove("ciphertexts.txt")
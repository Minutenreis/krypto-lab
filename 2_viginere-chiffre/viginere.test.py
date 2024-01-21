import subprocess
import os

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
run("encrypt-viginere.py", "Klartext_1.txt", "TAG", "temp.txt")

with open("Kryptotext_TAG.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("encrypt-viginere.py", expected, actual)

os.remove("temp.txt")

run("auto-decode-viginere.py", "Kryptotext_TAG.txt", "temp.txt")

with open("Klartext_1.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read().split("\n")[1]
    
expect("auto-decode.py", expected, actual)

os.remove("temp.txt")
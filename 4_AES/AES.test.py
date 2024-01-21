import subprocess
import os

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
run("AES.py","Klartext_1.txt","key.txt","temp.txt", "encrypt")

with open("Kryptotext_1.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("AES.py encrypt 1", expected, actual)

os.remove("temp.txt")

run("AES.py","Klartext_2.txt","key.txt","temp.txt", "encrypt")

with open("Kryptotext_2.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("AES.py encrypt 2", expected, actual)

os.remove("temp.txt")

run("AES.py","Kryptotext_1.txt","key.txt","temp.txt", "decrypt")

with open("Klartext_1.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("AES.py decrypt 1", expected, actual)

os.remove("temp.txt")

run("AES.py","Kryptotext_2.txt","key.txt","temp.txt", "decrypt")

with open("Klartext_2.txt", "r") as f:
    expected = f.read()
    
with open("temp.txt", "r") as f:
    actual = f.read()

expect("AES.py decrypt 2", expected, actual)

os.remove("temp.txt")
import subprocess
import os

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
run("RSA.py","ExampleText.txt","ExampleKey.txt","temp.txt")

with open("ExampleEncrypted.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("RSA.py encrypt", expected, actual)

os.remove("temp.txt")

run("RSA.py","ExampleEncrypted.txt","ExampleKeyDecrypt.txt","temp.txt")

with open("ExampleText.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("RSA.py decrypt", expected, actual)

os.remove("temp.txt")

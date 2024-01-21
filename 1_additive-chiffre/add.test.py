import subprocess
import os

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

run("encrypt-add.py", "Klartext_1.txt", "7", "temp.txt")

with open("Kryptotext_1_Key_7.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("encrypt-add.py", expected, actual)

os.remove("temp.txt")

run("decrypt-add.py", "Kryptotext_1_Key_7.txt", "7", "temp.txt")

with open("Klartext_1.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("decrypt-add.py", expected, actual)

os.remove("temp.txt")

run("auto-decode-add.py","sampleEncrypted.txt","temp.txt")

with open("sampleDecrypted.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("auto-decode-add.py", expected, actual)

os.remove("temp.txt")


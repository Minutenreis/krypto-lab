import subprocess
import os

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

run("AES_Encryption.py", "ECB","Klartext_dirty.txt", "key.txt", "temp_dirty.txt")
run("AES_Encryption.py", "ECB","Klartext_clean.txt", "key.txt", "temp_clean.txt")

with open("temp_clean.txt", "r") as f:
    expected = f.read()
with open("temp_dirty.txt", "r") as f:
    actual = f.read()

expect("AES_Encryption.py Clean Input", expected, actual)

os.remove("temp_clean.txt")
os.remove("temp_dirty.txt")

run("AES_Encryption.py", "ECB","Klartext_1.txt", "key.txt", "temp.txt")

with open("Kryptotext_1.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("AES_Encryption.py encrypt 1", expected, actual)

os.remove("temp.txt")

run("AES_Decryption.py", "ECB","Kryptotext_1.txt", "key.txt", "temp.txt")

with open("Klartext_1.txt", "r") as f:
    expected = f.read()
with open("temp.txt", "r") as f:
    actual = f.read()

expect("AES_Encryption.py decrypt 1", expected, actual)

os.remove("temp.txt")

run("AES_Encryption.py", "ECB","Klartext_clean.txt", "key.txt", "temp.txt")
run("AES_Decryption.py", "ECB","temp.txt", "key.txt", "temp_2.txt")

with open("Klartext_clean.txt", "r") as f:
    expected = f.read()
with open("temp_2.txt", "r") as f:
    actual = f.read()
    
expect("AES_Encryption.py ECB", expected, actual)

os.remove("temp.txt")
os.remove("temp_2.txt")

run("AES_Encryption.py", "CBC","Klartext_clean.txt", "key.txt", "temp.txt", "InitVec.txt")
run("AES_Decryption.py", "CBC","temp.txt", "key.txt", "temp_2.txt","InitVec.txt")

with open("Klartext_clean.txt", "r") as f:
    expected = f.read()
with open("temp_2.txt", "r") as f:
    actual = f.read()

expect("AES_Encryption.py CBC", expected, actual)

os.remove("temp.txt")
os.remove("temp_2.txt")

run("AES_Encryption.py", "OFB","Klartext_clean.txt", "key.txt", "temp.txt","InitVec.txt")
run("AES_Decryption.py", "OFB","temp.txt", "key.txt", "temp_2.txt","InitVec.txt")

with open("Klartext_clean.txt", "r") as f:
    expected = f.read()
with open("temp_2.txt", "r") as f:
    actual = f.read()

expect("AES_Encryption.py OFB", expected, actual)

os.remove("temp.txt")
os.remove("temp_2.txt")

run("AES_Encryption.py", "CTR","Klartext_clean.txt", "key.txt", "temp.txt","InitVec.txt")
run("AES_Decryption.py", "CTR","temp.txt", "key.txt", "temp_2.txt","InitVec.txt")

with open("Klartext_clean.txt", "r") as f:
    expected = f.read()
with open("temp_2.txt", "r") as f:
    actual = f.read()

expect("AES_Encryption.py CTR", expected, actual)

os.remove("temp.txt")
os.remove("temp_2.txt")
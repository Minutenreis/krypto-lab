import subprocess
import os
import hashlib
import codecs

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    

run("sha3.py", "LoremIpsum5Hex.txt", "test.txt")

with open("test.txt", "r") as file:
    output = file.read()

with open("LoremIpsum5Hex.txt", "r") as file:
    hexData = file.read()
    hexData = hexData.replace(" ", "")
    utf8Data = codecs.decode(hexData, "hex").decode("utf-8")
    
expect("sha3_224", hashlib.sha3_224(utf8Data.encode()).hexdigest(), output)

os.remove("test.txt")
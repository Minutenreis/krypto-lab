import subprocess
import os
import hashlib

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    

run("sha3.py", "input.txt", "test.txt")

with open("test.txt", "r") as file:
    output = file.read()

with open("input.txt", "r") as file:
    data = file.read()

expect("sha3_224", hashlib.sha3_224(data.encode()).hexdigest(), output)

os.remove("test.txt")

print(hashlib.sha3_224("".encode()).hexdigest())
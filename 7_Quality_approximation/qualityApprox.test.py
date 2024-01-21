import subprocess
import os

def expect(name, expected, actual):
    print("  ",name, "\033[92mpassed" if expected == actual else "\033[91mfailed",'\033[0m')

def run(*args):
    arguments = list(args)
    arguments.insert(0, "python3")
    subprocess.call(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

run("qualityApprox.py", "testSbox.txt", "testApprox.txt", "temp.txt")

with open("temp.txt", 'r') as f:
    approxQuality = f.read()

# a = 0011, b = 1001, see lecture L(a,b) = 2 => bias = -3/8
# T = (-3/8)**4 because of 4 rounds with the same approximation
expect("qualityApprox.py", (3/8)**4, float(approxQuality))

os.remove("temp.txt")
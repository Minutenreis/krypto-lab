import sys
import re

def hexToBinary(hex: str) -> str:
    hex = re.sub(r"[^a-f0-9]", '', hex)
    return ''.join(format(int(hex[i:i+2], 16), '08b') for i in range(0, len(hex), 2))

def binaryToHex(binary: str) -> str:
    return ' '.join(''.join([hex(int(binary[i:i+4], 2))[2:],hex(int(binary[i+4:i+8], 2))[2:],hex(int(binary[i+8:i+12], 2))[2:],hex(int(binary[i+12:i+16], 2))[2:]]) for i in range(0, len(binary), 16))

# XOR two binary strings of the same length
def xor(a:str, b:str) -> str:
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

def binaryToInt(binary: str) -> int:
    return int(binary, 2)

def toBlocks(binary: str) -> list:
    return [binary[i:i+16] for i in range(0, len(binary), 16)]


sbox = ["1110","0100", "1101", "0001", "0010", "1111", "1011", "1000", "0011", "1010", "0110", "1100", "0101", "1001", "0000", "0111"]
perm = [0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]

def SBox(x: str) -> str:
    return sbox[binaryToInt(x[0:4])] + sbox[binaryToInt(x[4:8])] + sbox[binaryToInt(x[8:12])] + sbox[binaryToInt(x[12:16])]
    
def permute(x: str) -> str:
    return ''.join(x[perm[i]] for i in range(16))
    
def spn(input: str, k: str) -> str:
    xBlocks = toBlocks(input)
    output = ""
    for x in xBlocks:
        w = x
        for r in range(1,3):
            u = xor(w, k)
            v = SBox(u)
            w = permute(v)
        u = xor(w, k)
        v = SBox(u)
        output += xor(v, k)
    return output

if len(sys.argv) != 4:
    print("Usage: python3 SPN.py <input file> <key file> <output file>")
    sys.exit(1)

inputFile = sys.argv[1]
keyFile = sys.argv[2]
outputFile = sys.argv[3]

with open(inputFile, 'r') as f:
    input = hexToBinary(f.read())

with open(keyFile, 'r') as f:
    key = hexToBinary(f.read())

output = spn(input, key)

with open(outputFile, 'w') as f:
    f.write(binaryToHex(output))
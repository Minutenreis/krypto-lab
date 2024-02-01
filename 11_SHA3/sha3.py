import sys
import re
import os

# Sha3-224
# rounds: 24
rounds = 24
# Hash length: d = 224 bits
d = 224
# Block size: r = 1152 bits
r = 1152
# Capacity: c = 448 bits
c = 448
# Block width: b = c + r = 1600 bits
b = c + r

def cleanHex(hex):
    return re.sub(r"[^A-Fa-f0-9]", '', hex).lower()

def cleanBinary(binary):
    return re.sub(r"[^01]", '', binary)

def convert2HexTo8Bit(hex):
    return bin(int(hex, 16))[2:].zfill(8)[::-1]

def convertHexToBinary(hex):
    hex = cleanHex(hex)
    return "".join([convert2HexTo8Bit(hex[i:i+2]) for i in range(0, len(hex), 2)])

def convert8BitTo2Hex(binary):
    return hex(int(binary[::-1], 2))[2:].zfill(2)

def convertBinaryToHex(binary):
    binary = cleanBinary(binary)
    return "".join([convert8BitTo2Hex(binary[i:i+8]) for i in range(0, len(binary), 8)])

# XOR n binary strings of the same length
def xor(*args):
    return ''.join(str(sum(int(i) for i in x) % 2) for x in zip(*args))

# AND n binary strings of the same length
def and_(*args):
    return ''.join(str(min(int(i) for i in x)) for x in zip(*args))

# not a binary string
def not_(a):
    return ''.join(str(1-int(i)) for i in a)

# get the rotations and roundConstants from the files
dir = os.path.dirname(__file__)
rotationFile = os.path.join(dir, 'rotations.txt')
roundConstantsFile = os.path.join(dir, 'roundConstants.txt')

# rotation[i][j] = rotation[i+j*5]
rotation = [[0, 1, 62, 28, 27],
            [36, 44, 6, 55, 20],
            [3, 10, 43, 25, 39],
            [41, 45, 15, 21, 8],
            [18, 2, 61, 56, 14]]

with open(roundConstantsFile, "r") as file:
    roundConstantsHex = file.read().split(",\n")
    roundConstantsHex = ["".join((hex[14:16],hex[12:14],hex[10:12],hex[8:10],hex[6:8],hex[4:6],hex[2:4],hex[0:2])) for hex in roundConstantsHex]
    roundConstants = [convertHexToBinary(hex) for hex in roundConstantsHex]

# calculates coordinates in strided array (string)
def getCoord(i,j,k):
    return (i % 5) * 5 * 64 + (j % 5) * 64 + (k % 64)

def getBlock(A,i,j):
    return A[getCoord(i,j,0):getCoord(i,j,0)+64]

# rotation of words
def pi(A):
    out = ""
    for i in range(5):
        for j in range(5):
            out+=getBlock(A,j,3*i+j)
    return out

# nonlinear adding
def chi(A):
    out = ""
    for i in range(5):
        for j in range(5):
            out += xor(getBlock(A,i,j), 
                       and_(
                           not_(getBlock(A,i,j+1)), 
                           getBlock(A,i,j+2)
                       ))
    return out

# add roundconstant
def iota(A,r):
    return xor(A[:64], roundConstants[r]) + A[64:]

# inplace rotation of the blocks
def rho(A):
    out = ""
    for i in range(5):
        for j in range(5):
            # right shift
            out += getBlock(A,i,j)[64-rotation[i][j]:]+getBlock(A,i,j)[:64-rotation[i][j]]
    return out
        
# calculates parity of a column
def parityCol(A,j,k):
    return xor(A[getCoord(0,j,k)], A[getCoord(1,j,k)], A[getCoord(2,j,k)], A[getCoord(3,j,k)], A[getCoord(4,j,k)])

# calculate parity of a column
def theta(A):
    out = ""
    for i in range(5):
        for j in range(5):
            for k in range(64): # start at 63 so we move linearly through the array
                out += xor(A[getCoord(i,j,k)], parityCol(A,j-1,k),parityCol(A,j+1,k-1))
    return out
                
# Padding function
def pad(N):
    N = N + "1"
    padded = []
    while len(N) - r >= 0:
        padded += [N[:r]]
        N = N[r:]
    padded += [N + "0" * (r - len(N) - 1) + "1"]
    return padded

# Permutation function
def f(A):
    for r in range(rounds):
        A = theta(A)
        A = rho(A)
        A = pi(A)
        A = chi(A)
        A = iota(A,r)
    return A

# Sha3-224
def sha3_224(str):
    str = str + "01"
    blocks = pad(str)
    state = "0" * b
    for block in blocks:
        state = xor(state, block+("0"*c))
        state = f(state)
    return state[0:d]

# input = """
# 06 00 00 00 00 00 00 00 00 00 10 00 00 70 00 00
# 00 00 03 00 00 00 00 00 06 00 10 00 00 00 00 00
# 00 00 03 00 00 70 00 00 00 00 00 08 00 00 00 00
# 00 00 C0 00 00 E0 00 00 00 00 00 00 00 00 00 00
# 00 00 00 08 00 E0 00 00 00 00 C0 00 00 00 00 00
# 0E 00 00 01 00 00 00 00 00 0C 00 00 00 00 00 00
# 00 00 00 01 00 00 00 00 0E 0C 00 00 00 00 00 00
# 00 00 00 00 00 00 00 00 00 1C 00 60 00 00 00 00
# 00 40 00 00 00 00 00 00 00 1C 00 00 00 00 80 00
# 00 40 00 60 00 00 00 00 00 00 00 00 00 00 80 00
# 00 00 00 00 00 06 00 00 00 00 00 00 00 00 40 00
# 1C 00 00 00 00 06 00 00 00 00 00 00 00 00 00 00
# 1C 00 00 00 00 00 40 00
# """

# binInput = convertHexToBinary(input)
# output = iota(binInput,0)
# hexOutput = convertBinaryToHex(output)
# result = """
# 07 00 00 00 00 00 00 00 00 00 10 00 00 70 00 00
# 00 00 03 00 00 00 00 00 06 00 10 00 00 00 00 00
# 00 00 03 00 00 70 00 00 00 00 00 08 00 00 00 00
# 00 00 C0 00 00 E0 00 00 00 00 00 00 00 00 00 00
# 00 00 00 08 00 E0 00 00 00 00 C0 00 00 00 00 00
# 0E 00 00 01 00 00 00 00 00 0C 00 00 00 00 00 00
# 00 00 00 01 00 00 00 00 0E 0C 00 00 00 00 00 00
# 00 00 00 00 00 00 00 00 00 1C 00 60 00 00 00 00
# 00 40 00 00 00 00 00 00 00 1C 00 00 00 00 80 00
# 00 40 00 60 00 00 00 00 00 00 00 00 00 00 80 00
# 00 00 00 00 00 06 00 00 00 00 00 00 00 00 40 00
# 1C 00 00 00 00 06 00 00 00 00 00 00 00 00 00 00
# 1C 00 00 00 00 00 40 00
# """
# result = cleanHex(result)
# print(result)
# print()
# print(hexOutput)
# print(result == hexOutput)



if len(sys.argv) != 3:
    print("Usage: python sha3.py input_file output_file")
    sys.exit(1)
    
input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as file:
    data = convertHexToBinary(file.read())

with open(output_file, "w") as file:
    file.write(convertBinaryToHex(sha3_224("")))
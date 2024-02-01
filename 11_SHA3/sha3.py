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

# converts hex string to binary string
def hexToBinary(hex: str) -> str:
    hex = re.sub(r"[^A-Fa-f0-9]", '', hex)
    return ''.join(format(int(hex[i], 16), '04b') for i in range(0, len(hex), 1))

# converts binary string to hex string
def binaryToHex(binary: str) -> str:
    return ''.join(''.join([hex(int(binary[i:i+4], 2))[2:]]) for i in range(0, len(binary), 4))

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
rotation = []

with open(rotationFile, "r") as file:
    rotation = " ".join(file.read().split("\n")).split(", ")
    rotation = [int(x) for x in rotation]

with open(roundConstantsFile, "r") as file:
    roundConstantsHex = file.read().split(",\n")
    roundConstants = [hexToBinary(hex[2:]) for hex in roundConstantsHex]

# calculates coordinates in strided array (string)
def getCoord(i,j,k):
    return (i % 5) * 5 * 64 + (j % 5) * 64 + 63-(k % 64)

def getBlock(A,i,j):
    return A[getCoord(i,j,0):getCoord(i,j,0)+1]

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
    for i in range(25):
        block = A[i*64:(i+1)*64]
        block = block[:rotation[i]] + block[rotation[i]:]
        out += block
    return out
        
# calculates parity of a column
def parityCol(A,j,k):
    return xor(A[getCoord(0,j,k)], A[getCoord(1,j,k)], A[getCoord(2,j,k)], A[getCoord(3,j,k)], A[getCoord(4,j,k)])

# calculate parity of a column
def theta(A):
    out = ""
    for i in range(5):
        for j in range(5):
            for k in range(63,-1,-1): # start at 63 so we move linearly through the array
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
    # str = str + "01"
    blocks = pad(str)
    state = "0" * b
    for block in blocks:
        state = xor(state, block+("0"*c))
        state = f(state)
    return state[0:d]
print(len("00000110"+ "0"*1136+"10000000"+"0"*448))
test = binaryToHex(theta("00000110"+ "0"*1136+"10000000"+"0"*448))
result = """
06 00 00 00 00 00 00 00 07 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80
0C 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 80 0C 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 07 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80
0C 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80
00 00 00 00 00 00 00 80 0C 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 07 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80
0C 00 00 00 00 00 00 00
"""
print(re.sub(r"[^A-Fa-f0-9]", '', result) == test)



# if len(sys.argv) != 3:
#     print("Usage: python sha3.py input_file output_file")
#     sys.exit(1)
    
# input_file = sys.argv[1]
# output_file = sys.argv[2]

# with open(input_file, "r") as file:
#     data = hexToBinary(file.read())

# with open(output_file, "w") as file:
#     file.write(binaryToHex(sha3_224(data)))
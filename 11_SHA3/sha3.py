import sys
import re

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

# clean hex string of non-hex characters and convert to lowercase
def cleanHex(hex):
    return re.sub(r"[^A-Fa-f0-9]", '', hex).lower()

# clean binary string of non-binary characters
def cleanBinary(binary):
    return re.sub(r"[^01]", '', binary)

# convert 2 hex characters to 8 bit binary string in little endian
def convert2HexTo8Bit(hex):
    return bin(int(hex, 16))[2:].zfill(8)[::-1]

# convert hex string to binary string in little endian
def convertHexToBinary(hex):
    hex = cleanHex(hex)
    return "".join([convert2HexTo8Bit(hex[i:i+2]) for i in range(0, len(hex), 2)])

# convert 8 bit binary string in little endian to 2 hex characters
def convert8BitTo2Hex(binary):
    return hex(int(binary[::-1], 2))[2:].zfill(2)

# convert binary string in little endian to hex string
def convertBinaryToHex(binary):
    binary = cleanBinary(binary)
    return "".join([convert8BitTo2Hex(binary[i:i+8]) for i in range(0, len(binary), 8)])

# bitwise XOR n binary strings of the same length
def xor(*args):
    return ''.join(str(sum(int(i) for i in x) % 2) for x in zip(*args))

# bitwise AND n binary strings of the same length
def and_(*args):
    return ''.join(str(min(int(i) for i in x)) for x in zip(*args))

# bitwise not a binary string
def not_(a):
    return ''.join(str(1-int(i)) for i in a)

# rotation[i][j]
rotation = [[0, 1, 62, 28, 27],
            [36, 44, 6, 55, 20],
            [3, 10, 43, 25, 39],
            [41, 45, 15, 21, 8],
            [18, 2, 61, 56, 14]]

# round constants
roundConstantsHex = [
    "0000000000000001",
    "0000000000008082",
    "800000000000808A",
    "8000000080008000",
    "000000000000808B",
    "0000000080000001",
    "8000000080008081",
    "8000000000008009",
    "000000000000008A",
    "0000000000000088",
    "0000000080008009",
    "000000008000000A",
    "000000008000808B",
    "800000000000008B",
    "8000000000008089",
    "8000000000008003",
    "8000000000008002",
    "8000000000000080",
    "000000000000800A",
    "800000008000000A",
    "8000000080008081",
    "8000000000008080",
    "0000000080000001",
    "8000000080008008"]

roundConstantsHex = ["".join((hex[14:16],hex[12:14],hex[10:12],hex[8:10],hex[6:8],hex[4:6],hex[2:4],hex[0:2])) for hex in roundConstantsHex]
roundConstants = [convertHexToBinary(hex) for hex in roundConstantsHex]

# calculates coordinates in strided array (string)
def getCoord(i,j,k):
    return (i % 5) * 5 * 64 + (j % 5) * 64 + (k % 64)

# get block from array
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

# main
if len(sys.argv) != 3:
    print("Usage: python sha3.py input_file output_file")
    sys.exit(1)
    
input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as file:
    data = convertHexToBinary(file.read())

with open(output_file, "w") as file:
    file.write(convertBinaryToHex(sha3_224(data)))
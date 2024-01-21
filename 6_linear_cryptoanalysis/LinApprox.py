import sys
import re

# XOR n binary strings of the same length
def xor(*args):
    return ''.join(str(sum(int(i) for i in x) % 2) for x in zip(*args))

# converts hex string to binary string
def hexToBinary(hex: str) -> str:
    hex = re.sub(r"[^A-Fa-f0-9]", '', hex)
    return ''.join(format(int(hex[i], 16), '04b') for i in range(0, len(hex), 1))

# converts binary string to hex string
def binaryToHex(binary: str) -> str:
    return ''.join(''.join([hex(int(binary[i:i+4], 2))[2:]]) for i in range(0, len(binary), 4))

# converts binary string to integer
def binaryToInt(binary: str) -> int:
    return int(binary, 2)

# converts integer to 4 bit binary string
def intTo4BitBinary(i: int) -> str:
    return format(i, '04b')

sbox = ["1110","0100", "1101", "0001", "0010", "1111", "1011", "1000", "0011", "1010", "0110", "1100", "0101", "1001", "0000", "0111"]
invSbox = [intTo4BitBinary(sbox.index(intTo4BitBinary(i))) for i in range(16)]
perm = [0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]
hexDigits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
partialKeys = [(hexToBinary(i),hexToBinary(j)) for i in hexDigits for j in hexDigits] # (L1, L2, alpha(L1,L2))

# access InvSBox with binary string
def InvSBox(x: str) -> str:
    return invSbox[binaryToInt(x)]

alpha = [0 for i in range(16**2)]

# calculate the most likely approximation
def getMaxKey(M):
    for (x,y) in M:
        for (L1, L2) in partialKeys:
            v2 = xor(L1, y[4:8])
            v4 = xor(L2, y[12:16])
            u2 = InvSBox(v2)
            u4 = InvSBox(v4)
            if xor(x[4],x[6],x[7],u2[1],u2[3],u4[1],u4[3]) == "0":
                alpha[binaryToInt(L1)+ binaryToInt(L2)*16] += 1
    maxval = -1
    for (L1, L2) in partialKeys:
        beta = abs(alpha[binaryToInt(L1)+ binaryToInt(L2)*16] - len(M)/2)
        if beta > maxval:
            maxval = beta
            maxkey = (L1, L2)
    return maxkey
    
            
if len(sys.argv) != 3 and len(sys.argv) != 4:
    print("Usage: python3 LinApprox.py plaintexts.txt ciphertexts.txt [output_file]")
    exit(1)

output_file = sys.argv[3] if len(sys.argv) == 4 else None

plaintext = sys.argv[1]
ciphertext = sys.argv[2]

with open(plaintext, "r") as f:
    plaintexts = f.read()
    plaintexts = re.sub(r"[^a-f0-9]", '', plaintexts)
    plaintexts = [hexToBinary(plaintexts[i:i+4]) for i in range(0, len(plaintexts), 4)]

with open(ciphertext, "r") as f:
    ciphertexts = f.read()
    ciphertexts = re.sub(r"[^a-f0-9]", '', ciphertexts)
    ciphertexts = [hexToBinary(ciphertexts[i:i+4]) for i in range(0, len(ciphertexts), 4)]

M = [(plain, cipher) for (plain, cipher) in zip(plaintexts, ciphertexts)]

maxKey = getMaxKey(M)

if output_file:
    with open(output_file, 'w') as f:
        f.write(binaryToHex(maxKey[0]+maxKey[1]))
print(binaryToHex(maxKey[0]+maxKey[1]))

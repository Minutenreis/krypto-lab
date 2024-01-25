import sys
import re

# XOR n binary strings of the same length
def xor(*args):
    return ''.join(str(sum(int(i) for i in x) % 2) for x in zip(*args))

# AND n binary strings of the same length
def andBin(*args):
    return ''.join(str(min(int(i) for i in x)) for x in zip(*args))

# converts hex string to binary string
def hexToBinary(hex: str) -> str:
    hex = re.sub(r"[^A-Fa-f0-9]", '', hex)
    return ''.join(format(int(hex[i], 16), '04b') for i in range(0, len(hex), 1))

# converts integer to 4 bit binary string
def intTo4BitBinary(i: int) -> str:
    return format(i, '04b')

# calculates the quality of the approximation
def calcQuality(U, V, approximation):
    T = 1
    for i in range(4):
        L = 0
        for j in range(16):
            u = U[j]
            v = V[j]
            Ua = andBin(u, approximation[i][0:4])
            Vb = andBin(v, approximation[i][4:8])
            if xor(Ua[0],Ua[1],Ua[2],Ua[3],Vb[0],Vb[1],Vb[2],Vb[3]) == "0":
                L += 1
        bias = (L - 8)/16
        T *= abs(bias)
    return T
    

# main
if len(sys.argv) != 3 and len(sys.argv) != 4:
    print("Usage: python3 SPN.py sBox_file approximation_file [output_file]")
    sys.exit(1)

output_file = sys.argv[3] if len(sys.argv) == 4 else None

sBoxFile = sys.argv[1]	
approximationFile = sys.argv[2]

with open(sBoxFile, 'r') as f:
    sBox = f.read()

U = [intTo4BitBinary(i) for i in range(16)]
V = [hexToBinary(sBox[i]) for i in range(16)]

with open(approximationFile, 'r') as f:
    approximation = " ".join(f.read().split("\n"))
    approximation = approximation.split(" ")
    if(approximation[1] == "00" or approximation[5] == "00" or approximation[9] == "00" or approximation[11] == "00"):
        print("-1")
        exit(0)
    approximation = [hexToBinary(approximation[1]), hexToBinary(approximation[5]), hexToBinary(approximation[9]), hexToBinary(approximation[11])]

quality = calcQuality(U, V, approximation)
print(quality)
if output_file:
    with open(output_file, 'w') as f:
        f.write(str(quality))
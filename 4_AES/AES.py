import os
import sys

def hexToBinary(hex: str) -> str:
    hex = hex.replace(' ', '')
    return ''.join(format(int(hex[i:i+2], 16), '08b') for i in range(0, len(hex), 2))

def binaryToHex(binary: str) -> str:
    return ' '.join(''.join([hex(int(binary[i:i+4], 2))[2:],hex(int(binary[i+4:i+8], 2))[2:]]) for i in range(0, len(binary), 8))

dir = os.path.dirname(__file__)
sBoxFile = os.path.join(dir, 'SBox.txt')
sBoxInvFile = os.path.join(dir, 'SBoxInvers.txt')

with open(sBoxFile, 'r') as f:
    sBoxLines : list[str] = [hexToBinary(line) for line in f.read().split('\n')]
    # sBox[row][col]
    sBox : list[list[str]] = [[sBoxLine[i*8:(i+1)*8] for i in range(16)] for sBoxLine in sBoxLines]
    
with open(sBoxInvFile, 'r') as f:
    sBoxInvLines : list[str] = [hexToBinary(line) for line in f.read().split('\n')]
    # sBoxInv[row][col]
    sBoxInv : list[list[str]] = [[sBoxInvLine[i*8:(i+1)*8] for i in range(16)] for sBoxInvLine in sBoxInvLines]

# XOR two binary strings of the same length
def xor(a:str, b:str) -> str:
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

# convert a byte to a coordinate in the sBox
def byteToCoord(byte: str) -> tuple[int, int]:
    return (int(byte[0:4], 2), int(byte[4:8], 2))

# matrix[row][col]
matrixEncrypt = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
matrixDecrypt = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]

# adds 2 8-bit binary strings in galois field
def addGalois(a: str, b:str):
    return xor(a, b)

def doubleGalois(a: str):
    t = a[1:8] + "0"
    if a[0] == '1':
        t = xor(t, '00011011')
    return t

# multiplies 2 8-bit binary strings in galois field
def mulGalois(a: str, b:int):   
    listLeft = []
    listRight = []
    
    #init lists
    while b > 1:
        listLeft.append(b)
        listRight.append(a)
        b = b // 2
        a = doubleGalois(a)
    listLeft.append(b)
    listRight.append(a)
    
    #take sum if left not even
    sum = "00000000"
    for i in range(len(listRight)):
        if listLeft[i] % 2 != 0:
            sum = addGalois(sum,listRight[i])
    return sum

def matMulGalois(matrix: list[list[int]], col: list[str]) -> str:
    mixed = []
    for i in range(4):
        add0 = mulGalois(col[0],matrix[i][0])
        add1 = mulGalois(col[1],matrix[i][1])
        add2 = mulGalois(col[2],matrix[i][2])
        add3 = mulGalois(col[3],matrix[i][3])
        mixed.append(addGalois(add0,addGalois(add1,addGalois(add2,add3))))
    return mixed

# xor a 4x4 block with a 4x4 key
def addRoundKey(text: list[list[str]], key: list[list[str]]) -> list[list[str]]:
    for i in range(4):
        for j in range(4):
            text[i][j] = xor(text[i][j], key[i][j])
    return text

# substitute each byte with the corresponding byte in the sBox
def subBytes(text: list[list[str]]) -> list[list[str]]:
    for i in range(4):
        for j in range(4):
            x, y = byteToCoord(text[i][j])
            text[i][j] = sBox[x][y]
    return text

# substitute each byte with the corresponding byte in the sBoxInv
def invSubBytes(text: list[list[str]]) -> list[list[str]]:
    for i in range(4):
        for j in range(4):
            x, y = byteToCoord(text[i][j])
            text[i][j] = sBoxInv[x][y]
    return text

# shift each row to the left by i bytes, where i is the row number
def shiftRows(text: list[list[str]]) -> list[list[str]]:
    shifted = [[],[],[],[]]
    for i in range(4):
        for j in range(4):
            shifted[i].append(text[(j+i) % 4][j])
    return shifted

# shift each row to the right by i bytes, where i is the row number
def invShiftRows(text: list[list[str]]) -> list[list[str]]:
    shifted = [[],[],[],[]]
    for i in range(4):
        for j in range(4):
            shifted[i].append(text[(i-j) % 4][j])
    return shifted

def mixColumns(text: list[list[str]]) -> list[list[str]]:
    return [matMulGalois(matrixEncrypt, text[i]) for i in range(4)]

def invMixColumns(text: list[list[str]]) -> list[list[str]]:
    return [matMulGalois(matrixDecrypt, text[i]) for i in range(4)]

# convert to 4x4 block [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]
# list[col][row] to access
def convertToBlock(text: str) -> list[list[str]]:
    block: list[4][4] = []
    for i in range(4):
        block.append([])
        for j in range(4):
            block[i].append(text[((i*4+j)*8):((i*4+(j+1))*8)])
    return block

def blockToString(block: list[list[str]]) -> str:
    return ''.join(''.join(block[i][j] for j in range(4)) for i in range(4))

# text and key are 128-bit binary strings (16 byte)
def encrypt(text: str, key: list[str]) -> str:
    textBlock : list[list[str]] = convertToBlock(text)
    keyBlock : list[list[list[str]]] = [convertToBlock(line) for line in key]
    
    textBlock = addRoundKey(textBlock, keyBlock[0])
    for i in range(1, 10):
        textBlock = subBytes(textBlock)
        textBlock = shiftRows(textBlock)
        textBlock = mixColumns(textBlock)
        textBlock = addRoundKey(textBlock, keyBlock[i])
    textBlock = subBytes(textBlock)
    textBlock = shiftRows(textBlock)
    textBlock = addRoundKey(textBlock, keyBlock[10])
    return blockToString(textBlock)

def decrypt(text: str, key: str) -> str:
    textBlock : list[list[str]] = convertToBlock(text)
    keyBlock : list[list[list[str]]] = [convertToBlock(line) for line in key]
    
    textBlock = addRoundKey(textBlock, keyBlock[10])
    for i in range(9, 0, -1):
        textBlock = invSubBytes(textBlock)
        textBlock = invShiftRows(textBlock)
        textBlock = addRoundKey(textBlock, keyBlock[i])
        textBlock = invMixColumns(textBlock)
    textBlock = invSubBytes(textBlock)
    textBlock = invShiftRows(textBlock)
    textBlock = addRoundKey(textBlock, keyBlock[0])
    return blockToString(textBlock)
    

if len(sys.argv) != 5:
    print("Usage: python3 AES.py path-to-plaintext path-to-key path-to-output encrypt/decrypt")
    exit()

inputFile = sys.argv[1]
keyfile = sys.argv[2]
outputFile = sys.argv[3]
isEncrypt = sys.argv[4].lower() == 'encrypt'

with open(inputFile, 'r') as f:
    inputText = hexToBinary(f.read())

with open(keyfile, 'r') as f:
    key : list[str] = [hexToBinary(line) for line in f.read().split('\n')]

with open(outputFile, 'w') as f:
    if(isEncrypt):
        f.write(binaryToHex(encrypt(inputText, key)))
    else:
        f.write(binaryToHex(decrypt(inputText, key)))
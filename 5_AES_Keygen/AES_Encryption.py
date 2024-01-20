import os
import sys
import re

# convert a hex string to a binary string
def hexToBinary(hex: str) -> str:
    hex = re.sub(r"[^a-f0-9]", '', hex)
    return ''.join(format(int(hex[i:i+2], 16), '08b') for i in range(0, len(hex), 2))

# convert a binary string to a hex string
def binaryToHex(binary: str) -> str:
    return ' '.join(''.join([hex(int(binary[i:i+4], 2))[2:],hex(int(binary[i+4:i+8], 2))[2:]]) for i in range(0, len(binary), 8))

# get the sBox and sBoxInv from the files

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

# doubles an 8-bit binary string in galois field
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

# matrix multiplication in galois field
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

# mix the columns of the block
def mixColumns(text: list[list[str]]) -> list[list[str]]:
    return [matMulGalois(matrixEncrypt, text[i]) for i in range(4)]

# inverse mix the columns of the block
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

# convert a 4x4 block to a string
def blockToString(block: list[list[str]]) -> str:
    return ''.join(''.join(block[i][j] for j in range(4)) for i in range(4))

rconTable = ['00000001','00000010','00000100','00001000','00010000','00100000','01000000','10000000','00011011','00110110']

# generate key array from key
def rcon(i):
    return rconTable[i-1] + '00000000'+'00000000'+'00000000'

# SubWord(b0,b1,b2,b3) = (S(b0),S(b1),S(b2),S(b3))
def subWord(word):
    bytes  = [word[i:i+8] for i in range(0, len(word), 8)]
    newWordArr = []
    for i in range(4):
        x, y = byteToCoord(bytes[i])
        newWordArr.append(sBox[x][y])
    return ''.join(newWordArr)

# RotWord(b0,b1,b2,b3) = (b1,b2,b3,b0)
def rotWord(word):
    return word[8:32] + word[0:8]

# assume key is 128-bit binary string (4 32bit words)
def keyExpansion(key: str) -> list[str]:
    words = [key[i:i+32] for i in range(0, len(key), 32)] # K[0], K[1], K[2], K[3]
    for i in range(4, 44):
        if(i % 4 == 0):
            word_i = xor(subWord(rotWord(words[i-1])),xor(words[i-4], rcon(i//4)))
        else:
            word_i = xor(words[i-4],words[i-1])
        words.append(word_i)
    keys = [''.join(words[i:i+4]) for i in range(0, len(words), 4)]
    return keys

# encrypts 128-bit binary strings (both text and key are 128-bit) (16 byte)
def encrypt(text: str, key: str) -> str:
    textBlock : list[list[str]] = convertToBlock(text)
    keyBlock : list[list[list[str]]] = [convertToBlock(roundKey) for roundKey in keyExpansion(key)]
    
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

# decrypts 128-bit binary strings (both text and key are 128-bit) (16 byte)
def decrypt(text: str, key: str) -> str:
    textBlock : list[list[str]] = convertToBlock(text)
    keyBlock : list[list[list[str]]] = [convertToBlock(roundKey) for roundKey in keyExpansion(key)]
    
    textBlock = addRoundKey(textBlock, keyBlock[10])
    for i in range(9, 0, -1):
        textBlock = invShiftRows(textBlock)
        textBlock = invSubBytes(textBlock)
        textBlock = addRoundKey(textBlock, keyBlock[i])
        textBlock = invMixColumns(textBlock)
    textBlock = invShiftRows(textBlock)
    textBlock = invSubBytes(textBlock)
    textBlock = addRoundKey(textBlock, keyBlock[0])
    return blockToString(textBlock)

# XOR two binary strings of the same length
def xor(a:str, b:str) -> str:
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

# any encryption algorithm
def blackBoxEncrypt(plaintext, key):
    return encrypt(plaintext, key)

# any decryption algorithm
def blackBoxDecrypt(ciphertext, key):
    return decrypt(ciphertext, key)

# convert a counter to a binary string of a given length
def counterToBinary(counter:int, keyLength:int) -> str:
    return format(counter, '0'+str(keyLength)+'b')

# pad a plaintext to a multiple of a given key length
def pad(plaintext:str, keyLength:int) -> str:
    if len(plaintext) % keyLength == 0:
        return plaintext
    return plaintext + '0'*(keyLength - len(plaintext) % keyLength)

# split a string into blocks of a given length
def toBlocks(text:str, keyLength:int) -> list:
    return [text[i:i+keyLength] for i in range(0, len(text), keyLength)]

# encrypt a plaintext using the ECB mode
def encryptECB(plaintext:str, key:str)-> str:
    paddedText = pad(plaintext, len(key))
    cipherText = ""
    for block in toBlocks(paddedText, len(key)):
        cipherText += blackBoxEncrypt(block, key)
    return cipherText

# encrypt a plaintext using the CBC mode
def encryptCBC(plaintext:str, initVec:str, key:str)-> str:
    paddedText = pad(plaintext, len(key))
    cipherText = ""
    for block in toBlocks(paddedText, len(key)):
        bitsToEncrypt = xor(block, initVec)
        encryptedBits = blackBoxEncrypt(bitsToEncrypt, key)
        cipherText += encryptedBits
        initVec = encryptedBits
    return cipherText

# encrypt a plaintext using the OFB mode
def encryptOFB(plaintext:str, initVec:str, key:str)-> str:
    cipherText = ""
    for block in toBlocks(plaintext, len(key)):
        initVec = blackBoxEncrypt(initVec, key)
        cipherText += xor(block, initVec)
    return cipherText

# encrypt a plaintext using the COUNTER mode
def encryptCounter(plaintext:str, initVec:str, key:str)-> str:
    cipherText = ""
    for i,block in enumerate(toBlocks(plaintext, len(key))):
        tempVec = xor(initVec, counterToBinary(i, len(key)))
        encryptedVec = blackBoxEncrypt(tempVec, key)
        cipherText += xor(block, encryptedVec)
    return cipherText
        
# decrypt a ciphertext using the ECB mode
def decryptECB(ciphertext:str, key:str)-> bytes:
    plainText = ""
    for block in toBlocks(ciphertext, len(key)):
        plainText += blackBoxDecrypt(block, key)
    return plainText

# decrypt a ciphertext using the CBC mode
def decryptCBC(ciphertext:str, initVec:str, key:str)-> bytes:
    plainText = ""
    for block in toBlocks(ciphertext, len(key)):
        decryptedBits = blackBoxDecrypt(block, key)
        plainText += xor(decryptedBits, initVec)
        initVec = block
    return plainText

# decrypt a ciphertext using the OFB mode
def decryptOFB(ciphertext:str, initVec:str, key:str)-> bytes:
    return encryptOFB(ciphertext, initVec, key)

# decrypt a ciphertext using the COUNTER mode
def decryptCounter(ciphertext:str, initVec:str, key:str)-> bytes:
    return encryptCounter(ciphertext, initVec, key)

# convert a text to a binary string
def textToBinary(text:str) -> str:
    return ''.join(format(i, '08b') for i in bytearray(text, encoding ='utf-8'))

# convert a binary string to a text
def binaryToText(binary:str) -> str:
    intArray = [int(binary[i:i+8], 2) for i in range(0, len(binary), 8)]
    byteArray = bytearray(intArray)
    return str(byteArray, encoding ='utf-8')

# main
if len(sys.argv) != 5 and len(sys.argv) != 6:
    print("Usage: python3 AES_Encryption.py <mode> <input file> <key file> <output file> <optional: initVec file>")
    sys.exit(1)

mode = sys.argv[1].upper() # ECB, CBC, OFB, CTR

if len(sys.argv) != 6 and mode != 'ECB':
    print("Initvector file required for mode " + mode)
    sys.exit(1)
    
inputFile = sys.argv[2]
keyFile = sys.argv[3]
outputFile = sys.argv[4]
initVecFile = sys.argv[5] if len(sys.argv) == 6 else ""

with open(inputFile, 'r') as f:
    inputText = hexToBinary(f.read())

with open(keyFile, 'r') as f:
    key = hexToBinary(f.read())

with open(outputFile, 'w') as f:
    if mode == 'ECB':
        f.write(binaryToHex(encryptECB(inputText, key)))
    elif mode == 'CBC':
        with open(initVecFile, 'r') as f2:
            initVec = hexToBinary(f2.read())
        f.write(binaryToHex(encryptCBC(inputText, initVec, key)))
    elif mode == 'OFB':
        with open(initVecFile, 'r') as f2:
            initVec = hexToBinary(f2.read())
        f.write(binaryToHex(encryptOFB(inputText, initVec, key)))
    elif mode == 'CTR':
        with open(initVecFile, 'r') as f2:
            initVec = hexToBinary(f2.read())
        f.write(binaryToHex(encryptCounter(inputText, initVec, key)))
    else:
        print("Invalid mode")
        sys.exit(1)
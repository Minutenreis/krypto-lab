import sys

# XOR two binary strings of the same length
def xor(a:str, b:str) -> str:
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

# any encryption algorithm
def blackBoxEncrypt(plaintext, key):
    return xor(plaintext, key)

# any decryption algorithm
def blackBoxDecrypt(ciphertext, key):
    return xor(ciphertext, key)

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

def textToBinary(text:str) -> str:
    return ''.join(format(i, '08b') for i in bytearray(text, encoding ='utf-8'))

def binaryToText(binary:str) -> str:
    intArray = [int(binary[i:i+8], 2) for i in range(0, len(binary), 8)]
    byteArray = bytearray(intArray)
    return str(byteArray, encoding ='utf-8')


plainText = "Hellö World!"
bytes = textToBinary(plainText)
print(plainText)
print(bytes)
# mode = sys.argv[1].upper() # ECB, CBC, OFB, COUNTER
# keyLength = int(sys.argv[2]) # 128, 192, 256

mode = "CTR"
encrypt = True
key = '10101010'
nullVec= '0'*len(key)
initVec = '11111111'
ciphertext = ""
decipheredText = ""

if mode == "ECB":
    ciphertext = encryptECB(bytes, key)
    decipheredText = decryptECB(ciphertext, key)
elif mode == "CBC":
    ciphertext = encryptCBC(bytes, nullVec, key)
    decipheredText = decryptCBC(ciphertext, nullVec, key)
elif mode == "OFB":
    ciphertext = encryptOFB(bytes, initVec, key)
    decipheredText = decryptOFB(ciphertext, initVec, key)
elif mode == "CTR":
    ciphertext = encryptCounter(bytes, nullVec, key)
    decipheredText = decryptCounter(ciphertext, nullVec, key)
print(ciphertext)
print(decipheredText)
print(binaryToText(decipheredText))

import sys

def xor(a:str, b:str) -> str:
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

def blackBoxEncrypt(plaintext, key):
    return xor(plaintext, key)

def blackBoxDecrypt(ciphertext, key):
    return xor(ciphertext, key)

def pad(plaintext:str, keyLength:int) -> str:
    if len(plaintext) % keyLength == 0:
        return plaintext
    return plaintext + '0'*(keyLength - len(plaintext) % keyLength)

def encryptECB(plaintext:str, key:str)-> str:
    paddedText = pad(plaintext, len(key))
    cipherText = ""
    for i in range(0, len(paddedText), len(key)):
        cipherText += blackBoxEncrypt(paddedText[i:i+len(key)], key)
    return cipherText

def encryptCBC(plaintext:str, initVec:str, key:str)-> str:
    paddedText = pad(plaintext, len(key))
    cipherText = ""
    for i in range(0, len(paddedText), len(key)):
        bitsToEncrypt = xor(paddedText[i:i+len(key)], initVec)
        encryptedBits = blackBoxEncrypt(bitsToEncrypt, key)
        cipherText += encryptedBits
        initVec = encryptedBits
    return cipherText

def encryptOFB(plaintext:str, initVec:str, key:str)-> str:
    pass

def encryptCounter(plaintext:str, initVec:str, key:str)-> str:
    pass

def decryptECB(ciphertext:str, key:str)-> bytes:
    plainText = ""
    for i in range(0, len(ciphertext), len(key)):
        plainText += blackBoxDecrypt(ciphertext[i:i+len(key)], key)
    return plainText

def decryptCBC(ciphertext:str, initVec:str, key:str)-> bytes:
    plainText = ""
    for i in range(0, len(ciphertext), len(key)):
        decryptedBits = blackBoxDecrypt(ciphertext[i:i+len(key)], key)
        plainText += xor(decryptedBits, initVec)
        initVec = ciphertext[i:i+len(key)]
    return plainText

def decryptOFB(ciphertext:str, initVec:str, key:str)-> bytes:
    pass

def decryptCounter(ciphertext:str, initVec:str, key:str)-> bytes:
    pass

def textToBinary(text:str) -> str:
    return ''.join(format(i, '08b') for i in bytearray(text, encoding ='utf-8'))

def binaryToText(binary:str) -> str:
    intArray = [int(binary[i:i+8], 2) for i in range(0, len(binary), 8)]
    byteArray = bytearray(intArray)
    return str(byteArray, encoding ='utf-8')



plaintext = "Hellö Wörld!"
bytes = textToBinary(plaintext)
print(bytes)
# mode = sys.argv[1].upper() # ECB, CBC, OFB, COUNTER
# keyLength = int(sys.argv[2]) # 128, 192, 256

mode = "CBC"
encrypt = True
key = '10101010'
initVec= '0'*len(key)

if mode == "ECB":
    ciphertext = encryptECB(bytes, key)
    print(ciphertext)
    plaintext = decryptECB(ciphertext, key)
    print(plaintext)
    print(binaryToText(plaintext))
elif mode == "CBC":
    ciphertext = encryptCBC(bytes, initVec, key)
    print(ciphertext)
    plaintext = decryptCBC(ciphertext, initVec, key)
    print(plaintext)
    print(binaryToText(plaintext))
elif mode == "OFB":
    ciphertext = encryptOFB(bytes, initVec, key)
    print(ciphertext)
    plaintext = decryptOFB(ciphertext, initVec, key)
    print(plaintext)
    print(binaryToText(plaintext))
elif mode == "COUNTER":
    ciphertext = encryptCounter(bytes, initVec, key)
    print(ciphertext)
    plaintext = decryptCounter(ciphertext, initVec, key)
    print(plaintext)
    print(binaryToText(plaintext))
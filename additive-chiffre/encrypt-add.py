import sys
import os

# Shifts a character by a given key e [-26,26]
def shift(charAscii, key):
    newChar = charAscii + key
    if(newChar > 90):
        newChar = newChar - 26
    elif(newChar < 65):
        newChar = newChar + 26
    return chr(newChar)
    

# Encrypts a string with a given key e [-26,26]
def encrypt(str, key):
    cryptText = ""
    for char in str:
        charAscii = ord(char)
        cryptChar = char
        if(charAscii >= 65 and charAscii <= 90):
            cryptChar = shift(charAscii, key)
        cryptText += cryptChar
    return cryptText


        

if(len(sys.argv) != 4):
    print("Usage: python3 encrypt-add.py <path-to-plaintext> <key> <path-to-output>")
    exit()

dirname = os.path.dirname(__file__)

plaintextfile = os.path.join(dirname,sys.argv[1])
key = int(sys.argv[2])
ciphertextfile = os.path.join(dirname,sys.argv[3])

with open(plaintextfile, "r") as plaintextFile:
    plaintext = plaintextFile.read()
    crypttext = encrypt(plaintext, key)
    with open(ciphertextfile, "w") as cyphertextFile:
        cyphertextFile.write(crypttext)
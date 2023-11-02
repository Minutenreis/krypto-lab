import sys

# Shifts a character by a given key e [-26,26]
def shift(charAscii, key):
    newChar = charAscii + key
    if(newChar > 90):
        newChar = newChar - 26
    elif(newChar < 65):
        newChar = newChar + 26
    return chr(newChar)
    

# Encrypts a char e [A,Z] with a given key e [-26,26]
def encryptChar(char, key):
    return shift(ord(char), key)

# Encrypts a string with a given viginere key as number e [-26,26] Array
def encrypt(str, key):
    cryptText = ""
    i = 0
    for char in str:
        if(ord(char) < 65 or ord(char) > 90):
            cryptText += char
        else:
            cryptText += encryptChar(char, key[i])
            i = (i + 1) % len(key)
    return cryptText;

#convert string to number array
def stringToNumberArray(str):
    numberArray = []
    for char in str:
        numberArray.append(ord(char) - 65)
    return numberArray

if(len(sys.argv) != 4):
    print("Usage: python3 encrypt-add.py path-to-plaintext key path-to-output")
    exit()

plaintextfile = sys.argv[1]
key = stringToNumberArray(sys.argv[2])
ciphertextfile = sys.argv[3]

with open(plaintextfile, "r") as plaintextFile:
    plaintext = plaintextFile.read()
    crypttext = encrypt(plaintext, key)
    with open(ciphertextfile, "w") as cyphertextFile:
        cyphertextFile.write(crypttext)
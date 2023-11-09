import sys

# Shifts a character e [A-Z] by a given key
def shift(charAscii, key):
    return chr((charAscii -65 + key)%26 + 65)

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
    print("Usage: python3 encrypt-add.py path-to-plaintext key path-to-output")
    exit()


plaintextfile = sys.argv[1]
key = int(sys.argv[2])
ciphertextfile = sys.argv[3]

with open(plaintextfile, "r") as plaintextFile:
    plaintext = plaintextFile.read()
    crypttext = encrypt(plaintext, key)
    
    with open(ciphertextfile, "w") as cyphertextFile:
        cyphertextFile.write(crypttext)
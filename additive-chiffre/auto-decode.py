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
def decrypt(str, key):
    cryptText = ""
    for char in str:
        charAscii = ord(char)
        cryptChar = char
        if(charAscii >= 65 and charAscii <= 90):
            cryptChar = shift(charAscii, -key) # negative key for decryption
        cryptText += cryptChar
    return cryptText

def getMostCommonChar(str):
    return max(set(str), key = str.count)

if(len(sys.argv) != 3 and len(sys.argv) != 2):
    print("Usage: python3 auto-decode.py <path-to-crypttext> <optional-path-to-output>")
    exit()

dirname = os.path.dirname(__file__)

crypttextfile = os.path.join(dirname,sys.argv[1])
if(len(sys.argv) == 3):
    plaintextfile = os.path.join(dirname,sys.argv[2])
else:
    plaintextfile = os.path.join(dirname,"output.txt")

with open(crypttextfile, "r") as crypttextFile:
    crypttext = crypttextFile.read()
    mostCommonChar = getMostCommonChar(crypttext)
    key = ord(mostCommonChar) - ord('E') #assume E is most common in German
    plaintext = decrypt(crypttext, key)
    with open(plaintextfile, "w") as plaintextFile:
        plaintextFile.write(str(key)+"\n"+plaintext)
    
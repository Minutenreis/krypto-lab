import sys

# Shifts a character e [A-Z] by a given key
def shift(charAscii, key):
    return chr((charAscii -65 + key)%26 + 65)

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

# Decrypts a string with guessing the key
def autoDecodeAdd(str) -> (int, str):
    mostCommonChar = getMostCommonChar(str)
    key = (ord(mostCommonChar) - ord('E'))%26 #assume E is most common in German
    return (key, decrypt(str, key))

# get the character that occurs most often in a string
def getMostCommonChar(str):
    return max(set(str), key = str.count)

# main
if(len(sys.argv) != 3 and len(sys.argv) != 2):
    print("Usage: python3 auto-decode-add.py path-to-crypttext [path-to-output]")
    exit()

crypttextfile = sys.argv[1]
if(len(sys.argv) == 3):
    plaintextfile = sys.argv[2]
else:
    plaintextfile = "output.txt"

with open(crypttextfile, "r") as crypttextFile:
    crypttext = crypttextFile.read()
    (key, plaintext) = autoDecodeAdd(crypttext)

with open(plaintextfile, "w") as plaintextFile:
        plaintextFile.write(str(key)+"\n"+plaintext)
    
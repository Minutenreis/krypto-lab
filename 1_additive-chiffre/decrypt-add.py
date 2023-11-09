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


        

if(len(sys.argv) != 4):
    print("Usage: python3 decrypt-add.py path-to-crypttext key path-to-output")
    exit()


crypttextfile = sys.argv[1]
key = int(sys.argv[2])
plaintextfile = sys.argv[3]

with open(crypttextfile, "r") as crypttextFile:
    crypttext = crypttextFile.read()
    plaintext = decrypt(crypttext, key)
    
    with open(plaintextfile, "w") as plaintextFile:
        plaintextFile.write(plaintext)
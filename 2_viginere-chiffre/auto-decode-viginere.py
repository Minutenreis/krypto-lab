import sys
import re


# Shifts a character e [A-Z] by a given key
def shift(charAscii, key):
    return chr((charAscii -65 + key)%26 + 65)


# Encrypts a char e [A,Z] with a given key e [-26,26]
def encryptChar(char, key):
    return shift(ord(char), key)


# Encrypts a string with a given viginere key as number e [-26,26] Array
def decrypt(str, key):
    cryptText = ""
    i = 0
    for char in str:
        if ord(char) < 65 or ord(char) > 90:
            cryptText += char
        else:
            cryptText += encryptChar(char, -key[i])
            i = (i + 1) % len(key)
    return cryptText


def IC(str):
    n = len(str)
    # count occurences of each character
    H = {}
    for char in str:
        H[char] = H.get(char, 0) + 1
    
    # calculate and return index of coincidence
    return sum([H[chr] * (H[chr] - 1) for chr in H])/ (n * (n - 1))


def getCoincidenceIndex(str, keyLength):
    # split string into substrings
    subStrings = [str[i::keyLength] for i in range(keyLength)]

    # calculate coincidence index for each substring
    coincidenceIndexOfSubstrings = [IC(subString) for subString in subStrings]
    
    # calculate and return average coincidence index
    return sum(coincidenceIndexOfSubstrings) / len(coincidenceIndexOfSubstrings)


# get Key Length by calculating the coincidence index
def getKeyLength(str):
    possibleKeyLenghts = range(1, 101)

    # calculate coincidence index for each possible key length
    coincidenceIndex = [getCoincidenceIndex(str, keyLength) for keyLength in possibleKeyLenghts]
    maxIndex = max(coincidenceIndex)

    # find the most likely key length (minimum length within 20% of maxIndex)
    probableMinimumLength = [
        keyLength
        for keyLength in possibleKeyLenghts
        if coincidenceIndex[keyLength - 1] >= 0.80 * maxIndex
    ][0]
    return probableMinimumLength

def getMostCommonChar(str):
    return max(set(str), key = str.count)


# tries to guess the most likely key
def getMostLikelyKey(str):
    # clean of non [A-Z] charcters
    sanitizedStr = re.sub("[^A-Z]", "", str)
    
    keyLength = getKeyLength(sanitizedStr)
    subStrings = [sanitizedStr[i::keyLength] for i in range(keyLength)]
    
    # get key for all subStrings
    key = []
    for subString in subStrings:
        mostCommonChar = getMostCommonChar(subString)
        key.append((ord(mostCommonChar) - ord('E'))%26) #assume E is most common in each Substring
    return key


# converts number[] to str (0-25) -> (A-Z)
def numberArrayToString(numberArray):
    str = ""
    for number in numberArray:
        str += chr(number + 65)
    return str


if len(sys.argv) != 3:
    print("Usage: python3 auto-decode-viginere.py path-to-crypttext path-to-output")
    exit()


crypttextfile = sys.argv[1]
plaintextfile = sys.argv[2]

with open(crypttextfile, "r") as crypttextFile:
    crypttext = crypttextFile.read()
    key = getMostLikelyKey(crypttext)
    plaintext = decrypt(crypttext, key)
    
    with open(plaintextfile, "w") as plaintextFile:
        plaintextFile.write(numberArrayToString(key) + "\n" + plaintext)

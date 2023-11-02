import sys
import re


# Shifts a character by a given key e [-26,26]
def shift(charAscii, key):
    newChar = charAscii + key
    if newChar > 90:
        newChar = newChar - 26
    elif newChar < 65:
        newChar = newChar + 26
    return chr(newChar)


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
    dict = {}
    for char in str:
        dict[char] = dict.get(char, 0) + 1
    sum = 0
    for key in dict:
        sum += dict[key] * (dict[key] - 1)
    return sum / (n * (n - 1))


def getCoincidenceIndex(str, keyLength):
    subStrings = []
    coincidenceIndexOfSubstrings = []

    # split string into substrings
    for i in range(keyLength):
        subStrings.append("")
    for i in range(len(str)):
        subStrings[i % keyLength] += str[i]

    # calculate coincidence index for each substring
    for subString in subStrings:
        coincidenceIndexOfSubstrings.append(IC(subString))

    # calculate average coincidence index
    avgCoincidenceIndex = 0
    for coincidenceIndex in coincidenceIndexOfSubstrings:
        avgCoincidenceIndex += coincidenceIndex
    avgCoincidenceIndex /= len(coincidenceIndexOfSubstrings)
    return avgCoincidenceIndex


# get Key Length by calculating the coincidence index
def getKeyLength(str):
    possibleKeyLenghts = range(1, 101)

    # calculate coincidence index for each possible key length
    coincidenceIndex = []
    for keyLength in possibleKeyLenghts:
        coincidenceIndex.append(getCoincidenceIndex(str, keyLength))
    maxIndex = max(coincidenceIndex)

    # find the most likely key length (minimum length within 20% of maxIndex)
    probableMinimumLength = [
        idx
        for idx in possibleKeyLenghts
        if coincidenceIndex[idx - 1] >= 0.80 * maxIndex
    ][0]
    return probableMinimumLength

def getMostCommonChar(str):
    return max(set(str), key = str.count)


# tries to guess the most likely key
def getMostLikelyKey(str):
    sanitizedStr = re.sub("[^A-Z]", "", str)
    keyLength = getKeyLength(sanitizedStr)
    subStrings = []
    key = []
    for i in range(keyLength):
        subStrings.append("")
    for i in range(len(sanitizedStr)):
        subStrings[i % keyLength] += sanitizedStr[i]
    for subString in subStrings:
        mostCommonChar = getMostCommonChar(subString)
        key.append((ord(mostCommonChar) - ord('E'))%26) #assume E is most common in each Substring
    return key


# converts number[] to str
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

import sys
import random

# converts integer [0, 2^16-1] to hex string with 4 digits
def intTo4DigitHex(i: int) -> str:
    return format(i, '04x')

if len(sys.argv) != 3:
    print("Usage: python3 generateExampleTexts.py plaintext_file number_of_texts")
    sys.exit(1)

plaintextFile = sys.argv[1]
numTexts = int(sys.argv[2])

with open(plaintextFile, 'w') as f:
    for i in range(numTexts):
        rand4digitHex = random.randint(0,2**16-1)
        f.write(intTo4DigitHex(rand4digitHex) + "\n")
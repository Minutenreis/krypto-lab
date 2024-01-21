import AES_Encryption
import sys

# main (all the functions are in AES_Encryption.py)
if len(sys.argv) != 5 and len(sys.argv) != 6:
    print("Usage: python3 AES_Encryption.py mode input_file key_file output_file [initVec_file]")
    sys.exit(1)

mode = sys.argv[1].upper() # ECB, CBC, OFB, CTR

if mode not in ['ECB', 'CBC', 'OFB', 'CTR']:
    print("Unknown mode: " + mode)
    sys.exit(1)
elif len(sys.argv) != 6 and mode != 'ECB':
    print("Initvector file required for mode " + mode)
    sys.exit(1)
elif mode == 'ECB' and len(sys.argv) == 6:
    print("Initvector file not required for mode " + mode)
    sys.exit(1)
    
inputFile = sys.argv[2]
keyFile = sys.argv[3]
outputFile = sys.argv[4]
initVecFile = sys.argv[5] if len(sys.argv) == 6 else ""

with open(inputFile, 'r') as f:
    inputText = AES_Encryption.hexToBinary(f.read())

with open(keyFile, 'r') as f:
    key = AES_Encryption.hexToBinary(f.read())

with open(outputFile, 'w') as f:
    if(mode == 'ECB'):
        f.write(AES_Encryption.binaryToHex(AES_Encryption.decryptECB(inputText, key)))
    elif(mode == 'CBC'):
        with open(initVecFile, 'r') as f2:
            initVec = AES_Encryption.hexToBinary(f2.read())
        f.write(AES_Encryption.binaryToHex(AES_Encryption.decryptCBC(inputText, initVec, key)))
    elif(mode == 'OFB'):
        with open(initVecFile, 'r') as f2:
            initVec = AES_Encryption.hexToBinary(f2.read())
        f.write(AES_Encryption.binaryToHex(AES_Encryption.decryptOFB(inputText, initVec, key)))
    elif(mode == 'CTR'):
        with open(initVecFile, 'r') as f2:
            initVec = AES_Encryption.hexToBinary(f2.read())
        f.write(AES_Encryption.binaryToHex(AES_Encryption.decryptCounter(inputText, initVec, key)))
    else:
        print("Unknown mode: " + mode)
        sys.exit(1)
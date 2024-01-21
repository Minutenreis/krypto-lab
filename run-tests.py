import subprocess
import os

dir = os.path.dirname(__file__)

allFiles = [] # (name,dir,absolute-path)[]
for path, subdirs, files in os.walk(dir):
    for name in files:
        allFiles.append((name,path))

tests = [file for file in allFiles if str(file[0]).endswith(".test.py")]
tests.sort(key=lambda tup: int(os.path.basename(tup[1]).split("_")[0]))

for test in tests:
    os.chdir(test[1])
    print("testing",os.path.basename(test[1]))
    subprocess.call(["python3",test[0]])
    print()

os.chdir(dir)
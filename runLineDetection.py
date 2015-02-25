# runs LineDetection.py

import sys
from LineDetection import detectLines

inFile = sys.argv[1]
output = detectLines(inFile)
for i in output:
    print(i,end="")

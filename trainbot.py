#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'isPower' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY arr as parameter.
#
import math
def isPower(arr):
    # Write your code here
    out = []
    for i in arr:
        if i / (i/2*(math.sqrt(2))) == math.sqrt(2):
            out.append(1) 
        else:
            out.append(0)
    return out

if __name__ == '__main__':
    arr = [1,4,7,16,28,64,32]
    result = isPower(arr)

    print(result)
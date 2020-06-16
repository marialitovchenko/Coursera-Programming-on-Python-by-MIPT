"""
Draws stairs from # with number of steps given by user
"""
 
import sys
 
numb_steps = int(sys.argv[1])

for i in range(1, numb_steps + 1):
    oneStairStep = (" " * (numb_steps - i)) + ("#" * i)
    print(oneStairStep)

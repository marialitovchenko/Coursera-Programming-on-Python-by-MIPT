"""
Computes sum of numbers in the string given by user.
It's guarantied that there is no other symbols in the string except numbers and
that string isn't empty
"""

import sys

digit_string = sys.argv[1]

result = 0
for digit in digit_string:
    result += int(digit)

print(result)

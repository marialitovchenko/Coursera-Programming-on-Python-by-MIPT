"""
Save key - value pairs into the file storage.py. 
If one argument is given (--key) retrieve the pair from the file:
	storage.py --key key_name
If two arguments are given (--key, --val), put the pair into the file:
	storage.py --key key_name --val value
Several values can be assigned to one key
"""

import argparse # working with arguments from command line
import json # json format
import os
import tempfile

# specify the key and value arguments
parser = argparse.ArgumentParser()
parser.add_argument("--key", required = True, help = "Key")
parser.add_argument("--value", required = False, help = "Value")
# parse the arguments
args = parser.parse_args()

# key and values will be stored here
key_values = {}
# storage path
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
print(storage_path)

# open storage file, if it exists and read keys and values
if os.path.isfile(storage_path):
    with open(storage_path) as f:
        one_line = f.read()
        key_values = json.loads(one_line)

if args.value is None:
    if args.key in key_values:
        print(*key_values[args.key], sep = ", ")
    else:
        print('None')
        key_values[args.key] = []
else:
    if args.key in key_values:
        new_values = key_values[args.key]
        new_values.append(args.value)
        key_values.update({args.key : new_values })
    else:
        key_values[args.key] = [args.value, ]

# write to storage file
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
with open(storage_path, 'w') as file:
     file.write(json.dumps(key_values))

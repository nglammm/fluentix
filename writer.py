"""NAME: writer
DESCRIPTION: A package that reads/writes files.
VERSION: v0.0.1"""

import os
import interpreter

def check_path(path):
    """Checks whether current path's end point is a file"""
    if os.path.isdir(path):
        return 1 # is directory
    elif os.path.isfile(path):
        return 2 # is file
    else:
        return 0 # not exist

def write(string, path, mode):
    """Simply write a string into a specified file via path
- Usage:
writer: write: <value>; <path>; <mode>
-> Will write <value> to a new file in <path> via <mode>
- Modes:
1. "write": will delete file's past data and write a new one
2. "continuous": continues to write without deleting file's past data"""
    
    value = int(check_path(path))
    
    if value == 1:
        return None, interpreter.Error('Error', 'Path is a directory.')
    elif value == 0:
        return None, interpreter.Error('Error', 'Path is non-existed.')
    
    # Mode: write
    if mode == 'write':
        with open(path, 'w') as f:
            f.write(str(string))
        return None
    # Mode: continuous
    elif mode == 'continuous':
        with open(path, 'a') as f:
            f.write(str(string))
        return None
    
def read(path, mode):
    """Simply write a string into a specified file via path
- Usage:
a is writer: read: <path>; <mode>
-> Will read file's data inside <path> and return to a variable.
- Modes:
1. "read": reads current file.
2. "readall": read every line and stored in a list."""
    
    value = int(check_path(path))

    if value == 1:
        return None, interpreter.Error('Error', 'Path is a directory.')
    elif value == 0:
        return None, interpreter.Error('Error', 'Path is non-existed.')
    
    # Mode: read
    if mode == 'read':
        with open(path, 'r') as f:
            return f.read(), None
    # Mode: readall
    elif mode == 'readall':
        with open(path, 'r') as f:
            return f.read().split('\n'), None

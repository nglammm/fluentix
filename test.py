import sys

print("Enter multiple lines of input (Ctrl+D to end on Unix or Ctrl+Z on Windows):")

# Read all lines from stdin
input_lines = sys.stdin.read().strip().splitlines()

# Process the input
for line in input_lines:
    print("You entered:", line)
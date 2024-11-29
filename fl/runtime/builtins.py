import sys
def show(values: list):
    sys.stdout.write(" ".join(([value for value in values])))
    sys.stdout.write("\n")
    return None
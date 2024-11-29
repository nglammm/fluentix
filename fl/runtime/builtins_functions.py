import sys

def show(values: list, newline=True):
    def representation(value):
        if isinstance(value, bool):
            return "true" if value else "false"
        
        if isinstance(value, (list, tuple, set)):
            return f"[{'; '.join([representation(element) for element in value])}]"
        
        if value is None:
            return "null"
        
        return str(value)
    
    sys.stdout.write(" ".join([representation(value) for value in values]))
    if newline:
        sys.stdout.write("\n")

    return None

def ask(prompts: list):
    show(prompts, False)
    return sys.stdin.readline()[0:-1]
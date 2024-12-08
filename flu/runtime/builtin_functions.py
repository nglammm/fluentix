import sys
from ..errors import RuntimeResult
from .values import translate_python_to_fluentix
def show(arguments):
    sys.stdout.write(" ".join([translate_python_to_fluentix(argument).__repr__() for argument in arguments]))
    sys.stdout.write("\n")
    return RuntimeResult(None)
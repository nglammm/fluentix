from .frontend.lexer import tokenize
from .frontend.parser import Parser
from .runtime.interpreter import evaluate
from .runtime.values import Environment, NativeFunction
import flu.runtime.builtin_functions

def execute_code(code, extension):
    global_environment = Environment()
    global_environment.assign("show", NativeFunction("show", flu.runtime.builtin_functions.show), True)

    rt = tokenize(code, extension)
    if rt.error:
        rt.error.show_error()

    #print(f"Tokens: {rt.result}\n")

    parser = Parser(rt.result, extension)
    rt = parser.produce_ast()
    if rt.error:
        rt.error.show_error()
    
    #print(f"Tree: {rt.result}\n")

    rt = evaluate(rt.result, global_environment)
    if rt.error:
        rt.error.show_error()
    
    #print(f"Result: {rt.result}")
from .frontend.parser import Parser
from .runtime.interpreter import evaluate
from .runtime.values import *
from .frontend.lexer import tokenize
import asyncio

def execute_code(file):
    with open(file) as file:
        code = file.read()
    
    asyncio.run(fluentix(code))

async def fluentix(source):
    tokens = tokenize(source)
    parser = Parser(tokens)
    environment = Environment()

    program = parser.produce_ast()
    
    evaluate(program, environment)

if __name__ == "__main__":
    file = input("Which file do you want to run? ")
    execute_code(f"{file}.fluentix")
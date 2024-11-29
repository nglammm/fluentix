from __future__ import annotations
import sys
from typing import Literal
from .builtins_functions import *

# Environment
class Environment:
    def __init__(self, parent: Environment | None = None) -> None:
        self.parent = parent
        self.variables = {}
        self.constants = set()
        if not self.parent:
            self.declare_variable("show", NativeFunctionValue("show", show), True)
            self.declare_variable("ask", NativeFunctionValue("ask", ask), True)
            self.declare_variable("input", NativeFunctionValue("input", ask), True)
    
    def declare_variable(self, var_name: str, value: RuntimeValue, constant: bool) -> RuntimeValue:
        if var_name in self.variables:
            print(f"VariableError: '{var_name}' is already defined")
            sys.exit(1)
    
        self.variables.update({var_name: value})
        if constant:
            self.constants.add(var_name)
        return value
    
    def assign_variable(self, var_name: str, value: RuntimeValue) -> RuntimeValue:
        environment = self.resolve(var_name)

        if var_name in environment.constants:
            print(f"VariableError: Cannot update constant '{var_name}'")
            sys.exit(1)

        environment.variables[var_name] = value

        return value

    def lookup_variable(self, var_name: str) -> RuntimeValue:
        environment = self.resolve(var_name)
        return environment.variables[var_name]

    def resolve(self, var_name: str) -> Environment:
        if var_name in self.variables:
            return self
        
        if not self.parent:
            print(f"VariableError: Cannot resolve '{var_name}' because it does not exist.")
            sys.exit(1)
        
        return self.parent.resolve(var_name)

class ValueType:
    def __init__(self,
        type: Literal["null"]
        | Literal["number"]
        | Literal["boolean"]
        | Literal["string"]
        | Literal["array"]
        | Literal["native_function"]
    ) -> None:
        self.type = type

class FunctionCall:
    def __init__(self, arguments: list[RuntimeValue], environment: Environment) -> None:
        self.arguments = arguments
        self.environment = environment

class RuntimeValue:
    def __init__(self, type: ValueType) -> None:
        self.type = type

class NullValue(RuntimeValue):
    def __init__(self) -> None:
        super().__init__(ValueType("null"))
        self.value = "null"
    
    def __repr__(self) -> str:
        return "null"

class NumberValue(RuntimeValue):
    def __init__(self, value: int | float) -> None:
        super().__init__(ValueType("number"))
        self.value = value
    
    def __repr__(self) -> str:
        return str(self.value)

class BooleanValue(RuntimeValue):
    def __init__(self, value: Literal["true"] | Literal["false"]) -> None:
        super().__init__(ValueType("boolean"))
        self.value = value
    
    def __repr__(self) -> str:
        return self.value

class StringValue(RuntimeValue):
    def __init__(self, value: str):
        super().__init__(ValueType("string"))
        self.value = value
    
    def __repr__(self) -> str:
        return self.value

class ArrayValue(RuntimeValue):
    def __init__(self, value: list[RuntimeValue]):
        super().__init__(ValueType("array"))
        self.value = value
    
    def __repr__(self) -> str:
        return f"[{'; '.join([i.__repr__() for i in self.value])}]"

class NativeFunctionValue(RuntimeValue):
    def __init__(self, name: str, call: function) -> None:
        super().__init__(ValueType("native_function"))
        self.name = name
        self.call = call
    
    def __repr__(self) -> str:
        return f"(NATIVE FUNCTION: {self.name})"

def translate_boolean(boolean: BooleanValue) -> bool:
    if boolean.value == "true":
        return True
    
    if boolean.value == "false":
        return False

def create_number(number: float) -> NumberValue:
    return NumberValue(int(number) if number % 1 == 0 else number)
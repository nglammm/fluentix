from __future__ import annotations
from typing import Literal

class NodeType:
    def __init__(self, type: 
    
        # Statements
        Literal["Program"]
        | Literal["VariableDeclaration"]
        | Literal["AssignmentStatement"]

        # Expressions
        | Literal["NumericLiteral"]
        | Literal["BooleanLiteral"]
        | Literal["Identifier"]
        | Literal["NullLiteral"]
        | Literal["BinaryExpr"]
        | Literal["UnaryExpr"]
        | Literal["FetchExpr"]
        | Literal["CallExpr"]
        | Literal["MemberExpr"]
        | Literal["StringLiteral"]
        | Literal["ArrayLiteral"]
    ) -> None:
        self.type = type

class Statement:
    def __init__(self, kind: NodeType):
        self.kind = kind

class Program(Statement):
    def __init__(self, body: list[Statement]) -> None:
        super().__init__(NodeType("Program"))
        self.body = body
    
    def __repr__(self) -> str:
        string = "(PROGRAM {"
        for sub in self.body:
            string += f"\n    {sub.__repr__()}"
        
        string += "\n})"
        return string

class VariableDeclaration(Statement):
    def __init__(self, constant: bool, identifier: str, value: Expression) -> None:
        super().__init__(NodeType("VariableDeclaration"))
        self.constant = constant
        self.identifier = identifier
        self.value = value
    
    def __repr__(self) -> str:
        return f"(VARIABLE DECLARATION: {self.identifier} is {self.value.__repr__()}, also constant is {str(self.constant).lower()})"

class AssignmentStatement(Statement):
    def __init__(self, identifier: str, value: Expression) -> None:
        super().__init__(NodeType("AssignmentStatement"))
        self.identifier = identifier
        self.value = value
    
    def __repr__(self) -> str:
        return f"(ASSIGNMENT STATEMENT: {self.identifier} is {self.value.__repr__()})"

class Expression(Statement):
    def __init__(self, kind) -> None:
        super().__init__(kind)

class BinaryExpression(Expression):
    def __init__(self,
        left: Expression,
        right: Expression,
        operator: str
    ) -> None:
        super().__init__(NodeType("BinaryExpr"))
        self.left = left
        self.right = right
        self.operator = operator
    
    def __repr__(self) -> str:
        return f"(BINARY EXPRESSION: {self.left.__repr__()} {self.operator} {self.right.__repr__()})"

class UnaryExpression(Expression):
    def __init__(self, sign: str, expression: Expression) -> None:
        super().__init__(NodeType("UnaryExpr"))
        self.sign = sign
        self.expression = expression
    
    def __repr__(self) -> str:
        return f"(UNARY EXPRESSION: {self.sign}{self.expression.__repr__()})"

class FetchExpression(Expression):
    def __init__(self, fetched: Expression, index: Expression):
        super().__init__(NodeType("FetchExpr"))
        self.fetched = fetched
        self.index = index
    
    def __repr__(self) -> str:
        return f"(FETCH EXPRESSION: {self.fetched}[{self.index}])"

class CallExpression(Expression):
    def __init__(self, callee: Expression, arguments: list[Expression]):
        super().__init__(NodeType("CallExpr"))
        self.callee = callee
        self.arguments = arguments
    
    def __repr__(self) -> str:
        return f"(CALL EXPRESSION: {self.callee.__repr__()} with arguments [{'; '.join([arg.__repr__() for arg in self.arguments])}])"

class Identifier(Expression):
    def __init__(self, symbol) -> None:
        super().__init__(NodeType("Identifier"))
        self.symbol = symbol
    
    def __repr__(self) -> str:
        return f"(IDENTIFIER: {self.symbol})"

class NumericLiteral(Expression):
    def __init__(self, value: int | float) -> None:
        super().__init__(NodeType("NumericLiteral"))
        self.value = value
    
    def __repr__(self) -> str:
        return f"(NUMBER: {self.value})"

class BooleanLiteral(Expression):
    def __init__(self, value: Literal["true"] | Literal["false"]) -> None:
        super().__init__(NodeType("BooleanLiteral"))
        self.value = value
    
    def __repr__(self) -> str:
        return f"(BOOLEAN: {self.value})"

class NullLiteral(Expression):
    def __init__(self) -> None:
        super().__init__(NodeType("NullLiteral"))
        self.value = "no"
    
    def __repr__(self) -> str:
        return "(NO)"
    
class StringLiteral(Expression):
    def __init__(self, value: str) -> None:
        super().__init__(NodeType("StringLiteral"))
        self.value = value
    
    def __repr__(self) -> str:
        return f"(STRING: {self.value})"

class ArrayLiteral(Expression):
    def __init__(self, value: list[Expression]) -> None:
        super().__init__(NodeType("ArrayLiteral"))
        self.value = value
    
    def __repr__(self) -> str:
        return f"(ARRAY: [{'; '.join([i.__repr__() for i in self.value])}])"
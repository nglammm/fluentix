class NodeType:
    def __init__(self, type):
        self.type = type

class Statement:
    def __init__(self, kind):
        self.kind = kind

class Program(Statement):
    def __init__(self, body):
        super().__init__(NodeType("Program"))
        self.body = body

    def __repr__(self):
        return f"""(PROGRAM [
    {''';
    '''.join([statement.__repr__() for statement in self.body])}
])"""

class Expression(Statement):
    def __init__(self, kind):
        super().__init__(kind)

class BinaryExpression(Expression):
    def __init__(self, left, operator, right):
        super().__init__(NodeType("BinaryExpression"))
        self.left = left
        self.right = right
        self.operator = operator
    
    def __repr__(self):
        return f"(BINARY EXPRESSION {self.left} {self.operator} {self.right})"

class CallExpression(Expression):
    def __init__(self, callee, arguments):
        super().__init__(NodeType("CallExpression"))
        self.callee = callee
        self.arguments = arguments
    
    def __repr__(self):
        return f"(FUNCTION CALL {self.callee} with arguments [{'; '.join([argument.__repr__() for argument in self.arguments])}])"

class UnaryExpression(Expression):
    def __init__(self, sign, value):
        super().__init__(NodeType("UnaryExpression"))
        self.sign = sign
        self.value = value
    
    def __repr__(self):
        return f"(UNARY EXPRESSION {self.sign}{self.value})"

class Identifier(Expression):
    def __init__(self, symbol):
        super().__init__(NodeType("Identifier"))
        self.symbol = symbol
    
    def __repr__(self):
        return f"(IDENTIFIER {self.symbol})"

class NumberLiteral(Expression):
    def __init__(self, value):
        super().__init__(NodeType("NumberLiteral"))
        self.value = value
    
    def __repr__(self):
        return f"(NUMBER LITERAL {self.value})"

class BooleanLiteral(Expression):
    def __init__(self, value):
        super().__init__(NodeType("BooleanLiteral"))
        self.value = value
    
    def __repr__(self):
        return f"(BOOLEAN LITERAL {self.value})"

class TrueLiteral(BooleanLiteral):
    def __init__(self):
        super().__init__("true")

class FalseLiteral(BooleanLiteral):
    def __init__(self):
        super().__init__("false")

class NullLiteral(Expression):
    def __init__(self):
        super().__init__(NodeType("NullLiteral"))
    
    def __repr__(self):
        return f"(NULL LITERAL)"

class StringLiteral(Expression):
    def __init__(self, value):
        super().__init__(NodeType("StringLiteral"))
        self.value = value
    
    def __repr__(self):
        return f"(STRING LITERAL {self.value})"

class ArrayLiteral(Expression):
    def __init__(self, value):
        super().__init__(NodeType("ArrayLiteral"))
        self.value = value
    
    def __repr__(self):
        return f"(ARRAY LITERAL [{'; '.join([element.__repr__() for element in self.value])}])"

class AssignmentStatement(Statement):
    def __init__(self, identifier, value, constant=False):
        super().__init__(NodeType("AssignmentStatement"))
        self.identifier = identifier
        self.value = value
        self.constant = constant
    
    def __repr__(self):
        return f"(ASSIGNMENT STATEMENT {self.identifier} with value {self.value}, constant set to {str(self.constant).lower()})"

class UpdateStatement(Statement):
    def __init__(self, identifier, value):
        super().__init__(NodeType("UpdateStatement"))
        self.identifier = identifier
        self.value = value
    
    def __repr__(self):
        return f"(UPDATE STATEMENT {self.identifier} with value {self.value})"
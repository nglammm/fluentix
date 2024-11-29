from .abstract_syntax_tree import *
from .lexer import *

import sys

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
    
    def not_end(self) -> bool:
        if not self.tokens:
            return False
        
        return self.tokens[0].type.type not in END_TOKENS

    def at(self) -> Token:
        return self.tokens[0]
    
    def eat(self) -> Token:
        self.skip_tabs()
        if not self.tokens:
            return None

        return self.tokens.pop(0)
    
    def expect(self, *types: TokenType, error) -> Token:
        prev = self.eat()
        if not prev:
            print(f"SyntaxError: {error}")
            sys.exit(1)

        if prev.type.type not in [type.type for type in types]:
            print(f"SyntaxError: {error}, got '{prev.type.type}'")
            sys.exit(1)
        
        return prev

    def skip_tabs(self):
        while self.at().type.type == "Tab":
            self.tokens.pop(0)
        
    def produce_ast(self) -> Program:
        program = Program([])

        # Parse until EOF
        while True:
            if not self.tokens:
                break

            self.skip_tabs()
            if self.at().type.type == "EOF":
                break

            if self.at().type.type == "Newline":
                self.eat()
                continue

            while self.not_end():
                program.body += [self.parse_statement()]
        #print(program)
        return program

    def parse_statement(self) -> Statement:      
        self.skip_tabs()  
        if self.at().type.type in ("Let", "Variable"):
            return self.parse_variable_declaration()

        if self.at().type.type == "Constant":
            return self.parse_const_variable_declaration()
        
        if self.at().type.type == "Identifier":
            saved = self.eat()
            if self.at().type.type.lower() in KEYWORDS:
                return self.parse_assignment_statement(saved)
            
            self.tokens = [saved] + self.tokens

        return self.parse_expression()

    def parse_variable_declaration(self) -> VariableDeclaration:
        keyword = self.eat()
        identifier = self.expect(TokenType("Identifier"), error="Expected identifier").value

        if keyword.type.type == "Let":
            self.expect(TokenType("Be"), error="Expected 'be'")
        else:
            self.expect(TokenType("Is"), error="Expected 'is'")
        
        self.skip_tabs()
        if self.at().type.type in END_TOKENS:
            print("SyntaxError: Expected expression")
            sys.exit(1)

        expression = self.parse_expression()
        if self.at().type.type not in END_TOKENS:
            print(f"SyntaxError: Expected nothing after the expression, got {self.at()}")
            sys.exit(1)

        self.eat()
        return VariableDeclaration(False, identifier, expression)

    def parse_assignment_statement(self, identifier: str) -> AssignmentStatement:
        if self.at().type.type != "Is":
            print(f"SyntaxError: Expected 'is', got {self.at()}")
            sys.exit(1)

        self.eat()
        self.expect(TokenType("Now"), error="SyntaxError: Expected 'now'")

        self.skip_tabs()
        if self.at().type.type in END_TOKENS:
            print("SyntaxError: Expected expression")
            sys.exit(1)

        expression = self.parse_expression()

        if self.at().type.type not in END_TOKENS:
            print(f"SyntaxError: Expected nothing after the expression, got {self.at()}")
            sys.exit(1)

        self.eat()
        return AssignmentStatement(identifier, expression)

    def parse_const_variable_declaration(self) -> VariableDeclaration:
        self.eat()
        identifier = self.expect(TokenType("Identifier"), error="Expected identifier").value

        self.expect(TokenType("Is"), error="Expected 'is'")

        self.skip_tabs()
        if self.at().type.type in END_TOKENS:
            print("SyntaxError: Expected expression")
            sys.exit(1)

        expression = self.parse_expression()

        if self.at().type.type not in END_TOKENS:
            print(f"SyntaxError: Expected nothing after the expression, got {self.at()}")
            sys.exit(1)

        self.eat()
        return VariableDeclaration(True, identifier, expression)

    def parse_expression(self) -> Expression:
        self.skip_tabs()
        return self.parse_comparison_expression()

    def parse_comparison_expression(self) -> Expression:
        left = self.parse_additive_expression()
        self.skip_tabs()
        while self.at().value in ("=", "!=", ">", "<", ">=", "<=") and self.at().type.type == "BinaryOperator":
            operator = self.eat().value

            right = self.parse_additive_expression()
            left = BinaryExpression(left, right, operator)
        
        return left

    def parse_additive_expression(self) -> Expression:
        left = self.parse_multiplicative_expression()
        self.skip_tabs()
        while self.at().value in ("+", "-") and self.at().type.type == "BinaryOperator":
            operator = self.eat().value

            right = self.parse_multiplicative_expression()
            left = BinaryExpression(left, right, operator)
        
        return left
    
    def parse_multiplicative_expression(self) -> Expression:
        left = self.parse_call_expression()
        self.skip_tabs()
        while self.at().value in ("*", "/") and self.at().type.type == "BinaryOperator":
            operator = self.eat().value

            right = self.parse_call_expression()
            left = BinaryExpression(left, right, operator)
        
        return left

    def parse_elements_in_array(self, inside) -> list[Expression]:
        # seperate elements using ;
        elements = []
        element = []
        stack = []
        for token in inside:
            # newline
            if token.type.type == "Newline":
                continue

            # check for brackets
            if token.type.type in ("OpenBracket", "OpenParen"):
                stack += [token.type.type]
            elif token.type.type == "CloseParen":
                if "OpenParen" not in stack:
                    print("SyntaxError: Unexpected ')'")
                    sys.exit(1)
                
                if stack[0] != "OpenParen":
                    print("SyntaxError: Unexpected ')'")
                    sys.exit(1)

                stack.pop(0)
            elif token.type.type == "CloseBracket":
                if "OpenBracket" not in stack:
                    print("SyntaxError: Unexpected ']'")
                    sys.exit(1)
                
                if stack[0] != "OpenBracket":
                    print("SyntaxError: Unexpected ']'")
                    sys.exit(1)

                stack.pop(0)
            
            # check for semicolon
            if token.type.type == "Semi" and not stack:
                if element:
                    elements += [element]
                    element = []
            else:
                element += [token]
            
        if element:
            elements += [element]

        new = []
        for element in elements:
            parser = Parser(element + [create_token(TokenType("EOF"), "EOF")])
            new += [parser.parse_expression()]
        
        return ArrayLiteral(new)

    def parse_call_expression(self) -> Expression:
        left = self.parse_fetch_expression()
        if self.at().type.type == "Colon":
            self.eat()
            # PARSE ALL SHIT ARGUMENTS YEAH GUYS
            inside = []
            stack = []
            while self.not_end():
                if self.at().type.type in ("OpenBracket", "OpenParen"):
                    stack += [self.at().type.type]
                elif self.at().type.type == "CloseParen":
                    if not stack:
                        break
                    
                    if stack[0] != "OpenParen":
                        print("SyntaxError: Unexpected ')'")
                        sys.exit(1)

                    stack.pop(0)
                elif self.at().type.type == "CloseBracket":
                    if not stack:
                        break
                    
                    if stack[0] != "OpenBracket":
                        print("SyntaxError: Unexpected ']'")
                        sys.exit(1)

                    stack.pop(0)
                
                inside += [self.eat()]
            
            # seperate into arguments
            arguments = self.parse_elements_in_array(inside)
            left = CallExpression(left, arguments.value)

        return left

    def parse_fetch_expression(self) -> Expression:
        left = self.parse_unary_expression()
        while self.at().type.type == "OpenBracket":
            self.eat()
            inside = []
            stack = []
            while (self.at().type.type != "CloseBracket" or stack) and self.at().type.type != "EOF":
                token = self.eat()

                # check for brackets
                if token.type.type in ("OpenBracket", "OpenParen"):
                    stack += [token.type.type]
                elif token.type.type == "CloseParen":
                    if "OpenParen" not in stack:
                        print("SyntaxError: Unexpected ')'")
                        sys.exit(1)
                    
                    if stack[0] != "OpenParen":
                        print("SyntaxError: Unexpected ')'")
                        sys.exit(1)

                    stack.pop(0)
                elif token.type.type == "CloseBracket":
                    if "OpenBracket" not in stack:
                        print("SyntaxError: Unexpected ']'")
                        sys.exit(1)
                    
                    if stack[0] != "OpenBracket":
                        print("SyntaxError: Unexpected ']'")
                        sys.exit(1)

                    stack.pop(0)
                
                inside += [token]
            
            if self.at().type.type == "EOF":
                print("SyntaxError: Expected ']'")
                sys.exit(1)

            self.eat()
            parser = Parser(inside + [create_token(TokenType("EOF"), "EOF")])
            index = parser.parse_expression()
            left = FetchExpression(left, index)
        
        return left

    def parse_unary_expression(self) -> Expression:
        sign = ""
        while self.at().type.type == "BinaryOperator" and self.at().value in ("+", "-"):
            if not sign:
                sign = self.eat().value
            elif sign == "-":
                sign = "+" if sign == "-" else "-"
        
        if not sign:
            return self.parse_primary_expression()
        
        return UnaryExpression(sign, self.parse_primary_expression())

    def parse_primary_expression(self) -> Expression:
        self.skip_tabs()
        tt = self.at().type.type

        if self.tokens[1].type.type == "EOF" and tt not in ("Identifier", "Null", "Number", "True", "False", "String", "Create"):
            print(f"SyntaxError: Unexpected token found during parsing: '{self.at()}'")
            sys.exit(1)

        if tt == "Identifier":
            identifier = self.eat().value
            return Identifier(identifier)
        
        if tt == "Null":
            self.eat()
            return NullLiteral()

        if tt == "Number":
            value = float(self.eat().value)
            return NumericLiteral(value)
        
        if tt == "True":
            self.eat()
            return BooleanLiteral("true")

        if tt == "False":
            self.eat()
            return BooleanLiteral("false")
        
        if tt == "String":
            string = self.eat().value
            return StringLiteral(string)

        if tt == "OpenParen":
            self.eat()
            value = self.parse_expression()
            self.expect(TokenType("CloseParen"), error="Expecting ')'")
            return value

        # array
        if tt == "OpenBracket":
            self.eat()
            inside = []
            stack = []
            while (self.at().type.type != "CloseBracket" or stack) and self.at().type.type != "EOF":
                token = self.eat()

                # check for brackets
                if token.type.type in ("OpenBracket", "OpenParen"):
                    stack += [token.type.type]
                elif token.type.type == "CloseParen":
                    if "OpenParen" not in stack:
                        print("SyntaxError: Unexpected ')'")
                        sys.exit(1)
                    
                    if stack[0] != "OpenParen":
                        print("SyntaxError: Unexpected ')'")
                        sys.exit(1)

                    stack.pop(0)
                elif token.type.type == "CloseBracket":
                    if "OpenBracket" not in stack:
                        print("SyntaxError: Unexpected ']'")
                        sys.exit(1)
                    
                    if stack[0] != "OpenBracket":
                        print("SyntaxError: Unexpected ']'")
                        sys.exit(1)

                    stack.pop(0)
                
                inside += [token]
            
            if self.at().type.type == "EOF":
                print("SyntaxError: Expected ']'")
                sys.exit(1)

            self.eat()
            return self.parse_elements_in_array(inside)

        print(f"SyntaxError: Unexpected token found during parsing: '{self.at()}'")
        sys.exit(1)
from typing import Literal
import sys
import ast

class TokenType:
    def __init__(self, 
        type:
        # End tokens
        Literal["EOF"]
        | Literal["Newline"]

        # Tab (WE WANT TO LOOK LIKE PYTHON)
        | Literal["Tab"]

        # others
        | Literal["Colon"]

        # numbers and operations
        | Literal["Number"]
        | Literal["Identifier"]
        | Literal["OpenParen"]
        | Literal["CloseParen"]
        | Literal["BinaryOperator"]

        # string
        | Literal["String"]

        # NULL IS THE BEST
        | Literal["Null"]

        # TRUE + FALSE
        | Literal["True"]
        | Literal["False"]

        # variable declaration
        | Literal["Variable"]
        | Literal["Let"]
        | Literal["Constant"]

        # support for variable declaration
        | Literal["Is"]
        | Literal["Be"]
        | Literal["Now"]

        # create keyword
        | Literal["Create"]

        # supported types for create
        | Literal["Changeable"]
        | Literal["Unchangeable"]

        # Comparison logic
        | Literal["Equals"]
        | Literal["NotEquals"]
        | Literal["GreaterThan"]
        | Literal["SmallerThan"]
        | Literal["GreaterThanOrEquals"]
        | Literal["SmallerThanOrEquals"]

        # support for arrays
        | Literal["OpenBracket"]
        | Literal["Semi"]
        | Literal["CloseBracket"]

        # object
        | Literal["Dot"]
    ) -> None:
        self.type = type

KEYWORDS = {

    # variable declaration
    "let": TokenType("Let"),
    "variable": TokenType("Variable"),
    "constant": TokenType("Constant"),

    # support for variable declaration
    "is": TokenType("Is"),
    "be": TokenType("Be"),
    "now": TokenType("Now"),

    # NULL
    "null": TokenType("Null"),

    # boolean
    "true": TokenType("True"),
    "false": TokenType("False"),

    # create
    "create": TokenType("Create"),

    # supported types for create
    "changeable": TokenType("Changeable"),
    "unchangeable": TokenType("Unchangeable")
}

TT_KEYWORDS = [tt.type for tt in KEYWORDS.values()]

END_TOKENS = {
    "EOF",
    "Newline"
}

INDENTATION = 4

class Token:
    def __init__(self, type: TokenType, value: str = "") -> None:
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        return f"(Token {self.type.type}{f': {self.value}' if self.value else ''})"

def is_alpha(source: str) -> bool:
    return source.isalpha() or source == "_"

def is_int(string: str) -> bool:
    if string == ".":
        return True
    
    try:
        int(string)
        return True
    except ValueError:
        return False
    
def is_skippable(source: str) -> bool:
    return source.isspace() and source != "\n"

def create_token(token_type: TokenType, value: str) -> Token:
    return Token(token_type, value)

def tokenize(source: str) -> list[Token]:
    tokens = []
    source = list(source)
    while source:
        if source[0] == "(":
            tokens += [create_token(TokenType("OpenParen"), source.pop(0))]
        elif source[0] == ")":
            tokens += [create_token(TokenType("CloseParen"), source.pop(0))]
        elif source[0] in "+-*/":
            tokens += [create_token(TokenType("BinaryOperator"), source.pop(0))]
        elif source[0] == ":":
            tokens += [create_token(TokenType("Colon"), source.pop(0))]
        elif source[0] == ";":
            tokens += [create_token(TokenType("Semi"), source.pop(0))]
        elif source[0] == "[":
            tokens += [create_token(TokenType("OpenBracket"), source.pop(0))]
        elif source[0] == "]":
            tokens += [create_token(TokenType("CloseBracket"), source.pop(0))]
        elif source[0] == "\n":
            tokens += [create_token(TokenType("Newline"), source.pop(0))]
        elif source[0] == ".":
            tokens += [create_token(TokenType("Dot"), source.pop(0))]
        else:
            # Handle multi-character tokens
            if source[0:INDENTATION] == [" "] * INDENTATION:
                tokens += [create_token(TokenType("Tab"), "\t")]
                for i in range(4):
                    source.pop(0)
            elif source[0] == "=":
                tokens += [create_token(TokenType("BinaryOperator"), source.pop(0))]
                if source:
                    if source[0] == "=":
                        source.pop(0)
            elif source[0] == "!":
                source.pop(0)
                if not source:
                    print("SyntaxError: Expected '='")
                    sys.exit(1)

                if source[0] != "=":
                    print(f"SyntaxError: Expected '=', got {source[0]}")
                
                source.pop(0)
                tokens += [create_token(TokenType("BinaryOperator"), "!=")]
            elif source[0] == ">":
                source.pop(0)
                if not source:
                    tokens += [create_token(TokenType("BinaryOperator"), ">")]
                elif source[0] == "=":
                    source.pop(0)
                    tokens += [create_token(TokenType("BinaryOperator"), ">=")]
                else:
                    tokens += [create_token(TokenType("BinaryOperator"), ">")]
            elif source[0] == "<":
                source.pop(0)
                if not source:
                    tokens += [create_token(TokenType("BinaryOperator"), "<")]
                elif source[0] == "=":
                    source.pop(0)
                    tokens += [create_token(TokenType("BinaryOperator"), "<=")]
                else:
                    tokens += [create_token(TokenType("BinaryOperator"), "<")]
            elif is_int(source[0]):
                number = ""
                while source and is_int(source[0]):
                    number += source.pop(0)
                
                count = number.count(".")
                if count > 1:
                    print(f"SyntaxError: Expected 1 '.', got {count}/1")
                    sys.exit(1)
                    
                tokens += [create_token(TokenType("Number"), number)]
            elif is_alpha(source[0]):
                identifier = ""
                while source and (is_alpha(source[0]) or is_int(source[0])):
                    identifier += source.pop(0)
                
                tt = KEYWORDS.get(identifier, TokenType("Identifier"))
                tokens += [create_token(tt, identifier)]
            elif source[0] in "'\"":
                string = source.pop(0)
                quote = string
                legal = True
                ran = False
                while source[0:1] != [quote] and source:
                    ran = True
                    char = source[0]
                    string += source.pop(0)
                    if not source:
                        legal = False
                        break

                    if char == "\\":
                        string += source.pop(0)
                
                if not legal or not ran:
                    print(f"SyntaxError: Expected '{quote}'")
                    sys.exit(1)
                
                string = ast.literal_eval(string + source.pop(0))
                tokens += [create_token(TokenType("String"), string)]
            elif is_skippable(source[0]):
                source.pop(0) # skip
            else:
                print(f"SyntaxError: Unexpected character: '{source[0]}'")
                sys.exit(1)
    #print(tokens)
    return tokens + [create_token(TokenType("EOF"), "EOF")]
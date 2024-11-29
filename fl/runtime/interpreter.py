from .values import *
from ..frontend.abstract_syntax_tree import *
import sys

# STATEMENTS
def evaluate_program(program: Program, environment: Environment) -> RuntimeValue:
    last_evaluated = NullValue()

    for statement in program.body:
        last_evaluated = evaluate(statement, environment)
    
    return last_evaluated

def evaluate_variable_declaration(node: VariableDeclaration, environment: Environment):
    value = evaluate(node.value, environment)
    environment.declare_variable(node.identifier, value, node.constant)
    return value

def evaluate_assignment_statement(node: AssignmentStatement, environment: Environment):
    value = evaluate(node.value, environment)
    environment.assign_variable(node.identifier, value)
    return value

# EXPRESSIONS (FUCK YOU CIRCULAR IMPORTS)
def evaluate_binary_expression(binary_operation: BinaryExpression, environment: Environment) -> RuntimeValue:
    left = evaluate(binary_operation.left, environment)
    right = evaluate(binary_operation.right, environment)
    operator = binary_operation.operator

    if operator == "+":
        if left.type.type in ("number", "boolean"):
            if right.type.type not in ("number", "boolean"):
                print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
                sys.exit(1)

            return evaluate_numeric_binary_expression(left, right, "+")
        
        print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
        sys.exit(1)
    
    if operator == "-":
        if left.type.type in ("number", "boolean"):
            if right.type.type not in ("number", "boolean"):
                print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
                sys.exit(1)

            return evaluate_numeric_binary_expression(left, right, "-")
        
        print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
        sys.exit(1)
    
    if operator == "*":
        if left.type.type in ("number", "boolean"):
            if right.type.type not in ("number", "boolean"):
                print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
                sys.exit(1)

            return evaluate_numeric_binary_expression(left, right, "*")
        
        print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
        sys.exit(1)
    
    if operator == "/":
        if left.type.type in ("number", "boolean"):
            if right.type.type not in ("number", "boolean"):
                print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
                sys.exit(1)

            return evaluate_numeric_binary_expression(left, right, "/")
        
        print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
        sys.exit(1)
    
    if operator == ">":
        if left.type.type in ("number", "boolean"):
            if right.type.type not in ("number", "boolean"):
                print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
                sys.exit(1)

            return evaluate_comparison_binary_expression(left, right, ">")
        
        print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
        sys.exit(1)
        
    if operator == "<":
        if left.type.type in ("number", "boolean"):
            if right.type.type not in ("number", "boolean"):
                print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
                sys.exit(1)

            return evaluate_comparison_binary_expression(left, right, "<")
        
        print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
        sys.exit(1)
    
    if operator == ">=":
        if left.type.type in ("number", "boolean"):
            if right.type.type not in ("number", "boolean"):
                print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
                sys.exit(1)

            return evaluate_comparison_binary_expression(left, right, ">=")
        
        print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
        sys.exit(1)
    
    if operator == "<=":
        if left.type.type in ("number", "boolean"):
            if right.type.type not in ("number", "boolean"):
                print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
                sys.exit(1)

            return evaluate_comparison_binary_expression(left, right, "<=")
        
        print(f"BinaryExpressionError: Unexpected binary operation between '{left.type.type}' and '{right.type.type}'")
        sys.exit(1)

    if operator == "=":
        return evaluate_equality_binary_expression(left, right, "=")
    
    if operator == "!=":
        return evaluate_equality_binary_expression(left, right, "!=")

def evaluate_equality_binary_expression(left: RuntimeValue, right: RuntimeValue, operator: str) -> RuntimeValue:
    if operator == "=":
        if left.type.type != right.type.type:
            return BooleanValue("false")
        
        return BooleanValue("true" if left.value == right.value else "false")
    
    if operator == "!=":
        if left.type.type != right.type.type:
            return BooleanValue("true")
        
        return BooleanValue("true" if left.value != right.value else "false")

def evaluate_comparison_binary_expression(left: NumberValue | BooleanValue, right: NumberValue | BooleanValue, operator: str) -> RuntimeValue:
    if left.type.type == "boolean":
        left.value = translate_boolean(left)
    
    if right.type.type == "boolean":
        right.value = translate_boolean(right)
    
    if operator == ">":
        return BooleanValue("true" if float(left.value) > float(right.value) else "false")
    
    if operator == "<":
        return BooleanValue("true" if float(left.value) < float(right.value) else "false")
    
    if operator == ">=":
        return BooleanValue("true" if float(left.value) >= float(right.value) else "false")
    
    if operator == "<=":
        return BooleanValue("true" if float(left.value) <= float(right.value) else "false")

def evaluate_numeric_binary_expression(left: NumberValue | BooleanValue, right: NumberValue | BooleanValue, operator: str) -> RuntimeValue:
    if left.type.type == "boolean":
        left.value = translate_boolean(left)
        
    if right.type.type == "boolean":
        right.value = translate_boolean(right)

    if operator == "+":
        return create_number(float(left.value) + float(right.value))
    
    if operator == "-":
        return create_number(float(left.value) - float(right.value))
    
    if operator == "*":
        return create_number(float(left.value) * float(right.value))
    
    if operator == "/":
        if float(right.value) == 0:
            print(f"MathError: Division by 0")
            sys.exit(1)

        return create_number(float(left.value) / float(right.value))
    
    print(f"SyntaxError: Operator '{operator}' was not implemented")
    sys.exit(1)

def evaluate_unary_expression(ast_node: UnaryExpression, environment: Environment):
    sign = ast_node.sign
    expression = evaluate(ast_node.expression, environment)
    if expression.type.type == "number":
        return expression if sign == "+" else create_number(-expression.value)
    
    if expression.type.type == "boolean":
        if sign == "+":
            return expression
        
        if expression.value == "true":
            return BooleanValue("false")
        
        return BooleanValue("true")
    
    if expression.type.type == "string":
        if sign == "-":
            return expression
        
        return StringValue(expression.value[::-1])

def evaluate_call_expression(call: CallExpression, environment: Environment) -> RuntimeValue:
    arguments = [evaluate(argument, environment) for argument in call.arguments]
    function = evaluate(call.callee, environment)
    if function.type.type != "native_function":
        print("SyntaxError: Expected function, got variable")
        sys.exit(1)
    
    # somehow, we need to translate from flu values to python values
    result = function.call(arguments)

    return result

def translate_flu_value(value: Expression):
    if value.type.type == "boolean":
        return translate_boolean(value.value)
    
    if value.type.type == "array":
        values = []
        for element in value.value:
            values += [translate_flu_value(element)]
        
        return values
    
    if value.type.type == "null":
        return None
    
    return value.value

def translate_python_value(value):
    if isinstance(value, (int, float)):
        return create_number(float(value))
    
    if isinstance(value, str):
        return StringValue(value)
    
    if isinstance(value, bool):
        return BooleanValue("true" if value else "false")
    
    if isinstance(value, (list, tuple, set)):
        array = []
        for element in value:
            array += [translate_python_value(element)]
        
        return ArrayValue(array)
    
    if value is None:
        return NullValue()

def evaluate_array(ast_node: ArrayLiteral, environment: Environment):
    return ArrayValue([evaluate(i, environment) for i in ast_node.value])

def evaluate_identifier(identifier: Identifier, environment: Environment) -> RuntimeValue:
    return environment.lookup_variable(identifier.symbol)

def evaluate_fetch_expression(ast_node: FetchExpression, environment: Environment):
    fetched = evaluate(ast_node.fetched, environment)
    index = evaluate(ast_node.index, environment)
    if fetched.type.type in ("number", "null", "boolean"):
        print(f"TypeError: Unexpected fetch operation between '{fetched.type.type}' and '{index.type.type}'")
        sys.exit(1)

    if index.type.type != "number":
        print(f"TypeError: Unexpected fetch operation between '{fetched.type.type}' and '{index.type.type}'")
        sys.exit(1)

    if index.value % 1 > 0:
        print(f"MathError: Invalid index value, got remainder of {index.value % 1}/1.")
        sys.exit(1)
    
    if fetched.type.type == "string":
        modulo = int(index.value % len(fetched.value))
        return StringValue(fetched.value[modulo])

    if fetched.type.type == "array":
        modulo = int(index.value % len(fetched.value))
        return fetched.value[modulo]
    
def evaluate(ast_node: Statement, environment: Environment) -> RuntimeValue:   
    if ast_node.kind.type == "NumericLiteral":
        return create_number(ast_node.value)
    
    if ast_node.kind.type == "NullLiteral":
        return NullValue()
    
    if ast_node.kind.type == "StringLiteral":
        return StringValue(ast_node.value)
    
    if ast_node.kind.type == "BooleanLiteral":
        return BooleanValue(ast_node.value)
    
    if ast_node.kind.type == "ArrayLiteral":
        return evaluate_array(ast_node, environment)

    if ast_node.kind.type == "Identifier":
        return evaluate_identifier(ast_node, environment)

    if ast_node.kind.type == "BinaryExpr":
        return evaluate_binary_expression(ast_node, environment)
    
    if ast_node.kind.type == "UnaryExpr":
        return evaluate_unary_expression(ast_node, environment)

    if ast_node.kind.type == "FetchExpr":
        return evaluate_fetch_expression(ast_node, environment)

    if ast_node.kind.type == "CallExpr":
        return evaluate_call_expression(ast_node, environment)

    if ast_node.kind.type == "Program":
        return evaluate_program(ast_node, environment)

    if ast_node.kind.type == "VariableDeclaration":
        return evaluate_variable_declaration(ast_node, environment)
    
    if ast_node.kind.type == "AssignmentStatement":
        return evaluate_assignment_statement(ast_node, environment)
    
    print(f"InterpreterError: This AST node has not been setup for interpretation node: '{ast_node}'")
    sys.exit(1)
from ast_nodes import NumberLiteral, BooleanLiteral, BinaryExpression

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, program):
        for statement in program.statements:
            pass

    def evaluate(self, expression):
        """converts AST values into Python values"""
        if isinstance(expression, NumberLiteral):
            return expression.value
        elif isinstance(expression, BooleanLiteral):
            return expression.value
        elif isinstance(expression, BinaryExpression):
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)

            match expression.op.value:
                case '+':
                    return left + right
                case '-':
                    return left - right
                case '*':
                    return left * right
                case '/':
                    if right == 0:
                        raise ZeroDivisionError("It is not possible to divide by 0")
                    return left / right
                case '%':
                    return left % right
                case '==':
                    return left == right
                case '!=':
                    return left != right
                case '>':
                    return left > right
                case '<':
                    return left < right
                case '>=':
                    return left >= right
                case '<=':
                    return left <= right
                    
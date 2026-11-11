from ast_nodes import NumberLiteral, BooleanLiteral, BinaryExpression, VariableReference, VariableDeclaration, Assignment

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, program):
        for statement in program.statements:
            if isinstance(statement, VariableDeclaration):
                name = statement.name.value
                value = self.evaluate(statement.initializer, program)
                self.variables[name] = value

            elif isinstance(statement, Assignment):
                name = statement.name.value
                expression = self.evaluate(statement.value, program)
                if statement.name.value not in self.variables:
                    raise NameError(f"name '{name}' is not defined")

                self.variables[name] = expression

    def evaluate(self, expression, program):
        """converts AST values into Python values"""
        if isinstance(expression, NumberLiteral):
            return expression.value
        elif isinstance(expression, BooleanLiteral):
            return expression.value
        elif isinstance(expression, BinaryExpression):
            left = self.evaluate(expression.left, program)

            match expression.op.value:
                case '&&':
                    if left is False:
                        return False
            
                case '||':
                    if left is True:
                        return True

            right = self.evaluate(expression.right, program)

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
                case '&&':
                    return left and right
                case '||':
                    return left or right

        elif isinstance(expression, VariableReference):
            if expression.name.value in self.variables:
                return self.variables[expression.name.value]
            else:
                raise NameError(f"name '{expression.name.value}' is not defined")
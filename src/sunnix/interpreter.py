from ast_nodes import NumberLiteral, BooleanLiteral, BinaryExpression, VariableReference, VariableDeclaration, Assignment, BlockStatement

class Interpreter:
    def __init__(self, program):
        self.variables = {}
        self.program = program

    def interpret(self):
        for statement in self.program.statements:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        if isinstance(statement, VariableDeclaration):
            name = statement.name.value
            value = self.evaluate(statement.initializer)
            self.variables[name] = value

        elif isinstance(statement, Assignment):
            name = statement.name.value
            expression = self.evaluate(statement.value)
            if name not in self.variables:
                raise NameError(f"name '{name}' is not defined")
    
            self.variables[name] = expression

        elif isinstance(statement, BlockStatement):
            for inner_statement in statement.statements:
                self.execute_statement(inner_statement)

    def evaluate(self, expression):
        """converts AST values into Python values"""
        if isinstance(expression, NumberLiteral):
            return expression.value
        elif isinstance(expression, BooleanLiteral):
            return expression.value
        elif isinstance(expression, BinaryExpression):
            left = self.evaluate(expression.left)

            match expression.op.value:
                case '&&':
                    if left is False:
                        return False
            
                case '||':
                    if left is True:
                        return True

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
                case '&&':
                    return left and right
                case '||':
                    return left or right

        elif isinstance(expression, VariableReference):
            if expression.name.value in self.variables:
                return self.variables[expression.name.value]
            else:
                raise NameError(f"name '{expression.name.value}' is not defined")
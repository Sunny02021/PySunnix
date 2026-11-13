from ast_nodes import NumberLiteral, BooleanLiteral, BinaryExpression, VariableReference, VariableDeclaration, Assignment, BlockStatement, UnaryExpression, FunctionCall, StringLiteral, ExpressionStatement, IfStatement, WhileStatement

class Interpreter:
    def __init__(self, program):
        self.variables = {}
        self.program = program

    def interpret(self):
        """calls execute_statement() for each statement on program.statements"""
        for statement in self.program.statements:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        """evaluates and executes the statement based on the object's type"""
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
        
        elif isinstance(statement, ExpressionStatement):
            self.evaluate(statement.expression)

        elif isinstance(statement, IfStatement):
            """for if, else if and else statements"""
            condition = self.evaluate(statement.condition)
            if condition:
                """falls on the BlockStatement treatment"""
                self.execute_statement(statement.then_branch)
            else:
                if statement.else_branch is not None:
                    self.execute_statement(statement.else_branch)

        elif isinstance(statement, WhileStatement):
            """for while statements"""
            condition = self.evaluate(statement.condition)
            while condition:
                self.execute_statement(statement.body)
                condition = self.evaluate(statement.condition)

    def evaluate(self, expression):
        """converts AST values into Python values"""
        if isinstance(expression, NumberLiteral):
            return expression.value
        elif isinstance(expression, BooleanLiteral):
            return expression.value
        elif isinstance(expression, StringLiteral):
            return expression.value
        elif isinstance(expression, VariableReference):
            if expression.name.value in self.variables:
                return self.variables[expression.name.value]
            else:
                raise NameError(f"name '{expression.name.value}' is not defined")

        elif isinstance(expression, UnaryExpression):
            value = self.evaluate(expression.operand)
            match expression.op.value:
                case '+':
                    return +value
                case '-':
                    return -value
                case '!':
                    return not value
                case _:
                    raise ValueError(f"Unknown unary operator: {expression.op!r}")

        elif isinstance(expression, FunctionCall):
            name = expression.name.value

            values = []
            for arg in expression.args:
                value = self.evaluate(arg)
                values.append(value)

            if name == "print":
                print(*values) # i'll use python functions for now
            else:
                raise NameError(f"Undefined function '{name}'")

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
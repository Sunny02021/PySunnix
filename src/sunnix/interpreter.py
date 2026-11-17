from .ast_nodes import NumberLiteral, BooleanLiteral, BinaryExpression, VariableReference, VariableDeclaration, Assignment, BlockStatement, UnaryExpression, FunctionCall, StringLiteral, ExpressionStatement, IfStatement, WhileStatement, FunctionDeclaration, ReturnStatement, NullLiteral, BreakStatement 
from .errors import ReturnException, BreakException
import operator

BINARY_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '%': operator.mod,
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

class Interpreter:
    def __init__(self, program):
        self.scopes = [{}] # the first dict is the global scope
        self.functions = {}
        self.program = program

    def interpret(self):
        """calls execute_statement() for each statement on program.statements"""
        # since we want a function to be callable even if its declaration
        # appears after the call in the source code, we add it to self.functions
        # in advance
        for statement in self.program.statements:
            if isinstance(statement, FunctionDeclaration):
                self.functions[statement.name.value] = statement

        for statement in self.program.statements:
            if not isinstance(statement, FunctionDeclaration):
                self.execute_statement(statement)

    def execute_statement(self, statement):
        """evaluates and executes the statement based on the object's type"""
        if isinstance(statement, VariableDeclaration):
            name = statement.name.value
            value = self.evaluate(statement.initializer)
            self.scopes[-1][name] = value # the last dict represents the
            # innermost scope. a.k.a, the one we're currently working with

        elif isinstance(statement, Assignment):
            name = statement.name.value
            expression = self.evaluate(statement.value)
            for scope in reversed(self.scopes):
                if name in scope:
                    scope[name] = expression
                    return

            raise NameError(f"name '{name}' is not defined")

        elif isinstance(statement, BlockStatement):
            self.enter_scope()
            try:
                for inner_statement in statement.statements:
                    self.execute_statement(inner_statement)
            finally:
                self.exit_scope()

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
                try:
                    self.execute_statement(statement.body)
                    condition = self.evaluate(statement.condition)
                except BreakException:
                    return

        elif isinstance(statement, ReturnStatement):
            value = self.evaluate(statement.value)
            raise ReturnException(value)

        elif isinstance(statement, BreakStatement):
            raise BreakException(None)

    def evaluate(self, expression):
        """converts AST values into Python values
        
        for NumberLiteral, BooleanLiteral and StringLiteral we simply
        return it, since our Lexer already converted
        """
        if isinstance(expression, NumberLiteral):
            return expression.value
        elif isinstance(expression, BooleanLiteral):
            return expression.value
        elif isinstance(expression, StringLiteral):
            return expression.value
        elif isinstance(expression, NullLiteral):
            return None

        elif isinstance(expression, VariableReference):
            for scope in reversed(self.scopes):
                if expression.name.value in scope:
                    return scope[expression.name.value]

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
                # change every None to "null"
                # every True to "true"
                # every False to "false"
                print_values = [
                    "null" if value is None
                    else "true" if value is True
                    else "false" if value is False
                    else value for value in values
                ]

                print(*print_values) # i'll use python functions for now

            elif name in self.functions:
                function = self.functions[name]

                if len(values) < len(function.parameters):
                    raise TypeError(
                        f"{name}() missing {len(function.parameters) - len(values)} "
                        "required positional argument."
                    )

                if len(values) > len(function.parameters):
                    raise TypeError(f"{name}() has too many positional arguments.")

                self.enter_scope()
                try:
                    # associating args to parameters
                    for parameter, value in zip(function.parameters, values):
                        self.scopes[-1][parameter.name.value] = value

                    # executing the function body
                    self.execute_statement(function.body)

                except ReturnException as result:
                    return result.value
                finally:
                    self.exit_scope()

            else:
                raise NameError(f"Undefined function '{name}'")


        elif isinstance(expression, BinaryExpression):
            left = self.evaluate(expression.left)
            op = expression.op.value

            if op == '&&':
                return left and self.evaluate(expression.right)
            if op == '||':
                return left or self.evaluate(expression.right)

            right = self.evaluate(expression.right)

            if op == '/':
                if right == 0:
                    raise ZeroDivisionError("It is not possible to divide by 0")
                return left / right

            if op in BINARY_OPS:
                return BINARY_OPS[op](left, right)

            raise ValueError(f"Unknown operator: {op}")

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

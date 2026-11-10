from tokens import Token, TokenType
from ast_nodes import NumberLiteral, BinaryExpression, VariableDeclaration, Program, Statement, Assignment, UnaryExpression, BooleanLiteral, BlockStatement, IfStatement, VariableReference, WhileStatement, FunctionCall, ExpressionStatement

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        """Returns current token or None"""
        if self.position >= len(self.tokens):
            return None

        return self.tokens[self.position]

    def peek(self):
        """returns next token or None"""
        next_position = self.position + 1

        if next_position >= len(self.tokens):
            return None

        return self.tokens[next_position]

    def advance(self):
        """Advance one position and returns the current token"""
        token = self.current_token()

        if token.type == TokenType.EOF:
            return token

        self.position += 1

        return token

    def expect(self, token_type):
        """
        Checks the current token and returns it if the type
        matches the passed token_type.
        """
        token = self.current_token()

        if token.type == token_type:
            self.advance()
            return token

        raise ParserError(
            f"Expected {token_type.name}, got {token.type.name} ({token.value})"
        )

    def parse_primary(self):
        """Converts a numeric token into a AST Node of type NumberLiteral"""

        token = self.current_token()

        if token.type == TokenType.NUMBER:
            num_literal = NumberLiteral(token.value)
            self.advance()
            return num_literal

        elif token.type in (TokenType.TRUE, TokenType.FALSE):
            if token.type == TokenType.TRUE:
                bool_literal = BooleanLiteral(True)
                self.advance()
                return bool_literal

            bool_literal = BooleanLiteral(False)
            self.advance()
            return bool_literal

        elif token.type == TokenType.LEFT_PAREN:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.RIGHT_PAREN)
            return expression

        elif token.type == TokenType.IDENTIFIER:
            peek = self.peek()
            if peek is not None and peek.type == TokenType.LEFT_PAREN:
                instruction = self.parse_function_call()
                return instruction
            else:
                tk = token
                self.advance()
                return VariableReference(tk)

        raise ParserError(
            f"Expected a number literal, but found '{token.value}' "
            f"({token.type.name}) at line {token.line}, column {token.column}."
        )
    
    def parse_unary(self):
        """recognises unary operators (-10, +10... etc)"""
        token = self.current_token()

        if token.type in (TokenType.MINUS, TokenType.PLUS):
            op = token
            self.advance()
            operand = self.parse_unary()
            return UnaryExpression(op, operand)

        return self.parse_primary()

    def parse_factor(self):
        left = self.parse_unary()

        token = self.current_token()
        while token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            self.advance()
            operator = token
            right = self.parse_unary()
            left = BinaryExpression(left, operator, right)
            token = self.current_token()

        return left

    def parse_expression(self):
        left = self.parse_factor()

        token = self.current_token()
        while token.type in (TokenType.PLUS, TokenType.MINUS):
            self.advance()
            operator = token
            right = self.parse_factor()
            left = BinaryExpression(left, operator, right)
            token = self.current_token()

        return left

    def parse_comparison(self):
        """for expressions such as:
        
        int a = 10 + 5 > 12;
        """
        left = self.parse_expression()
        
        token = self.current_token()
        while token.type in (
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL
        ):
            self.advance()
            operator = token
            right = self.parse_expression()
            left = BinaryExpression(left, operator, right)
            token = self.current_token()

        return left

    def parse_variable_declaration(self):
        var_type = self.current_token()
        self.advance()
        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQUAL) # =
        initializer = self.parse_or()
        self.expect(TokenType.SEMICOLON)
        
        return VariableDeclaration(var_type, name, initializer)

    def parse_program(self):
        """iterates through the tokens until curr token == EOF,
        calling the appropriate methods for each instruction"""
        
        statements: list[Statement] = []

        token = self.current_token()
        while token.type != TokenType.EOF:
            statements.append(self.parse_statement())
            token = self.current_token()

        return Program(statements)

    def parse_assignment(self):
        """recognises expressions that assign a value to an
        existing variable, such as:

        int age = 17;
        age = 18;"""

        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQUAL)
        value = self.parse_or()
        self.expect(TokenType.SEMICOLON)
        
        return Assignment(name, value)

    def parse_and(self):
        """recognizes expressions with the and (&&) operator"""

        left = self.parse_comparison()
        
        token = self.current_token()
        while token.type == TokenType.AND:
            op = token
            self.advance()
            right = self.parse_comparison()
            left = BinaryExpression(left, op, right)
            token = self.current_token()

        return left

    def parse_or(self):
        """recognizes expressions with the or (||) operator"""

        left = self.parse_and()
        
        token = self.current_token()
        while token.type == TokenType.OR:
            op = token
            self.advance()
            right = self.parse_and()
            left = BinaryExpression(left, op, right)
            token = self.current_token()

        return left

    def parse_block(self):
        """recognizes statements inside braces"""
        self.expect(TokenType.LEFT_BRACE)

        statements: list[Statement] = []
        token = self.current_token()

        while token.type not in (TokenType.RIGHT_BRACE, TokenType.EOF):
            statements.append(self.parse_statement())
            token = self.current_token()

        self.expect(TokenType.RIGHT_BRACE)

        return BlockStatement(statements)
    
    def parse_statement(self):
        """calls the appropriate method for each instruction"""
        token = self.current_token()

        if token.type in (TokenType.INT, TokenType.FLOAT):
            return self.parse_variable_declaration()

        elif token.type == TokenType.IDENTIFIER:
            peek = self.peek()
        
            if peek is not None and peek.type == TokenType.LEFT_PAREN:
                instruction = self.parse_function_call()
                self.expect(TokenType.SEMICOLON)
                return ExpressionStatement(instruction)
            else:
                return self.parse_assignment()

        elif token.type == TokenType.IF:
            return self.parse_if_statement()

        elif token.type == TokenType.WHILE:
            return self.parse_while_statement()

        else:
            raise ParserError(
                f"Unexpected token '{token.value}' of type {token.type.name} whilst attempting to read a statement."
                f" line {token.line}, column {token.column}"
            )

    def parse_if_statement(self):
        """recognizes if, else if and else statements"""
        self.expect(TokenType.IF)
        self.expect(TokenType.LEFT_PAREN)
        expression = self.parse_or()
        self.expect(TokenType.RIGHT_PAREN)
        block = self.parse_block()
        else_branch = None
        
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            if self.current_token().type == TokenType.IF:
                else_branch = self.parse_if_statement()
            else:
                else_branch = self.parse_block()

        return IfStatement(expression, block, else_branch)

    def parse_while_statement(self):
        """recognizes while statements"""
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LEFT_PAREN)
        expression = self.parse_or()
        self.expect(TokenType.RIGHT_PAREN)
        block = self.parse_block()

        return WhileStatement(expression, block)

    def parse_function_call(self):
        """recognizes function calls (sum(50 + 17))"""
        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LEFT_PAREN)
        args: list[Expression] = []

        # case 1: no arg passed
        if self.current_token().type == TokenType.RIGHT_PAREN:
            self.expect(TokenType.RIGHT_PAREN)
            return FunctionCall(name, args) # no-args passed; empty list
        else:
            # case 2: one arg passed
            args.append(self.parse_or())

            peek = self.peek()
            if self.current_token().type == TokenType.RIGHT_PAREN:
                self.expect(TokenType.RIGHT_PAREN)
                return FunctionCall(name, args)

            # case 3: 'n' args passed
            token = self.current_token()
            while token.type == TokenType.COMMA:
                self.expect(TokenType.COMMA)
                args.append(self.parse_or())
                token = self.current_token()

            self.expect(TokenType.RIGHT_PAREN)

            return FunctionCall(name, args)
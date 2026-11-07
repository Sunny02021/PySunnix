from tokens import Token, TokenType
from ast_nodes import NumberLiteral, BinaryExpression, VariableDeclaration, Program, Statement, Assignment

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

        elif token.type == TokenType.LEFT_PAREN:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.RIGHT_PAREN)
            return expression

        raise ParserError(
            f"Expected a number literal, but found '{token.value}' "
            f"({token.type.name}) at line {token.line}, column {token.column}."
        )

    def parse_factor(self):
        left = self.parse_primary()

        token = self.current_token()
        while token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            self.advance()
            operator = token
            right = self.parse_primary()
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

    def parse_variable_declaration(self):
        var_type = self.current_token()
        self.advance()
        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQUAL) # =
        initializer = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        return VariableDeclaration(var_type, name, initializer)

    def parse_program(self):
        """iterates through the tokens until curr token == EOF,
        calling the appropriate methods for each instruction"""
        
        statements: list[Statement] = []

        token = self.current_token()
        while token.type != TokenType.EOF:
            if token.type in (TokenType.INT, TokenType.FLOAT):
                statements.append(self.parse_variable_declaration())

            elif token.type == TokenType.IDENTIFIER:
                statements.append(self.parse_assignment())

            else:
                raise ParserError(
                    f"Unexpected token '{token.value}' of type {token.type.name} whilst attempting to read a statement."
                    f"line {token.line}, column {token.column}"
                )

            token = self.current_token()

        return Program(statements)

    def parse_assignment(self):
        """recognises expressions that assign a value to an
        existing variable, such as:

        int age = 17;
        age = 18;"""

        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQUAL)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        return Assignment(name, value)
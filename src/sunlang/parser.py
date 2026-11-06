from tokens import Token, TokenType

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

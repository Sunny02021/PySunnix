from tokens import Token, TokenType

class LexerError(Exception):
    pass

class Lexer:
    KEYWORDS = {
        "int": TokenType.INT,
        "float": TokenType.FLOAT,
        "func": TokenType.FUNC,
        "return": TokenType.RETURN,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
    }

    def __init__(self, source):
        self.source = source

        self.position = 0
        self.line = 1
        self.column = 1

        self.tokens = []

    def current_char(self):
        """Returns current character or None"""
        if self.position >= len(self.source):
            return None

        return self.source[self.position]

    def peek(self):
        """Returns next character or None"""
        next_position = self.position + 1

        if next_position >= len(self.source):
            return None

        return self.source[next_position]

    def advance(self):
        """Advance one position and returns the current character"""
        char = self.current_char()

        if char is None:
            return None

        self.position += 1

        if char == "\n":
            self.line += 1
            self.column += 1
        else:
            self.column += 1

        return char

    def add_token(self, token_type, value):
        """Adds a token on the token list"""
        self.tokens.append(
            Token(
                token_type,
                value,
                self.line,
                self.column
            )
        )

    def skip_whitespace(self):
        """Skip whitespaces (duh)"""
        while self.current_char() is not None:
            if self.current_char().isspace():
                self.advance()
            else:
                break

    def skip_comment(self):
        """Skip comments (duh²)"""
        while self.current_char() is not None:
            if self.current_char() == "\n":
                break

            self.advance()

    def read_number(self):
        """Reads a number, ddcimal included"""
        start = self.position
        has_decimal = False

        while self.current_char() is not None:
            char = self.current_char()

            if char.isdigit():
                self.advance()
            elif char == "." and not has_decimal:
                if self.peek() is not None and self.peek().isdigit():
                    has_decimal = True
                    self.advance()
                else:
                    break
            else:
                break

        value = self.source[start:self.position]

        if has_decimal:
            self.add_token(TokenType.NUMBER, float(value))
        else:
            self.add_token(TokenType.NUMBER, int(value))

    def read_identifier(self):
        """Reads a idenfifier"""
        start = self.position

        while self.current_char() is not None:
            char = self.current_char()

            if char.isalnum() or char == "_":
                self.advance()
            else:
                break

        value = self.source[start:self.position]

        token_type = self.KEYWORDS.get(
            value,
            TokenType.IDENTIFIER
        )

        self.add_token(token_type, value)

    def read_string(self):
        """Reads a string"""
        self.advance() # open quotes

        value = ""

        while self.current_char() is not None:
            char = self.current_char()

            # empty string (like name = "")
            if char == '"':
                self.advance()
                self.add_token(TokenType.STRING, value)
                return

            if char == "\\":
                self.advance()
                escaped = self.current_char()

                if escaped is None:
                    break

                escape_map = {
                    "n": "\n",
                    "t": "\t",
                    '"': '"',
                    "\\": "\\",
                }

                if escaped not in escape_map:
                    raise LexerError(
                        f"Invalid escape sequence: \\{escape}"
                    )

                value += escape_map[escaped]
                self.advance()
            else:
                value += self.advance()

        raise LexerError("Unfinished string")

    def tokenize(self):
        """divides the source code into a sequence of tokens"""

        while self.current_char() is not None:
            char = self.current_char()

            if char.isspace():
                self.skip_whitespace()
                continue

            if char == "/" and self.peek() == "/":
                self.skip_comment()
                continue

            if char.isdigit():
                self.read_number()
                continue

            if char.isalpha() or char == "_":
                self.read_identifier()
                continue

            if char == '"':
                self.read_string()
                continue

            operators = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MULTIPLY,
                "/": TokenType.DIVIDE,
                ";": TokenType.SEMICOLON,
                ",": TokenType.COMMA,
                ".": TokenType.DOT,
                "(": TokenType.LEFT_PAREN,
                ")": TokenType.RIGHT_PAREN,
                "{": TokenType.LEFT_BRACE,
                "}": TokenType.RIGHT_BRACE
            }

            if char in operators:
                self.advance()
                self.add_token(operators[char], char)
                continue

            double_operators = {
                "==": TokenType.EQUAL_EQUAL,
                "!=": TokenType.NOT_EQUAL,
                ">=": TokenType.GREATER_EQUAL,
                "<=": TokenType.LESS_EQUAL,
            }

            pair = char + (self.peek() or "")

            if pair in double_operators:
                self.advance()
                self.advance()
                self.add_token(double_operators[pair], char)
                continue

            single_operators = {
                "=": TokenType.EQUAL, # TODO: change this to
                                      # "EQUALS" and change on tokens.py too
                ">": TokenType.GREATER,
                "<": TokenType.LESS,
            }

            if char in single_operators:
                self.advance()
                self.add_token(single_operators[char], char)
                continue

            raise LexerError(
                f"Unexpected character '{char}' "
                f"on line {self.line}, column {self.column}"
            )

        self.tokens.append(
                Token(TokenType.EOF, None, self.line, self.column)
            )

        return self.tokens

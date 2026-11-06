import sys

sys.path.insert(0, "src/sunlang")

from lexer import Lexer
from parser import Parser

code = """
10 + 20
"""

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)

print(f"Current Token: {parser.current_token()}")
parser.advance()
print(f"After advance(): {parser.current_token()}")

import sys

sys.path.insert(0, "src/sunlang")

from lexer import Lexer
from parser import Parser

code = """
int a = true && false;
int b = true && false && true;
int c = 10 > 5 && 8 < 20;
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)

#node = parser.parse_primary()
#node = parser.parse_factor()
#node = parser.parse_expression()
#node = parser.parse_variable_declaration()
node = parser.parse_program()

print(node)
print(type(node))
#print(node.value)

#print(f"Current Token: {parser.current_token()}")

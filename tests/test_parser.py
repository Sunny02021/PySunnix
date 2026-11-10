import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser

code = """
print(sum(10 + 5, 20 * 2));
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)

#node = parser.parse_primary()
#node = parser.parse_factor()
#node = parser.parse_expression()
#node = parser.parse_variable_declaration()
node = parser.parse_program()
#node = parser.parse_block()
#node = parser.parse_if_statement()

print(node)
print(type(node))
#print(node.value)

#print(f"Current Token: {parser.current_token()}")

import sys

sys.path.insert(0, "src/sunlang")

from lexer import Lexer
from parser import Parser
from ast_nodes import NumberLiteral

code = """
int f = 10 > 5 > 2;
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

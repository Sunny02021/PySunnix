import sys

sys.path.insert(0, "src/sunlang")

from lexer import Lexer
from parser import Parser
from ast_nodes import NumberLiteral

#code = "10 + 20 + 30"
# code = "10 * 20 / 5"
code = "(10 + 20) * (3 + 4)"
# code = "((10 + 5) * 2) - 3"
# code = "()"
# code = "(10 + )"

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)

#node = parser.parse_primary()
#node = parser.parse_factor()
node = parser.parse_expression()

print(node)
print(type(node))
#print(node.value)

#print(f"Current Token: {parser.current_token()}")

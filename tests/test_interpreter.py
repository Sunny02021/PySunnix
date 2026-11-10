
import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

code = """
print(10 + 5 * 2);
print((10 + 5) * 2);
print(20 / 0);
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse_program()

interpreter = Interpreter()

for statement in program.statements:
    expression = statement.expression
    result = interpreter.evaluate(expression.args[0])
    print(result)

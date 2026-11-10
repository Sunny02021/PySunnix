
import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

code = """
print(false && (10 / 0 > 2));
print(true || (10 / 0 > 2));
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

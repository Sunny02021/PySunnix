
import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

code = """
print("Hello, Sunnix!");
print(10 + 5, 20 * 2);
unknown_function(42);
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse_program()

interpreter = Interpreter(program)
interpreter.interpret()



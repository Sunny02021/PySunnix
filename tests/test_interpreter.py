import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

code = """
func sum(int a, int b, int c) {
    print(a + b * c);
}

sum(10, 20, 30);
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse_program()

interpreter = Interpreter(program)
interpreter.interpret()

# print(program)

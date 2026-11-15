import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

code = """
print(null == null);
print(null != null);

func test() {
}

print(test() == null);
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse_program()

interpreter = Interpreter(program)
interpreter.interpret()

# print(program)

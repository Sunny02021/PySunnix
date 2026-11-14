
import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

code = """
int x = 10;

{
    int y = 20;
    print(x);
    print(y);
}
"""
# should print:
# 10
# 20

code2 = """
int x = 10;

{
    int x = 20;
    print(x);
}

print(x);
"""
# should print:
# 20
# 10

lexer = Lexer(code2)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse_program()

interpreter = Interpreter(program)
interpreter.interpret()



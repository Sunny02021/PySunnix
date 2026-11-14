
import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

code = """
int x = 10;

{
    x = 20;
    print(x);
}

print(x);
"""
# 20
# 20

code2 = """
{
    int y = 42;
}

print(y);
"""
# NameError

lexer = Lexer(code2)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse_program()

interpreter = Interpreter(program)
interpreter.interpret()



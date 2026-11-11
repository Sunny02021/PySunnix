
import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

code = """
int idade = 20;
int resultado = 10 + 5;
float altura = 1.75;
resultado = 20;
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse_program()

interpreter = Interpreter(program)
interpreter.interpret()

print(interpreter.variables)

#for statement in program.statements:
#    expression = statement.expression
#    result = interpreter.evaluate(expression.args[0])
#    print(result)

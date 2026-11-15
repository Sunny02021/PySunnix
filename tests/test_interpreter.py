import sys

sys.path.insert(0, "src/sunnix")

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

code = """
func greet() {
    print("Hello!");
}

func main() {
    int result = greet();
    print(result);
}

main();
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse_program()

interpreter = Interpreter(program)
interpreter.interpret()

# print(program)

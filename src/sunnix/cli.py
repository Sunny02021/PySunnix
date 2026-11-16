import sys
from pathlib import Path
from sunnix.lexer import Lexer
from sunnix.parser import Parser
from sunnix.interpreter import Interpreter

def run_file(filepath):
    path = Path(filepath)

    if not path.exists():
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    code = path.read_text(encoding="utf-8")

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    program = parser.parse_program()

    interpreter = Interpreter(program)
    interpreter.interpret()

def main():
    if len(sys.argv) < 2:
        print("Usage: sunnix <file.snx>")
        sys.exit(1)

    run_file(sys.argv[1])
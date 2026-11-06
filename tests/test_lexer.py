import sys

sys.path.insert(0, "src/sunlang")

from lexer import Lexer

code = """
int idade = 20;
float altura = 1.75;

// test

if (idade >= 18) {
    print("Over 18");
}
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

for token in tokens:
    print(
        f"{token.type.name:<15} "
        f"{str(token.value):<20} "
        f"Linha: {token.line}"
    )

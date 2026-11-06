import sys

sys.path.insert(0, "src/sunlang")

from lexer import Lexer

code = """
int age = 20;
float height = 1.75;

// test

if (age >= 18) {
    print("Over 18");
}
"""

code2 = """
int num1 = 10;
int num2 = 10;

int sum = num1 + num2;

print("Soma: " + sum);
"""

lexer = Lexer(code2)
tokens = lexer.tokenize()

for token in tokens:
    print(
        f"{token.type.name:<15} "
        f"{str(token.value):<10} "
        f"Linha: {token.line:<5}"
        f"Coluna: {token.column}"
    )

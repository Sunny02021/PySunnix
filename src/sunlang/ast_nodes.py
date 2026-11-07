from tokens import Token
from dataclasses import dataclass

class Expression:
    pass

@dataclass
class NumberLiteral(Expression):
    value: int | float

@dataclass
class BinaryExpression(Expression):
    left: Expression
    op: Token
    right: Expression

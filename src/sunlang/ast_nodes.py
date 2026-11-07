from tokens import Token
from dataclasses import dataclass

class Expression:
    pass

class Statement:
    pass

@dataclass
class NumberLiteral(Expression):
    value: int | float

@dataclass
class BinaryExpression(Expression):
    left: Expression
    op: Token
    right: Expression

@dataclass
class VariableDeclaration(Statement):
    var_type: Token
    name: Token
    initializer: Expression
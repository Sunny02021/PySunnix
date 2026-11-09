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
class BooleanLiteral(Expression):
    value: bool

@dataclass
class BinaryExpression(Expression):
    left: Expression
    op: Token
    right: Expression

@dataclass
class UnaryExpression(Expression):
    op: Token
    operand: Expression

@dataclass
class VariableDeclaration(Statement):
    var_type: Token
    name: Token
    initializer: Expression

@dataclass
class Assignment(Statement):
    name: Token
    value: Expression

@dataclass
class Program:
    statements: list[Statement]

@dataclass
class BlockStatement(Statement):
    statements: list[Statement]

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_branch: BlockStatement
    else_branch: BlockStatement | None
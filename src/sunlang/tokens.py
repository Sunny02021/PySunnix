"""tokens.py
Muitos comentarios aqui são só identificacoes pra
mim mesmo
"""

from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # literais
    NUMBER = auto()
    STRING = auto()

    # identificsdores
    IDENTIFIER = auto()

    # palavrss reservadas
    INT = auto()
    FLOAT = auto()
    FUNC = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    TRUE = auto()
    FALSE = auto()

    # ops
    PLUS = auto() # +
    MINUS = auto() # -
    MULTIPLY = auto() # *
    DIVIDE = auto() # /

    EQUAL = auto() # =
    EQUAL_EQUAL = auto() # ==
    NOT_EQUAL = auto() # !=

    GREATER = auto() # >
    LESS = auto() # <
    GREATER_EQUAL = auto() # >=
    LESS_EQUAL = auto() # <=

    # simbolos
    SEMICOLON = auto() # ;
    COMMA = auto() # ,
    DOT = auto() # .

    LEFT_PAREN = auto() # (
    RIGHT_PAREN = auto() # )

    LEFT_BRACE = auto() # {
    RIGHT_BRACE = auto() # }

    # controle
    EOF = auto() # end of file

@datatype
class Token:
    type: TokenType # categoris do token
    value: object # conteudo encontrado
    line: int # linha em que aparece
    column: int # coluna em q aparece
    # guardar linha e coluna serve para reportar erros

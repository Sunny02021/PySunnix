from dataclasses import dataclass

@dataclass
class ReturnException(Exception):
    value: object
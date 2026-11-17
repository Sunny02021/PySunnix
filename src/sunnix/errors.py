from dataclasses import dataclass

@dataclass
class ReturnException(Exception):
    value: object

@dataclass
class BreakException(Exception):
    value: object
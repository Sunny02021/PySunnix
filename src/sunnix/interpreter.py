class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, program):
        for statement in program.statements:
            pass
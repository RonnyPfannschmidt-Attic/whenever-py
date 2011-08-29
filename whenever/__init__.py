
from .parse import parse, parse_command
from .eval import Evaluator
from pypy.rlib.rrandom import Random

random = Random()


class Runner(object):
    __slots__ = 'statements', 'todo'
    def __init__(self, statements):
        assert isinstance(statements, dict)
        self.statements = statements
        self.todo = list(statements.keys())

    def run(self):

        while len(self.todo):
            rand = random.random()
            l = len(self.todo)

            number = int(l*rand)

            command = self.todo.pop(number)

            evaluator = Evaluator(self.todo)
            evaluator.handle(self.statements[command])
            if evaluator.keep:
                self.todo.append(number)

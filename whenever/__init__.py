
from .parse import parse, parse_command
from .eval import Evaluator
from pypy.rlib.rrandom import Random

random = Random(200)


class Runner(object):
    __slots__ = 'statements', 'todo'
    def __init__(self, statements):
        self.statements = statements
        items = statements.keys()
        self.todo = {}
        for i in range(len(items)):
            self.todo[items[i]] = 1

    
    def has_work(self):
        items = self.todo.keys()
        for i in range(len(items)):
            if self.todo[items[i]]:
                return True
        return False

    def run(self):
        i = 1
        while self.has_work():
            rand = random.random()
            keys = [x for x, y in self.todo.items() if y]
            l = len(keys)

            number = int(l*rand)

            command = keys[number]
            tree = self.statements[command]
            #print tree

            evaluator = Evaluator(self.todo)
            evaluator.execute(tree)
            if not evaluator.keep:
                if self.todo[command] > 0:
                    self.todo[command] -= 1

            if i%1000 == 0:
                print todo

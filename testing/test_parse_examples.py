import py
from whenever import parse

def test_parse_example():
    file = py.path.local(__file__).join('../../examples/fib.when')
    parse(str(file))

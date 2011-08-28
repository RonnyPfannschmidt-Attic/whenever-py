import py
from whenever import parse
examples = py.path.local(__file__).join('../../examples/')

def pytest_generate_tests(metafunc):
    for path in examples.visit('*.when'):
        metafunc.addcall(id=path.basename, funcargs={'path': path})

def test_parse_example(path):
    parse(str(path))

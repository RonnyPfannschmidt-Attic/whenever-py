import py
from whenever import parse, Runner
examples = py.path.local(__file__).join('../../examples/')

def pytest_generate_tests(metafunc):
    for path in examples.visit('*.when'):
        metafunc.addcall(id=path.basename, funcargs={'path': path})

def test_parse_example(path):
    parse(str(path))


def test_run_example(path):
    statements = parse(str(path))
    if path.basename == 'fib.when':
        py.test.xfail('logic error')

    runner = Runner(statements)
    runner.run()


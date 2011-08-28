from whenever import parse_command
commands = [
    '1;',
    '1#2;',
    'print(42);',
    '4,-3,7;',
    'print("a");',
    'defer (3 || 6) 1,3;',
    'defer (1) again (2) 3;',
    'defer (3 || N(1)<=N(2) || N(7)>99) 2#N(1),3,7;',
    'again (1) defer (3 || N(1)<=N(2) || N(7)>99) 2#N(1),3,7;',
    'defer (3 || N(1)<=N(2));',
    'print(N(1)+N(2));',
    'defer (5) print(N(1)+N(2));',
    'defer (5) print(1+1);',
    'defer (N(1) + N(3));',
]


def pytest_generate_tests(metafunc):
    for command in commands:
        metafunc.addcall(id=command, funcargs={"command": command})

def test_parse_command(command):
    try:
        parse_command(command)
    except Exception, e:
        if not hasattr(e, 'nice_error_message'):
            raise
        print e.nice_error_message()
        print command
        print ' '*e.args[0].i + '^'
        raise


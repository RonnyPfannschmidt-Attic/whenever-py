from whenever import parse_command
commands = [
    'defer (1) again (2) 3;',
    'again (1) defer (3 || N(1)<=N(2) || N(7)>99) 2#N(1),3,7;'
]


def pytest_generate_tests(metafunc):
    for command in commands:
        metafunc.addcall(id=command, funcargs={"command": command})

def test_parse_command(command):
    try:
        parse_command(command)
    except Exception, e:
        print e.nice_error_message()
        print command
        print ' '*e.args[0].i + '^'
        raise


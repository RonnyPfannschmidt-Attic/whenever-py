
from whenever import parse, Runner

def target(*args):
    return main, None

def main(args):
    if len(args) < 2:
        print 'missing arg'
        return 1

    cmd = args[1]
    try:
        statements = parse(cmd)
    except OSError, e:
        print 'cant parse:', cmd, 'os error', e.errno
        return 1
    runner = Runner(statements)
    runner.run()

    return 0


if __name__ == '__main__':
    import sys
    main(sys.argv)


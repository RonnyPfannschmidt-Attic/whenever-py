from pypy.rlib.streamio import open_file_as_stream

from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function



def parse(filename):
    result = {}

    fp = open_file_as_stream(filename)
    while True:
        line = fp.readline()
        number, commands = parseline(line)
        assert number not in result
        result[number] = commands



def parseline(line):
    number_str, commands = line.split(' ', 1)
    print commands
    try:
        return int(number_str), parse_command(commands[:-1])
    except Exception, e:
        print e.args[0], e.nice_error_message()
        print commands
        raise

regexs, rules, ToAST = parse_ebnf(
"""
IGNORE: " ";
DECIMAL: "0|[1-9][0-9]*";

command:  op ";";
op: action+ statements | statements | action+;


number: DECIMAL;
math: number;

compare: ">" | ">=" | "<" | "<=";
bool: math "||" math | math compare math;
function: "N" "(" expr ")";
expr: bool | math | function;

statement: expr "#" expr | expr;
statements: (statement ",")* statement;

action_name: "print" | "defer" | "again" | "forget";
action: action_name "(" expr ")";

""")

parse_command = make_parse_function(regexs, rules)


class Command(object):
    def __init__(self, tree):
        self.tree = tree


class Runner(object):
    def __init__(self, statements):
        self.statements = statements
    def run(self):
        pass

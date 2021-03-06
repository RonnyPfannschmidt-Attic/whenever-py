
from pypy.rlib.streamio import open_file_as_stream

from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from pypy.rlib.parsing.deterministic import LexerError
from pypy.rlib.parsing.parsing import ParseError


def parse(filename):
    result = {}

    fp = open_file_as_stream(filename)
    while True:
        line = fp.readline()
        if len(line) == 0:
            break
        number, commands = parseline(line)
        #commands.view()
        assert number not in result
        result[number] = commands
    return result


def parseline(line):
    number_str, commands = line.split(' ', 1)
    try:
        return int(number_str), parse_command(commands[:-1])
    except LexerError, e:
        print e.args[0], e.nice_error_message()
        print commands
        print ' ' * e.args[2].i + '^'
        raise
    except ParseError, e:
        print e.args[0], e.nice_error_message()
        print commands
        print ' ' * e.args[0].i + '^'
        raise

regexs, rules, ToAST = parse_ebnf(
"""
IGNORE: " ";
DECIMAL: "0|[1-9][0-9]*";
STRING: "\\"[^\\\\"]*\\"";

RPAR: "\)";
LPAR: "\(";
PLUS: "\+";
STAR: "\*";
FUNC: "N";

EQ: "==";
LT: "<";
GT: ">";
LTE: "<=";
GTE: ">=";

SHARP: "#";
COMMA: ",";
SEMICOLON: ";";

OR: "\|\|";
AND: "&&";

command:  >op<  [SEMICOLON] ;
op: action+ statements | action+ | statements;



integer: <DECIMAL> | "-" DECIMAL;
number: <integer>| <function> | <STRING>;

statement: integer [SHARP] expr | integer;
statements: (statement [COMMA])* statement;



function: ["N"] [LPAR] expr [RPAR];

addition: (number [PLUS])* number;
expr: <addition>;

comparisation: EQ | LT | GT | LTE | GTE;
compare: expr >comparisation< expr;


bool: <compare> | >expr<;
chain: AND |OR;
boolean: (bool >chain<)* bool;


ACTION: "defer|again|forget";
PRINT: "print";
action: ACTION [LPAR] boolean [RPAR] | [PRINT] [LPAR] expr [RPAR];

""")

parse_function = make_parse_function(regexs, rules)


def parse_command(command):
    parse_tree = parse_function(command)
    to_ast = ToAST()
    tree = to_ast.transform(parse_tree)
    #tree.view()
    return tree

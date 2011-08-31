from pypy.rlib.parsing.tree import Nonterminal
from pypy.rlib.objectmodel import specialize


class W_Object(object):
    __slots__ = ()


class W_Int(W_Object):
    __slots__ = 'intval',
    def __init__(w_self, intval):
        w_self.intval = intval

    def __repr__(self):
        return '(int %s)' % self.intval

class W_String(W_Object):
    __slots__ = 'strval',
    def __init__(w_self, strval):
        w_self.strval = strval

class W_Action(W_Object):
    __slots__ = 'name',
    def __init__(w_self, name):
        w_self.name = name



class W_Compare(W_Object):
    __slots__ = 'symbol',

    mapping = {
        'EQ': lambda x,y: x==y,
        'LT': lambda x,y: x<y,
        'GT': lambda x,y: x>y,
        'LTE': lambda x,y: x<=y,
        'GTE': lambda x,y: x>=y,
    }

    def __init__(w_self, op):
        w_self.symbol = op

    def op(self, a, b):
        call = self.mapping[self.symbol](a,b)


class W_Chain(W_Object):
    __slots__ = 'op',
    def __init__(w_self, op):
        w_self.op = op


class W_Bool(W_Object):
    __slots__ = 'value',
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return str(self.value)

class Paused(Exception):
    pass

class Evaluator(object):
    __slots__ = 'todo', 'resultstate', 'stack', 'node_stack', 'keep'

    def __init__(self, todo):
        self.todo = todo
        self.stack = []
        self.node_stack = []
        self.keep = False


    def push(self, item):
        self.stack.append(item)
    
    @specialize.arg(1)
    def pop(self, type):
        assert len(self.stack) > 0
        item = self.stack.pop()
        assert isinstance(item, type)
        return item

    def execute(self, node):
        try:
            self.handle(node)
        except Paused:
            pass
        except Exception:
            print node
            raise

    def handle(self, node):
        #print ' '*len(self.node_stack), node.symbol
        self.node_stack.append(node)
        if isinstance(node, Nonterminal):
            #print node.children
            for child in node.children:
                self.handle(child)


        #print self.stack
        #print [x.symbol for x in self.node_stack]
        #print ' '*(len(self.node_stack)-1), node.symbol, '!'
        if not node.symbol[0] == '_':
            handler = self.dispatch[node.symbol]
            handler(self, node)
        self.node_stack.pop()

    def ignore(self, node):
        pass

    def handle_ACTION(self, node):
        self.push(W_Action(node.token.source))

    def handle_DECIMAL(self, node):
        self.push(W_Int(int(node.token.source)))

    def handle_STRING(self, node):
        source = node.token.source
        l = len(source)
        assert l >= 2 # for the ""
        end = l-1
        assert end >=0
        striped = source[1:end]
        
        self.push(W_String(striped)) # unescape?

    

    def push_symbol(self, node):
        self.push(W_Compare(node.symbol))

    handle_GT = handle_LT = handle_GTE = \
            handle_LTE = handle_EQ = push_symbol

    def handle_OR(self, node):
        self.push(W_Chain('o'))

    def handle_AND(self, node):
        self.push(W_Chain('a'))

    def handle_integer(self, node):
        if len(node.children) == 2:
            i = self.pop(W_Int)
            i.intval = -i.intval
            self.push(i)

    def handle_compare(self, node):
        b = self.pop(W_Int)
        comp = self.pop(W_Compare)
        a = self.pop(W_Int)

        op = comp.op
        an = a.intval
        bn = b.intval
        result = op(an, bn)
        self.push(W_Bool(bool(result)))

    def handle_statement(self, node):
        if len(node.children) == 1:
            count = 1
        else:
            count = self.pop(W_Int).intval
        number = self.pop(W_Int).intval
        if number < 0:
            count = -count
            number = -number
        self.todo[number] = max(self.todo[number] + count, 0)




    def handle_addition(self, node):
        if len(node.children) == 1:
            return
        b = self.stack.pop()
        a = self.stack.pop()

        if isinstance(a, W_Int) and isinstance(b, W_Int):
            self.stack.append(W_Int(a.intval+b.intval))
        elif isinstance(a, W_String) and isinstance(b, W_String):
            self.stack.append(W_String(a.strval + b.strval))
        elif isinstance(a, W_Int) and isinstance(b, W_String):
            self.stack.append(W_String(str(a.intval) + b.strval))
        elif isinstance(a, W_String) and isinstance(b,  W_Int):
            self.stack.append(W_String(a.strval + str(b.intval)))
        else:
            raise ValueError


    def handle_function(self, node):
        #XXX: its n
        w_int = self.pop(W_Int)
        self.push(W_Int(self.todo[w_int.intval]))

    def handle_bool(self, node):
        val = self.stack.pop()
        if isinstance(val, W_Int):
            number = self.todo[val.intval]
            self.push(W_Bool(bool(number)))
        else:
            self.push(val)

    def handle_boolean(self, node):
        if len(node.children) == 1:
            return

        b = self.pop(W_Bool).value
        op = self.pop(W_Chain).op
        a = self.pop(W_Bool).value

        if op == 'a':
            res = a and b
        elif op == 'o':
            res = a or b
        else:
            raise ValueError
        self.push(W_Bool(res))

    def handle_statements(self, node):
        pass

    handle_number = handle_op = ignore

    def handle_action(self, node):
        if len(self.stack) >=2 and isinstance(self.stack[-2], W_Action):
            truth = self.pop(W_Bool).value
            action = self.pop(W_Action).name

            if not truth:
                return

            if  action == 'defer':
                self.keep = True
                raise Paused
            elif action=='forget':
                self.keep = False
                raise Paused
            elif action=='again':
                self.keep = True
        else:
            maybe_text = self.stack.pop()
            if isinstance(maybe_text, W_Int):
                print maybe_text.intval
            elif isinstance(maybe_text, W_String):
                print maybe_text.strval



    def handle_command(self, node):
        pass

    dispatch = {}
    for name, function in locals().items():
        if name.startswith('handle_'):
            dispatch[name[7:]] = function

    del name, function


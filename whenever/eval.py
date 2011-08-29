from pypy.rlib.parsing.tree import Nonterminal



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
    __slots__ = 'op',
    def __init__(w_self, op):
        w_self.op = op


class W_Bool(W_Object):
    __slots__ = 'value',
    def __init__(self, value):
        self.value = value

class Evaluator(object):
    __slots__ = 'todo', 'resultstate', 'stack', 'node_stack', 'keep'

    def __init__(self, todo):
        self.todo = todo
        self.stack = []
        self.node_stack = []
        self.keep = False

    def handle(self, node):
        #print ' '*len(self.node_stack), node.symbol
        self.node_stack.append(node)
        if isinstance(node, Nonterminal):
            #print node.children
            for child in node.children:
                self.handle(child)


        #print self.stack
        #print [x.symbol for x in self.node_stack]
        if not node.symbol[0] == '_':
            handler = self.dispatch[node.symbol]
            handler(self, node)
        self.node_stack.pop()

    def ignore(self, node):
        pass

    handle_COMMA = handle_LPAR = handle_RPAR = \
            handle_SEMICOLON = handle_PRINT = handle_PLUS = \
            handle_SHARP = ignore

    def handle_ACTION(self, node):
        self.stack.append(W_Action(node.token.source))

    def handle_DECIMAL(self, node):
        self.stack.append(W_Int(int(node.token.source)))

    def handle_STRING(self, node):
        self.stack.append(W_String(node.token.source[1:-1])) # unescape?

    def handle_LT(self, node): self.stack.append(W_Compare(lambda a,b: a<b))
    def handle_GT(self, node): self.stack.append(W_Compare(lambda a,b: a>b))
    def handle_LTE(self, node): self.stack.append(W_Compare(lambda a,b: a<=b))

    def handle_OR(self, node): self.stack.append(W_Compare(lambda a,b: a | b))

    def handle_integer(self, node):
        if len(node.children) == 2:
            w_int = self.stack[-1]
            assert isinstance(w_int, W_Int)
            w_int.intval = -w_int.intval

    handle_comparisation = handle_chain = ignore
    def handle_compare(self, node):
        a = self.stack.pop()
        comp = self.stack.pop()
        b = self.stack.pop()

        assert isinstance(a, W_Int)
        assert isinstance(b, W_Int)
        assert isinstance(comp, W_Compare)
        self.stack.append(W_Bool(comp.op(a.intval, b.intval)))

    def handle_statement(self, node):
        def remove(n):
            i = self.todo.index(n)
            if i >= 0:
                del self.todo[i]

        if len(node.children) == 1:
            number = self.stack.pop()
            n = number.intval
            if n < 0:
                remove(-n)
            else:
                self.todo.append(n)
        else:
            b_count = self.stack.pop()
            b_number = self.stack.pop()
            count = b_count.intval
            number = b_number.intval
            if number < 0:
                count = -count
                number = -number
            if count < 0:
                for i in range(count):
                    remove(number)
            else:
                for i in range(count):
                    self.todo.append(number)



    def handle_addition(self, node):
        if len(node.children) == 1:
            return
        #XXX STRINGS
        a = self.stack.pop()
        b = self.stack.pop()
        assert isinstance(a, W_Int)
        assert isinstance(b, W_Int)
        self.stack.append(W_Int(a.intval+b.intval))


    def handle_function(self, node):
        #XXX: its n
        w_int = self.stack.pop()
        assert isinstance(w_int, W_Int)
        count = 0
        for i in range(len(self.todo)):
            if self.todo[i] == w_int.intval:
                count += 1
        self.stack.append(W_Int(count))

    def handle_expr(self, node):
        pass

    def handle_bool(self, node):
        val = self.stack.pop()
        if isinstance(val, W_Int):
            self.stack.append(W_Bool(bool(val.intval)))
        else:
            self.stack.append(val)

    def handle_boolean(self, node):
        pass

    def handle_statements(self, node):
        pass

    handle_number = handle_op = ignore

    def handle_action(self, node):
        if len(self.stack) >=2 and isinstance(self.stack[-2], W_Action):
            truth = self.stack.pop()
            assert isinstance(truth, W_Bool)
            action = self.stack.pop()
            if not truth.value:
                return

            if  action == 'defer':
                self.keep = True
                raise StopIteration
            elif action=='forget':
                self.keep = False
                raise StopIteration
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


# LogicAPI without any list functionality

from collections import OrderedDict
import operator

from LogicAPI.constants import BaseClass
from LogicAPI.utils import *


kb = OrderedDict()

def fromPythonArg(arg):
    if isinstance(arg, AnonVar):
        return IntVar()
    elif is_class(arg, BaseClass.Var):
        arg.rank = 0
        return arg
    elif is_term(arg):
        return arg
    else:
        for t in supportedConstTypes:
            if isinstance(arg, t):
                return Const(arg)
        raise Exception("Unsupported constant type of " + repr(arg))


class Term(object):
    base_class = BaseClass.Term

    def __init__(self, *args):
        self.functor = self.__class__
        self.args = [fromPythonArg(arg) for arg in args]

    def __le__(self, other):
        if is_term(other):
            other = Terms(other)
        key = (self.functor, len(self.args))
        if key in kb:
            kb[key].append((self, other))
        else:
            kb[key] = [(self, other)]

    def __pos__(self):
        key = (self.functor, len(self.args))
        if key in kb:
            kb[key].append((self, Terms()))
        else:
            kb[key] = [(self, Terms())]

    def __repr__(self):
        return self.functor.__name__ + \
            '(' + ','.join([repr(arg) for arg in self.args]) + ')'

    def __invert__(self):
        return ~Terms(self)

    def __and__(self, other):
        return Terms(self) & other

    def unifyWith(self, other, env):
        if is_class(other, BaseClass.Var) or is_class(other, BaseClass.Func):
            return other.unifyWith(self, env)
        if is_term(other):
            match_functor = self.functor == other.functor
            match_length = len(self.args) == len(other.args)
            if match_functor and match_length:
                for i in range(len(self.args)):
                    arg1 = self.args[i].applyEnv(env)
                    arg2 = other.args[i].applyEnv(env)
                    if not arg1.unifyWith(arg2, env):
                        return False
                return True
        return False

    def applyEnv(self, env):
        res = self.__class__.__new__(self.__class__)
        res.functor = self.functor
        res.args = [arg.applyEnv(env) for arg in self.args]
        return res

    def query(self):
        key = (self.functor, len(self.args))
        if key not in kb:
            raise Exception('Undefined procedure: ' +
                            str(self.functor) + '/' + str(len(self.args)))
        rules = kb[key]
        for left, rights in rules:
            int_names = {}
            left = self.unique(int_names, left)
            if rights:
                rights_new = Terms()
                rights_new.inverted = rights.inverted
                rights_new += [self.unique(int_names, right)
                               for right in rights]
                rights = rights_new
            env = {}
            if not self.unifyWith(left, env):
                continue
            for res in rights.query(env):
                yield res
            if rights.cut:
                return

    def __eq__(self, other):
        return Eq(self, other)

    def unique(self, names, term):
        if is_class(term, BaseClass.Const):
            return term
        if is_class(term, BaseClass.Terms):
            res = Terms()
            res.inverted = term.inverted
            res.cut = term.cut
            list.__init__(res, [self.unique(names, t) for t in term])
            return res
        else:
            args = []
            for i in range(len(term.args)):
                if is_term(term.args[i]):
                    args.append(self.unique(names, term.args[i]))
                elif is_class(term.args[i], BaseClass.Var):
                    if Key(term.args[i]) in names:
                        args.append(names[Key(term.args[i])])
                    else:
                        intVar = IntVar()
                        names[Key(term.args[i])] = intVar
                        args.append(intVar)
            res = term.__class__.__new__(term.__class__)
            res.functor = term.functor
            res.args = args
            return res

class Cut(Term):
    __metaclass__ = Singleton

class Const(Term):
    args = []
    base_class = BaseClass.Const

    def __init__(self, val):
        self.functor = val

    def __repr__(self):
        return repr(self.functor)

    def unifyWith(self, other, env):
        if is_class(other, BaseClass.Var) or is_class(other, BaseClass.Func):
            return other.unifyWith(self, env)
        if is_class(other, BaseClass.Const):
            return self.functor == other.functor
        return False

    def applyEnv(self, env):
        return self


class Object(Const):
    __metaclass__ = ObjectType


class Terms(list):
    base_class = BaseClass.Terms

    def __init__(self, term=None):
        if term:
            list.__init__(self, [term])
        else:
            list.__init__(self)
        self.inverted = False
        self.cut = False

    def __and__(self, other):
        if self.inverted:
            self = Terms(self)
        if is_class(other, BaseClass.Terms):
            if other.inverted:
                other = Terms(other)
            self += other
        elif is_term(other):
            self.append(other)
        else:
            raise Exception(repr(other) + ' is not a legal term')
        return self

    def __invert__(self):
        if self.inverted:
            self = Terms(self)
        self.inverted = True
        return self

    def __repr__(self):
        res = ' & '.join([repr(term) if is_term(term)
                          else '(' + repr(term) + ')' for term in self])
        if self.inverted:
            return '~(' + res + ')'
        else:
            return res

    def query(self, env={}):
        index = 0
        prev = None
        while index >= 0:
            if index == len(self):
                if self.inverted:
                    return
                yield env
                if prev is None:
                    return
                state = prev
                index -= 1
            elif isinstance(self[index], Cut):
                index += 1
                self.cut = True
                prev = None
                continue
            else:
                state = State(self[index], env, prev)
            env = state.generate()
            while env is None:
                state = state.prev
                index -= 1
                if state is None:
                    if self.inverted:
                        yield {}
                    return
                env = state.generate()
            index += 1
            prev = state


var_id = 0


class IntVar(object):
    rank = 0
    base_class = BaseClass.Var

    def __init__(self):
        global var_id
        self.id = var_id
        var_id += 1

    def __repr__(self):
        return '_G' + str(self.id)

    def __eq__(self, another):
        return Eq(self, another)

    def __hash__(self):
        return object.__hash__(self)

    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        return Add(other, self)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        return Mul(other, self)

    def __div__(self, other):
        return Div(self, other)

    def __rdiv__(self, other):
        return Div(other, self)

    def __mod__(self, other):
        return Mod(self, other)

    def __rmod__(self, other):
        return Mod(other, self)

    def __pow__(self, other):
        return Pow(self, other)

    def __rpow__(self, other):
        return Pow(other, self)

    def __lt__(self, other):
        return LT(self, other)

    def __le__(self, other):
        return LE(self, other)

    def __ne__(self, other):
        return NE(self, other)

    def __ge__(self, other):
        return GE(self, other)

    def __gt__(self, other):
        return GT(self, other)

    def unifyWith(self, other, env):
        if is_class(other, BaseClass.Func):
            return other.unifyWith(self, env)
        self = self.applyEnv(env)
        other = other.applyEnv(env)
        if self is other:
            return True
        if is_class(other, BaseClass.Var):
            if self.rank < other.rank:
                env[Key(self)] = other
            elif self.rank > other.rank:
                env[Key(other)] = self
            else:
                env[Key(self)] = other
                other.rank += 1
        else:
            env[Key(self)] = other
        return True

    def applyEnv(self, env):
        if Key(self) in env:
            env[Key(self)] = env[Key(self)].applyEnv(env)
            return env[Key(self)]
        return self


class Var(IntVar):
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception(repr(name) + ' is not a string!')
        if name.startswith('_G'):
            raise Exception('The name of variable cannot start with \'_G\'')
        self.name = name

    def __repr__(self):
        return self.name


class AnonVar(object):
    __metaclass__ = Singleton

    def __repr__(self):
        return '_'

    def __radd__(self, other):
        if isinstance(other, list):
            return List(other, IntVar())


_ = AnonVar()


class Func(Term):
    base_class = BaseClass.Func

    def function(self, *args):
        raise Exception('function in ' + self + ' is not defined')

    def __init__(self, *args):
        print(args, self.function)
        self.functor = self.function
        self.args = [fromPythonArg(arg) for arg in args]

    def __repr__(self):
        return self.__class__.__name__ + '.' + Term.__repr__(self)

    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        return Add(other, self)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        return Mul(other, self)

    def __div__(self, other):
        return Div(self, other)

    def __rdiv__(self, other):
        return Div(other, self)

    def __mod__(self, other):
        return Mod(self, other)

    def __rmod__(self, other):
        return Mod(other, self)

    def __pow__(self, other):
        return Pow(self, other)

    def __rpow__(self, other):
        return Pow(other, self)

    def __lt__(self, other):
        return LT(self, other)

    def __le__(self, other):
        return LE(self, other)

    def __ne__(self, other):
        return NE(self, other)

    def __ge__(self, other):
        return GE(self, other)

    def __gt__(self, other):
        return GT(self, other)

    def __eq__(self, other):
        return Eq(self, other)

    def eval(self):
        for i in range(len(self.args)):
            cur_arg = self.args[i]
            if cur_arg.base_class == BaseClass.Var:
                raise Exception(
                    'There are variables in the function: ' + str(self))
            elif cur_arg.base_class == BaseClass.Func:
                self.args[i] = cur_arg.eval()
            elif cur_arg.base_class == BaseClass.Const:
                self.args[i] = cur_arg.functor
        return self.functor(*self.args)

    def unifyWith(self, other, env):
        return other.unifyWith(fromPythonArg(self.applyEnv(env).eval()), env)

    def query(self):
        self.eval()
        yield {}


class format(Func):
    def function(self, form, *args):
        print(str(form) % args)


class BoolFunc(Func):
    def query(self):
        if self.eval():
            yield {}


class Add(Func):
    function = operator.add


class Sub(Func):
    function = operator.sub


class Mul(Func):
    function = operator.mul


class Div(Func):
    function = operator.truediv


class Mod(Func):
    function = operator.mod


class Pow(Func):
    function = operator.pow


class LT(BoolFunc):
    function = operator.lt


class LE(BoolFunc):
    function = operator.le


class GE(BoolFunc):
    function = operator.ge


class GT(BoolFunc):
    function = operator.gt


class Eq(Term):
    def query(self):
        env = {}
        if self.args[0].unifyWith(self.args[1], env):
            yield env


class NE(Term):
    def query(self):
        if not self.args[0].unifyWith(self.args[1], {}):
            yield {}


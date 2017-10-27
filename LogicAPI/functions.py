from collections import OrderedDict, defaultdict

from LogicAPI.constants import BaseClass
from LogicAPI.utils import *


class Result(object):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        output = [repr(k) + ' = ' + repr(v) for k, v in self.data.items()]
        return '{' + ', '.join(output) + '}'

    def __getitem__(self, var):
        return toPythonArg(self.data[Key(var)])

    def __contains__(self, var):
        return Key(var) in self.data


def variables_list(term, env):
    if is_class(term, BaseClass.Var) and not term.name.startswith('_'):
        env.append(term)
    elif is_class(term, BaseClass.Terms):
        for t in term:
            variables_list(t, env)
    elif is_class(term, BaseClass.Term):
        for t in term.args:
            variables_list(t, env)


def query(x):
    print(type(x))
    for env in x.query():
        l = []
        variables_list(x, l)
        res = OrderedDict()
        for var in l:
            if Key(var) not in res:
                res[Key(var)] = var.applyEnv(env)
        rev = defaultdict(list)
        for key in res:
            if is_class(res[key], BaseClass.Var):
                rev[Key(res[key])].append(key.var)
        for l in rev.values():
            for i in range(1, len(l)):
                res[Key(l[i - 1])] = l[i]
            del res[Key(l[len(l) - 1])]
        yield Result(res)


def toPythonArg(arg):
    if is_class(arg, BaseClass.Const):
        arg = arg.functor
    return arg

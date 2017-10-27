import numbers

from LogicAPI.constants import *

supportedConstTypes = set()
supportedConstTypes.add(type(None))
supportedConstTypes.add(numbers.Number)
supportedConstTypes.add(str)
supportedConstTypes.add(bool)

def is_of_class(item, base_class):
    return item.base_class == base_class

def is_term_base(item):
    return (is_of_class(item, BaseClass.Term)
        or is_of_class(item, BaseClass.Func)
        or is_of_class(item, BaseClass.Const))


def joinEnv(env1, env2):
    env1 = env1.copy()
    env1.update(env2)
    return env1


class State(object):
    def __init__(self, term, env, prev):
        self.env = env
        if (is_term_base(term)):
            self.gen = term.applyEnv(env).query()
        elif is_of_class(term, BaseClass.Terms):
            self.gen = term.query(env)
        self.prev = prev

    def generate(self):
        try:
            return joinEnv(self.env, next(self.gen))
        except StopIteration:
            return None


class Key(object):
    def __init__(self, var):
        self.var = var

    def __hash__(self):
        return hash(self.var)

    def __eq__(self, other):
        return isinstance(other, Key) and self.var is other.var

    def __repr__(self):
        return repr(self.var)

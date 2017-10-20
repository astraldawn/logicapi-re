var_id = 0


class Var(object):
    rank = 0

    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception(repr(name) + ' is not a string!')
        if name.startswith('_G'):
            raise Exception('The name of variable cannot start with \'_G\'')
        self.name = name

    def __repr__(self):
        return self.name


class IntVar(Var):
    def __init__(self):
        global var_id
        self.id = var_id
        var_id += 1

    def __repr__(self):
        return '_G' + str(self.id)


class Singleton(type):
    _instance = None

    def __call__(cls):
        if cls._instance is None:
            cls._instance = type.__call__(cls)
        return cls._instance


class AnonVar(object):
    __metaclass__ = Singleton

    def __repr__(self):
        return '_'

    # def __radd__(self, other):
    #     if isinstance(other, list):
    #         return List(other, IntVar())

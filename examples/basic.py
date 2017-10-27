import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from LogicAPI.reduceAPI import Term, Var, Cut, Object
from LogicAPI.functions import query

# from LogicAPI.sampleAPI import Term, Var, Cut, Object, query

class f(Term):
    pass  # define predicates


class g(Term):
    pass


class h(Term):
    pass


X = Var('X')
+f(1)  # define facts
+f(2)
+g(4)
+g(5)
+g(6)
+h(4)
f(X) <= g(X) & h(X)  # define rules
print('query f(X):\n\t', list(query(f(X))))  # lists all solutions to the query
print('query f(X) & Cut():\n\t', list(query(f(X) & Cut())))

A = Var('A')
B = Var('B')
C = Var('C')
D = Var('D')
E = Var('E')
F = Var('F')
+f(A, C, C, E, E, 0)
print('query f(B, C, F, E, 0, 0):\n\t', list(query(f(B, C, F, E, 0, 0))))


class path(Term):
    pass


class arc(Term):
    pass


From = Var('From')
To = Var('To')
I = Var('I')
L = Var('L')
L2 = Var('L2')

path(From, To) <= arc(From, To)
path(From, To) <= arc(From, I) & path(I, To)
+arc('a', 'b')
+arc('b', 'c')
+arc('c', 'd')
+arc('b', 'e')
+arc('c', 'f')
print('query path(From, To):\n\t', list(query(path(From, To))))


class parent(Term):
    pass


class grandparent(Term):
    pass


X = Var('X')
Y = Var('Y')
Z = Var('Z')

+parent('pete', 'ian')
+parent('ian', 'peter')
+parent('ian', 'lucy')
+parent('lou', 'pete')
+parent('lou', 'pauline')
+parent('cathy', 'ian')

grandparent(X, Y) <= parent(X, Z) & parent(Z, Y)
print('query grandparent(X, Y):\n\t', list(query(grandparent(X, Y))))


class Person(Object):  # enables object-oriented paradigm
    class age(Term):
        pass  # define predicate in class

    def __init__(self, name, age):
        self.name = name
        +self.age(self, age)

    def __repr__(self):
        return self.name


a = Person('a', 15)
b = Person('b', 19)
c = Person('c', 13)
d = Person('d', 24)
e = Person('e', 16)
f = Person('f', 17)

print('query Person.age(X, A) & (A <= 18):\n\t',
      list(query(Person.age(X, A) & (A <= 18))))

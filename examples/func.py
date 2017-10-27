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

print('query f(X):\n\t', list(query(f(X) & (X <= 1))))

print('query f(X):\n\t', list(query((X <= 1) & f(X)))) # Fails
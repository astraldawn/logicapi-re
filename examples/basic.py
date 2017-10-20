import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from LogicAPI.sampleAPI import Term, Var, query, Cut


class f(Term):
    pass  # define predicates


X = Var('X')
+f(1)
+f(4)
print('query f(X):\n\t', list(query(f(X))))  # lists all solutions to the query
print('query f(X) & Cut():\n\t', list(query(f(X) & Cut())))

print(list(query(f(X))))

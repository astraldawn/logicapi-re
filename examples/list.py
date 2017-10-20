import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from LogicAPI.sampleAPI import Var, Term, query


class f(Term):
    pass  # define predicates


A = Var('A')
B = Var('B')
C = Var('C')
D = Var('D')
E = Var('E')
F = Var('F')
+f(A, C, C, E, E, A)
print ('query f(B, C, F, E, 0, 0):\n\t', list(query(f(B, C, F, E, 0, 0))))

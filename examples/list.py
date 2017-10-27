import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from LogicAPI.reduceAPI import Var, Term, query, Cut, Func, _


class append(Term):
    pass


L = Var('L')
L2 = Var('L2')
L3 = Var('L3')
H = Var('H')
T = Var('T')
X = Var('X')
Y = Var('Y')

+append([], L, L)
append([H] + T, L2, [H] + L3) <= append(T, L2, L3)
print('query append([1,2], [4,6], L):\n\t',
      list(query(append([1, 2], [4, 6], L))))


class reverse(Term):
    pass


+reverse([], L, L)
reverse([H] + T, L, L2) <= reverse(T, L, [H] + L2)
reverse(L, L2) <= reverse(L, L2, [])
print('query reverse([4,5,6,\'a\'], L):\n\t',
      list(query(reverse([4, 5, 6, 'a'], L))))


# class reverse2(Term):
#     pass


# +reverse2([], [])
# reverse2([H] + T, L) <= reverse2(T, L2) & (L == L2 + [H])
# print('query reverse2([4,5,6,\'a\'], L):\n\t',
#       list(query(reverse2([4, 5, 6, 'a'], L))))


# class reverseFunc(Func):  # define functions
#     def function(self, l):
#         return l[::-1]


# class reverse3(Term):
#     pass


# +reverse3(L, reverseFunc(L))
# print('query reverse3([4,5,6,\'a\'], L):\n\t',
#       list(query(reverse3([4, 5, 6, 'a'], L))))


class member(Term):
    pass


+member(X, [X] + _)
member(X, [Y] + T) <= member(X, T)
print('query member(X,[1,2,3]) & ~member(X, [1,4,5]):\n\t',
      list(query(member(X, [1, 2, 3]) & ~member(X, [1, 4, 5]))))


class not_in(Term):
    pass


+not_in([], L, [])
not_in([X] + Y, L, [X] + L2) <= (~member(X, L)) & Cut() & not_in(Y, L, L2)
not_in([X] + Y, L, L2) <= not_in(Y, L, L2)
print('query not_in([1,2,3,4], [1], L):\n\t',
      list(query(not_in([1, 2, 3, 4], [1], L))))

from sympy import *
from itertools import product

from predicate import MetitEquation
from predicate import MetitPredicate
from predicate import get_derivs

t = Symbol('t')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

q = [('cont',)]

bad = False

system_def = {('cont',): {'flow': {x1.diff(t): x2,
                                   x2.diff(t): -sin(x1)-x2},
                          't': [],
                          'inv': []}}

initial_state = {'d': ('cont',), 'c': [str(MetitPredicate(*x)) for x in
                                       [(x1-0.1, '='),
                                        (x2, '='),
                                        (x1-2, '<')]]}
                                        
extra_constraints = ['X1<3', 'X1>-3', 'X2<5', 'X2>-5']
bad_state = MetitPredicate(x1-2, '>')


equations = [MetitEquation(x1),
             MetitEquation(x2),
             MetitEquation(x1-0.1),
             MetitEquation(x1-2)]

e5 = MetitEquation(system_def[('cont',)]['flow'][x2.diff(t)])
equations.extend(get_derivs(4, e5, system_def, ('cont',)))

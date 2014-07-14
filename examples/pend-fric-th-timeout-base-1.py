from sympy import *
from itertools import product

from predicate import MetitEquation
from predicate import MetitPredicate

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
                                        (x1-2, '<'),
                                        (8.9116 - 8.4428*cos(x1) + 4.2214*x2**2 + 4.2214 - 7,'<')]]}
                                        
extra_constraints = ['X1<3', 'X1>-3']
bad_state = []

equations = [MetitEquation(x1),
             MetitEquation(x2),
             MetitEquation(x1-0.1),
             MetitEquation(x1-2),
             MetitEquation(8.9116 - 8.4428*cos(x1) + 4.2214*x2**2 + 4.2214 - 7)]

# e5 = predicate.MetitEquation(system_def[('cont',)]['flow'][x2.diff(t)])
# equations.extend(predicate.get_derivs(4,e5,system_def,('cont',)))

from sympy import *
from itertools import product

t = Symbol('t')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

bad = False
q = [('cont',)]

system_def = {('cont',): {'flow': {x1.diff(t): x2,
                                   x2.diff(t): -9.8*sin(x1)},
                         't': [],
                         'inv': []}}

seed_predicates = [x1, x2, -9.8*sin(x1)]    
equations = [predicate.MetitEquation(n) for n in seed_predicates]

equations.extend(predicate.get_derivs(1,equations[-1],system_def,('cont',)))

#equations = [predicate.MetitEquation(x1),
#             predicate.MetitEquation(x2(t))]
#predicate.MetitEquation(1.90843655*sin(x1)**2 + 1.90843655*cos(x1)**2 - 3.916868466*cos(x1) + 0.19984*x2**2 + 0.0084319171,'t',deriv_dict,vars_dict,is_lyapunov=True)]




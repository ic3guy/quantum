from sympy import *
from itertools import product

t = Symbol('t')
X1 = Symbol('X1')
X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

q = [('cont',)]

bad = False

deriv_dict = {('cont',): {'flow': {x1.diff(t): x2,
                                  x2.diff(t): -9.8*sin(x1)},
                         't': [],
                         'inv': []}}

vars_dict = {x1 : X1, x2 : X2}
    
equations = [predicate.MetitEquation(x1,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x2,'t',deriv_dict,vars_dict)]
#predicate.MetitEquation(1.90843655*sin(x1)**2 + 1.90843655*cos(x1)**2 - 3.916868466*cos(x1) + 0.19984*x2**2 + 0.0084319171,'t',deriv_dict,vars_dict,is_lyapunov=True)]

e5 = predicate.MetitEquation(deriv_dict[('cont',)]['flow'][x2.diff(t)],'t',deriv_dict,vars_dict)
equations.extend(predicate.get_derivs(1,e5))


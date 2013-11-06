from sympy import *
from itertools import product

import predicate

t = Symbol('t')
X1 = Symbol('X1')
X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

q = [('cont',)]

bad = False
extra_constraints = ['X1<3.141', 'X1>-3.141']

system_def = {('cont',): {'flow': {x1.diff(t): x2,
                                  x2.diff(t): -9.8*sin(x1)},
                         't': [],
                         'inv': []}}

initial_state = {'d':('cont',),'c':['X1>10^-6','X2>10^-6','0.19984*X2^2 + 1.90843655*sin(X1)^2 + 1.90843655*cos(X1)^2 - 3.916868466*cos(X1) + 0.3084319171<-10^-6']}

equations = [predicate.MetitEquation(x1,'t',eq_num=0),
             predicate.MetitEquation(x2,'t',eq_num=1),
             predicate.MetitEquation(1.90843655*sin(x1)**2 + 1.90843655*cos(x1)**2 - 3.916868466*cos(x1) + 0.19984*x2**2 + 0.3084319171,'t',is_lyapunov=True,eq_num=2)]

lf1 = 1.90843655*sin(x1)**2 + 1.90843655*cos(x1)**2 - 3.916868466*cos(x1) + 0.19984*x2**2 + 0.3084319171

bad_state = None
#bad_state = predicate.MetitPredicate(lf1,'>')
#bad_state = predicate.MetitPredicate(x2-8,'>')

#e5 = predicate.MetitEquation(system_def[('cont',)]['flow'][x2.diff(t)],'t')
#equations.extend(predicate.get_derivs(2,e5,system_def,('cont',)))

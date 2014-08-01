from sympy import *
from itertools import product

import predicate

from predicate import MetitEquation
from predicate import MetitPredicate

t = Symbol('t')
# X1 = Symbol('X1')
# X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

q = [('cont',)]

bad = False

system_def = {('cont',): {'flow': {x1.diff(t): x2,
                                   x2.diff(t): -sin(x1)-x2},
                         't': [],
                         'inv': []}}

initial_state = {'d':('cont',),'c':['X1>0','X2>0',str(MetitPredicate(140.2141 - 127.418*cos(x1) + 63.709*x2**2 + 63.709 - 100,'<'))]}
bad_state = []
#extra_constraints = ['X1<3','X1>-3','X2<1','X2>-1']
extra_constraints = ['X1<3', 'X1>-3', 'X2<2', 'X2>-2']


#is_lyapunov looks nice

equations = [predicate.MetitEquation(x1),
             predicate.MetitEquation(x2),
             predicate.MetitEquation(140.2141 - 127.418*cos(x1) + 63.709*x2**2 + 63.709 - 100)]

             
# predicate.MetitEquation(1.90843655*sin(x1)**2 + 1.90843655*cos(x1)**2 - 3.916868466*cos(x1) + 0.19984*x2**2 - 0.0084319171,is_lyapunov=True),
# predicate.MetitEquation(1.90843655*sin(x1)**2 + 1.90843655*cos(x1)**2 - 3.916868466*cos(x1) + 0.19984*x2**2 - 4.3084319171,is_lyapunov=True)]

#bad_state = predicate.MetitPredicate(x2-8,'>')

# e5 = predicate.MetitEquation(system_def[('cont',)]['flow'][x2.diff(t)])
# equations.extend(predicate.get_derivs(2,e5,system_def,('cont',)))

#adding more derivatives, makes more generate that have to be proved, balance between the two

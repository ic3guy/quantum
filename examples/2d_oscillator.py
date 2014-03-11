from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
import abstraction
import predicate
from predicate import MetitPredicate

t = Symbol('t')
x = Function('x')(t)
y = Function('y')(t)
tau = Function('tau')(t)

q = [('m1',)]

bad = False
extra_constraints = ''

omega = 3.14
ax = 1
ay = 1.2

inv1 = x + 10
inv2 = y + 10

ddx = -ax * sin(omega * tau)
ddy = -ay * sin(omega * tau) * omega

equations = [predicate.MetitEquation(ddx),
             predicate.MetitEquation(ddy),
             predicate.MetitEquation(inv1),
             predicate.MetitEquation(inv2),
             predicate.MetitEquation(tau, oplist=['>', '=']),
             predicate.MetitEquation(x),
             predicate.MetitEquation(y),
             predicate.MetitEquation(tau - 10, oplist=['<', ]),
             predicate.MetitEquation(x - 10, oplist=['<', ]),
             predicate.MetitEquation(y - 10, oplist=['<', ]), ]
             #predicate.MetitEquation(x + 10, oplist=['>', '=']),
             #predicate.MetitEquation(y + 10, oplist=['>', '='])]
             
            
initial_state = {'d': ('m1', ),
                 'c': [str(predicate.MetitPredicate(*_)) for _ in
                       [(x, '='), (y, '='), (tau, '='), ]]}

bad_state = ''

system_def = {('m1',):
              {'flow': {x.diff(t): ddx,
                        y.diff(t): ddy,
                        tau.diff(t): 1},
               't': [],
               'inv': (MetitPredicate(x + 10, '<'),
                       MetitPredicate(y + 10, '<'),),
               'colour': 'lightblue'}, }
                                     
# x1eq = predicate.MetitEquation(1 - sqrt(x1))
# x1d = predicate.metit_derivative(x1eq, ('s1',), system_def)

# x2eq = predicate.MetitEquation(sqrt(x1)-sqrt(x2))
# x2d = predicate.metit_derivative(x2eq, ('s1',), system_def)

if __name__ == '__main__':
    print initial_state










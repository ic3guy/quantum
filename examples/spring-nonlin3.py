from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
from predicate import MetitEquation
from predicate import MetitPredicate
from predicate import get_derivs

t = Symbol('t')
x = Function('x')(t)
v = Function('v')(t)

bad = False
extra_constraints = ''
bad_state = ''

q = [('m1',)]

system_def = {('m1', ):
              {'flow': {x.diff(t): v, v.diff(t): -x + 2*x**3},
               't': [],
               'inv': [], }}
              
equations = [MetitEquation(x),
             MetitEquation(v),
             # MetitEquation(x - 1, var_id=1),
             # MetitEquation(x + 1, var_id=1),
             MetitEquation(0.5*v**2 + 0.5*x**2 + 0.5*x**4, oplist=['>'])]
# MetitEquation(x - x**3)]


equations.extend(get_derivs(1, MetitEquation(v), system_def, ('m1',)))
#equations.extend(get_derivs(2, MetitEquation(-5/2 * x + 0.5 * x**3), system_def,('m1',)))

initial_state = {'d': ('m1', ), 'c': [str(MetitPredicate(*_)) for _ in
                                     [(v, '>'),
                                      (x, '='),]]}
                                      # (x + 1, '>'),
                                      # (v, '>'),]]}
                                      # (0.5*x**3 - 2.5*x, '<'),
                                      # (1.5*v*x**2 - 2.5*v, '<')]]}

#MetitEquation(v-1,var_id=1)
#(v-1), '=')
#x - 1, '>')

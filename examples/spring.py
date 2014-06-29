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
              {'flow': {x.diff(t): v, v.diff(t): -5/2*x},
               't': [],
               'inv': [], }}
              
equations = [MetitEquation(x),
             MetitEquation(v, var_id=1)]


equations.extend(get_derivs(1, MetitEquation(v), system_def, ('m1',)))

initial_state = {'d': ('m1', ), 'c': [str(MetitPredicate(*_)) for _ in
                                     [(x, '='),
                                      (v, '>')]]}

#MetitEquation(v-1,var_id=1)
#(v-1), '=')

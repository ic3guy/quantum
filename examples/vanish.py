from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
from predicate import MetitEquation
from predicate import MetitPredicate

t = Symbol('t')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

bad = False
extra_constraints = ''
bad_state = ''

q = [('m1',)]

system_def = {('m1', ):
              {'flow': {x1.diff(t): x1, x2.diff(t): x2},
               't': [],
               'inv': [], }}
              
equations = [MetitEquation((x1**2+x2**2-1)**3)]

initial_state = {'d': ('m1',), 'c': [str(MetitPredicate(*x)) for x in
                                     [((x1**2+x2**2-1)**3, '<')]]}


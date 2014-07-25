from sympy import *
from itertools import product

import predicate
from predicate import MetitPredicate
from predicate import MetitEquation

t = Symbol('t')
w = Function('w')(t)
x = Function('x')(t)
g = Function('g')(t)
c = Function('c')(t)
w = Function('w')(t)

#r = 2

q = [('left_border',)]

bad = False

extra_constraints = []

equations = [MetitEquation(x+2,var_id=1),
             MetitEquation(x+1,var_id=1),
             MetitEquation(g),
             #MetitEquation(g-0.785),
             MetitEquation(-2*sin(g)),
             MetitEquation(-2*cos(g)*-0.785),
             MetitEquation(1.23245*sin(g))]

initial_state = {'d':('left_border',),'c':[str(predicate.MetitPredicate(*e)) for e in
                                           [(x+2,'>'),
                                            (x+1,'='),
                                            (g,'>'),
                                            (-2*sin(g),'>'),
                                            (1.23245*sin(g),'>')]]}

bad_state = MetitPredicate(x+2,'=')

system_def = {('left_border',): {'flow': {x.diff(t): -2*sin(g),
                                          g.diff(t): -0.785,},
                                 't': [],
                                 'inv': [MetitPredicate(x+2,'<'),],
                                 'colour':'blue'},}





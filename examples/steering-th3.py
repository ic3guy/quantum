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
#extra_constraints = ['X1<3.141', 'X1>-3.141']
#extra_constraints = ['G<pi/4','G>0']
extra_constraints = []

eq1 = c
eq2 = x-1
eq3 = x+1
eq4 = x+200
eq5 = g-0.785
eq6 = g-0.5
#eq7 = w - 

equations = [MetitEquation(x+1,var_id=3),
             MetitEquation(x,var_id=3),
             MetitEquation(g-0.5,var_id=1),
             MetitEquation(g-0.6,var_id=1),
             MetitEquation(g,var_id=1),
             MetitEquation(x+200,var_id=3),
             MetitEquation(1.57*cos(g)),
             MetitEquation(1.23245*sin(g))]


initial_state = {'d':('left_border',),'c':[str(predicate.MetitPredicate(*e)) for e in
                                        [(x+1,'='),
                                         (g+0.6,'>'),
                                         (g+0.5,'<'),]]}

bad_state = MetitPredicate(eq4,'=')

system_def = {('left_border',): {'flow': {x.diff(t): -2*sin(g),
                                          g.diff(t): -0.785,},
                                 't': [],
                                 'inv': [MetitPredicate(x+2,'<'),
                                         MetitPredicate(x+1,'>')],
                                 'colour':'blue'},
}





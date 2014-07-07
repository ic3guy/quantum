from sympy import *
from itertools import product

import predicate

timeout = 1000

metit_options = ('metit', 
                 '--autoInclude', 
                 '--time',str(timeout),
                 '-q',
                 '-')

t = Symbol('t')
#X1 = Symbol('X1')
#X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

q = [('cont',)]

bad = False
extra_constraints = ''

system_def = {('cont',): {'flow': {x1.diff(t): x2,
                                   x2.diff(t): -9.8*sin(x1)-x2},
                         't': [],
                         'inv': []}}

initial_state = {'d':('cont',),'c':['X1>0','X2>0']}


equations = [predicate.MetitEquation(x1,'t'),
             predicate.MetitEquation(x2,'t'),
             ]

bad_state = []

e5 = predicate.MetitEquation(system_def[('cont',)]['flow'][x2.diff(t)],'t')
equations.extend(predicate.get_derivs(1,e5,system_def,('cont',)))



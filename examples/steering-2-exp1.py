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

q = [('go_ahead','straight_ahead','correct_right','left_border','correct_left','right_border','in_canal')]

bad = False
#extra_constraints = ['X1<3.141', 'X1>-3.141']
#extra_constraints = ['G<2*3.14','G>2*-3.14']
extra_constraints = []

eq1 = c
eq2 = x-1
eq3 = x+1
eq4 = x+2
#eq5 = g-0.785
#eq6 = g+0.785
#eq7 = w - 

equations = [MetitEquation(x-1,var_id=1),
             MetitEquation(x+1,var_id=1),
             MetitEquation(x+2,var_id=1),
             MetitEquation(c),
             MetitEquation(g-0.785,var_id=2),
             MetitEquation(g+0.785,var_id=2)]

c_eq_z = predicate.MetitPredicate(c,'=')
x_eq_1 = predicate.MetitPredicate(x-1,'=')
x_eq_m1 = predicate.MetitPredicate(x+1,'=')
x_eq_m2 = predicate.MetitPredicate(eq4,'=')

initial_state = {'d':('go_ahead',),'c':[str(predicate.MetitPredicate(*e)) for e in
                                         [(x+1,'>'),
                                          (c,'='),
                                          (g-0.785,'<'),
                                          (g+0.785,'>')]]}

bad_state = []

system_def = {('correct_left',): {'flow': {x.diff(t): -2*sin(g),
                                           g.diff(t): 0.628,
                                           c.diff(t):-2},
                                  't': [{'guard': ([x_eq_1],),
                                         'next_state': ('right_border',),
                                         'updates': {c : 0}},
                                        {'guard': ([c_eq_z],),
                                         'next_state': ('straight_ahead',),
                                         'updates': {}}],
                                  'inv': [MetitPredicate(x+1,'<'),MetitPredicate(x-1,'>'),MetitPredicate(c,'<')]},
              ('straight_ahead',): {'flow': {x.diff(t): -2*sin(g),
                                            g.diff(t): 0,
                                            c.diff(t): 0},
                                    't': [],
                                    'inv' : []},
              ('correct_right',): {'flow': {x.diff(t): -2*sin(g),
                                            g.diff(t): -0.628,
                                            c.diff(t): -2},
                                   't' : [{'guard': ([c_eq_z],),
                                           'next_state': ('straight_ahead',),
                                           'updates': {}},
                                        {'guard': ([x_eq_m1],),
                                         'next_state': ('left_border',),
                                         'updates': {c : 0}}],
                                   'inv' : [MetitPredicate(x+1,'<'),MetitPredicate(x-1,'>'),MetitPredicate(c,'<')]},
              ('left_border',): {'flow': {x.diff(t): -2*sin(g),
                                         g.diff(t): -0.628,
                                         c.diff(t): 1},
                                   't' : [{'guard': ([x_eq_m1],),
                                           'next_state': ('correct_left',),
                                           'updates': {}},
                                          {'guard': ([x_eq_m2], ),
                                           'next_state': ('in_canal',),
                                           'updates': {}}],
                                'inv' : [MetitPredicate(x+2,'<'),MetitPredicate(x-1,'>')]},
              ('go_ahead',): {'flow': {x.diff(t): -2*sin(g),
                                      g.diff(t): 0,
                                      c.diff(t): 0},
                                   't' : [{'guard': ([x_eq_m1],),
                                           'next_state': ('left_border',),
                                           'updates': {c:0}},
                                          {'guard': ([x_eq_1],),
                                           'next_state': ('right_border',),
                                           'updates': {c : 0}}],
                                   'inv' : [MetitPredicate(x+1,'<'),MetitPredicate(x-1,'>')]},
              ('right_border',): {'flow': {x.diff(t): -2*sin(g),
                                          g.diff(t): 0.628,
                                          c.diff(t): 1},
                                   't' : [{'guard': ([x_eq_1],),
                                           'next_state': ('correct_right',),
                                           'updates': {}},],
                                   'inv' : [MetitPredicate(x+1,'<'),MetitPredicate(x+1,'='),MetitPredicate(x-1,'<')]},
              ('in_canal',): {'flow': {x.diff(t): 0,
                                      g.diff(t): 0,
                                      c.diff(t): 0},
                                   't' : [{'guard': ([x_eq_m2],),
                                           'next_state': [],
                                           'updates': {}}],
                                   'inv' : [],
                              'colour': 'red'},
}

#initial_state = {'d':('cont',),'c':['X1>0','X2>0','0.19984*X2^2 + 1.90843655*sin(X1)^2 + 1.90843655*cos(X1)^2 - 3.916868466*cos(X1) + 0.3084319171<0']}



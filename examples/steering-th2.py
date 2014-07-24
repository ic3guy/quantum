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

q = [('go_ahead','straight_ahead','left_border','correct_left','in_canal')]

bad = False
#extra_constraints = ['X1<3.141', 'X1>-3.141']
extra_constraints = ['G<pi/2','G>0']

eq1 = c
eq2 = x-1
eq3 = x+1
eq4 = x+2
eq5 = g-0.785
eq6 = g-0.5
#eq7 = w - 

equations = [MetitEquation(eq1),
             MetitEquation(eq3,var_id=3),
             MetitEquation(x-0.5,var_id=3),
             MetitEquation(g-0.5,var_id=1),
             MetitEquation(g-0.6,var_id=1),
             MetitEquation(eq4,var_id=3),
             MetitEquation(cos(g)*0.785),
             MetitEquation(-2*sin(g))]



c_eq_z = predicate.MetitPredicate(c,'=')
x_eq_1 = predicate.MetitPredicate(x-1,'=')
x_eq_m1 = predicate.MetitPredicate(x+1,'=')
x_eq_m2 = predicate.MetitPredicate(eq4,'=')
c_lt_z = predicate.MetitPredicate(c,'<')

initial_state = {'d':('go_ahead',),'c':[str(predicate.MetitPredicate(*e)) for e in
                                        [(x-0.5,'>'),
                                         (g-0.6,'<'),
                                         (g-0.5,'>'),
                                         (eq1,'=')]]}

bad_state = MetitPredicate(eq4,'=')

system_def = {('correct_left',): {'flow': {x.diff(t): -2*sin(g),
                                           g.diff(t): 0.785,
                                           c.diff(t): -2},
                                  't': [{'guard': ([c_eq_z],),
                                         'next_state': ('straight_ahead',),
                                         'updates': {}}],
                                  'inv': [MetitPredicate(x+1,'<'),
                                          MetitPredicate(x-1,'>'),
                                          MetitPredicate(c,'<')],
                                  'colour':'purple'},
              ('straight_ahead',): {'flow': {x.diff(t): -2*sin(g),
                                             g.diff(t): 0,
                                             c.diff(t): 0},
                                    't': [],
                                    'inv': [],
                                    'colour': 'orange'},
              ('left_border',): {'flow': {x.diff(t): -2*sin(g),
                                          g.diff(t): -0.785,
                                          c.diff(t): 1},
                                 't': [{'guard': ([x_eq_m1], ),
                                        'next_state': ('correct_left',),
                                        'updates': {}},
                                       {'guard': ([x_eq_m2], ),
                                        'next_state': ('in_canal',),
                                        'updates': {}}],
                                 'inv': [MetitPredicate(x+2,'<'),
                                         MetitPredicate(x+1,'>')],
                                 'colour':'blue'},
              ('go_ahead',): {'flow': {x.diff(t): -2*sin(g),
                                       g.diff(t): 0,
                                       c.diff(t): 0},
                              't': [{'guard': ([x_eq_m1], ),
                                     'next_state': ('left_border',),
                                     'updates': {c:0}}],
                              'inv': [MetitPredicate(x+1,'<'),
                                      MetitPredicate(x-1,'>')],
                              'colour': 'green'},
              ('in_canal',): {'flow': {x.diff(t): 0,
                                      g.diff(t): 0,
                                       c.diff(t): 0},
                              't' : [],
                              'inv' : [],
                              'colour' : 'black'},
}





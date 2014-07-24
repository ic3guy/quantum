from sympy import *
from itertools import product

import predicate
from predicate import MetitPredicate

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
extra_constraints = ['G<2*3.14','G>2*-3.14']

eq1 = c
eq2 = x-1
eq3 = x+1
eq4 = x+1.5
eq5 = g-0.785
eq6 = g+0.785
#eq7 = w - 

equations = [predicate.MetitEquation(eq) for eq in [x, eq1, eq2, eq3, eq4, eq5, eq6]]

c_eq_z = predicate.MetitPredicate(c,'=')
x_eq_1 = predicate.MetitPredicate(x-1,'=')
x_eq_m1 = predicate.MetitPredicate(x+1,'=')
x_eq_m2 = predicate.MetitPredicate(eq4,'=')
c_lt_z = predicate.MetitPredicate(c,'<')

initial_state = {'d':('go_ahead',),'c':[str(predicate.MetitPredicate(*e)) for e in
                                        [(x,'<'),
                                         (eq3,'>'),
                                         (eq5,'<'),
                                         (eq6,'>'),
                                         (eq1,'=')]]}

bad_state = []

system_def = {('correct_left',): {'flow': {x.diff(t): -2*sin(g),
                                           g.diff(t): 0.785,
                                           c.diff(t): -2},
                                  't': [{'guard': ([x_eq_1],),
                                         'next_state': ('right_border',),
                                         'updates': {c: 0}},
                                        {'guard': ([c_eq_z],),
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
              ('correct_right',): {'flow': {x.diff(t): -2*sin(g),
                                            g.diff(t): -0.785,
                                            c.diff(t): -2},
                                   't': [{'guard': ([c_eq_z], ),
                                          'next_state': ('straight_ahead',),
                                          'updates': {}},
                                         {'guard': ([x_eq_m1],),
                                          'next_state': ('left_border', ),
                                          'updates': {c: 0}}],
                                   'inv': [MetitPredicate(x+1,'<'),
                                           MetitPredicate(x-1,'>'),
                                           MetitPredicate(c,'<')],
                                   'colour': 'yellow'},
              ('left_border',): {'flow': {x.diff(t): -2*sin(g),
                                          g.diff(t): -0.785,
                                          c.diff(t): 1},
                                 't': [{'guard': ([x_eq_m1], ),
                                        'next_state': ('correct_left',),
                                        'updates': {}}],
                                 'inv': [MetitPredicate(x+1.5,'<'),
                                         MetitPredicate(x-1,'>')],
                                 'colour':'blue'},
              ('go_ahead',): {'flow': {x.diff(t): -2*sin(g),
                                       g.diff(t): 0,
                                       c.diff(t): 0},
                              't': [{'guard': ([x_eq_m1], ),
                                     'next_state': ('left_border',),
                                     'updates': {c:0}},
                                    {'guard': ([x_eq_1],),
                                     'next_state': ('right_border',),
                                     'updates': {c: 0}}],
                              'inv': [MetitPredicate(x+1,'<'),
                                      MetitPredicate(x-1,'>')],
                              'colour': 'green'},
              ('right_border',): {'flow': {x.diff(t): -2*sin(g),
                                           g.diff(t): 0.758,
                                           c.diff(t): 1},
                                  't': [{'guard': ([x_eq_1], ),
                                         'next_state': ('correct_right',),
                                         'updates': {}}],
                                  'inv': [MetitPredicate(x+1,'<'),
                                           MetitPredicate(x+1,'='),MetitPredicate(x-1,'<')],
                                  'colour':'pink'},
              ('in_canal',): {'flow': {x.diff(t): 0,
                                      g.diff(t): 0,
                                       c.diff(t): 0},
                              't' : [{'guard': ([x_eq_m2],),
                                      'next_state': [],
                                      'updates': {}}],
                              'inv' : [],
                              'colour' : 'black'},
}





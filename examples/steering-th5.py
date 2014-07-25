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
#extra_constraints = ['G<pi/2','G>-pi/2']
extra_constraints = ['G<1.5','G>-1.5']

eq1 = c
eq2 = x-1
eq3 = x+1
eq4 = x+2
eq5 = g-0.785
eq6 = g-0.5
#eq7 = w - 

equations = [MetitEquation(c),
             MetitEquation(x+2,var_id=1,oplist=['>']),
             MetitEquation(x+1,var_id=1),
             MetitEquation(x-1,var_id=1),
             MetitEquation(g,var_id=2),
             MetitEquation(g-0.5,var_id=2),]
             #MetitEquation(g-0.785),
             #MetitEquation(-2*sin(g)),
             #MetitEquation(-2*cos(g)*-0.785),
             #MetitEquation(1.23245*sin(g))]


c_eq_z = predicate.MetitPredicate(c,'=')
x_eq_1 = predicate.MetitPredicate(x-1,'=')
x_eq_m1 = predicate.MetitPredicate(x+1,'=')
x_eq_m2 = predicate.MetitPredicate(eq4,'=')
c_lt_z = predicate.MetitPredicate(c,'<')

initial_state = {'d':('go_ahead',),'c':[str(predicate.MetitPredicate(*e)) for e in
                                        [(x+1,'>'),
                                         (g,'>'),
                                         #(-2*sin(g),'<'),
                                         #(-2*cos(g)*-0.785,'<'),
                                         #(1.23245*sin(g),'>'),
                                         (g-0.5,'<'),
                                         (c,'=')
                                    ]]}

# initial_state = {'d':('go_ahead',),'c':[str(predicate.MetitPredicate(*e)) for e in
#                                         [(x-0.6,'<'),
#                                          (x-0.5,'>'),
#                                          (eq5,'<'),
#                                          (eq6,'>'),
#                                          (eq1,'=')]]}

# bad_state = MetitPredicate(eq4,'=') 
bad_state = ''

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
                                        'updates': {}},
                                       {'guard': ([x_eq_m2], ),
                                        'next_state': ('in_canal',),
                                        'updates': {}}],
                                 'inv': [MetitPredicate(x+2,'<'),
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
                              'colour' : 'red'},
}





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
tt = Function('tt')(t)

#r = 2

q = [('go_ahead','correct_right','left_border','correct_left','right_border','in_canal')]

bad = False
#extra_constraints = ['X1<3.141', 'X1>-3.141']
#extra_constraints = ['G<pi/2','G>-pi/2']
extra_constraints = ['G<1.5','G>-1.5','TT>=0','TT<6']

lc = 0.4*cos(tt)*exp(-0.2*tt)+2


equations = [# MetitEquation(tt,oplist=['>','=']),
             MetitEquation(x-lc,var_id=1),
             MetitEquation(x+lc,var_id=1),
             MetitEquation(x-(0.2*cos(tt-1.5)-0.25)),
             MetitEquation(x-(0.2*sin(tt)+0.5)),
             MetitEquation(g,var_id=2),
             MetitEquation(g-0.5,var_id=2),]
             #MetitEquation(g-0.785),
             #MetitEquation(-2*sin(g)),
             #MetitEquation(-2*cos(g)*-0.785),
             #MetitEquation(1.23245*sin(g))]

x_eq_ls = predicate.MetitPredicate((x-(0.2*sin(tt)+0.5)),'=')
x_eq_rs = predicate.MetitPredicate(x-(0.2*cos(tt-1.5)-0.25),'=')

#x_eq_m2 = predicate.MetitPredicate(x+2,'=')
#x_eq_2 = predicate.MetitPredicate(x-2,'=')

x_eq_m2 = MetitPredicate(x+lc,'=')
x_eq_2 = MetitPredicate(x-lc, '=')

g_eq_z = MetitPredicate(g,'=')

initial_state = {'d':('go_ahead',),'c':[str(predicate.MetitPredicate(*e)) for e in
                                        [(x-(0.2*cos(tt-1.5)-0.25),'>'),
                                         (x-(0.2*sin(tt)+0.5),'<'),
                                         (g,'>'),
                                         #(-2*sin(g),'<'),
                                         #(-2*cos(g)*-0.785,'<'),
                                         #(1.23245*sin(g),'>'),
                                         (g-0.5,'<'),
                                         #(tt,'=')
                                         ]]}


# bad_state = MetitPredicate(eq4,'=')
bad_state = ''

system_def = {('correct_left',): {'flow': {x.diff(t): -2*sin(g),
                                           g.diff(t): -0.785,
                                           tt.diff(t): 1},
                                  't': [{'guard': ([x_eq_rs],),
                                         'next_state': ('right_border',),
                                         'updates': {}},
                                        {'guard': ([g_eq_z],),
                                         'next_state': ('go_ahead',),
                                         'updates': {}}],
                                  'inv': [],
                                  'colour':'purple'},
          
              
              ('correct_right',): {'flow': {x.diff(t): -2*sin(g),
                                            g.diff(t): 0.785,
                                            tt.diff(t): 1},
                                   't': [{'guard': ([g_eq_z],),
                                          'next_state': ('go_ahead', ),
                                          'updates': {}},
                                         {'guard': ([x_eq_ls],),
                                          'next_state': ('left_border', ),
                                          'updates': {}}],
                                   'inv': [],
                                   'colour': 'yellow'},
              
              ('left_border',): {'flow': {x.diff(t): -2*sin(g),
                                          g.diff(t): 0.785,
                                          tt.diff(t): 1},
                                 't': [{'guard': ([x_eq_ls], ),
                                        'next_state': ('correct_left',),
                                        'updates': {}},
                                       {'guard': ([x_eq_2], ),
                                        'next_state': ('in_canal',),
                                        'updates': {}}],
                                 'inv': [MetitPredicate(x-(0.2*sin(tt)+0.5),'<')],
                                 'colour':'blue'},

              ('go_ahead',): {'flow': {x.diff(t): -2*sin(g),
                                       g.diff(t): 0,
                                       tt.diff(t): 1},
                              't': [{'guard': ([x_eq_ls], ),
                                     'next_state': ('left_border',),
                                     'updates': {}},
                                    {'guard': ([x_eq_rs],),
                                     'next_state': ('right_border',),
                                     'updates': {}}],
                              'inv': [],
                              'colour': 'green'},
              
              ('right_border',): {'flow': {x.diff(t): -2*sin(g),
                                           g.diff(t): -0.758,
                                           tt.diff(t): 1},
                                  't': [{'guard': ([x_eq_rs], ),
                                         'next_state': ('correct_right',),
                                         'updates': {}},
                                        {'guard': ([x_eq_m2], ),
                                         'next_state': ('in_canal',),
                                         'updates': {}}],
                                  'inv': [MetitPredicate(x-(0.2*cos(tt-1.5)-0.25),'>')],
                                  'colour':'pink'},

              ('in_canal',): {'flow': {x.diff(t): 0,
                                       g.diff(t): 0,
                                       tt.diff(t): 0},
                              't': [{'guard': (),
                                     'next_state': [],
                                     'updates': {}}],
                              'inv': [],
                              'colour': 'red'},
}





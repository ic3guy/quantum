from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work

t = Symbol('t')
py = Function('py')(t)
vy = Function('vy')(t)

q = [('falling',)] #can just get dictionary keys...

bad = False

#guard_equation = predicate.MetitEquation(sin(px)-py,'t',[],vars_dict)

guard_equation = py
guard = predicate.MetitPredicate(guard_equation,'=')
g_inv = predicate.MetitPredicate(guard_equation,'<')

#inv = predicate.MetitEquation(px,'t',[],vars_dict)
#inv_pred_pxlz = predicate.MetitPredicate(px, '<')

#inv = predicate.MetitEquation(py,'t',[],vars_dict)
inv_pred_pylz = predicate.MetitPredicate(py, '<')

#inv = predicate.MetitEquation(vx,'t',[],vars_dict)
#inv_pred_vxlz = predicate.MetitPredicate(vx, '<')

#inv = predicate.MetitEquation(vy,'t',[],vars_dict)
#inv_pred_vylz = predicate.MetitPredicate(vy, '<')


system_def = {('falling',) : {'flow' : {py.diff(t): vy,
                                        vy.diff(t): -9.8},
                              't' : [{'guard':(guard,), 
                                      'next_state' : ('falling',),
                                      'updates' : {vy : -0.2*vy}}],
                              'inv' : (g_inv,)}}


equations = [predicate.MetitEquation(py),
             predicate.MetitEquation(vy),
             predicate.MetitEquation(py-1),
             predicate.MetitEquation(py-5)]


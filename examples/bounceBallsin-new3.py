from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work

t = Symbol('t')
h = Symbol('h')
ss = Symbol('ss')
c = Symbol('c')

px = Function('px')(t)
py = Function('py')(t)
vx = Function('vx')(t)
vy = Function('vy')(t)

q = [('falling',)] #can just get dictionary keys...

bad = False

#guard_equation = predicate.MetitEquation(sin(px)-py,'t',[],vars_dict)

guard_equation = py-ss
guard = predicate.MetitPredicate(guard_equation,'=')
g_inv = predicate.MetitPredicate(guard_equation,'<')

#inv = predicate.MetitEquation(px,'t',[],vars_dict)
inv_pred_pxlz = predicate.MetitPredicate(px, '<')

#inv = predicate.MetitEquation(py,'t',[],vars_dict)
inv_pred_pylz = predicate.MetitPredicate(py, '<')

#inv = predicate.MetitEquation(vx,'t',[],vars_dict)
inv_pred_vxlz = predicate.MetitPredicate(vx, '<')

#inv = predicate.MetitEquation(vy,'t',[],vars_dict)
inv_pred_vylz = predicate.MetitPredicate(vy, '<')

h_inv = predicate.MetitPredicate(h,'<')
h_inv2 = predicate.MetitPredicate(h,'=')

vx_gt_z = predicate.MetitPredicate(vx,'>')
vx_lt_z = predicate.MetitPredicate(vx,'<')

system_def = {('falling',) : {'flow' : {px.diff(t): vx,
                                        py.diff(t): vy,
                                        vx.diff(t): 0,
                                        vy.diff(t): -9.8 + 0.01*vy**2},
                              't' : [{'guard':([guard],), 
                                      'next_state' : ('falling',),
                                      'updates' : {vx : ((1-0.8*c**2)*vx + 1.8*c*vy)/(1+c**2), 
                                                   vy : (1.8*c*vx + (-0.8+c**2)*vy)/(1+c**2)}}],
                              'inv' : (g_inv,)}}



equations = [#predicate.MetitEquation(py),
             #predicate.MetitEquation(px),
             predicate.MetitEquation(py),
             predicate.MetitEquation(vx),
             predicate.MetitEquation(vy),
             #predicate.MetitEquation(vx-0.1),
             #predicate.MetitEquation(vx+0.1),
             #predicate.MetitEquation(h),
             #predicate.MetitEquation(vx**2-2*9.8),
             #predicate.MetitEquation(vx**2-vy**2),
             predicate.MetitEquation(vx**2+vy**2+2*9.8*py-9.8),
             predicate.MetitEquation(guard_equation)]










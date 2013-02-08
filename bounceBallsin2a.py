from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work

t = Symbol('t')
PX = Symbol('PX') #x1 = vx
PY = Symbol('PY') #x2 = vy
VX = Symbol('VX')
VY = Symbol('VY')
T = Symbol('T')

px = Function('px')(t)
py = Function('py')(t)
vx = Function('vx')(t)
vy = Function('vy')(t)

q = [('falling',)] #can just get dictionary keys...

bad = False

vars_dict = {px : PX, py : PY, vx : VX, vy: VY, t : T}

guard_equation = predicate.MetitEquation(sin(px)-py,'t',[],vars_dict)
guard = predicate.MetitPredicate(guard_equation,'=')
g_inv = predicate.MetitPredicate(guard_equation,'<')

inv = predicate.MetitEquation(px,'t',[],vars_dict)
inv_pred_pxlz = predicate.MetitPredicate(inv, '<')

inv = predicate.MetitEquation(py,'t',[],vars_dict)
inv_pred_pylz = predicate.MetitPredicate(inv, '<')

inv = predicate.MetitEquation(vx,'t',[],vars_dict)
inv_pred_vxlz = predicate.MetitPredicate(inv, '<')

inv = predicate.MetitEquation(vy,'t',[],vars_dict)
inv_pred_vylz = predicate.MetitPredicate(inv, '<')

t_inv = predicate.MetitEquation(t, 't',[],vars_dict)
t_pred = predicate.MetitPredicate(t_inv, '<')

deriv_dict = {('falling',) : {'flow' : {px.diff(t): vx,
                                        py.diff(t): vy,
                                        vx.diff(t): 0,
                                        vy.diff(t): (-9.8 + 0.01*vy**2)*(1-exp(-3*t))},
                              't' : [{'guard':(guard,), 
                                      'next_state' : ('falling',),
                                      'updates' : {vx : ((1-0.8*cos(px)**2)*vx + 1.8*cos(px)*vy)/(1+cos(px)**2), 
                                                   vy : (1.8*cos(px)*vx + (-0.8+cos(px)**2)*vy)/(1+cos(px)**2)}}],
                              'inv' : (g_inv,t_pred)}}



equations = [predicate.MetitEquation(px,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(py,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(vx,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(vy,'t',deriv_dict,vars_dict),
             t_inv,
             guard_equation]

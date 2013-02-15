from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work

t = Symbol('t')
x = Function('x')(t)

bad = False

pre = x-80
g_pred_80gt = predicate.MetitPredicate(pre,'>')
g_pred_80eq = predicate.MetitPredicate(pre,'=')

pre = x-70
g_pred_70lt = predicate.MetitPredicate(pre,'<') 	
g_pred_70eq = predicate.MetitPredicate(pre,'=')

pre = x-82
g_pred_82gt = predicate.MetitPredicate(pre,'>')
g_pred_82eq = predicate.MetitPredicate(pre,'=')

pre = x-68
g_pred_68lt = predicate.MetitPredicate(pre,'<')
g_pred_68eq = predicate.MetitPredicate(pre,'=')

q = [('on','off')]

system_def = {('on',) : {'flow' : {x.diff(t): -x+100},
                           't' : [{'guard': [[g_pred_80gt],[g_pred_80eq]], 'next_state' : ('off',), 'updates' : ()}],
                           'inv' : (g_pred_82eq,g_pred_82gt)},  
              ('off',) : {'flow': {x.diff(t): -x},
                            't' : [{'guard': [[g_pred_70lt],[g_pred_70eq]], 'next_state' : ('on',), 'updates' : ()}],
                            'inv' : (g_pred_68eq,g_pred_68lt)}}
 
equations = [predicate.MetitEquation(x-70),
             predicate.MetitEquation(x-80),
             predicate.MetitEquation(x),
             predicate.MetitEquation(x-82),
             predicate.MetitEquation(x-68)]
#             predicate.MetitEquation(x-100,'t',deriv_dict,vars_dict)]
#'

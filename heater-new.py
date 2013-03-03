from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
import predicate

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
 
equations = [predicate.MetitEquation(x-70,var_id=1),
             predicate.MetitEquation(x-80,var_id=1),
             predicate.MetitEquation(x,var_id=1),
             predicate.MetitEquation(x-82,var_id=1),
             predicate.MetitEquation(x-68,var_id=1)]
#             predicate.MetitEquation(x-100,'t',deriv_dict,vars_dict)]
#'

initial_state = {'d':('on',),'c':['X - 70>0','X - 80<0']}
bad_state = []
#initial_state = {'d':('falling',),'c':['VY=0','PY<0','G<0','-G - PY + sin(PX)=0','PX<0','VX=0']}

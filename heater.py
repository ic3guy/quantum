from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work

t = Symbol('t')
X = Symbol('X') 
x = Function('x')(t)

deriv_dict = {('on',) : {x.diff(t): -x+100},
              ('off',) : {x.diff(t): -x}}

vars_dict = {x : X}
    
equations = [predicate.MetitEquation(x-70,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x-80,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x-68,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x-82,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x,'t',deriv_dict,vars_dict)]
#             predicate.MetitEquation(x-100,'t',deriv_dict,vars_dict)]




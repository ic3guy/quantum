from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work

#time taken Time taken 0:40:33.411

t = Symbol('t')
X1 = Symbol('X1')
X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)
    
deriv_dict = {x1.diff(t): x2,
              x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

vars_dict = {x1(t) : X1, x2(t) : X2}
    
equations = [predicate.MetitEquation(x1,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x2,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(sin(x1)*cos(x1)-10*sin(x1),'t',deriv_dict,vars_dict),
#predicate.MetitEquation(x1-3.141592654,'t',deriv_dict,vars_dict),
#predicate.MetitEquation(x2-15,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(0.33445*x2**2+1.4615*sin(x1)**2+1.7959*cos(x1)**2-6.689*cos(x1)+4.8931-3, 't',deriv_dict, vars_dict)]

e5 = predicate.MetitEquation(deriv_dict[x2.diff(t)],'t',deriv_dict,vars_dict)
equations.extend(predicate.get_derivs(1,e5))


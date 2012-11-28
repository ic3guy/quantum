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
              x2.diff(t): -9.8*sin(x1)}

vars_dict = {x1 : X1, x2 : X2}
    
equations = [predicate.MetitEquation(x1,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x2,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(-9.8*sin(x1),'t',deriv_dict,vars_dict),
#predicate.MetitEquation(x1-3.141592654,'t',deriv_dict,vars_dict),
#predicate.MetitEquation(x2-15,'t',deriv_dict,vars_dict),
#with friction predicate.MetitEquation(2.1351*sin(x1)**2 + 2.1351*cos(x1)**2 - 4.3702*cos(x1) + 0.22297*x2**2 + 0.2351,'t',deriv_dict,vars_dict)]
predicate.MetitEquation(1.90843655*sin(x1)**2 + 1.90843655*cos(x1)**2 - 3.916868466*cos(x1) + 0.19984*x2**2 + 0.0084319171,'t',deriv_dict,vars_dict)]
#   3.5892-3.7822*cos(x1)+3.0066*cos(x1)**2+2.8136*sin(x1)**2 + 0.19297*x2**2-5,'t',deriv_dict, vars_dict)]

e5 = predicate.MetitEquation(deriv_dict[x2.diff(t)],'t',deriv_dict,vars_dict)
equations.extend(predicate.get_derivs(1,e5))


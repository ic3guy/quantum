from __future__ import division
from sympy import *

t = Symbol('t')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

deriv_dict = {x1.diff(t): x2,
              x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

#x1d = x2(t)
#x2d = sin(x1(t))*cos(x1(t))-10*sin(x1(t))

odelist = []

#diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_dict)
#print diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_dict).diff().subs(deriv_dict)
#print diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_dict).diff().subs(deriv_dict).diff().subs(deriv_dict)

def get_derivs (n, seed):

    for n in range(n):
        print str(n) + " : "  + str(diff(seed).subs(deriv_dict))
        seed = diff(seed).subs(deriv_dict)


get_derivs(3, sin(x1)*cos(x1)-10*sin(x1))
from __future__ import division
from sympy import *


def gen_dif_equations (n, *variables, **derivatives):

    t = symbols('t')
    varlist = []
    derlist = []
    
    for var in variables:
        print var
        varlist.append(Function(var)(t))
        #varlist.append(var)
        
    for eq in derivatives:
        #print eq
        eq = Function(str(eq))(t)
      #  eq = sympify(derivatives[eq])
        derlist.append(eq)
        #print eq
        #print eq.diff(t)
        
        v = eq.diff(t)

        print "Varlist: " + str(varlist)
        
        print "V: " + str(v)

    print "Derlist: " + str(derlist)

    for eq in derlist:
        print eq
        
    for var in varlist:
        print "Var: " + repr(var)
        print sympify(var).diff(t)
        print v.subs(sympify(var).diff(t),2) 
            #v = v.subs(cos,sin)
        print v
    
    #for i in range(n):
        
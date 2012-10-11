from __future__ import division
from sympy import *
from sympy.plotting.plot import Plot
from MetitarskiPrinter import MetitarskiPrinter


def metitarski(expr, **settings):
    """Transform an expression to a string with Mathematica syntax. """
    p = MetitarskiPrinter(settings)
    s = p.doprint(expr)

    return s

#from matplotlib import *

t = Symbol('t')
X1 = Symbol('X1')
X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

#taken from https://groups.google.com/forum/?fromgroups=#!searchin/sympy/derivatives$20back$20substitution/sympy/BcVatqiR5Ss/5506c-y7QvgJ

deriv_dict = {x1.diff(t): x2,
              x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

plot_dict = {x1(t):X1,x2(t):X2}
#x1d = x2(t)
#x2d = sin(x1(t))*cos(x1(t))-10*sin(x1(t))

odelist = []
plotlist = []
#diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_dict)
#print diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_dict).diff().subs(deriv_dict)
#print diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_dict).diff().subs(deriv_dict).diff().subs(deriv_dict)

def get_derivs (n, seed):

    for n in range(n):

        dn = diff(seed).subs(deriv_dict)

        #print str(n) + " : "  + str(dn)
        #plot(diff(seed).subs(deriv_dict))
        plotlist.append(dn.subs(plot_dict))
        seed = diff(seed).subs(deriv_dict)

get_derivs(3, sin(x1)*cos(x1)-10*sin(x1))
#print plotlist

p = Plot()

# from sys import *
#getrecursionlimit()
#setrecursionlimit()

for plot in plotlist:
    p.extend(plot_implicit(Eq(plot,0), (X1,-2,2),(X2,-2,2), adaptive=False, show=False, points=400))

p.show()


for plot in plotlist:
    print metitarski(plot)

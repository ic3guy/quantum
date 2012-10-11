from __future__ import division
from sympy import *
from sympy.plotting.plot import Plot

#from matplotlib import *

t = Symbol('t')
x = Symbol('x')
y = Symbol('y')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

#taken from https://groups.google.com/forum/?fromgroups=#!searchin/sympy/derivatives$20back$20substitution/sympy/BcVatqiR5Ss/5506c-y7QvgJ

deriv_dict = {x1.diff(t): x2,
              x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

plot_dict = {x1(t):x,x2(t):y}
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
        

get_derivs(6, sin(x1)*cos(x1)-10*sin(x1))

x = Symbol('x')

p = Plot()

for plot in plotlist:
    p.extend(plot_implicit(Eq(plot,0), (x,-pi,pi),(y,-pi,pi), adaptive=False, show=False))

p.show()





from __future__ import division
from sympy import *
from sympy.plotting.plot import Plot
from MetitarskiPrinter import MetitarskiPrinter
from itertools import product
import subprocess

def metitarski(expr, **settings):
    """Transform an expression to a string with Mathematica syntax. """
    p = MetitarskiPrinter(settings)
    s = p.doprint(expr)

    return s

#from matplotlib import *

t = Symbol('t')

#X1 = Symbol('X1')
#X2 = Symbol('X2')
#x1 = Function('x1')(t)
#x2 = Function('x2')(t)

W = Symbol('W')
TH = Symbol('TH')
w = Function('w')(t)
th = Function('th')(t)


#taken from https://groups.google.com/forum/?fromgroups=#!searchin/sympy/derivatives$20back$20substitution/sympy/BcVatqiR5Ss/5506c-y7QvgJ

#deriv_dict = {x1.diff(t): x2,
 #             x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

deriv_dict = {th.diff(t): w, w.diff(t):-2*sin(th)}
plot_dict = {th(t):TH, w(t):W}

#plot_dict = {x1(t):X1,x2(t):X2}
#x1d = x2(t)
#x2d = sin(x1(t))*cos(x1(t))-10*sin(x1(t))

odelist = []
plotlist = [W,TH]
#diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_dict)
#print diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_dict).diff().subs(deriv_dict)
#print diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_dict).diff().subs(deriv_dict).diff().subs(deriv_dict)

def get_derivs (n, seed):

    for n in range(n):
        dn = diff(seed).subs(deriv_dict)
        #print str(n) + " : "  + str(dn)
        #plot(diff(seed).subs(deriv_dict))
        plotlist.append(dn.subs(plot_dict))
        #plotlist.append(dn)
        seed = diff(seed).subs(deriv_dict)

get_derivs(4, -2*sin(th))
print plotlist

p = Plot()

# from sys import *
#getrecursionlimit()
#setrecursionlimit()

for plot in plotlist:
    p.extend(plot_implicit(Eq(plot,0), (TH,-pi,pi),(W,-pi,pi), adaptive=False, show=False, points=800))

p.show()

vv = sympify('And(' + ','.join([str(x < 0) for x in plotlist]) + ')')

plot_implicit(vv,(TH,-pi,pi), (W,-pi,pi))

oplist = ['>','<']

for plot in plotlist:
    odelist.append(metitarski(plot))

#inftest = product(odelist,oplist)

inftest = []

for ode in odelist:
    predlist = []    
    for op in oplist:
        predlist.append('(' + ode + op + '0' + ')')

    inftest.append(predlist)

for element in product(*inftest):
    print element
    
print list(inftest)

metit_options = ['metit', 
                 '--autoIncludeExtended', 
                 '--strategy','1',
                 '--time','5',
                 '-']

def make_imp (varlist, preds) :
    out_string = " & ".join(map(str,preds))
    return 'fof(stdin,conjecture, ![' + varlist + '] : ((TH>-2 & TH < 2) => ~(' + out_string + '))).'


for element in product(*inftest):
    #process = subprocess.Popen(metit_options, shell=False, stdout=open('/dev/null','w'), stdin=subprocess.PIPE)
    process = subprocess.Popen(metit_options, stdin=subprocess.PIPE)
    metit_input = make_imp('W,TH', element)
    print metit_input
    process.communicate(metit_input)
    print "Return code: " + str(process.returncode)
    if process.returncode == 0: print element
   
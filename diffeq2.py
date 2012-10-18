from __future__ import division
from sympy import *
from sympy.plotting.plot import Plot
from MetitarskiPrinter import MetitarskiPrinter
from itertools import product
import subprocess
import metitarski
import predicate




#from matplotlib import *

t = Symbol('t')

X1 = Symbol('X1')
X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

#W = Symbol('W')
#TH = Symbol('TH')
#w = Function('w')(t)
#th = Function('th')(t)

#taken from https://groups.google.com/forum/?fromgroups=#!searchin/sympy/derivatives$20back$20substitution/sympy/BcVatqiR5Ss/5506c-y7QvgJ

deriv_sub_dict = {x1.diff(t): x2,
              x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

#deriv_sub_dict = {th.diff(t): w, w.diff(t):-2*sin(th)}
#plot_dict = {th(t):TH, w(t):W}

plot_dict = {x1(t):X1,x2(t):X2}
#x1d = x2(t)
#x2d = sin(x1(t))*cos(x1(t))-10*sin(x1(t))

odelist = []
#plotlist = [W,TH,5*W-16*TH,-80*W+231*TH]

plotlist = [X1,X2,0.3345*X2**2+1.4615*sin(X1)**2+1.7959*cos(X1)**2-6.689*cos(X1)+4.6931,X2-0.5]
#plotlist = [X1,X2]


#diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_sub_dict)
#print diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_sub_dict).diff().subs(deriv_sub_dict)
#print diff(sin(x1)*cos(x1)-10*sin(x1)).subs(deriv_sub_dict).diff().subs(deriv_sub_dict).diff().subs(deriv_sub_dict)

def get_derivs (n, seed):

    for n in range(n):
        dn = diff(seed).subs(deriv_sub_dict)
        plotlist.append(dn.subs(plot_dict))
        seed = diff(seed).subs(deriv_sub_dict)

#get_derivs(3, -2*sin(th))
get_derivs(1, sin(x1)*cos(x1)-10*sin(x1))
print plotlist

#p = Plot()

# from sys import *
#getrecursionlimit()
#setrecursionlimit()

#for plot in plotlist:
#    p.extend(plot_implicit(Eq(plot,0), (X1,-pi,pi),(X2,-pi,pi), adaptive=False, show=False, points=800))

#p.show()

vv = sympify('And(' + ','.join([str(x < 0) for x in plotlist]) + ')')

#print 'vv : %s' % vv
#plot_implicit(vv,(X1,-pi,pi), (X2,-pi,pi))

oplist = ['>','<']

for plot in plotlist:
    odelist.append(metitarski_pp(plot))

#inftest = product(odelist,oplist)

inftest = []

for ode in odelist:
    predlist = []    
    for op in oplist:
        predlist.append(predicate.MetitPredicate(ode,op))

    inftest.append(predlist)

#for element in product(*inftest):
#    print element
    
#print list(inftest)

metit_options = ['metit', 
                 '--autoInclude', 
                 '--time','5', '-t','0',
                 '-']

def make_imp (varlist, preds) :
    out_string = " & ".join(map(str,preds))
    out_string = out_string.replace('sin(X1)', 'X')
    out_string = out_string.replace('cos(X1)', 'Y')
    #out_string = out_string.replace('sin(X2)', 'A')
    #out_string = out_string.replace('cos(X2)', 'B')
    
    return 'fof(stdin,conjecture, (![' + varlist + '] : ~(X^2+Y^2=1 & (' + out_string + ')))).'
    #return 'fof(stdin,conjecture, (?[' + varlist + '] : ((X^2+Y^2=1) & (' + out_string + ')))).'
    #return 'fof(stdin,conjecture, (![' + varlist + '] : ~((X1<pi & X1>-pi) & (' + out_string + ')))).'

feasible = 0
infeasible = 0

system = []

for element in product(*inftest):
    #print element
    system.append(predicate.State('X1,X2',*element))
    #y = State('x1,x2',*element)
    
for state in system:
    print metitarski.make_fof_inf(state)
    rc = metitarski.send_to_metit(metitarski.make_fof_inf(state))
    if rc == 0: infeasible = infeasible+1
    if rc == 1: feasible = feasible+1
    
    #process = subprocess.Popen(metit_options, shell=False, stdout=open('/dev/null','w'), stdin=subprocess.PIPE)
    #process = subprocess.Popen(metit_options, stdin=subprocess.PIPE)
#metit_input = make_fof_inf(element)
#print metit_input
#returncode = send_to_metit(metit_input)
#print "Return code: " + str(returncode)
#if returncode == 0: infeasible = infeasible+1
#if returncode == 1: feasible = feasible+1
    
print "Feasible %s" % feasible
print "Infeasible %s" % infeasible
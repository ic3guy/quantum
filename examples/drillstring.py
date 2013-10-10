from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
import predicate

t = Symbol('t')
#h = Symbol('h')
x1 = Function('x1')(t)
x2 = Function('x2')(t)
x3 = Function('x3')(t)

#ct = Symbol('ct')

q = [('slip+','slip-','stuck')] #can just get dictionary keys...

bad = False

#guard_equation = predicate.MetitEquation(sin(px)-py,'t',[],vars_dict)

#ct = sympify(2.3)
#ueq = predicate.MetitEquation(2.3*x1)

Wob = 50000

ueqTsb1 = 172.3067*x1 + 861.5336*x2 - (50 + 172.3067)*x3 - 0.12446*Wob
ueqTsb2 = 172.3067*x1 + 861.5336*x2 - (50 + 172.3067)*x3 + 0.12446*Wob
Absueq = 172.3067*x1 + 861.5336*x2 - (50 + 172.3067)*x3 - 0.122446*Wob

slipp_to_slipn_guard = predicate.MetitPredicate(ueqTsb2,'<')
slipn_to_slipp_guard = predicate.MetitPredicate(ueqTsb1,'>')
absueq_guard = predicate.MetitPredicate(Absueq,'<')

x3_gtz = predicate.MetitPredicate(x3,'>')
x3_ltz = predicate.MetitPredicate(x3,'<')
x3_eqz = predicate.MetitPredicate(x3,'=')


initial_state = {'d' : ('stuck',),'c' : ['X1=0','X3=0']}
bad_state = []

system_def = {('slip+',) : {'flow' : {x1.diff(t): (6000 - 597.3067*x1 - 861.5336*x2 + 172.3067*x3)/2122,
                                      x2.diff(t): x1-x3,
                                      x3.diff(t): ((-(0.155575*(0.5 + (-1*0.5 + 0.8)/exp(0.9*x3))*Wob) + 172.3067*x1 + 861.5336*x2 - (50 + 172.3067)*x3)/471.9698)},
                            't'    : [{'guard'      : ([slipp_to_slipn_guard,x3_eqz],[x3_ltz]), 
                                       'next_state' : ('slip-',),
                                       'updates'    : {}},
                                      {'guard'      : ([x3_eqz,absueq_guard]),
                                       'next_state' : ('stuck',),
                                       'updates' : {}}],
                            'inv'  : (x3_ltz,)},
              ('slip-',) : {'flow' : {x1.diff(t): (6000 - 597.3067*x1 - 861.5336*x2 + 172.3067*x3)/2122,
                                      x2.diff(t): x1-x3,
                                      x3.diff(t): ((0.155575*(0.5 + (-1*0.5 + 0.8)/exp(-0.9*x3))*Wob + 172.3067*x1 + 861.5336*x2 - (50 + 172.3067)*x3)/471.9698)},
                            't'    : [{'guard'      : ([slipn_to_slipp_guard,x3_eqz],[x3_gtz]), 
                                       'next_state' : ('slip+',),
                                       'updates'    : {}},
                                      {'guard'       : ([x3_eqz,absueq_guard]),
                                       'next_state' : ('stuck',),
                                       'updates' : {}}],
                            'inv'  : (x3_gtz,)},
              ('stuck',) : {'flow' : {x1.diff(t): (6000 - 597.3067*x1 - 861.5336*x2 + 172.3067*x3)/2122,
                                      x2.diff(t): x1-x3,
                                      x3.diff(t): 0},
                            't'    : [{'guard'      : ([slipp_to_slipn_guard,x3_eqz],[x3_ltz]), 
                                       'next_state' : ('slip-',),
                                       'updates'    : {}},
                                      {'guard'      : ([slipn_to_slipp_guard,x3_eqz],[x3_gtz]), 
                                       'next_state' : ('slip+',),
                                       'updates'    : {}}],
                            'inv'  : (x3_ltz,x3_gtz)}}

equations = [predicate.MetitEquation(x1),
             predicate.MetitEquation(x3),
             predicate.MetitEquation(Absueq),
             predicate.MetitEquation(ueqTsb1),
             predicate.MetitEquation(ueqTsb2)]

e5 = predicate.MetitEquation(system_def[('slip+',)]['flow'][x3.diff(t)])
equations.extend(predicate.get_derivs(2,e5,system_def,('slip+',)))
#equations.extend(predicate.get_derivs(2,e5,system_def,('slip+',)))

# import pdb; pdb.set_trace()







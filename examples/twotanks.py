from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
import abstraction
import predicate

t = Symbol('t')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

q = [('s1','s2')] #can just get dictionary keys...

bad = False

#guard_equation = predicate.MetitEquation(sin(px)-py,'t',[],vars_dict)

guard_equation = x2 - 1
guard = predicate.MetitPredicate(guard_equation,'=')

#inv = predicate.MetitEquation(px,'t',[],vars_dict)

#energy_inv = predicate.MetitPredicate(0.5*vx**2+0.5*vy**2+2*9.8*py-2*9.8*sin(px)-9.8,'>')

initial_state = {'d':('s1',),'c':['X1 - 5.25>0','X1 - 5.75<0','X2 - 1<0','(X1 - 4.25)^2 + (X2 - 0.25)^2 - 0.0625>0']}
bad_state = predicate.MetitPredicate((x1-4.25)**2+(x2-0.25)**2-0.0625,'=')

x1_inv1 = predicate.MetitPredicate(x1-4,'<')
x1_inv2 = predicate.MetitPredicate(x1-6,'>')

s1x2_inv1 = predicate.MetitPredicate(x2,'<')
s1x2_inv2 = predicate.MetitPredicate(x2-1,'>')

s2x2_inv1 = predicate.MetitPredicate(x2-1,'<')
s2x2_inv2 = predicate.MetitPredicate(x2-2,'>')


system_def = {('s1',) : {'flow' : { x1.diff(t): 1 - sqrt(x1),
                                    x2.diff(t): sqrt(x1)-sqrt(x2),},
                                        #b.diff(t): 1},
                        't' : [{'guard':([guard],), 
                                'next_state' : ('s2',),
                                'updates' : {}}],
                        'inv' : (x1_inv1,x1_inv2,s1x2_inv1,s1x2_inv2)},
              ('s2',) : {'flow' : { x1.diff(t): 1 - sqrt(x1-x2+1),
                                    x2.diff(t): sqrt(x1-x2+1)-sqrt(x2)},
                         't' : [{'guard':([guard],),
                                 'next_state' : ('s1',),
                                 'updates' : {}}],
                        'inv' : (x1_inv1,x1_inv2,s2x2_inv1,s2x2_inv2)}}
                                 
                                    
x1eq = predicate.MetitEquation(1 - sqrt(x1))
x1d = predicate.metit_derivative(x1eq, ('s1',), system_def)

x2eq = predicate.MetitEquation(sqrt(x1)-sqrt(x2))
x2d = predicate.metit_derivative(x2eq, ('s1',), system_def)

equations = [predicate.MetitEquation(guard_equation,var_id=2),
             #predicate.MetitEquation(x1,var_id=1),
             #predicate.MetitEquation(x2,var_id=2),
             predicate.MetitEquation((x1-4.25)**2+(x2-0.25)**2-0.0625),
             predicate.MetitEquation(x1-4,var_id=1),
             predicate.MetitEquation(x1-6,var_id=1),
             #predicate.MetitEquation(x2-2,var_id=2),
             predicate.MetitEquation(x1-5.25,var_id=1),
             predicate.MetitEquation(x1-5.75,var_id=1),
             #predicate.MetitEquation(x2-0.5,var_id=2),
             #x1d,x2d
             predicate.MetitEquation(1-sqrt(x1)),
             predicate.MetitEquation(sqrt(x1)-sqrt(x2))]
             

             
             










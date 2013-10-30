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

ge = x2 - 1
guard = predicate.MetitPredicate(ge,'=')

e1 = x1-4
e2 = x1-6
e3 = x1-5.25
e4 = x1-5.75
e5 = 1-sqrt(x1)
e6 = sqrt(x1)-sqrt(x2)
e7 = (x1-4.25)**2+(x2-0.25)**2-0.0625

equations = [predicate.MetitEquation(ge,var_id=2),
             predicate.MetitEquation(e7),
             predicate.MetitEquation(e1,var_id=1),
             predicate.MetitEquation(e2,var_id=1),
             predicate.MetitEquation(e3,var_id=1),
             predicate.MetitEquation(e4,var_id=1),
             predicate.MetitEquation(e6),
             predicate.MetitEquation(e7)]


initial_state = {'d':('s1',),'c': [str(predicate.MetitPredicate(*x)) for x in
                                          [(e3,'>'),
                                           (e4,'<'),
                                           (ge,'<'),
                                           (e7,'>')]]}


#['X1 - 5.25>0','X1 - 5.75<0','X2 - 1<0','(X1 - 4.25)^2 + (X2 - 0.25)^2 - 0.0625>0']}

bad_state = predicate.MetitPredicate(e7,'=')

x1_inv1 = predicate.MetitPredicate(e1,'<')
x1_inv2 = predicate.MetitPredicate(e2,'>')

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

                        'inv' : (x1_inv1,x1_inv2,s1x2_inv1,s1x2_inv2)}
,
              ('s2',) : {'flow' : { x1.diff(t): 1 - sqrt(x1-x2+1),
                                    x2.diff(t): sqrt(x1-x2+1)-sqrt(x2)}
                         ,
                         't' : [{'guard':([guard],),
                                 'next_state' : ('s1',),
                                 'updates' : {}}]
                         ,
                        'inv' : (x1_inv1,x1_inv2,s2x2_inv1,s2x2_inv2)}}
                                 
                                    
x1eq = predicate.MetitEquation(1 - sqrt(x1))
x1d = predicate.metit_derivative(x1eq, ('s1',), system_def)

x2eq = predicate.MetitEquation(sqrt(x1)-sqrt(x2))
x2d = predicate.metit_derivative(x2eq, ('s1',), system_def)


if __name__ == '__main__':
    print initial_state

             
             










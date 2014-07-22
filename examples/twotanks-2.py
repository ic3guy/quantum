from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
import abstraction
import predicate
from predicate import MetitPredicate

t = Symbol('t')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

q = [('s1','s2','unsafe')] #can just get dictionary keys...

bad = False
extra_constraints = ''

ge = x2 - 1
guard = predicate.MetitPredicate(ge,'=')

e1 = x1-4
e2 = x1-6
e3 = x2-2

#e3 = x2-1

e4 = x1-5.25
e5 = x1-5.75
e6 = x2-0.5
#e5 = 1-sqrt(x1)
#e6 = sqrt(x1)-sqrt(x2)
e7 = (x1-4.25)**2+(x2-0.25)**2-0.0625
#e8 = x2-(6.47243 - 1.23943*x1)

equations = [predicate.MetitEquation(ge,var_id=2),
             predicate.MetitEquation(x2,var_id=2,oplist=['>','=']),
             predicate.MetitEquation(e3,var_id=2,oplist=['<','=']),
             predicate.MetitEquation(e2, var_id=1,oplist=['<','=']),
             predicate.MetitEquation(e7, oplist=['>','=']),
             predicate.MetitEquation(e1,var_id=1,oplist=['>','=']),
             predicate.MetitEquation(e5,var_id=1),
             predicate.MetitEquation(e6,var_id=2),
            # predicate.MetitEquation(e8),
             predicate.MetitEquation(e4,var_id=1)
            ]


initial_state = {'d':('s1',),'c': [str(predicate.MetitPredicate(*x)) for x in
                                          [(ge,'<'),
                                           (x2,'>'),
                                           (e7,'>'),
                                           (e4,'>'),
                                           (e5,'<'),
                                           (e6,'>'),
                                           (e1,'>')]]}


#['X1 - 5.25>0','X1 - 5.75<0','X2 - 1<0','(X1 - 4.25)^2 + (X2 - 0.25)^2 - 0.0625>0']}

bad_state = predicate.MetitPredicate(e7,'=')
#bad_state = ''

system_def = {('s1',) : {'flow' : { x1.diff(t): 1 - sqrt(x1),
                                    x2.diff(t): sqrt(x1)-sqrt(x2),},
                                        #b.diff(t): 1},

                        't' : [{'guard':([guard],), 
                                'next_state' : ('s2',),
                                'updates' : {}},
                               {'guard':([MetitPredicate(e7,'=')],),
                                'next_state': ('unsafe',),
                                'updates' : {}}],
                         'inv' : (MetitPredicate(x1-4,'<'),
                                  MetitPredicate(x1-6,'>'),
                                  MetitPredicate(x2,'<'),
                                  MetitPredicate(x2-1,'>'),
                                  MetitPredicate(x2-2,'>'), 
                                  MetitPredicate(x2-2,'=')),
                         'colour':'lightblue'},
              ('s2',) : {'flow' : { x1.diff(t): 1 - sqrt(x1-x2+1),
                                    x2.diff(t): sqrt(x1-x2+1)-sqrt(x2)}
                         ,
                         't' : [{'guard':([guard],),
                                 'next_state' : ('s1',),
                                 'updates' : {}}],
                         'inv' : (MetitPredicate(x1-4,'<'),
                                  MetitPredicate(x1-6,'>'),
                                  MetitPredicate(x2-1,'<'),
                                  MetitPredicate(x2-2,'>'),
                                  MetitPredicate(x2,'<'),
                                  MetitPredicate(x2,'='),
                                  MetitPredicate(x2-0.5,'<'),
                                  MetitPredicate(x2-0.5,'=')),
                         'colour':'green'},
              ('unsafe',): {'flow' : {x1.diff(t) : 0,
                                      x2.diff(t) : 0},
                            't' : [],
                            'inv': (MetitPredicate(x1-4,'<'),
                                    MetitPredicate(x1-6,'>'),
                                    MetitPredicate(x2,'<'),
                                    MetitPredicate(x2-1,'>')),
                            'colour': 'red'}}
                                 
                                    
x1eq = predicate.MetitEquation(1 - sqrt(x1))
x1d = predicate.metit_derivative(x1eq, ('s1',), system_def)

x2eq = predicate.MetitEquation(sqrt(x1)-sqrt(x2))
x2d = predicate.metit_derivative(x2eq, ('s1',), system_def)



if __name__ == '__main__':
    print initial_state

             
             










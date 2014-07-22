from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
import abstraction
import predicate
from predicate import MetitPredicate
from predicate import MetitEquation

t = Symbol('t')
x1 = Function('x1')(t)
x2 = Function('x2')(t)

q = [('s1','s2','unsafe')] #can just get dictionary keys...

bad = False
extra_constraints = ''

ge = x2 - 1
guard = predicate.MetitPredicate(ge,'=')

# e1 = x1-4
# e2 = x1-6
# e3 = x2-2

# #e3 = x2-1

# e4 = x1-5.25
# e5 = x1-5.75
# e6 = x2-0.5
#e5 = 1-sqrt(x1)
#e6 = sqrt(x1)-sqrt(x2)
unsafe = (x1-4.25)**2+(x2-0.25)**2-0.0625
init = (x1-5.5)**2+(x2-0.25)**2-0.0625
e8 = x2-(6.47243 - 1.23943*x1)

equations = [predicate.MetitEquation(ge,var_id=2),
             MetitEquation(unsafe),
             MetitEquation(init),
             e8
            ]


initial_state = {'d':('s1',),'c': [str(predicate.MetitPredicate(*x)) for x in
                                   [(e8, '>'),
                                    (init, '<'),
                                    (unsafe, '>')]]}



bad_state = MetitPredicate(unsafe,'<')

system_def = {('s1', ): {'flow': {x1.diff(t): 1 - sqrt(x1),
                                  x2.diff(t): sqrt(x1)-sqrt(x2),},
                         't': [{'guard': ([guard], ),
                                'next_state': ('s2', ),
                                'updates': {}},
                               {'guard':([MetitPredicate(unsafe,'=')],),
                                'next_state': ('unsafe',),
                                'updates': {}}],
                         'inv': (),
                         'colour':'lightblue'},
              ('s2',) : {'flow' : { x1.diff(t): 1 - sqrt(x1-x2+1),
                                    x2.diff(t): sqrt(x1-x2+1)-sqrt(x2)}
                         ,
                         't' : [{'guard':([guard],),
                                 'next_state' : ('s1',),
                                 'updates' : {}}],
                         'inv' : (),
                         'colour':'green'},
              ('unsafe',): {'flow' : {x1.diff(t) : 0,
                                      x2.diff(t) : 0},
                            't' : [],
                            'inv': (),
                            'colour': 'red'}}
                                 
                                    


if __name__ == '__main__':
    print initial_state

             
             










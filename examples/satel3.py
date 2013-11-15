from sympy import *
from sympy import sqrt as ssqrt
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
import abstraction
import predicate
from predicate import MetitPredicate, MetitEquation

t = Symbol('t')
nu1 = Function('nu1')(t)
nu2 = Function('nu2')(t)

q = [('initial','rendezvous')] #can just get dictionary keys...

bad = False
extra_constraints = ['NU1<5.5','NU2<5.5']
#extra_constraints = ''
bad_state = ''

def nudot(nu, p, e):
    b = ssqrt(1.0/(p**3))
    e = (1+e*cos(nu))**2
    
    return b*e

def nu_x(nu, p, e):
    r = p/(1+e*cos(nu))
    
    return r*cos(nu)

def nu_y(nu, p, e):
    r = p/(1+e*cos(nu))
    
    return r*sin(nu)

def dist(nu1, p1, e1, nu2, p2, e2):
    return (nu_x(nu1,p1,e1)-nu_x(nu2,p2,e2))**2 + (nu_y(nu1,p1,e1)-nu_y(nu2,p2,e2))**2

e1 = nu1 - 4
e2 = nu2 - 1
e4 = nu1 - 5

#e3 = dist(nu1,7467,0.10,nu2,7670,0.10) - 2500000
#e3 = 4.124 + 0.817*nu1 - nu2

#this better1
#e3 = -137.513 + 1.59823*nu1 - 0.00142977*nu1**2 - nu2
e3=-5.76876 + 2.418415*nu1 - 0.16014*nu1**2 - nu2

e6 = 1.1*nu1 - nu2 - 50
e7 = nu1 - 90

nd1 = nudot(nu1, 7467,0.10)
nd2 = nudot(nu2, 7670,0.10)


equations = [predicate.MetitEquation(nu1),
             predicate.MetitEquation(nu2),
             predicate.MetitEquation(e3),
             MetitEquation(e1),
             MetitEquation(e2),
             MetitEquation(e4)
            ]

initial_state = {'d':('initial',),'c': [str(predicate.MetitPredicate(*x)) for x in
                                          [(nu1,'>'),
                                           (nu2,'>'),
                                           (e3,'>'),
                                           (e2,'<'),
                                           (e1,'>'),
                                           (e4,'<')]]}


system_def = {('initial',) : {'flow' : { nu1.diff(t): nd1,
                                         nu2.diff(t): nd2},
                              't' : [{'guard':([MetitPredicate(e3,'=')],), 
                                      'next_state' : ('rendezvous',),
                                      'updates' : {}}],
                              'inv' : [MetitPredicate(e3,'<')],
                              'colour':'green'},
              ('rendezvous',) : {'flow' : { nu1.diff(t): 0,
                                            nu2.diff(t): 0},
                                 't' : [{'guard':(),
                                         'next_state' : (),
                                         'updates' : {}}],
                                 'inv' : (),
                                 'colour':'red'}}
                                 

if __name__ == '__main__':
    print initial_state
    print nu1

             
             










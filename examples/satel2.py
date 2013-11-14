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
extra_constraints = ['NU1<300','NU2<300']
#extra_constraints = ''
bad_state = ''

def nudot(nu, p, e):
    b = ssqrt(1.0/(p**3))
    e = (1+e*cos(nu * 3.14/180))**2
    
    return b*e

def nu_x(nu, p, e):
    r = p/(1+e*cos(nu*3.14/180))
    
    return r*cos(nu*3.14/180)

def nu_y(nu, p, e):
    r = p/(1+e*cos(nu*3.14/180))
    
    return r*sin(nu*3.14/180)

def dist(nu1, p1, e1, nu2, p2, e2):
    return (nu_x(nu1,p1,e1)-nu_x(nu2,p2,e2))**2 + (nu_y(nu1,p1,e1)-nu_y(nu2,p2,e2))**2

e1 = nu1 - 100
e2 = nu2 - 150
e3 = dist(nu1,7074,0.05,nu2,7748,0.10) - 250000

e6 = 1.1*nu1 - nu2 - 50
e7 = nu1 - 90

nd1 = nudot(nu1, 7074,0.05)
nd2 = nudot(nu2, 7748,0.10)


equations = [predicate.MetitEquation(nu1),
             predicate.MetitEquation(nu2),
             predicate.MetitEquation(e3),
             MetitEquation(e1),
             MetitEquation(e2),
             MetitEquation(e7),
             MetitEquation(e6)
            ]

initial_state = {'d':('initial',),'c': [str(predicate.MetitPredicate(*x)) for x in
                                          [(nu1,'>'),
                                           (nu2,'>'),
                                           (e3,'>'),
                                           (e1,'<'),
                                           (e2,'<'),
                                           (e6,'>'),
                                           (e7,'>')]]}


system_def = {('initial',) : {'flow' : { nu1.diff(t): nd1,
                                         nu2.diff(t): nd2},
                              't' : [{'guard':([MetitPredicate(dist(nu1,7074,0.05,nu2,7748,0.10) - 250000,'=')],), 
                                      'next_state' : ('rendezvous',),
                                      'updates' : {}}],
                              'inv' : [MetitPredicate(dist(nu1,7074,0.05,nu2,7748,0.10) - 250000,'<')],
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

             
             









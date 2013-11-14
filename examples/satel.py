from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work
import abstraction
import predicate
from predicate import MetitPredicate, MetitEquation

t = Symbol('t')
nu1 = Function('nu1')(t)
nu2 = Function('nu2')(t)

q = [('initial','transfer','rendezvous')] #can just get dictionary keys...

bad = False
extra_constraints = ''
bad_state = ''

def nudot (nu, p, e):
    b = sqrt(1.0/p**3)
    e = (1+e*cos(nu))**2
    
    return b*e

def nu_x (nu, p, e):
    r = p/(1+e*cos(nu))
    
    return r*cos(nu)

def nu_y (nu, p, e):
    r = p/(1+e*cos(nu))
    
    return r*sin(nu)

def dist (nu1, p1, e1, nu2, p2, e2):
    return sqrt((nu_x(nu1,p1,e1)-nu_x(nu2,p2,e2))**2 + (nu_y(nu1,p1,e1)-nu_y(nu2,p2,e2))**2)

e1 = nu1 - 330
e2 = nu2 - 330
e3 = dist(nu1,6718,0,nu2,676,0.0585) - 500
e4 = nu1 - 270
e5 = nu2 - 267.5

equations = [predicate.MetitEquation(nu1,var_id=2),
             predicate.MetitEquation(nu2),
             predicate.MetitEquation(e3),
             predicate.MetitEquation(e1),
             MetitEquation(e2),
             MetitEquation(e4),
             MetitEquation(e5)
            ]

initial_state = {'d':('initial',),'c': [str(predicate.MetitPredicate(*x)) for x in
                                          [(e4,'='),
                                           (e5,'='),
                                           (e1,'<'),
                                           (e2,'<')]]}


system_def = {('initial',) : {'flow' : { nu1.diff(t): nudot(nu1, 6718,0),
                                         nu2.diff(t): nudot(nu2, 7340,0.05)},
                              't' : [{'guard':([MetitPredicate(nu1-330,'='), MetitPredicate(nu2-330,'=')],), 
                                      'next_state' : ('transfer',),
                                      'updates' : {}}],
                              'inv' : (),
                              'colour':'lightblue'},
              ('transfer',) : {'flow' : { nu1.diff(t): nudot(nu1, 6718,0),
                                          nu2.diff(t): nudot(nu2, 6767,0.0585)},
                               't' : [{'guard':([MetitPredicate(dist(nu1,6718,0,nu2,676,0.0585) - 500,'<')],),
                                       'next_state' : ('rendezvous',),
                                       'updates' : {}}],
                         'inv' : (),
                         'colour':'green'},
              ('rendezvous',): {'flow' : {nu1.diff(t) : 0,
                                          nu2.diff(t) : 0},
                                't' : [],
                                'inv': (),
                                'colour': 'red'}}
                                 

if __name__ == '__main__':
    print initial_state

             
             










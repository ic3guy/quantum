from sympy import *
from itertools import product
#product is a name inside sympy, so we can't redefine it here. Otherwise import won't work

t = Symbol('t')
PX = Symbol('PX') #x1 = vx
PY = Symbol('PY') #x2 = vy
VX = Symbol('VX')
VY = Symbol('VY')

px = Function('px')(t)
py = Function('py')(t)
vx = Function('vx')(t)
vy = Function('vy')(t)

q = [('falling',)] #can just get dictionary keys...

deriv_dict = {('falling',) : {px.diff(t): vx,
                              py.diff(t): vy,
                              vx.diff(t): 0,
                              vy.diff(t): -9.8 + 0.01*vy**2}}

vars_dict = {px : PX, py : PY, vx : VX, vy: VY}

guard_equation = predicate.MetitEquation(sin(px)-py,'t',deriv_dict,vars_dict)
guard = predicate.MetitPredicate(guard_equation,'=')

updates = {guard : {'vx' : ((1-0.8*cos(px)**2)*vx + 1.8*cos(px)*vy)/(1+cos(px)**2), 
                    'vy' : (1.8*cos(px)*vx + (-0.8+cos(px)**2)*vy)/(1+cos(px)**2)}}

equations = [predicate.MetitEquation(vx,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(vy,'t',deriv_dict,vars_dict),
#predicate.MetitEquation(-9.8*sin(x1),'t',deriv_dict,vars_dict),
#predicate.MetitEquation(x1-3.141592654,'t',deriv_dict,vars_dict),
#predicate.MetitEquation(x2-15,'t',deriv_dict,vars_dict),
#with friction predicate.MetitEquation(2.1351*sin(x1)**2 + 2.1351*cos(x1)**2 - 4.3702*cos(x1) + 0.22297*x2**2 + 0.2351,'t',deriv_dict,vars_dict)]
predicate.MetitEquation(1.90843655*sin(x1)**2 + 1.90843655*cos(x1)**2 - 3.916868466*cos(x1) + 0.19984*x2**2 + 0.0084319171,'t',deriv_dict,vars_dict,is_lyapunov=True)]
#   3.5892-3.7822*cos(x1)+3.0066*cos(x1)**2+2.8136*sin(x1)**2 + 0.19297*x2**2-5,'t',deriv_dict, vars_dict)]

#e5 = predicate.MetitEquation(deriv_dict[x2.diff(t)],'t',deriv_dict,vars_dict)
#equations.extend(predicate.get_derivs(1,e5))


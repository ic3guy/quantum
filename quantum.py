from sympy import *
import metitarski
from itertools import product

t = Symbol('t')
X1 = Symbol('X1')
X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)
    
    
deriv_dict = {x1.diff(t): x2,
              x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

vars_dict = {x1(t) : X1, x2(t) : X2}
    
equations = [MetitEquation(x1,'t',deriv_dict,vars_dict),
             MetitEquation(x2,'t',deriv_dict,vars_dict),
             MetitEquation(sin(x1)*cos(x1)-10*sin(x1),'t',deriv_dict,vars_dict),
             MetitEquation(0.3345*x2**2+1.4615*sin(x1)**2+1.7959*cos(x1)**2-6.689*cos(x1)+4.6931, 't',deriv_dict, vars_dict)]

e5 = MetitEquation(deriv_dict[x2.diff(t)],'t',deriv_dict,vars_dict)
equations.extend(get_derivs(1,e5))

feasible = 0
infeasible = 0
oplist = ['>','<','=']
inftest = []
    
for equation in equations:
    predlist = [MetitPredicate(equation,op) for op in oplist]
    inftest.append(predlist)

system = [State('X1,X2',*element) for element in product(*inftest)]

for state in system:
    print metitarski.make_fof_inf(state)
    rc = metitarski.send_to_metit(metitarski.make_fof_inf(state),output=False)
    if rc == 0:
        infeasible = infeasible+1
        state.is_feasible = False
    
print "Feasible %s" % feasible
print "Infeasible %s" % infeasible

system_f = [state for state in system if state.is_feasible]

for state in system_f:
    for predicate in state.state:
        print metitarski.checkTransition(state,predicate)

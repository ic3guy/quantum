from sympy import *
import metitarski
from itertools import product
import predicate

t = Symbol('t')
X1 = Symbol('X1')
X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)
    
    
deriv_dict = {x1.diff(t): x2,
              x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

vars_dict = {x1(t) : X1, x2(t) : X2}
    
equations = [predicate.MetitEquation(x1,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x2,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(sin(x1)*cos(x1)-10*sin(x1),'t',deriv_dict,vars_dict),
             predicate.MetitEquation(0.3345*x2**2+1.4615*sin(x1)**2+1.7959*cos(x1)**2-6.689*cos(x1)+4.6931, 't',deriv_dict, vars_dict)]

e5 = predicate.MetitEquation(deriv_dict[x2.diff(t)],'t',deriv_dict,vars_dict)
equations.extend(predicate.get_derivs(1,e5))

feasible = 0
infeasible = 0
oplist = ['>','=']
inftest = []
    
for equation in equations:
    predlist = [predicate.MetitPredicate(equation,op) for op in oplist]
    inftest.append(predlist)

system = [predicate.State('X1,X2',*element) for element in product(*inftest)]

for state in system:
    #print metitarski.make_fof_inf(state)
    rc = metitarski.send_to_metit(metitarski.make_fof_inf(state),output=False)
    if rc == 0:
        infeasible = infeasible+1
        state.is_feasible = False
    else:
        feasible = feasible+1
        
print "Feasible %s" % feasible
print "Infeasible %s" % infeasible

system_f = [state for state in system if state.is_feasible]

def find_states(state_list, preds):
    for sta in preds:
        return [x for x,state in enumerate(state_list) if all(i in sta for i in state.state)]
    
for n,state in enumerate(system_f):
    pos_successors = []
    
    for pred in state.state:
        print pred.operator
        pos_successors.append(metitarski.checkTransition(state,pred))

    #print pos_successors
    #print "State %s :" % list(product(*pos_successors))

    #for state in product(*pos_successors)

    nstate = []
    
    for state2 in product(*pos_successors):
        #print state
        ss = predicate.State('X1,X2',*state2)
        #print ss
        
        for x, s in enumerate(system_f):
            if s == ss:
                nstate.append(x)
            #else:
                #print 'no state found'

    print "From State %s Next State %s" % (n,nstate)
   # print find_states(system_f,product(*pos_successors))
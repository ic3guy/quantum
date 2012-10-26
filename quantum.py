from sympy import *
import metitarski
from itertools import product
import predicate
import datetime
import os
import nusmv

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
oplist = ['>','=','<']
inftest = []
    
for equation in equations:
    predlist = [predicate.MetitPredicate(equation,op) for op in oplist]
    inftest.append(predlist)

system = [predicate.State('X1,X2',n,*element) for n,element in enumerate(product(*inftest))]

now = datetime.datetime.now()
directory_name = now.strftime('%d-%m-%Y--%H:%M:%S')

os.makedirs('/opt/quantum/'+ directory_name + '/firstpass/proved')
os.makedirs('/opt/quantum/'+ directory_name + '/firstpass/unproved')

for state in system:
    #print metitarski.make_fof_inf(state)
    print "checking state %s"  % state.get_state_number()
    fof = metitarski.make_fof_inf(state)
    rc = metitarski.send_to_metit(fof,output=False,tofile=False)
    if rc == 0:
        infeasible = infeasible+1
        state.is_feasible = False
        print 'it is not feasible, proved'
    else:
        feasible = feasible+1
        print 'it is feasible, unproved'
        metitarski.send_to_file(fof, directory_name + '/firstpass/unproved', '%s' % state.number)

print "Feasible %s" % feasible
print "Infeasible %s" % infeasible

print "Second Run"

feasible = 0
infeasible = 0

options = ('metit', 
           '--autoInclude', 
           '--time','30',
           '-')

os.makedirs('/opt/quantum/'+ directory_name + '/secondpass/proved')
os.makedirs('/opt/quantum/'+ directory_name + '/secondpass/unproved')

for state in system:
    #print metitarski.make_fof_inf(state)
    if state.is_feasible:
        print "checking state %s"  % state.get_state_number()
        fof = metitarski.make_fof_inf(state)
        rc = metitarski.send_to_metit(fof,output=False,tofile=False,metit_options=options)
        if rc == 0:
            infeasible = infeasible+1
            state.is_feasible = False
        else:
            feasible = feasible+1
            metitarski.send_to_file(fof, directory_name + '/secondpass/unproved', '%s' % state.number)

print "Feasible %s" % feasible
print "Infeasible %s" % infeasible

system_f = [state for state in system if state.is_feasible]

raw_input()

def find_states(state_list, preds):
    for sta in preds:
        return [x for x,state in enumerate(state_list) if all(i in sta for i in state.state)]
    
for state in system_f:
    pos_successors = []
    
    for pred in state.state:
        #print pred.operator
        pos_successors.append(metitarski.checkTransition(state,pred))

    #print pos_successors
    #print "State %s :" % list(product(*pos_successors))

    #for state in product(*pos_successors)

    nstate = []
    
    for state2 in product(*pos_successors):
        #print state
        ss = predicate.State('X1,X2',666,*state2)
        #print ss
        
        for s in system_f:
            if s == ss:
                nstate.append(s.number)
            #else:
            #    print 'no state found'

    print "From State %s Next State %s" % (state.number,nstate)
    state.next_states = nstate
   # print find_states(system_f,product(*pos_successors))

nusmv.construct_nusmv_input(system_f,23)

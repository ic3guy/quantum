from sympy import *
import metitarski
from itertools import product
import predicate
import datetime
import os
import nusmv
import timing

t = Symbol('t')
X1 = Symbol('X1')
X2 = Symbol('X2')
x1 = Function('x1')(t)
x2 = Function('x2')(t)
    
    
deriv_dict = {x1.diff(t): x2,
              x2.diff(t): -9.8*sin(x1)}

vars_dict = {x1(t) : X1, x2(t) : X2}
    
equations = [predicate.MetitEquation(x1,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x2,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(-9.8*sin(x1),'t',deriv_dict,vars_dict),
             #predicate.MetitEquation(x1-1,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(x2-15,'t',deriv_dict,vars_dict),
             predicate.MetitEquation(0.3345*x2**2+1.4615*sin(x1)**2+1.7959*cos(x1)**2-6.689*cos(x1)+4.6931-15, 't',deriv_dict, vars_dict)]

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
    rc = metitarski.send_to_metit(fof,output=True,tofile=False)
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

'''print "Second Run"

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
'''
system_f = [state for state in system if state.is_feasible]

#print 'Press -ENTER- to continue'
#raw_input()

def find_states(state_list, preds):
    for sta in preds:
        return [x for x,state in enumerate(state_list) if all(i in sta for i in state.state)]

    
for state in system:
    pos_successors = []
    
    if state.is_feasible:
        for pred in state.state:
            Q1,Q2,Q3 = metitarski.checkTransition2(state,pred)
            print "In Q1 : %s" % Q1
            print "In Q2 : %s" % Q2
            print "In Q3 : %s" % Q3

            pre = predicate.MetitEquation(pred.equation.equation,pred.equation.depvar,pred.equation.subs_dict,pred.equation.vars_dict)
            lt_pred = predicate.MetitPredicate(pre,'<')
            gt_pred = predicate.MetitPredicate(pre,'>')
            eq_pred = predicate.MetitPredicate(pre,'=')

            if pred.operator == '>':
                if state in Q1: 
                    pos_successors.append([gt_pred])
                else:
                    pos_successors.append([gt_pred,eq_pred])
            elif pred.operator == '<':
                if state in Q3:
                    pos_successors.append([lt_pred])
                else:
                    pos_successors.append([lt_pred,eq_pred])
            else:
                if state in Q1 and state in Q2:
                    pos_successors.append([gt_pred])
                elif state in Q3 and state in Q2:
                    pos_successors.append([lt_pred])
                elif state in Q1 and state in Q3:
                    pos_successors.append([eq_pred])
                else:
                    pos_successors.append([eq_pred,lt_pred,gt_pred])
#print pred.operator
        
       # pos_successors.append(metitarski.checkTransition(state,pred))

    #print pos_successors
    #print "State %s :" % list(product(*pos_successors))

    #for state in product(*pos_successors)

        nstate = []
        
        for state2 in product(*pos_successors):
        #print state
            ss = predicate.State('X1,X2',666,*state2)
        #print ss
        
            for s in system:
                if s == ss and s.is_feasible:
                    nstate.append(s.number)
            #else:
                #print 'no next state state found'
                
        if nstate: 
            print "From State %s Next State %s" % (state.number,nstate)
            state.next_states = nstate
        else:
            print 'no next state found, deleting'
            state.is_feasible = False
   # print find_states(system_f,product(*pos_successors))

nusmv.construct_nusmv_input(system,23)
timing.endlog()

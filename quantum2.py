from sympy import *
import metitarski
from itertools import product
import predicate
import datetime
import os
import nusmv
#import timing
import time
from termcolor import colored, cprint

#abspath = os.path.abspath(__file__)
#dname = os.path.dirname(abspath)
#os.chdir(dname)

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])
           
#execfile('/Users/will/Research/quantum/simplePendulum.py')
execfile('simplePendulum.py')
start_time = time.time()    

feasible = 0
infeasible = 0
oplist = ['>','=','<']
inftest = []
system = []
    
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
    fof = metitarski.make_fof_inf(state,subsdict={'e':'*10^'})
    rc = metitarski.send_to_metit(fof,output=True,tofile=False)
    if rc == 0:
        infeasible = infeasible+1
        state.is_feasible = False
        cprint('it is not feasible, proved', 'green')
    else:
        feasible = feasible+1
        print cprint('it is feasible, unproved', 'red')
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
        for x,pred in enumerate(state.state):
            Q1,Q2,Q3 = metitarski.checkTransition2(state,pred,x)
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
end_time = time.time()

print 40*'='
print 'Time taken', secondsToStr(end_time-start_time)
print 40*'='

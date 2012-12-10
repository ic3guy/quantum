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
import qutilities

#abspath = os.path.abspath(__file__)
#dname = os.path.dirname(abspath)
#os.chdir(dname)

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])
           
#execfile('/Users/will/Research/quantum/simplePendulum.py')
#execfile('heater.py')
#execfile('/Users/will/Research/quantum/heater.py')
#execfile('/Users/will/Research/quantum/bounceBallsin.py',globals())
execfile('bounceBallsin.py',globals())

start_time = time.time()    

feasible = 0
infeasible = 0
oplist = ['>','=','<']
inftest = []
system = []
    
for equation in equations:
    predlist = [predicate.MetitPredicate(equation,op) for op in oplist]
    inftest.append(predlist)

system = [predicate.State('PX,PY,VX,VY',n,'None', deriv_dict,*element) for n,element in enumerate(product(*inftest))]

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

system_f = [state for state in system if state.is_feasible]

system_fd = qutilities.make_discrete_system(system_f,q)

#removing states that violate the invariant
for state in system_fd:
	if [pred for pred in deriv_dict[state.discrete_part]['inv'] if pred in state.state]:
		state.is_feasible = False

system_fd = [state for state in system_fd if state.is_feasible]

#pre = predicate.MetitEquation(x-82,'t',[],{x : X})
#g_pred_82gt = predicate.MetitPredicate(pre,'>')
#pre = predicate.MetitEquation(x-68,'t',[],{x : X})
#g_pred_68lt = predicate.MetitPredicate(pre,'<')

#for s in system_fd:
#	if g_pred_82gt in s.state or g_pred_68lt in s.state:
#		s.is_feasible=False

#print 'Press -ENTER- to continue'
#raw_input()

def find_states(state_list, preds):
    for sta in preds:
        return [z for z,state in enumerate(state_list) if all(i in sta for i in state.state)]

for state in system_fd:
	pos_successors = []
	for z,pred in enumerate(state.state):
		Q1,Q2,Q3 = metitarski.checkTransition2(state,pred,z)
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
		ss = predicate.State('X',666,state.discrete_part, deriv_dict,*state2) #check only states within same discrete mode
        #print ss
        
		for s in system_fd:
			if s == ss and s.is_feasible and s.discrete_part==ss.discrete_part: #check matching discrete parts
				nstate.append(s.number)
            #else:
                #print 'no next state state found'
                
	if nstate: 
		print "From State %s Next State %s" % (state.number,nstate)
		state.next_states = nstate
	else:
		print 'no next state found, deleting'
		state.is_feasible = False
   # print find_states(system_f,product(*pos_successors
   
for state in system_fd:
    nstate = []
    for qn,discrete_q in enumerate(product(*q)):
        if state.discrete_part == discrete_q:
            for pred in state.state:
                for transition in state.deriv_dict[state.discrete_part]['t']:
                    if pred in transition['guard']:
                        print 'found guard'
                        pos_successors = []
                        if transition['updates']:
                            print 'doing some updating'
                            for z,pred2 in enumerate(state.state):
                                Q1,Q2,Q3 = metitarski.checkTransition3(state,pred2,z,state.deriv_dict,transition)
                                print "In Q1 : %s" % Q1
                                print "In Q2 : %s" % Q2
                                print "In Q3 : %s" % Q3
                        
                                pre = predicate.MetitEquation(pred2.equation.equation,pred2.equation.depvar,pred2.equation.subs_dict,pred2.equation.vars_dict)
                                lt_pred = predicate.MetitPredicate(pre,'<')
                                gt_pred = predicate.MetitPredicate(pre,'>')
                                eq_pred = predicate.MetitPredicate(pre,'=')

                                if state in Q1 and state in Q2: 
                                    pos_successors.append([gt_pred])
                                elif state in Q3 and state in Q2:
                                    pos_successors.append([lt_pred])
                                elif state in Q1 and state in Q3:
                                    pos_successors.append([eq_pred])
                                elif state in Q1:
                                    pos_successors.append([gt_pred,eq_pred])
                                elif state in Q2:
                                    pos_successors.append([gt_pred,lt_pred])
                                elif state in Q3:
                                    pos_successors.append([lt_pred,eq_pred])
                                else:
                                    pos_successors.append([eq_pred,lt_pred,gt_pred])              

                                for state2 in product(*pos_successors):
                                    ss = predicate.State('X',666,transition['next_state'], deriv_dict,*state2) 
                                    for s in system_fd:
                                        if s == ss and s.is_feasible and s.discrete_part==ss.discrete_part: #check matching discrete parts
                                            nstate.append(s.number)
                                            print 'found new continuous abstract state'
           
                
                                            if nstate: 
                                                print "From State %s Next State %s" % (state.number,nstate)
                                                state.next_states = nstate
                                            else:
                                                print 'no next state found, deleting'
                                                state.is_feasible = False

                        for next_discrete_state in product(*q): 
                            #made it from qn+1 to qn
                            print 'in here'
                            ss = predicate.State('X',666,transition['next_state'], deriv_dict,*state.state)
                            for s in system_fd:
                                if s == ss and s.is_feasible and s.discrete_part==ss.discrete_part: #check matching discrete parts
									if s.number not in state.next_states and s.number not in nstate: 
										nstate.append(s.number)
										print nstate
									else:
										print 'already in nstate or next_states'
    if nstate:
		#if [i for i in nstate if i in state.next_states]: 
		print "From State %s Next State %s" % (state.number,nstate)
		state.next_states.extend(nstate)
    else:
        print 'no next state found, no switching'
        #tate.is_feasible = False


#remove duplicate next states.
for s in system_fd:
	s.next_states = list(set(s.next_states))

#convert from list to dictionary
system_fdd = {}
        
for s in system_fd:
	system_fdd[s.number] = s
   
nusmv.construct_nusmv_input(system_fdd,2)
end_time = time.time()

print 40*'='
print 'Time taken', secondsToStr(end_time-start_time)
print 40*'='

#for s in system:
#	if s.is_feasible:
#		if 'X - 80>0' in [pred.equation_string for pred in s.state]:
#			s.discrete_part = 'off'

   
for key,s in system_fdd.iteritems():
	if s.is_feasible:
		print "From State %s : %s-%s to States %s" % (s.number, s.get_state(),s.discrete_part,s.next_states)




    

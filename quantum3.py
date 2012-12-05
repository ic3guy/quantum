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
execfile('heater.py')
start_time = time.time()    

feasible = 0
infeasible = 0
oplist = ['>','=','<']
inftest = []
system = []
    
for equation in equations:
    predlist = [predicate.MetitPredicate(equation,op) for op in oplist]
    inftest.append(predlist)

system = [predicate.State('X',n,'None',*element) for n,element in enumerate(product(*inftest))]

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

system_fd = qutilities.make_discrete_system(system_f,['on','off'])

pre = predicate.MetitEquation(x-82,'t',[],{x : X})
g_pred_82gt = predicate.MetitPredicate(pre,'>')
pre = predicate.MetitEquation(x-68,'t',[],{x : X})
g_pred_68lt = predicate.MetitPredicate(pre,'<')

for s in system_fd:
	if g_pred_82gt in s.state or g_pred_68lt in s.state:
		s.is_feasible=False

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
		ss = predicate.State('X',666,state.discrete_part,*state2) #check only states within same discrete mode
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

pre = predicate.MetitEquation(x-80,'t',[],{x : X})
g_pred_80gt = predicate.MetitPredicate(pre,'>')
g_pred_80eq = predicate.MetitPredicate(pre,'=')

pre = predicate.MetitEquation(x-70,'t',[],{x : X})	
g_pred_70lt = predicate.MetitPredicate(pre,'<') 	
g_pred_70eq = predicate.MetitPredicate(pre,'=') 
   
for state in system_fd:
	nstate = []
	if state.discrete_part == ('on',):
		for pred in state.state:           
			if pred == g_pred_80gt or pred == g_pred_80eq:
				print 'in 80'
				ss = predicate.State('X',666,('off',),*state.state)
				for s in system_fd:
					if s == ss and s.is_feasible and s.discrete_part==ss.discrete_part: #check matching discrete parts
						nstate.append(s.number)
	elif state.discrete_part == ('off',):
		#print 'in off'
		for pred in state.state:
			if pred == g_pred_70lt or pred == g_pred_70eq:
				print 'in 70'
				ss = predicate.State('X',666,('on',),*state.state)
				for s in system_fd:
					#print 'searching'
					if s == ss and s.is_feasible and s.discrete_part==ss.discrete_part: #check matching discrete parts
						nstate.append(s.number)
	if nstate: 
		print "From State %s Next State %s" % (state.number,nstate)
		state.next_states.extend(nstate)
	else:
		print 'no next state found, no switching'
		#tate.is_feasible = False
	
	
   
nusmv.construct_nusmv_input(system,23)
end_time = time.time()

print 40*'='
print 'Time taken', secondsToStr(end_time-start_time)
print 40*'='

#for s in system:
#	if s.is_feasible:
#		if 'X - 80>0' in [pred.equation_string for pred in s.state]:
#			s.discrete_part = 'off'



    
for s in system_fd:
	if s.is_feasible:
		print "From State %s : %s-%s to States %s" % (s.number, s.get_state(),s.discrete_part,s.next_states)




    

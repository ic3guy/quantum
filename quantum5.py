from sympy import *
import metitarski
from itertools import product
import predicate
import datetime
import os
import nusmv
import timing
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

execfile(exp_name)

print system_def
start_time = time.time()    

#f = open('/Users/will/Research/quantum/log.txt', 'a', 0)
f = open('log.txt', 'a', 0)

f.write(40*'*'+'\n')
f.write(exp_name + '\n')
f.write(40*'*' + '\n')

eq_list = ','.join([str(eq) for eq in equations])

f.write('Metit in Bad State : %s\n' % bad)
f.write('Predicates : %s : %s\n' % (len(equations), eq_list))

feasible = 0
infeasible = 0
oplist = ['>','=','<']
inftest = []
system = []
    
for equation in equations:
    predlist = [predicate.MetitPredicate(equation.equation,op) for op in oplist]
    inftest.append(predlist)

var_string = predicate.get_var_string(equations)
    
system = [predicate.State(n,'None',*element) for n,element in enumerate(product(*inftest))]

#f.write('Number of initial abstract states : %s \n' % len(system))
#print 'Done system'
#raw_input()

# Create directories to store proved and unproved tptp files for later analysis
now = datetime.datetime.now()
experiment_dir = 'experiments/'+ file_name + now.strftime('--%d-%m-%Y--%H:%M:%S')
# Try to enforce the current directory. Check to see how Emacs does this in OSX.

feas_check_dir = experiment_dir + '/feasability/'
feas_check_proved_dir = feas_check_dir + '/proved/'
feas_check_unproved_dir = feas_check_dir + '/unproved/'

trans_check_dir = experiment_dir + '/transitions/'
cont_trans_proved_dir = trans_check_dir + 'continuous/proved'
cont_trans_unproved_dir = trans_check_dir + 'continuous/unproved'

disc_trans_proved_dir = trans_check_dir + 'discrete/proved'
disc_trans_unproved_dir = trans_check_dir + 'discrete/unproved'

os.makedirs(feas_check_proved_dir)
os.makedirs(feas_check_unproved_dir)

os.makedirs(cont_trans_proved_dir)
os.makedirs(cont_trans_unproved_dir)

os.makedirs(disc_trans_proved_dir)
os.makedirs(disc_trans_unproved_dir)

for state in system:
    #print metitarski.make_fof_inf(state)
    print "checking state %s"  % state.print_state_number()
    fof = metitarski.make_fof_inf(state, var_string)
    #print fof
    rc = metitarski.send_to_metit(fof,output=True)
    if rc == 0:
        infeasible = infeasible+1
        state.is_feasible = False
        cprint('it is not feasible, proved', 'green')
        metitarski.send_to_file(fof, feas_check_proved_dir, '%s.tptp' % state.number)
    else:
        feasible = feasible+1
        print cprint('it is feasible, unproved', 'red')
        metitarski.send_to_file(fof, feas_check_unproved_dir, '%s.tptp' % state.number)

        #print "Feasible %s" % feasible
        #print "Infeasible %s" % infeasible

end_time1 = time.time()

#f.write('Number of feasible %s, Number of infeasible %s \n' % (feasible,infeasible))
#f.write('Abstract Feasibility took %s \n' % secondsToStr(end_time1-start_time))

system_f = [state for state in system if state.is_feasible]

system_fd = qutilities.make_discrete_system(system_f,q)

#f.write('Number of initial states in hybrid system abs : %s \n' % len(system_fd))

xx = len(system_fd)

#removing states that violate the invariant
for state in system_fd:
	if [pred for pred in system_def[state.discrete_part]['inv'] if pred in state.state]:
		state.is_feasible = False

system_fd = [state for state in system_fd if state.is_feasible]

#print 'Done system'
#raw_input()

f.write('Number that violate the invariants : %s \n' % (xx - len(system_fd))) 

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

start_abs = time.time()
    
for state in system_fd:
    pos_successors = []
    for z,pred in enumerate(state.state):
        if bad:
            Q1,Q2,Q3 = ([],[],[])
        else:
            Q1,Q2,Q3 = metitarski.checkTransition2(var_string, state,pred,z, system_def, cont_trans_unproved_dir)
        
        print "In Q1 : %s" % Q1
        print "In Q2 : %s" % Q2
        print "In Q3 : %s" % Q3

        #pre = predicate.MetitEquation(pred.equation, pred.depvar, system_def, pred.equation)
        lt_pred = predicate.MetitPredicate(pred.equation,'<')
        gt_pred = predicate.MetitPredicate(pred.equation,'>')
        eq_pred = predicate.MetitPredicate(pred.equation,'=')

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
        ss = predicate.State(666, state.discrete_part, *state2) #check only states within same discrete mode
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
        print 'no next state found, but might come during discrete abstraction. State %s' % (state.number)
        #only delete the state at the end
        #state.is_feasible = False
   # print find_states(system_f,product(*pos_successors

fcount = 0
   
for s in system_fd:
    if s.is_feasible:
        fcount = fcount + 1 

end_abs = time.time()

f.write('Number of feasible states after cont abs : %s\n' % fcount)
f.write('Cont abstraction took : %s\n'  % secondsToStr(end_abs-start_abs))

dis_abs = time.time()

for state in system_fd:
    nstate = []
    for qn,discrete_q in enumerate(product(*q)):
        if state.discrete_part == discrete_q:
            for pred in state.state:
                for transition in system_def[state.discrete_part]['t']:
                    if pred in transition['guard']:
                        print 'found guard'
                        pos_successors = []
                        if transition['updates']:
                            print 'doing some updating'
                            for z,pred2 in enumerate(state.state):
                                if bad:
                                    Q1,Q2,Q3 = ([],[],[])
                                else:
                                    Q1,Q2,Q3 = metitarski.checkTransition3(var_string, state, pred2, z, system_def, transition['updates'], directory=disc_trans_unproved_dir)
                                print "In Q1 : %s" % Q1
                                print "In Q2 : %s" % Q2
                                print "In Q3 : %s" % Q3
                        
                                #pre = predicate.MetitEquation(pred2.equation.equation,pred2.equation.depvar,pred2.equation.subs_dict,pred2.equation.vars_dict)
                                lt_pred = predicate.MetitPredicate(pred2.equation,'<')
                                gt_pred = predicate.MetitPredicate(pred2.equation,'>')
                                eq_pred = predicate.MetitPredicate(pred2.equation,'=')

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
                                    ss = predicate.State(666,transition['next_state'],*state2) 
                                    for s in system_fd:
                                        if s == ss and s.is_feasible and s.discrete_part==ss.discrete_part: #check matching discrete parts
                                            nstate.append(s.number)
                                            print 'found new continuous abstract state'
           
                
                                            if nstate: 
                                                print "From State %s Next State %s" % (state.number,nstate)
                                                state.next_states.extend(nstate)
                                            else:
                                                print 'no next state found with substitution' % (state.number)
                                                #state.is_feasible = False

                        for next_discrete_state in product(*q): 
                            #made it from qn+1 to qn
                            print 'in here'
                            ss = predicate.State(666,transition['next_state'],*state.state)
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

dis_abs_end = time.time()

f.write('Total Time for Discrete Abstraction: %s\n' % secondsToStr(dis_abs_end-dis_abs))
        
total_next_states = 0
#remove duplicate next states.
for s in system_fd:
    s.next_states = list(set(s.next_states))
    total_next_states = total_next_states + len(s.next_states)

f.write('Total number of abstract transitions: %s\n' % total_next_states)
f.write('Total number of states in final abstract system: %s\n' % len(system_fd))
    
#convert from list to dictionary
system_fdd = {}
        
for s in system_fd:
	system_fdd[s.number] = s
   

#SMV = open('/Users/will/Research/quantum/'+exp_name+'.smv','w')
SMV = open(exp_name+'.smv','w')

smv_output = nusmv.construct_nusmv_input(system_fdd,2)

SMV.write(smv_output)
end_time = time.time()

#print 40*'='
f.write('Total Time taken : %s\n' % secondsToStr(end_time-start_time))
#print 40*'='

#for s in system:
#	if s.is_feasible:
#		if 'X - 80>0' in [pred.equation_string for pred in s.state]:
#			s.discrete_part = 'off'
   
for key,s in system_fdd.iteritems():
	if s.is_feasible:
		print "From State %s : %s-%s to States %s" % (s.number, s, s.discrete_part,s.next_states)

SMV.close()        
f.close()



    

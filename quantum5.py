from sympy import *
import metitarski
from itertools import product
import predicate
import abstraction
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

#print system_def
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
initial_abstract_system = []
    
for equation in equations:
    predlist = [predicate.MetitPredicate(equation.equation,op) for op in oplist]
    inftest.append(predlist)

var_string = predicate.get_var_string(equations)
initial_abstract_system = [predicate.State(n,'None',*element) for n,element in enumerate(product(*inftest))]

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

print '*'*10 + 'CONTINUOUS FEASABILITY' + '*'*10

for state in initial_abstract_system:
    fof = metitarski.make_fof_inf(state, var_string)
    #print "Sending: " + fof
    rc = metitarski.send_to_metit(fof)
    if rc == 0:
        infeasible = infeasible+1
        state.is_feasible = False
        cprint('State %s is DEFINITELY not feasible. PROVED' % state.number, 'green')
        metitarski.send_to_file(fof, feas_check_proved_dir, '%s.tptp' % state.number)
    else:
        feasible = feasible+1
        cprint('State %s is POSSIBLY feasible. UNPROVED' % state.number, 'red')
        metitarski.send_to_file(fof, feas_check_unproved_dir, '%s.tptp' % state.number)

end_time1 = time.time()

f.write('Number of feasible %s, Number of infeasible %s \n' % (feasible,infeasible))
f.write('Abstract Feasibility took %s \n' % secondsToStr(end_time1-start_time))

system_feasible = [state for state in initial_abstract_system if state.is_feasible]

system_feasible_disc = qutilities.make_discrete_system(system_feasible,q)

f.write('Number of initial states in hybrid system abs : %s \n' % len(system_feasible_disc))

xx = len(system_feasible_disc)

#removing states that violate the invariant
for state in system_feasible_disc:
	if [pred for pred in system_def[state.discrete_part]['inv'] if pred in state.state]:
		state.is_feasible = False

system_feasible_disc_inv = [state for state in system_feasible_disc if state.is_feasible]

f.write('Number that violate the invariants : %s \n' % (xx - len(system_feasible_disc_inv))) 

start_abs = time.time()

print '*'*10 + 'CONTINUOUS ABSTRACTION' + '*'*10

for state in system_feasible_disc_inv:
    pos_successors = []
    for z,pred in enumerate(state.state):
        if bad:
            Q1,Q2,Q3 = ([],[],[])
        else:
            Q1,Q2,Q3 = metitarski.checkTransition2(var_string, state,pred,z, system_def, cont_trans_unproved_dir)
        
        lt_pred, eq_pred, gt_pred = abstraction.gen_pos_pred(pred.equation)

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
                
    next_states = []
        
    for possible_next_state in product(*pos_successors):
        found_next_state = abstraction.find_state(system_feasible_disc_inv, predicate.State(666, state.discrete_part, *possible_next_state))

        if found_next_state and not abstraction.more_than_one_diff(state, found_next_state):
            next_states.append(found_next_state.number)
        #else:
            #print 'Multiple variable jumps'
                
    if next_states: 
        print "Continuous Abstract Transition: From State %s Next State %s" % (state.number, next_states)
        state.next_states = next_states
    #else:
        #print 'no next state found, but might come during discrete abstraction. State %s' % (state.number)
        #only delete the state at the end
        #state.is_feasible = False
                    
fcount = 0
   
for s in system_feasible_disc_inv:
    if s.is_feasible:
        fcount = fcount + 1 

end_abs = time.time()

f.write('Number of feasible states after cont abs : %s\n' % fcount)
f.write('Cont abstraction took : %s\n'  % secondsToStr(end_abs-start_abs))

dis_abs = time.time()

for state in system_feasible_disc_inv:
    next_states = []
    for transition in system_def[state.discrete_part]['t']:
        if any([all([p in state.state for p in guard_conj]) for guard_conj in transition['guard']]):
            #Numpy+ipython bug. Does not like any+generator (automatically evaluates true) therefore wrap in list comprehension
            #print [x in state.state for x in transition['guard']]
            #print 'From State %s, %s, from guards %s' % (state.number, str(state), [str(x) for x in transition['guard']])
            pos_successors = []
            if transition['updates']:
                #print 'doing some updating'
                for z,pred2 in enumerate(state.state):
                    if bad:
                        Q1,Q2,Q3 = ([],[],[])
                    else:
                        Q1,Q2,Q3 = metitarski.checkTransition3(var_string, state, pred2, z, system_def, transition['updates'], directory=disc_trans_unproved_dir)

                    lt_pred, eq_pred, gt_pred = abstraction.gen_pos_pred(pred2.equation)

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

                for possible_next_state in product(*pos_successors):
                    found_next_state = abstraction.find_state(system_feasible_disc_inv, predicate.State(666, transition['next_state'], *possible_next_state))

                    if found_next_state:
                        next_states.append(found_next_state.number)
           
                if next_states: 
                    print "Updating State %s has produced Next States %s" % (state.number,next_states)
                            #is this ok, check alogorithm
                    state.next_states.extend(next_states)
                else:
                    print 'Substitution sends us to an infeasible state...possible error here.'
                    #state.is_feasible = False
            else:
                found_next_state = abstraction.find_state(system_feasible_disc_inv, predicate.State(666,transition['next_state'],*state.state))

                if found_next_state:
                    next_states.append(found_next_state.number)
                       
        if next_states:
            print "Discrete Abstract Transition: From State %s Next State %s" % (state.number, next_states)
            state.next_states.extend(next_states)
        #else:
            #print 'No Next state found, No switching'
                        
dis_abs_end = time.time()

f.write('Total Time for Discrete Abstraction: %s\n' % secondsToStr(dis_abs_end-dis_abs))
        
total_next_states = 0
#remove duplicate next states.
for s in system_feasible_disc_inv:
    s.next_states = list(set(s.next_states))
    total_next_states = total_next_states + len(s.next_states)

f.write('Total number of abstract transitions: %s\n' % total_next_states)
f.write('Total number of states in final abstract system: %s\n' % len(system_feasible_disc_inv))
    
#convert from list to dictionary
system_fdd = {}
        
for s in system_feasible_disc_inv:
	system_fdd[s.number] = s
   

#SMV = open('/Users/will/Research/quantum/'+exp_name+'.smv','w')
SMV = open(exp_name+'.smv','w')

smv_output = nusmv.construct_nusmv_input(system_fdd,2)

SMV.write(smv_output)
SMV.close()

end_time = time.time()

#print 40*'='
f.write('Total Time taken : %s\n' % secondsToStr(end_time-start_time))
#print 40*'='

#for s in system:
#	if s.is_feasible:
#		if 'X - 80>0' in [pred.equation_string for pred in s.state]:
#			s.discrete_part = 'off'

print ""

for key,s in system_fdd.iteritems():
    if s.is_feasible and s.next_states:
		print "From State {:>5} : {} - {} \tto States {}".format(s.number, s, s.discrete_part, s.next_states)


f.close()



    

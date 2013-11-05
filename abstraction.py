import predicate
from itertools import product
import qutilities
import metitarski
from termcolor import colored, cprint
import multiprocessing as mp
from multiprocessing.dummy import Pool
#from multiprocessing import Pool
import functools
import dill as pickle


def find_state(system, next_state):
    for state in system.values():
        if state == next_state and state.is_feasible:
            return state
    #else:
    #    return None

def update_next_states(pos_state, system, next_states, more_than_one=False):
    found_next_state = find_state(system, pos_state)

    if found_next_state:
        if more_than_one:
            if more_than_one_diff(pos_state, found_next_state):
                next_states.append(found_next_state.number)
        else:
            next_states.append(found_next_state.number)
                
def more_than_one_diff(s1, s2):
    id_dict = {p.var_id:0 for p in s1.state}
    
    comp_list = zip(s1.state,s2.state)

    for t in comp_list:
        if t[0]!=t[1] and t[0].var_id!=0:
            id_dict[t[0].var_id] += 1

    if [diffs for diffs in id_dict.values() if diffs>1]:
        return True
    else:
        return False

def get_true_guards(state, guards):
    true_guards = list()
    for guard_list in guards:
        for guard in guard_list:
            if guard in state.state:
                true_guards.append(guard)
    return true_guards
                
def gen_pos_pred(equation):
    
    lt_pred = predicate.MetitPredicate(equation,'<')
    gt_pred = predicate.MetitPredicate(equation,'>')
    eq_pred = predicate.MetitPredicate(equation,'=')

    return (lt_pred, eq_pred, gt_pred)

def print_reach(system, state, depth):

    #print state.number, state
    #print '****'
    
    if depth==1:
        print state.number, state
        print '****'
        #return
    else:
        for x in state.next_states:
            #print state.number, state
            print_reach(system, system[x], depth-1)

def conc_to_abs(system, discrete_part, predicates):
    return [state.number for state in system.values() if all([p in [str(pred) for pred in state.state] for p in predicates]) and discrete_part==state.discrete_part]

def initial_abstract_system_setup(exp):
    oplist = ['>','=','<']
    predicates = []
    
    ## For each continous equation, create a predicate
    for equation in exp.equations:
        predicates.append([predicate.MetitPredicate(equation.equation,op,equation.var_id,is_lyapunov=equation.is_lyapunov) for op in oplist])

    predicates.append(product(*exp.q))
    
    #for p in predicates:
    #    print list(p)

    ## Create an abstract state for each combination of the predicates
    #import pdb; pdb.set_trace()
    
    initial_abstract_system = [predicate.State(n,element[-1],*element[:-1]) for n, element in enumerate(product(*predicates)) if not any([invariant in exp.system_def[element[-1]]['inv'] for invariant in element[:-1]])]
                               
    #should create a state here everytime!!
    
    ## For each discrete variable, make a copy of the state
    #hybrid_system =  qutilities.make_discrete_system(initial_abstract_system,q, system_def)

    ## Delete any states that violate their respective invariant
    #for state_number, state in hybrid_system.items():
    #    if [pred for pred in system_def[state.discrete_part]['inv'] if pred in state.state]:
    #        state.is_feasible = False

    return {state.number:state for state in initial_abstract_system}
    #return initial_abstract_system

def print_system(system, feasible_only=True):
    for key, s in system.items():
        if s.is_feasible and s.feasability_checked and s.next_states and feasible_only:
            print("{} : From State {:>5} : {} - {} \tto States {}".format(s.is_feasible, s.number, s, s.discrete_part, s.next_states))
        elif feasible_only==False:
            print("{} : From State {:>5} : {} - {} \tto States {}".format(s.is_feasible, s.number, s, s.discrete_part, s.next_states))

def is_state_feasible(state, var_string, feas_check_proved_dir, feas_check_unproved_dir,exp, check=False):
    if check or not(state.feasability_checked):
        fof = metitarski.make_fof_inf(state, var_string)
        #print "Sending: " + fof
        rc = metitarski.send_to_metit(fof,metit_options=exp.metit_options)
        state.feasability_checked = True
        if rc == 0:
            metitarski.send_to_file(fof, feas_check_proved_dir, '%s.tptp' % state.number)
            state.is_feasible = False
            cprint('State %s is DEFINITELY not feasible. PROVED' % state.number, 'green')
            exp.infeas_proved += 1
            return False
        
        else:
            metitarski.send_to_file(fof, feas_check_unproved_dir, '%s.tptp' % state.number)    
            #feasible = feasible+1
            exp.infeas_unproved += 1
            cprint('State %s is POSSIBLY feasible. UNPROVED' % state.number, 'red')
            return True
        
    else:
        cprint('State %s Already Checked : It is %s' % (state.number, ('Possibly Feasible' if state.is_feasible else 'Not Feasible')), 'blue')
        return state.is_feasible

def gen_pos_successors(pred, state, system, system_def, var_string, experiment,bad=False,z=1):
    """Generates a list possible predicates in the next abstract continous state from the current predicate.

    pred -- current state predicate function
    state -- current state

    """
    pos_successors = []

    if bad:
        Q1,Q2,Q3 = ([],[],[])
    else:
        Q1,Q2,Q3 = metitarski.cont_abs_trans_rel(var_string, state, pred, z, experiment)
        
    lt_pred, eq_pred, gt_pred = gen_pos_pred(pred.equation)

    if pred.operator == '>':
        if state.number in Q1: 
            pos_successors.extend([gt_pred])
        else:
            pos_successors.extend([gt_pred,eq_pred])
    elif pred.operator == '<':
        if state.number in Q3:
            pos_successors.extend([lt_pred])
        else:
            pos_successors.extend([lt_pred,eq_pred])
    else:
        if state.number in Q1 and state.number in Q2:
            pos_successors.extend([gt_pred])
        elif state.number in Q3 and state.number in Q2:
            pos_successors.extend([lt_pred])
        elif state.number in Q1 and state.number in Q3:
            pos_successors.extend([eq_pred])
        else:
            pos_successors.extend([eq_pred,lt_pred,gt_pred])

    return pos_successors


def next_cont_states(state, system, system_def, var_string, experiment, bad=False, check=False):
    
    pool = Pool()
    #args = state, system,system_def,var_string, experiments
    #import pdb; pdb.set_trace()
    next_pos_states = pool.map(functools.partial(gen_pos_successors,system=system,state=state,system_def=system_def, var_string=var_string, experiment=experiment), state.state, chunksize=1)
    
    #import pdb; pdb.set_trace()
    #for z, pred in enumerate(state.state): #pos multiproc on this
        
    #for pos_successors in next_pos_states:
           
    next_states = []
        
    for possible_next_state in product(*next_pos_states):
        found_state = find_state(system, predicate.State(666, state.discrete_part, *possible_next_state))
        if found_state:        
            next_states.append(found_state)
        #find all next states, and parallel send to metiTarski
        #not more_than_one_diff(state, found_next_state)
    #import pdb; pdb.set_trace()
    feas_pos_states = pool.map(functools.partial(is_state_feasible,var_string=var_string, feas_check_proved_dir=experiment.feas_check_proved_dir, feas_check_unproved_dir=experiment.feas_check_unproved_dir,exp=experiment,check=check), next_states, chunksize=1)
    #if found_next_state and is_state_feasible(found_next_state, var_string, experiment.feas_check_proved_dir, experiment.feas_check_unproved_dir,experiment,check) and not more_than_one_diff(state, found_next_state) :
   #             next_states.append(found_next_state.number)
        #else:
            #print 'Multiple variable jumps'
    
    feas_next_states = []

    for state2, is_feas in zip(next_states,feas_pos_states):
        if is_feas and not more_than_one_diff(state,state2):
            feas_next_states.append(state2.number)
    
    #import pdb; pdb.set_trace()

    if feas_next_states:
        feas_next_states = list(set(feas_next_states))
        print "Continuous Abstract Transition: From State %s Next State %s" % (state.number, feas_next_states)
        state.next_states = feas_next_states
        

    return feas_next_states
    #else:
        #print 'no next state found, but might come during discrete abstraction. State %s' % (state.number)
        #only delete the state at the end
        #state.is_feasible = False

def next_disc_states(state, system, system_def, var_string, exp, bad=False, check=False):
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
                        Q1,Q2,Q3 = metitarski.checkTransition3(var_string, state, pred2, z, system_def, transition['updates'], exp)

                    lt_pred, eq_pred, gt_pred = gen_pos_pred(pred2.equation)

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
                    found_next_state = find_state(system, predicate.State(666, transition['next_state'], *possible_next_state))

                    #print abstraction.get_true_guards(state, transition['guard'])
                    #print [s for s in found_next_state.state if s in abstraction.get_true_guards(state, transition['guard'])]
                    
                    if found_next_state and is_state_feasible(found_next_state, var_string, exp.feas_check_proved_dir, exp.feas_check_unproved_dir, exp, check) :
                        next_states.append(found_next_state.number)
           
                if next_states: 
                    print "Updating State %s has produced Next States %s" % (state.number,next_states)
                            #is this ok, check alogorithm
                    state.next_states.extend(next_states)
                else:
                    print 'Substitution sends us to an infeasible state...possible error here.'
                    #state.is_feasible = False
            else:
                found_next_state = find_state(system, predicate.State(666,transition['next_state'],*state.state))

                if found_next_state and is_state_feasible(found_next_state, var_string, exp.feas_check_proved_dir, exp.feas_check_unproved_dir, exp, check):
                    next_states.append(found_next_state.number)
                       
        if next_states:
            print "Discrete Abstract Transition: From State %s Next State %s" % (state.number, next_states)
            state.next_states.extend(next_states)
            state.next_states = list(set(state.next_states))
        #else:
            #print 'No Next state found, No switching'

    return next_states
            
def lazy_cont_abs(system, initial_states, system_def, var_string, exp, bad_predicate=''):
    new_next_states = set(initial_states)
    old_next_states = set()

    print 'Initial states are %s' % new_next_states
    
    while new_next_states != old_next_states:
        old_next_states = set(new_next_states)
        for state_num in old_next_states:
            if not system[state_num].next_states:
                print 'Analyzing state %s' % state_num
                new_cont_states = [x for x in next_cont_states(system[state_num], system, system_def, var_string, exp)]
                new_disc_states  = [x for x in next_disc_states(system[state_num], system, system_def, var_string, exp)]
                
                done = False
                iter_num = 0
                orig_timeout = exp.metit_timeout
                orig_opt = exp.metit_options
                current_states = new_cont_states+new_disc_states
                
                while not done:
                    for to_state_num in current_states:
                        if bad_predicate and bad_predicate in system[to_state_num].state:
                            import pdb; pdb.set_trace()
                            current_states_copy = list(current_states)
                            print 'found bad transition from state %s to state %s' % (state_num, to_state_num)  
                            #double check here!
                            iter_num += 1
                            old_timeout = exp.metit_timeout
                            new_timeout = old_timeout*2
                            
                            exp.metit_options =  ['metit', 
                                                  '--autoInclude', 
                                                  '--time',str(new_timeout)]
                                                

                            print 'new timeout: %s' % new_timeout
                            exp.metit_timeout = new_timeout
    
                            new_cont_states = [x for x in next_cont_states(system[state_num], system, system_def, var_string, exp, check=True)]
                            new_disc_states  = [x for x in next_disc_states(system[state_num], system, system_def, var_string, exp, check=True)]
                            new_current_states = new_cont_states+new_disc_states
                            
                            import pdb; pdb.set_trace()

                            if len(new_current_states) == len(current_states_copy): 
                                if iter_num > 4:
                                    print 'Too many retries'
                                    return False
                                else:
                                    print 'Iteration %s' % iter_num
                                    break
                            elif len(new_current_states) < len(current_states_copy):
                                print 'progress!'
                                break
                    else:
                        done = True
                
                exp.metit_timeout = orig_timeout
                exp.metit_options = orig_opt
                iter_num = 0
                new_next_states.update(new_cont_states+new_disc_states)
                #exp.trans_proved += len(new_cont_states) +len(new_disc_states)
                #new_next_states.anew_disc_states)
            else:
                cprint('Next states of state %s already computed' % state_num, 'yellow')
                    
        #new_next_states = set(new_next_states)
        print 'iterating again'
        print 'number of new states %s' % (len(new_next_states)-len(old_next_states))
        print 'new_next_states %s' % new_next_states

    return True

def ex_state(system, state_num):
    print '%s : %s' % (state_num, system[state_num])
    print '-'*10
    for s in system[state_num].next_states:
        print '%s : %s' % (system[s].number, system[s])

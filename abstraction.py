import predicate
from itertools import product
import qutilities
import metitarski
from termcolor import colored, cprint

def find_state(system, next_state):
    for state in system.values():
        if state == next_state and state.is_feasible:
            return state

def update_next_states(pos_state, system, next_states, more_than_one=False):
    found_next_state = find_state(system, pos_state)

    if found_next_state:
        if more_than_one:
            if more_than_one_diff(pos_state, found_next_state):
                next_states.append(found_next_state.number)
        else:
            next_states.append(found_next_state.number)
                
def more_than_one_diff(s1, s2):

    num_same = 0
    
    for pred1 in s1.state:
        for pred2 in s2.state:
            if pred1 == pred2:
                #print 'found matching predicate'
                num_same += 1

    if num_same < len(s1.state)-1:
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

def conc_to_abs(system, discrete_part, *predicates):
    return [state.number for state in system.values() if all([p in [str(pred) for pred in state.state] for p in predicates]) and discrete_part==state.discrete_part]

def initial_abstract_system_setup(equations, q, system_def):
    oplist = ['>','=','<']
    predicates = []

    ## For each continous equation, create a predicate
    for equation in equations:
        predicates.append([predicate.MetitPredicate(equation.equation,op) for op in oplist])
    
    ## Create an abstract state for each combination of the predicates
    initial_abstract_system = {n:predicate.State(n,'None',*element) for n, element in enumerate(product(*predicates))}
    
    ## For each discrete variable, make a copy of the state
    hybrid_system =  qutilities.make_discrete_system(initial_abstract_system,q)

    ## Delete any states that violate their respective invariant
    for state_number, state in hybrid_system.items():
        if [pred for pred in system_def[state.discrete_part]['inv'] if pred in state.state]:
            state.is_feasible = False

    return {state.number:state for state in hybrid_system.values() if state.is_feasible}

def print_system(system, feasible_only=True):
    for key, s in system.items():
        if s.is_feasible and s.feasability_checked and feasible_only:
            print("{} : From State {:>5} : {} - {} \tto States {}".format(s.is_feasible, s.number, s, s.discrete_part, s.next_states))
        elif feasible_only==False:
            print("{} : From State {:>5} : {} - {} \tto States {}".format(s.is_feasible, s.number, s, s.discrete_part, s.next_states))

def is_state_feasible(state, var_string):
    if not(state.feasability_checked):
        fof = metitarski.make_fof_inf(state, var_string)
        #print "Sending: " + fof
        rc = metitarski.send_to_metit(fof)
        state.feasability_checked = True
        if rc == 0:
            state.is_feasible = False
            cprint('State %s is DEFINITELY not feasible. PROVED' % state.number, 'green')
            return False
        #metitarski.send_to_file(fof, feas_check_proved_dir, '%s.tptp' % state.number)
        else:
            #feasible = feasible+1
            cprint('State %s is POSSIBLY feasible. UNPROVED' % state.number, 'red')
            return True
        #metitarski.send_to_file(fof, feas_check_unproved_dir, '%s.tptp' % state.number)

        
    else:
        return state.is_feasible

def next_cont_states(state, system, system_def, var_string, cont_trans_unproved_dir, bad=False):
    pos_successors = []
    for z, pred in enumerate(state.state):
        if bad:
            Q1,Q2,Q3 = ([],[],[])
        else:
            Q1,Q2,Q3 = metitarski.checkTransition2(var_string, state,pred,z, system_def, cont_trans_unproved_dir)
        
        lt_pred, eq_pred, gt_pred = gen_pos_pred(pred.equation)

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
        found_next_state = find_state(system, predicate.State(666, state.discrete_part, *possible_next_state))

        #not more_than_one_diff(state, found_next_state)
        
        if found_next_state and is_state_feasible(found_next_state, var_string):
            next_states.append(found_next_state.number)
        #else:
            #print 'Multiple variable jumps'
                
    if next_states: 
        print "Continuous Abstract Transition: From State %s Next State %s" % (state.number, next_states)
        state.next_states = next_states
        list(set(state.next_states))

    return next_states
    #else:
        #print 'no next state found, but might come during discrete abstraction. State %s' % (state.number)
        #only delete the state at the end
        #state.is_feasible = False

def next_disc_states(state, system, system_def, var_string, disc_trans_unproved_dir, bad=False):
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
                found_next_state = find_state(system, predicate.State(666,transition['next_state'],*state.state))

                if found_next_state:
                    next_states.append(found_next_state.number)
                       
        if next_states:
            print "Discrete Abstract Transition: From State %s Next State %s" % (state.number, next_states)
            state.next_states.extend(next_states)
            state.next_states = list(set(state.next_states))
        #else:
            #print 'No Next state found, No switching'

    return next_states
            
def lazy_cont_abs(system, initial_states, system_def, var_string, cont_trans_unproved_dir, disc_trans_unproved_dir):
    new_next_states = list(initial_states)
    old_next_states = []

    print 'trying states %s' % new_next_states
    
    while new_next_states != old_next_states:
        old_next_states = list(new_next_states)
        for state_num in old_next_states:
            if not system[state_num].next_states:
                new_next_states.extend([x for x in next_cont_states(system[state_num], system, system_def, var_string, cont_trans_unproved_dir)])
                new_next_states.extend([x for x in next_disc_states(system[state_num], system, system_def, var_string, disc_trans_unproved_dir)])
                
        new_next_states = list(set(new_next_states))
        print 'iterating again'
        print 'new_next_states %s' % new_next_states
    

        

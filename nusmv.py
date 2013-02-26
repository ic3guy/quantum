import predicate

def remove_inf_states(system):

    while True:
        system_copy = system.copy()
        for state_number, state in system.iteritems():
            if state.next_states:
                if all([not(system[s].is_feasible) for s in state.next_states]) and state.is_feasible:
                    state.is_feasible=False
                    print "found infeasible state with no feasible next states"
                
        if system_copy==system:
            return

def transition_relation(cur_state,next_states,system):  
    if next_states:
        if len(next_states) == 1:
            next_states_str = str(next_states[0])
        else:
            next_states_str = ','.join(map(str,next_states))
            next_states_str = '{' + next_states_str + '}'
        
        return '\t\tstate = %s: %s;\n' % (cur_state, next_states_str)
    else:
        #system[cur_state].is_feasible = False
        return '\n'
    
def construct_nusmv_input(system, init_state):
    remove_inf_states(system)
    case_block = construct_transition_case_block(system)
    states = ','.join([s.print_state_number() for key, s in system.iteritems() if s.is_feasible and s.feasability_checked]) 

    nusmv_output = 'MODULE main\nVAR\n\t'
    nusmv_output += 'state : {%s};\nASSIGN\n\t' % states
    nusmv_output += 'init(state) := %s;\n' % str(init_state)
    nusmv_output += case_block

    return nusmv_output

def construct_transition_case_block(system):
    case_block = '\tnext(state) := case\n'
    
    for state_num, state in system.iteritems():
        #filter out next states that have been shown to have no next state (deleted)
        next_states = [n for n in state.next_states if system[n].is_feasible]
        
        if state.is_feasible and next_states:
            case_block += transition_relation(state.print_state_number(), next_states, system)
    
    case_block += '\tesac;\n'
    
    return case_block

if __name__ == '__main__':

    e1 = predicate.MetitEquation('x(t)','t',{},{})
    e2 = predicate.MetitEquation('x(t)','t',{},{})
    
    p1 = predicate.MetitPredicate(e1,'<')
    p2 = predicate.MetitPredicate(e2,'>')
    p3 = predicate.MetitPredicate(e2, '>')
    s1 = predicate.State('X,Y',1,[1,2,3],p1,p2,p3)
    s2 = predicate.State('X,Y',2,[4],p1,p2,p3) 
    
    system = [s1,s2]

    construct_nusmv_input(system,3)

def concrete_initial_to_abstract(system, *predicates):
    initial_states = []
    
    initial_states = [state.number for state in system if all(p in [str(pred) for pred in state.state] for p in predicates) and state.is_feasible]

    return initial_states

def construct_safety_ltl_property(bad_states):
    ltl_property = "LTLSPEC G !("

    for state in bad_states:
        ltl_property += "state = %s|" % state
    
    ltl_property += ")"

    return ltl_property

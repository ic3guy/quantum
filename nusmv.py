import predicate

def transition_relation(cur_state,next_states, system):  
    if next_states:
        if len(next_states) == 1:
            next_states_str = str(next_states[0])
        else:
            next_states_str = ','.join(map(str,next_states))
            next_states_str = '{' + next_states_str + '}'
    else:
        system[cur_state].is_feasible = False
    
        return '\t\tstate = %s: %s;\n' % (cur_state, next_states_str)
    
def construct_nusmv_input(system, init_state):
    case_block = construct_transition_case_block(system)
    states = ','.join([s.get_state_number() for s in system if s.is_feasible])

    nusmv_output = 'MODULE main\nVAR\n\t'
    nusmv_output += 'state : {%s};\nASSIGN\n\t' % states
    nusmv_output += 'init(state) := %s;\n' % str(init_state)
    nusmv_output += case_block

    print nusmv_output

def construct_transition_case_block(system):
    case_block = '\tnext(state) := case\n'
    
    for tr in system:
        #filter out next states that have been shown to have no next state (deleted)
        next_states = [n for n in tr.next_states if system[n].is_feasible]
        
        if tr.is_feasible and next_states:
            case_block += transition_relation(tr.get_state_number(),next_states,system)
    
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






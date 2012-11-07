import predicate

def transition_relation(cur_state,next_states, system):
    
    #filter out next states that have been shown to have no next state (deleted)
    next_states = [n for n in next_states if system[n].is_feasible] 
    
    if len(next_states) == 1:
        next_states_str = str(next_states[0])
    else:
        next_states_str = ','.join(map(str,next_states))
        next_states_str = '{' + next_states_str + '}'
    
    return '\t\tstate = %s: %s;\n' % (cur_state, next_states_str)
    
def construct_nusmv_input(system, init_state):
    transition = 'MODULE main\nVAR\n\t'

    states = ','.join([s.get_state_number() for s in system if s.is_feasible])
    
    transition = transition + 'state : {%s};\nASSIGN\n\t' % states

    transition = transition + 'init(state) := %s;\n' % str(init_state)
    transition = transition + '\tnext(state) := case\n'

    for tr in system:
        if tr.is_feasible:
            transition = transition + transition_relation(tr.get_state_number(),tr.next_states,system)
    
    transition = transition + ('\tesac;\n')

    print transition
    
    
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






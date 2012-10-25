import predicate

def state_to_transition(cur_state, next_states):
    transition = 'next(state) := case\n'

    if len(next_states) == 1:
        next_states_str = next_states[0]
    else:
        next_states_str = ','.join(next_states)
        next_states_str = '{' + next_states_str + '}'
    
    transition = transition + ('state = %s: %s;\n' % (cur_state, next_states_str))

    transition = transition + ('esac;\n')

    print transition
    
    
if __name__ == '__main__':

    e1 = predicate.MetitEquation('x(t)','t',{},{})
    e2 = predicate.MetitEquation('x(t)','t',{},{})
    
    p1 = predicate.MetitPredicate(e1,'<')
    p2 = predicate.MetitPredicate(e2,'>')
    p3 = predicate.MetitPredicate(e2, '>')
    s1 = predicate.State('X,Y',p1,p2,p3)
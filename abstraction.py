import predicate

def find_state(system, next_state):
    for state in system:
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

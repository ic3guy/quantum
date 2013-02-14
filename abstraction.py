def find_state(system, next_state):
    for state in system:
        if state == next_state and state.is_feasible:
            return state

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

import pickle
from sympy import *
from sympy.plotting.plot import Plot
import predicate
import itertools
import pydot

#import experiment
#import cfg

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

def save_system(system, filename):
    
    system_to_save = list(system)

    #sympy functions cannot be pickled, therefore we remove them
    #this shouldn't be an issue
    for state in system_to_save:
        for p in state.state:
            p.equation = ''
    
    #writing and binary mode (wb)
    pickle.dump(system_to_save, open(filename, 'wb'))

def load_system(filename):
    return pickle.load(open(filename, 'rb'))

def plot_state(state):

    X1 = Symbol('X1')
    X2 = Symbol('X2')

    #p = Plot()

    v = sympify('And(' + ','.join([s.plot_format_str for s in state.state]) + ')')
   
    plot_implicit(v,(X1,-pi,pi),(X2,-20,20),title='State %s' % state.number,linewidth=2,axis=False)

def copy_state(state, discrete_part, number, system_def):
    if any([invariant in system_def[discrete_part]['inv'] for invariant in state.state]):
        return 'invariant violated'
    else:
        return predicate.State(number, discrete_part, *state.state)

def make_discrete_system(system, discrete_variables_q, system_def):
    #add in the guards to the state, maybe make a guards variable
    system_fd = {}
    
    for state in system:    
        for n, discrete_state in enumerate(itertools.product(*discrete_variables_q)):
            system_fd[str(state.number+n*1000)]=copy_state(state,discrete_part=discrete_state,number=state.number+n*1000,system_def=system_def)

    return system_fd

nodes = {}
    
def output_graphiz(system):

    nodes = {}
    graph = pydot.Dot(graph_type='digraph')

    for state_number, state in system.iteritems():
        if state.is_feasible and state.feasability_checked: #and state.next_states:
            nodes[state_number] = pydot.Node(state_number,label=state.pretty_print() + '\n' + str(state.discrete_part),style='filled',fillcolor=state.colour)
            
    #print nodes

    for n, node in nodes.iteritems():
        graph.add_node(node)

    for state_number, state in system.iteritems():
        print state_number, set(state.next_states), state.colour
        for ns in set(state.next_states):
            try:
                if system[ns].is_feasible:
                    graph.add_edge(pydot.Edge(nodes[state_number],nodes[ns]))
            except KeyError:
                next

    graph.write_png('test.png')
            

import pickle
from sympy import *
from sympy.plotting.plot import Plot
import predicate
import itertools

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

def copy_state(state,discrete_part,number):
   return predicate.State('X',number,discrete_part,*state.state)

def make_discrete_system(system, discrete_variables_q):
    #add in the guards to the state, maybe make a guards variable
    system_fd = []
    
    for state in system:    
        for n,discrete_state in enumerate(itertools.product(discrete_variables_q)):
            system_fd.append(copy_state(state,discrete_part=discrete_state,number=state.number+n*1000))

    return system_fd
           
    

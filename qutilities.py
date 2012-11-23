import pickle
from sympy import *
from sympy.plotting.plot import Plot

def save_system(system, filename):
    
    system_to_save = list(system)


    #sympy functions cannot be pickled, therefore we remove them
    #this shouldn't be an issue
    for state in system_to_save:
        for predicate in state.state:
            predicate.equation = ''
    
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
    
    

from sympy import *
import metitarski
from itertools import product
import predicate
import abstraction
import datetime
import os
import nusmv
import timing
import time
from termcolor import colored, cprint
import qutilities

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

# Create directories to store proved and unproved tptp files for later analysis
now = datetime.datetime.now()
experiment_dir = 'experiments/'+ file_name + now.strftime('--%d-%m-%Y--%H:%M:%S')
# Try to enforce the current directory. Check to see how Emacs does this in OSX.

feas_check_dir = experiment_dir + '/feasability/'
feas_check_proved_dir = feas_check_dir + '/proved/'
feas_check_unproved_dir = feas_check_dir + '/unproved/'

trans_check_dir = experiment_dir + '/transitions/'
cont_trans_proved_dir = trans_check_dir + 'continuous/proved'
cont_trans_unproved_dir = trans_check_dir + 'continuous/unproved'

disc_trans_proved_dir = trans_check_dir + 'discrete/proved'
disc_trans_unproved_dir = trans_check_dir + 'discrete/unproved'

os.makedirs(feas_check_proved_dir)
os.makedirs(feas_check_unproved_dir)

os.makedirs(cont_trans_proved_dir)
os.makedirs(cont_trans_unproved_dir)

os.makedirs(disc_trans_proved_dir)
os.makedirs(disc_trans_unproved_dir)

execfile(exp_name)

start_time = time.time()    
f = open('log.txt', 'a', 0)
f.write(40*'*'+'\n')
f.write(exp_name + '\n')
f.write(40*'*' + '\n')

hybrid_system = abstraction.initial_abstract_system_setup(equations, q, system_def)
var_string = predicate.get_var_string(equations)

initial_state_numbers = abstraction.conc_to_abs(hybrid_system,('falling',),'VY=0','PY<0','G<0','-G - PY + sin(PX)=0')

next_states = [state_num for state_num in initial_state_numbers if abstraction.is_state_feasible(hybrid_system[state_num], var_string)]
    
## LAZY QUAL ABS ##

abstraction.lazy_cont_abs(hybrid_system, next_states, system_def, var_string, cont_trans_unproved_dir,disc_trans_unproved_dir)

SMV = open(exp_name+'.smv','w')

smv_output = nusmv.construct_nusmv_input(hybrid_system,2)

SMV.write(smv_output)
SMV.close()

end_time = time.time()

f.write('Total Time taken : %s\n' % secondsToStr(end_time-start_time))
f.close()

abstraction.print_system(hybrid_system)

    

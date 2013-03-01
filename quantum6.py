from sympy import *
import metitarski
from itertools import product
import predicate
import abstraction
import datetime
import os
import nusmv
#import timing
import time
from termcolor import colored, cprint
import qutilities
import experiment

filenames = ['bounceBallsin-new5c']
#filenames = ['heater-new']

for file_name in filenames:             
    cur_exp = experiment.Experiment(file_name)        
    #execfile('quantum6.py',globals())

    print cur_exp.system_def

    experiment.create_exp_dirs(cur_exp)

    feas_check_proved_dir = cur_exp.feas_check_proved_dir
    feas_check_unproved_dir = cur_exp.feas_check_unproved_dir
    cont_trans_proved_dir =  cur_exp.cont_trans_proved_dir
    cont_trans_unproved_dir = cur_exp.cont_trans_unproved_dir
    disc_trans_proved_dir = cur_exp.disc_trans_proved_dir
    disc_trans_unproved_dir = cur_exp.disc_trans_unproved_dir
        
    start_time = time.time()    
    f = open('log.txt', 'a', 0)
    f.write(40*'*'+'\n')
    f.write(cur_exp.filename + '\n')
    f.write(40*'*' + '\n')

    print 'starting quantum6'

    hybrid_system = abstraction.initial_abstract_system_setup(cur_exp.equations, cur_exp.q, cur_exp.system_def)
    var_string = predicate.get_var_string(cur_exp.equations)

    #initial_state_numbers = abstraction.conc_to_abs(hybrid_system,('falling',),'VY=0','PY<0','G<0','-G - PY + sin(PX)=0','PX<0','VX=0')

    #initial_state_numbers = abstraction.conc_to_abs(hybrid_system,('falling',),'-H + PY<0','VY=0','VX=0')

    initial_state_numbers = abstraction.conc_to_abs(hybrid_system,cur_exp.initial_state['d'],cur_exp.initial_state['c'])

    next_states = [state_num for state_num in initial_state_numbers if abstraction.is_state_feasible(hybrid_system[state_num], var_string,feas_check_proved_dir, feas_check_unproved_dir)]
    
## LAZY QUAL ABS ##

    #bad = predicate.MetitPredicate(py-h,'>')
    #bad2 = predicate.MetitPredicate(0.5*vx**2+0.5*vy**2+2*9.8*py-2*9.8*sin(px)-9.8,'>')

    abstraction.lazy_cont_abs(hybrid_system, next_states, cur_exp.system_def, var_string, cont_trans_unproved_dir,disc_trans_unproved_dir,feas_check_proved_dir, feas_check_unproved_dir,bad_predicate=cur_exp.bad_state)

    SMV = open(cur_exp.filename + '.smv','w')

    smv_output = nusmv.construct_nusmv_input(hybrid_system,2)

    SMV.write(smv_output)
    SMV.close()

    end_time = time.time()

    f.write('Total Time taken : %s\n' % qutilities.secondsToStr(end_time-start_time))
    f.close()

    abstraction.print_system(hybrid_system)

    

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
import sys

sys.path.insert(0,'./examples/')

#cur_exp = None
#filenames = ['twotanks']
#filenames = ['heater-new-timed']
#filenames = ['bounceBallsin-new5c']
#filenames = ['simplePendulum3-new','simplePendulum4-new']
#filenames = ['simplePendulum-new','simplePendulum2-new',]
#filenames = ['simplePendulum4-new']
#filenames = ['simplePendulum-new','simplePendulum2-new','simplePendulum3-new','simplePendulum4-new']

hybrid_system = None
cur_exp = None

def run(filenames, to=100):
    for file_name in filenames:

        for metit_timeout in [to]:
            global cur_exp
            cur_exp = experiment.Experiment(file_name,metit_timeout)        
            #execfile('quantum6.py',globals())

            print cur_exp.system_def
        
            cur_exp.metit_options = ['metit', 
                 '--autoInclude', 
                 '--time',str(metit_timeout)]
        
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
            f.write(cur_exp.filename + '-' + str(metit_timeout) + '-' + '\n')
            f.write(40*'*' + '\n')

            print 'starting quantum6'
            
            global hybrid_system
            hybrid_system = abstraction.initial_abstract_system_setup(cur_exp.equations, cur_exp.q, cur_exp.system_def)
            var_string = predicate.get_var_string(cur_exp.equations)

            #initial_state_numbers = abstraction.conc_to_abs(hybrid_system,('falling',),'VY=0','PY<0','G<0','-G - PY + sin(PX)=0','PX<0','VX=0')

            #initial_state_numbers = abstraction.conc_to_abs(hybrid_system,('falling',),'-H + PY<0','VY=0','VX=0')

            initial_state_numbers = abstraction.conc_to_abs(hybrid_system,cur_exp.initial_state['d'],cur_exp.initial_state['c'])

            f.write('Number of Abstraction Functions : %s\n' % len(cur_exp.equations))
            f.write('Number of Initial Abstract States : %s\n' % len(hybrid_system))
    
            next_states = [state_num for state_num in initial_state_numbers if abstraction.is_state_feasible(hybrid_system[state_num], var_string,feas_check_proved_dir, feas_check_unproved_dir,cur_exp)]
        
            ## LAZY QUAL ABS ##

            #bad = predicate.MetitPredicate(py-h,'>')
            #bad2 = predicate.MetitPredicate(0.5*vx**2+0.5*vy**2+2*9.8*py-2*9.8*sin(px)-9.8,'>')
    
            if not(abstraction.lazy_cont_abs(hybrid_system, next_states, cur_exp.system_def, var_string, cur_exp, bad_predicate=cur_exp.bad_state)):
                f.write('**PROP VIOLATED**')
            else:
                SMV = open(cur_exp.filename + '-' + str(metit_timeout) + '.smv','w')
            
                smv_output = nusmv.construct_nusmv_input(hybrid_system,2)
            
                SMV.write(smv_output)
                SMV.close()
            
                end_time = time.time()

    
                f.write('Number of Final Abstract States : %s\n' % len([x for x in hybrid_system.itervalues() if x.is_feasible and x.feasability_checked and x.next_states]))
                f.write('Number of UnProved InFeasible : %s\n' % cur_exp.infeas_unproved)
                f.write('Number of Proved Infeasible : %s\n' % cur_exp.infeas_proved)
                f.write('Number of Proved Transitions : %s\n' % cur_exp.trans_proved)
                f.write('Number of UnProved Transitions : %s\n' % cur_exp.trans_unproved)        
                f.write('Total Time taken : %s\n' % qutilities.secondsToStr(end_time-start_time))
                f.close()
            
                abstraction.print_system(hybrid_system)

    




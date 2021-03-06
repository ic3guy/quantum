#from sympy import *
#import metitarski
#from itertools import product
import predicate
import abstraction
#import datetime
#import os
import nusmv
#import timing
import time
#from termcolor import colored, cprint
import qutilities
import experiment
import sys
from multiprocessing.dummy import Pool
import functools

sys.path.insert(0, './examples/')

exps = ['pend-fric-th-timeout-base-1',
        'pend-fric-th-timeout-base-2',
        'pend-fric-th-timeout-base1-1',
        'pend-fric-th-timeout-base1-2',
        'pend-fric-th-timeout-base2-1',
        'pend-fric-th-timeout-base2-2',
        'pend-fric-th-timeout-base3-1'] 

exps = ['pend-fric-th-timeout-base4-1',
        'pend-fric-th-timeout-base4-2',
        'pend-fric-th-timeout-base3-2']

# 'pend-fric-th-timeout-base3-2'

# exps = ['pfth-base-b',
#         'pfth-base-b1',
#         'pfth-base-b2',
#         'pfth-base-b3',
#         'pfth-base-b4']

hybrid_system = None
cur_exp = None

def run(filenames, to=[0.1]):
    for file_name in filenames:

        for metit_timeout in to:
            global cur_exp
            cur_exp = experiment.Experiment(file_name, metit_timeout)

            print cur_exp.system_def
        
            #cur_exp.metit_options = ['metit', 
            #     '--autoInclude', 
            #     '--time',str(metit_timeout)]
        
            cur_exp.create_dirs()

            start_time = time.time()
            f = open('log.txt', 'a', 0)
            f.write(40*'*'+'\n')
            f.write(cur_exp.filename + '-' + str(metit_timeout) + '-' + '\n')
            f.write(40*'*' + '\n')

            print 'starting quantum6'
            
            #global hybrid_system
            cur_exp.hybrid_system = abstraction.initial_abstract_system_setup(cur_exp)
            cur_exp.var_string = predicate.get_var_string(cur_exp)

            #initial_state_numbers = abstraction.conc_to_abs(hybrid_system,('falling',),'VY=0','PY<0','G<0','-G - PY + sin(PX)=0','PX<0','VX=0')

            #initial_state_numbers = abstraction.conc_to_abs(hybrid_system,('falling',),'-H + PY<0','VY=0','VX=0')

            cur_exp.initial_state_numbers = abstraction.conc_to_abs(cur_exp)

            f.write('Number of Abstraction Functions : %s\n' % len(cur_exp.equations))
            f.write('Number of Initial Abstract States : %s\n' % len(cur_exp.hybrid_system))
            
            #next_states = [state_num for state_num in initial_state_numbers if abstraction.is_state_feasible(hybrid_system[state_num], var_string,feas_check_proved_dir, feas_check_unproved_dir,cur_exp)]
            
            
            next_states=[]
            pool2 = Pool()
            
            next_states_res = pool2.map(functools.partial(abstraction.is_state_feasible,exp=cur_exp), [cur_exp.hybrid_system[state_num] for state_num in cur_exp.initial_state_numbers], chunksize=1)
            
            for sn, res in zip(cur_exp.initial_state_numbers, next_states_res):
                if res:
                    next_states.append(sn)
            ## LAZY QUAL ABS ##
            
            #bad = predicate.MetitPredicate(py-h,'>')
            #bad2 = predicate.MetitPredicate(0.5*vx**2+0.5*vy**2+2*9.8*py-2*9.8*sin(px)-9.8,'>')
            pool2.close()

            if not(abstraction.lazy_cont_abs(cur_exp,initial_states=next_states)):
                end_time = time.time()
                f.write('Total Time taken : %s\n' % qutilities.secondsToStr(end_time-start_time))
                f.write('Number of Final Abstract States : %s\n' % len([x for x in cur_exp.hybrid_system.itervalues() if x.is_feasible and x.feasability_checked and x.next_states]))
                f.write('Number of UnProved InFeasible : %s\n' % cur_exp.infeas_unproved)
                f.write('Number of Proved Infeasible : %s\n' % cur_exp.infeas_proved)
                f.write('Number of Proved Transitions : %s\n' % cur_exp.trans_proved)
                f.write('Number of UnProved Transitions : %s\n' % cur_exp.trans_unproved)
                f.write('**PROP VIOLATED**')
            else:
                SMV = open('./smv/'+cur_exp.filename + '-' + str(metit_timeout) + '.smv','w')
            
                smv_output = nusmv.construct_nusmv_input(cur_exp.hybrid_system,2)
            
                SMV.write(smv_output)
                SMV.close()
            
                end_time = time.time()

    
                f.write('Number of Final Abstract States : %s\n' % len([x for x in cur_exp.hybrid_system.itervalues() if x.is_feasible and x.feasability_checked and x.next_states]))
                f.write('Number of UnProved InFeasible : %s\n' % cur_exp.infeas_unproved)
                f.write('Number of Proved Infeasible : %s\n' % cur_exp.infeas_proved)
                f.write('Number of Proved Transitions : %s\n' % cur_exp.trans_proved)
                f.write('Number of UnProved Transitions : %s\n' % cur_exp.trans_unproved)
                f.write('Total Time taken : %s\n' % qutilities.secondsToStr(end_time-start_time))
                f.close()

                f = open('abs.txt', 'a', 0)
                f.write('\n'+40*'*'+'\n')
                f.write(cur_exp.filename + '-' + str(metit_timeout) + '-' + '\n')
                f.write(40*'*' + '\n')
                f.write(abstraction.print_system(cur_exp.hybrid_system))
                f.close()
    














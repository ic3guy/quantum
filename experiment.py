import os
import datetime

class Experiment:
    def __init__(self, name):
        self.filename = name + '.py'
        experiment = __import__(name)
        self.system_def = experiment.system_def
        self.q = experiment.q
        self.equations = experiment.equations
        self.initial_state = experiment.initial_state

        now = datetime.datetime.now()
        experiment_dir = 'experiments/'+ self.filename + now.strftime('--%d-%m-%Y--%H:%M:%S')
        feas_check_dir = experiment_dir + '/feasability/'
        trans_check_dir = experiment_dir + '/transitions/'
        
        self.feas_check_proved_dir = feas_check_dir + '/proved/'
        self.feas_check_unproved_dir = feas_check_dir + '/unproved/'
        self.cont_trans_proved_dir = trans_check_dir + 'continuous/proved'
        self.cont_trans_unproved_dir = trans_check_dir + 'continuous/unproved'
        self.disc_trans_proved_dir = trans_check_dir + 'discrete/proved'
        self.disc_trans_unproved_dir = trans_check_dir + 'discrete/unproved'

        self.bad_state = experiment.bad_state
        
def create_exp_dirs(exp):
    os.makedirs(exp.feas_check_proved_dir)
    os.makedirs(exp.feas_check_unproved_dir)

    os.makedirs(exp.cont_trans_proved_dir)
    os.makedirs(exp.cont_trans_unproved_dir)

    os.makedirs(exp.disc_trans_proved_dir)
    os.makedirs(exp.disc_trans_unproved_dir)

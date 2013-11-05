import os
import datetime

class Experiment:
    """A class to hold all data from a run."""

    def __init__(self, name, metit_timeout=1000):
        """

        name -- filename (sans extension) in examples/ subdir
        metit_timeout -- default metit_timeout (in milliseconds)
        
        """
        
        self.filename = name + '.py'
        experiment = __import__(name) #run-time loading of experiment

        self.metit_timeout = metit_timeout
        self.metit_options = ['metit', '--autoInclude', '--time', str(metit_timeout)]
        
        self.system_def = experiment.system_def
        self.q = experiment.q
        self.equations = experiment.equations # a list of predicate.MetitEquations
        self.initial_state = experiment.initial_state # dictionary 
        self.bad_state = experiment.bad_state # a predicate.MetitPredicate
        
        self.now = datetime.datetime.now()
        
        #setup folders for the experimental results

        self.experiment_dir = 'experiments/'+ name + '-' + str(metit_timeout) + '-' + self.now.strftime('--%d-%m-%Y--%H:%M:%S')
        self.feas_check_dir = self.experiment_dir + '/feasability/'
        self.trans_check_dir = self.experiment_dir + '/transitions/'
        
        self.feas_check_proved_dir = self.feas_check_dir + '/proved/'
        self.feas_check_unproved_dir = self.feas_check_dir + '/unproved/'
        self.cont_trans_proved_dir = self.trans_check_dir + 'continuous/proved'
        self.cont_trans_unproved_dir = self.trans_check_dir + 'continuous/unproved'
        self.disc_trans_proved_dir = self.trans_check_dir + 'discrete/proved'
        self.disc_trans_unproved_dir = self.trans_check_dir + 'discrete/unproved'
        
        self.trans_proved = 0
        self.trans_unproved = 0
        self.infeas_proved = 0
        self.infeas_unproved = 0        
    
    def set_metit_timeout(self, timeout):
        self.metit_timeout = timeout
        self.metit_options = ['metit', '--autoInclude', '--time', str(timeout)]

    def create_dirs(self):
        os.makedirs(self.feas_check_proved_dir)
        os.makedirs(self.feas_check_unproved_dir)

        os.makedirs(self.cont_trans_proved_dir)
        os.makedirs(self.cont_trans_unproved_dir)

        os.makedirs(self.disc_trans_proved_dir)
        os.makedirs(self.disc_trans_unproved_dir)

import code
import cmd, sys
import quantum

#my_console = code.InteractiveConsole()
#my_console.interact('Quantum Top Level')
#my_console.raw_input('Command: ')

class CLI(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(QUANTUM) > '

    def do_quit(self, arg):
        sys.exit(1)
    
    def do_abstract(self, arg):
        
        try:
            #print type(arg)
            if not arg:
                quantum.restart()
            else :
                quantum.run(arg.split())
        except KeyboardInterrupt:
            pause = 1
            print 'abstraction paused'
            
            
    def do_print(self, arg):
        #print quantum.filenames
        print quantum.cur_exp.system_def
    
    def do_stats(self, arg):

        hs = quantum.hybrid_system

        print '*'*40
        print 'Abstraction Proof Statistics'
        print '*'*40

        print 'Total Number of States : {}'.format(len([x for x in hs.itervalues() if x.is_feasible and x.feasability_checked and x.next_states]))
        print 'Total Number of Proved Transition Problems : {}'.format(quantum.cur_exp.trans_proved)
        print 'Total Number of Unproved Transition Problems : {}'.format(quantum.cur_exp.trans_unproved)
        print 'Total Number of Proved Infeasible Problems : {}'.format(quantum.cur_exp.infeas_proved)
        print 'Total Number of Unproved Infeasible Problems : {}'.format(quantum.cur_exp.infeas_unproved)
                                                                    
    def do_run(self, arg):
        
        try:
            while True:
                print 'hello world'
        except KeyboardInterrupt:
            print 'done'

    # shortcuts
    do_q = do_quit

if __name__ == '__main__':
    cli = CLI()
    cli.cmdloop('Quantum V0.1')

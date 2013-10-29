import code
import cmd, sys

#my_console = code.InteractiveConsole()
#my_console.interact('Quantum Top Level')
#my_console.raw_input('Command: ')

class CLI(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(QUANTUM) >'

    def do_quit(self, arg):
        sys.exit(1)

    def do_run(self, arg):
        
        try:
            while True:
                print 'hello world'
        except KeyboardInterrupt:
            print 'done'

if __name__ == '__main__':
    cli = CLI()
    cli.cmdloop('Quantum V0.1')

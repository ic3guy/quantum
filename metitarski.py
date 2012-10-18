import subprocess
import re
import predicate
#import predicates.State

metit_options = ('metit', 
                 '--autoInclude', 
                 '--time','1', '-t','0',
                 '-')

process = None

def send_to_metit(fof,output=True):
    if output:
        process = subprocess.Popen(metit_options, stdin=subprocess.PIPE)
    else:
        process = subprocess.Popen(metit_options, shell=False, stdout=open('/dev/null','w'), stdin=subprocess.PIPE)

    process.communicate(fof)

    return process.returncode

def make_fof_inf(state, subsdict=None):

    equation = state.get_state()
    
    if subsdict:
        rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        equation = pattern.sub(lambda m: rep[m.group(0)], equation)
    
    return 'fof(stdin, conjecture, (![%s] : ((X1>-pi & X1<pi) => ~(%s)))).' % (state.varstring, equation)

def make_fof_rel(state, derivative, op):

    return 'fof(checkTransition, conjecture, (![%s] : (%s => %s %s 0))).' % (state.varstring, state.get_state(), derivative, op)

def checkTransition(state, pred):
    next_state_predicates = []

    der = pred.derivative
    
    if pred.operator == '<':
        if not send_to_metit(make_fof_rel(state,der,'<')):
            next_state_predicates.append(predicate.MetitPredicate(pred.equation),'<')
        elif not  send_to_metit(make_fof_rel(state,der,'=')):
            next_state_predicates.append(predicate.MetitPredicate(pred.equation),'<')
        elif not send_to_metit(make_fof_rel(state,der,'>')):
            next_state_predicates.extend([predicate.MetitPredicate(pred.equation,'<'),predicate.MetitPredicate(pred.equation,'=')])
        else:
            next_state_predicates.extend([predicate.MetitPredicate(pred.equation,'<'),predicate.MetitPredicate(pred.equation,'='), predicate.MetitPredicate(pred.equation,'>')])
    elif pred.operator ==

    return next_state_predicates
            
    
if __name__ == '__main__': print 'hello world'

import subprocess
import re
import predicate
import uuid
#import predicates.State

metit_options = ('metit', 
                 '--autoInclude', 
                 '--time','1',
                 '-')

process = None

def send_to_metit(fof,output=False,tofile=True,metit_options=metit_options):
    if output:
        print fof
        process = subprocess.Popen(metit_options, stdin=subprocess.PIPE)
    else:
        process = subprocess.Popen(metit_options, shell=False, stdout=open('/dev/null','w'), stdin=subprocess.PIPE)

    #print fof
    process.communicate(fof)

    if tofile:
        if process.returncode==0:
            send_to_file(fof,'proved',uuid.uuid4())
            
    return process.returncode

def make_fof_inf(state, subsdict=None):

    equation = state.get_state()
    
    if subsdict:
        rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        equation = pattern.sub(lambda m: rep[m.group(0)], equation)
    
    return 'fof(stdin, conjecture, (![%s] : ((X1>-pi & X1<pi) => ~(%s)))).' % (state.varstring, equation)

def make_fof_rel(state, derivative, op):

    return 'fof(checkTransition, conjecture, (![%s] : ((X1>-pi & X1<pi) & %s => %s %s 0))).' % (state.varstring, state.get_state(), derivative, op)

def make_fof_rel_2(state, derivative, op1, op2):

    return 'fof(checkTransition, conjecture, (![%s] : ((X1>-pi & X1<pi) & %s => (%s %s 0 | %s %s 0)))).' % (state.varstring, state.get_state(), derivative, op1, derivative, op2)
    
def send_to_file(formula, directory, name):
    f = open('/opt/quantum/%s/%s.tptp' % (directory, name), 'wa')
    f.write(formula)
    f.close()
        
    
def checkTransition(state, pred):
    next_state_predicates = []

    der = pred.derivative
    pre = predicate.MetitEquation(pred.equation.equation,pred.equation.depvar,pred.equation.subs_dict,pred.equation.vars_dict)
    #the error was above, I was assigning the derivative to the pre equation. Coudln't find a state'
    
    lt = make_fof_rel(state,der,'<')
    eq = make_fof_rel(state,der,'=')
    gt = make_fof_rel(state,der,'>')

    lt_pred = predicate.MetitPredicate(pre,'<')
    gt_pred = predicate.MetitPredicate(pre,'>')
    eq_pred = predicate.MetitPredicate(pre,'=')
    
    if pred.operator == '<':
        if not send_to_metit(lt):
            next_state_predicates.extend([lt_pred])
        elif not  send_to_metit(eq):
            next_state_predicates.extend([lt_pred])
        elif not send_to_metit(gt):
            next_state_predicates.extend([lt_pred,eq_pred])
        else:
            send_to_file(lt,'unproved',uuid.uuid4())
            send_to_file(gt,'unproved',uuid.uuid4())
            send_to_file(eq,'unproved',uuid.uuid4())
            next_state_predicates.extend([lt_pred,eq_pred, gt_pred])
    elif pred.operator == '>':
        if not send_to_metit(lt):
            next_state_predicates.extend([gt_pred,eq_pred])
        elif not send_to_metit(eq):
            next_state_predicates.extend([gt_pred])
        elif not send_to_metit(gt):
            next_state_predicates.extend([gt_pred])
        else:
            send_to_file(lt,'unproved',uuid.uuid4())
            send_to_file(gt,'unproved',uuid.uuid4())
            send_to_file(eq,'unproved',uuid.uuid4())
            next_state_predicates.extend([gt_pred,eq_pred])
    elif pred.operator == '=':
        if not send_to_metit(lt):
            next_state_predicates.extend([lt_pred])
        elif not send_to_metit(eq):
            next_state_predicates.extend([eq_pred])
        elif not send_to_metit(gt):
            next_state_predicates.extend([gt_pred])
        else:
            send_to_file(lt,'unproved',uuid.uuid4())
            send_to_file(gt,'unproved',uuid.uuid4())
            send_to_file(eq,'unproved',uuid.uuid4())
            next_state_predicates.extend([gt_pred,eq_pred,lt_pred])
        

    return next_state_predicates

def checkTransition2(state, pred):
    Q1,Q2,Q3 = [],[],[]

    options = ('metit', 
           '--autoInclude', 
           '--time','30',
           '-')
    
    der = pred.derivative
    #pre = predicate.MetitEquation(pred.equation.equation,pred.equation.depvar,pred.equation.subs_dict,pred.equation.vars_dict)

    lteq = make_fof_rel_2(state,der,'<','=')
    gt_or_lt = make_fof_rel_2(state,der,'>', '<')
    #lt = make_fof_rel(state,der,'<')
    gteq = make_fof_rel_2(state,der,'>', '=')

    if not send_to_metit(gteq, output=True):
        Q1.append(state)
        print 'In Q1'
    
    if not send_to_metit(lteq, output=True):
        Q3.append(state)
        print 'In Q3'
    
    if not send_to_metit(gt_or_lt,output=True):
        Q2.append(state)
        print 'In Q2'

    return (Q1,Q2,Q3)

    
if __name__ == '__main__': print 'hello world'

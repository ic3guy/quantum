import subprocess
import re
import predicate
import uuid
import os
#import predicates.State

metit_options = ('metit', 
                 '--autoInclude', 
                 '--time','1','--allowSF',
                 '-q',
                 '-')

process = None

def send_to_metit(fof,output=False,metit_options=metit_options):
    if output:
        print fof
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
    
        #return 'fof(stdin, conjecture, (![%s] : ((X1>-3.141 & X1<3.141) => ~(%s)))).' % (state.varstring, equation)
        return 'fof(stdin, conjecture, (![%s] : (~(%s)))).' % (state.varstring, equation)


def make_fof_rel(state, derivative, op, subsdict=None):

    equation = state.get_state()
    
    if subsdict:
        rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        equation = pattern.sub(lambda m: rep[m.group(0)], equation)
    
        #return 'fof(checkTransition, conjecture, (![%s] : ((X1>-3.141 & X1<3.141) & %s => %s %s 0))).' % (state.varstring, equation, derivative, op)
        return 'fof(checkTransition, conjecture, (![%s] : (%s => %s %s 0))).' % (state.varstring, equation, derivative, op)

def make_fof_rel_2(state, derivative, op1, op2, subsdict=None):

    print state.varstring
    equation = state.get_state()
    
    if subsdict:
        rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        derivative = pattern.sub(lambda m: rep[m.group(0)], derivative)

        #return 'fof(checkTransition, conjecture, (![%s] : ((X1>-3.141 & X1<3.141) & %s => (%s %s 0 | %s %s 0)))).' % (state.varstring, equation, derivative, op1, derivative, op2)
        return 'fof(checkTransition, conjecture, (![%s] : (%s => (%s %s 0 | %s %s 0)))).' % (state.varstring, equation, derivative, op1, derivative, op2)
    
def send_to_file(formula, directory, name):
    f = open('%s/%s' % (directory, name), 'wa')
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

def pred_2_text(pred):
    if pred == '>':
        return 'gt'
    elif pred == '<':
        return 'lt'
    elif pred == '=':
        return 'eq'


def checkTransition2(state, pred, x, directory='.'):

    #os.makedirs('/opt/quantum/'+ directory_name + '/unproved')
    
    Q1,Q2,Q3 = [],[],[]

    options = ('metit', 
               '--autoInclude', 
               '--time','1', '--allowSF',
               '-q',
               '-')
    
    der = str(state.derivative(pred))
    #pre = predicate.MetitEquation(pred.equation.equation,pred.equation.depvar,pred.equation.subs_dict,pred.equation.vars_dict)

    lteq = make_fof_rel_2(state,der,'<','=',subsdict={'e':'*10^'})
    gt_or_lt = make_fof_rel_2(state,der,'>', '<',subsdict={'e':'*10^'})
    #lt = make_fof_rel(state,der,'<')
    gteq = make_fof_rel_2(state,der,'>', '=',subsdict={'e':'*10^'})

    if pred.operator == '>' or pred.operator == '=':
        if not send_to_metit(gteq, output=True,metit_options=options):
            Q1.append(state)
            #print 'In Q1'
        else: 
            send_to_file(gteq, directory, 'S_%s--Q1--P_%s--O_%s--I_gteq' % (state.number, x, pred_2_text(pred.operator)))
    
    if pred.operator == '<' or pred.operator == '=':
        if not send_to_metit(lteq, output=True,metit_options=options):
            Q3.append(state)
            #print 'In Q3'
        else:
            send_to_file(lteq, directory, 'S_%s--Q3--P_%s--O_%s--I_lteq' % (state.number, x, pred_2_text(pred.operator)))
    
    if pred.operator == '=':
        if not send_to_metit(gt_or_lt,output=True,metit_options=options):
            Q2.append(state)
            #print 'In Q2'
        else:
            send_to_file(gt_or_lt, directory, 'S_%s--Q2--P_%s--O_%s--I_neq' % (state.number, x, pred_2_text(pred.operator)))

    return (Q1,Q2,Q3)

def checkTransition3(state, pred, x, deriv_dict,transition,directory='.'):
    Q1,Q2,Q3 = [],[],[]

    options = ('metit', 
               '--autoInclude', 
               '--time','1',
               '-q',
               '-')
    
    der = predicate.metitarski_pp(pred.equation.equation.subs(transition['updates']).subs(pred.equation.vars_dict))
    print der
    #pre = predicate.MetitEquation(pred.equation.equation,pred.equation.depvar,pred.equation.subs_dict,pred.equation.vars_dict)

    lteq = make_fof_rel_2(state,der,'<','=',subsdict={'e':'*10^'})
    gt_or_lt = make_fof_rel_2(state,der,'>', '<',subsdict={'e':'*10^'})
    #lt = make_fof_rel(state,der,'<')
    gteq = make_fof_rel_2(state,der,'>', '=',subsdict={'e':'*10^'})

    if not send_to_metit(gteq, output=True,metit_options=options):
        Q1.append(state)
            #print 'In Q1'
    else: 
        send_to_file(gteq, directory, 'S_%s--Q1--P_%s--O_%s--I_gteq' % (state.number, x, pred_2_text(pred.operator)))
    
    if not send_to_metit(lteq, output=True,metit_options=options):
        Q3.append(state)
            #print 'In Q3'
    else:
        send_to_file(lteq, directory, 'S_%s--Q3--P_%s--O_%s--I_lteq' % (state.number, x, pred_2_text(pred.operator)))

    if not send_to_metit(gt_or_lt,output=True,metit_options=options):
        Q2.append(state)
            #print 'In Q2'
    else:
        send_to_file(gt_or_lt, directory, 'S_%s--Q2--P_%s--O_%s--I_neq' % (state.number, x, pred_2_text(pred.operator)))

    return (Q1,Q2,Q3)

    
if __name__ == '__main__': print 'hello world'

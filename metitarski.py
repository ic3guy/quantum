import subprocess
import re
import predicate
import uuid
import os
#import predicates.State

metit_options = ('metit', 
                 '--autoInclude', 
                 '--time','1',
                 '-q',
                 '-')

metit_output = False
sc_heur = False

#extra_constraints = ['SS^2+C^2=1','SS<1','SS>-1','C<1','C>-1']
#extra_constraints = ['PX<3.141', 'PX>-3.141']
extra_constraints = []

process = None

def send_to_metit(fof,output=metit_output,metit_options=metit_options):
    if output:
        print fof
        process = subprocess.Popen(metit_options, stdin=subprocess.PIPE)
    else:
        process = subprocess.Popen(metit_options, shell=False, stdout=open('/dev/null','w'), stdin=subprocess.PIPE)

    process.communicate(fof)
    
    return process.returncode

def make_fof_inf(state, var_string,sc_heur=False):
    #print [str(state)]
    y = list(extra_constraints)
    y.extend([str(state)])
    #print y
    if sc_heur:
        subsdict={'cos(PX)':'C','sin(PX)':'S'}
        rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        y = pattern.sub(lambda m: subsdict[m.group(0)], ' & '.join(y))
    
        return 'fof(stdin, conjecture, (![%s,S,C] : (~(%s & S^2+C^2=1)))).' % (var_string, y)
    else:
        return 'fof(stdin, conjecture, (![%s] : (~(%s)))).' % (var_string, ' & '.join(y))
        
def make_fof_rel(state, derivative, op, subsdict={'exp':'10^','e':'*10^'}):

    equation = state.get_state()
    
    if subsdict:
        rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        equation = pattern.sub(lambda m: rep[m.group(0)], equation)
    
        #return 'fof(checkTransition, conjecture, (![%s] : ((X1>-3.141 & X1<3.141) & %s => %s %s 0))).' % (state.varstring, equation, derivative, op)
        return 'fof(checkTransition, conjecture, (![%s] : (%s => %s %s 0))).' % (state.varstring, equation, derivative, op)

def make_fof_rel_2(var_string, state, derivative, op1, op2, sc_heur=False):
    y = list(extra_constraints)
    y.extend([str(state)])
    #y = ' & '.join(y)
    #print y
    #print y
    if sc_heur:
        subsdict={'cos(PX)':'C','sin(PX)':'S'}
        rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        #y = pattern.sub(lambda m: subsdict[m.group(0)], y)

        fof_rel = 'fof(checkTransition, conjecture, (![%s,S,C] : (%s & S^2+C^2=1 => (%s %s 0 | %s %s 0)))).' % (var_string, ' & '.join(y), derivative, op1, derivative, op2)

        return pattern.sub(lambda m: subsdict[m.group(0)], fof_rel)
    else:
        return 'fof(checkTransition, conjecture, (![%s] : (%s => (%s %s 0 | %s %s 0)))).' % (var_string, y, derivative, op1, derivative, op2)
    
def send_to_file(formula, directory, name):
    f = open('%s/%s' % (directory, name), 'wa')
    f.write(formula)
    f.close()        
    
def pred_2_text(pred):
    if pred == '>':
        return 'gt'
    elif pred == '<':
        return 'lt'
    elif pred == '=':
        return 'eq'

def checkTransition2(var_string, state, pred, x, system_def, directory='.'):

    #os.makedirs('/opt/quantum/'+ directory_name + '/unproved')
    
    Q1,Q2,Q3 = [],[],[]
     
    der = str(predicate.metit_derivative(pred, state.discrete_part, system_def))
    #pre = predicate.MetitEquation(pred.equation.equation,pred.equation.depvar,pred.equation.subs_dict,pred.equation.vars_dict)

    lteq = make_fof_rel_2(var_string, state, der,'<','=',sc_heur=sc_heur)
    gt_or_lt = make_fof_rel_2(var_string, state, der,'>', '<',sc_heur=sc_heur)
    #lt = make_fof_rel(state,der,'<')
    gteq = make_fof_rel_2(var_string, state,der,'>', '=',sc_heur=sc_heur)

    if pred.operator == '>' or pred.operator == '=':
        if not send_to_metit(gteq,metit_options=metit_options):
            Q1.append(state)
            #print 'In Q1'
        else: 
            send_to_file(gteq, directory, 'S_%s--Q1--P_%s--O_%s--I_gteq' % (state.number, x, pred_2_text(pred.operator)))
    
    if pred.operator == '<' or pred.operator == '=':
        if not send_to_metit(lteq,metit_options=metit_options):
            Q3.append(state)
            #print 'In Q3'
        else:
            send_to_file(lteq, directory, 'S_%s--Q3--P_%s--O_%s--I_lteq' % (state.number, x, pred_2_text(pred.operator)))
    
    if pred.operator == '=':
        if not send_to_metit(gt_or_lt,metit_options=metit_options):
            Q2.append(state)
            #print 'In Q2'
        else:
            send_to_file(gt_or_lt, directory, 'S_%s--Q2--P_%s--O_%s--I_neq' % (state.number, x, pred_2_text(pred.operator)))

    return (Q1,Q2,Q3)

def checkTransition3(var_string, state, pred, x, system_def, updates, directory='.'):
    Q1,Q2,Q3 = [],[],[]

    #options = ('metit', 
    #           '--autoInclude', 
    #           '--time','1',
    #           '--allowSF',
    #           '-q',
    #           '-')

    der = str(predicate.metit_substitution(pred, state.discrete_part, system_def, updates))
    #der = predicate.metitarski_pp(pred.equation.equation.subs(transition['updates']).subs(pred.equation.vars_dict))
    #print der
    #pre = predicate.MetitEquation(pred.equation.equation,pred.equation.depvar,pred.equation.subs_dict,pred.equation.vars_dict)

    #print state
    #print der
    
    lteq = make_fof_rel_2(var_string, state, der,'<', '=',sc_heur=sc_heur)
    gt_or_lt = make_fof_rel_2(var_string, state,der,'>', '<',sc_heur=sc_heur)
    #lt = make_fof_rel(state,der,'<')
    gteq = make_fof_rel_2(var_string, state,der,'>', '=',sc_heur=sc_heur)

    if not send_to_metit(gteq,metit_options=metit_options):
        Q1.append(state)
            #print 'In Q1'
    else: 
        send_to_file(gteq, directory, 'S_%s--Q1--P_%s--O_%s--I_gteq' % (state.number, x, pred_2_text(pred.operator)))
    
    if not send_to_metit(lteq,metit_options=metit_options):
        Q3.append(state)
            #print 'In Q3'
    else:
        send_to_file(lteq, directory, 'S_%s--Q3--P_%s--O_%s--I_lteq' % (state.number, x, pred_2_text(pred.operator)))

    if not send_to_metit(gt_or_lt,metit_options=metit_options):
        Q2.append(state)
            #print 'In Q2'
    else:
        send_to_file(gt_or_lt, directory, 'S_%s--Q2--P_%s--O_%s--I_neq' % (state.number, x, pred_2_text(pred.operator)))

    return (Q1,Q2,Q3)

    
if __name__ == '__main__':
    print 'Hello World'

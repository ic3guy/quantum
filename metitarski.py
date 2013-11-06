import subprocess
import re
import predicate
import uuid
import os
import tempfile
#import predicates.State
#from multiprocessing import Pool
from functools import partial

#metit_options = ('metit', 
#                  '--autoInclude', 
#                  '--time','10',
#                  '-q',
#                  '-')

metit_options = "NONE"


metit_output = True
sc_heur = False

#extra_constraints = ['SS^2+C^2=1','SS<1','SS>-1','C<1','C>-1']
#extra_constraints = ['X1<3.141', 'X1>-3.141']
#extra_constraints = []

process = None

def send_to_metit(fof,output=metit_output,metit_options=metit_options):

    with tempfile.NamedTemporaryFile() as temp:
        temp.write(fof)
        temp.flush()
        temp.seek(0)
        
        #metit_options.append(str(temp.name))
        metit_options_call = metit_options + [str(temp.name)]
        #print metit_options_call

        if output:
            print fof
            print metit_options
            process = subprocess.call(metit_options_call,stderr=subprocess.STDOUT)
        else:
            process = subprocess.call(metit_options_call, shell=False, stdout=open('/dev/null','w'))

    #process.communicate(fof)
            
        print "return code: %s" % process
        return process

def send_to_metit_nob(fof,output=metit_output,metit_options=metit_options):

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(fof)
        temp.flush()
        temp.seek(0)
        
        #metit_options.append(str(temp.name))
        metit_options_call = metit_options + [str(temp.name)]
        #print metit_options_call

        if output:
            print fof
            print metit_options
            process = subprocess.Popen(metit_options_call,stderr=subprocess.STDOUT)
        else:
            process = subprocess.Popen(metit_options_call, shell=False, stdout=open('/dev/null','w'))

    #process.communicate(fof)
            
        print "return code: %s" % process
        return process


def make_fof_inf(state, var_string,sc_heur=False,extra_constraints=[]):
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
        
# def make_fof_rel(state, derivative, op, subsdict={'exp':'10^','e':'*10^'}):

#     equation = state.get_state()
    
#     if subsdict:
#         rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
#         pattern = re.compile("|".join(rep.keys()))
#         equation = pattern.sub(lambda m: rep[m.group(0)], equation)
    
#         #return 'fof(checkTransition, conjecture, (![%s] : ((X1>-3.141 & X1<3.141) & %s => %s %s 0))).' % (state.varstring, equation, derivative, op)
#         return 'fof(checkTransition, conjecture, (![%s] : (%s => %s %s 0))).' % (state.varstring, equation, derivative, op)

def make_fof_rel_2(var_string, state, derivative, op1, op2, sc_heur=False, extra_constraints=[]):
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
            #derivative someties contain e, but very small, simplify to zero
        if op2 == '=' and op1 =='>':
            return 'fof(checkTransition, conjecture, (![%s] : (%s => (%s %s 10^-6 | (%s < 10^-6 & %s > -10^-6))))).' % (var_string,  ' & '.join(y), derivative, op1, derivative, derivative)
        elif op2 =='=' and op1 == '<':
            return 'fof(checkTransition, conjecture, (![%s] : (%s => (%s %s -10^-6 | (%s < 10^-6 & %s > -10^-6))))).' % (var_string,  ' & '.join(y), derivative, op1, derivative, derivative)
        else:
            return 'fof(checkTransition, conjecture, (![%s] : (%s => (%s %s 10^-6 | %s %s -10^-6)))).' % (var_string,  ' & '.join(y), derivative, op1, derivative, op2)
    
def send_to_file(formula, directory, name):
    print 'sending %s\n' % name
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

def cont_abs_trans_rel(state, pred, exp, subsdict={'exp':'10^','e':'*10^'}):

    #use multiprocessing on calling this function.

    metit_options = exp.metit_options
    Q1,Q2,Q3 = [],[],[]
     
    der = str(predicate.metit_derivative(pred, state.discrete_part, exp.system_def))
    
    if subsdict:
            rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
            pattern = re.compile("|".join(rep.keys()))
            der = pattern.sub(lambda m: rep[m.group(0)], der)
            
    ec = exp.extra_constraints

    lteq = make_fof_rel_2(exp.var_string, state, der,'<','=',sc_heur=sc_heur,extra_constraints=ec)
    gt_or_lt = make_fof_rel_2(exp.var_string, state, der,'>', '<',sc_heur=sc_heur,extra_constraints=ec)
    gteq = make_fof_rel_2(exp.var_string, state,der,'>', '=',sc_heur=sc_heur,extra_constraints=ec)

    if pred.operator == '>': #or pred.operator == '=':
        if not send_to_metit(gteq,metit_options=metit_options):
            Q1.append(state.number)
            exp.trans_proved += 1
            #print 'In Q1'
            send_to_file(gteq, exp.cont_trans_proved_dir, 'S_%s--Q1--P_%s--O_%s--I_gteq' % (state.number, pred.eq_num, pred_2_text(pred.operator)))
        else: 
            send_to_file(gteq, exp.cont_trans_unproved_dir, 'S_%s--Q1--P_%s--O_%s--I_gteq' % (state.number, pred.eq_num, pred_2_text(pred.operator)))
            exp.trans_unproved += 1
    
    if pred.operator == '<': #or pred.operator == '=':
        if not send_to_metit(lteq,metit_options=metit_options):
            Q3.append(state.number)
            exp.trans_proved += 1
            #print 'In Q3'
            send_to_file(lteq, exp.cont_trans_proved_dir, 'S_%s--Q3--P_%s--O_%s--I_lteq' % (state.number, pred.eq_num, pred_2_text(pred.operator)))
        else:
            send_to_file(lteq, exp.cont_trans_unproved_dir, 'S_%s--Q3--P_%s--O_%s--I_lteq' % (state.number, pred.eq_num, pred_2_text(pred.operator)))
            exp.trans_unproved +=1
    
    #multi processing here
    if pred.operator == '=':
        #pool = Pool(processes=4)
    
        commands = [lteq, gteq, gt_or_lt]
        processes = [send_to_metit_nob(cmd,metit_options=metit_options) for cmd in commands]

        for proc in processes:
            proc.wait()

        if not processes[0].returncode:
            Q3.append(state.number)
        
        if not processes[1].returncode:
            Q1.append(state.number)
       
        if not processes[2].returncode:
            Q2.append(state.number)

        #jobs = [('lteq', 'metit_options=metit_options'),('gteq', 'metit_options=metit_options'),('gt_or_lt', 'metit_options=metit_options')]

        #result = pool.map(lambda args: send_to_metit(*args),jobs)
        
        #print result

        # if not send_to_metit(gt_or_lt,metit_options=metit_options):
        #     Q2.append(state.number)
        #     exp.trans_proved += 1
        #     send_to_file(gt_or_lt, exp.cont_trans_proved_dir, 'S_%s--Q2--P_%s--O_%s--I_neq' % (state.number, x, pred_2_text(pred.operator)))
        #     #print 'In Q2'
        # else:
        #     send_to_file(gt_or_lt, exp.cont_trans_unproved_dir, 'S_%s--Q2--P_%s--O_%s--I_neq' % (state.number, x, pred_2_text(pred.operator)))
        #     exp.trans_unproved += 1

    return (Q1,Q2,Q3)

def checkTransition3(state, pred, updates, exp):
    Q1,Q2,Q3 = [],[],[]
    
    metit_options = exp.metit_options

    #options = ('metit', 
    #           '--autoInclude', 
    #           '--time','1',
    #           '--allowSF',
    #           '-q',
    #           '-')

    der = str(predicate.metit_substitution(pred, state.discrete_part, exp.system_def, updates))
    #der = predicate.metitarski_pp(pred.equation.equation.subs(transition['updates']).subs(pred.equation.vars_dict))
    #print der
    #pre = predicate.MetitEquation(pred.equation.equation,pred.equation.depvar,pred.equation.subs_dict,pred.equation.vars_dict)

    #print state
    #print der
    
    ec = exp.extra_constraints

    lteq = make_fof_rel_2(exp.var_string, state, der,'<', '=',sc_heur=sc_heur, extra_constraints=ec)
    gt_or_lt = make_fof_rel_2(exp.var_string, state,der,'>', '<',sc_heur=sc_heur,extra_constraints=ec)
    #lt = make_fof_rel(state,der,'<')
    gteq = make_fof_rel_2(exp.var_string, state,der,'>', '=',sc_heur=sc_heur,extra_constraints=ec)
    
    commands = [lteq, gteq, gt_or_lt]
    processes = [send_to_metit_nob(cmd,metit_options=metit_options) for cmd in commands]

    for proc in processes:
        proc.wait()

    if not processes[1].returncode:
        Q1.append(state)
            #print 'In Q1'
        send_to_file(gteq, exp.disc_trans_proved_dir, 'S_%s--Q1--P_%s--O_%s--I_gteq' % (state.number, pred.eq_num, pred_2_text(pred.operator)))
    else: 
        send_to_file(gteq, exp.disc_trans_unproved_dir, 'S_%s--Q1--P_%s--O_%s--I_gteq' % (state.number,pred.eq_num, pred_2_text(pred.operator)))
    
    if not processes[0].returncode:
        Q3.append(state)
            #print 'In Q3'
        send_to_file(lteq, exp.disc_trans_proved_dir, 'S_%s--Q3--P_%s--O_%s--I_lteq' % (state.number,pred.eq_num, pred_2_text(pred.operator)))
    else:
        send_to_file(lteq, exp.disc_trans_unproved_dir, 'S_%s--Q3--P_%s--O_%s--I_lteq' % (state.number,pred.eq_num, pred_2_text(pred.operator)))

    if not processes[2].returncode:
        Q2.append(state)
            #print 'In Q2'
        send_to_file(gt_or_lt, exp.disc_trans_proved_dir, 'S_%s--Q2--P_%s--O_%s--I_neq' % (state.number,pred.eq_num, pred_2_text(pred.operator)))
    else:
        send_to_file(gt_or_lt, exp.disc_trans_unproved_dir, 'S_%s--Q2--P_%s--O_%s--I_neq' % (state.number,pred.eq_num, pred_2_text(pred.operator)))

    return (Q1,Q2,Q3)

    
if __name__ == '__main__':
    print 'Hello World'

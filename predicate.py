__metaclass__ = type

from sympy import *
from sympy import diff
import metitarski
from itertools import product
import MetitarskiPrinter
import re

#to find all functions.
from sympy.core.function import AppliedUndef

assert diff

def get_derivs(n, seed, system, state):
    #Input is a metit equation
    derivatives = []

    for n in range(n):
        dn = MetitEquation(seed.equation.diff(seed.depvar).subs(system[state]['flow']))
        derivatives.append(dn)
        seed = dn

    return derivatives

def gen_meti_string(cls, subsdict={'e':'*10^', '**':'^', 'Abs':'abs'}):
        var_replace_list = [[var, sympify(str(var).replace("("+str(cls.depvar)+")","").upper())] for var in cls.equation.atoms(AppliedUndef)]
        #print var_list
        # any other variables
        var_replace_list.extend([[var, sympify(str(var).upper())] for var in cls.equation.free_symbols])
        #print var_list

        #print into a format by metitarski)
        rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
        #print rep
        pattern = re.compile("|".join(rep.keys()))
        equation_out = pattern.sub(lambda m: subsdict[m.group(0)], str(cls.equation.subs(var_replace_list)))

        return equation_out

class MetitEquation:
    def __init__(self, equation, var_id=0, depvar=Symbol('t'), is_lyapunov=False):
        #only accept a sympy function
        self.equation = equation
        #self.derivative = sympify(equation).diff(depvar).subs(subs_dict)
        self.depvar = depvar
        #self.subs_dict = subs_dict
        self.is_lyapunov = is_lyapunov
        self.var_list = [sympify(str(var).replace("("+str(self.depvar)+")","").upper()) for var in self.equation.atoms(AppliedUndef)]
        self.var_id = var_id
        self.meti_string = gen_meti_string(self)
        
    def __str__(self):
        return self.meti_string


    
    def plot_format(self, subs_dict):
        return self.equation.subs(subs_dict)
    
class MetitPredicate(MetitEquation):

    def __init__(self,equation,operator,var_id=0):
        super(MetitPredicate, self).__init__(equation,var_id=var_id)
        self.operator = operator
        #self.derivative = equation.print_derivative()
        #self.depvar = equation.depvar
        #self.equation_string = str(equation) + operator + '0'
        #self.plot_format_str = plot_format(equation,operator)
        #self.subs_dict = equation.subs_dict
        #self.vars_dict = equation.vars_dict

    def __str__(self):
        x = super(MetitPredicate, self).__str__() + self.operator + '0'
        return x

    def print_equation(self):
        return super(MetitPredicate, self).__str__()
    
    def __eq__(self, other):
        return str(self) == str(other)


def get_var_string(equations):

    var_list = []
    for equation in equations:
        for variable in equation.var_list:
            if str(variable) not in var_list:
                var_list.append(str(variable))
                
    return ','.join(var_list)
    
def plot_format(equation, operator):
    if operator == '=':
        return 'Eq(%s,0)' % equation
    else:
        return str(equation) + operator + '0'
        
class State:

    def __init__(self, number, discrete_part, *predicates):
        self.is_feasible = True
        self.state = predicates
        self.number = number
        self.next_states = [] #no variable args and keyword with default
        self.discrete_part = discrete_part
        self.guards = []
        self.feasability_checked = False
      
    def __eq__(self, other):
        for pred in self.state:
            if pred not in other.state:
                return False

        if self.discrete_part != other.discrete_part:
            return False

        return True

    #def __iter__(self):
    #    return self
        
    def __str__(self):
        return " & ".join([str(x) for x in self.state])

    def print_state_number(self):
        return str(self.number)

#    def derivative(self,pred):
#        if pred.equation.is_lyapunov:
#            return  metitarski_pp(pred.equation.equation.diff(pred.equation.depvar).subs(self.deriv_dict[self.discrete_part]['flow']).subs(pred.equation.vars_dict)) + '-10^-2'
#        else:
#            return metitarski_pp(pred.equation.equation.diff(pred.equation.depvar).subs(self.deriv_dict[self.discrete_part]['flow']).subs(pred.equation.vars_dict))

def metit_derivative(metit_equation, discrete_state, system):
    sympy_equation = metit_equation.equation.diff(metit_equation.depvar).subs(system[discrete_state]['flow'])
    return MetitEquation(sympy_equation)
    
def metit_substitution(metit_equation, discrete_state, system, updates):
    sympy_equation = metit_equation.equation.subs(updates)
    return MetitEquation(sympy_equation)
    
if __name__ == '__main__':
    t = Symbol('t')
    x1 = Function('x1')(t)
    x2 = Function('x2')(t)
    a = Symbol('a')

    x = MetitEquation(-9.8*sin(x1))
    y = MetitEquation(x2(t)+a)
    z = MetitEquation(1.90843655*sin(x1(t))**2 + 1.90843655*cos(x1(t))**2 - 3.916868466*cos(x1(t)) + 0.19984*x2(t)**2 - 0.0084319171)

    system_def_test = {('cont',): {'flow': {x1.diff(t): x2,
                                   x2.diff(t): -9.8*sin(x1)},
                              't': [],
                              'inv': []}}
    
    #flow = {x1.diff(t): x2, x2.diff(t): -9.8*sin(x1)}
    
    z = MetitPredicate(-9.8*sin(x1(t)),'<')
    #zz = MetitPredicate(-9.8*sin(x1(t)),'<')
    #y = MetitEquation(-9.8*sin(x1(t)))
    
    print x
    print y
    print z

    for i in range(4):
        xx = metit_derivative(x, ('cont',), system_def_test)
        print x
        x = xx

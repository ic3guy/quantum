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


def get_derivs(n, seed):

    derivatives = []

    for n in range(n):
        dn = MetitEquation(seed.equation.diff(seed.depvar).subs(seed.subs_dict[('cont',)]['flow']),'t',seed.subs_dict,seed.vars_dict)
        derivatives.append(dn)
        seed = dn

    return derivatives
    
class MetitEquation:
    def __init__(self, equation, depvar=Symbol('t'), is_lyapunov=False):
        #only accept a sympy function
        self.equation = equation
        #self.derivative = sympify(equation).diff(depvar).subs(subs_dict)
        self.depvar = depvar
        #self.subs_dict = subs_dict
        self.is_lyapunov = is_lyapunov
        
    def __str__(self, subsdict={'e':'*10^', '**':'^'}):

        #this gives us the functions
        var_list = [[var, sympify(str(var).replace("("+str(self.depvar)+")","").upper())] for var in self.equation.atoms(AppliedUndef)]
        #print var_list
        # any other variables
        var_list.extend([[var, sympify(str(var).upper())] for var in self.equation.free_symbols])
        #print var_list

        #print into a format by metitarski)
        rep = dict((re.escape(k), v) for k, v in subsdict.iteritems())
        #print rep
        pattern = re.compile("|".join(rep.keys()))
        equation_out = pattern.sub(lambda m: subsdict[m.group(0)], str(self.equation.subs(var_list)))
        
        return equation_out

    def plot_format(self, subs_dict):
        return self.equation.subs(subs_dict)
        
class MetitPredicate(MetitEquation):

    def __init__(self,equation,operator):
        super(MetitPredicate, self).__init__(equation)
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
    
    def __eq__(self, other):
        return self.equation.equation == other.equation.equation and self.operator == other.operator
        
    def get_equation(self):
        #pred_equation = str(self.equation) + self.operator + '0'
        return self.equation_string
    
def plot_format(equation, operator):
    if operator == '=':
        return 'Eq(%s,0)' % equation
    else:
        return str(equation) + operator + '0'
        
class State:

    def __init__(self, varstring, number, discrete_part, deriv_dict, *predicates):
        self.is_feasible = True
        self.state = predicates
        self.varstring = varstring
        self.number = number
        self.next_states = [] #no variable args and keyword with default
        self.discrete_part = discrete_part
        self.guards = []
        self.deriv_dict = deriv_dict

    def __eq__(self, other):
        for pred in self.state:
            #print self.state
            if pred not in other.state:
                #print other.state
                return False

        return True

    #def __iter__(self):
    #    return self
        
    def get_state(self):
        return " & ".join([x.get_equation() for x in self.state])

    def get_state_number(self):
        return str(self.number)

    def derivative(self,pred):
        if pred.equation.is_lyapunov:
            return  metitarski_pp(pred.equation.equation.diff(pred.equation.depvar).subs(self.deriv_dict[self.discrete_part]['flow']).subs(pred.equation.vars_dict)) + '-10^-2'
        else:
            return metitarski_pp(pred.equation.equation.diff(pred.equation.depvar).subs(self.deriv_dict[self.discrete_part]['flow']).subs(pred.equation.vars_dict))

       
if __name__ == '__main__':
    t = Symbol('t')
    x1 = Function('x1')(t)
    x2 = Function('x2')(t)
    a = Symbol('a')
    
    x = MetitEquation(-9.8*sin(x1(t)))
    y = MetitEquation(x2(t)+a)
    z = MetitEquation(1.90843655*sin(x1(t))**2 + 1.90843655*cos(x1(t))**2 - 3.916868466*cos(x1(t)) + 0.19984*x2(t)**2 - 0.0084319171)

    flow = {x1.diff(t): x2, x2.diff(t): -9.8*sin(x1)}

    z = MetitPredicate(-9.8*sin(x1(t)),'<')
        
    print x
    print y
    print z

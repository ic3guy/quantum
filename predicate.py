__metaclass__ = type

from sympy import *
from sympy import diff
import metitarski
from itertools import product
import MetitarskiPrinter

assert diff

def get_derivs(n, seed):

    derivatives = []
    
    for n in range(n):
        dn = MetitEquation(seed.derivative,seed.depvar,seed.subs_dict,seed.vars_dict)
        derivatives.append(dn)
        seed = dn

    return derivatives
    
def metitarski_pp(expr, **settings):
    """Transform an expression to a string with Mathematica syntax. """
    p = MetitarskiPrinter.MetitarskiPrinter(settings)
    s = p.doprint(expr)

    return s

class MetitEquation:
    def __init__(self,equation,depvar,subs_dict,vars_dict,is_lyapunov=False):
        self.equation = sympify(equation)
        self.derivative = sympify(equation).diff(depvar).subs(subs_dict)
        self.depvar = depvar
        self.subs_dict = subs_dict
        self.vars_dict = vars_dict
        self.is_lyapunov = is_lyapunov
        
    def __str__(self):
        return metitarski_pp(self.equation.subs(self.vars_dict))

    def print_derivative(self):
        if self.is_lyapunov:
            return metitarski_pp(self.derivative.subs(self.vars_dict)) + '-10^-2'
        else:
            return metitarski_pp(self.derivative.subs(self.vars_dict))
        
    def plot_format(self, subs_dict):
        return self.equation.subs(subs_dict)

    def get_derivative(self):
        return self.derivative.subs(vars_dict)
        
class MetitPredicate:

    def __init__(self,equation,operator):
        self.equation = equation
        self.operator = operator
        self.derivative = equation.print_derivative()
        self.depvar = equation.depvar
        self.equation_string = str(equation) + operator + '0'
        self.plot_format_str = plot_format(equation,operator)
        #self.subs_dict = equation.subs_dict
        #self.vars_dict = equation.vars_dict
        
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

    def __init__(self, varstring, number, *predicates):
        self.is_feasible = True
        self.state = predicates
        self.varstring = varstring
        self.number = number
        self.next_states = [] #no variable args and keyword with default

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

if __name__ == '__main__':

    e1 = MetitEquation('x(t)','t',{},{})
    e2 = MetitEquation('x(t)','t',{},{})
    
    p1 = MetitPredicate(e1,'<')
    p2 = MetitPredicate(e2,'>')
    p3 = MetitPredicate(e2, '>')
    s1 = State('X,Y',p1,p2,p3)
    p = metitarski.make_fof_inf(s1)
    #metitarski.send_to_metit(p)
    
    t = Symbol('t')
    X1 = Symbol('X1')
    X2 = Symbol('X2')

    x1 = Function('x1')(t)
    x2 = Function('x2')(t)
    
    
    deriv_dict = {x1.diff(t): x2,
                  x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

    vars_dict = {x1(t) : X1, x2(t) : X2}
    
    #def get_derivs(n, seed):
     #   dn = diff(seed).subs(deriv_dict)

    #e1 = MetitEquation('x2(t)','t',deriv_dict)
    #e2 = MetitEquation('sin(x1(t))*cos(x1(t))-10*sin(x1(t))','t',deriv_dict)

#    gen_equations = 

    #equations_initial = [MetitEquation(x1,'t',deriv_dict,vars_dict), MetitEquation(x2,t,deriv_dict,vars_dict), MetitEquation(sin(x1)*cos(x1)-10*sin(x1),t,deriv_dict,vars_dict)]

    
    #equations = [MetitEquation(x,'t',deriv_dict,vars_dict) for x in deriv_dict.values()]

    #equations = [MetitEquation(x1,'t',deriv_dict,vars_dict),
    #             MetitEquation(x2,'t',deriv_dict,vars_dict),
    #             MetitEquation(sin(x1)*cos(x1)-10*sin(x1),'t',deriv_dict,vars_dict),
   #              MetitEquation(0.3345*x2**2+1.4615*sin(x1)**2+1.7959*cos(x1)**2-6.689*cos(x1)+4.6931, 't',deriv_dict, vars_dict)]

   # e5 = MetitEquation(deriv_dict[x2.diff(t)],'t',deriv_dict,vars_dict)
    
    #equations.extend(e4)
    #equations.extend(get_derivs(1,e5))

    #feasible = 0
    #infeasible = 0
    #oplist = ['>','<']
    #inftest = []
    
   # for equation in equations:
    #    predlist = [MetitPredicate(equation,op) for op in oplist]
    #    inftest.append(predlist)

    #system = [State('X1,X2',*element) for element in product(*inftest)]

    #for state in system:
    #    print metitarski.make_fof_inf(state)
    #    rc = metitarski.send_to_metit(metitarski.make_fof_inf(state),output=False)
    #    if rc == 0: infeasible = infeasible+1
    #    if rc == 1: feasible = feasible+1

    #print "Feasible %s" % feasible
    #print "Infeasible %s" % infeasible


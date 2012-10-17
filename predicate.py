__metaclass__ = type

from sympy import *
from sympy import diff
import metitarski

assert diff

class MetitPredicate:

    def __init__(self,equation,operator):
        self.equation = equation
        self.operator = operator
        
    def get_equation(self):
        pred_equation = str(self.equation) + self.operator + '0'
        return pred_equation

    def get_derivative(self,var):
        return sympify(equation).diff(var)

class State:

    def __init__(self, varstring, *predicates):
        self.is_feasible = True
        self.state = predicates
        self.varstring = varstring
        
    def get_state(self):
        return " & ".join([x.get_equation() for x in self.state])

#if __name__ == '__main__':
#    p1 = Predicate('X','<')
#    p2 = Predicate('(X-3)','>')
#    p3 = Predicate('Y', '>')
#    s1 = State('X,Y',p1,p2,p3)
#    p = metitarski.make_fof_inf(s1)
    #metitarski.send_to_metit(p)

#    t = Symbol('t')
#    x1 = Function('x1')(t)
#    x2 = Function('x2')(t)

    #deriv_dict = {x1.diff(t): x2,
     #             x2.diff(t): sin(x1)*cos(x1)-10*sin(x1)}

    #def get_derivs(n, seed):
     #   dn = diff(seed).subs(deriv_dict)
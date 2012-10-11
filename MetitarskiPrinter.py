from sympy.printing.str import StrPrinter
from sympy.printing.precedence import precedence
from sympy.core import S
from sympy.polys.polyerrors import PolynomialError

class MetitarskiPrinter(StrPrinter):

    printmethod = "_metitarski"

   # _default_settings = {}

    #_translation_table = {
        #'**':'^',
   #     'x':'X',
   #     'y':'Y'
   # }

    def _print_Pow(self, expr, rational=False):
        PREC = precedence(expr)

        if expr.exp is S.Half and not rational:
            return "sqrt(%s)" % self._print(expr.base)

        if expr.is_commutative:
            if -expr.exp is S.Half and not rational:
                # Note: Don't test "expr.exp == -S.Half" here, because that will
                # match -0.5, which we don't want.
                return "1/sqrt(%s)" % self._print(expr.base)
            if expr.exp == -1:
                return '1/%s' % self.parenthesize(expr.base, PREC)

        e = self.parenthesize(expr.exp, PREC)
        if self.printmethod == '_metitarski' and expr.exp.is_Rational and expr.exp.q != 1:
            # the parenthesized exp should be '(Rational(a, b))' so strip parens,
            # but just check to be sure.
            if e.startswith('(Rational'):
                return '%s^%s' % (self.parenthesize(expr.base, PREC), e[1:-1])
        return '%s^%s' % (self.parenthesize(expr.base, PREC), e)

    def _print_Poly(self, expr):
        terms, gens = [], [ self._print(s) for s in expr.gens ]

        for monom, coeff in expr.terms():
            s_monom = []

            for i, exp in enumerate(monom):
                if exp > 0:
                    if exp == 1:
                        s_monom.append(gens[i])
                    else:
                        s_monom.append(gens[i] + "^%d" % exp)

            s_monom = "*".join(s_monom)

            if coeff.is_Add:
                if s_monom:
                    s_coeff = "(" + self._print(coeff) + ")"
                else:
                    s_coeff = self._print(coeff)
            else:
                if s_monom:
                    if coeff is S.One:
                        terms.extend(['+', s_monom])
                        continue

                    if coeff is S.NegativeOne:
                        terms.extend(['-', s_monom])
                        continue

                s_coeff = self._print(coeff)

            if not s_monom:
                s_term = s_coeff
            else:
                s_term = s_coeff + "*" + s_monom

            if s_term.startswith('-'):
                terms.extend(['-', s_term[1:]])
            else:
                terms.extend(['+', s_term])

        if terms[0] in ['-', '+']:
            modifier = terms.pop(0)

            if modifier == '-':
                terms[0] = '-' + terms[0]

        format = expr.__class__.__name__ + "(%s, %s"

        try:
            format += ", modulus=%s" % expr.get_modulus()
        except PolynomialError:
            format += ", domain='%s'" % expr.get_domain()

        format += ")"

        return format % (' '.join(terms), ', '.join(gens))


    def _print_MatPow(self, expr):
        PREC = precedence(expr)

        return '%s^%s'%(self.parenthesize(expr.base, PREC),
                         self.parenthesize(expr.exp, PREC))

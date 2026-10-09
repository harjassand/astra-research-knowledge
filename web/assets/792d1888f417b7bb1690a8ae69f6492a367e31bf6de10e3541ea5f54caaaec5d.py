"""Exact compiler for the divisibility construction (research artifact, 2026-10-09).

Requires Python 3.10+ and SymPy. All compilation arithmetic is rational.
The generated absorbing Markov chain uses nonnegative integer vector marks.
No Diophantine solver is called or supplied. The compiler does NOT decide
whether the resulting law is divisible.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb, lcm
import json
import random
from typing import Optional
import sympy as sp


@dataclass(eq=False, frozen=True)
class Expr:
    kind: str
    children: tuple['Expr', ...] = ()
    coefficient: Fraction = Fraction(1)
    mark: tuple[int, ...] = ()


def const(c) -> Expr:
    c = Fraction(c)
    if c < 0:
        raise ValueError('Negative constants are forbidden in positive expressions.')
    return Expr('const', coefficient=c)


def add(*children: Expr) -> Expr:
    return Expr('sum', tuple(children))


def mul(*children: Expr) -> Expr:
    return Expr('product', tuple(children))


def scale(c, child: Expr) -> Expr:
    return mul(const(c), child)


def star(child: Expr) -> Expr:
    return Expr('star', (child,))


def power(child: Expr, exponent: int) -> Expr:
    if exponent < 0:
        raise ValueError('A positive-expression power must be nonnegative.')
    return mul(*([child] * exponent))


def rational(x) -> Fraction:
    a, b = sp.Rational(x).as_numer_denom()
    return Fraction(int(a), int(b))


class Construction:
    """Compile p(x) to a rational law for m-divisibility or infinite divisibility.

    mode='finite' produces the law with PGF proportional to R**m.
    mode='infinite' produces H/(1-y*R). Each output is a valid law for EVERY
    integer polynomial p. Divisibility is equivalent to absence of a zero of p
    on N**d. degree_caps, when supplied, bound the coordinate degrees of p**2;
    fixed caps preserve the expression topology when coefficients vary.
    """
    def __init__(self, polynomial, variables: tuple[sp.Symbol, ...],
                 mode: str = 'infinite', m: int = 2,
                 degree_caps: Optional[tuple[int, ...]] = None):
        if not variables:
            raise ValueError('At least one Diophantine variable is required.')
        if mode not in {'finite', 'infinite'}:
            raise ValueError("mode must be 'finite' or 'infinite'.")
        if not isinstance(m, int) or m < 2:
            raise ValueError('m must be an integer at least two.')
        self.variables, self.d, self.mode, self.m = variables, len(variables), mode, m
        self.p = sp.Poly(polynomial, *variables, domain=sp.ZZ)
        g = sp.Poly(self.p.as_expr()**2 - sp.Rational(1, 2), *variables, domain=sp.QQ)
        actual = tuple(max(0, int(g.degree(v))) for v in variables)
        caps = actual if degree_caps is None else tuple(degree_caps)
        if len(caps) != self.d or any(c < a for c, a in zip(caps, actual)):
            raise ValueError('degree_caps must bound every coordinate degree of p**2.')
        self.caps = caps
        self.e = tuple(c + 1 for c in caps)
        self.E = sum(self.e)
        self.dimension = self.d + (2 if mode == 'infinite' else 1)
        self.rho = Fraction(1, 16 * self.E * (m if mode == 'finite' else 1))
        self.z = sp.symbols(f'z0:{self.d}')
        self.t, self.y = sp.symbols('t y')
        self.all_symbols = self.z + (self.t,) + ((self.y,) if mode == 'infinite' else ())
        Q = sp.prod((1-z)**e for z, e in zip(self.z, self.e))
        self.Q = sp.expand(Q)

        @lru_cache(None)
        def power_series_sum(i: int, k: int):
            z = self.z[i]
            if k == 0:
                return 1/(1-z)
            return sp.cancel(z * sp.diff(power_series_sum(i, k-1), z))

        signed_series = 0
        for exponent, coefficient in g.terms():
            signed_series += coefficient * sp.prod(
                power_series_sum(i, k) for i, k in enumerate(exponent))
        self.N = sp.Poly(sp.cancel(Q * signed_series), *self.z, domain=sp.QQ)
        self.index_set = tuple(product(*(range(c+1) for c in caps)))
        self.ncoeff = {a: rational(self.N.coeff_monomial(a)) for a in self.index_set}
        self.C = sum((1+c*c for c in self.ncoeff.values()), Fraction(0))
        self.A_formula = 1/Q
        self.T_formula = self.N.as_expr()/(2*sp.Rational(self.C.numerator, self.C.denominator)*Q)
        q = 1 + 2*self.t + 2*self.t**3 + self.t**4
        self.R_formula = self.A_formula*q + self.t**2*self.T_formula

        self.A = self.denominator_expr(self.e)
        self.U, self.V = self.positive_envelope(+1), self.positive_envelope(-1)
        self.R2 = self.positive_power(2)
        self.R3 = self.positive_power(3)
        if mode == 'finite':
            b = m % 2
            a = (m - 3*b)//2
            self.expression = mul(power(self.R2, a), power(self.R3, b))
            self.F_formula = self.R_formula**m
        else:
            H = star(self.monomial((0,)*self.d + (1, 0)))
            # HR coefficients: A, 3A, (5A+U)/2, (9A+U)/2,
            # and (11A+U)/2 for all t-degrees at least four.
            HR = add(self.A,
                     mul(self.t_power(1), scale(3, self.A)),
                     mul(self.t_power(2), scale(Fraction(1,2), add(scale(5,self.A),self.U))),
                     mul(self.t_power(3), scale(Fraction(1,2), add(scale(9,self.A),self.U))),
                     mul(self.t_power(4), H, scale(Fraction(1,2),add(scale(11,self.A),self.U))))
            y = self.monomial((0,)*(self.d+1)+(1,))
            self.expression = mul(add(H, mul(y, HR)), star(mul(power(y,2), self.R2)))
            self.F_formula = 1/((1-self.t)*(1-self.y*self.R_formula))
        self._value_cache: dict[int, Fraction] = {}
        self.normalizer = self.value(self.expression)
        self.states: list[list[dict]] = [[]]  # state zero is absorbing
        self.start = self._compile(self.expression, 0)
        for i, edges in enumerate(self.states[1:], 1):
            assert edges and sum((e['probability'] for e in edges), Fraction(0)) == 1
            assert all(e['probability'] >= 0 for e in edges)
        self.p0 = 1/self.normalizer

    def monomial(self, mark: tuple[int, ...]) -> Expr:
        if len(mark) != self.dimension or any(k < 0 for k in mark):
            raise ValueError('Invalid monomial mark.')
        return Expr('monomial', mark=tuple(mark))

    def t_power(self, k: int) -> Expr:
        return self.monomial((0,)*self.d + (k,) + ((0,) if self.mode=='infinite' else ()))

    def denominator_expr(self, exponents: tuple[int, ...]) -> Expr:
        factors = []
        for i, e in enumerate(exponents):
            mark = [0]*self.dimension
            mark[i] = 1
            factors.extend([star(self.monomial(tuple(mark)))] * e)
        return mul(*factors)

    def weighted_term(self, coefficient: Fraction, mark: tuple[int, ...],
                      denominators: tuple[int, ...]) -> Expr:
        return mul(const(coefficient), self.monomial(mark), self.denominator_expr(denominators))

    def positive_envelope(self, sign: int) -> Expr:
        """Positive expression for (C + sign*N)/(C*Q) = A + sign*2T."""
        zero = (0,)*self.d
        n0 = self.ncoeff[zero]
        terms = [scale((1+n0*n0+sign*n0)/self.C, self.A)]
        for alpha in self.index_set:
            if alpha == zero:
                continue
            n = self.ncoeff[alpha]
            b = 1+n*n
            padded = alpha + (0,)*(self.dimension-self.d)
            terms.append(self.weighted_term((b+sign*n)/self.C, padded, self.e))
            # Positive expansion of (1-z**alpha)/Q by telescoping and cancelling
            # exactly one geometric denominator in each nonempty summand.
            for i, a_i in enumerate(alpha):
                for j in range(a_i):
                    mark = [0]*self.dimension
                    for k in range(i):
                        mark[k] = alpha[k]
                    mark[i] = j
                    e = list(self.e)
                    e[i] -= 1
                    terms.append(self.weighted_term(b/self.C,tuple(mark),tuple(e)))
        return add(*terms)

    def positive_power(self, r: int) -> Expr:
        if r not in {2,3}:
            raise ValueError('Only the two base powers are used.')
        t = self.t
        q = 1+2*t+2*t**3+t**4
        plus, minus = q+t**2/2, q-t**2/2
        terms = []
        for j in range(r+1):
            h = sp.Poly(sp.expand(plus**j * minus**(r-j)),t)
            for k in range(4*r+1):
                c = rational(h.nth(k))*Fraction(comb(r,j),2**r)
                assert c >= 0
                if c:
                    terms.append(mul(const(c),self.t_power(k),power(self.U,j),power(self.V,r-j)))
        return add(*terms)

    def value(self, node: Expr) -> Fraction:
        key = id(node)
        if key in self._value_cache:
            return self._value_cache[key]
        if node.kind == 'const':
            v = node.coefficient
        elif node.kind == 'monomial':
            v = self.rho**sum(node.mark)
        elif node.kind == 'sum':
            v = sum((self.value(c) for c in node.children),Fraction(0))
        elif node.kind == 'product':
            v = Fraction(1)
            for c in node.children:
                v *= self.value(c)
        elif node.kind == 'star':
            q = self.value(node.children[0])
            if not 0 <= q < 1:
                raise ValueError('A star fails its convergence condition.')
            v = 1/(1-q)
        else:
            raise ValueError(node.kind)
        self._value_cache[key] = v
        return v

    def _new_state(self, edges: list[dict]) -> int:
        self.states.append(edges)
        return len(self.states)-1

    def _edge(self, probability: Fraction, target: int, mark=None) -> dict:
        return {'probability': Fraction(probability), 'target':target,
                'mark': (0,)*self.dimension if mark is None else mark}

    def _compile(self, node: Expr, continuation: int) -> int:
        # Subexpressions are normalized locally. Constants cancel in products
        # and are charged as weights at the enclosing sum.
        if node.kind == 'const':
            return continuation
        if node.kind == 'monomial':
            return self._new_state([self._edge(1,continuation,node.mark)])
        if node.kind == 'sum':
            total = self.value(node)
            if total <= 0:
                raise ValueError('Cannot normalize a zero expression.')
            edges = []
            for c in node.children:
                v = self.value(c)
                if v:
                    edges.append(self._edge(v/total,self._compile(c,continuation)))
            return self._new_state(edges)
        if node.kind == 'product':
            state = continuation
            for c in reversed(node.children):
                state = self._compile(c,state)
            return state
        if node.kind == 'star':
            q = self.value(node.children[0])
            loop = self._new_state([])
            body = self._compile(node.children[0],loop)
            self.states[loop] = [self._edge(1-q,continuation),self._edge(q,body)]
            return loop
        raise ValueError(node.kind)

    def sample(self, rng=None, max_steps: Optional[int]=None) -> tuple[int, ...]:
        """Exact rational transition draws (ideal unbiased bits).

        The optional cap raises an exception; it never silently returns a
        truncated sample. random.Random(seed) is only for reproducible demos.
        """
        rng = random.SystemRandom() if rng is None else rng
        state, steps = self.start, 0
        output = [0]*self.dimension
        while state:
            if max_steps is not None and steps >= max_steps:
                raise RuntimeError('Step cap reached; no sample returned.')
            edges = self.states[state]
            denominator = lcm(*(e['probability'].denominator for e in edges))
            draw = rng.randrange(denominator)
            for edge in edges:
                weight = edge['probability'].numerator*(denominator//edge['probability'].denominator)
                if draw < weight:
                    for i,k in enumerate(edge['mark']):
                        output[i] += k
                    state = edge['target']
                    break
                draw -= weight
            else:
                raise AssertionError('Invalid transition normalization.')
            steps += 1
        return tuple(output)

    def export(self, path: str) -> None:
        data = {'format':'marked-absorbing-chain-v1','mode':self.mode,'m':self.m,
                'polynomial':str(self.p.as_expr()),'variables':[str(v) for v in self.variables],
                'degree_caps':self.caps,'dimension':self.dimension,'rho':str(self.rho),
                'normalizer':str(self.normalizer),'mass_at_zero':str(self.p0),
                'start':self.start,'absorbing':0,
                'states':[[{'probability':str(e['probability']),'target':e['target'],'mark':e['mark']}
                           for e in edges] for edges in self.states]}
        with open(path,'w',encoding='utf-8') as f:
            json.dump(data,f,indent=2)


def exact_checks() -> dict:
    """Finite diagnostic checks, not a formal verification of the theorem."""
    A,T,U,V,t = sp.symbols('A T U V t')
    q = 1+2*t+2*t**3+t**4
    R=A*q+T*t**2
    for r in (2,3):
        expr=sum(sp.binomial(r,j)*U**j*V**(r-j)*(q+t*t/2)**j*(q-t*t/2)**(r-j)
                 for j in range(r+1))/2**r
        assert sp.expand(expr.subs({U:A+2*T,V:A-2*T})-R**r)==0
        lower=sp.Poly(sp.expand(2*q**r-(q+t*t/2)**r),t)
        assert all(lower.nth(k)>0 for k in range(4*r+1))
    HR=A+3*A*t+(5*A+U)*t*t/2+(9*A+U)*t**3/2+(11*A+U)*t**4/(2*(1-t))
    assert sp.cancel(HR.subs(U,A+2*T)-R/(1-t))==0
    x=sp.symbols('x')
    cases=[]
    for poly,mode,m in [(x-3,'finite',2),(x*x+1,'finite',3),(x-3,'infinite',2)]:
        c=Construction(poly,(x,),mode,m)
        substitutions={z:sp.Rational(c.rho.numerator,c.rho.denominator) for z in c.all_symbols}
        expected=sp.cancel(c.F_formula.subs(substitutions))
        assert rational(expected)==c.normalizer
        assert c.p0>Fraction(1,3)
        doubled={z:2*sp.Rational(c.rho.numerator,c.rho.denominator) for z in c.all_symbols}
        moment=rational(sp.cancel(c.F_formula.subs(doubled)))/c.normalizer
        assert moment<3
        z=c.z[0]
        coefficients=sp.series(c.T_formula,z,0,9).removeO().expand()
        for n in range(9):
            expected_T=(rational(poly.subs(x,n))**2-Fraction(1,2))/(2*c.C)
            assert rational(coefficients.coeff(z,n))==expected_T
        rng=random.Random(20261009)
        demo=[c.sample(rng,max_steps=100000) for _ in range(20)]
        cases.append({'polynomial':str(poly),'mode':mode,'m':m,'states':len(c.states),
                      'mass_at_zero':str(c.p0),'exponential_moment_2':str(moment),
                      'normalizer_identity':True,'first_9_T_coefficients':True,
                      'first_20_demo_samples':demo})
    # A separate bivariate rationalization check exercises the tensor product.
    x,y=sp.symbols('x y')
    c=Construction(x+y-2,(x,y),'infinite')
    assert rational(sp.cancel(c.F_formula.subs({z:sp.Rational(c.rho.numerator,c.rho.denominator)
                                              for z in c.all_symbols})))==c.normalizer
    return {'status':'all listed exact checks passed','formal_proof':False,
            'symbolic_padding_identities':True,'positive_base_power_bounds':True,
            'cases':cases,'bivariate_normalizer_identity':True}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',default='.')
    args=parser.parse_args()
    from pathlib import Path
    out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    report=exact_checks()
    (out/'exact_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    x=sp.symbols('x')
    for mode in ('finite','infinite'):
        c=Construction(x-3,(x,),mode)
        c.export(str(out/f'example_{mode}_chain.json'))
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))

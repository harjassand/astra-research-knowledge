"""Exact rational finite receiver for the audited global Lipschitz reward oracle.

This is NOT an implementation of the unrestricted oracle's proof enumeration.
The backend must return a checked GLOBAL polynomial upper certificate and an
actual paid law, and must certify the law's feature-vector approximation.
A finite restricted backend is permitted only with scope='finite_test', whose
outputs are deliberately not labelled global Morrey certificates.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from math import isqrt, factorial
from typing import Any, Callable


def ceilq(x: Q) -> int:
    return -((-x.numerator) // x.denominator)


def sqrt_bounds(x: Q, bits: int = 80) -> tuple[Q, Q]:
    assert x >= 0
    den = 1 << bits
    k = isqrt((x.numerator * den * den) // x.denominator)
    lo = Q(k, den)
    hi = lo if lo * lo == x else Q(k + 1, den)
    assert lo * lo <= x <= hi * hi
    return lo, hi


def determinant(z):
    u, v, w = z
    return 1 - u*u - v*v - w*w + 2*u*v*w


def null_q(z):
    u, v, w = z
    return u*v + u*w + v*w


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q
    def __post_init__(self):
        assert self.lo <= self.hi
    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo+other.lo, self.hi+other.hi)
    __radd__ = __add__
    def __neg__(self):
        return Interval(-self.hi, -self.lo)
    def __sub__(self, other):
        return self + (-as_interval(other))
    def __rsub__(self, other):
        return as_interval(other) - self
    def __mul__(self, other):
        other = as_interval(other)
        a = [self.lo*other.lo, self.lo*other.hi,
             self.hi*other.lo, self.hi*other.hi]
        return Interval(min(a), max(a))
    __rmul__ = __mul__
    def __truediv__(self, other):
        other = as_interval(other)
        assert not other.lo <= 0 <= other.hi
        return self * Interval(1/other.hi, 1/other.lo)
    def __rtruediv__(self, other):
        return as_interval(other) / self
    def mid(self):
        return (self.lo+self.hi)/2
    def width(self):
        return self.hi-self.lo


def as_interval(x):
    return x if isinstance(x, Interval) else Interval(Q(x), Q(x))


def atan_interval(x: Q, terms: int):
    assert 0 < x < 1
    s = sum(((-1)**k*x**(2*k+1)/Q(2*k+1)
             for k in range(terms)), Q(0))
    next_term = x**(2*terms+1)/Q(2*terms+1)
    return Interval(s, s+next_term) if terms % 2 == 0 else Interval(s-next_term, s)


def pi_interval(terms=40):
    return 16*atan_interval(Q(1,5), terms)-4*atan_interval(Q(1,239), terms)


def phase_cos_interval(k: int, m: int, error: Q):
    """cos(2*pi*k/m), using only rational Taylor/Machin enclosures."""
    assert m > 0 and error > 0
    k %= m
    if 2*k > m:
        k -= m
    terms = 4
    while True:
        x = pi_interval(terms) * Q(2*k,m)
        mid = x.mid()
        s = sum(((-1)**j*mid**(2*j)/Q(factorial(2*j))
                 for j in range(terms)), Q(0))
        remainder = abs(mid)**(2*terms)/Q(factorial(2*terms)) + x.width()/2
        if 2*remainder <= error:
            return Interval(max(Q(-1),s-remainder), min(Q(1),s+remainder))
        terms += 4


class TensorGrid:
    def __init__(self, n: int):
        assert n >= 1
        self.n = n
        self.h = Q(2,n)
        self.indices = list(product(range(n+1), repeat=3))
        self.nodes = [tuple(-1+self.h*j for j in ijk) for ijk in self.indices]
        self.index = {ijk:i for i,ijk in enumerate(self.indices)}
        self.N = len(self.nodes)

    def weights(self, z):
        assert len(z) == 3 and all(-1 <= a <= 1 for a in z)
        one_d = []
        for a in z:
            x = (Q(a)+1)/self.h
            k = min(self.n-1, x.numerator//x.denominator)
            t = x-k
            assert 0 <= t <= 1
            one_d.append(((k,1-t),(k+1,t)))
        out = {}
        for items in product(*one_d):
            ijk = tuple(t[0] for t in items)
            mass = items[0][1]*items[1][1]*items[2][1]
            if mass:
                out[self.index[ijk]] = mass
        assert sum(out.values(),Q(0)) == 1 and min(out.values()) >= 0
        return out

    def lift(self, v, z):
        return sum((v[i]*w for i,w in self.weights(z).items()),Q(0))

    def feature_lipschitz(self):
        # Each coordinate derivative of one tensor hat has magnitude <=1/h.
        return Q(2)/self.h

    def lifted_lipschitz(self, gamma):
        return 2*(1+gamma/self.h)

    def source_column(self, m: int, error: Q):
        """Rational p_hat; ||x_ab-Z_ab|| <= error, beta=2h+10/m+error."""
        assert error > 0
        # Each coordinate interval radius <=error/4; Euclidean error <error.
        cs = [phase_cos_interval(i,m,error/2).mid() for i in range(m)]
        out = [Q(0)]*self.N
        for i,j in product(range(m),repeat=2):
            for k,w in self.weights((cs[i],cs[j],cs[(i+j)%m])).items():
                out[k] += w/Q(m*m)
        assert sum(out,Q(0)) == 1 and min(out) >= 0
        return out, 2*self.h+Q(10,m)+error


def rational_upper_metric(nodes, gamma: Q):
    assert 0 < gamma <= Q(1,2)
    n = len(nodes)
    d = [[Q(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i):
            sq = sum((a-b)**2 for a,b in zip(nodes[i],nodes[j]))
            x = sq/(gamma*gamma)
            k = isqrt(x.numerator//x.denominator)
            if Q(k*k) < x:
                k += 1
            d[i][j] = d[j][i] = gamma*k
            assert d[i][j]**2 >= sq
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k]+d[k][j])
    for i in range(n):
        for j in range(n):
            sq = sum((a-b)**2 for a,b in zip(nodes[i],nodes[j]))
            assert d[i][j]**2 >= sq
            # d<=sqrt(sq)+gamma is equivalent to (d-gamma)_+^2<=sq.
            assert max(Q(0),d[i][j]-gamma)**2 <= sq
            assert d[i][j] < 4
    return d


def simplex_from_intervals(intervals, requested_l1):
    assert requested_l1 > 0
    lo = [max(Q(0), x.lo) for x in intervals]
    hi = [min(Q(1), x.hi) for x in intervals]
    assert all(a <= b for a,b in zip(lo,hi))
    assert sum(lo,Q(0)) <= 1 <= sum(hi,Q(0))
    missing = 1-sum(lo,Q(0))
    # The true vector lies above lo; moving all missing mass to one coordinate
    # causes L1 error at most twice that missing mass.
    assert 2*missing <= requested_l1
    out = lo.copy()
    out[0] += missing
    assert sum(out,Q(0)) == 1 and min(out) >= 0
    return out, 2*missing


@dataclass(frozen=True)
class AxisChordLaw:
    """An exact complete binary null law rooted at a rational interior point."""
    root: tuple[Q,Q,Q]
    axis: int = 0
    def __post_init__(self):
        assert all(abs(t) < 1 for t in self.root)
        assert determinant(self.root) > 0
        assert self.axis in (0,1,2)
    def atom_intervals(self, bits=80):
        j,k = [i for i in range(3) if i != self.axis]
        u,v,w = self.root[self.axis], self.root[j], self.root[k]
        lo,hi = sqrt_bounds((1-v*v)*(1-w*w),bits)
        r = Interval(lo,hi)
        assert r.lo > 0
        a_minus = v*w-r
        a_plus = v*w+r
        # p_plus=1/2+(u-vw)/(2r), avoids dependent denominator subtraction.
        p_plus = Q(1,2)+(u-v*w)/(2*r)
        p_minus = 1-p_plus
        atoms = []
        for coord,p in ((a_minus,p_minus),(a_plus,p_plus)):
            zz = [as_interval(t) for t in self.root]
            zz[self.axis] = coord
            atoms.append((zz,p))
        return atoms
    def feature_column(self, grid, budget):
        bits = 16
        while True:
            intervals = [Interval(Q(0),Q(0)) for _ in range(grid.N)]
            for atom,prob in self.atom_intervals(bits):
                z = [max(Q(-1),min(Q(1),t.mid())) for t in atom]
                # Euclidean radius <= sum coordinate half-widths, conservative.
                r = sum((max(abs(t.lo-a),abs(t.hi-a)) for t,a in zip(atom,z)),Q(0))
                weights = grid.weights(z)
                err = grid.feature_lipschitz()*r
                for i in range(grid.N):
                    center = weights.get(i,Q(0))
                    feat = Interval(max(Q(0),center-err),min(Q(1),center+err))
                    intervals[i] += prob*feat
            if sum((x.hi-x.lo for x in intervals),Q(0)) <= budget/2:
                return simplex_from_intervals(intervals,budget)
            bits *= 2


@dataclass
class RestrictedSolution:
    cost: Q
    mixture: list[Q]
    coupling: list[list[Q]]
    potential: list[Q]
    h: Q
    dual_value: Q


def _feasible_equalities(x, eq, rhs):
    return min(x)>=0 and all(sum((a*b for a,b in zip(row,x)),Q(0))==r
                            for row,r in zip(eq,rhs))


def _solve_square_or_tall(a,b):
    import sympy as sp
    try:
        answer,params=sp.Matrix(a).gauss_jordan_solve(sp.Matrix(b))
    except ValueError:
        return None
    if params.rows:
        return None
    return list(map(Q,answer))


def _transport_primal_candidate(c,eq,rhs):
    """Float discoveries are accepted ONLY after exact rational feasibility."""
    from scipy.optimize import linprog
    r=linprog(list(map(float,c)),A_eq=[[float(x) for x in row] for row in eq],
              b_eq=list(map(float,rhs)),bounds=(0,None),method='highs')
    if not r.success:
        return None
    for den in (10**6,10**12,10**18):
        x=[Q(float(v)).limit_denominator(den) for v in r.x]
        if _feasible_equalities(x,eq,rhs): return x
    # Recover basic variables from the float support, using exact equations.
    for tol in (1e-8,1e-12,1e-15,0):
        support=[j for j,a in enumerate(r.x) if a>tol]
        vals=_solve_square_or_tall([[row[j] for j in support] for row in eq],rhs)
        if vals is not None:
            x=[Q(0)]*len(c)
            for j,v in zip(support,vals):x[j]=v
            if _feasible_equalities(x,eq,rhs):return x
    return None


def _transport_primal_exhaustive(c,eq,rhs):
    """Finite exact fallback: enumerate basic feasible supports. No rate claim."""
    import sympy as sp
    from itertools import combinations
    rank=sp.Matrix(eq).rank();best=None;bestvalue=None
    for support in combinations(range(len(c)),rank):
        vals=_solve_square_or_tall([[row[j] for j in support] for row in eq],rhs)
        if vals is None:continue
        x=[Q(0)]*len(c)
        for j,v in zip(support,vals):x[j]=v
        if not _feasible_equalities(x,eq,rhs):continue
        value=sum((a*b for a,b in zip(c,x)),Q(0))
        if bestvalue is None or value<bestvalue:best,bestvalue=x,value
    assert best is not None
    return best


def _feasible_inequalities(x,a,b):
    return all(sum((u*v for u,v in zip(row,x)),Q(0))<=r for row,r in zip(a,b))


def _dual_candidate(c,a,b):
    from scipy.optimize import linprog
    r=linprog(list(map(float,c)),A_ub=[[float(x) for x in row] for row in a],
              b_ub=list(map(float,b)),bounds=(None,None),method='highs')
    if not r.success:return None
    for den in (10**6,10**12,10**18):
        x=[Q(float(v)).limit_denominator(den) for v in r.x]
        if _feasible_inequalities(x,a,b):return x
    for tol in (1e-7,1e-10,1e-13):
        tight=[i for i,(row,rhs) in enumerate(zip(a,b))
               if abs(sum(float(u)*v for u,v in zip(row,r.x))-float(rhs))<tol]
        x=_solve_square_or_tall([a[i] for i in tight],[b[i] for i in tight])
        if x is not None and _feasible_inequalities(x,a,b):return x
    return None


def _dual_exhaustive(c,a,b):
    from itertools import combinations
    best=None;bestvalue=None
    for active in combinations(range(len(a)),len(c)):
        x=_solve_square_or_tall([a[i] for i in active],[b[i] for i in active])
        if x is None or not _feasible_inequalities(x,a,b):continue
        value=sum((u*v for u,v in zip(c,x)),Q(0))
        if bestvalue is None or value<bestvalue:best,bestvalue=x,value
    assert best is not None
    return best


def exact_restricted_transport(p, columns, d):
    """Rational primal/dual certificates, never an unchecked solver value.

    HiGHS is merely a candidate finder. Exact reconstruction and every constraint
    are checked. If the primal/dual values fail to agree, finite rational basic
    vertex enumeration is the complete (potentially impractical) fallback.
    """
    n,s = len(p),len(columns)
    assert s and all(len(q)==n and sum(q,Q(0))==1 and min(q)>=0 for q in columns)
    assert sum(p,Q(0)) == 1 and min(p) >= 0
    width = n*n+s
    c = [d[i][j] for i in range(n) for j in range(n)]+[Q(0)]*s
    eq=[]; rhs=[]
    for i in range(n):
        row=[Q(0)]*width
        for j in range(n): row[i*n+j]=1
        eq.append(row);rhs.append(p[i])
    for j in range(n):
        row=[Q(0)]*width
        for i in range(n): row[i*n+j]=1
        for k in range(s): row[n*n+k]=-columns[k][j]
        eq.append(row);rhs.append(Q(0))
    eq.append([Q(0)]*(n*n)+[Q(1)]*s);rhs.append(Q(1))
    dual_c=[-x for x in p]+[Q(1)]
    ine=[];limits=[]
    for i in range(n):
        for j in range(n):
            if i==j: continue
            r=[Q(0)]*(n+1);r[i]=1;r[j]=-1
            ine.append(r);limits.append(d[i][j])
    for q in columns:
        ine.append(list(q)+[Q(-1)]);limits.append(Q(0))
    # Translation-invariant dual can be restricted to 0<=v_i,t<=4.
    for i in range(n+1):
        r=[Q(0)]*(n+1);r[i]=1;ine.append(r);limits.append(Q(4))
        r=[Q(0)]*(n+1);r[i]=-1;ine.append(r);limits.append(Q(0))
    answer=_transport_primal_candidate(c,eq,rhs)
    dual=_dual_candidate(dual_c,ine,limits)
    if answer is None or dual is None or sum((a*x for a,x in zip(c,answer)),Q(0)) != -sum((a*x for a,x in zip(dual_c,dual)),Q(0)):
        answer=_transport_primal_exhaustive(c,eq,rhs)
        dual=_dual_exhaustive(dual_c,ine,limits)
    assert _feasible_equalities(answer,eq,rhs)
    assert _feasible_inequalities(dual,ine,limits)
    value=sum((a*x for a,x in zip(c,answer)),Q(0))
    v=dual[:-1]
    h=max(sum((a*b for a,b in zip(v,q)),Q(0)) for q in columns)
    dual_value=sum((a*b for a,b in zip(v,p)),Q(0))-h
    assert value==dual_value==-sum((a*x for a,x in zip(dual_c,dual)),Q(0))
    return RestrictedSolution(value,answer[n*n:],
        [answer[i*n:(i+1)*n] for i in range(n)],v,h,dual_value)


@dataclass
class OracleResponse:
    law: Any
    lower: Q
    upper: Q
    certificate: Any
    scope: str = 'global_paid'


@dataclass
class ReceiverResult:
    lower: Q
    upper: Q
    laws: list[Any]
    mixture: list[Q]
    dual_potential: list[Q]
    upper_certificate: Any
    iterations: int
    scope: str


def received_bounds(sol, p, oracle_upper, beta, h, gamma, column_l1):
    raw_lower=sum((a*b for a,b in zip(sol.potential,p)),Q(0))-oracle_upper-beta-2*h-gamma
    lower=max(Q(0),raw_lower)
    upper=sol.cost+beta+2*h+2*column_l1
    gap=oracle_upper-sol.h
    lp_gap=sol.cost-sol.dual_value
    budget=lp_gap+gap+2*beta+4*h+gamma+2*column_l1
    assert upper-lower <= budget
    assert lower <= upper
    return lower,upper,gap,budget


def optimize_receiver(grid, p, d, beta, gamma, backend, initial_law,
                      *, epsilon, oracle_accuracy, column_l1, stop_gap,
                      scope='global_paid', max_iterations=None):
    """Run certified column generation.

    backend.price(grid,v,a) -> OracleResponse
    backend.check_upper(grid,v,response) -> True only for a replayed certificate
    backend.column(grid,law,b) -> (rational simplex vector, certified L1 error)

    The backend owns actual-law verification and integration. Never pass a
    finite-control upper value as a global certificate. max_iterations is an
    optional diagnostic limit: hitting it raises, never returns success.
    """
    assert scope in ('global_paid','finite_test')
    assert stop_gap-oracle_accuracy-2*column_l1 > 0
    assert stop_gap+2*beta+4*grid.h+gamma+2*column_l1 < epsilon
    laws=[initial_law]
    col,err=backend.column(grid,initial_law,column_l1)
    assert err <= column_l1
    columns=[col]
    iteration=0
    while True:
        iteration += 1
        if max_iterations is not None and iteration>max_iterations:
            raise RuntimeError('Diagnostic iteration limit; no completion certificate')
        sol=exact_restricted_transport(p,columns,d)
        r=backend.price(grid,sol.potential,oracle_accuracy)
        assert r.scope == scope
        assert backend.check_upper(grid,sol.potential,r)
        assert 0 <= r.upper-r.lower < oracle_accuracy
        low,up,gap,budget=received_bounds(sol,p,r.upper,beta,grid.h,gamma,column_l1)
        if gap<=stop_gap:
            assert up-low < epsilon
            return ReceiverResult(low,up,laws,sol.mixture,sol.potential,
                                  r.certificate,iteration,scope)
        col,err=backend.column(grid,r.law,column_l1)
        assert err <= column_l1
        assert sum(col,Q(0))==1 and min(col)>=0
        priced=sum((a*b for a,b in zip(sol.potential,col)),Q(0))
        assert priced>=r.lower-2*column_l1
        separation=stop_gap-oracle_accuracy-2*column_l1
        assert priced>sol.h+separation
        assert all(sum((abs(a-b) for a,b in zip(col,old)),Q(0))>separation/2
                   for old in columns)
        laws.append(r.law);columns.append(col)


@dataclass(frozen=True)
class DyadicNullTree:
    root: tuple[Q,Q,Q]
    left: Any = None
    right: Any = None
    left_probability: Q | None = None
    def __post_init__(self):
        assert determinant(self.root)>0 and all(abs(t)<1 for t in self.root)
        assert all(t.denominator & (t.denominator-1)==0 for t in self.root)
        if self.left is None:
            assert self.right is None and self.left_probability is None
        else:
            p=self.left_probability
            assert self.right is not None and 0<p<1
            assert self.left.root != self.right.root
            assert tuple(p*a+(1-p)*b for a,b in zip(self.left.root,self.right.root))==self.root
            assert null_q(tuple(a-b for a,b in zip(self.left.root,self.right.root)))==0
    def atom_intervals(self,bits=80):
        if self.left is None:
            return AxisChordLaw(self.root).atom_intervals(bits)
        return [(z,self.left_probability*p) for z,p in self.left.atom_intervals(bits)]+[
            (z,(1-self.left_probability)*p) for z,p in self.right.atom_intervals(bits)]
    def feature_column(self,grid,budget):
        if self.left is None:
            return AxisChordLaw(self.root).feature_column(grid,budget)
        a,ea=self.left.feature_column(grid,budget)
        b,eb=self.right.feature_column(grid,budget)
        p=self.left_probability
        return [p*x+(1-p)*y for x,y in zip(a,b)],p*ea+(1-p)*eb


def algebraic_expectation(law, reward: Callable, lipschitz: Q, accuracy: Q):
    """Reward is rational-valued on rational cube inputs (e.g. tensor lift)."""
    bits=16
    while True:
        answer=Interval(Q(0),Q(0))
        for atom,prob in law.atom_intervals(bits):
            z=[max(Q(-1),min(Q(1),x.mid())) for x in atom]
            radius=sum((max(abs(x.lo-a),abs(x.hi-a)) for x,a in zip(atom,z)),Q(0))
            value=Q(reward(z));error=lipschitz*radius
            answer+=prob*Interval(value-error,value+error)
        if answer.width()<accuracy:
            return answer
        bits*=2


def finite_horizon_dyadic_lower(level, horizon, reward, lipschitz, accuracy):
    """A computable COMPLETE paid lower search. Increasing level and horizon
    fairly is dense. This does not return a global upper bound.
    """
    from math import gcd
    den=1<<level
    ints=[ijk for ijk in product(range(-den+1,den),repeat=3)
          if determinant(tuple(Q(x,den) for x in ijk))>0]
    roots=[tuple(Q(x,den) for x in ijk) for ijk in ints]
    lookup={x:i for i,x in enumerate(ints)}
    actions=[[] for _ in roots]
    for i in range(len(roots)):
        for j in range(i):
            d=tuple(a-b for a,b in zip(ints[i],ints[j]))
            if null_q(d): continue
            g=gcd(gcd(abs(d[0]),abs(d[1])),abs(d[2]))
            for t in range(1,g):
                c=tuple(b+t*(a-b)//g for a,b in zip(ints[i],ints[j]))
                k=lookup.get(c)
                if k is not None:
                    actions[k].append((i,j,Q(t,g)))
    laws=[DyadicNullTree(z) for z in roots]
    lower=[algebraic_expectation(law,reward,lipschitz,accuracy).lo for law in laws]
    for _ in range(horizon):
        newlaws=laws.copy();newlower=lower.copy()
        for k,aa in enumerate(actions):
            for i,j,p in aa:
                value=p*lower[i]+(1-p)*lower[j]
                if value>newlower[k]:
                    newlower[k]=value
                    newlaws[k]=DyadicNullTree(roots[k],laws[i],laws[j],p)
        laws,lower=newlaws,newlower
    i=lookup[(0,0,0)]
    return laws[i],lower[i],{'level':level,'horizon':horizon,'helpers':len(roots),
                           'actions':sum(map(len,actions))}

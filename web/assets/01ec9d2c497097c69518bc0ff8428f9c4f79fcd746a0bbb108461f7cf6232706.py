"""Checks for conditional Slater/Jastrow/thermal transfer; not an FPRAS.

Run with the bundled Python to enable the numerical NumPy checks as well.
All purification and support identities below use exact rational arithmetic.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from math import ceil
from decimal import Decimal, localcontext
from pathlib import Path
import json
import random


@dataclass(frozen=True)
class QI:
    re: F = F(0)
    im: F = F(0)

    def __add__(self, z):
        z = qi(z)
        return QI(self.re + z.re, self.im + z.im)

    __radd__ = __add__

    def __neg__(self):
        return QI(-self.re, -self.im)

    def __sub__(self, z):
        return self + (-qi(z))

    def __mul__(self, z):
        z = qi(z)
        return QI(self.re*z.re-self.im*z.im, self.re*z.im+self.im*z.re)

    __rmul__ = __mul__

    def __truediv__(self, z):
        z = qi(z)
        n = z.re*z.re + z.im*z.im
        if not n:
            raise ZeroDivisionError
        return self * QI(z.re/n, -z.im/n)

    def conj(self):
        return QI(self.re, -self.im)

    def norm2(self):
        return self.re*self.re + self.im*self.im

    def __bool__(self):
        return bool(self.re or self.im)


def qi(x):
    return x if isinstance(x, QI) else QI(F(x))


def det(a):
    n = len(a)
    if not n:
        return QI(F(1))
    a = [[qi(x) for x in row] for row in a]
    out = QI(F(1))
    for i in range(n):
        pivot = next((j for j in range(i,n) if a[j][i]), None)
        if pivot is None:
            return QI()
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            out = -out
        z = a[i][i]
        out = out*z
        for j in range(i+1,n):
            c = a[j][i]/z
            for k in range(i+1,n):
                a[j][k] = a[j][k] - c*a[i][k]
    return out


def gram(b):
    n = len(b)
    return [[sum((b[i][k]*b[j][k].conj() for k in range(n)), QI())
             for j in range(n)] for i in range(n)]


def minor(a, rows, cols=None):
    cols = range(len(a[0])) if cols is None else cols
    return [[a[i][j] for j in cols] for i in rows]


def subsets(n, size=None):
    if size is None:
        return [frozenset(c) for k in range(n+1) for c in combinations(range(n), k)]
    return [frozenset(c) for c in combinations(range(n), size)]


def purification_checks(rng):
    checks = 0
    entries = 0
    for n in range(1,6):
        for trial in range(4):
            b = [[QI(F(rng.randint(-3,3),rng.randint(1,4)),
                     F(rng.randint(-2,2),rng.randint(1,4)))
                  for j in range(n)] for i in range(n)]
            a = b + [[qi(int(i==j)) for j in range(n)] for i in range(n)]
            w = gram(b)
            for r in range(n+1):
                ss = [tuple(sorted(s)) for s in subsets(n,r)]
                ts = [tuple(sorted(t)) for t in subsets(n,n-r)]
                amp = {(s,t):det(minor(a,s+tuple(n+j for j in t))) for s in ss for t in ts}
                # A positive local occupation filter, rational at the amplitude level.
                ds = {s:F(1,2)**sum(int(i in s) for i in range(0,n,2)) for s in ss}
                for s in ss:
                    for sp in ss:
                        lhs = ds[s]*ds[sp]*sum((amp[s,t]*amp[sp,t].conj() for t in ts), QI())
                        rhs = ds[s]*ds[sp]*det(minor(w,s,sp))
                        assert lhs == rhs, (n,trial,r,s,sp,lhs,rhs)
                        entries += 1
                checks += 1
    return {"sector_instances":checks,"exact_density_entries":entries}


def interval_support_checks(rng):
    tests = 0
    for _ in range(80):
        n = 6
        blocks = [frozenset((0,1)),frozenset((2,3)),frozenset((4,5))]
        lower = [rng.randint(0,2) for _ in blocks]
        upper = [rng.randint(l,2) for l in lower]
        r = rng.randint(0,n)
        bases = [s for s in subsets(n,r)
                 if all(l<=len(s&e)<=u for e,l,u in zip(blocks,lower,upper))]
        if not bases:
            continue
        for i in subsets(n):
            explicit = any(i<=b for b in bases)
            oracle = (all(len(i&e)<=u for e,u in zip(blocks,upper))
                      and sum(max(l,len(i&e)) for e,l in zip(blocks,lower))<=r)
            assert explicit == oracle, (i,lower,upper,r)
            tests += 1
    return {"exact_independence_oracle_tests":tests}


def laminar_support_checks(rng):
    # Universe -> two pairs -> singletons.
    clusters = [frozenset(range(4)),frozenset((0,1)),frozenset((2,3))]
    children = {clusters[0]:clusters[1:]}
    children[clusters[1]] = [frozenset((0,)),frozenset((1,))]
    children[clusters[2]] = [frozenset((2,)),frozenset((3,))]
    allsets = subsets(4)
    tests = 0
    for _ in range(100):
        r = rng.randint(0,4)
        intervals = {clusters[0]:(r,r)}
        for c in clusters[1:]:
            l = rng.randint(0,2)
            intervals[c] = (l,rng.randint(l,2))
        for forced in allsets:
            for deleted in allsets:
                if forced&deleted:
                    continue
                bs = [s for s in allsets if forced<=s and not(s&deleted)
                      and all(l<=len(s&c)<=u for c,(l,u) in intervals.items())]
                def dp(c):
                    if len(c)==1:
                        return (1,1) if c<=forced else (0,0) if c<=deleted else (0,1)
                    ivs = [dp(d) for d in children[c]]
                    if any(v is None for v in ivs):
                        return None
                    lo = sum(v[0] for v in ivs)
                    hi = sum(v[1] for v in ivs)
                    l,u = intervals.get(c,(0,len(c)))
                    lo,hi = max(lo,l),min(hi,u)
                    return (lo,hi) if lo<=hi else None
                assert bool(bs) == (dp(clusters[0]) is not None), (intervals,forced,deleted)
                tests += 1
    return {"exact_laminar_prefix_feasibility_tests":tests}


def taylor_checks():
    tests = 0
    largest = Decimal(0)
    with localcontext() as ctx:
        ctx.prec = 100
        for radius in [F(0),F(1,3),F(1),F(3),F(10)]:
            for p in [4,12,30,60]:
                degree = 12*ceil(radius)+p+1
                for j in range(-8,9):
                    x = radius*F(j,8)
                    term = F(1)
                    v = term
                    for k in range(1,degree+1):
                        term *= x/F(k)
                        v += term
                    xd = Decimal(x.numerator)/Decimal(x.denominator)
                    vd = Decimal(v.numerator)/Decimal(v.denominator)
                    err = abs(vd/xd.exp()-1)
                    assert v>0 and err<=Decimal(2)**(-p), (radius,p,j,err)
                    largest = max(largest,err)
                    tests += 1
    return {"scalar_relative_taylor_tests":tests,"max_relative_error":str(largest)}


def numerical_stability_checks():
    import numpy as np
    rng = np.random.default_rng(671)
    tests = 0
    max_ratio = 0.0
    def unitary(n):
        z = rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
        return np.linalg.qr(z)[0]
    def gamma(q,r):
        ids = list(combinations(range(q.shape[0]),r))
        return np.array([[np.linalg.det(q[np.ix_(i,j)]) for j in ids] for i in ids])
    for _ in range(200):
        n,r = 4,2
        u = unitary(n)
        vals = np.exp(-rng.uniform(0,12,n))
        q = (u*vals)@u.conj().T
        root = (u*np.sqrt(vals))@u.conj().T
        v = unitary(n)
        delta = rng.uniform(0.001,0.4)
        mid = (v*np.exp(rng.uniform(-delta,delta,n)))@v.conj().T
        qt = root@mid@root
        d = np.diag(np.exp(-rng.uniform(0,10,6)))
        if tests%3==0:
            d[0,0]=0
        aa = d@gamma(q,r)@d
        bb = d@gamma(qt,r)@d
        rho,sigma = aa/np.trace(aa),bb/np.trace(bb)
        td = sum(abs(np.linalg.eigvalsh(rho-sigma)))/2
        bound = np.tanh(r*delta/2)
        assert td<=bound+1e-9,(td,bound)
        max_ratio=max(max_ratio,float(td/bound))
        tests+=1
    return {"numerical_filtered_loewner_tests":tests,"max_distance_to_bound_ratio":max_ratio}


def interacting_gibbs_obstruction():
    # One-particle h has identical spin-preserving hops between two sites.
    # Parameter c=5/4,s=3/4 gives c^2-s^2=1 and corresponds to beta*t=ln 2.
    c,s=F(5,4),F(3,4)
    w = [[qi(c if i==j else -s if (i,j) in [(0,2),(2,0),(1,3),(3,1)] else 0)
          for j in range(4)] for i in range(4)]
    ss=[(0,1),(0,3),(1,2),(2,3)]
    # Keep one fermion per site instead; ordering [1up,1down,2up,2down].
    ss=[(0,2),(0,3),(1,2),(1,3)]
    g=[[det(minor(w,a,b)) for b in ss] for a in ss]
    expected=[[qi(1),qi(0),qi(0),qi(0)],
              [qi(0),qi(c*c),qi(-s*s),qi(0)],
              [qi(0),qi(-s*s),qi(c*c),qi(0)],
              [qi(0),qi(0),qi(0),qi(1)]]
    assert g==expected
    singlet=c*c+s*s
    triplets=F(1)
    td=3*(singlet-1)/(4*(singlet+3))
    assert td==F(27,164)
    return {"exact_projected_thermal_singlet_weight":str(singlet),
            "triplet_weight":str(triplets),
            "distance_from_projected_H_gibbs":str(td)}


def bcs_particle_hole_checks(rng):
    entries=0
    instances=0
    for n in range(1,5):
        for trial in range(10):
            f=[[QI(F(rng.randint(-2,2),rng.randint(1,3)),
                   F(rng.randint(-2,2),rng.randint(1,3)))
                for j in range(n)] for i in range(n)]
            if trial%2==0:
                # Symmetric F is the spin-singlet subclass.
                for i in range(n):
                    for j in range(i):
                        f[i][j]=f[j][i]
            gs=[rng.choice([F(3,4),F(1),F(2)]) for _ in range(n)]
            assert all(g*g>=F(1,2) for g in gs)
            a=[[gs[i]*x for x in f[i]] for i in range(n)]
            a += [[qi(int(i==j)) for j in range(n)] for i in range(n)]
            for k in range(n+1):
                for ss in combinations(range(n),k):
                    for ds in combinations(range(n),k):
                        hs=tuple(j for j in range(n) if j not in ds)
                        # Graph Slater after the symmetric residual onsite filter.
                        graph=det(minor(a,ss+tuple(n+j for j in hs)))
                        for j in set(ss)&set(hs):
                            graph=graph/gs[j]
                        # X every hole, then Z each odd-indexed physical down mode.
                        graph=graph*((-1)**sum(ds))
                        bcs=det(minor(f,ss,ds))*((-1)**(k*(k-1)//2))
                        for j in set(ss)&set(ds):
                            bcs=bcs*gs[j]
                        assert graph==bcs,(n,trial,ss,ds,graph,bcs)
                        entries+=1
            instances+=1
    return {"opposite_spin_bcs_instances":instances,
            "exact_bcs_particle_hole_filtered_amplitudes":entries}


def main():
    rng=random.Random(625)
    result={"status":"PASS; identities/support/stability only; no FPRAS or quantum compiler executed"}
    result.update(purification_checks(rng))
    result.update(interval_support_checks(rng))
    result.update(laminar_support_checks(rng))
    result.update(taylor_checks())
    result.update(numerical_stability_checks())
    result.update(interacting_gibbs_obstruction())
    result.update(bcs_particle_hole_checks(rng))
    out=Path(__file__).with_suffix('.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()

"""Small exact spin-j transcription checks; not an all-N theorem verifier.

Only output: higher_spin_exact_checks.json beside this owned script.
Uses rational complex scalars and second-order Taylor jets, no dependencies.
The symmetric weight basis is unnormalized: its Gram diagonal is binom(p,k).
All matrix identities, traces and similarity invariants are basis independent.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from math import comb, factorial
from pathlib import Path
import json
import time


class Q:
    __slots__ = ("re", "im")
    def __init__(self, re=0, im=0):
        if isinstance(re, Q):
            self.re, self.im = re.re, re.im
        else:
            self.re, self.im = F(re), F(im)
    @staticmethod
    def coerce(x):
        return x if isinstance(x, Q) else Q(x)
    def __add__(self, x):
        if isinstance(x, Jet):
            return NotImplemented
        x = self.coerce(x)
        return Q(self.re+x.re, self.im+x.im)
    __radd__ = __add__
    def __neg__(self):
        return Q(-self.re, -self.im)
    def __sub__(self, x):
        return self + (-self.coerce(x))
    def __rsub__(self, x):
        return self.coerce(x) + (-self)
    def __mul__(self, x):
        if isinstance(x, Jet):
            return NotImplemented
        x = self.coerce(x)
        return Q(self.re*x.re-self.im*x.im, self.re*x.im+self.im*x.re)
    __rmul__ = __mul__
    def __truediv__(self, x):
        x = self.coerce(x)
        den = x.re*x.re+x.im*x.im
        return Q((self.re*x.re+self.im*x.im)/den,
                 (self.im*x.re-self.re*x.im)/den)
    def __rtruediv__(self, x):
        return self.coerce(x)/self
    def __eq__(self, x):
        try:
            x = self.coerce(x)
        except (TypeError, ValueError):
            return False
        return self.re == x.re and self.im == x.im
    def __bool__(self):
        return bool(self.re or self.im)
    def __repr__(self):
        return f"({self.re}+{self.im}i)"


ZERO = (0, 0, 0)
MONOMIALS = [a for a in product(range(3), repeat=3) if sum(a) <= 2]


class Jet:
    __slots__ = ("c",)
    def __init__(self, value=0, coeff=None):
        if isinstance(value, Jet) and coeff is None:
            self.c = value.c.copy()
        else:
            self.c = {ZERO: Q.coerce(value)} if coeff is None else {
                a: Q.coerce(v) for a, v in coeff.items() if v
            }
    @staticmethod
    def coerce(x):
        return x if isinstance(x, Jet) else Jet(x)
    @staticmethod
    def variable(value, axis):
        a = [0, 0, 0]
        a[axis] = 1
        return Jet(coeff={ZERO: value, tuple(a): 1})
    def __add__(self, x):
        x = self.coerce(x)
        return Jet(coeff={a: self.c.get(a, Q())+x.c.get(a, Q())
                          for a in set(self.c)|set(x.c)})
    __radd__ = __add__
    def __neg__(self):
        return Jet(coeff={a: -v for a, v in self.c.items()})
    def __sub__(self, x):
        return self + (-self.coerce(x))
    def __rsub__(self, x):
        return self.coerce(x) + (-self)
    def __mul__(self, x):
        x = self.coerce(x)
        out = {}
        for a, va in self.c.items():
            for b, vb in x.c.items():
                ab = tuple(a[i]+b[i] for i in range(3))
                if sum(ab) <= 2:
                    out[ab] = out.get(ab, Q())+va*vb
        return Jet(coeff=out)
    __rmul__ = __mul__
    def reciprocal(self):
        c = self.c.get(ZERO, Q())
        if not c:
            raise ZeroDivisionError
        v = self*(1/c)-1
        return (1-v+v*v)*(1/c)
    def __truediv__(self, x):
        return self*self.coerce(x).reciprocal()
    def __rtruediv__(self, x):
        return self.coerce(x)*self.reciprocal()
    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        out, base = Jet(1), self
        while n:
            if n & 1:
                out = out*base
            base = base*base
            n //= 2
        return out
    def derivative(self, a):
        return self.c.get(a, Q())*product_factorial(a)


def product_factorial(a):
    out = 1
    for x in a:
        out *= factorial(x)
    return out


def mat_zero(d):
    return [[Q() for _ in range(d)] for _ in range(d)]


def mat_identity(d):
    return [[Q(int(i == j)) for j in range(d)] for i in range(d)]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def multiply(a, b):
    d = len(a)
    return [[sum((a[i][k]*b[k][j] for k in range(d)), Q())
             for j in range(d)] for i in range(d)]


def kron(a, b):
    return [[a[i][j]*b[k][l] for j in range(len(a)) for l in range(len(b))]
            for i in range(len(a)) for k in range(len(b))]


def tensor_power(a, n):
    out = [[Q(1)]]
    for _ in range(n):
        out = kron(out, a)
    return out


def linear(c, mats):
    out = mat_zero(len(mats[0]))
    for ci, mi in zip(c, mats):
        out = add(out, scale(ci, mi))
    return out


def trace(a):
    return sum((a[i][i] for i in range(len(a))), Q())


def equal(a, b):
    return all(x == y for ar, br in zip(a, b) for x, y in zip(ar, br))


def transpose(a):
    return [list(row) for row in zip(*a)]


def local_spin(p):
    d = p+1
    sp, sm, sz = mat_zero(d), mat_zero(d), mat_zero(d)
    for k in range(d):
        sz[k][k] = Q(F(p, 2)-k)
        if k > 0:
            sp[k-1][k] = Q(p-k+1)
        if k < p:
            sm[k+1][k] = Q(k+1)
    sx = scale(F(1, 2), add(sp, sm))
    sy = scale(Q(0, F(-1, 2)), add(sp, scale(-1, sm)))
    return sx, sy, sz


def total_spin(local, n):
    d = len(local)
    out = mat_zero(d**n)
    for slot in range(n):
        term = [[Q(1)]]
        for a in range(n):
            term = kron(term, local if a == slot else mat_identity(d))
        out = add(out, term)
    return out


def local_kernel(p, m):
    x, y, z = m
    rho = [[(1+z)/2, (x-Q(0, 1)*y)/2],
           [(x+Q(0, 1)*y)/2, (1-z)/2]]
    qp = []
    for l in range(p+1):
        row = []
        for k in range(p+1):
            val = Jet()
            for a in range(max(0, k-(p-l)), min(l, k)+1):
                val += (comb(l, a)*comb(p-l, k-a)
                        *rho[1][1]**a *rho[1][0]**(l-a)
                        *rho[0][1]**(k-a) *rho[0][0]**(p-l-k+a))
            row.append(val)
        qp.append(row)
    zp = sum((qp[i][i] for i in range(p+1)), Jet())
    return [[val/zp for val in row] for row in qp], zp


def fp(p, x, order=0):
    out = Jet()
    for h in range(order, p//2+1):
        coeff = comb(p+1, 2*h+1)
        for z in range(order):
            coeff *= h-z
        out += coeff*x**(h-order)
    return out


def scalar_dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q())


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0]]


def const(jet):
    return jet.c.get(ZERO, Q())


def derivative_matrix(a, powers):
    return [[x.derivative(powers) for x in row] for row in a]


def check_fixture(p, n, point, axis):
    m = [Jet.variable(point[i], i) for i in range(3)]
    rloc, zp = local_kernel(p, m)
    x = sum((mi*mi for mi in m), Jet())
    norm_identity = zp - fp(p, x)/2**p
    assert not any(norm_identity.c.values()), "normalizer polynomial"
    eta = p+2*(1-x)*fp(p, x, 1)/fp(p, x)
    u = sum((axis[i]*m[i] for i in range(3)), Jet())
    mu = eta*u
    v = [Q(axis[i])-const(u)*Q(point[i]) for i in range(3)]
    r = cross(list(map(Q, axis)), list(map(Q, point)))
    kval = tensor_power(rloc, n)
    val = derivative_matrix(kval, ZERO)
    grad = []
    for i in range(3):
        powers = tuple(int(i == a) for a in range(3))
        grad.append(derivative_matrix(kval, powers))
    hess = []
    for i in range(3):
        row = []
        for j in range(3):
            powers = tuple(int(i == a)+int(j == a) for a in range(3))
            row.append(derivative_matrix(kval, powers))
        hess.append(row)
    jloc = linear(axis, local_spin(p))
    jtot = total_spin(jloc, n)
    jk, kj = multiply(jtot, val), multiply(val, jtot)
    bval = add(scale(n*const(mu), val), linear(v, grad))
    rval = linear(r, grad)
    assert equal(add(jk, kj), bval), "normalized anticommutator"
    assert equal(add(jk, scale(-1, kj)), scale(Q(0, 1), rval)), "rotation sign"
    dmu = scalar_dot(v, [mu.derivative(tuple(int(i == a) for a in range(3)))
                         for i in range(3)])
    uu = const(u)
    vg_v = [-Q(point[i])-uu*Q(axis[i])+2*uu*uu*Q(point[i])
            for i in range(3)]
    rg_r = [uu*Q(axis[i])-Q(point[i]) for i in range(3)]
    second = scale(n*n*const(mu)*const(mu)+n*dmu, val)
    second = add(second, linear([2*n*const(mu)*v[i]+vg_v[i]-rg_r[i]
                                for i in range(3)], grad))
    for i in range(3):
        for j in range(3):
            second = add(second, scale(v[i]*v[j]-r[i]*r[j], hess[i][j]))
    jsq = multiply(jtot, jtot)
    rhs = scale(2, add(multiply(jsq, val), multiply(val, jsq)))
    assert equal(second, rhs), "sandwich second order"
    assert trace(val) == 1
    return {"p": p, "j": str(F(p, 2)), "N": n,
            "matrix_dimension": (p+1)**n,
            "point": [str(z) for z in point],
            "axis": [str(z) for z in axis],
            "normalizer": True, "anticommutator": True,
            "rotation": True, "sandwich_second_order": True,
            "trace_one": True}


def check_aggregate(p, n, point):
    """Check the expanded drift/potential/DC against a rotated physical Q_C."""
    m = [Jet.variable(point[i], i) for i in range(3)]
    rloc, _ = local_kernel(p, m)
    kval = tensor_power(rloc, n)
    val = derivative_matrix(kval, ZERO)
    grad = [derivative_matrix(kval, tuple(int(i == a) for a in range(3)))
            for i in range(3)]
    hess = [[derivative_matrix(kval, tuple(int(i == a)+int(j == a)
             for a in range(3))) for j in range(3)] for i in range(3)]
    xj = sum((mi*mi for mi in m), Jet())
    eta_j = p+2*(1-xj)*fp(p, xj, 1)/fp(p, xj)
    eta_prime_j = (-2*fp(p, xj, 1)/fp(p, xj)
        +2*(1-xj)*(fp(p, xj, 2)/fp(p, xj)
                         -(fp(p, xj, 1)/fp(p, xj))**2))
    x, eta, eta_prime = const(xj), const(eta_j), const(eta_prime_j)
    b = [F(1, 3), F(-1, 5), F(2, 7)]
    axes = [(F(3, 5), F(4, 5), F(0)),
            (F(-4, 5), F(3, 5), F(0)), (F(0), F(0), F(1))]
    lam = [F(1), F(2), F(3)]
    c = [[Q(sum(lam[a]*axes[a][i]*axes[a][j] for a in range(3)))
          for j in range(3)] for i in range(3)]
    mq = list(map(Q, point))
    cm = [scalar_dot(c[i], mq) for i in range(3)]
    mcm = scalar_dot(mq, cm)
    bm = scalar_dot(list(map(Q, b)), mq)
    mm = [[int(i == j)-mq[i]*mq[j] for j in range(3)] for i in range(3)]
    mx, my, mz = mq
    skew = [[Q(), -mz, my], [mz, Q(), -mx], [-my, mx, Q()]]
    dc = add(multiply(multiply(mm, c), mm),
             scale(-1, multiply(multiply(skew, c), transpose(skew))))
    eps = F(1, n*n)
    avec = [(n*eta-1)*eps/2*(cm[i]-mcm*mq[i])
                         +(Q(b[i])-bm*mq[i])/2 for i in range(3)]
    potential = (n*n*eta*eta*mcm+n*eta*trace(c)
                +n*(2*(1-x)*eta_prime-eta)*mcm)*eps/4+n*eta*bm/2
    gval = add(scale(potential, val), linear(avec, grad))
    for i in range(3):
        for j in range(3):
            gval = add(gval, scale(eps*dc[i][j]/4, hess[i][j]))
    h = mat_zero((p+1)**n)
    spin = local_spin(p)
    for weight, axis in zip(lam, axes):
        jt = total_spin(linear(axis, spin), n)
        h = add(h, scale(eps*weight, multiply(jt, jt)))
    h = add(h, total_spin(linear(b, spin), n))
    target = scale(F(1, 2), add(multiply(h, val), multiply(val, h)))
    assert equal(gval, target), "expanded rotated quadratic plus unscaled field"
    assert potential == trace(multiply(h, val)), "physical trace potential"
    return {"p": p, "j": str(F(p, 2)), "N": n,
            "matrix_dimension": (p+1)**n,
            "expanded_generator": True, "trace_potential": True,
            "cross_axis_quadratic": True, "unscaled_field": True}


def main():
    started = time.monotonic()
    point = (F(1, 7), F(-2, 9), F(1, 6))
    axes = [(F(1), F(0), F(0)), (F(3, 5), F(4, 5), F(0)),
            (F(2, 3), F(1, 3), F(2, 3))]
    rows = []
    for p, n in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2), (4, 1)]:
        for axis in axes:
            assert sum(a*a for a in axis) == 1
            rows.append(check_fixture(p, n, point, axis))
    aggregate_rows = [check_aggregate(p, n, point) for p, n in [(2, 2), (3, 1)]]
    elapsed = time.monotonic()-started
    result = {"status": "PASS", "arithmetic": "exact rational complex and Taylor jets",
              "fixture_count": len(rows), "max_matrix_dimension": 16,
              "runtime_seconds": elapsed, "fixtures": rows,
              "aggregate_fixture_count": len(aggregate_rows),
              "aggregate_fixtures": aggregate_rows,
              "scope": "Finite transcription checks, not theorem or novelty validation.",
              "energy": "UNKNOWN", "dependencies": "Python standard library only"}
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ["status", "fixture_count",
                     "max_matrix_dimension", "runtime_seconds"]}))


if __name__ == "__main__":
    main()

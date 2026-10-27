"""Exact algebra, certified-bound evaluation, and legal-query implementation checks.

Only Python's standard library is used. Floating simulations are NOT TV tests.
The proof of the full-law bound is FOUR_QUERY_SCALAR_CORRECTION.md.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from math import atan, comb, cos, exp, log1p, pi, sqrt
from pathlib import Path
from random import Random


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and not p[-1]:
        p.pop()
    return tuple(p)


def padd(p, q):
    a = [F(0)] * max(len(p), len(q))
    for i, v in enumerate(p):
        a[i] += v
    for i, v in enumerate(q):
        a[i] += v
    return trim(a)


def pmul(p, q):
    a = [F(0)] * (len(p) + len(q) - 1)
    for i, v in enumerate(p):
        for j, w in enumerate(q):
            a[i + j] += v * w
    return trim(a)


def pscale(p, c):
    return trim([F(c) * v for v in p])


def pder(p):
    return trim([i * p[i] for i in range(1, len(p))] or [0])


def one_plus_x2(n):
    p = [F(0)] * (2 * n + 1)
    for k in range(n + 1):
        p[2 * k] = F(comb(n, k))
    return tuple(p)


@dataclass(frozen=True)
class Rx:
    """Polynomial numerator divided by (1+x*x)**power."""
    num: tuple
    power: int = 0

    def __post_init__(self):
        object.__setattr__(self, "num", trim(self.num))
        if self.num == (F(0),):
            object.__setattr__(self, "power", 0)

    @staticmethod
    def lift(v):
        return v if isinstance(v, Rx) else Rx((F(v),))

    def __add__(self, other):
        b = Rx.lift(other)
        p = max(self.power, b.power)
        return Rx(padd(pmul(self.num, one_plus_x2(p - self.power)), pmul(b.num, one_plus_x2(p - b.power))), p)

    __radd__ = __add__

    def __neg__(self):
        return Rx(pscale(self.num, -1), self.power)

    def __sub__(self, other):
        return self + -Rx.lift(other)

    def __rsub__(self, other):
        return Rx.lift(other) + -self

    def __mul__(self, other):
        b = Rx.lift(other)
        return Rx(pmul(self.num, b.num), self.power + b.power)

    __rmul__ = __mul__

    def dx(self):
        return Rx(padd(pmul(pder(self.num), (1, 0, 1)), pscale(pmul(self.num, (0, 2)), -self.power)), self.power + 1)

    def zero(self):
        return self.num == (F(0),)


def eclean(e):
    return {k: v for k, v in e.items() if not v.zero()}


def eadd(*es):
    out = {}
    for e in es:
        for key, v in e.items():
            out[key] = out.get(key, Rx((0,))) + v
    return eclean(out)


def escale(e, c):
    return eclean({key: v * c for key, v in e.items()})


def emul(e, f):
    out = {}
    for (l, z), a in e.items():
        for (m, w), b in f.items():
            key = (l + m, z + w)
            out[key] = out.get(key, Rx((0,))) + a * b
    return eclean(out)


def edx(e):
    return eclean({key: v.dx() for key, v in e.items()})


def edz(e):
    return eclean({(l, z - 1): v * z for (l, z), v in e.items() if z})


def exact_identities():
    x = Rx((0, 1))
    k = Rx((0, 1), 1)
    f = Rx((1,)) - Rx((2,), 2)
    assert (x * k - k.dx() - f).zero()
    s = Rx((0, 0, -4), 4)
    t = Rx((0, 0, F(8, 3), 0, -8), 6)
    assert (s + k * f.dx() * F(1, 2)).zero()
    assert (t + k * s.dx() * F(1, 3)).zero()
    assert (s.dx() - Rx((0, -8, 0, 24), 5)).zero()
    assert (s.dx().dx() - Rx((-8, 0, 144, 0, -168), 6)).zero()
    assert (t.dx() - Rx((0, F(16, 3), 0, F(-176, 3), 0, 64), 7)).zero()
    assert (t.dx().dx() - Rx((F(16, 3), 0, F(-736, 3), 0, F(2896, 3), 0, -576), 8)).zero()
    S = {(2, 0): s, (3, 1): t}
    K, h, Z, one = {(1, 0): k}, {(1, 0): f}, {(0, 1): Rx((1,))}, {(0, 0): Rx((1,))}
    X = eadd(h, Z)
    u = eadd(emul(S, X), escale(emul(K, edx(S)), -1), escale(edz(S), -1))
    u_expected = {(2, 1): s, (3, 0): s * f + 2 * t, (3, 2): t, (4, 1): t * f - k * t.dx()}
    assert not eadd(u, escale(u_expected, -1))
    R = emul(K, edx(h))
    E = eadd(R, emul(K, edx(u)), edz(u), emul(S, eadd(one, R)))
    r = k * f.dx()
    B0 = 2 * t * r + k * f * t.dx() - k * k.dx() * t.dx() - k * k * t.dx().dx()
    expected = {(4, 0): -4 * s * s + k * t.dx() - 2 * t * f,
                (4, 2): k * t.dx(), (5, 1): B0}
    assert not eadd(E, escale(expected, -1))
    # Positivity certificates in q=x*x for bounds on s' and s''.
    # (1+q)^10 -16q(1-3q)^2 = (1-3q)^2 + q^2(132-24q+210q^2) + positive tail.
    D = tuple(F(comb(10, j)) for j in range(11))
    lhs = padd(D, (0, -16, 96, -144))
    rhs = (1, -6, 141, -24, 210, 252, 210, 120, 45, 10, 1)
    assert lhs == trim(rhs)
    assert 24**2 - 4 * 132 * 210 < 0
    D6 = tuple(F(comb(6, j)) for j in range(7))
    assert padd(D6, (-1, 18, -21)) == trim((0, 24, -6, 20, 15, 6, 1))
    assert padd(D6, (1, -18, 21)) == trim((2, -12, 36, 20, 15, 6, 1))
    assert 6**2 - 4 * 24 * 20 < 0
    assert 12**2 - 4 * 2 * 36 < 0
    upper_t2 = padd(pscale(tuple(F(comb(8, j)) for j in range(9)), F(13, 2)), (-1, -46, -181, -108))
    assert all(v >= 0 for v in upper_t2)


def certified_bound(lam, a):
    phi0 = 1 / sqrt(2 * pi)
    phi1 = phi0 * exp(-0.5)
    phi3 = phi0 * exp(-1.5)
    s0 = 27 / 64
    L0 = 125 / (27 * sqrt(5))
    D0, Bmax = 7307 / 3072, 539 / 48
    A2 = 3 + 2 * D0 + D0 * D0
    e = lam**4 * sqrt(A2 + lam**2 * Bmax**2)
    U2 = (lam**2 * s0 + (4 / 3) * lam**4)**2 + lam**6 * (s0 + sqrt(11) / 3)**2
    V2 = L0**2 * (lam**6 * (s0**2 + 4) + lam**8 * (1 / 9 + 4))
    r0 = 27 / 32 * lam**2
    C2 = phi1 * log1p(a**-2)
    C3 = (phi0 + 4 * phi3) * (1 / a - atan(1 / a))
    bound = C2 * e + C3 * r0 * sqrt(U2) + phi1 * (U2 + V2) / a**2
    # A lower bound for exactly four independent averaged raw source values.
    # Ef^2=(2/3)E[1/(1+G^2)] >=1/3 by Jensen; |average f|<=1.
    baseline_lower = exp(-0.5) * (1 - cos(1)) * lam**2 / (6 * (1 + a*a) * 4)
    return bound, baseline_lower, U2 + V2


class CountingOracle:
    def __init__(self, lam, offset):
        self.lam, self.offset, self.calls = lam, offset, 0

    def __call__(self, x):
        self.calls += 1
        return self.offset + self.lam * (1 - 2 / (1 + x*x)**2)


def coefficient(x, z, lam):
    q = x*x
    s = -4*q / (1+q)**4
    sp = -8*x*(1-3*q) / (1+q)**5
    t = (8/3)*q*(1-3*q) / (1+q)**6
    tp = (16/3)*x*(1-11*q+12*q*q) / (1+q)**7
    return lam**2*s + lam**3*t*z, lam**2*sp + lam**3*tp*z, lam**3*t


def sample(oracle, lam, a, rng):
    G, Z, Gprime, W = (rng.gauss(0, 1) for _ in range(4))
    q1, q2, q3 = (rng.gauss(0, 1) for _ in range(3))
    rn = sqrt(q1*q1 + q2*q2 + q3*q3)
    U = (1 + q1/rn) / 2 if rn else 0.5
    c1, c2, c3 = (rng.gauss(0, 1) for _ in range(3))
    radius = sqrt(max(0.0, 1-U*U) * (c1*c1+c2*c2+c3*c3))
    hG, hprime = oracle(G), oracle(Gprime)
    hp, hm = oracle(U*G+radius), oracle(U*G-radius)
    Jhat = (hp-hm)/(2*radius) if radius else 0.0
    S, SG, SZ = coefficient(G, Z, lam)
    Uhat = S*(hG-hprime+Z) - SG*Jhat - SZ
    return hG+Z+Uhat+a*W, Uhat


def main():
    exact_identities()
    lines = ["FOUR-QUERY SCALAR CORRECTION: EXACT CHECKS AND IMPLEMENTATION DIAGNOSTIC",
             "PASS: delta k=f; exact S derivatives; u expansion; complete residual E=lambda^4 A+lambda^5 BZ.",
             "PASS: exact positive-polynomial certificates for the rational derivative bounds.",
             "lambda, reserve_a, actual_law_TV_upper_bound, four_raw_average_TV_lower_bound"]
    for lam in (0.1, 0.05, 0.02, 0.01, 0.001):
        upper, lower, _ = certified_bound(lam, 0.5)
        lines.append(f"{lam:g}, 0.5, {upper:.12g}, {lower:.12g}")
    lam, a, offset, n = 0.05, 0.5, 3.0, 60000
    oracle, rng = CountingOracle(lam, offset), Random(27610)
    sum_y = sum_y2 = sum_u = sum_u2 = 0.0
    for _ in range(n):
        before = oracle.calls
        y, u = sample(oracle, lam, a, rng)
        assert oracle.calls - before == 4
        sum_y += y
        sum_y2 += (y-offset)**2
        sum_u += u
        sum_u2 += u*u
    assert oracle.calls == 4*n
    _, _, second_upper = certified_bound(lam, a)
    # Same seeds and changed additive offsets check the algebraic equivariance.
    o1, o2, r1, r2 = CountingOracle(lam, 0), CountingOracle(lam, 10), Random(2710), Random(2710)
    offset_error = max(abs((sample(o2, lam, a, r2)[0] - sample(o1, lam, a, r1)[0]) - 10) for _ in range(1000))
    lines += ["", f"Numerical execution: {n} samples, {oracle.calls} total source queries; exactly 4 on every execution.",
              f"Output empirical mean: {sum_y/n:.12g}; proved mean: {offset:g}.",
              f"Output empirical centered second moment: {sum_y2/n:.12g}; target variance: {1+a*a:g}.",
              f"Correction empirical mean: {sum_u/n:.12g}; proved mean: 0.",
              f"Correction empirical second moment: {sum_u2/n:.12g}; analytical upper bound: {second_upper:.12g}.",
              f"Paired additive-offset implementation error: {offset_error:.12g}.",
              "The floating moments are consistency checks only. No numerical moment, KS, or finite-grid check is treated as TV certification.",
              "The TV upper bounds evaluate the analytical theorem; source/primitive roundoff needs its own budget for finite-bit guarantees.",
              "The exact known source template admits a stronger one-query reference-subtraction sampler; no advantage over that comparator is claimed."]
    output = "\n".join(lines) + "\n"
    Path(__file__).with_name("FOUR_QUERY_CHECK_RESULTS.txt").write_text(output)
    print(output)


if __name__ == "__main__":
    main()

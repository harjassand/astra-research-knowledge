"""Exact checks and legal executions for the universal scalar comparator.

The full-law statement is analytic; empirical moments are not TV tests.
"""

from fractions import Fraction as F
from math import exp, pi, sqrt
from pathlib import Path
from random import Random
from check_four_query_correction import CountingOracle, certified_bound


def padd(*ps):
    out = {}
    for p in ps:
        for key, value in p.items():
            out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}


def pmul(p, q):
    out = {}
    for key, v in p.items():
        for key2, w in q.items():
            k = tuple(a+b for a, b in zip(key, key2))
            out[k] = out.get(k, F(0)) + v*w
    return {key: value for key, value in out.items() if value}


def ppow(p, n):
    out = {(0, 0, 0): F(1)}
    for _ in range(n):
        out = pmul(out, p)
    return out


def gm(n):
    if n % 2:
        return 0
    out = 1
    for j in range(1, n, 2):
        out *= j
    return out


def gaussian_expectation(p):
    return sum(v*gm(k[0])*gm(k[1])*gm(k[2]) for k, v in p.items())


def exact_checks():
    p = {(1, 0, 0): F(1), (0, 1, 0): F(-1)}
    q = {(1, 0, 0): F(1), (0, 0, 1): F(-1)}
    vhat = {key: val/2 for key, val in ppow(p, 2).items()}
    mhat = pmul(ppow(p, 2), q)
    # Any monomial having an independent centered variable to power 1 vanishes.
    surviving_m = {key: val for key, val in mhat.items() if 1 not in key}
    assert surviving_m == {(3, 0, 0): F(1)}
    surviving_v = {key: val for key, val in vhat.items() if 1 not in key}
    assert surviving_v == {(2, 0, 0): F(1, 2), (0, 2, 0): F(1, 2)}
    assert gaussian_expectation(ppow(p, 4)) == 12
    assert gaussian_expectation(pmul(ppow(p, 4), ppow(q, 2))) == 48
    assert gaussian_expectation(ppow(vhat, 2)) == 3
    assert gaussian_expectation(ppow(mhat, 2)) == 48


def bound(ell, a):
    phi = lambda x: exp(-x*x/2)/sqrt(2*pi)
    rm, rp = sqrt(3-sqrt(6)), sqrt(3+sqrt(6))
    D4 = 2*sqrt(6)*(rm*phi(rm)+rp*phi(rp))
    assert D4 <= sqrt(6)
    c4 = 19*D4/(24*(1+a*a)**2)+3*phi(1)/(4*a*a)
    c6 = 8*phi(1)/(3*a*a)
    return min(1.0, c4*ell**4+c6*ell**6), D4, c4, c6


def sample(oracle, a, rng):
    values = [oracle(rng.gauss(0, 1)) for _ in range(4)]
    Z, W = rng.gauss(0, 1), rng.gauss(0, 1)
    d12, d13 = values[1]-values[2], values[1]-values[3]
    vhat, mhat = d12*d12/2, d12*d12*d13
    correction = -vhat*Z/2-mhat*(Z*Z-1)/6
    return values[0]+Z+correction+a*W, correction


def main():
    exact_checks()
    _, D4, c4, c6 = bound(0.1, 0.5)
    lines = ["UNIVERSAL FOUR-VALUE SCALAR POSITIVE COMPARATOR",
             "PASS: exact coefficient expectations v and centered third moment.",
             "PASS: exact Gaussian difference moments 12 and 48, and coefficient second moments 3 and 48.",
             f"D4 = {D4:.12g}.",
             f"At reserve a=0.5, the proved TV bound is {c4:.12g} ell^4 + {c6:.12g} ell^6, clipped at one.",
             "ell, TV upper bound"]
    for ell in (0.2, 0.1, 0.05, 0.02, 0.01):
        lines.append(f"{ell:g}, {bound(ell, 0.5)[0]:.12g}")
    L0 = 125/(27*sqrt(5))
    lines += ["", "Rational source test family: lambda, universal TV upper bound, four-raw-average TV lower bound"]
    for lam in (0.05, 0.02, 0.01, 0.005):
        _, lower, _ = certified_bound(lam, 0.5)
        lines.append(f"{lam:g}, {bound(lam*L0, 0.5)[0]:.12g}, {lower:.12g}")
    n, lam, a, offset = 60000, 0.05, 0.5, 3.0
    oracle, rng = CountingOracle(lam, offset), Random(76210)
    sum_y = sum_centered2 = sum_u = sum_u2 = 0.0
    for _ in range(n):
        before = oracle.calls
        y, u = sample(oracle, a, rng)
        assert oracle.calls-before == 4
        sum_y += y
        sum_centered2 += (y-offset)**2
        sum_u += u
        sum_u2 += u*u
    assert oracle.calls == 4*n
    ell = lam*L0
    upper_u2 = (3/4)*ell**4+(8/3)*ell**6
    lines += ["", f"Executed {n} samples with {oracle.calls} source queries; exactly 4 on each execution.",
              f"Empirical mean {sum_y/n:.12g}; proved mean {offset:g}.",
              f"Empirical centered second moment {sum_centered2/n:.12g}; target variance {1+a*a:g}.",
              f"Correction empirical mean {sum_u/n:.12g}; proved mean zero.",
              f"Correction empirical second moment {sum_u2/n:.12g}; proved bound {upper_u2:.12g}.",
              "No S coefficient, mean, derivative, K action, or conditional mean was supplied.",
              "Moments are implementation diagnostics only; the full-law result follows from the proved uniform remainder bound.",
              "The direct vector covariance version has second-moment budget ell^4*d*(d+2)/4 even for g(x)=ell*x; no high-dimensional target theorem follows.",
              "For the exact known rational family, one-query reference subtraction is still a stronger alternative."]
    output = "\n".join(lines)+"\n"
    Path(__file__).with_name("UNIVERSAL_SCALAR_CHECK_RESULTS.txt").write_text(output)
    print(output)


if __name__ == "__main__":
    main()

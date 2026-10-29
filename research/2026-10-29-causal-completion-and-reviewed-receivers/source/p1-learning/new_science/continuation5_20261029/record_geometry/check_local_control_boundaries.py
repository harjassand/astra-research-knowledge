#!/usr/bin/env python3
"""Exact synthetic checks; no sampled physical data or precision claim."""
from fractions import Fraction as F
from itertools import product
from math import cosh, exp, sqrt
from pathlib import Path
import hashlib
import json


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def eye(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = F(1)
    return a


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def mpow(a, n):
    out = eye(len(a))
    while n:
        if n & 1:
            out = mm(out, a)
        a = mm(a, a)
        n //= 2
    return out


def tr(a):
    return sum(a[i][i] for i in range(len(a)))


def dualmul(a, b):
    x, dx = a
    y, dy = b
    return mm(x, y), add(mm(dx, y), mm(x, dy))


def dualpow(a, da, n):
    out, base = (eye(len(a)), zero(len(a))), (a, da)
    while n:
        if n & 1:
            out = dualmul(out, base)
        base = dualmul(base, base)
        n //= 2
    return out


def reversible(p, mu):
    assert sum(mu) == 1
    for i, row in enumerate(p):
        assert min(row) >= 0 and sum(row) == 1
        assert sum(mu[j]*p[j][i] for j in range(len(p))) == mu[i]
        for j in range(len(p)):
            assert mu[i]*p[i][j] == mu[j]*p[j][i]


def slow_hidden():
    states = list(product((-1, 1), repeat=2))
    index = {s: i for i, s in enumerate(states)}
    out = []
    for m in (2, 4, 8, 16, 32, 64, 128, 256):
        delta = F(1, 2*m)
        p = zero(4)
        for i, (y, h) in enumerate(states):
            flip = delta*(1+F(h, 2))
            p[i][i], p[i][index[-y, h]] = 1-flip, flip
        reversible(p, [F(1, 4)]*4)
        p2, residual = mm(p, p), F(0)
        for b in (-1, 1):
            d = sum(F(1, 4)*p2[i][j]
                    for i, (y, h) in enumerate(states) if y == b
                    for j, (z, g) in enumerate(states) if z == b)
            proj = F(0)
            for a in (-1, 1):
                k = sum(F(1, 4)*p[i][j]
                        for i, (y, h) in enumerate(states) if y == a
                        for j, (z, g) in enumerate(states) if z == b)
                proj += k*k/F(1, 2)
            residual += d-proj
        assert residual == delta*delta/2
        pn = mpow(p, m)
        corr = sum(F(1, 4)*y*z*pn[i][j]
                   for i, (y, h) in enumerate(states)
                   for j, (z, g) in enumerate(states))
        assert corr == ((1-delta)**m+(1-3*delta)**m)/2
        tv = abs(corr-(1-2*delta)**m)/2
        assert tv > F(1, 50)
        out.append({"calls": m, "epsilon_squared": str(residual),
                    "epsilon": sqrt(float(residual)), "joint_tv": float(tv)})
    return {"cases": out, "limiting_joint_tv": exp(-1)*(cosh(.5)-1)/2}


def rare_selection():
    out = []
    for m in (4, 8, 16, 32):
        q, n = F(1, m), m*m
        length = 2*(n-1).bit_length()
        a = q+(1-q)*F(1, 2**length)
        b = (1-q)*F(1, 2**length)
        exact_tv = (1-(1-a)**n)*((1-q)-b/a)/2
        lower = (1-q)/2*(1-(1-q)**n-F(n, 2**length))
        assert 0 < lower <= exact_tv <= F(1, 2)
        assert F(n, 2**length) <= F(1, n)
        out.append({"q": str(q), "sites": n, "calls_per_site": length,
                    "total_calibration_calls": n*length,
                    "epsilon_squared": str(q*(1-q)/2),
                    "exact_joint_tv": float(exact_tv), "lower_bound": float(lower)})
    q, n, length = F(1, 3), 3, 2
    probs = [q, (1-q)*F(1, 2**length), (1-q)*(1-F(1, 2**length))]
    actual = ref = F(0)
    for cats in product(range(3), repeat=n):
        w = F(1)
        for c in cats:
            w *= probs[c]
        first = next((c for c in cats if c != 2), None)
        if first is not None:
            ref += w*(1-q)/2
            actual += w*(F(1, 2) if first == 1 else 0)
    a = probs[0]+probs[1]
    assert ref-actual == (1-(1-a)**n)*((1-q)-probs[1]/a)/2
    return {"cases": out, "exhaustive_category_cases": 27,
            "small_exact_tv": str(ref-actual)}


def weight(s, q, r):
    return q**sum(s[i] != s[(i+1) % len(s)] for i in range(len(s)))*r**sum(s)


def partition(n, q, r):
    a, da = [[F(1), q*r], [q, r]], [[F(0), q], [F(0), F(1)]]
    an, dan = dualpow(a, da, n)
    z = tr(an)
    return z, F(2, n)*r*tr(dan)/z-1, 1-(1+r**n)/z


def ring():
    out = []
    for n in (3, 4, 6, 8, 16, 32, 64, 128):
        q, r = F(1, n*n), F(n+1, n)
        z, mean, nonconstant = partition(n, q, r)
        assert partition(n, q, F(1))[1] == 0
        cm = (r**n-1)/(r**n+1)
        assert abs(mean-cm) <= 2*nonconstant
        errors = [r*u/(1+r*u)-u/(1+u) for u in (F(1, n**4), F(1), F(n**4))]
        row_tv = F(1, 2*(2*n+1))
        assert max(errors) == row_tv
        assert nonconstant <= 2*r**n/(1+r**n)*((1+q)**n-1-n*q)
        if n <= 8:
            states = list(product((0, 1), repeat=n))
            weights = [weight(s, q, r) for s in states]
            assert sum(weights) == z
            assert sum(w*(F(2*sum(s), n)-1) for s, w in zip(states, weights))/z == mean
        out.append({"sites": n, "row_tv": str(row_tv), "row_tv_decimal": float(row_tv),
                    "stationary_local_spin_error": float(mean),
                    "constant_configuration_mean": float(cm),
                    "nonconstant_probability": float(nonconstant)})
    n, q = 4, F(1, 16)
    states = list(product((0, 1), repeat=n))
    idx = {s: i for i, s in enumerate(states)}
    for r in (F(1), F(5, 4)):
        ws = [weight(s, q, r) for s in states]
        mu = [w/sum(ws) for w in ws]
        p = zero(len(states))
        for si, s in enumerate(states):
            for i in range(n):
                s0, s1 = list(s), list(s)
                s0[i], s1[i] = 0, 1
                s0, s1 = tuple(s0), tuple(s1)
                w0, w1 = weight(s0, q, r), weight(s1, q, r)
                p[si][idx[s0]] += w0/(n*(w0+w1))
                p[si][idx[s1]] += w1/(n*(w0+w1))
        reversible(p, mu)
    return {"cases": out, "heat_bath_contexts_checked": 128,
            "limiting_local_spin_error": (exp(1)-1)/(exp(1)+1)}


def moment_supplier():
    """Exact path moments and serial covariance after the independent bath."""
    gs, bath = [F(1, 4), F(3, 4)], [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]
    states = list(product((0, 1), repeat=2))  # (hidden index, visible value)
    idx = {s: i for i, s in enumerate(states)}
    cases, total_cov_checks, conditional_checks = [], 0, 0
    for p in (F(1, 4), F(1, 3), F(1, 2), F(3, 4)):
        transition, scores = zero(4), [zero(4), zero(4)]
        mu = [(p if y else 1-p)/2 for h, y in states]
        for si, (h, y0) in enumerate(states):
            means = [F(0), F(0)]
            for f1, f2 in product((0, 1), repeat=2):
                y1, y2 = y0 ^ f1, y0 ^ f1 ^ f2
                q1, q2 = (p if y0 == 0 else 1-p), (p if y1 == 0 else 1-p)
                prob1 = gs[h]*q1 if f1 else 1-gs[h]*q1
                prob2 = gs[h]*q2 if f2 else 1-gs[h]*q2
                prob = prob1*prob2
                z = [F(f1)/q1, F(f1*f2)/(p*(1-p))]
                for a in range(2):
                    means[a] += prob*z[a]
                for hp in (0, 1):
                    sj, w = idx[hp, y2], prob*bath[h][hp]
                    transition[si][sj] += w
                    for a in range(2):
                        scores[a][si][sj] += w*z[a]
            assert means == [gs[h], gs[h]**2]
            conditional_checks += 2
        assert all(sum(row) == 1 for row in transition)
        assert all(sum(mu[i]*transition[i][j] for i in range(4)) == mu[j] for j in range(4))
        for a in range(2):
            vals = [g**(a+1) for g in gs]
            mean = sum(vals)/2
            var = sum((v-mean)**2 for v in vals)/2
            for lag in range(1, 7):
                weighted = mm(mm(scores[a], mpow(transition, lag-1)), scores[a])
                product_mean = sum(mu[i]*sum(weighted[i]) for i in range(4))
                assert product_mean-mean*mean == var*F(1, 2)**lag
                total_cov_checks += 1
        cases.append({"p": str(p), "mean_mobility": "1/2", "mobility_variance": "1/16",
                      "bath_nonconstant_eigenvalue": "1/2"})
    return {"cases": cases, "conditional_moment_checks": conditional_checks,
            "serial_covariance_checks": total_cov_checks}


def main():
    result = {"status": "all exact Fraction assertions passed",
              "scope": "population models, not acquired experimental data",
              "slow_hidden": slow_hidden(), "rare_selection": rare_selection(),
              "finite_range_phase": ring(), "local_mobility_supplier": moment_supplier(),
              "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = Path(__file__).with_name("LOCAL_CONTROL_BOUNDARY_CHECKS.json")
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "report": str(out),
                      "largest_ring": result["finite_range_phase"]["cases"][-1],
                      "largest_selection": result["rare_selection"]["cases"][-1],
                      "supplier_checks": result["local_mobility_supplier"]}, indent=2))


if __name__ == "__main__":
    main()

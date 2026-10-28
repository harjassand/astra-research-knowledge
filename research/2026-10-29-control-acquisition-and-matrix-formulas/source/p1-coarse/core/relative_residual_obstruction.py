"""Exact obstruction to a gap-free switched relative-residual certificate.

All proof obligations use rational arithmetic. Very long word powers are
bounded analytically, not simulated and rounded into a certificate.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json


def tr(a):
    return [list(x) for x in zip(*a)]


def mm(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in tr(b)] for row in a]


def add(a, b, sign=1):
    return [[x+sign*y for x, y in zip(row, other)]
            for row, other in zip(a, b)]


def scale(a, z):
    return [[z*x for x in row] for row in a]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def outer(v):
    return [[x*y for y in v] for x in v]


def psd2(a):
    return (a[0][1] == a[1][0] and a[0][0] >= 0 and a[1][1] >= 0
            and a[0][0]*a[1][1] >= a[0][1]**2)


def encode(x):
    if isinstance(x, F):
        return {"exact": str(x), "decimal": float(x)}
    if isinstance(x, list):
        return [encode(y) for y in x]
    if isinstance(x, dict):
        return {k: encode(v) for k, v in x.items()}
    return x


def fixture(epsilon):
    delta, eta = epsilon**2, epsilon**10
    s = 1+delta**2+epsilon**2
    us = [[delta, F(1), epsilon], [-delta, F(1), -epsilon]]
    aa = [add(eye(3), scale(outer(u), 1/s), -1) for u in us]
    v = [[F(1), F(0)], [F(0), F(1)], [F(0), epsilon]]
    w = mm(tr(v), v)
    winv = [[F(1), F(0)], [F(0), 1/(1+epsilon**2)]]
    tt = [mm(winv, mm(tr(v), mm(a, v))) for a in aa]
    ee = []
    for a, t in zip(aa, tt):
        assert a == tr(a) and mm(a, a) == a
        d = add(mm(a, v), mm(v, t), -1)
        ee.append(mm(tr(d), d))
        assert mm(w, t) == mm(tr(t), w)
    assert ee[0] == [[F(0), F(0)], [F(0), F(0)]]
    kappa2 = 4*epsilon**2/((1+epsilon**2)*delta**2+(1-epsilon**2)**2)
    kminus = add(eye(2), tt[1], -1)
    assert ee[1] == scale(mm(tr(kminus), mm(w, kminus)), kappa2)

    # S is the span of the actually reachable words empty and plus.
    native = [[F(1), aa[0][0][0]], [F(0), aa[0][1][0]],
              [F(0), aa[0][2][0]]]
    change = [[F(1), (1+epsilon**2)/delta], [F(0), -s/delta]]
    assert mm(native, change) == v

    cycle = mm(tt[1], tt[0])
    chi = 4*delta**2/((1+epsilon**2)*s**2)
    lam = 1-chi
    assert F(0) < lam < F(1)
    assert mm(cycle, cycle) == scale(cycle, lam)
    h_cycles = (F(10)/chi).__ceil__()+1
    assert chi*(h_cycles-1) >= 10
    # (1-chi)^(H-1) <= exp(-10) < 1/20000, rigorously.
    assert sum((F(10**n, factorial(n)) for n in range(40)), F(0)) > 20000
    reduced_upper = F(1, 20000)

    fixed = [[epsilon], [F(0)], [-delta]]
    assert all(mm(a, fixed) == fixed for a in aa)
    true_allword_lower = (epsilon**2-delta**2)/(epsilon**2+delta**2)

    # Remove every exact common fixed vector by a strictly positive damping.
    # The same relative inequality survives, not necessarily as equality.
    scaled = [scale(a, 1-eta) for a in aa]
    scaled_t = [scale(t, 1-eta) for t in tt]
    for a, t, e in zip(scaled, scaled_t, ee):
        d = add(mm(a, v), mm(v, t), -1)
        es = mm(tr(d), d)
        assert es == scale(e, (1-eta)**2)
        k = add(eye(2), t, -1)
        assert psd2(add(scale(mm(tr(k), mm(w, k)), kappa2), es, -1))
    primitive_length = 2*h_cycles
    assert primitive_length*eta < 1
    scaled_true_lower = (1-primitive_length*eta)*true_allword_lower
    gap_lower = scaled_true_lower-reduced_upper
    assert gap_lower > 0
    return {
        "epsilon": epsilon, "delta": delta, "eta": eta,
        "positive_projection_primitives": aa,
        "strictly_contracting_primitives": scaled,
        "reachable_dictionary": [[], [0]], "basis_change": change,
        "computational_metric": w, "coefficient_maps": tt,
        "relative_defect_coefficient_squared": kappa2,
        "reduced_cycle_eigenvalue": lam,
        "cycles": h_cycles, "primitive_word_length": primitive_length,
        "reduced_word_amplitude_upper": reduced_upper,
        "scaled_true_word_amplitude_lower": scaled_true_lower,
        "true_minus_reduced_gap_lower": gap_lower,
        "exact_checks_passed": True,
        "scope": "Galerkin maps have F=0, so signed correction is zero."
    }


def main():
    result = {"claim": "Relative per-operation residuals alone do not give a uniform switched-word approximation.",
              "proof_arithmetic": "exact rational identities and elementary analytic power bounds",
              "fixtures": [fixture(F(1, d)) for d in [4, 8, 16, 32, 64]]}
    out = Path(__file__).resolve().parents[1]/"results"/"RELATIVE_RESIDUAL_OBSTRUCTION.json"
    out.write_text(json.dumps(encode(result), indent=2)+"\n")
    for f in result["fixtures"]:
        print({"epsilon": float(f["epsilon"]),
               "relative_defect_squared": float(f["relative_defect_coefficient_squared"]),
               "word_length": f["primitive_word_length"],
               "gap_lower": float(f["true_minus_reduced_gap_lower"]),
               "exact_checks": f["exact_checks_passed"]})


if __name__ == "__main__":
    main()

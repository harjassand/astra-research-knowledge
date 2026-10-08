"""Exact-field d=5 repair and interval audit of the stored EB comparator.

Run from the repository root with
  PYTHONPATH=work/agents/weyl_compatible_lift/vendor python3 \
    work/agents/weyl_compatible_lift/scripts/d5_exact_repair_audit.py

The target channel and its self-compatibility witness are exact over Q(sqrt(5)).
For the EB comparator, the decimal coordinates/weights in the saved six-state
fixture are interpreted as exact decimal rationals; interval arithmetic checks
the resulting exact separable construction against all 24 nonidentity modes.
"""
from __future__ import annotations

import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import sympy as sp


ROOT = Path(__file__).resolve().parents[5]
EB_FIXTURE = ROOT / "work/agents/weyl_compatible_lift/d5_eb_comparator.json"


def exact_target():
    r = sp.sqrt(5)
    c1, c2 = (r - 1) / 4, -(r + 1) / 4
    x0 = (23 - 2 * r) / 25
    x1 = (75 - 16 * r) / 500
    x2, x3, x4 = sp.Rational(3, 20), sp.Rational(9, 100), sp.Rational(1, 4)
    N = sp.simplify(x0**2 + 10 * x1**2 + 10 * x2**2 + 2 * x3**2 + 2 * x4**2)

    # The five equations are precisely the Fourier-transform conditions on
    # the five symmetry classes of the vector v.
    ysum = x0 + 2 * x3 + 2 * x4
    equations = [
        (x0 + 2 * x3 * c1 + 2 * x4 * c2) / 5 - x1,
        (x0 + 2 * x3 * c2 + 2 * x4 * c1) / 5 - x2,
        ysum / 5 + 2 * x1 + 2 * x2 - x0,
        ysum / 5 + 2 * x1 * c1 + 2 * x2 * c2 - x3,
        ysum / 5 + 2 * x1 * c2 + 2 * x2 * c1 - x4,
    ]
    assert all(sp.simplify(e) == 0 for e in equations)

    # Weyl eigenvalues lambda_(u,v), with S((a,b),(u,v))=av-bu.
    d0, d1, d2 = x0**2 - x2**2, x3**2 - x2**2, x4**2 - x2**2
    lam_v1 = sp.simplify((d0 + 2 * d1 * c1 + 2 * d2 * c2) / N)
    lam_v2 = sp.simplify((d0 + 2 * d1 * c2 + 2 * d2 * c1) / N)
    lam_u1 = sp.simplify((d0 + 2 * d1 + 2 * d2 + 10 * (x1**2 - x2**2) * c1) / N)
    lam_u2 = sp.simplify((d0 + 2 * d1 + 2 * d2 + 10 * (x1**2 - x2**2) * c2) / N)
    expected = [
        (sp.Integer(13_376_451) - 752_320 * r) / 25_213_768,
        (sp.Integer(14_203_331) + 281_824 * r) / 25_213_768,
        (sp.Integer(13_041_363) + 255_168 * r) / 25_213_768,
        (sp.Integer(17_214_643) + 498_112 * r) / 25_213_768,
    ]
    assert all(sp.simplify(a - b) == 0 for a, b in zip(
        [lam_v1, lam_v2, lam_u1, lam_u2], expected))
    return {
        "sqrt5": r,
        "c1": c1,
        "c2": c2,
        "x": (x0, x1, x2, x3, x4),
        "N": N,
        "lambdas": (lam_v1, lam_v2, lam_u1, lam_u2),
    }


def interval_fraction(q: Fraction):
    return mp.iv.mpf(q.numerator) / q.denominator


def eb_comparator_gaps(target):
    # Preserve the fixture's decimal spellings and interpret every decimal as
    # an exact rational. Re-normalize positive weights exactly to sum to one.
    fixture = json.loads(EB_FIXTURE.read_text(), parse_float=Decimal)
    weights = [Fraction(x) for x in fixture["weights_normalized_to_sum_one"]]
    total_w = sum(weights)
    weights = [w / total_w for w in weights]

    states = []
    for ket in fixture["product_kets"]:
        z = [(Fraction(a), Fraction(b)) for a, b in ket]
        norm2 = sum(a * a + b * b for a, b in z)
        assert norm2 > 0
        states.append((z, norm2))

    mp.iv.dps = 80
    iv = mp.iv
    sqrt5 = iv.sqrt(5)
    c1, c2 = (sqrt5 - 1) / 4, -(sqrt5 + 1) / 4
    x0, x1 = (23 - 2 * sqrt5) / 25, (75 - 16 * sqrt5) / 500
    x2, x3, x4 = iv.mpf(3) / 20, iv.mpf(9) / 100, iv.mpf(1) / 4
    N = x0*x0 + 10*x1*x1 + 10*x2*x2 + 2*x3*x3 + 2*x4*x4
    d0, d1, d2 = x0*x0 - x2*x2, x3*x3 - x2*x2, x4*x4 - x2*x2
    lam_v1 = (d0 + 2*d1*c1 + 2*d2*c2) / N
    lam_v2 = (d0 + 2*d1*c2 + 2*d2*c1) / N
    lam_u1 = (d0 + 2*d1 + 2*d2 + 10*(x1*x1 - x2*x2)*c1) / N
    lam_u2 = (d0 + 2*d1 + 2*d2 + 10*(x1*x1 - x2*x2)*c2) / N

    # For the Weyl twirl of |psi><psi| tensor |conj(psi)><conj(psi)|,
    # the random-Weyl multiplier at (u,v) is
    #   |sum_j conj(psi[j+u]) omega^(-v*j) psi[j]|^2.
    # This is also directly obtained by Fourier transforming the Bell weights.
    trig_cos = [[iv.cos(2 * iv.pi * k*j / 5) for j in range(5)] for k in range(5)]
    trig_sin = [[iv.sin(2 * iv.pi * k*j / 5) for j in range(5)] for k in range(5)]
    all_gaps, clipped_gaps, comparator_modes = [], [], []
    for u in range(5):
        for v in range(5):
            if (u, v) == (0, 0):
                continue
            mu = iv.mpf(0)
            for w, (z, norm2) in zip(weights, states):
                real, imag = iv.mpf(0), iv.mpf(0)
                for j in range(5):
                    ar, ai = z[(j + u) % 5]
                    br, bi = z[j]
                    # conj(z[j+u]) * z[j] = cr + i ci
                    cr, ci = ar*br + ai*bi, ar*bi - ai*br
                    cc, ss = trig_cos[v][j], trig_sin[v][j]
                    real += interval_fraction(cr)*cc + interval_fraction(ci)*ss
                    imag += interval_fraction(ci)*cc - interval_fraction(cr)*ss
                real, imag = real / interval_fraction(norm2), imag / interval_fraction(norm2)
                mu += interval_fraction(w) * (real*real + imag*imag)

            if v != 0:
                lam = lam_v1 if v in (1, 4) else lam_v2
            else:
                lam = lam_u1 if u in (1, 4) else lam_u2
            gap = mu - (2*lam - 1)
            clipped_gap = mu - max(2*lam - 1, iv.mpf(0))
            all_gaps.append(((u, v), gap))
            clipped_gaps.append(((u, v), clipped_gap))
            comparator_modes.append(((u, v), mu))

    min_all = min(all_gaps, key=lambda pair: float(pair[1].a))
    min_clipped = min(clipped_gaps, key=lambda pair: float(pair[1].a))
    min_mu = min(comparator_modes, key=lambda pair: float(pair[1].a))
    assert float(min_all[1].a) > 0.02
    assert float(min_clipped[1].a) > 0.01
    return min_all, min_clipped, min_mu, weights


def main():
    target = exact_target()
    r = target["sqrt5"]
    print("exact x =", target["x"])
    print("exact N =", sp.radsimp(target["N"]))
    print("exact nonidentity lambda classes =")
    for lam in target["lambdas"]:
        print(" ", sp.radsimp(lam), "≈", sp.N(lam, 16))
    # Six projective lines: one horizontal line peaks at lambda_(2,0), while
    # each of the other five peaks at any mode with v=±2.
    budget = sp.radsimp(2*target["lambdas"][3] - 1 +
                        5*(2*target["lambdas"][1] - 1))
    print("exact selected line-cover budget =", budget, "≈", sp.N(budget, 16))
    # The exact expression is (6294997 + 953616*sqrt(5))/6303442;
    # strict excess over one is equivalent to 953616*sqrt(5) > 8445.
    assert 953_616**2 * 5 > 8_445**2

    min_all, min_clipped, min_mu, weights = eb_comparator_gaps(target)
    print("exact decimal-rational EB weights sum =", sum(weights))
    print("min direct-order gap mu-(2 lambda-1) at", min_all[0], "=", min_all[1])
    print("min clipped gap mu-(2 lambda-1)_+ at", min_clipped[0], "=", min_clipped[1])
    print("minimum nonidentity EB eigenvalue at", min_mu[0], "=", min_mu[1])
    print("all 24 mode inequalities have rigorous interval lower bounds > 0")


if __name__ == "__main__":
    main()

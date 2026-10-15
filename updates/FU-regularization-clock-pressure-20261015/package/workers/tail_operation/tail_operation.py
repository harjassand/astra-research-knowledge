#!/usr/bin/env python3
"""Independent rare-tail calculations. No incoming ZIP or physical rates replayed.

Run with Python and mpmath. Writes results.json and exact_certificate.json beside
this file. Fraction/SymPy checks are exact; decimal evaluations are diagnostics.
No Monte Carlo timing or physical capability claim is made.
"""

from __future__ import annotations

import json
import math
import platform
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
import sympy as sp

OUT = Path(__file__).resolve().parent
mp.mp.dps = 90


def dec(x, digits=28):
    return mp.nstr(x, digits)


def survival(M, p, t):
    C = p * M / (M - 1)
    return (1 - C) * mp.exp(-t) + C * mp.exp(-t / M)


def mgf(M, p, theta):
    return (1 - p + p / (1 - M * theta)) / (1 - theta)


def tilted_tail_integral(M, p, theta, t):
    C = p * M / (M - 1)
    return ((1 - C) * mp.exp(-(1 + theta) * t) / (1 + theta)
            + C * mp.exp(-(1 / M + theta) * t) / (1 + M * theta))


def relative_second_moment(M, p, c):
    theta = c / M
    S = survival(M, p, M)
    return mgf(M, p, theta) * tilted_tail_integral(M, p, theta, M) / S**2


def golden_min(fn, a, b, iterations=250):
    """Numerical minimization only. The uniform theorem does not rely on it."""
    ratio = (mp.sqrt(5) - 1) / 2
    left, right = b - ratio * (b - a), a + ratio * (b - a)
    fl, fr = fn(left), fn(right)
    for _ in range(iterations):
        if fl < fr:
            b, right, fr = right, left, fl
            left = b - ratio * (b - a)
            fl = fn(left)
        else:
            a, left, fl = left, right, fr
            right = a + ratio * (b - a)
            fr = fn(right)
    center = (a + b) / 2
    return center, fn(center)


def exact_checks():
    M, p, z = sp.symbols("M p z", positive=True)
    A = sp.Matrix([[-1, p], [0, -1 / M]])
    one = sp.ones(2, 1)
    row = sp.Matrix([[1, 0]])
    C = p * M / (M - 1)
    survival_resolvent = (row * (z * sp.eye(2) - A).inv() * one)[0]
    expected_resolvent = (1 - C) / (z + 1) + C / (z + 1 / M)
    assert sp.factor(survival_resolvent - expected_resolvent) == 0
    laplace_passage = 1 - z * survival_resolvent
    excursion_transform = (1 - p + p / (1 + M * z)) / (1 + z)
    assert sp.factor(laplace_passage - excursion_transform) == 0
    theta = sp.symbols("theta", real=True)
    mgf_from_excursion = excursion_transform.subs(z, -theta)
    assert sp.factor(mgf_from_excursion - (1 - p + p / (1 - M * theta)) / (1 - theta)) == 0

    # e is rigorously enclosed using the nonnegative series and a geometric tail.
    K = 24
    e_lo = sum((F(1, math.factorial(k)) for k in range(K + 1)), F(0))
    next_term = F(1, math.factorial(K + 1))
    e_hi = e_lo + next_term / (1 - F(1, K + 2))
    assert F(2) < e_lo < e_hi < F(3)

    # For integer M >= 16: r_M <= 3 M^3 / 2^M <= 3/16.
    # Monotonicity follows from ((M+1)/M)^3 / 2 <= (17/16)^3/2 < 1.
    ratio_max = F(17, 16)**3 / 2
    r_max = F(3 * 16**3, 2**16)
    constant = (1 - F(1, 16**3)) * F(15, 17) / (2 * (1 + r_max)**2)
    assert ratio_max < 1
    assert r_max == F(3, 16)
    assert constant > F(1, 4)

    # The same exact e enclosure supplies an actual relative decision interval.
    decisions = []
    for mint in (16, 32, 100, 1000):
        p_exact = F(1, mint**3)
        c_exact = p_exact * F(mint, mint - 1)
        lo = c_exact / e_hi
        hi = c_exact / e_lo + (1 - c_exact) / 2**mint
        assert lo > p_exact / 3
        assert hi < p_exact / 2
        decisions.append({
            "M": mint,
            "p": str(p_exact),
            "lower": str(lo),
            "upper": str(hi),
            "verified_decision": "p/3 < S(M) < p/2",
            "tail_bound": "e^(-M) < 2^(-M)",
        })

    return {
        "arithmetic_scope": "Exact Fraction and SymPy identities; no rate-model acquisition",
        "symbolic_checks": ["killed resolvent equals two-mode survival resolvent",
                            "passage Laplace transform equals exact excursion transform",
                            "moment generating function equals transform at -theta"],
        "e_enclosure": {"series_degree": K, "lower": str(e_lo), "upper": str(e_hi)},
        "all_integer_M_ge_16_uniform_bound": {
            "claim": "Every finite-second-moment scalar time tilt has R_theta >= M^3/4",
            "monotonicity_ratio_max": str(ratio_max),
            "r_max": str(r_max),
            "proved_p_times_R_lower": str(constant),
            "target_p_times_R_lower": "1/4",
            "verified": True,
        },
        "relative_survival_decisions": decisions,
    }


def main():
    cert = exact_checks()
    cases = []
    for mint in (4, 8, 10, 16, 32, 100, 1000, 10**6):
        M = mp.mpf(mint)
        p = M**-3
        C = p * M / (M - 1)
        S = survival(M, p, M)
        pg = mp.exp(-M / (1 + p * M))
        exact_uniform_bound = (1 - p) * C * mp.exp(-2) / (2 * (1 + 1 / M) * S**2)
        c_star, r_star = golden_min(lambda c: relative_second_moment(M, p, c),
                                   mp.mpf("-0.999999"), 1 - mp.mpf("1e-70"))
        sharp_c = 1 - mp.sqrt(p)
        sharp_r = relative_second_moment(M, p, sharp_c)
        q = (M * mp.exp(-1) - mp.exp(-M)) / (M - 1)
        branch_cv2 = p**2 * q * (1 - q) / S**2
        assert r_star >= exact_uniform_bound * (1 - mp.mpf("1e-65"))
        assert branch_cv2 <= mp.e - 1
        # Independent mpmath matrix-exponential check on the smallest cases.
        # This is high precision agreement, not an interval certificate.
        expm_error = None
        if mint <= 1000:
            A = mp.matrix([[-1, p], [0, -1 / M]])
            v = mp.expm(A * M) * mp.matrix([1, 1])
            expm_error = abs(v[0] / S - 1)
            assert expm_error < mp.mpf("1e-70")
        cases.append({
            "M": mint, "p": dec(p), "deadline": mint,
            "survival": dec(S), "pGT_survival": dec(pg),
            "pGT_relative_error": dec(1 - pg / S),
            "pGT_log_survival_ratio": dec(-M / (1 + p * M) - mp.log(S)),
            "pGT_W2_squared": dec(2 * p * M**2),
            "naive_relative_second_moment": dec(1 / S),
            "uniform_R_lower": dec(exact_uniform_bound),
            "uniform_p_times_R_lower": dec(p * exact_uniform_bound),
            "numerical_optimum_c_Mtheta": dec(c_star),
            "numerical_optimum_p_times_R": dec(p * r_star),
            "constructive_sharp_tilt_c": dec(sharp_c),
            "constructive_sharp_tilt_p_times_R": dec(p * sharp_r),
            "branch_conditioned_relative_variance": dec(branch_cv2),
            "matrix_exp_relative_discrepancy": dec(expm_error) if expm_error is not None else None,
            "numerical_scope": "Diagnostic high-precision calculations; no timings or physical inputs",
        })

    result = {
        "status": "DECISIVE_FAILURE_OF_SCALAR_TIME_TILT; NO_NEW_SCIENTIFIC_CAPABILITY",
        "source_zip_replayed": False,
        "primary_LJ38_data_acquired": False,
        "precision_decimal_digits": mp.mp.dps,
        "runtime": {"python": sys.version, "platform": platform.platform(),
                    "mpmath": mp.__version__, "sympy": sp.__version__},
        "theorem": "inf_theta R_theta = (1+o(1))/(2p) for p=M^-3",
        "domain": "-1/M < theta < 1/M; other valid tilts have infinite second moment",
        "branch_competitor": "relative variance <= e-1 after supplied p and branch sampling interface",
        "cases": cases,
    }
    (OUT / "exact_certificate.json").write_text(json.dumps(cert, indent=2) + "\n")
    (OUT / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"cases": len(cases), "exact_checks": "PASS",
                      "M_max": cases[-1]["M"],
                      "pR_optimum_at_M_max": cases[-1]["numerical_optimum_p_times_R"],
                      "branch_CV2_at_M_max": cases[-1]["branch_conditioned_relative_variance"],
                      "written": ["results.json", "exact_certificate.json"]}))


if __name__ == "__main__":
    main()

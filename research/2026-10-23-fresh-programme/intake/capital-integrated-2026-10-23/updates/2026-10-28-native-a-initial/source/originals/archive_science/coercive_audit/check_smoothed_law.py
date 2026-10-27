"""Deterministic diagnostics for SMOOTHED_LAW_NEWTON_THEOREM.md.

These checks are not the proof. They compare the analytic theorem against
exact affine Gaussian laws, verify its Gaussian integral constant, and check
the weak cancellation with a nontrivial polynomial test. No source oracle or
mean acquisition claim is made.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def adaptive_simpson(f, left, right, tol=1e-12, maxdepth=30):
    def one(a, b, fa, fm, fb):
        return (b - a) * (fa + 4 * fm + fb) / 6

    a, b = left, right
    m = (a + b) / 2
    fa, fm, fb = f(a), f(m), f(b)
    base = one(a, b, fa, fm, fb)

    def rec(a, b, fa, fm, fb, whole, err, depth):
        m = (a + b) / 2
        lm, rm = (a + m) / 2, (m + b) / 2
        flm, frm = f(lm), f(rm)
        lhs = one(a, m, fa, flm, fm)
        rhs = one(m, b, fm, frm, fb)
        correction = lhs + rhs - whole
        if depth == 0 or abs(correction) <= 15 * err:
            return lhs + rhs + correction / 15
        return rec(a, m, fa, flm, fm, lhs, err / 2, depth - 1) + rec(
            m, b, fm, frm, fb, rhs, err / 2, depth - 1
        )

    return rec(a, b, fa, fm, fb, base, tol, maxdepth)


def normal_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def exact_centered_normal_tv(var_p, var_q):
    """Exact TV for two one-dimensional centered Gaussian laws."""
    lo, hi = sorted([var_p, var_q])
    if math.isclose(lo, hi, rel_tol=1e-15, abs_tol=0):
        return 0.0
    crossing = math.sqrt(lo * hi * math.log(hi / lo) / (hi - lo))
    return 2 * (normal_cdf(crossing / math.sqrt(lo)) - normal_cdf(crossing / math.sqrt(hi)))


def constant(a, c):
    return (
        math.sqrt(6) / (2 * math.sqrt(c)) * (1 / a - math.atan(1 / a))
        + math.sqrt(2) / (8 * c * a * a)
    )


def main():
    integral_errors = []
    for a in [0.125, 0.25, 0.5, 1.0, 2.0, 4.0]:
        numerical = adaptive_simpson(
            lambda s: s * s / (1 + a * a - s * s) ** 1.5, 0.0, 1.0
        )
        exact = 1 / a - math.atan(1 / a)
        integral_errors.append(abs(numerical - exact))
    assert max(integral_errors) < 2e-11

    rows = []
    max_cancel_error = 0.0
    max_residual_error = 0.0
    for amplitude in [0.05, 0.1, 0.2, 0.4, 0.8]:
        # X=amplitude*G+Z, B=(amplitude,1), tau=1+amplitude^2.
        tau = 1 + amplitude * amplitude
        residual = tau - 1
        s = -residual / (2 * tau)
        var_after = (1 + s) ** 2 * tau
        exact_new_residual = residual * residual / (4 * tau)
        formula_new_residual = -s * residual - s * s * tau
        max_residual_error = max(
            max_residual_error,
            abs(var_after - 1 - exact_new_residual),
            abs(formula_new_residual - exact_new_residual),
        )
        # Test h(x)=x^4, f(x)=x^4/4+3x^2/2.
        # E[h(X)+h'(X)u]-E[h(Z)] = E[R f'''(X)u].
        first_order_law_defect = 3 * tau * tau * (1 + 4 * s) - 3
        mixed_term = 6 * residual * s * tau
        max_cancel_error = max(max_cancel_error, abs(first_order_law_defect - mixed_term))

        for reserve in [0.25, 0.5, 1.0, 2.0]:
            exact_tv = exact_centered_normal_tv(var_after + reserve**2, 1 + reserve**2)
            bound = constant(reserve, tau) * residual**2
            assert exact_tv <= bound + 1e-13
            rows.append(
                {
                    "amplitude": amplitude,
                    "reserve_sd": reserve,
                    "initial_tau": tau,
                    "correction_S": s,
                    "new_stein_residual": exact_new_residual,
                    "exact_full_law_TV": exact_tv,
                    "proved_smoothed_TV_bound": min(1.0, bound),
                }
            )

    assert max_cancel_error < 2e-14
    assert max_residual_error < 2e-14
    with (ROOT / "exact_affine_law_checks.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    report = (
        "Deterministic diagnostics: PASS\n"
        f"Gaussian integral constant: max absolute error {max(integral_errors):.3e}\n"
        f"Weak first-order law cancellation: max error {max_cancel_error:.3e}\n"
        f"Exact scalar residual identity: max error {max_residual_error:.3e}\n"
        f"Exact Gaussian full-law TV comparisons: {len(rows)}, all within theorem bound\n"
        "These diagnostics use analytically known affine fields. They do not acquire "
        "an unknown mean or establish the value-only compiler.\n"
    )
    (ROOT / "CHECK_RESULTS.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()

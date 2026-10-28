"""Exact paired-defect and signed-corrector sharpness checks."""
from fractions import Fraction as F
import json
from pathlib import Path


def kernel_sum(a, n):
    return (n * (1 - a) - 1 + a ** n) / (1 - a) ** 2


def scalar_case(m):
    n, a = m * m, F(m - 1, m)
    k = (1 - a) / (1 - a ** n)
    energy = n * k * k
    theta2 = a ** (2 * n) / (1 - a * a)
    remainder = a ** (2 * n) * k * k * kernel_sum(a, n)
    ratio = remainder / (theta2 * energy)
    assert ratio == (1 + a) * (1 - (1 - a ** n) / (n * (1 - a)))
    lower = (1 + a) * (1 - F(1, m))
    assert lower < ratio < 2
    if n <= 64:
        v = [a ** (n - 1 - j) for j in range(n)]
        assert k * sum(v) == 1
        defect = [a * v[0]] + [a * v[j] - v[j-1] for j in range(1, n)]
        assert defect == [a ** n] + [F(0)] * (n - 1)
        alpha = [k] * n
        correction = F(0)
        spent = F(0)
        for s in range(1, n + 1):
            beta = [k] * s + [F(0)] * (n - s)
            correction += sum(x*y for x, y in zip(v, beta)) * a ** n * alpha[0]
            spent += alpha[0] ** 2
            alpha = alpha[1:] + [F(0)]
        assert alpha == [F(0)] * n
        assert spent == energy
        assert a ** n - correction == remainder
    return {"m": m, "q_and_horizon": n, "a": str(a),
            "ratio_diagnostic": float(ratio),
            "exact_rational_lower_bound": str(lower),
            "theta_squared_diagnostic": float(theta2),
            "initial_metric_norm_squared_diagnostic": float(energy),
            "all_assertions_exact": True}


def full_rank_case(m):
    n = m * m
    amin = 1 - F(2, m)
    aa = [1 - F(1, m) - F(j + 1, m * (n + 1)) for j in range(n)]
    assert len(set(aa)) == n and all(0 < a < 1 for a in aa)
    k = (1 - amin) / (1 - amin ** n)
    bb = [F(1, m)] * n
    zz = [b * (1 - a) / (k * (1 - a ** n)) for a, b in zip(aa, bb)]
    assert sum(b*b for b in bb) == 1
    assert all(0 < z <= b for z, b in zip(zz, bb))
    theta2 = sum((a ** (2*n) * z*z / (1-a*a) for a, z in zip(aa, zz)), F(0))
    remainder = k*k * sum((a ** (2*n) * z*z * kernel_sum(a, n)
                            for a, z in zip(aa, zz)), F(0))
    truth = sum((b*b * a**n for a, b in zip(aa, bb)), F(0))
    correction = k*k * sum((z*z * a**n * sum(
        ((r+1)*a**r for r in range(n)), F(0)) for a, z in zip(aa, zz)), F(0))
    assert truth - correction == remainder
    for a, z, b in zip(aa, zz, bb):
        assert k * z * sum((a**r for r in range(n)), F(0)) == b
    ratio = remainder / (theta2 * n * k*k)
    lower = (2 - F(2, m)) * (1 - F(1, m))
    assert lower < ratio < 2
    return {"m": m, "physical_and_dictionary_dimension": n,
            "full_rank_warrant": "Distinct eigenvalues and nonzero z: Vandermonde determinant.",
            "ratio_diagnostic": float(ratio),
            "exact_rational_lower_bound": str(lower),
            "same_receiver_and_source": True, "all_assertions_exact": True}


if __name__ == "__main__":
    result = {"scalar": [scalar_case(m) for m in (2, 3, 4, 8, 16, 32, 64, 128)],
              "full_rank": [full_rank_case(m) for m in (3, 4)],
              "all_checks_passed": True}
    path = Path(__file__).with_name("DISSIPATION_SHARPNESS_RESULTS.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"all_checks_passed": True,
                      "scalar_ratios": [[r["q_and_horizon"], r["ratio_diagnostic"]]
                                        for r in result["scalar"]],
                      "full_rank_ratios": [r["ratio_diagnostic"] for r in result["full_rank"]],
                      "output": str(path)}, indent=2))

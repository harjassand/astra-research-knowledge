"""Finite spin checks for the boundary-compression factorial moment identity.

These checks are diagnostics, not a replacement for the derivation in
quantum_boundary.md.  No external packages are used.
"""

import cmath
import json
import math
from pathlib import Path


def falling(x, k):
    if k > x:
        return 0
    return math.factorial(x) // math.factorial(x - k)


def choose(x, k):
    return math.comb(x, k) if 0 <= k <= x else 0


def rotated_number_law(t, n, lam, z):
    r = (lam / n) / (1 - lam / n)
    c = 1 / math.sqrt(1 + abs(z) ** 2 / n)
    s = z / math.sqrt(n) * c
    weights = [(1 - r) * r ** ell / (1 - r ** (t + 1))
               for ell in range(t + 1)]
    probabilities = [0.0] * (t + 1)
    for ell, weight in enumerate(weights):
        for m in range(t + 1):
            amp = 0j
            for j in range(max(0, m + ell - t), min(m, ell) + 1):
                amp += (choose(m, j) * choose(t - m, ell - j)
                        * s ** (m - j) * (-s.conjugate()) ** (ell - j)
                        * c ** (t - m - ell + 2 * j))
            amp *= math.sqrt(choose(t, m) / choose(t, ell))
            probabilities[m] += weight * abs(amp) ** 2
    return probabilities, weights


def formula_moment(t, n, z, weights, k):
    a = abs(z) ** 2 / (n + abs(z) ** 2)
    return sum(
        weight * choose(k, j) ** 2 * falling(ell, j)
        * falling(t - ell, k - j) * a ** (k - j) * (1 - a) ** j
        for ell, weight in enumerate(weights)
        for j in range(k + 1)
    )


def main():
    count = 0
    max_normalization_error = 0.0
    max_identity_relative_error = 0.0
    largest_bound_ratio = 0.0
    for t in range(13):
        for n in {max(1, t), max(1, t + 3)}:
            for lam in (0.0, min(0.125, n / 8), n / 4):
                for z in (0j, 0.2 + 0.1j, cmath.rect(1.2, 0.73)):
                    probabilities, weights = rotated_number_law(t, n, lam, z)
                    max_normalization_error = max(
                        max_normalization_error, abs(sum(probabilities) - 1))
                    for k in range(1, t + 2):
                        direct = sum(falling(m, k) * p
                                     for m, p in enumerate(probabilities))
                        formula = formula_moment(t, n, z, weights, k)
                        relative = abs(direct - formula) / max(1.0, direct)
                        max_identity_relative_error = max(
                            max_identity_relative_error, relative)
                        bound = 1.5 * (abs(z) ** 2 + 2 * lam) ** k
                        if bound > 0:
                            largest_bound_ratio = max(
                                largest_bound_ratio, direct / bound)
                        assert relative < 1e-9, (t, n, lam, z, k, direct, formula)
                        assert direct <= bound + 1e-8 * max(1.0, bound)
                        tail = sum(probabilities[k:])
                        assert tail <= bound / math.factorial(k) + 1e-10
                        count += 1
    result = {
        "status": "diagnostic_checks_passed",
        "moment_tail_comparisons": count,
        "largest_t": 12,
        "n_1_and_t_0_included": True,
        "max_normalization_error": max_normalization_error,
        "max_identity_relative_error": max_identity_relative_error,
        "largest_bound_ratio": largest_bound_ratio,
        "scope": "finite examples only; analytic proof is separate"
    }
    destination = Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

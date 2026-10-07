"""Small independent transcription check; not a separability proof.

The actual proof of the weak-coupling PPT statement is in
06_multispecies_exact_audit.txt. No peer program is imported or executed.
Only spin-sector matrices are assembled; no N-site dense matrix is used.
"""

import json
import math
import time
from pathlib import Path

import numpy as np


def coefficients(n, delta, two_j):
    j = two_j / 2
    return [delta / (n + 1) * math.sqrt((j - (-j + k)) * (j + (-j + k) + 1))
            for k in range(two_j)]


def predicted_pt_minimum(n, delta, two_j):
    cs = coefficients(n, delta, two_j)
    diagonals_up = [math.cosh(c) for c in cs] + [1.0]
    diagonals_down = [1.0] + [math.cosh(c) for c in cs]
    candidates = [diagonals_up[0], diagonals_down[-1]]
    determinants = []
    for k, c in enumerate(cs):
        a, b = diagonals_down[k], diagonals_up[k + 1]
        off = math.sinh(c)
        determinants.append(a * b - off * off)
        candidates.append((a + b - math.hypot(a - b, 2 * off)) / 2)
    return min(candidates), min(determinants, default=1.0)


def independent_matrix_check(n, delta):
    # Maximal spin j=n/2; basis is (up,m=-j..j), then (down,m=-j..j).
    two_j = n
    dim = two_j + 1
    h = np.zeros((2 * dim, 2 * dim))
    for k, c in enumerate(coefficients(n, delta, two_j)):
        h[k, dim + k + 1] = c
        h[dim + k + 1, k] = c
    vals, vecs = np.linalg.eigh(h)
    exp_h = (vecs * np.exp(vals)) @ vecs.T
    pt = exp_h.reshape(2, dim, 2, dim).transpose(2, 1, 0, 3).reshape(2 * dim, 2 * dim)
    actual = float(np.linalg.eigvalsh(pt)[0])
    predicted, _ = predicted_pt_minimum(n, delta, two_j)
    return {"n": n, "delta": delta, "spin_sector_dimension": 2 * dim,
            "matrix_pt_min_eigenvalue": actual,
            "formula_pt_min_eigenvalue": predicted,
            "absolute_residual": abs(actual - predicted)}


def main():
    start = time.perf_counter()
    fixtures = [independent_matrix_check(n, delta)
                for n, delta in [(1, 0.3), (2, 1.0), (5, 2.5)]]
    assert all(row["absolute_residual"] < 1e-12 for row in fixtures)
    rows = []
    for n in [1, 2, 3, 5, 10, 20, 50]:
        for delta in [0.1, 1.0, 1.7, 2.0, 4.0, 8.0, 16.0]:
            # All allowed angular-momentum sectors of n spin-1/2 sites.
            sector_values = [predicted_pt_minimum(n, delta, two_j)[0]
                             for two_j in range(n % 2, n + 1, 2)]
            rows.append({"n_small": 1, "n_large": n, "delta": delta,
                         "minimum_unnormalized_pt_eigenvalue": min(sector_values),
                         "npt_diagnostic": min(sector_values) < -1e-12})
    assert all(not row["npt_diagnostic"] for row in rows if row["delta"] <= 1.7)
    result = {"status": "PASS_TRANSCRIPTION_ONLY",
              "proof": "06_multispecies_exact_audit.txt Section 9",
              "claimed_radius_counterexample": "NONE",
              "PPT_does_not_establish_full_separability": True,
              "weak_PPT_range_exact": "abs(delta)<=2*asinh(1)",
              "normalization": "HS basis F=Pauli/sqrt(2), cross coefficient delta/(n+1)",
              "field": 0, "within_species_Casimir": "scalar in each spin sector",
              "fixtures": fixtures, "stress_rows": rows,
              "elapsed_seconds": time.perf_counter() - start,
              "dense_full_N_site_operator_constructed": False,
              "max_dense_dimension": 12}
    target = Path(__file__).with_name("unbalanced_xy_checks.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "fixture_count": len(fixtures),
                      "stress_rows": len(rows), "claimed_radius_counterexample": "NONE",
                      "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent exact identities and stress diagnostics, never proof premises.

Writes only into this independent audit directory. No finite LP is used.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent


def main():
    counts = {"geometric_variance_identity": 0,
              "one_sided_residual_gap": 0,
              "operator_determinant": 0,
              "dimensionless_product_equivalence": 0}
    for r_num in range(1, 31):
        r = F(r_num, 31)
        eta = (1-r)/(1+r)
        for scale_num in range(1, 9):
            a = F(scale_num, 7)
            v = 2*(2*a)**2*r/(1-r)**2
            assert v == 2*a*a*(eta**-2-1)
            counts["geometric_variance_identity"] += 1
        one_sided_second = (F(1, 2)+r/(1-r))**2+r/(1-r)**2
        baseline = 2*r/(1-r)**2
        assert one_sided_second-baseline == F(1, 4)
        counts["one_sided_residual_gap"] += 1

    # Rational directions on the unit circle, both signs of c and m,n.
    for c, d in [(F(0), F(1)), (F(3, 5), F(4, 5)),
                 (F(-3, 5), F(4, 5)), (F(5, 13), F(12, 13))]:
        assert c*c+d*d == 1
        for mi in range(-12, 13):
            m = F(mi, 12)
            for ni in range(-12, 13):
                n = F(ni, 12)
                D = 1+m*n*c
                Q = [[D+m+n*c, n*d], [n*d, D-m-n*c]]
                det = Q[0][0]*Q[1][1]-Q[0][1]*Q[1][0]
                polynomial = 1-m*m-n*n+c*c*m*m*n*n
                assert det == polynomial
                counts["operator_determinant"] += 1
                if m and n:
                    x, y = m**-2-1, n**-2-1
                    assert det == m*m*n*n*(x*y-d*d)
                    counts["dimensionless_product_equivalence"] += 1

    # Exact Gaussian countermodel: variances 3,3 exceed the threshold 4.
    gaussian_m = F(3, 4)
    gaussian_det = 1-2*gaussian_m**2
    assert gaussian_det == F(-1, 8)
    assert F(3)*F(3) > 4

    # Exact orthogonal boundary witness with unequal costs.
    eta1, eta2 = F(3, 5), F(4, 5)
    v1, v2 = 2*(eta1**-2-1), 2*(eta2**-2-1)
    assert eta1**2+eta2**2 == 1
    assert v1 == F(32, 9) and v2 == F(9, 8) and v1*v2 == 4

    # Continuous-spectrum δ=1 is not attained on x in (0,1).
    # Every sampled fiber is strictly positive at m=n=1/sqrt(2),
    # and the lowest eigenvalue tends to zero as x tends to zero.
    eta = 1/math.sqrt(2)
    spectrum_diagnostic = []
    for x in [0.8, 0.2, 0.05, 0.01, 0.001]:
        D = 1+eta*eta*x
        eigen_min = D-math.sqrt(2*eta*eta*(1+x))
        determinant = x*x/4
        # Stable eigenvalue formula avoids near-zero cancellation.
        stable_min = determinant/(D+math.sqrt(2*eta*eta*(1+x)))
        assert stable_min > 0
        assert abs(eigen_min-stable_min) < 1e-14
        spectrum_diagnostic.append({"x": x, "minimum_eigenvalue": stable_min})

    r = (1-eta)/(1+eta)
    alpha = math.atanh(eta)
    beta = alpha/2
    q = r*math.exp(2*beta)
    D = (1-r)*math.exp(beta)/(1-q)
    N = 18
    tilt_bound = 2*D*D*q**(N+1)
    tv_bound = 2*r**(N+1)
    assert tilt_bound < 1e-6
    assert tv_bound < 1e-13

    result = {
        "status": "PASSED_EXACT_IDENTITIES_AND_DIAGNOSTICS_ONLY",
        "counts": counts,
        "total_exact_identity_cases": sum(counts.values()),
        "gaussian_variance_only_countermodel": {
            "A": "sigma_z", "B": "sigma_x", "variances": [3, 3],
            "variance_product": 9, "commutator_norm_squared": 4,
            "output_coordinates": "x=y=(3/2)*log(7)",
            "contrasts": ["3/4", "3/4"], "Q_determinant": "-1/8",
            "analytic_status": "Negative on an open set with strictly positive reference density"},
        "geometric_boundary_witness": {"eta1": str(eta1), "eta2": str(eta2),
                                       "variance1": str(v1), "variance2": str(v2),
                                       "variance_product": str(v1*v2)},
        "continuous_spectrum_boundary_diagnostic": spectrum_diagnostic,
        "finite_output_example": {"N_each": N, "alphabet_upper_bound": 4*(N+1)**2,
                                  "maximum_coordinate_magnitude": 2*N+1,
                                  "tilt_half_width": beta,
                                  "uniform_tilt_error_bound": tilt_bound,
                                  "uniform_TV_bound": tv_bound},
        "audit_sha256": hashlib.sha256((HERE/"AUDIT.md").read_bytes()).hexdigest(),
        "limits": "Finite identities are diagnostics; the saved analytic proof carries universal quantifiers. No formal or external verification."
    }
    (HERE/"CHECKS.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

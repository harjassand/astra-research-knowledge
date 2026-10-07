"""Exact examples and outward-rounded intervals for the entropy/power bound.

The symbolic calculation is for an orthonormal left-invariant frame
E0,E+,E- with brackets
    [E0,E+] = -a E+, [E0,E-] = a E-, [E+,E-] = beta E0,
and X = v E0.  Rational example parameters and all algebraic operations are
exact.  The only floating-looking outputs (pi and exp) are enclosed by
rational-series bounds with explicit remainders.

This script checks finite-dimensional geometry, not the entropy theorem,
Pesin's formula, lattice existence, or physical model adequacy.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction as F
from itertools import product
from math import factorial
import json
from pathlib import Path

import sympy as sp


def symbolic_certificate():
    a, beta, v, nu = sp.symbols("a beta v nu", real=True)
    n = 3
    c = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for i, j, k, value in (
        (0, 1, 1, -a),
        (0, 2, 2, a),
        (1, 2, 0, beta),
    ):
        c[i][j][k] = value
        c[j][i][k] = -value

    jacobi = all(
        sp.simplify(sum(
            c[i][j][m] * c[m][k][ell]
            + c[j][k][m] * c[m][i][ell]
            + c[k][i][m] * c[m][j][ell]
            for m in range(n)
        )) == 0
        for i, j, k, ell in product(range(n), repeat=4)
    )
    unimodular = all(sum(c[i][j][j] for j in range(n)) == 0 for i in range(n))
    gamma = [[[
        sp.simplify((c[i][j][k] - c[j][k][i] + c[k][i][j]) / 2)
        for k in range(n)
    ] for j in range(n)] for i in range(n)]
    torsion_free = all(
        sp.simplify(gamma[i][j][k] - gamma[j][i][k] - c[i][j][k]) == 0
        for i, j, k in product(range(n), repeat=3)
    )
    metric_compatible = all(
        sp.simplify(gamma[i][j][k] + gamma[i][k][j]) == 0
        for i, j, k in product(range(n), repeat=3)
    )

    # A[k,i] = <nabla_{E_i} X,E_k>; rows are output coordinates.
    grad_x = sp.Matrix(n, n, lambda k, i: sp.simplify(v * gamma[i][0][k]))
    strain = sp.simplify((grad_x + grad_x.T) / 2)
    div_strain = sp.Matrix(n, 1, lambda j, _:
        sp.simplify(-sum(
            gamma[i][i][k] * strain[k, j]
            + gamma[i][j][k] * strain[i, k]
            for i in range(n) for k in range(n)
        )))
    ric = sp.Matrix(n, n, lambda j, k: sp.simplify(sum(
        sum(
            gamma[j][k][ell] * gamma[i][ell][i]
            - gamma[i][k][ell] * gamma[j][ell][i]
            - c[i][j][ell] * gamma[ell][k][i]
            for ell in range(n)
        ) for i in range(n)
    )))

    expected_grad = sp.Matrix([
        [0, 0, 0],
        [0, a * v, beta * v / 2],
        [0, -beta * v / 2, -a * v],
    ])
    expected_strain = sp.diag(0, a * v, -a * v)
    expected_div = sp.Matrix([-2 * a**2 * v, 0, 0])
    strain_sq = sp.simplify(sp.trace(strain.T * strain))
    power_density = sp.simplify((-2 * nu * div_strain).dot(sp.Matrix([v, 0, 0])))
    h = a * v
    scalar_curvature = sp.simplify(sp.trace(ric))

    checks = {
        "jacobi_identity": jacobi,
        "unimodular_volume_preservation": unimodular,
        "koszul_torsion_free": torsion_free,
        "koszul_metric_compatible": metric_compatible,
        "nabla_X_X_zero": sp.simplify(grad_x[:, 0]) == sp.zeros(n, 1),
        "div_X_zero": sp.trace(grad_x) == 0,
        "nabla_X_matrix": sp.simplify(grad_x - expected_grad) == sp.zeros(n),
        "strain_matrix": sp.simplify(strain - expected_strain) == sp.zeros(n),
        "strain_norm_squared": sp.simplify(strain_sq - 2 * a**2 * v**2) == 0,
        "stress_divergence": sp.simplify(div_strain - expected_div) == sp.zeros(n, 1),
        "power_density": sp.simplify(power_density - 4 * nu * a**2 * v**2) == 0,
        "entropy_power_residual_given_H_av": sp.simplify(power_density - 4 * nu * h**2) == 0,
        "scalar_curvature": sp.simplify(scalar_curvature + 2 * a**2 + beta**2 / 2) == 0,
    }

    # For beta != 0, H=-2E0/a, e=E+, f=-2E-/(a beta) obey the standard sl2 brackets.
    H = sp.Matrix([-2 / a, 0, 0])
    e = sp.Matrix([0, 1, 0])
    f = sp.Matrix([0, 0, -2 / (a * beta)])
    def bracket(u, w):
        out = sp.zeros(n, 1)
        for i, j in product(range(n), repeat=2):
            for k in range(n):
                out[k] += u[i] * w[j] * c[i][j][k]
        return sp.simplify(out)
    checks["beta_nonzero_sl2_brackets"] = (
        sp.simplify(bracket(H, e) - 2 * e) == sp.zeros(n, 1)
        and sp.simplify(bracket(H, f) + 2 * f) == sp.zeros(n, 1)
        and sp.simplify(bracket(e, f) - H) == sp.zeros(n, 1)
    )

    # Directly transform the canonical Sasaki frame on a constant-curvature
    # surface, whose standard brackets are [X,H]=-k^2 V, [X,V]=-H, [H,V]=X.
    k = sp.symbols("k", positive=True, real=True)
    cc = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for i, j, m, value in ((0, 1, 2, -k**2), (0, 2, 1, -1), (1, 2, 0, 1)):
        cc[i][j][m] = value
        cc[j][i][m] = -value
    denom = sp.sqrt(1 + k**2)
    T = sp.Matrix([[1, 0, 0], [0, 1 / denom, 1 / denom],
                    [0, k / denom, -k / denom]])
    E0, Ep, Em = T[:, 0], T[:, 1], T[:, 2]
    def canonical_bracket(u, w):
        out = sp.zeros(n, 1)
        for i, j in product(range(n), repeat=2):
            for m in range(n):
                out[m] += u[i] * w[j] * cc[i][j][m]
        return sp.simplify(T.inv() * out)
    beta_k = -2 * k / (1 + k**2)
    checks["constant_curvature_sasaki_frame"] = (
        sp.simplify(canonical_bracket(E0, Ep) + k * sp.Matrix([0, 1, 0])) == sp.zeros(n, 1)
        and sp.simplify(canonical_bracket(E0, Em) - k * sp.Matrix([0, 0, 1])) == sp.zeros(n, 1)
        and sp.simplify(canonical_bracket(Ep, Em) - beta_k * sp.Matrix([1, 0, 0])) == sp.zeros(n, 1)
    )

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "nabla_X": str(grad_x),
        "strain": str(strain),
        "div_strain": str(div_strain),
        "ricci": str(ric),
        "scalar_curvature": str(scalar_curvature),
        "scope": "Exact frame algebra only. H=av is derived from the adjoint flow rates plus the smooth-measure entropy formula; the script does not verify either theorem or compact quotient existence.",
    }


def arctan_bounds(x: F, n_terms: int) -> tuple[F, F]:
    """Alternating-series enclosure for atan(x), 0 < x <= 1."""
    partial = sum(((-1) ** k) * x ** (2 * k + 1) / (2 * k + 1)
                  for k in range(n_terms + 1))
    next_term = ((-1) ** (n_terms + 1)) * x ** (2 * n_terms + 3) / (2 * n_terms + 3)
    return (partial, partial + next_term) if next_term > 0 else (partial + next_term, partial)


def pi_bounds(n_terms: int = 20) -> tuple[F, F]:
    """Machin identity pi=16 atan(1/5)-4 atan(1/239), with exact remainders."""
    a_lo, a_hi = arctan_bounds(F(1, 5), n_terms)
    b_lo, b_hi = arctan_bounds(F(1, 239), n_terms)
    return 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo


def exp_bounds(x: F, n_terms: int = 20) -> tuple[F, F]:
    """Taylor lower bound plus geometric upper bound for exp(x), x >= 0."""
    partial = sum(x**k / factorial(k) for k in range(n_terms + 1))
    first_omitted = x ** (n_terms + 1) / factorial(n_terms + 1)
    ratio_bound = x / (n_terms + 2)
    if ratio_bound >= 1:
        raise ValueError("choose more Taylor terms so x/(N+2) < 1")
    tail_bound = first_omitted / (1 - ratio_bound)
    return partial, partial + tail_bound


def outward_decimal(value: F, places: int, rounding: str) -> str:
    with localcontext() as ctx:
        ctx.prec = places + 12
        ctx.rounding = rounding
        d = Decimal(value.numerator) / Decimal(value.denominator)
        quantum = Decimal(1).scaleb(-places)
        return str(d.quantize(quantum, rounding=rounding))


def rational_string(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def exact_case(name: str, a: F, beta: F, v: F, nu: F) -> dict:
    h = a * v
    s2 = 2 * a * a * v * v
    power_per_volume = 2 * nu * s2
    rhs_per_volume = 4 * nu * h * h
    exp_lo, exp_hi = exp_bounds(h)
    return {
        "name": name,
        "a": rational_string(a),
        "beta": rational_string(beta),
        "speed_v": rational_string(v),
        "nu": rational_string(nu),
        "lie_algebra": "sl2(R)" if beta != 0 else "solvable Sol algebra",
        "entropy_rate_H": rational_string(h),
        "strain_norm_squared": rational_string(s2),
        "sustaining_force_coefficient_F_equals_cX": rational_string(4 * nu * a * a),
        "power_per_unit_volume": rational_string(power_per_volume),
        "bound_per_unit_volume": rational_string(rhs_per_volume),
        "exact_residual": rational_string(power_per_volume - rhs_per_volume),
        "time_one_expansion_interval_lower": outward_decimal(exp_lo, 18, ROUND_FLOOR),
        "time_one_expansion_interval_upper": outward_decimal(exp_hi, 18, ROUND_CEILING),
        "time_one_expansion_width_lt_1e-8": exp_hi - exp_lo < F(1, 10**8),
    }


def closed_geodesic_example(genus: int, kappa: F, nu: F) -> dict:
    """Closed curvature -kappa^2 surface; Sasaki metric on its unit tangent bundle."""
    h = kappa
    volume_coeff = F(8 * (genus - 1), 1) / (kappa * kappa)  # V = coeff*pi^2
    work_coeff = F(32 * (genus - 1), 1) * nu  # W = coeff*pi^2
    s2 = 2 * kappa * kappa
    force_c = 4 * nu * kappa * kappa
    p_lo, p_hi = pi_bounds()
    pi2_lo, pi2_hi = p_lo * p_lo, p_hi * p_hi
    vol_lo, vol_hi = volume_coeff * pi2_lo, volume_coeff * pi2_hi
    work_lo, work_hi = work_coeff * pi2_lo, work_coeff * pi2_hi
    exp_lo, exp_hi = exp_bounds(h)
    return {
        "surface_genus": genus,
        "curvature": f"-{rational_string(kappa*kappa)}",
        "kappa": rational_string(kappa),
        "nu": rational_string(nu),
        "lie_algebra_frame_beta": rational_string(-2 * kappa / (1 + kappa * kappa)),
        "entropy_rate_H": rational_string(h),
        "strain_norm_squared": rational_string(s2),
        "power_per_unit_volume": rational_string(4 * nu * kappa * kappa),
        "volume_exact": f"{rational_string(volume_coeff)}*pi^2",
        "work_exact": f"{rational_string(work_coeff)}*pi^2",
        "volume_interval_outward_24dp": [
            outward_decimal(vol_lo, 24, ROUND_FLOOR),
            outward_decimal(vol_hi, 24, ROUND_CEILING),
        ],
        "work_interval_outward_24dp": [
            outward_decimal(work_lo, 24, ROUND_FLOOR),
            outward_decimal(work_hi, 24, ROUND_CEILING),
        ],
        "pi_interval_width_lt_1e-30": p_hi - p_lo < F(1, 10**30),
        "time_one_expansion_interval_outward_18dp": [
            outward_decimal(exp_lo, 18, ROUND_FLOOR),
            outward_decimal(exp_hi, 18, ROUND_CEILING),
        ],
        "interval_method": "Exact rational Machin arctan alternating-series bounds for pi; positive interval squaring and multiplication. Exact rational Taylor lower bound plus geometric upper bound for exp(kappa).",
    }


def measurement_residual_error(H0: F, nu0: F, P0: F,
                               dH: F, dnu: F, dP: F) -> F:
    """Bound |(P-4 nu H^2)-(P0-4 nu0 H0^2)| for nonnegative quantities."""
    H_hi = H0 + dH
    return dP + 4 * (dnu * H_hi**2 + nu0 * dH * (2 * H0 + dH))


def main():
    cert = symbolic_certificate()
    cases = [
        exact_case("sl2 compact quotient A", F(3, 2), F(1), F(2), F(5, 7)),
        exact_case("sl2 compact quotient B", F(2, 3), F(-3, 2), F(5, 4), F(7, 5)),
    ]
    surfaces = [
        closed_geodesic_example(2, F(1, 2), F(1, 3)),
        closed_geodesic_example(2, F(2), F(1, 3)),
        closed_geodesic_example(3, F(3, 2), F(7, 5)),
    ]
    # Rounded independent measurements around the exact equality case have no
    # strictly positive certification margin; the algebraic identity does.
    H0, nu0, P0 = F(3), F(5, 7), F(180, 7)
    error_radius = measurement_residual_error(
        H0, nu0, P0, F(1, 10**6), F(1, 10**8), F(1, 10**7)
    )
    output = {
        "status": "PASS" if cert["status"] == "PASS" and all(
            F(case["exact_residual"]) == 0 for case in cases
        ) and all(surface["pi_interval_width_lt_1e-30"] for surface in surfaces) else "FAIL",
        "symbolic_certificate": cert,
        "exact_sl2_cases": cases,
        "constant_negative_curvature_geodesic_cases": surfaces,
        "finite_measurement_warning": {
            "exact_residual_case_A": "0",
            "residual_uncertainty_bound_for_delta_H_1e-6_delta_nu_1e-8_delta_P_1e-7": rational_string(error_radius),
            "interpretation": "This bound cannot certify nonnegativity from independent rounded measurements at an exact equality point. The exact symbolic identity and exact supplied parameters do certify equality; decimal agreement alone does not.",
        },
        "limitations": [
            "The entropy rate uses the smooth-volume Pesin formula after exact Lyapunov exponents are derived; the script does not prove Pesin's theorem.",
            "Compactness uses a supplied cocompact lattice in PSL(2,R), realized for the geodesic examples by a closed hyperbolic surface group.",
            "No lattice/metric acquisition protocol, external-force implementation, Navier-Stokes time evolution, or empirical work meter is modeled.",
        ],
    }
    out = Path(__file__).with_name("homogeneous_power_examples.json")
    out.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

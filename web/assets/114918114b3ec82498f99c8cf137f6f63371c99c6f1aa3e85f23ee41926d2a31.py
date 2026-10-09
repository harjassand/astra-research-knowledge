#!/usr/bin/env python3
"""Exact small-object and scalar diagnostics, not general proof validation."""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import sympy as s


HERE = Path(__file__).resolve().parent
checks: list[dict] = []


def exact(name: str, condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(name + ": " + detail)
    checks.append({"name": name, "status": "PASS", "kind": "exact", "detail": detail})


def is_zero(mat: s.Matrix) -> bool:
    return all(s.simplify(x) == 0 for x in mat)


# Full-domain d=2,L=2 channel, including bottom-sector replacement.
dim = 5
k0 = s.zeros(dim * dim, dim)
k1 = s.zeros(dim * dim, dim)
v = s.zeros(dim * dim, dim)
k0[0, 0] = 1
k1[0, 1] = 1
v[0, 2] = 1
v[1, 3] = 1 / s.sqrt(2)
v[5, 3] = 1 / s.sqrt(2)
v[6, 4] = 1
kraus = [k0, k1, v]
exact("full_domain_Kraus_TP", is_zero(sum((k.H * k for k in kraus), s.zeros(dim)) - s.eye(dim)),
      "Three 25x5 algebraic Kraus matrices have sum K* K=I_5, including bottom inputs.")
exact("splitter_isometry", is_zero(v[:, 2:5].H * v[:, 2:5] - s.eye(3)),
      "Occupation-basis Sym^2(C^2) grouping is an exact isometry.")


def partial_trace_second(mat: s.Matrix) -> s.Matrix:
    return s.Matrix(dim, dim, lambda a, b: sum(mat[a * dim + c, b * dim + c] for c in range(dim)))


def partial_trace_first(mat: s.Matrix) -> s.Matrix:
    return s.Matrix(dim, dim, lambda a, b: sum(mat[c * dim + a, c * dim + b] for c in range(dim)))


u, w = s.symbols("u w", real=True)
norm_ideal = s.groebner([u * u + w * w - 1], w, u, extension=s.sqrt(2))


def norm_zero(mat: s.Matrix) -> bool:
    return all(norm_ideal.reduce(s.expand(x))[1] == 0 for x in mat)


omega = s.zeros(dim)
omega[0, 0] = 1
for phase in [s.Integer(1), s.I, s.Integer(-1), -s.I]:
    psi = s.Matrix([u, phase * w])
    psi2 = s.Matrix([u * u, s.sqrt(2) * u * phase * w, phase * phase * w * w])
    rho = s.diag(psi * psi.H, psi2 * psi2.H) / 2
    out = sum((k * rho * k.H for k in kraus), s.zeros(dim * dim))
    target = (s.diag(psi * psi.H, s.zeros(3)) + omega) / 2
    # Include i in coefficient field for exact polynomial reductions.
    norm_ideal = s.groebner([u * u + w * w - 1], w, u, extension=[s.sqrt(2), s.I])
    exact("broadcast_marginals_phase_" + str(phase),
          norm_zero(partial_trace_second(out) - target) and norm_zero(partial_trace_first(out) - target),
          "Both marginals equal (bottom psi+omega)/2 under u^2+w^2=1; top input is shifted down.")

# Eight algebraic directions: two Gauss-Legendre magnitude nodes x four phases.
y_nodes = [(1 - 1 / s.sqrt(3)) / 2, (1 + 1 / s.sqrt(3)) / 2]
phases = [s.Integer(1), s.I, s.Integer(-1), -s.I]
for n in [1, 2, 3]:
    for a, b in itertools.product(range(n + 1), repeat=2):
        phase_mean = sum((z ** a) * s.conjugate(z ** b) for z in phases) / 4
        if a != b:
            moment = s.Integer(0) if s.simplify(phase_mean) == 0 else None
            exact(f"design_{n}_offdiag_{a}_{b}", moment == 0,
                  "Fourth-root phase sum kills all nonzero exponent differences through order 3.")
        else:
            moment = sum(s.binomial(n, a) * y ** (n - a) * (1 - y) ** a for y in y_nodes) / 2
            exact(f"design_{n}_diag_{a}", s.simplify(moment - s.Rational(1, n + 1)) == 0,
                  "Weighted occupation-basis diagonal moment equals 1/(n+1) exactly.")

# Two EPR-projection subspaces and the exact d=2 Choi score operator.
epr = s.Matrix([1, 0, 0, 1]) / s.sqrt(2)
p_ab = s.kronecker_product(epr * epr.H, s.eye(2))
embed_ac = s.zeros(8, 2)
for b in range(2):
    for a in range(2):
        embed_ac[a * 4 + b * 2 + a, b] = 1 / s.sqrt(2)
p_ac = embed_ac * embed_ac.H
omega_choi = (s.eye(8) + p_ab + p_ac) / 6
eigenvalues = omega_choi.eigenvals()
exact("Choi_score_norm", max(eigenvalues) == s.Rational(5, 12),
      "Largest score-operator eigenvalue is 5/12; unnormalized Choi trace 2 gives score<=5/6.")

# Finite scalar checks cover trace-inactive clipping, trace-active clipping,
# and the exact included reference, as diagnostics of the KKT branches.
for name, avec, zvec, cap, lam, multiplier in [
    ("inactive_trace_clipped", [s.Integer(2), s.Integer(0)], [s.Rational(3, 2), s.Integer(0)],
     s.Rational(3, 2), s.Rational(1, 100), s.Integer(0)),
    ("active_trace_clipped", [s.Rational(2331, 1250), s.Rational(169, 1250)],
     [s.Rational(3, 2), s.Rational(1, 2)], s.Rational(3, 2), s.Rational(1, 100), s.Rational(1, 4)),
    ("exact_reference", [s.Integer(1), s.Integer(1)], [s.Integer(1), s.Integer(1)],
     s.Integer(2), s.Rational(1, 100), s.Rational(12, 25)),
]:
    c = 2 * multiplier
    stationary = True
    for ai, zi in zip(avec, zvec):
        if ai == 0:
            stationary &= zi == 0
        elif zi == cap:
            stationary &= ai / cap >= (c + 4 * lam * cap) ** 2
        else:
            stationary &= s.simplify(ai / zi - (c + 4 * lam * zi) ** 2) == 0
    trace = sum(zvec) / 2
    stationary &= sum(avec) / 2 == 1 and trace <= 1
    stationary &= multiplier == 0 or trace == 1
    lower = all(zi >= min(ai, cap) / (1 + 4 * lam * cap) ** 2 for ai, zi in zip(avec, zvec))
    exact("KKT_" + name, bool(stationary and c < 1 and lower),
          "Rational fixture satisfies stationarity/complementarity, c<1 and clipped-component lower bound.")

scalar_conditions = {
    "normalization_t_above_half": s.Rational(16, 27) > s.Rational(1, 2),
    "beta_coefficient_below_27": s.Rational(187, 7) < 27,
    "tail_coefficient_below_8": s.Rational(5, 3) ** 8 > 27,
    "rate_derivative_domain": 288 > 68,
    "optimized_tail_below_epsilon": s.Rational(625, 16) > 24,
    "final_500_constant": 3 * 144 < 500,
    "large_error_branch": 500 > 288,
}
for name, value in scalar_conditions.items():
    exact(name, bool(value), "Exact rational inequality used by the tracial logarithmic composition.")

parameter_diagnostics = []
for ladder_l in [2, 3, 4, 6, 8]:
    m = 2 ** (ladder_l - 1)
    d = ladder_l * m
    ds = [math.comb(2 ** j + d - 1, 2 ** j) for j in range(ladder_l)]
    capacity = sum(math.log(x) for x in ds) / ladder_l
    c_lower = m * math.log(ladder_l) / ladder_l
    c_upper = 2 * m * (1 + math.log(ladder_l + 1) + math.log(2)) / ladder_l
    if not c_lower <= capacity <= c_upper:
        raise AssertionError("capacity interval diagnostic")
    parameter_diagnostics.append({
        "L": ladder_l, "d": d, "max_copy_number": m,
        "C_nats_numeric": capacity, "C_explicit_lower_numeric": c_lower,
        "C_explicit_upper_numeric": c_upper,
        "b_lower_rational": str(s.Rational(d - 1, 2 * ladder_l * (d + 1))),
        "displayed_b_rational": str(s.Rational(1, ladder_l)),
        "e_lower_rational": str(1 - s.Rational(m + 1, m + d)),
        "kind": "finite_numeric_formula_diagnostic_not_asymptotic_materialization",
    })

sparse_matrices = []
for name, mat in zip(["bottom_basis_0_replacement", "bottom_basis_1_replacement", "Sym2_splitter"], kraus):
    sparse_matrices.append({
        "name": name, "shape": list(mat.shape),
        "entries": [[a, b, str(mat[a, b])] for a in range(mat.rows) for b in range(mat.cols) if mat[a, b] != 0],
    })

report = {
    "schema": "cycle04-exact-diagnostics-v1", "status": "PASS",
    "exact_check_count": len(checks), "checks": checks,
    "fixture": {"d": 2, "L": 2, "H_dimension": 5, "output_dimension": 25,
                "third_design_label_count": 8, "C_exact": "ln(6)/2",
                "e_lower_exact": "7/24", "b_lower_exact": "1/12", "displayed_b_exact": "1/2"},
    "parameter_diagnostics": parameter_diagnostics,
    "scope": "Finite exact object and scalar diagnostics; not general theorem, external validation, solver proof, or materialized asymptotic family.",
}
(HERE / "EXACT_REPLAY_RESULTS.json").write_text(json.dumps(report, indent=2) + "\n")
(HERE / "EXACT_SMALL_KRAUS_MATRICES.json").write_text(json.dumps(sparse_matrices, indent=2) + "\n")
print(json.dumps({"status": "PASS", "exact_check_count": len(checks), "finite_parameter_count": len(parameter_diagnostics)}))

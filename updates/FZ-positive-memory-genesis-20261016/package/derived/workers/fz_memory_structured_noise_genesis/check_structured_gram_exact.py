#!/usr/bin/env python3
"""Finite exact algebra diagnostics, not a memory or novelty certificate.

All writes are confined to this script's directory. Python 3 and SymPy are
required. This checks Gaussian-rational examples and symbolic counterminors.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as s

Q = s.Rational
ii = s.I
I2 = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -ii], [ii, 0]])
Z = s.diag(1, -1)


def clean(A):
    return A.applyfunc(s.simplify)


def zero(A):
    assert clean(A) == s.zeros(*A.shape), A


def units(d):
    for i in range(d):
        for j in range(d):
            E = s.zeros(d)
            E[i, j] = 1
            yield E


def dissipator(L, rho):
    K = L.H * L
    return L * rho * L.H - (K * rho + rho * K) / 2


def normalized_vec(A):
    d = A.rows
    return s.Matrix([A[i, j] for i in range(d) for j in range(d)]) / s.sqrt(d)


def choi(map_fn, d):
    out = s.zeros(d * d)
    for E in units(d):
        out += s.kronecker_product(map_fn(E), E) / d
    return clean(out)


def trace_out(J, d):
    return s.Matrix(d, d, lambda i, j: sum(J[o * d + i, o * d + j] for o in range(d)))


def pauli_modes(m):
    letters = {"I": I2, "X": X, "Y": Y, "Z": Z}
    for word in itertools.product(letters, repeat=m):
        yield "".join(word), s.kronecker_product(*(letters[c] for c in word))


def signed_gram_example():
    modes = [s.kronecker_product(X, I2), s.kronecker_product(Y, Z), s.kronecker_product(Z, Z)]
    d, n = 4, 3
    C = s.Matrix([[Q(1, 20), -ii / 40, 0], [ii / 40, -Q(1, 50), 0], [0, 0, 0]])
    h = s.Matrix([Q(1, 30), 0, Q(1, 40)])
    gamma = s.Matrix([Q(1, 5)] * n)
    Gamma = sum(gamma)
    H = sum((h[j] * modes[j] for j in range(n)), s.zeros(d))
    K = sum((C[j, k] * modes[k] * modes[j] for j in range(n) for k in range(n)), s.zeros(d))
    k0 = s.simplify(s.trace(K) / d)
    k = s.Matrix([s.simplify(s.trace(P * K) / d) for P in modes])
    zero(K - k0 * s.eye(d) - sum((k[j] * modes[j] for j in range(n)), s.zeros(d)))
    assert k0 == s.trace(C)
    assert k == s.Matrix([0, 0, -Q(1, 20)])
    D = s.diag(*gamma) + C
    a = -k / 2 - ii * h
    s0 = s.simplify((a.H * D.inv() * a)[0])
    r_min = s.simplify(Gamma + s.trace(C) + s0)
    principal = [s.simplify(D[:j, :j].det()) for j in range(1, n + 1)]
    assert all(x > 0 for x in principal)
    assert C[1, 1] < 0

    def G(rho):
        result = -ii * (H * rho - rho * H)
        for j in range(n):
            result += gamma[j] * (modes[j] * rho * modes[j] - rho)
        result += sum((C[j, k] * modes[j] * rho * modes[k] for j in range(n) for k in range(n)), s.zeros(d))
        return clean(result - (K * rho + rho * K) / 2)

    # Explicit exact Cholesky factor yields jumps B_j, not merely a PSD flag.
    V = D.cholesky()
    zero(V * V.H - D)
    c = (V.inv() * a).conjugate()
    B = [clean(c[j] * s.eye(d) + sum((V[k, j] * modes[k] for k in range(n)), s.zeros(d))) for j in range(n)]
    zero(sum((b.H * b for b in B), s.zeros(d)) - r_min * s.eye(d))
    for rho in units(d):
        zero(sum((dissipator(b, rho) for b in B), s.zeros(d)) - G(rho))

    Psi = lambda rho: rho + G(rho) / r_min
    J = choi(Psi, d)
    M = s.zeros(n + 1)
    M[0, 0] = r_min - Gamma - s.trace(C)
    M[0, 1:] = a.H
    M[1:, 0] = a
    M[1:, 1:] = D
    W = s.Matrix.hstack(normalized_vec(s.eye(d)), *(normalized_vec(P) for P in modes))
    zero(J - W * M * W.H / r_min)
    zero(trace_out(J, d) - s.eye(d) / d)
    assert J.rank() == n
    assert s.simplify(M[0, 0] - (a.H * D.inv() * a)[0]) == 0
    # At rate below the sharp minimum the same Schur complement is negative.
    r_less = r_min - Q(1, 100)
    assert s.simplify(r_less - Gamma - s.trace(C) - s0) == -Q(1, 100)
    return {
        "case": "signed_non_Pauli_GKSL_two_qubit_catalog",
        "catalog": ["XI", "YZ", "ZZ"],
        "ambient_dimension": d,
        "catalog_size": n,
        "C_is_PSD": False,
        "D_leading_principal_minors": [str(x) for x in principal],
        "K_identity_coefficient": str(k0),
        "K_nonidentity_coefficients": [str(x) for x in k],
        "minimum_proposal_rate": str(r_min),
        "floor_rate": str(Gamma),
        "proposal_Kraus_rank": n,
        "matrix_units_checked": d * d,
        "scalar_rate_operator_verified": True,
        "direct_Choi_Gram_identity_verified": True,
        "trace_preservation_verified": True,
        "below_boundary_Schur_complement": "-1/100",
    }


def missing_directions():
    d = 4
    floor_modes = [s.kronecker_product(P, I2) for P in (X, Y, Z)] + [s.kronecker_product(I2, P) for P in (X, Y, Z)]
    gamma = Q(1, 10)
    ZZ = s.kronecker_product(Z, Z)
    r = s.symbols("r", real=True)
    h = s.symbols("h", real=True)

    def F(rho):
        return sum((gamma * (P * rho * P - rho) for P in floor_modes), s.zeros(d))

    W = s.Matrix.hstack(normalized_vec(s.eye(d)), normalized_vec(ZZ))
    J_coh = choi(lambda rho: r * rho + F(rho) - ii * h * (ZZ * rho - rho * ZZ), d)
    minor_coh = clean(W.H * J_coh * W)
    det_coh = s.simplify(minor_coh.det())
    assert det_coh == -h**2

    L = s.zeros(d)
    L[0, 3] = 1  # |00><11|, a genuine positive two-site dissipator.
    effect = clean(L.H * L)
    zero(effect - (s.eye(d) - s.kronecker_product(Z, I2) - s.kronecker_product(I2, Z) + ZZ) / 4)
    J_diss = choi(lambda rho: r * rho + F(rho) + dissipator(L, rho), d)
    minor_diss = clean(W.H * J_diss * W)
    det_diss = s.simplify(minor_diss.det())
    assert det_diss == -Q(1, 64)

    J_signed = choi(lambda rho: r * rho + F(rho) - (ZZ * rho * ZZ - rho) / 100, d)
    omitted_diag = s.simplify((normalized_vec(ZZ).H * J_signed * normalized_vec(ZZ))[0])
    assert omitted_diag == -Q(1, 100)
    return {
        "case": "independent_single_site_floor_countermodels",
        "floor_rate_per_Pauli": str(gamma),
        "coherent_ZZ_principal_block": [[str(x) for x in row] for row in minor_coh.tolist()],
        "coherent_ZZ_determinant_for_all_r": str(det_coh),
        "positive_two_site_lowering_principal_block": [[str(x) for x in row] for row in minor_diss.tolist()],
        "positive_two_site_lowering_determinant_for_all_r": str(det_diss),
        "missing_signed_ZZ_diagonal_for_all_r": str(omitted_diag),
        "conclusion": "No finite CPTP proposal rate repairs any of these missing directions.",
    }


def sharp_pauli_identity():
    gamma, h = Q(2, 5), Q(3, 10)
    r = s.simplify(gamma + h * h / gamma)
    U = clean((h * I2 - ii * gamma * X) / s.sqrt(h * h + gamma * gamma))
    zero(U.H * U - I2)
    for rho in units(2):
        zero(-ii * h * (X * rho - rho * X) + gamma * (X * rho * X - rho) - r * (U * rho * U.H - rho))
    lower_rate = r - Q(1, 100)
    lower_minor = s.Matrix([[lower_rate - gamma, ii * h], [-ii * h, gamma]])
    assert lower_minor.det() == -Q(1, 250)
    return {
        "case": "sharp_Pauli_Hamiltonian_dephasing_identity",
        "gamma": str(gamma),
        "h": str(h),
        "minimum_proposal_rate": str(r),
        "unitary": [[str(x) for x in row] for row in U.tolist()],
        "matrix_units_checked": 4,
        "determinant_at_rate_r_minus_one_hundredth": str(lower_minor.det()),
    }


def amplitude_damping_completion():
    L = s.Matrix([[0, 1], [0, 0]])
    e0 = s.diag(1, 0)
    for rho in units(2):
        zero(dissipator(L, rho) + (Z * rho * Z - rho) / 4 - (s.trace(rho) * e0 - rho))
    return {
        "case": "amplitude_damping_plus_Z_floor_is_reset_proposals",
        "lambda": "1",
        "Z_floor_rate": "1/4",
        "proposal_rate": "1",
        "matrix_units_checked": 4,
    }


def locality_counts():
    m = 486
    one_body = 3 * m
    two_body_closure = one_body + 9 * s.binomial(m, 2)
    assert one_body == 1458
    return {
        "case": "catalog_resource_counts_not_performance_evidence",
        "patch_qubits": m,
        "full_Pauli_directions": str(4**m - 1),
        "one_body_Pauli_modes": one_body,
        "all_weight_at_most_two_modes": int(two_body_closure),
        "Hamiltonian_tolerance_denominator_in_nu_units": str(2 * s.sqrt(one_body)),
        "note": "Low Pauli weight is not by itself a strictly few-site Lindblad-jump promise.",
    }


def main():
    cases = [signed_gram_example(), missing_directions(), sharp_pauli_identity(), amplitude_damping_completion(), locality_counts()]
    result = {
        "status": "PASS_EXACT_FINITE_ALGEBRA_ONLY",
        "arithmetic": "SymPy rational, Gaussian rational and exact radicals; no floating-point pass tolerance",
        "claims_not_tested": ["universal memory good-schedule interface", "asymptotic lifetime", "historical novelty", "physical implementation", "practical advantage"],
        "cases": cases,
    }
    out = Path(__file__).resolve().parent / "STRUCTURED_GRAM_CHECKS.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "cases": len(cases), "signed_example_r_min": cases[0]["minimum_proposal_rate"], "output": str(out)}))


if __name__ == "__main__":
    main()

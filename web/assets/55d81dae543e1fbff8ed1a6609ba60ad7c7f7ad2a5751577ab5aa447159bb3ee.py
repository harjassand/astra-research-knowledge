#!/usr/bin/env python3
"""Exact small fixtures for the N62 compressed-Gram and g(c) formulas.

Requires SymPy. All matrix and eigenvalue identities below are exact. The
fixtures are finite diagnostics only; they do not prove the general theorem.
Run from any directory with:

    python3 exact_fixtures.py

The script writes fixtures.json beside itself.
"""

from __future__ import annotations

import json
from pathlib import Path
from itertools import product

import sympy as sp


X = sp.symbols("x")


def kron_power(matrix: sp.Matrix, n: int) -> sp.Matrix:
    out = sp.Matrix([[1]])
    for _ in range(n):
        out = sp.kronecker_product(out, matrix)
    return out


def block_diag(*blocks: sp.Matrix) -> sp.Matrix:
    return sp.diag(*blocks)


def energy_indices(local_energies: list[sp.Expr], n: int, ceiling: sp.Expr) -> list[int]:
    """Indices of tensor basis states whose exact additive energy is <= ceiling."""
    selected: list[int] = []
    for index, word in enumerate(product(range(len(local_energies)), repeat=n)):
        energy = sp.simplify(sum(local_energies[j] for j in word))
        sign = sp.simplify(ceiling - energy).is_nonnegative
        if sign is True:
            selected.append(index)
        elif sign is not False:
            raise AssertionError(f"could not decide exact cutoff comparison: {ceiling} vs {energy}")
    return selected


def compress(matrix: sp.Matrix, indices: list[int]) -> sp.Matrix:
    return matrix.extract(indices, indices)


def eigenvalues_with_multiplicity(matrix: sp.Matrix) -> dict[sp.Expr, int]:
    return {sp.simplify(value): multiplicity for value, multiplicity in matrix.eigenvals().items()}


def assert_is_minimum(matrix: sp.Matrix, candidate: sp.Expr) -> None:
    candidate = sp.simplify(candidate)
    assert sp.simplify(matrix.charpoly(X).as_expr().subs(X, candidate)) == 0
    for value in eigenvalues_with_multiplicity(matrix):
        gap = sp.simplify(value - candidate)
        assert gap.is_nonnegative is True or gap == 0, (value, candidate, gap)


def assert_is_maximum(matrix: sp.Matrix, candidate: sp.Expr) -> None:
    candidate = sp.simplify(candidate)
    assert sp.simplify(matrix.charpoly(X).as_expr().subs(X, candidate)) == 0
    for value in eigenvalues_with_multiplicity(matrix):
        gap = sp.simplify(candidate - value)
        assert gap.is_nonnegative is True or gap == 0, (candidate, value, gap)


def verify_reciprocal_characteristic_polynomials(gram: sp.Matrix, inverse_gram: sp.Matrix) -> None:
    """Check that the compressed Gram spectra are exact reciprocals."""
    degree = gram.rows
    gram_det = sp.factor(gram.det())
    gram_poly = gram.charpoly(X).as_expr()
    inverse_poly = inverse_gram.charpoly(X).as_expr()
    reciprocal = sp.cancel((-1) ** degree * X**degree * gram_poly.subs(X, 1 / X) / gram_det)
    assert sp.simplify(inverse_poly - reciprocal) == 0


def verify_pair(
    *,
    name: str,
    effect: sp.Matrix,
    cholesky: sp.Matrix,
    local_energies: list[sp.Expr],
    n: int,
    ceiling: sp.Expr,
    expected_p: sp.Expr,
) -> dict[str, object]:
    """Directly compare p_n(Q) with ||B^tensor n P||^{-2} by exact spectra."""
    effect = effect.applyfunc(sp.simplify)
    cholesky = cholesky.applyfunc(sp.simplify)
    expected_p = sp.simplify(expected_p)
    assert (effect - cholesky.T * cholesky).applyfunc(sp.simplify) == sp.zeros(effect.rows)

    inverse = cholesky.inv().applyfunc(sp.simplify)
    A = (inverse.T * inverse).applyfunc(sp.simplify)
    indices = energy_indices(local_energies, n, ceiling)
    assert indices, "the ground vector must always be legal"

    gram = compress(kron_power(effect, n), indices).applyfunc(sp.simplify)
    inverse_gram = compress(kron_power(A, n), indices).applyfunc(sp.simplify)
    assert_is_minimum(gram, expected_p)
    assert_is_maximum(inverse_gram, 1 / expected_p)
    verify_reciprocal_characteristic_polynomials(gram, inverse_gram)

    return {
        "case": name,
        "n": n,
        "Q": str(sp.simplify(ceiling)),
        "legal_dimension": len(indices),
        "p_n(Q)_exact": str(expected_p),
        "||B^tensor_n P||^2_exact": str(sp.simplify(1 / expected_p)),
        "reciprocal_spectra_exact": True,
    }


def assert_nonnegative(expr: sp.Expr) -> None:
    expr = sp.simplify(expr)
    assert expr.is_nonnegative is True or expr == 0, expr


def main() -> None:
    sqrt2 = sp.sqrt(2)

    # A degenerate positive energy level H_+=I_2, with a rational non-diagonal
    # effect block. The upper triangular factor is rational as well.
    Tdeg_plus = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 3)],
                           [0, sp.Rational(1, 2)]])
    Edeg_plus = (Tdeg_plus.T * Tdeg_plus).applyfunc(sp.simplify)
    Tdeg = block_diag(sp.Matrix([[1]]), Tdeg_plus)
    Edeg = (Tdeg.T * Tdeg).applyfunc(sp.simplify)
    local_deg = [sp.Integer(0), sp.Integer(1), sp.Integer(1)]
    lam_minus = sp.simplify((11 - 2 * sp.sqrt(10)) / 36)
    lam_plus = sp.simplify((11 + 2 * sp.sqrt(10)) / 36)
    assert Edeg_plus == sp.Matrix([[sp.Rational(1, 4), sp.Rational(1, 6)],
                                   [sp.Rational(1, 6), sp.Rational(13, 36)]])
    assert sp.simplify(Edeg_plus.charpoly(X).as_expr().subs(X, lam_minus)) == 0
    assert sp.simplify(Edeg_plus.charpoly(X).as_expr().subs(X, lam_plus)) == 0
    assert_is_minimum(Edeg_plus, lam_minus)
    assert_is_maximum(Edeg_plus, lam_plus)
    assert_nonnegative(1 - lam_plus)
    Ldeg = sp.log(1 / lam_minus)

    degenerate_rows = []
    for n in (1, 2, 3):
        for q in range(n + 1):
            p = lam_minus**q
            degenerate_rows.append(verify_pair(
                name="degenerate_energy_block",
                effect=Edeg,
                cholesky=Tdeg,
                local_energies=local_deg,
                n=n,
                ceiling=sp.Integer(q),
                expected_p=p,
            ))

    # Rotate only within the exactly degenerate energy-1 eigenspace. This
    # changes the displayed matrix while preserving the hard-support problem.
    U = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                   [sp.Rational(4, 5), sp.Rational(3, 5)]])
    assert U.T * U == sp.eye(2)
    Edeg_plus_rot = (U.T * Edeg_plus * U).applyfunc(sp.simplify)
    Edeg_rot = block_diag(sp.Matrix([[1]]), Edeg_plus_rot)
    Tdeg_rot = Edeg_rot.cholesky().T.applyfunc(sp.simplify)
    rotated_rows = []
    for n, q in ((1, 1), (2, 1), (2, 2)):
        rotated_rows.append(verify_pair(
            name="degenerate_energy_block_rotated_basis",
            effect=Edeg_rot,
            cholesky=Tdeg_rot,
            local_energies=local_deg,
            n=n,
            ceiling=sp.Integer(q),
            expected_p=lam_minus**q,
        ))
    assert sp.simplify(Edeg_plus_rot.charpoly(X).as_expr() - Edeg_plus.charpoly(X).as_expr()) == 0

    # N62's source qutrit: H=diag(0,1,2), E=1 direct-sum E_+.
    Tq_plus = sp.Matrix([[1 / sqrt2, sp.Rational(1, 2)],
                         [0, 1 / sqrt2]])
    Eq_plus = (Tq_plus.T * Tq_plus).applyfunc(sp.simplify)
    Tq = block_diag(sp.Matrix([[1]]), Tq_plus)
    Eq = (Tq.T * Tq).applyfunc(sp.simplify)
    local_q = [sp.Integer(0), sp.Integer(1), sp.Integer(2)]
    R = sp.simplify((1 + sp.sqrt(17)) / 2)
    sH = sp.log(R)
    h_star = sp.simplify((17 - sp.sqrt(17)) / 10)
    qutrit_expected = {
        0: sp.Integer(1),
        1: sp.Rational(1, 2),
        2: sp.Rational(1, 4),
        3: sp.simplify((3 - sp.sqrt(5)) / 8),
        4: sp.Rational(1, 16),
    }
    qutrit_rows = []
    for q, p in qutrit_expected.items():
        qutrit_rows.append(verify_pair(
            name="N62_qutrit",
            effect=Eq,
            cholesky=Tq,
            local_energies=local_q,
            n=2,
            ceiling=sp.Integer(q),
            expected_p=p,
        ))

    # Exact top-space degeneracy at the threshold. The ground eigenvalue of
    # the full tilt is 1; the excited block also has eigenvalue 1.
    A_q = (Tq.inv().T * Tq.inv()).applyfunc(sp.simplify)
    tilt_excited = sp.diag(R ** sp.Rational(-1, 2), R ** -1) * A_q[1:3, 1:3] * sp.diag(
        R ** sp.Rational(-1, 2), R ** -1
    )
    assert sp.simplify((sp.eye(2) - tilt_excited).det()) == 0
    other_tilt_eigenvalue = sp.simplify(tilt_excited.det())
    assert_nonnegative(1 - other_tilt_eigenvalue)
    assert sp.simplify(other_tilt_eigenvalue - 4 / R**3) == 0

    # Exact g(c) checks in the source's low-density branch and plateau.
    # For 0<=c<=h_star, g(c)=c log R; for c>=5/3, g(c)=log 4.
    qutrit_g_rows = []
    for n, c in ((1, sp.Rational(1, 2)), (2, sp.Rational(1, 2)),
                 (2, sp.Integer(1)), (2, sp.Integer(2))):
        ceiling = n * c
        q = int(sp.floor(ceiling))
        p = qutrit_expected[q]
        if c <= 1:  # 1 < h_star, so these lie in the exact linear branch.
            predicted = R ** (-n * c)
            ng = n * c * sH
            branch = "c log(R)"
        else:
            predicted = sp.Rational(1, 4) ** n
            ng = n * sp.log(4)
            branch = "log(4) plateau"
        assert_nonnegative(p - predicted)
        qutrit_g_rows.append({
            "n": n,
            "c": str(c),
            "Q=nc": str(ceiling),
            "exact_p": str(p),
            "exact_g_branch": branch,
            "exact_exp_minus_ng": str(sp.simplify(predicted)),
            "F_n_minus_ng_decimal": str(sp.N(-sp.log(p) - ng, 18)),
            "F_n_le_ng_exact": True,
        })

    # The degenerate-block g curve is closed form on the full half-line.
    # At c=1/4 with n=2 the finite floor effect is visible; c=1/2 and c=1
    # hit exact types.
    degenerate_g_rows = []
    for n, c in ((2, sp.Rational(1, 4)), (2, sp.Rational(1, 2)),
                 (2, sp.Integer(1)), (2, sp.Rational(3, 2))):
        q = min(n, int(sp.floor(n * c)))
        p = lam_minus**q
        g = sp.Min(c, 1) * Ldeg
        predicted = lam_minus ** (n * sp.Min(c, 1))
        assert_nonnegative(p - predicted)
        degenerate_g_rows.append({
            "n": n,
            "c": str(c),
            "Q=nc": str(n * c),
            "exact_p": str(sp.simplify(p)),
            "exact_g": "min(c,1)*log(1/lambda_minus)",
            "lambda_minus": str(lam_minus),
            "exact_exp_minus_ng": str(sp.simplify(predicted)),
            "F_n_minus_ng_decimal": str(sp.N(-sp.log(p) - n * g, 18)),
            "F_n_le_ng_exact": True,
        })

    payload = {
        "status": "FINITE-EVIDENCE",
        "scope": "Exact small matrices and selected exact g(c) branches only; not a proof of N62.",
        "source": "N62 source d-073e71b6349e6f34, local archive work/astra_prior/web/pages/d-073e71b6349e6f34.html",
        "degenerate_energy": {
            "H_diagonal": [0, 1, 1],
            "E_plus": [["1/4", "1/6"], ["1/6", "13/36"]],
            "E_plus_eigenvalues": [str(lam_minus), str(lam_plus)],
            "g(c)": "min(c,1)*log(1/lambda_minus)",
            "exact_p_checks": degenerate_rows,
            "rotated_basis_checks": rotated_rows,
            "rotated_E_plus": [[str(v) for v in row] for row in Edeg_plus_rot.tolist()],
            "basis_rotation_preserves_characteristic_polynomial": True,
            "g_checks": degenerate_g_rows,
        },
        "N62_qutrit": {
            "H_diagonal": [0, 1, 2],
            "E_plus": [["1/2", "sqrt(2)/4"], ["sqrt(2)/4", "3/4"]],
            "R": str(R),
            "s_H": "log(R)",
            "h_star": str(h_star),
            "p_2(Q)_for_Q_0_to_4": {str(q): str(p) for q, p in qutrit_expected.items()},
            "exact_p_checks": qutrit_rows,
            "tilted_top_space": {
                "ground_eigenvalue": "1",
                "excited_eigenvalue": "1",
                "other_excited_eigenvalue": str(other_tilt_eigenvalue),
                "top_eigenvalue_degeneracy_at_sH": 2,
            },
            "g_checks": qutrit_g_rows,
        },
        "identity_checked": "charpoly(P E^tensor_n P) and charpoly(P A^tensor_n P) are reciprocal exactly; p is the first minimum eigenvalue, and inverse norm squared is the second maximum eigenvalue.",
        "limitations": [
            "Only dimensions 3 and tensor counts at most 3 for the degenerate fixture and 2 for the qutrit are checked.",
            "No general proof, novelty assessment, or external validation follows from these calculations.",
            "The qutrit g(c) assertion is checked on source-stated exact branches, not over the full intermediate interval.",
        ],
    }
    path = Path(__file__).with_name("fixtures.json")
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path}")
    print(f"exact compressed-Gram cases: {len(degenerate_rows) + len(rotated_rows) + len(qutrit_rows)}")
    print("all exact assertions passed")


if __name__ == "__main__":
    main()

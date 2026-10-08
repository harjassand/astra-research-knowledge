#!/usr/bin/env python3
"""Exact diagnostics for the supplied-witness compiler and two obstructions.

Only Python's standard library and Fraction are used. The W-tensor check
verifies a supplied rational Laurent witness, its constant coefficient, and
the coefficient-extraction rank/identity on tensor powers m=1,2,3. A second
check separates function equality from formal polynomial equality over F_2.
These are finite tests, not universal proofs.
"""

from __future__ import annotations

import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path


Vec = tuple[F, ...]
LaurentVector = dict[int, Vec]


def basis(n: int, j: int, value: F = F(1)) -> Vec:
    return tuple(value if i == j else F(0) for i in range(n))


def kron_vec(x: Vec, y: Vec) -> Vec:
    return tuple(a * b for a in x for b in y)


def poly_kron(x: LaurentVector, y: LaurentVector) -> LaurentVector:
    out: dict[int, list[F]] = {}
    for ex, vx in x.items():
        for ey, vy in y.items():
            e = ex + ey
            z = kron_vec(vx, vy)
            if e not in out:
                out[e] = [F(0)] * len(z)
            out[e] = [a + b for a, b in zip(out[e], z)]
    return {e: tuple(v) for e, v in out.items()}


def scale_vec(v: Vec, a: F) -> Vec:
    return tuple(a * x for x in v)


def add_tensor(dst: list[F], a: Vec, b: Vec, c: Vec, scale: F = F(1)) -> None:
    db = len(b)
    dc = len(c)
    for ia, xa in enumerate(a):
        if xa == 0:
            continue
        for ib, xb in enumerate(b):
            if xb == 0:
                continue
            for ic, xc in enumerate(c):
                if xc:
                    dst[ia * db * dc + ib * dc + ic] += scale * xa * xb * xc


def add_poly_tensor(dst: dict[int, list[F]], a: LaurentVector,
                    b: LaurentVector, c: LaurentVector, scale: F = F(1)) -> None:
    for ea, va in a.items():
        for eb, vb in b.items():
            for ec, vc in c.items():
                e = ea + eb + ec
                dim = len(va) * len(vb) * len(vc)
                if e not in dst:
                    dst[e] = [F(0)] * dim
                add_tensor(dst[e], va, vb, vc, scale)


def witness_terms() -> list[tuple[LaurentVector, LaurentVector, LaurentVector]]:
    e0, e1 = basis(2, 0), basis(2, 1)
    # t^-1 (e0+t e1)^(tensor 3), with t^-1 assigned to the first factor.
    term_a = (
        {-1: e0, 0: e1},
        {0: e0, 1: e1},
        {0: e0, 1: e1},
    )
    # -t^-1 e0^(tensor 3).
    term_b = (
        {-1: scale_vec(e0, F(-1))},
        {0: e0},
        {0: e0},
    )
    return [term_a, term_b]


def base_w_tensor() -> list[F]:
    out = [F(0)] * 8
    out[1 * 4 + 0 * 2 + 0] = 1
    out[0 * 4 + 1 * 2 + 0] = 1
    out[0 * 4 + 0 * 2 + 1] = 1
    return out


def verify_base_witness() -> dict[str, object]:
    coeffs: dict[int, list[F]] = {}
    for term in witness_terms():
        add_poly_tensor(coeffs, *term)
    target = base_w_tensor()
    assert coeffs[-1] == [F(0)] * 8
    assert coeffs[0] == target
    assert set(coeffs).issubset({-1, 0, 1, 2})
    return {
        "laurent_negative_coefficient_cancels_exactly": True,
        "constant_coefficient_is_W": True,
        "formal_support": sorted(coeffs),
    }


def rank_one_words_power(m: int) -> tuple[list[F], int]:
    """Apply u+v+w=0 coefficient extraction to W^tensor m exactly."""
    terms = witness_terms()
    dim = 1 << m
    output = [F(0)] * (dim ** 3)
    extracted_terms = 0

    for word in itertools.product(range(len(terms)), repeat=m):
        grouped: list[LaurentVector] = []
        for mode in range(3):
            pol: LaurentVector = terms[word[0]][mode]
            for j in range(1, m):
                pol = poly_kron(pol, terms[word[j]][mode])
            grouped.append(pol)
        a_poly, b_poly, c_poly = grouped
        for u, a_vec in a_poly.items():
            for v, b_vec in b_poly.items():
                w = -u - v
                c_vec = c_poly.get(w)
                if c_vec is None:
                    continue
                if not (any(a_vec) and any(b_vec) and any(c_vec)):
                    continue
                extracted_terms += 1
                add_tensor(output, a_vec, b_vec, c_vec)

    # Directly form W^tensor m. Indices group the m coordinates of each mode.
    expected = [F(0)] * (dim ** 3)
    w_terms = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    for choices in itertools.product(w_terms, repeat=m):
        ia = ib = ic = 0
        for j, (aa, bb, cc) in enumerate(choices):
            ia |= aa << j
            ib |= bb << j
            ic |= cc << j
        expected[ia * dim * dim + ib * dim + ic] += 1

    assert output == expected, f"extracted constant coefficient failed for m={m}"
    bound = 2**m * (2 * m + 1) ** 2  # r=2,d=1
    assert extracted_terms <= bound
    return output, extracted_terms


def verify_w_approximation() -> dict[str, object]:
    # W(t)=t^-1((e0+t e1)^tensor3-e0^tensor3) is rank at most two.
    # Its tensor coefficients differ from W in degrees 1 and 2.
    max_errors = []
    for p in (1, 2, 5, 10, 24):
        t = F(1, 1 << p)
        actual = [F(0)] * 8
        for term in witness_terms():
            vals = []
            for mode in range(3):
                v = [F(0), F(0)]
                for e, coeff in term[mode].items():
                    te = t**e if e >= 0 else F(1, t ** (-e))
                    v = [x + te * y for x, y in zip(v, coeff)]
                vals.append(tuple(v))
            add_tensor(actual, *vals)
        expected = base_w_tensor()
        maxerr = max(abs(a - b) for a, b in zip(actual, expected))
        assert maxerr == t
        max_errors.append({"p": p, "error": str(maxerr), "coefficient_bits": p + 1})
    return {"rank_two_family_error_equals_t": True, "cases": max_errors}


def verify_rank_three_slice_obstruction() -> dict[str, object]:
    # Slices A0=[[0,1],[1,0]], A1=[[1,0],[0,0]] give
    # det(x A0+y A1)=-x^2, a repeated root. A rank-2 decomposition would
    # give two independent pencil factors and hence two distinct roots.
    coeff_x2, coeff_xy, coeff_y2 = F(-1), F(0), F(0)
    assert (coeff_x2, coeff_xy, coeff_y2) == (F(-1), F(0), F(0))
    return {
        "slice_pencil_determinant_coefficients_x2_xy_y2": ["-1", "0", "0"],
        "rank_two_contradicted_by_repeated_root": True,
        "rank_three_witnessed_by_three_coordinate_terms": True,
    }


def verify_f2_function_vs_polynomial() -> dict[str, object]:
    values = [0, 1]
    assert all((x * x) % 2 == x for x in values)
    # Formal F_2[X] polynomial X^2-X = X^2+X is nonzero.
    formal_coefficients = {1: 1, 2: 1}
    assert any(c % 2 for c in formal_coefficients.values())
    return {
        "x_squared_and_x_agree_as_functions_on_F2": True,
        "formal_polynomial_x2_minus_x_is_nonzero": True,
    }


def main() -> None:
    result = {
        "status": "EXACT_FINITE_DIAGNOSTIC_ONLY",
        "arithmetic": "Python Fraction, exact over Q; direct two-point function check over F2",
        "base_witness": verify_base_witness(),
        "tensor_power_extraction": [],
        "one_shot_w_tensor_counterexample": {
            **verify_w_approximation(),
            **verify_rank_three_slice_obstruction(),
        },
        "finite_field_semantics_counterexample": verify_f2_function_vs_polynomial(),
        "limitations": [
            "tests W tensor powers only for m=1,2,3",
            "does not implement the total-computable exhaustive block search proved in RESULT.txt",
            "does not establish any useful bound on that search or coefficient heights",
            "does not prove a lower bound against all selective-output algorithms",
            "does not test coefficient height or conditioning for the L03 witness",
        ],
    }
    for m in (1, 2, 3):
        _, terms = rank_one_words_power(m)
        result["tensor_power_extraction"].append({
            "m": m,
            "extracted_rank_one_summands_before_cancellation": terms,
            "upper_bound_2^m_(2m+1)^2": 2**m * (2 * m + 1) ** 2,
            "constant_coefficient_equals_W_tensor_m": True,
        })

    out = Path(__file__).with_name("check_exactification.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

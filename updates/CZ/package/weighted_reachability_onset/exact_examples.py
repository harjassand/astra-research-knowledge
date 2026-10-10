#!/usr/bin/env python3
"""Exact qubit Lindblad examples for the weighted row-core calculation.

Everything here is over SymPy's exact rational/Gaussian-rational domain.  The
Choi matrices are Taylor-expanded by powers of the exact 4-by-4 generator;
eigenvalue orders are read from the exact Newton polygon of the characteristic
polynomial, never from floating-point eigenvalues.

Run from any directory with:

    python3 exact_examples.py

The script writes only the sibling ``exact_examples.json`` artifact.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


T = sp.Symbol("t")
DIM = 2
TAYLOR_ORDER = 12


def row_major_vector(matrix: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(
        [matrix[row, col] for row in range(matrix.rows) for col in range(matrix.cols)]
    )


def matrix_json(matrix: sp.MatrixBase) -> list[list[str]]:
    return [
        [sp.sstr(sp.cancel(matrix[row, col])) for col in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def vector_json(vector: sp.MatrixBase) -> list[str]:
    return [sp.sstr(sp.cancel(value)) for value in vector]


def lindblad_generator(
    rho: sp.MatrixBase, hamiltonian: sp.MatrixBase, jump: sp.MatrixBase
) -> sp.Matrix:
    """Return -i[H,rho] + L rho L^* - {L^*L,rho}/2 exactly."""
    jump_star = jump.conjugate().T
    return sp.simplify(
        -sp.I * (hamiltonian * rho - rho * hamiltonian)
        + jump * rho * jump_star
        - (jump_star * jump * rho + rho * jump_star * jump) / 2
    )


def generator_superoperator(
    hamiltonian: sp.MatrixBase, jump: sp.MatrixBase
) -> sp.Matrix:
    """Matrix of the generator in the row-major matrix-unit basis."""
    units = []
    for row in range(DIM):
        for col in range(DIM):
            unit = sp.zeros(DIM)
            unit[row, col] = 1
            units.append(unit)
    return sp.Matrix.hstack(
        *[
            row_major_vector(lindblad_generator(unit, hamiltonian, jump))
            for unit in units
        ]
    )


def choi_taylor_coefficients(
    superoperator: sp.MatrixBase, order: int
) -> list[sp.Matrix]:
    """Return J_n with J(t)=sum_{n=0}^order J_n t^n, using S^n/n!."""
    units = []
    for row in range(DIM):
        for col in range(DIM):
            unit = sp.zeros(DIM)
            unit[row, col] = 1
            units.append(unit)

    power = sp.eye(DIM * DIM)
    coefficients: list[sp.Matrix] = []
    for degree in range(order + 1):
        coefficient = sp.zeros(DIM * DIM)
        for input_row in range(DIM):
            for input_col in range(DIM):
                unit_index = input_row * DIM + input_col
                image = power * row_major_vector(units[unit_index]) / math.factorial(degree)
                for output_row in range(DIM):
                    for output_col in range(DIM):
                        # Choi basis is input tensor output, with index (i,a).
                        coefficient[
                            input_row * DIM + output_row,
                            input_col * DIM + output_col,
                        ] += image[output_row * DIM + output_col]
        coefficients.append(coefficient.applyfunc(sp.simplify))
        power = power * superoperator
    return coefficients


def polynomial_matrix(coefficients: list[sp.Matrix]) -> sp.Matrix:
    return sp.Matrix(
        DIM * DIM,
        DIM * DIM,
        lambda row, col: sp.Add(
            *[
                coefficients[degree][row, col] * T**degree
                for degree in range(len(coefficients))
            ]
        ),
    )


def leading_term(expression: sp.Expr) -> dict[str, Any]:
    polynomial = sp.Poly(sp.expand(expression), T, domain="EX")
    terms = [(monomial[0], coeff) for monomial, coeff in polynomial.terms() if coeff != 0]
    if not terms:
        return {"order": None, "coefficient": "0"}
    order = min(degree for degree, _ in terms)
    coefficient = sp.cancel(polynomial.nth(order))
    return {"order": int(order), "coefficient": sp.sstr(coefficient)}


def principal_minor_sum(matrix: sp.MatrixBase, size: int) -> sp.Expr:
    total = sp.S.Zero
    for indices in __import__("itertools").combinations(range(matrix.rows), size):
        total += matrix.extract(indices, indices).det(method="domain-ge")
    return sp.expand(total)


def characteristic_newton_data(choi: sp.MatrixBase) -> dict[str, Any]:
    """For det(lambda I-J), return coefficient valuations and Newton slopes."""
    dimension = choi.rows
    # det(lambda I-J) = sum_k (-1)^k e_k(J) lambda^(d-k), e_0=1.
    lambda_coefficients: list[sp.Expr] = [sp.S.Zero] * (dimension + 1)
    lambda_coefficients[dimension] = sp.S.One
    elementary: list[sp.Expr] = [sp.S.One]
    for size in range(1, dimension + 1):
        elementary.append(principal_minor_sum(choi, size))
        lambda_coefficients[dimension - size] = (-1) ** size * elementary[size]

    data = []
    points: list[tuple[int, int]] = []
    for lambda_power, coefficient in enumerate(lambda_coefficients):
        lead = leading_term(coefficient)
        data.append(
            {
                "lambda_power": lambda_power,
                "t_valuation": lead["order"],
                "leading_coefficient": lead["coefficient"],
            }
        )
        if lead["order"] is not None:
            points.append((lambda_power, lead["order"]))

    # Lower convex hull, in increasing lambda-power order.
    hull: list[tuple[int, int]] = []
    for point in points:
        while len(hull) >= 2:
            x0, y0 = hull[-2]
            x1, y1 = hull[-1]
            x2, y2 = point
            previous_slope = sp.Rational(y1 - y0, x1 - x0)
            next_slope = sp.Rational(y2 - y1, x2 - x1)
            if previous_slope < next_slope:
                break
            hull.pop()
        hull.append(point)

    segments = []
    eigenvalue_orders: list[int] = []
    for (x0, y0), (x1, y1) in zip(hull, hull[1:]):
        slope = sp.Rational(y1 - y0, x1 - x0)
        order = -slope
        segments.append(
            {
                "from": [x0, y0],
                "to": [x1, y1],
                "slope": sp.sstr(slope),
                "root_valuation": sp.sstr(order),
                "multiplicity": x1 - x0,
            }
        )
        if order.q == 1 and order > 0:
            eigenvalue_orders.extend([int(order)] * (x1 - x0))

    return {
        "lambda_coefficients_low_to_high": data,
        "newton_polygon_points": [list(point) for point in hull],
        "newton_polygon_segments": segments,
        "positive_eigenvalue_t_valuations": sorted(eigenvalue_orders),
        "all_eigenvalue_t_valuations": [0] + sorted(eigenvalue_orders),
    }


def independent_matrix_basis(matrices: list[sp.MatrixBase]) -> list[sp.Matrix]:
    if not matrices:
        return []
    columns = sp.Matrix.hstack(*[row_major_vector(matrix) for matrix in matrices])
    return [sp.Matrix(DIM, DIM, list(vector)) for vector in columns.columnspace()]


def weighted_closure(
    jump: sp.MatrixBase, no_jump_generator: sp.MatrixBase, max_grade: int = 5
) -> list[dict[str, Any]]:
    """Build F_r from L-left-multiplication (cost 1) and [G,.] (cost 2)."""
    filtration: dict[int, list[sp.Matrix]] = {0: [sp.eye(DIM)]}
    result = []
    for grade in range(max_grade + 1):
        if grade > 0:
            candidates = list(filtration[grade - 1])
            candidates += [jump * matrix for matrix in filtration[grade - 1]]
            if grade >= 2:
                candidates += [
                    no_jump_generator * matrix - matrix * no_jump_generator
                    for matrix in filtration[grade - 2]
                ]
            filtration[grade] = independent_matrix_basis(candidates)

        basis = filtration[grade]
        basis_columns = sp.Matrix.hstack(*[row_major_vector(matrix) for matrix in basis])
        # F_r^perp is the exact nullspace of the conjugate transpose.
        perpendicular_vectors = basis_columns.conjugate().T.nullspace()
        constraints: list[list[sp.Expr]] = []
        for vector in perpendicular_vectors:
            q = sp.Matrix(DIM, DIM, list(vector))
            # P_perp kills b tensor e_j for every j iff these rows annihilate b.
            for input_basis_index in range(DIM):
                constraints.append(
                    [
                        sp.conjugate(q[output_index, input_basis_index])
                        for output_index in range(DIM)
                    ]
                )
        constraint_matrix = sp.Matrix(constraints) if constraints else sp.zeros(0, DIM)
        core_basis = constraint_matrix.nullspace()
        result.append(
            {
                "grade": grade,
                "filtration_dimension": len(basis),
                "filtration_basis_row_major": [matrix_json(matrix) for matrix in basis],
                "perpendicular_dimension": len(perpendicular_vectors),
                "row_core_constraint_rank": int(constraint_matrix.rank()),
                "row_core_dimension": len(core_basis),
                "row_core_basis": [vector_json(vector) for vector in core_basis],
            }
        )
    return result


def build_example(name: str, hamiltonian: sp.Matrix, jump: sp.Matrix) -> dict[str, Any]:
    no_jump_generator = -sp.I * hamiltonian - jump.conjugate().T * jump / 2
    superoperator = generator_superoperator(hamiltonian, jump)
    choi_coefficients = choi_taylor_coefficients(superoperator, TAYLOR_ORDER)
    choi = polynomial_matrix(choi_coefficients)

    determinant = sp.expand(choi.det(method="domain-ge"))
    adjugate = choi.adjugate()
    partial_trace_input = sp.Matrix(
        DIM,
        DIM,
        lambda row, col: sp.expand(
            sum(
                adjugate[input_index * DIM + row, input_index * DIM + col]
                for input_index in range(DIM)
            )
        ),
    )
    determinant_a = sp.expand(partial_trace_input.det(method="domain-ge"))
    trace_adjugate_a = sp.expand(sp.trace(partial_trace_input.adjugate()))

    lead_det = leading_term(determinant)
    lead_det_a = leading_term(determinant_a)
    lead_trace_adjugate_a = leading_term(trace_adjugate_a)
    h_order = (
        lead_det["order"]
        + lead_trace_adjugate_a["order"]
        - lead_det_a["order"]
    )
    h_coefficient = sp.cancel(
        sp.Rational(lead_det["coefficient"])
        * sp.Rational(lead_trace_adjugate_a["coefficient"])
        / sp.Rational(lead_det_a["coefficient"])
    )

    characteristic = characteristic_newton_data(choi)
    return {
        "name": name,
        "hamiltonian": matrix_json(hamiltonian),
        "jump": matrix_json(jump),
        "generator_superoperator_row_major": matrix_json(superoperator),
        "choi_taylor_order": TAYLOR_ORDER,
        "choi_taylor_coefficients": [matrix_json(matrix) for matrix in choi_coefficients],
        "determinant_choi_leading": lead_det,
        "A_is_partial_trace_input_of_adjugate_choi": True,
        "determinant_A_leading": lead_det_a,
        "trace_adjugate_A_leading": lead_trace_adjugate_a,
        "h_leading": {
            "order": int(h_order),
            "coefficient": sp.sstr(h_coefficient),
            "definition": "det(J) * Tr(adj(A)) / det(A)",
        },
        "characteristic_newton_data": characteristic,
        "no_jump_generator_G": matrix_json(no_jump_generator),
        "beta_exponent_from_h_order": int(h_order),
        "weighted_closure": weighted_closure(jump, no_jump_generator),
    }


def main() -> None:
    x_pauli = sp.Matrix([[0, 1], [1, 0]])
    z_pauli = sp.diag(1, -1)
    hamiltonian = x_pauli / 2
    examples = {
        "amplitude_damping": build_example(
            "Driven amplitude damping", hamiltonian, sp.Matrix([[0, 1], [0, 0]])
        ),
        "dephasing": build_example("Driven dephasing", hamiltonian, z_pauli),
    }
    output = {
        "schema_version": 1,
        "conventions": {
            "hilbert_dimension": DIM,
            "choi_normalization": "unnormalized: J(0)=|Omega><Omega|, |Omega>=|00>+|11>",
            "choi_tensor_order": "input tensor output, basis index (input, output)",
            "lindblad_generator": "-i[H,rho] + L rho L^* - {L^*L,rho}/2",
            "closure_scalar_field": "C; exact Gaussian-rational representatives are used",
            "closure_costs": {"left_multiply_by_L": 1, "commutator_with_G": 2},
            "row_core": "ker Tr_input(P_perp), equivalently all |b><x| lie in F_r",
            "beta_convention": (
                "the supplied bounds identify beta's exponent with ord_t(h) here; "
                "h's leading coefficient is reported separately and need not equal beta's"
            ),
            "no_jump_generator": "G=-iH-L^*L/2",
            "eigenvalue_orders": "exact Newton polygon valuations of det(lambda I-J(t))",
            "taylor_method": "J_n assembled from S^n/n! for n=0,...,12",
        },
        "examples": examples,
    }
    destination = Path(__file__).resolve().with_name("exact_examples.json")
    destination.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(destination)


if __name__ == "__main__":
    main()

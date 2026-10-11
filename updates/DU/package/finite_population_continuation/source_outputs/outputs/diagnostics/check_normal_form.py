#!/usr/bin/env python3
"""Finite exact checks for the independently derived normal form.

The universal result is the written proof, not these checks.
Only Python's standard library is used.
"""

from fractions import Fraction as Q
import json
import random
from pathlib import Path


def plus(a, b):
    result = dict(a)
    for monomial, coefficient in b.items():
        result[monomial] = result.get(monomial, Q(0)) + coefficient
        if not result[monomial]:
            del result[monomial]
    return result


def times(a, b):
    result = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(sorted(ma + mb))
            result[m] = result.get(m, Q(0)) + ca * cb
    return {m: c for m, c in result.items() if c}


def scaled(a, coefficient):
    return {m: coefficient * c for m, c in a.items() if coefficient * c}


def evaluate(polynomial, x):
    result = Q(0)
    for monomial, coefficient in polynomial.items():
        term = coefficient
        for variable in monomial:
            term *= x[variable]
        result += term
    return result


def monomial(*indices, coefficient=Q(1)):
    return {tuple(sorted(indices)): coefficient}


def centralize(polynomial):
    """Return 1/4 + (1/2) P(2y-1/2), expanded exactly."""
    result = {(): Q(1, 4)}
    for variables, coefficient in polynomial.items():
        term = {(): coefficient / 2}
        for variable in variables:
            term = times(term, {(): Q(-1, 2), (variable,): Q(2)})
        result = plus(result, term)
    return result


def compile_circuit(circuit):
    s = len(circuit)
    gamma = Q(1, 128 * s)
    rows = []
    values = []
    true_values = []
    for i, gate in enumerate(circuit):
        operation = gate[0]
        if operation in ("zero", "one"):
            p, q, lam = (Q(1, 8), Q(1, 8), Q(1, 8))
            if operation == "one":
                p = Q(1, 4)
            new_rows = [{(): p}, {(): q}, {(): lam}]
            true_value = int(operation == "one")
        else:
            a, b = gate[1:]
            pa, qa, la = (3 * a, 3 * a + 1, 3 * a + 2)
            pb, qb, lb = (3 * b, 3 * b + 1, 3 * b + 2)
            if operation == "add":
                p_terms = ((pa, lb), (pb, la))
                q_terms = ((qa, lb), (qb, la))
                true_value = true_values[a] + true_values[b]
            elif operation == "sub":
                p_terms = ((pa, lb), (qb, la))
                q_terms = ((qa, lb), (pb, la))
                true_value = true_values[a] - true_values[b]
            elif operation == "mul":
                p_terms = ((pa, pb), (qa, qb))
                q_terms = ((pa, qb), (qa, pb))
                true_value = true_values[a] * true_values[b]
            else:
                raise ValueError(operation)
            p_row = plus(*(monomial(*pair, coefficient=gamma) for pair in p_terms))
            q_row = plus(*(monomial(*pair, coefficient=gamma) for pair in q_terms))
            new_rows = [p_row, q_row, monomial(la, lb, coefficient=gamma)]
            p, q, lam = (evaluate(row, values) for row in new_rows)
        rows.extend(new_rows)
        values.extend((p, q, lam))
        true_values.append(true_value)
        assert lam > 0
        assert (p - q) / lam == true_value
        assert all(Q(0) < v <= Q(1, 4) for v in (p, q, lam))
    p_out, q_out = 3 * (s - 1), 3 * (s - 1) + 1
    z_row = {(): Q(1, 2), (p_out,): gamma, (q_out,): -gamma}
    z = evaluate(z_row, values)
    rows.append(z_row)
    values.append(z)
    assert (z > Q(1, 2)) == (true_values[-1] > 0)
    assert (z == Q(1, 2)) == (true_values[-1] == 0)
    assert all(Q(0) < v < Q(1) for v in values)
    objective = {}
    for i, row in enumerate(rows):
        residual = plus(monomial(i), scaled(row, Q(-1)))
        objective = plus(objective, scaled(times(residual, residual), Q(1, 2)))
    assert max(map(len, objective), default=0) <= 4
    assert evaluate(objective, values) == 0
    assert all(evaluate(row, values) == values[i] for i, row in enumerate(rows))
    central_rows = [centralize(row) for row in rows]
    central_values = [Q(1, 4) + value / 2 for value in values]
    central_objective = {}
    for i, row in enumerate(central_rows):
        residual = plus(monomial(i), scaled(row, Q(-1)))
        central_objective = plus(
            central_objective, scaled(times(residual, residual), Q(1, 2))
        )
    assert all(Q(1, 4) < value < Q(3, 4) for value in central_values)
    assert (central_values[-1] > Q(1, 2)) == (true_values[-1] > 0)
    assert evaluate(central_objective, central_values) == 0
    assert all(
        evaluate(row, central_values) == central_values[i]
        for i, row in enumerate(central_rows)
    )
    return {
        "s": s,
        "dimension": len(rows),
        "monomials": len(objective),
        "central_monomials": len(central_objective),
        "coefficient_bit_length_max": max(
            max(abs(c.numerator).bit_length(), c.denominator.bit_length())
            for c in objective.values()
        ),
        "output_positive": true_values[-1] > 0,
        "denominator_bits_z": z.denominator.bit_length(),
    }, z


def main():
    rng = random.Random(381275)
    reports = []
    for _ in range(120):
        circuit = [("zero",), ("one",)]
        s = rng.randrange(3, 11)
        for i in range(2, s):
            circuit.append((rng.choice(("add", "sub", "mul")), rng.randrange(i), rng.randrange(i)))
        report, _ = compile_circuit(circuit)
        reports.append(report)
    heights = []
    for n in range(7):
        circuit = [("one",)] + [("mul", i - 1, i - 1) for i in range(1, n + 1)]
        report, z = compile_circuit(circuit)
        s = n + 1
        expected = Q(1, 2) + Q(1, (1024 * s) ** (2 ** n))
        assert z == expected
        heights.append({"n": n, "s": s, "z_denominator_bits": z.denominator.bit_length()})
    # Explicit positive circuits with a double-exponentially small relative gap.
    a, b = 2, 1
    for n in range(8):
        assert a == 2 ** (2 ** n)
        assert a - b == 1
        assert Q(a - b, a) == Q(1, 2 ** (2 ** n))
        a, b = a * a, b * (b + 2)
    result = {
        "status": "FINITE_EXACT_CHECKS_PASS",
        "scope": "120 deterministic-seed small mixed circuits, seven height examples, eight positive-pair examples; no universal or novelty certification",
        "mixed_circuits": len(reports),
        "max_dimension": max(r["dimension"] for r in reports),
        "max_sparse_monomials": max(r["monomials"] for r in reports),
        "max_central_sparse_monomials": max(r["central_monomials"] for r in reports),
        "max_coefficient_bits": max(r["coefficient_bit_length_max"] for r in reports),
        "height_examples": heights,
        "global_analytic_bounds_used_in_proof": {
            "DT_infinity": "<= 1/(32s)",
            "DT_one": "<= 1/8",
            "DT_two": "<= 1/(16 sqrt(s)) <= 1/16",
            "residual_weighted_second_derivative_two": "<= 1/8",
            "hessian_lower": "193/256 > 1/2",
            "hessian_upper": "321/256 < 3/2"
        },
        "central_analytic_bounds_used_in_proof": {
            "DT_infinity": "<= 3/(64s)",
            "DT_one": "<= 3/16",
            "DT_two": "<= 3/(32 sqrt(s)) <= 3/32",
            "residual_weighted_second_derivative_two": "<= 1/4",
            "hessian_lower": "585/1024 > 1/2",
            "hessian_upper": "1481/1024 < 3/2",
            "optimizer_coordinates": "all in (1/4,3/4)"
        }
    }
    output = Path(__file__).with_name("FINITE_CHECKS.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

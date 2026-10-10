#!/usr/bin/env python3
"""Exact small fixtures for the rank-one-history/#SAT reduction.

The circuit uses only 2-local H tensor H (all entries +/-1/2), X, CNOT,
Toffoli and final single-qubit computational projectors. No dense global
Kraus matrix is constructed. This is a finite diagnostic, not a complexity
proof; the all-size reduction is in RESULT.txt.
"""

from collections import defaultdict
from fractions import Fraction
import json


def bit(word, index):
    return (word >> index) & 1


def apply_h2(state, left, right):
    result = defaultdict(Fraction)
    mask = (1 << left) | (1 << right)
    for word, amplitude in state.items():
        a, b = bit(word, left), bit(word, right)
        for u in (0, 1):
            for v in (0, 1):
                target = (word & ~mask) | (u << left) | (v << right)
                sign = -1 if (a * u + b * v) % 2 else 1
                result[target] += sign * amplitude / 2
    return {word: amp for word, amp in result.items() if amp}


def apply_permutation(state, gate):
    kind, wires = gate
    result = {}
    for word, amplitude in state.items():
        if kind == "X":
            target = word ^ (1 << wires[0])
        elif kind == "CX":
            target = word ^ ((bit(word, wires[0])) << wires[1])
        elif kind == "CCX":
            target = word ^ ((bit(word, wires[0]) & bit(word, wires[1])) << wires[2])
        else:
            raise ValueError(kind)
        assert target not in result
        result[target] = amplitude
    return result


def compile_cnf(num_variables, clauses):
    """Return fresh-target reversible Boolean circuit and output wire."""
    next_wire = num_variables
    gates = []

    def fresh():
        nonlocal next_wire
        wire = next_wire
        next_wire += 1
        return wire

    def not_wire(a):
        target = fresh()
        gates.extend([("X", (target,)), ("CX", (a, target))])
        return target

    def and_wire(a, b):
        target = fresh()
        gates.append(("CCX", (a, b, target)))
        return target

    def or_wire(a, b):
        target = fresh()
        gates.extend([
            ("CX", (a, target)), ("CX", (b, target)),
            ("CCX", (a, b, target)),
        ])
        return target

    clause_wires = []
    for clause in clauses:
        if not clause:
            raise ValueError("empty clauses are excluded from this fixture")
        literals = []
        for literal in clause:
            source = abs(literal) - 1
            if not 0 <= source < num_variables:
                raise ValueError(literal)
            literals.append(source if literal > 0 else not_wire(source))
        output = literals[0]
        for literal_wire in literals[1:]:
            output = or_wire(output, literal_wire)
        clause_wires.append(output)

    if not clause_wires:
        raise ValueError("empty formula is excluded from this fixture")
    output = clause_wires[0]
    for clause_wire in clause_wires[1:]:
        output = and_wire(output, clause_wire)
    return next_wire, gates, output


def evaluate_cnf(assignment, clauses):
    return all(any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0)
                   for lit in clause) for clause in clauses)


def fixture(num_variables, clauses):
    assert num_variables % 2 == 0
    total_wires, gates, output = compile_cnf(num_variables, clauses)
    state = {0: Fraction(1)}
    for wire in range(0, num_variables, 2):
        state = apply_h2(state, wire, wire + 1)
    for gate in gates:
        state = apply_permutation(state, gate)

    expected_count = sum(evaluate_cnf(x, clauses) for x in range(1 << num_variables))
    total_probability = sum((amp * amp for amp in state.values()), Fraction())
    accept_probability = sum((amp * amp for word, amp in state.items()
                              if bit(word, output)), Fraction())
    assert total_probability == 1
    assert len(state) == 1 << num_variables
    assert accept_probability == Fraction(expected_count, 1 << num_variables)
    assert all(amp == Fraction(1, 1 << (num_variables // 2))
               for amp in state.values())

    d = 1 << total_wires
    dense_check = None
    if d <= 8:
        columns = []
        for input_word in range(d):
            basis_state = {input_word: Fraction(1)}
            for wire in range(0, num_variables, 2):
                basis_state = apply_h2(basis_state, wire, wire + 1)
            for gate in gates:
                basis_state = apply_permutation(basis_state, gate)
            columns.append(basis_state)
        for j in range(d):
            for k in range(d):
                inner = sum((columns[j].get(z, 0) * columns[k].get(z, 0)
                             for z in range(d)), Fraction())
                assert inner == int(j == k)
        # P_z U has only one nonzero row; unitary row normalization makes
        # that row nonzero, so all d branch products have rank exactly one.
        for z in range(d):
            row_norm = sum((columns[j].get(z, 0) ** 2 for j in range(d)), Fraction())
            assert row_norm == 1
        dense_check = "unitary columns and nonzero rank-one branch rows verified"
    return {
        "variables": num_variables,
        "clauses": clauses,
        "local_gates": num_variables // 2 + len(gates),
        "qubits_including_ancillas": total_wires,
        "satisfying_assignments": expected_count,
        "accept_probability": str(accept_probability),
        "nonzero_final_basis_probabilities": len(state),
        "final_global_measurement_branch_rank": 1,
        "terminal_channel_choi_rank": d,
        "dense_hilbert_dimension_d": d,
        "N636_exterior_dimension": d * (d - 1) // 2,
        "N636_conic_support_cap_d4": d ** 4,
        "small_dense_check": dense_check,
    }


if __name__ == "__main__":
    cases = [
        (2, [[1], [2]]),
        (4, [[1, 2], [-3, 4]]),
        (4, [[1, -2, 3], [-1, 4], [2, -3]]),
    ]
    print(json.dumps([fixture(n, clauses) for n, clauses in cases], indent=2))

"""Bounded exact audit of the ACTUAL lifted-gate exchange implementation.

No finite pass establishes the preprint's all-size Poincare theorem or executes
its full FPRAS. Every reported algebra check uses fractions, including a small
independent PSD certificate for the discrete gap on four-variable instances.
"""
import json
from collections import deque
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from time import perf_counter

from xxz_local_chain import (CoinTape, LocalExchange, TapeAbort, WeightTree,
                             compile_trace, enumerate_supports, mixing_steps,
                             product_fraction, thermal_plan)


def generic_row(instance, state, z, t, pins):
    """Literal Eq.(19), with n global coefficient queries per deletion."""
    S, T = map(set, state)
    row = {state: F(1)}
    for side, selected, other in ((0, S, T), (1, T, S)):
        included, excluded = pins[2 * side:2 * side + 2]
        oracle = instance.mu if side == 0 else instance.nu
        for u in selected:
            rest = selected - {u}
            weights = []
            for v in range(instance.n):
                candidate = rest | {v}
                if v not in rest and included <= candidate and not excluded.intersection(candidate):
                    w = z[v] * oracle(candidate)
                    if w > 0:
                        weights.append((v, w))
            denominator = sum((w for _, w in weights), F(0))
            assert denominator > 0
            scale = (F(1, 2) if u in other else t / 2) / instance.n
            for v, w in weights:
                if v == u:
                    continue
                target_set = frozenset(rest | {v})
                target = (target_set, frozenset(T)) if side == 0 else (frozenset(S), target_set)
                probability = scale * w / denominator
                row[target] = row.get(target, F(0)) + probability
                row[state] -= probability
    return row


def psd_elimination(matrix):
    """Exact Schur-complement PSD certificate, including singular last pivot."""
    A = [list(row) for row in matrix]
    pivots = []
    for k in range(len(A)):
        pivot = A[k][k]
        assert pivot >= 0, ("negative exact PSD pivot", k, pivot)
        pivots.append(str(pivot))
        if pivot == 0:
            assert all(A[k][j] == 0 for j in range(k + 1, len(A)))
            continue
        for i in range(k + 1, len(A)):
            for j in range(i, len(A)):
                A[i][j] -= A[i][k] * A[k][j] / pivot
                A[j][i] = A[i][j]
    return pivots


def matrix_gate(qubits, gate):
    kind, vertices, s, alpha, gamma = gate
    s, alpha, gamma = F(s), F(alpha), F(gamma)
    dimension = 1 << qubits
    out = [[F(0) for _ in range(dimension)] for _ in range(dimension)]
    for bits in range(dimension):
        if kind == "edge":
            u, v = vertices
            zu, zv = 1 - 2 * ((bits >> u) & 1), 1 - 2 * ((bits >> v) & 1)
            out[bits][bits] = 1 + s * (3 * alpha + gamma * zu * zv)
            if zu != zv:
                out[bits ^ (1 << u) ^ (1 << v)][bits] = 2 * s * alpha
        else:
            (u,) = vertices
            z = 1 - 2 * ((bits >> u) & 1)
            r = alpha + abs(gamma)
            out[bits][bits] = 1 + s * (r + gamma * z)
            out[bits ^ (1 << u)][bits] = s * alpha
    return out


def matmul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(A))), F(0))
             for j in range(len(B))] for i in range(len(A))]


def exact_trace(qubits, gates):
    n = 1 << qubits
    W = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for gate in gates:
        W = matmul(W, matrix_gate(qubits, gate))
    return sum((W[i][i] for i in range(n)), F(0))


def hard_coefficient(instance):
    total = F(0)
    local_choices = []
    for factor in instance.factors:
        local_choices.append([(frozenset(u for j, u in enumerate(factor.coordinates) if mask >> j & 1), weight)
                              for mask, weight in factor.table.items()])
    ground = frozenset(range(instance.n))
    for parts in product(*local_choices):
        S = frozenset().union(*(chosen for chosen, _ in parts))
        if instance.nu(ground - S):
            total += product_fraction(weight for _, weight in parts)
    return total * (1 << instance.inactive_qubits)


start = perf_counter()
fixtures = [
    ("edge_interior", 2, [("edge", (0, 1), F(1, 10), F(1), F(1, 3))]),
    ("edge_boundary", 2, [("edge", (0, 1), F(1, 8), F(1), F(-1))]),
    ("field_symmetric", 1, [("field", (0,), F(1, 11), F(2), F(0))]),
    ("field_longitudinal", 1, [("field", (0,), F(1, 7), F(1), F(-2))]),
    ("edge_zero", 2, [("edge", (0, 1), F(1, 13), F(0), F(0))]),
    ("edge_plus_field", 2, [("edge", (0, 1), F(1, 9), F(2), F(1)),
                           ("field", (0,), F(1, 5), F(3), F(-1))]),
    ("two_fields_dummy_tree", 1, [("field", (0,), F(1, 10), F(1), F(0)),
                                 ("field", (0,), F(1, 9), F(2), F(0))]),
    ("zero_X_plus_field", 2, [("field", (0,), F(1, 10), F(0), F(3)),
                             ("field", (1,), F(1, 9), F(2), F(0))]),
]
reports = []
total_rows = total_edges = gap_certificates = 0
for name, qubits, gates in fixtures:
    instance = compile_trace(qubits, gates)
    assert hard_coefficient(instance) == exact_trace(qubits, gates)
    pin_cases = [(frozenset(), frozenset(), frozenset(), frozenset())]
    if name == "two_fields_dummy_tree":
        pin_cases.append((frozenset({0}), frozenset({2}), frozenset({3}), frozenset({6})))
    for pin_number, pins in enumerate(pin_cases):
        supports = enumerate_supports(instance, pins)
        assert supports
        # Both unit and highly uneven rational fields are tested on four-variable
        # kernels. Larger kernels use uneven fields except for symmetry checks.
        z_sets = [[F(1) for _ in range(instance.n)]]
        if pin_number or instance.n == 4 or name == "edge_plus_field":
            z_sets.append([F(2) ** (u % 5 - 2) * F(3) ** (u % 3 - 1) for u in range(instance.n)])
        for z in z_sets:
            t = F(1, 256 * instance.n * instance.n)
            weights, rows = {}, {}
            for state in supports:
                chain = LocalExchange(instance, z, t, pins, state)
                weights[state] = chain.supported_weight()
                rows[state] = chain.kernel_row()
                assert rows[state] == generic_row(instance, state, z, t, pins)
                assert sum(rows[state].values(), F(0)) == 1
                assert min(rows[state].values()) >= 0
                assert rows[state][state] >= F(1, 2)
                total_rows += 1
            Z = sum(weights.values(), F(0))
            for state, row in rows.items():
                for target, probability in row.items():
                    assert target in weights
                    assert weights[state] * probability == weights[target] * rows[target].get(state, F(0))
                    total_edges += 1
            reached, queue = {supports[0]}, deque([supports[0]])
            while queue:
                current = queue.popleft()
                for target, probability in rows[current].items():
                    if probability and target not in reached:
                        reached.add(target)
                        queue.append(target)
            assert len(reached) == len(supports)
            if instance.n == 4 and z == [F(1)] * 4:
                stationary = [weights[state] / Z for state in supports]
                gap = t / (2 * instance.n)
                matrix = []
                for i, state in enumerate(supports):
                    row = []
                    for j, target in enumerate(supports):
                        identity = int(i == j)
                        row.append(stationary[i] * (identity - rows[state].get(target, F(0))) -
                                   gap * (identity * stationary[i] - stationary[i] * stationary[j]))
                    matrix.append(row)
                pivots = psd_elimination(matrix)
                gap_certificates += 1
            else:
                pivots = None
            p_hard = sum((weights[state] for state in supports if state[0].isdisjoint(state[1])), F(0)) / Z
            symmetric = instance.complement_symmetric() and not any(pins) and z == [F(1)] * instance.n
            if symmetric:
                assert p_hard >= F(3, 4)
                for u in range(instance.n):
                    grad = sum((weights[state] * (int(u in state[0]) + int(u in state[1]) - 1)
                                for state in supports), F(0))
                    assert grad == 0
            reports.append({"fixture": name, "pin_case": pin_number, "n": instance.n,
                            "states": len(supports), "unit_fields": z == [F(1)] * instance.n,
                            "symmetric": symmetric, "complement_probability": str(p_hard),
                            "literal_transition_match": True, "detailed_balance": True,
                            "irreducible": True, "psd_gap_pivots": pivots,
                            "hard_trace": str(hard_coefficient(instance)),
                            "tv_1_8_step_certificate": mixing_steps(instance, t, z, F(1, 8))})

# Production-path tape, dynamic dummy tree, forced/excluded pins, updates and
# expected whole-sample abort behavior are exercised separately from row audit.
instance = compile_trace(1, fixtures[6][2])
chain = LocalExchange(instance, [F(2) ** (u % 5 - 2) for u in range(instance.n)], F(1, 4))
tape = CoinTape(20261007, bit_cap=32, choice_cap=100000)
for j in range(4000):
    if j % 103 == 0:
        u = (j // 103) % instance.n
        chain.set_field(u, chain.z[u] * F(33, 32))
    chain.step(tape)
    assert instance.mu(chain.S) > 0 and instance.nu(chain.T) > 0
    for group, tree in chain.trees.items():
        expected = sum((chain.z[u] for u in instance.groups[group][0] if u not in chain.T), F(0))
        assert expected == tree.total

abort_observed = False
for seed in range(8):
    capped = CoinTape(seed, bit_cap=1, choice_cap=2)
    try:
        capped.bernoulli(F(1, 3))
        capped.bernoulli(F(1, 3))
        capped.bernoulli(F(1, 3))
    except TapeAbort:
        abort_observed = True
        break
assert abort_observed

# This is the actual, conservatively charged Euler plan. Its gates are NOT
# allocated or simulated, and no fast matrix powering is substituted for them.
plan = thermal_plan(3, [(0, 1, F(1), F(1, 2)), (1, 2, F(2, 3), F(-1, 3))],
                    [(0, F(1, 4), F(0)), (2, F(1, 3), F(0))], F(1, 2), F(1, 10))
out = {"status": "PASS_EXACT_FINITE_COMPONENT", "kernel_rows": total_rows,
       "detailed_balance_directed_entries": total_edges,
       "independent_small_exact_gap_certificates": gap_certificates,
       "fixtures": reports,
       "production_steps": 4000, "production_coin_choices": tape.choices,
       "production_coin_bits": tape.bits, "forced_abort_observed": abort_observed,
       "unallocated_thermal_plan": {k: str(v) if isinstance(v, F) else v for k, v in plan.items()},
       "wall_seconds": perf_counter() - start,
       "scope": "Exact transitions and small finite algebra; no all-size gap certification, full FPRAS or Gibbs preparation run."}
Path(__file__).with_name("checks.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({k: v for k, v in out.items() if k not in {"fixtures"}}, indent=2))

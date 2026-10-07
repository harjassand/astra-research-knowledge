"""Exact local/table/order checks plus labelled small floating diagnostics."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from time import perf_counter
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from xxz_local_chain import LocalExchange, compile_trace, enumerate_supports, product_fraction, thermal_plan
from nofield_counter import acquired_complement_ratio, ResourceRefusal, count_nofield, nofield_plan
from xxz_quadratic_gates import (compile_quadratic_trace, planned_quadratic_circuit,
                                 quadratic_edge_table, quadratic_field_table, quadratic_plan)
from pauli_order_certificate import third_certificate_plan, third_defect


def mul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(A))), F(0))
             for j in range(len(B))] for i in range(len(A))]


def add(A, B):
    return [[a + b for a, b in zip(ar, br)] for ar, br in zip(A, B)]


def scale(A, c):
    return [[c * x for x in row] for row in A]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def shifted_A(qubits, kind, vertices, a, g):
    n = 1 << qubits
    result = [[F(0) for _ in range(n)] for _ in range(n)]
    for bits in range(n):
        if kind == "edge":
            u, v = vertices
            zu, zv = 1 - 2 * ((bits >> u) & 1), 1 - 2 * ((bits >> v) & 1)
            result[bits][bits] = 3 * a + g * zu * zv
            if zu != zv:
                result[bits ^ (1 << u) ^ (1 << v)][bits] = 2 * a
        else:
            (u,) = vertices
            result[bits][bits] = a + abs(g) + g * (1 - 2 * ((bits >> u) & 1))
            result[bits ^ (1 << u)][bits] = a
    return result


def dense_trace(qubits, gates):
    W = eye(1 << qubits)
    for kind, vertices, s, a, g in gates:
        A = shifted_A(qubits, kind, vertices, a, g)
        gate = add(add(eye(len(A)), scale(A, s)), scale(mul(A, A), s * s / 2))
        W = mul(W, gate)
    return sum((W[i][i] for i in range(len(W))), F(0))


def hard_count(instance):
    total = F(0)
    choices = []
    for factor in instance.factors:
        choices.append([(frozenset(u for j, u in enumerate(factor.coordinates) if mask >> j & 1), value)
                        for mask, value in factor.table.items()])
    ground = frozenset(range(instance.n))
    for selected in product(*choices):
        S = frozenset().union(*(s for s, _ in selected))
        if instance.nu(ground - S):
            total += product_fraction(value for _, value in selected)
    return total * (1 << instance.inactive_qubits)


def product_coefficients(sequence, degree):
    n = len(sequence[0])
    result = [eye(n)] + [[[F(0) for _ in range(n)] for _ in range(n)] for _ in range(degree)]
    for A in sequence:
        local = [eye(n), A, scale(mul(A, A), F(1, 2))]
        new = [[[F(0) for _ in range(n)] for _ in range(n)] for _ in range(degree + 1)]
        for i in range(degree + 1):
            for j in range(min(2, i) + 1):
                new[i] = add(new[i], mul(result[i - j], local[j]))
        result = new
    return result


start = perf_counter()
table_checks = 0
for alpha in [F(0), F(1, 7), F(1), F(9)]:
    for ratio in [F(-1), F(-1, 3), F(0), F(2, 3), F(1)]:
        for s in [F(0), F(1, 100), F(1, 4), F(1), F(12)]:
            table = quadratic_edge_table(s, alpha, alpha * ratio)
            assert all(table[mask] == table.get(15 ^ mask) for mask in table)
            table_checks += 1
for b in [F(0), F(1, 13), F(2), F(10)]:
    for c in [F(-12), F(-1, 4), F(0), F(1, 3), F(9)]:
        for s in [F(0), F(1, 100), F(1, 4), F(1), F(12)]:
            table = quadratic_field_table(s, b, c)
            if c == 0:
                assert all(table[mask] == table.get(15 ^ mask) for mask in table)
            table_checks += 1

traces = []
for qubits, gates in [
    (2, [("edge", (0, 1), F(1, 8), F(1), F(1, 3))]),
    (1, [("field", (0,), F(1, 9), F(2), F(-1))]),
    (2, [("edge", (0, 1), F(1, 10), F(2), F(-1)),
         ("field", (1,), F(1, 13), F(1), F(2))]),
    (1, [("field", (0,), F(1, 7), F(2), F(0)),
         ("field", (0,), F(1, 11), F(1), F(0))])]:
    instance = compile_quadratic_trace(qubits, gates)
    count, trace = hard_count(instance), dense_trace(qubits, gates)
    assert count == trace
    traces.append({"qubits": qubits, "gates": len(gates), "n": instance.n,
                   "exact_trace": str(trace), "symmetric": instance.complement_symmetric()})

planned, gates, little_plan = planned_quadratic_circuit(
    2, [(0, 1, F(1), F(1, 2))], [], F(1, 20), F(1, 10), max_gates=10)
assert len(gates) == 4 and planned.n == 16
assert hard_count(planned) == dense_trace(2, gates)

# Complete noncommuting order-two matrix identity, rather than a numerical
# inference of its cancellation. The independent proof carries all sizes.
A = shifted_A(2, "edge", (0, 1), F(1), F(1, 2))
B = shifted_A(2, "field", (0,), F(2), F(-1))
sequence = [A, B, B, A]
coefficients = product_coefficients(sequence, 3)
S = scale(add(A, B), F(2))
assert coefficients[1] == S
assert coefficients[2] == scale(mul(S, S), F(1, 2))
third_error = add(coefficients[3], scale(mul(mul(S, S), S), F(-1, 6)))
third_witness = next((i, j, value) for i, row in enumerate(third_error)
                     for j, value in enumerate(row) if value)
pauli_defect, pauli_bound = third_defect([(0, 1, F(1), F(1, 2))], [(0, F(2), F(-1))])
pauli_matrix = [[F(0) for _ in range(4)] for _ in range(4)]
for (x, z), (real, imag) in pauli_defect.items():
    assert imag == 0 and (x & z).bit_count() % 2 == 0
    global_sign = (-1) ** ((x & z).bit_count() // 2)
    for bit in range(4):
        pauli_matrix[bit ^ x][bit] += real * global_sign * (-1) ** ((z & bit).bit_count())
assert pauli_matrix == third_error

# The entire no-balancing algorithm is present, but conservative certified
# caps are honestly refused before running, even for this four-variable case.
tiny = compile_quadratic_trace(1, [("field", (0,), F(1, 10), F(1), F(0))])
full_plan = nofield_plan(tiny, F(1), F(1, 4))
try:
    count_nofield(tiny, F(1), F(1, 4), max_steps=1000000)
    raise AssertionError("conservative plan unexpectedly admitted")
except ResourceRefusal as refusal:
    assert refusal.plan == full_plan

bias_checks = []
for qubits, biased_gates in [
    (1, [("field", (0,), F(1, 9), F(2), F(-1))]),
    (1, [("field", (0,), F(1), F(0), F(10))]),
    (2, [("edge", (0, 1), F(1, 10), F(2), F(-1)),
         ("field", (1,), F(1, 13), F(1), F(2))])]:
    biased = compile_quadratic_trace(qubits, biased_gates)
    ratio = acquired_complement_ratio(biased)
    plan = nofield_plan(biased, F(1), F(1, 4), allow_bounded_bias=True)
    assert plan["t"] == F(1, 256 * biased.n ** 2) / ratio
    states = enumerate_supports(biased)
    weights = {state:LocalExchange(biased, t=plan["t"], state=state).supported_weight() for state in states}
    ground = frozenset(range(biased.n))
    for S, T in states:
        flipped = (ground - S, ground - T)
        assert 1 / ratio <= weights[(S,T)] / weights[flipped] <= ratio
    Z = sum(weights.values(), F(0))
    phard = sum((w for (S,T),w in weights.items() if S.isdisjoint(T)), F(0)) / Z
    assert phard >= F(3,4)
    bias_checks.append({"n":biased.n,"ratio":str(ratio),"penalty":str(plan["t"]),
                        "complement_probability":str(phard),"numeric_ratio_charged":True})

example_edges = [(0, 1, F(1), F(1, 2)), (1, 2, F(2, 3), F(-1, 3))]
example_fields = [(0, F(1, 4), F(0)), (2, F(1, 3), F(0))]
linear = thermal_plan(3, example_edges, example_fields, F(1, 2), F(1, 10))
quadratic = quadratic_plan(3, example_edges, example_fields, F(1, 2), F(1, 10))
third_plan = third_certificate_plan(3, example_edges, example_fields, F(1, 2), F(1, 10))
assert quadratic["log_generator_error_bound"] <= F(1, 40)
assert quadratic["m"] == 84 and linear["m"] == 6235
assert third_plan["m"] == 23 and third_plan["log_generator_error_bound"] <= F(1, 40)

def jsonify(d):
    return {k: str(v) if isinstance(v, F) else v for k, v in d.items()}

out = {"status": "PASS_EXACT_QUADRATIC_COMPONENT", "local_table_checks": table_checks,
       "exact_trace_checks": traces, "actual_small_thermal_circuit": jsonify(little_plan),
       "actual_small_thermal_count": str(hard_count(planned)),
       "exact_second_order_palindrome_identity": True,
       "nonzero_third_order_error_witness": {"row": third_witness[0], "column": third_witness[1],
                                             "coefficient": str(third_witness[2])},
       "exact_dense_pauli_third_coefficient_match": True,
       "pauli_certificate_witness_l1": str(pauli_bound),
       "linear_example": jsonify(linear), "quadratic_example": jsonify(quadratic),
       "pauli_refined_example": jsonify({k:v for k,v in third_plan.items() if k != "third_coefficient"}),
       "four_variable_full_count_refused_before_science_steps": jsonify(full_plan),
       "bounded_complement_bias_checks": bias_checks,
       "wall_seconds": perf_counter() - start,
       "scope": "Exact gate/finite coefficient identities and resource admission. No full FPRAS or physical Gibbs preparation."}
Path(__file__).with_name("checks.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))

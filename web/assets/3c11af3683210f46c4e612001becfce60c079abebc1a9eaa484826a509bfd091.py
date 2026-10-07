"""Small exact check of quadratic gates inside a projected spin trace.

Uses c06_s01's read-only tensor compiler, but writes only in c06_l03's folder.
This checks coefficient/trace equality on finite fixtures, not the FPRAS or
the all-q projector theorem.
"""

from fractions import Fraction as F
from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "work/cycle6/c06_s01/spin_projection_transfer.py"
spec = importlib.util.spec_from_file_location("spin_projection_transfer", SOURCE)
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)


def p2_matrix(a, t):
    a2 = sp.matmul(a, a)
    eye = sp.identity(len(a))
    return [[eye[i][j] + t * a[i][j] + (t * t / 2) * a2[i][j]
             for j in range(len(a))] for i in range(len(a))]


def quadratic_edge(qubits, alpha, gamma, t):
    alpha, gamma, t = map(F, (alpha, gamma, t))
    shift = 3 * alpha
    aop = [
        [shift + gamma, 0, 0, 0],
        [0, shift - gamma, 2 * alpha, 0],
        [0, 2 * alpha, shift - gamma, 0],
        [0, 0, 0, shift + gamma],
    ]
    table = p2_matrix([[F(x) for x in row] for row in aop], t)
    return sp.Gate(tuple(qubits), "edge", tuple(tuple(x for x in row) for row in table))


def quadratic_field(qubit, b, c, t):
    b, c, t = map(F, (b, c, t))
    r = b + abs(c)
    aop = [[r + c, b], [b, r - c]]
    table = p2_matrix(aop, t)
    return sp.Gate((qubit,), "field", tuple(tuple(x for x in row) for row in table))


def projected_trace(gates, qsets, nqubits):
    projectors = [sp.Gate(tuple(qset), "projector") for qset in qsets]
    # Pi is applied before and after the local palindromic layer.
    return projectors + gates + list(reversed(gates)) + projectors


def run():
    t = F(1, 7)
    pi_q2 = sp.Gate((0, 1), "projector")
    pi_q1 = sp.Gate((2,), "projector")

    # A site-symmetric spin-1 / spin-1/2 interaction, embedded on q=2 and q=1
    # constituents. The two pair terms have equal parameters; the projector is
    # inserted at both ends of the palindromic layer.
    pair_gates = [
        quadratic_edge((0, 2), F(1, 4), F(-1, 8), t),
        quadratic_edge((1, 2), F(1, 4), F(-1, 8), t),
    ]
    gates = [pi_q2, pi_q1] + pair_gates + list(reversed(pair_gates)) + [pi_q2, pi_q1]
    circuit = sp.CompiledCircuit(3, gates)
    tensor, work, accepted = circuit.exact_diagnostic_count(cap=250_000)
    dense = sp.circuit_trace(gates, 3)
    assert tensor == dense

    # A separate one-site field fixture checks that the two dummy coordinates
    # still recover a quadratic Taylor gate under a projector boundary.
    field = quadratic_field(0, F(1, 3), F(-1, 5), t)
    field_gates = [pi_q2, field, field, pi_q2]
    field_circuit = sp.CompiledCircuit(2, field_gates)
    field_tensor, field_work, field_accepted = field_circuit.exact_diagnostic_count(cap=100_000)
    field_dense = sp.circuit_trace(field_gates, 2)
    assert field_tensor == field_dense

    return {
        "status": "PASS_EXACT_FINITE_PROJECTED_TRACE",
        "pair_fixture": {
            "tensor_trace": str(tensor), "dense_trace": str(dense),
            "enumerated_local_monomial_tuples": work, "accepted": accepted,
            "lifted_variables": circuit.n, "degree": circuit.degree,
        },
        "field_fixture": {
            "tensor_trace": str(field_tensor), "dense_trace": str(field_dense),
            "enumerated_local_monomial_tuples": field_work, "accepted": field_accepted,
            "lifted_variables": field_circuit.n, "degree": field_circuit.degree,
        },
        "scope": "finite rational coefficient-to-trace identities; no FPRAS, uniform theorem, or source proof validation",
    }


if __name__ == "__main__":
    import json
    result = run()
    print(json.dumps(result, indent=2))

"""Exact finite checks of complement symmetry for the c=0 P2/projector lift.

The all-q symmetry statement is proved in the accompanying revision. This
script checks small instances using c06_s01's read-only local coefficient
compiler; it does not run the no-balancing sampler or the FPRAS.
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
    return [[eye[i][j] + t * a[i][j] + t*t*a2[i][j]/2
             for j in range(len(a))] for i in range(len(a))]


def check_factor(factor):
    full = sum(1 << v for v in factor.variables)
    for local in range(1 << len(factor.variables)):
        mask = sum(((local >> j) & 1) << v
                   for j, v in enumerate(factor.variables))
        if factor.coefficient(mask) != factor.coefficient(full ^ mask):
            raise AssertionError((factor.gate.kind, local))


def main():
    t = F(1, 5)
    factors_checked = 0
    # Projector polynomials p_q for q<=5, checked over all 2^(2q) masks.
    for q in range(1, 6):
        gate = sp.Gate(tuple(range(q)), "projector")
        factor = sp.Factor(gate, tuple(range(q)), tuple(range(q, 2*q)), ())
        check_factor(factor)
        factors_checked += 1

    # Edge P2 gates for both boundary signs, and several rational points.
    for alpha, gamma in ((F(1, 3), F(1, 3)),
                         (F(1, 3), F(-1, 3)),
                         (F(2, 5), F(1, 10))):
        shift = 3*alpha
        a = [[shift+gamma,0,0,0],
             [0,shift-gamma,2*alpha,0],
             [0,2*alpha,shift-gamma,0],
             [0,0,0,shift+gamma]]
        table = p2_matrix([[F(x) for x in row] for row in a], t)
        gate = sp.Gate((0, 1), "edge", tuple(tuple(row) for row in table))
        factor = sp.Factor(gate, (0, 1), (2, 3), ())
        check_factor(factor)
        factors_checked += 1

    # The field lift is complement-symmetric precisely in this c=0 fixture.
    b = F(2, 7)
    a = [[b, b], [b, b]]  # shifted field A=b I+b X
    table = p2_matrix(a, t)
    gate = sp.Gate((0,), "field", tuple(tuple(row) for row in table))
    factor = sp.Factor(gate, (0,), (1,), (2, 3))
    check_factor(factor)
    factors_checked += 1

    # Full mu and nu coefficient functions for a small projected c=0 circuit.
    q2 = sp.Gate((0, 1), "projector")
    field = gate
    circuit = sp.CompiledCircuit(2, [q2, field, field, q2])
    full = (1 << circuit.n) - 1
    for mask in range(1 << circuit.n):
        assert circuit.p_coefficient(mask) == circuit.p_coefficient(full ^ mask)
        assert circuit.q_coefficient(mask) == circuit.q_coefficient(full ^ mask)

    return {
        "status": "PASS_EXACT_FINITE_COMPLEMENT_SYMMETRY",
        "local_factors_checked": factors_checked,
        "projector_arities": [1, 2, 3, 4, 5],
        "full_circuit_variables": circuit.n,
        "full_circuit_masks_checked": 1 << circuit.n,
        "scope": "finite coefficient-function symmetry checks only; no sampler or FPRAS execution",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2))

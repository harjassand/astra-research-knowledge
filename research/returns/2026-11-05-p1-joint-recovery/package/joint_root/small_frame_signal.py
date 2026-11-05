"""Exact fixed-two-qubit-frame signal in the channel constructor's slow limit.

This is a proof-sized symbolic identity, not an unrestricted optimal reader.
The physical cascade, limiting generator, and fixed-k scope are in
joint_channel/slow_generator_derivation.md.
"""
from itertools import product
from pathlib import Path
import json
import sympy as sp

ident = sp.eye(2)
pauli = [sp.Matrix([[0, 1], [1, 0]]),
         sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.diag(1, -1)]

def embed(site, component):
    ans = sp.ones(1, 1)
    for j in range(3):
        ans = sp.kronecker_product(ans, pauli[component] if j == site else ident)
    return ans

spin = [[embed(j, a) for a in range(3)] for j in range(3)]
current = [sp.zeros(8) for _ in range(3)]
for a, b, c in product(range(3), repeat=3):
    parity = sp.LeviCivita(a, b, c)
    if parity:
        for j in range(3):
            for k in range(j + 1, 3):
                current[a] += parity * spin[j][b] * spin[k][c]
chirality = sum((sp.LeviCivita(a, b, c) * spin[0][a] * spin[1][b] * spin[2][c]
                 for a, b, c in product(range(3), repeat=3)), sp.zeros(8))
pairs = [(0, 1), (0, 2), (1, 2)]
dots = [sum((spin[j][a] * spin[k][a] for a in range(3)), sp.zeros(8))
        for j, k in pairs]

def commutator(a, b):
    return a * b - b * a

def generator_adjoint(a):
    return (-sum((commutator(y, commutator(y, a)) for y in current), sp.zeros(8)) / 32
            - sp.I * commutator(chirality, a) / 8)

singlet = (sp.eye(8) - dots[2]) / 4
derivative = generator_adjoint(singlet)
expected = (-dots[0] + dots[1] + dots[2]) / 4
assert sp.simplify(derivative - expected) == sp.zeros(8)
matrix = sp.Matrix([[sp.simplify(sp.trace(a * generator_adjoint(b)) / sp.trace(a * a))
                     for b in dots] for a in dots])
for column, b in enumerate(dots):
    reconstructed = sum((matrix[row, column] * a for row, a in enumerate(dots)), sp.zeros(8))
    assert sp.simplify(generator_adjoint(b) - reconstructed) == sp.zeros(8)

record = {
    'basis': ['sigma_S dot sigma_M1', 'sigma_S dot sigma_M2', 'sigma_M1 dot sigma_M2'],
    'generator_adjoint_matrix': [[str(x) for x in row] for row in matrix.tolist()],
    'eigenvalues_with_multiplicity': {str(k): int(v) for k, v in matrix.eigenvals().items()},
    'singlet_derivative_coefficients': ['-1/4', '1/4', '1/4'],
    'frame': '|0>_M1 tensor |+>_M2',
    'probability_derivative': '(r_x-r_z)/4',
    'rigorous_consequence': 'The two z-basis inputs have different final singlet probabilities for sufficiently small positive slow time; two initialized receiver qubits retain nonzero information in the fixed-k weak-angle limit.',
    'limitation': 'The two-qubit receiver output commutant is abelian; this example transmits only classical information and does not resolve reference-preserving recovery.'
}
target = Path(__file__).resolve().parent / 'small_frame_signal_exact.json'
target.write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))

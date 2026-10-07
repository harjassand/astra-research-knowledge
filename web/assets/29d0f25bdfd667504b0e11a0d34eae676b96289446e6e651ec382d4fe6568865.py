#!/usr/bin/env python3
"""Exact small checks for the fixed-point/gap and pairwise-compatibility note."""

from fractions import Fraction as F
from itertools import product
import json

import sympy as s


def kron(a, b):
    return s.kronecker_product(a, b)


def ptrace_second(a):
    return s.Matrix(2, 2, lambda i, j: s.simplify(sum(a[2*i+k, 2*j+k] for k in range(2))))


I2 = s.eye(2)
I4 = s.eye(4)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
paulis = (I2, X, Y, Z)

# Verify the d=2 symmetric 1->2 cloner used in the pairwise/global example.
# Build swap directly in the computational basis |a,b> -> |b,a>.
swap = s.zeros(4)
for a in range(2):
    for b in range(2):
        swap[2*b+a, 2*a+b] = 1
Pplus = (I4 + swap) / 2
Kraus = []
for j in range(2):
    ket = s.zeros(2, 1)
    ket[j, 0] = 1
    Kraus.append(s.sqrt(s.Rational(2, 3)) * Pplus * kron(I2, ket))

assert all(s.simplify(x) == 0 for x in (sum((k.H*k for k in Kraus), s.zeros(2)) - I2))
assert s.simplify(swap * Pplus - Pplus) == s.zeros(4)

def clone(a):
    return sum((k * a * k.H for k in Kraus), s.zeros(4))

def depol(a, lam):
    return s.Rational(lam) * a + (1 - s.Rational(lam)) * s.trace(a) * I2 / 2

for a in paulis:
    marginal = ptrace_second(clone(a))
    assert s.simplify(marginal - depol(a, s.Rational(2, 3))) == s.zeros(2)

# The 9/10 cloner + 1/10 replacement broadcaster has marginal Delta_(3/5).
lam = F(3, 5)
assert F(9, 10) * F(2, 3) == lam

# Pairwise noisy Pauli measurements have an explicit exact parent. Positivity
# is equivalent to 2*eta^2 <= 1, checked without floating square roots.
eta = F(3, 5)
pair_positive_margin = F(1) - 2 * eta * eta
assert pair_positive_margin > 0

# A symmetrized joint parent for the triple would require 3*eta^2 <= 1.
triple_positivity_margin = F(1) - 3 * eta * eta
assert triple_positivity_margin < 0

# Classical two-state flip channel: Pauli eigenvalues (1,0,0,1-2eps).
eps = F(1, 20)
lam_slow = 1 - 2 * eps
gamma = min(F(1), 1 - lam_slow)
assert gamma == F(1, 10)
IminusE = s.diag(0, 1, 1, 0)
IminusPhi = s.diag(0, 1, 1, s.Rational(1, 10))
gap_slack = (1 / s.Rational(1, 10)) * IminusPhi - IminusE
assert gap_slack == s.diag(0, 9, 9, 1)

result = {
    "status": "PASS",
    "cloner_tp": True,
    "cloner_symmetric_output": True,
    "cloner_marginal_eigenvalues": ["1", "2/3", "2/3", "2/3"],
    "mixture_weights": ["9/10 cloner", "1/10 replacement"],
    "mixture_marginal": "Delta_(3/5)",
    "pairwise_parent_positivity_margin_squared": str(pair_positive_margin),
    "triple_parent_positivity_margin": str(triple_positivity_margin),
    "classical_flip_epsilon": str(eps),
    "classical_spectral_gap": str(gamma),
    "fixed_projection_comparison_slack": [[str(x) for x in gap_slack.row(i)] for i in range(4)],
    "limitations": [
        "finite exact checks validate formulas only",
        "the fixed-projection constant depends on the spectral gap",
        "the pair/triple example blocks a proof route, not EB rounding itself",
    ],
}
print(json.dumps(result, indent=2))

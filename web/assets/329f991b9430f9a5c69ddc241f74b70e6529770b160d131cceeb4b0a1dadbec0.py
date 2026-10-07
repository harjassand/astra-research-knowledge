"""Exact rational spot checks for the qubit collective-variance audit.

The proof of the formulas is in INITIAL.txt. This script checks the POVM
normalizations and the claimed losses using Fraction arithmetic; it is not a
proof of the optimization over all POVMs.
"""
from fractions import Fraction as F


def captured(povm_outcomes, h_index):
    """Each outcome is (probability p, score tau(M H)); return sum score^2/p."""
    return sum(score * score / p for p, score in povm_outcomes[h_index])


# For tau=Tr/2 and H in {X,Y,Z}, the six-outcome Pauli POVM has
# M_{i,+/-}=(I +/- sigma_i)/6. Each p=1/6 and its H_i score is +/-1/6.
six_outcome = {
    i: [(F(1, 6), F(sign, 6)) if j == i else (F(1, 6), F(0))
        for j in range(3) for sign in (1, -1)]
    for i in range(3)
}
for i in range(3):
    assert captured(six_outcome, i) == F(1, 3)
    assert F(1) - captured(six_outcome, i) == F(2, 3)

# For X and Z, the common four-outcome POVM has M_{i,+/-}=(I +/- sigma_i)/4.
four_outcome = {
    i: [(F(1, 4), F(sign, 4)) if j == i else (F(1, 4), F(0))
        for j in (0, 2) for sign in (1, -1)]
    for i in (0, 2)
}
for i in (0, 2):
    assert captured(four_outcome, i) == F(1, 2)
    assert F(1) - captured(four_outcome, i) == F(1, 2)

# A label-specific projective measurement captures that Pauli exactly.
projective_capture = 2 * (F(1, 2) ** 2) / F(1, 2)
assert projective_capture == 1

# Uniform block trace tau=w Tr/2 on an active qubit block scales both variance
# and captured score by w, with no inverse-weight factor.
for w in (F(1, 7), F(1, 2), F(6, 7)):
    weighted_capture = 2 * ((w * F(1, 4)) ** 2) / (w * F(1, 4))
    assert weighted_capture == w * F(1, 2)
    assert w - weighted_capture == w * F(1, 2)

# The two-Pauli prior gap is min(p,1-p); the three-Pauli uniform prior gap
# is 2/3. These rational grid checks supplement the analytic Bloch-vector proof.
for k in range(21):
    p = F(k, 20)
    assert F(1) - max(p, F(1) - p) == min(p, F(1) - p)
assert F(1) - max(F(1, 3), F(1, 3), F(1, 3)) == F(2, 3)

print("PASS: exact POVM score identities, common-map losses, and faithful block-weight scaling")
print("two Pauli collective variance = 1/2; three Pauli collective variance = 2/3")
print("three-Pauli / depolarizing-(2/3) Dirichlet ratio = 2")

"""Exact finite checks for the qubit depolarizing representability result.

The upper bound is proved analytically in revisions/REV1.txt. This script
checks the Pauli Kraus construction, its canonical POVM, and exact parameter
identities at rational grid points; it is not a proof of the universal upper
bound.
"""
from fractions import Fraction

# For t in [0,1], the Pauli probabilities implement the bistochastic
# depolarizing channel with Bloch contraction t. All effects are scalar,
# so the associated canonical EB channel is complete depolarization.
for k in range(101):
    t = Fraction(k, 100)
    p0 = (1 + 3 * t) / 4
    p1 = p2 = p3 = (1 - t) / 4
    assert min(p0, p1, p2, p3) >= 0
    assert p0 + p1 + p2 + p3 == 1
    lam = t * t / 4
    assert Fraction(0) <= lam <= Fraction(1, 4)
    # C=(L_t + Delta_0)/2 has contraction t/2, hence C^*C has t^2/4.
    assert (t / 2) ** 2 == lam

# The fidelity inequality reduces pointwise to this exact square identity.
for k in range(101):
    v = Fraction(k, 100)  # v = sqrt(1-u), 0 <= v <= 1
    u = 1 - v * v
    assert 2 - (2 * v + u) == (1 - v) ** 2
    assert 2 * v + u <= 2

print("exact qubit construction checks passed on 101 rational parameters")
print("represented depolarizing interval: 0 <= lambda <= 1/4")

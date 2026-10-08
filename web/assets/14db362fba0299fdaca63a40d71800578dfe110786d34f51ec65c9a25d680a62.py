"""Exact finite checks for the WR closure audit in REPORT.txt.

The infinite-product conclusion is proved algebraically in the report; this
script only checks finite graph/rank/order/rate identities and prints sample
rational conditional probabilities.
"""

from fractions import Fraction

complexes = {
    "C0": (2, 0),
    "C1": (4, 1),
    "C2": (6, 4),
    "C3": (3, 0),
}
edges = [("C0", "C1"), ("C1", "C2"), ("C2", "C3"), ("C3", "C0")]
rates = [Fraction(1), Fraction(1), Fraction(1), Fraction(2)]

# The listed directed cycle makes the complex graph strongly connected.
for start in complexes:
    seen = {start}
    frontier = [start]
    while frontier:
        here = frontier.pop()
        for source, target in edges:
            if source == here and target not in seen:
                seen.add(target)
                frontier.append(target)
    assert seen == set(complexes)

vectors = [
    (complexes[target][0] - complexes[source][0],
     complexes[target][1] - complexes[source][1])
    for source, target in edges
]
assert vectors[0][0] * vectors[1][1] - vectors[0][1] * vectors[1][0] == 4
assert len(complexes) - 1 - 2 == 1  # deficiency: |C|-linkage- rank
assert max(sum(complexes[source]) for source, _ in edges) == 10
cycle_sum = tuple(sum(vector[i] for vector in vectors) for i in range(2))
assert cycle_sum == (0, 0)

# At (n,0), only 2A->4A+B and 3A->2A are enabled.
for n in range(3, 15):
    lam_forward = rates[0] * n * (n - 1)
    lam_return = rates[3] * n * (n - 1) * (n - 2)
    p_forward = lam_forward / (lam_forward + lam_return)
    assert p_forward == Fraction(1, 1 + 2 * (n - 2))
    assert p_forward <= Fraction(1, n - 2)

partial = Fraction(1)
for n in range(3, 11):
    partial *= Fraction(1, 1 + 2 * (n - 2))

print("cycle strongly connected; rank=2; deficiency=1; max source order=10")
print("stoichiometric cycle sum:", cycle_sum)
print("product of p_n, n=3..10:", partial)
print("Exact formula: p_n = 1/(1+2(n-2)); infinite product is zero.")

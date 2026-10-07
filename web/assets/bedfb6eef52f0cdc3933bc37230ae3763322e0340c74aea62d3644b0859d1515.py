from fractions import Fraction
from math import factorial
import json


def det_int(a):
    """Exact determinant via fraction-free elimination for small integer matrices."""
    a = [list(map(int, row)) for row in a]
    n = len(a)
    if n == 0:
        return 1
    sign = 1
    prev = 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * p - a[i][k] * a[k][j]
                assert num % prev == 0
                a[i][j] = num // prev
            a[i][k] = 0
        prev = p
    return sign * a[n - 1][n - 1]


# Exterior-power amplitude to put R distinct fermions into one output orbital:
# all R rows of the one-particle transition minor are the same row, so its
# determinant vanishes. This is the algebraic form of (c_0^dagger)^R=0.
fermion_bunching = {}
for r in (2, 4, 8):
    repeated_row_minor = [[1] * r for _ in range(r)]
    fermion_bunching[str(r)] = det_int(repeated_row_minor)
    assert fermion_bunching[str(r)] == 0

# In contrast, the bosonic balanced-bunching probability amplitude used by V
# is sqrt(R!)/R^(R/2), nonzero. Verify its squared amplitude exactly.
boson_bunching_probability = {str(r): str(Fraction(factorial(r), r**r)) for r in (2, 4, 8)}
assert all(Fraction(v) > 0 for v in boson_bunching_probability.values())

# A fermionic alternative that keeps all R distinct rails needs no bunching:
# branch b occupies exactly one of two disjoint R-mode rail sets. Under
# independent loss eta=1/R, any-survivor probability is 1-(1-1/R)^R.
rail_readout = {}
for r in (4, 16, 64, 256):
    eta = Fraction(1, r)
    any_survivor = 1 - (1 - eta) ** r
    yes_gap = any_survivor / 6  # PostBQP gap p_x-1/2 >= 1/6
    assert yes_gap > Fraction(1, 10)
    rail_readout[str(r)] = {
        "any_survivor_decimal": f"{float(any_survivor):.12f}",
        "yes_no_gap_from_half_decimal": f"{float(yes_gap):.12f}",
        "exact_any_survivor": str(any_survivor) if r == 4 else "formula: 1-(1-1/R)^R",
        "expected_survivors": str(r * eta),
    }

# Exact two-branch check of the fermionic binary-loss filtering bound. A target
# block has mass p0 and one extra herald fermion has mass 1-p0. Filtering by
# g^N and losing the extra fermion gives posterior contamination below g^2/p0.
filter_checks = 0
for p0 in (Fraction(1, 3), Fraction(1, 2), Fraction(3, 4)):
    for g2 in (Fraction(1, 16), Fraction(1, 64)):
        for eta in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
            bad = (1 - p0) * (1 - eta) * g2
            post_bad = bad / (p0 + bad)
            assert post_bad <= g2 / p0
            filter_checks += 1

result = {
    "status": "PASS",
    "fermion_bunching_amplitude": fermion_bunching,
    "boson_bunching_probability": boson_bunching_probability,
    "uncompressed_fermion_readout": rail_readout,
    "binary_loss_filter_instances": filter_checks,
    "scope": "Exact small diagnostics; universal exterior-algebra and mixture arguments are in INITIAL.txt."
}
with open("work/cycle6/c03_s02/reviews/replayed_sources/fermion_transfer_checks.json", "w") as f:
    json.dump(result, f, indent=2)
    f.write("\n")
print(json.dumps(result, indent=2))

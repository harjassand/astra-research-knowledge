"""Finite exact diagnostics for global reset-macro F inequalities."""

from fractions import Fraction as Q


def F(b):
    return 0 if b == 0 else (5 if b == 1 else 2**b)


for b in range(1, 1001):
    birth = Q(b + 1)
    death = Q(5 * b * (b - 1))
    if b == 1:
        expected_F = F(2)
    else:
        # Stop immediately at the axis; do not include an A=2 reset there.
        death_F = 0 if b == 2 else max(F(b - 2), F(b - 1))
        expected_F = (birth * F(b + 1) + death * death_F) / (birth + death)
    assert expected_F <= Q(4, 5) * F(b), (b, expected_F)

# Verify the stated open box by its adverse rational endpoints.
c2_max = c3_max = c5_max = Q(21, 20)
c4_min = Q(79, 20)
c5_min = Q(19, 20)
d_min = c4_min + c5_min
assert 3 * (2 * c3_max + c2_max) < 2 * d_min
assert 8 * (3 * c3_max + c2_max) < 7 * d_min
assert 2 * c5_max < d_min
print('PASS: exact reset-macro F inequalities for b=1,...,1000.')
print('PASS: adverse rational endpoints establish the entire stated open parameter box.')
print('All-integer and renewal proofs are in report.md; these checks are finite diagnostics.')

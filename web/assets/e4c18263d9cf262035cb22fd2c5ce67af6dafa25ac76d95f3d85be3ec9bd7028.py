#!/usr/bin/env python3
"""Exact checks for the corrected N65 matching interface and conditional block algebra.

This script intentionally does NOT calculate the actual origin degree or
claim any abstract block dimensions occur in the retained N65 graph.
"""

from math import comb, gcd, isqrt


q = 8_796_093_022_237
r = 19_000
s = (q - 3) // 2

# Recheck the source matching at O. The line [1,0,0,0,0] has matched point
# (1,-1,0,1,0), whose canonical coordinate sum exceeds s, so it is not a
# retained line. The old assertion d_O=s was therefore invalid.
matched_point_of_origin_direction_1 = (1, q - 1, 0, 1, 0)
assert sum(matched_point_of_origin_direction_1) == q + 1
assert sum(matched_point_of_origin_direction_1) > s

# Explicit variation witness: mark m=(1,0,0,0,0) maps to label
# [1,1,1,0,0]; this label is incident to P=(0,1,1,q-1,q-1), not at its
# matched parameter t=1, so this retained direction-1 edge survives.
mark = (1, 0, 0, 0, 0)
assert sum(mark) <= s
label = (1, 1, 1, 0, 0)
point_p = (0, 1, 1, q - 1, q - 1)
a, b, c, d, e = label
t, y, z, w, v = point_p
assert (b - y - a * t) % q == 0
assert (c - z - b * t) % q == 0
assert (d - w - a * y) % q == 0
assert (e - v - a * z) % q == 0
assert point_p != mark

# Exact global edge count: all N=binom(s+5,5) matched lines retain q-1
# incidences. The average degree forces at least one actual regular point,
# though it does not identify that point or its block map.
N = comb(s + 5, 5)
edge_count = N * (q - 1)
point_count = q**5
threshold = 4 * r * r
average_floor, average_remainder = divmod(edge_count, point_count)
assert N == 13_712_537_977_926_146_630_731_028_580_700_279_228_663_771_409_617_594_022_371_704
assert average_floor == 2_290_649_224
assert average_remainder > 0
assert edge_count > point_count * threshold
assert average_floor + 1 == 2_290_649_225
assert average_floor + 1 > threshold

# All split arithmetic below is conditional on a hypothetical degree d=s;
# it is not the computed source degree at O.
conditional_degree = s
n2 = r + (conditional_degree % r)
n1, rem = divmod(conditional_degree - (r + 1) * n2, r)
assert q % 4 == 1
assert s == 4_398_046_511_117
assert conditional_degree % r == 3_117
assert n2 == 22_117
assert rem == 0
assert n1 == 231_454_014
assert conditional_degree >= 4 * r * r

# The obstruction witnesses are legal differences of indices from [r].
row_pair = (4, 4_750)
col_pair = (17_938, 12_903)
assert all(1 <= d < r for d in row_pair + col_pair)
assert row_pair[0] * row_pair[1] == r
assert col_pair[0] * col_pair[1] == n1

# Therefore every character order dividing either coordinate length kills
# the corresponding Cycle6 rectangle exponent 2*Delta_u*Delta_v.
for m, pair in ((r, row_pair), (n1, col_pair)):
    product = pair[0] * pair[1]
    # Since product=m, the exponent 2m is divisible by every divisor of m.
    assert product == m
    assert (2 * product) % m == 0

# Factor products certify that there is no prime coordinate quotient >= r.
assert 2**3 * 5**3 * 19 == r
assert 2 * 3 * 11 * 17 * 23 * 8_969 == n1
assert max(2, 3, 5, 7, 11, 13, 17, 19, 23, 8_969) < r

# Conditional abstract block B: size (r+1)*n2; no source-label claim.
p = r + 1
block_b_size = p * n2
assert block_b_size == 420_245_117
assert block_b_size <= s
block_a_start = block_b_size + 1
block_a_size = s - block_b_size
assert block_a_size == r * n1 == 4_397_626_266_000

# Primality certificate by trial division through floor(sqrt(p)).
def is_prime_small(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            return False
    return True


# Replay the supplied complete q-1 factorization and Pocklington witness 5.
q_factors = [2, 3, 13, 71, 227, 3_498_493]
assert q - 1 == 2**2 * 3 * 13 * 71 * 227 * 3_498_493
assert all(is_prime_small(pf) for pf in q_factors)
assert pow(5, q - 1, q) == 1
q_residues = [pow(5, (q - 1) // pf, q) for pf in q_factors]
assert all((residue - 1) % q != 0 for residue in q_residues)
assert all(gcd(residue - 1, q) == 1 for residue in q_residues)

# 5 has exact order q-1. The first-block table's rectangle exponent is
# nonzero and shorter than q-1.
exp_bound = (r - 1) * (n1 - 1)
assert exp_bound == 4_397_394_792_987
assert exp_bound < q - 1
assert n1 > r - 1

prime_divisors = [d for d in range(2, isqrt(p) + 1) if is_prime_small(d)]
assert isqrt(p) == 137
assert all(p % d != 0 for d in prime_divisors)
assert is_prime_small(p)
assert (q - 1) % p == 13_337
assert pow(2, 9_500, p) == 1
assert all(pow(2, 9_500 // d, p) != 1 for d in (2, 5, 19))
assert q % p == 13_338
assert pow(q, 9_500, p) == 1
assert all(pow(q, 9_500 // d, p) != 1 for d in (2, 5, 19))

# Quotient/remainder abstract indices give every coordinate exactly once,
# with beta ranging from 0 to n2-1. The inverse is a=alpha+p*beta+1.
assert p * n2 == block_b_size
for a in (1, 2, p, p + 1, block_b_size - 1, block_b_size):
    alpha = (a - 1) % p
    beta = (a - 1) // p
    assert 0 <= alpha < p and 0 <= beta < n2
    assert alpha + p * beta + 1 == a

# Conditional abstract block A's map is a quotient/remainder bijection on j.
for a in (block_a_start, block_a_start + 1, s - 1, s):
    j = a - block_a_start
    alpha = j % r
    beta = j // r
    assert 0 <= alpha < r and 0 <= beta < n1
    assert alpha + r * beta + block_a_start == a

# The shift set has r=p-1 distinct residues. Since p is prime, every
# nonzero rectangle difference product is nonzero modulo p.
assert r == p - 1
assert 2 % p != 0
print("Cycle7 correction checks passed; at least one actual regular point exists, d_O remains unevaluated, and block formulas are conditional.")

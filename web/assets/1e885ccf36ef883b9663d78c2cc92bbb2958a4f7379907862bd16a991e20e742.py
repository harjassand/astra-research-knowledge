"""Exact bookkeeping fixtures for the universal proof, not a sampler/FPRAS.

All determinant and field computations use integers/Fractions. Stability is
proved in the report and its chiral source, not certified by these fixtures.
"""
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
import json


def gm(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def determinant(matrix):
    size = len(matrix)
    result = [0, 0]
    for perm in permutations(range(size)):
        inv = sum(perm[i] > perm[j] for i in range(size) for j in range(i + 1, size))
        term = (1, 0)
        for i, j in enumerate(perm):
            term = gm(term, matrix[i][j])
        sign = (-1) ** inv
        result[0] += sign * term[0]
        result[1] += sign * term[1]
    return tuple(result)


def hard_bcs_coefficients(matrix, hole_masks=None):
    n = len(matrix)
    full = (1 << n) - 1
    f = {}
    for holes in range(1 << n) if hole_masks is None else hole_masks:
        if holes.bit_count() % 2:
            continue
        retained = [i for i in range(n) if not holes & (1 << i)]
        total = 0
        for left in combinations(retained, len(retained) // 2):
            right = [j for j in retained if j not in left]
            det = determinant([[matrix[i][j] for j in right] for i in left])
            total += det[0] ** 2 + det[1] ** 2
        f[holes] = total
    assert f[full] == 1
    return f


def fields(jset, variant):
    if variant == 0:
        return {j: Fraction(1) for j in jset}
    if variant == 1:
        return {j: Fraction(j + 2, j + 1) for j in jset}
    return {j: Fraction(2 ** (j + 1), 3 ** (j % 3 + 1)) for j in jset}


def fixture(f, n, S, T, a, variant):
    D = S ^ T
    assert D & (1 << a) and D.bit_count() % 2 == 0
    J = [j for j in range(n) if D & (1 << j) and j != a]
    d = len(J)
    w = fields(J, variant)
    coeff = [Fraction(0) for _ in range(d + 1)]
    # Exact full-T reciprocal twist, outside-D zero specialization, x_a=1.
    U = D
    while True:
        if U.bit_count() % 2 == 0:
            selected = [j for j in J if U & (1 << j)]
            term = Fraction(f[T ^ U])
            for j in selected:
                term *= w[j]
            coeff[len(selected)] += term
        if U == 0:
            break
        U = (U - 1) & D
    W = Fraction(1)
    for j in J:
        W *= w[j]
    A = sum(Fraction(f[T ^ (1 << a) ^ (1 << j)]) * w[j] for j in J)
    B = sum(Fraction(f[S ^ (1 << a) ^ (1 << j)]) / w[j] for j in J)
    assert coeff[0] == f[T]
    assert coeff[d] == f[S] * W
    assert coeff[1] == A
    assert coeff[d - 1] == W * B
    assert coeff[0] * coeff[d] <= coeff[1] * coeff[d - 1]
    assert f[S] * f[T] <= A * B
    return [str(c) for c in coeff]


def dense_matrix(n):
    return [[((3 * i + 2 * j + i * j) % 7 - 3, (i + 2 * j) % 3 - 1)
             for j in range(n)] for i in range(n)]


dense6 = hard_bcs_coefficients(dense_matrix(6))
endpoint_cases = 0
field_fixtures = 0
for S in dense6:
    for T in dense6:
        if S == T:
            continue
        for a in range(6):
            if (S ^ T) & (1 << a):
                endpoint_cases += 1
                for variant in range(3):
                    fixture(dense6, 6, S, T, a, variant)
                    field_fixtures += 1

# Eight ambient sites, six differing holes, two commonly occupied sites.
# This uses original F8 coefficients throughout, not a truncated F6.
dense8 = hard_bcs_coefficients(dense_matrix(8))
S = sum(1 << j for j in [0, 1, 2, 3])
T = sum(1 << j for j in [4, 5])
shared_core_polynomial = fixture(dense8, 8, S, T, 0, 1)

# Add two common holes and an occupied pair: twist must include common holes.
F10 = [[(0, 0) for _ in range(10)] for _ in range(10)]
for i in range(8):
    for j in range(8):
        F10[i][j] = dense_matrix(8)[i][j]
# Compute the 128 coefficients in the fixed eight-site slice directly from F10.
# Common holes 8,9 force their rows/columns out.
common_holes = (1 << 8) | (1 << 9)
f10_slice = hard_bcs_coefficients(F10, [mask | common_holes for mask in dense8])
assert f10_slice == {mask | common_holes: value for mask, value in dense8.items()}
common_holes_polynomial = fixture(f10_slice, 10, S | common_holes,
                                 T | common_holes, 0, 1)
assert common_holes_polynomial == shared_core_polynomial

# Leading-one sharpness inside the requested |S|=4, |T|=2 subclass.
pair6 = [[(0, 0) for _ in range(6)] for _ in range(6)]
for i, j in [(0, 1), (2, 3), (4, 5)]:
    pair6[i][j] = (1, 0)
pair_f = hard_bcs_coefficients(pair6)
S6 = sum(1 << j for j in [0, 1, 2, 3])
T6 = sum(1 << j for j in [4, 5])
sharp_products = [pair_f[S6 ^ 1 ^ (1 << j)] * pair_f[T6 ^ 1 ^ (1 << j)]
                  for j in range(1, 6)]
assert pair_f[S6] * pair_f[T6] == 1
assert sharp_products == [1, 0, 0, 0, 0]
sharp_poly = fixture(pair_f, 6, S6, T6, 0, 0)
assert sharp_poly == ["1", "1", "2", "2", "1", "1"]

# Boundary-root lemma is sharp at arbitrary odd degree.
# p=(1+2z)(1+3z^2)(1+5z^2) has roots -1/2 and imaginary conjugate pairs.
root_poly = [1, 2, 8, 16, 15, 30]
assert root_poly[0] * root_poly[-1] == root_poly[1] * root_poly[-2]
even_degree_counterexample = [1, 0, 1]
assert even_degree_counterexample[0] * even_degree_counterexample[-1] > 0
assert even_degree_counterexample[1] ** 2 == 0

result = {
    "status": "ALL_EXACT_ASSERTIONS_PASSED",
    "arithmetic": "Gaussian integers for complementary minors; rational fields",
    "dense6_even_coefficients": len(dense6),
    "dense6_positive_coefficients": sum(v > 0 for v in dense6.values()),
    "dense6_ordered_endpoint_and_distinguished_site_cases": endpoint_cases,
    "dense6_positive_field_fixtures": field_fixtures,
    "dense8_even_coefficients": len(dense8),
    "dense8_shared_occupied_core": [7, 8],
    "dense8_shared_core_holes_S": [1, 2, 3, 4],
    "dense8_shared_core_holes_T": [5, 6],
    "dense8_shared_core_polynomial_coefficients": shared_core_polynomial,
    "ambient10_shared_holes": [9, 10],
    "ambient10_full_twist_matches_expected_slice": True,
    "sharp_six_hole_exchange_squared_term_products": sharp_products,
    "sharp_six_hole_diagonal_polynomial_coefficients": sharp_poly,
    "sharp_odd_root_polynomial_coefficients": root_poly,
    "even_degree_failure_polynomial_coefficients": even_degree_counterexample,
    "not_executed": "microscopic sampler, FPRAS, stability-by-numerical-root-test",
}
path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))

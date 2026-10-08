#!/usr/bin/env python3
"""Exact finite Spin(9) orbit-POVM compiler/checker for Cycle 10.

Only the Python standard library is used.  The checker constructs PGL(2,8),
its signed-permutation extension in SO(9), exact Spin(9) lifts in the
octonionic real spinor model, and the three distinct projective seed orbits.
It verifies subset transitivity through k=4, orientation, seed stabilizers,
orbit sizes, exact tight-frame first moments, and rational effect coefficient
costs.  The Choi-moment identity follows from the exact signed-character and
subset-transitivity argument recorded in FINAL_REPORT.md.
"""

from fractions import Fraction
from itertools import combinations, product
from math import gcd
from functools import reduce

N_SPIN = 16
N_VECTOR = 9
GF8_MODULUS = 0b1011  # x^3 + x + 1
GROUP_SO_ORDER = 256 * 504


def gf_mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= GF8_MODULUS
    return out


def gf_inv(a):
    if not a:
        raise ZeroDivisionError("zero has no inverse")
    for b in range(1, 8):
        if gf_mul(a, b) == 1:
            return b
    raise AssertionError("nonzero GF(8) element had no inverse")


def projective_permutations():
    """Return all 504 normalized PGL(2,8) permutations of F_8 union infinity."""
    matrices = set()
    for a, b, c, d in product(range(8), repeat=4):
        if gf_mul(a, d) ^ gf_mul(b, c):
            row = (a, b, c, d)
            first = next(x for x in row if x)
            scale = gf_inv(first)
            matrices.add(tuple(gf_mul(scale, x) for x in row))

    def act(matrix, x):
        a, b, c, d = matrix
        if x == 8:  # infinity
            return 8 if c == 0 else gf_mul(a, gf_inv(c))
        denominator = gf_mul(c, x) ^ d
        numerator = gf_mul(a, x) ^ b
        return 8 if denominator == 0 else gf_mul(numerator, gf_inv(denominator))

    permutations = {tuple(act(m, x) for x in range(9)) for m in matrices}
    assert len(matrices) == 504
    assert len(permutations) == 504
    return permutations


def permutation_parity(p):
    inversions = sum(p[i] > p[j] for i in range(9) for j in range(i + 1, 9))
    return inversions & 1


def subset_orbit_sizes(permutations, k):
    remaining = set(map(frozenset, combinations(range(9), k)))
    sizes = []
    while remaining:
        seed = min(remaining, key=lambda item: tuple(sorted(item)))
        orbit = {frozenset(p[i] for i in seed) for p in permutations}
        sizes.append(len(orbit))
        remaining.difference_update(orbit)
    return sorted(sizes)


def zero_matrix(n=16):
    return [[0] * n for _ in range(n)]


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matadd(a, b, scale=1):
    return [[a[i][j] + scale * b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def gamma_model():
    """The exact real symmetric Cl_9 model from the Cycle 9 orbit proof."""
    fano = [(1, 2, 3), (1, 4, 5), (1, 7, 6), (2, 4, 6),
            (2, 5, 7), (3, 4, 7), (3, 6, 5)]
    table = {}
    for a, b, c in fano:
        for i, j, k in ((a, b, c), (b, c, a), (c, a, b)):
            table[i, j] = (1, k)
            table[j, i] = (-1, k)

    left = []
    for a in range(8):
        m = [[0] * 8 for _ in range(8)]
        for b in range(8):
            if a == 0:
                m[b][b] = 1
            elif b == 0:
                m[a][0] = 1
            elif a == b:
                m[0][b] = -1
            else:
                sign, c = table[a, b]
                m[c][b] = sign
        left.append(m)

    gammas = []
    for a in range(8):
        m = zero_matrix()
        conjugation_sign = 1 if a == 0 else -1
        for i in range(8):
            for j in range(8):
                m[i][8 + j] = conjugation_sign * left[a][i][j]
                m[8 + i][j] = left[a][i][j]
        gammas.append(m)
    m = zero_matrix()
    for i in range(8):
        m[i][i] = 1
        m[8 + i][8 + i] = -1
    gammas.append(m)
    return gammas


def transpose(a):
    return [list(row) for row in zip(*a)]


def transposition_factorization(p):
    """Return swaps whose successive action on coordinate labels yields p."""
    current = list(range(9))
    swaps = []
    for i in range(9):
        while current[i] != p[i]:
            j = current.index(p[i])
            swaps.append((i, j))
            current[i], current[j] = current[j], current[i]
    assert tuple(current) == tuple(p)
    return swaps


def reduce_matrix_fraction(matrix, denominator):
    common = reduce(gcd, (abs(x) for row in matrix for x in row), denominator)
    return [[x // common for x in row] for row in matrix], denominator // common


def spin_lift_of_permutation(p, gammas, identity):
    """Return integer M,d with U=M/d a Spin lift of the even permutation p."""
    swaps = transposition_factorization(p)
    assert len(swaps) % 2 == 0
    matrix = identity
    for a, b in swaps:
        # The unit vector (e_a-e_b)/sqrt(2) is a Clifford lift of that reflection.
        matrix = matmul(matrix, matadd(gammas[a], gammas[b], scale=-1))
    denominator = 2 ** (len(swaps) // 2)
    matrix, denominator = reduce_matrix_fraction(matrix, denominator)
    return matrix, denominator


def even_sign_monomials(gammas, identity):
    """The 256 even sign changes, as exact signed permutations on spinor coordinates."""
    actions = []
    for mask in range(256):
        vector_axes = [i for i in range(1, 9) if (mask >> (i - 1)) & 1]
        if len(vector_axes) & 1:
            vector_axes = [0] + vector_axes
        matrix = identity
        for i in vector_axes:
            matrix = matmul(matrix, gammas[i])
        row_sources, row_signs = [], []
        for row in matrix:
            nonzero = [j for j, value in enumerate(row) if value]
            assert len(nonzero) == 1
            source = nonzero[0]
            assert abs(row[source]) == 1
            row_sources.append(source)
            row_signs.append(row[source])
        actions.append((row_sources, row_signs))
    assert len(actions) == 256
    return actions


def apply_monomial(action, vector):
    sources, signs = action
    return [signs[i] * vector[sources[i]] for i in range(16)]


def primitive_key(numerators, denominator):
    common = reduce(gcd, (abs(x) for x in numerators), denominator)
    return tuple(x // common for x in numerators), denominator // common


def real_projector_key(column, denominator):
    entries = [column[i] * column[j] for i in range(16) for j in range(16)]
    return primitive_key(entries, denominator * denominator)


def balanced_projector_key(real_column, imag_column, denominator):
    # z=(a+i b)/(sqrt(2) d), and |z><z|=(aa^T+bb^T+i(ba^T-ab^T))/(2d^2).
    entries = []
    for i in range(16):
        for j in range(16):
            entries.append(real_column[i] * real_column[j] +
                           imag_column[i] * imag_column[j])
            entries.append(imag_column[i] * real_column[j] -
                           real_column[i] * imag_column[j])
    return primitive_key(entries, 2 * denominator * denominator)


def verify_projector_key(key, complex_entries):
    numerators, denominator = key
    if complex_entries:
        assert len(numerators) == 512
        real = numerators[0::2]
        imag = numerators[1::2]
        assert all(imag[16 * i + i] == 0 for i in range(16))
        assert all(real[16 * i + j] == real[16 * j + i]
                   for i in range(16) for j in range(16))
        assert all(imag[16 * i + j] == -imag[16 * j + i]
                   for i in range(16) for j in range(16))
        assert sum(real[16 * i + i] for i in range(16)) == denominator
        return [(x, y) for x, y in zip(real, imag)]
    assert len(numerators) == 256
    assert all(numerators[16 * i + j] == numerators[16 * j + i]
               for i in range(16) for j in range(16))
    assert sum(numerators[16 * i + i] for i in range(16)) == denominator
    return [(x, 0) for x in numerators]


def verify_tight_frame(projectors, complex_entries):
    """Check exactly that the uniform orbit mean is I/16."""
    outcome_count = len(projectors)
    total_real = [[Fraction(0) for _ in range(16)] for _ in range(16)]
    total_imag = [[Fraction(0) for _ in range(16)] for _ in range(16)]
    for key in projectors:
        numerators, denominator = key
        if complex_entries:
            real = numerators[0::2]
            imag = numerators[1::2]
        else:
            real = numerators
            imag = [0] * 256
        for i in range(16):
            for j in range(16):
                total_real[i][j] += Fraction(real[16 * i + j], denominator)
                total_imag[i][j] += Fraction(imag[16 * i + j], denominator)
    for i in range(16):
        for j in range(16):
            target = Fraction(outcome_count, 16) if i == j else Fraction(0)
            assert total_real[i][j] == target, (i, j, total_real[i][j], target)
            assert total_imag[i][j] == 0, (i, j, total_imag[i][j])


def max_effect_coefficient_bits(projectors, outcome_count):
    factor = Fraction(16, outcome_count)
    max_num_bits = 0
    max_den_bits = 0
    max_denominator = 1
    for numerators, denominator in projectors:
        for value in numerators:
            if value:
                coefficient = factor * Fraction(value, denominator)
                max_num_bits = max(max_num_bits, abs(coefficient.numerator).bit_length())
                max_den_bits = max(max_den_bits, coefficient.denominator.bit_length())
                max_denominator = max(max_denominator, coefficient.denominator)
    return max_num_bits, max_den_bits, max_denominator


def common_mixture_from_transfers(lambdas):
    """Return exact q_H,q_V,q_R with sum q_i eta_i >= 2 lambda - 1.

    Inputs are exact Fraction-compatible transfers in grade order 1..4.
    This is a bounded 2D rational feasibility search: write q_R=1-q_H-q_V,
    enumerate intersections of pairs of the seven half-space boundaries, and
    return a feasible vertex.  The Cycle 9 support theorem guarantees one for
    every compatible transfer vector in its stated channel class.
    """
    if len(lambdas) != 4:
        raise ValueError("supply lambda_1 through lambda_4")
    if any(isinstance(value, float) for value in lambdas):
        raise TypeError("use Fraction values or exact numeric strings, not floats")
    lam = tuple(Fraction(value) for value in lambdas)
    dimensions = (9, 36, 84, 126)
    vertices = ((0, 1, 7, 7), (1, 4, 4, 6), (1, 0, 0, 14))
    eta = tuple(tuple(Fraction(v[k], dimensions[k]) for k in range(4))
                for v in vertices)
    target = tuple(2 * value - 1 for value in lam)

    # Halfspaces a*x+b*y <= c, where x=q_H, y=q_V, q_R=1-x-y.
    inequalities = [
        (Fraction(-1), Fraction(0), Fraction(0)),   # q_H >= 0
        (Fraction(0), Fraction(-1), Fraction(0)),   # q_V >= 0
        (Fraction(1), Fraction(1), Fraction(1)),    # q_R >= 0
    ]
    for k in range(4):
        inequalities.append((eta[2][k] - eta[0][k],
                             eta[2][k] - eta[1][k],
                             eta[2][k] - target[k]))

    candidates = [(Fraction(0), Fraction(0)),
                  (Fraction(1), Fraction(0)),
                  (Fraction(0), Fraction(1))]
    for i, j in combinations(range(len(inequalities)), 2):
        a1, b1, c1 = inequalities[i]
        a2, b2, c2 = inequalities[j]
        determinant = a1 * b2 - a2 * b1
        if determinant:
            x = (c1 * b2 - c2 * b1) / determinant
            y = (a1 * c2 - a2 * c1) / determinant
            candidates.append((x, y))

    for x, y in candidates:
        if all(a * x + b * y <= c for a, b, c in inequalities):
            q = (x, y, 1 - x - y)
            assert all(value >= 0 for value in q)
            assert sum(q) == 1
            assert all(sum(q[i] * eta[i][k] for i in range(3)) >= target[k]
                       for k in range(4))
            return q
    return None


def make_projector_orbits(permutation_lifts, sign_actions):
    identity = [[int(i == j) for j in range(16)] for i in range(16)]
    specs = [("v_R", None, 144, 896), ("v_H", 8, 1152, 112),
             ("v_V", 1, 1008, 128)]
    result = {}
    for label, y_index, expected_orbit, expected_stabilizer in specs:
        orbit = set()
        stabilizer = 0
        for _p, matrix, denominator in permutation_lifts:
            x_col = [matrix[i][0] for i in range(16)]
            y_col = None if y_index is None else [matrix[i][y_index] for i in range(16)]
            for sign_action in sign_actions:
                x_image = apply_monomial(sign_action, x_col)
                if y_index is None:
                    if all(x_image[i] == 0 for i in range(1, 16)) and abs(x_image[0]) == denominator:
                        stabilizer += 1
                    orbit.add(real_projector_key(x_image, denominator))
                else:
                    y_image = apply_monomial(sign_action, y_col)
                    if all(x_image[i] == 0 and y_image[i] == 0
                           for i in range(16) if i not in (0, y_index)):
                        oriented_area = (x_image[0] * y_image[y_index] -
                                         x_image[y_index] * y_image[0])
                        if oriented_area > 0:
                            stabilizer += 1
                    orbit.add(balanced_projector_key(x_image, y_image, denominator))
        assert GROUP_SO_ORDER // expected_stabilizer == expected_orbit
        assert stabilizer == expected_stabilizer, (label, stabilizer)
        assert len(orbit) == expected_orbit, (label, len(orbit))
        is_complex = y_index is not None
        for key in orbit:
            verify_projector_key(key, is_complex)
        verify_tight_frame(orbit, is_complex)
        result[label] = {
            "outcomes": len(orbit),
            "stabilizer": stabilizer,
            "weight": Fraction(16, len(orbit)),
            "projectors": orbit,
            "coefficient_bits": max_effect_coefficient_bits(orbit, len(orbit)),
        }
    return result


def seed_moments(gammas, y_index):
    """Compute exact Clifford-grade squared moments for the three seed rays."""
    from itertools import combinations
    if y_index is None:
        # The real seed is the first octonionic spinor basis vector.
        seed_real, seed_imag = [1] + [0] * 15, [0] * 16
        balanced = False
    else:
        seed_real, seed_imag = [0] * 16, [0] * 16
        seed_real[0] = 1
        seed_imag[y_index] = 1
        balanced = True
    moments = [Fraction(0) for _ in range(5)]
    for k in range(5):
        phase_power = k * (k - 1) // 2
        phase = (1, 1j, -1, -1j)[phase_power % 4]
        for axes in combinations(range(9), k):
            word = [[int(i == j) for j in range(16)] for i in range(16)]
            for axis in axes:
                word = matmul(word, gammas[axis])
            # Evaluate <psi| i^phase_power Gamma_A |psi> exactly.
            xx = sum(seed_real[i] * word[i][j] * seed_real[j]
                     for i in range(16) for j in range(16))
            yy = sum(seed_imag[i] * word[i][j] * seed_imag[j]
                     for i in range(16) for j in range(16))
            xy = sum(seed_real[i] * word[i][j] * seed_imag[j]
                     for i in range(16) for j in range(16))
            yx = sum(seed_imag[i] * word[i][j] * seed_real[j]
                     for i in range(16) for j in range(16))
            if balanced:
                raw_real, raw_imag = Fraction(xx + yy, 2), Fraction(xy - yx, 2)
            else:
                raw_real, raw_imag = Fraction(xx), Fraction(0)
            if phase == 1:
                expectation_real, expectation_imag = raw_real, raw_imag
            elif phase == -1:
                expectation_real, expectation_imag = -raw_real, -raw_imag
            elif phase == 1j:
                expectation_real, expectation_imag = -raw_imag, raw_real
            else:
                expectation_real, expectation_imag = raw_imag, -raw_real
            assert expectation_imag == 0
            moments[k] += expectation_real ** 2
    return tuple(moments[1:])


def main():
    perms = projective_permutations()
    assert all(permutation_parity(p) == 0 for p in perms)
    target_counts = (9, 36, 84, 126)
    subset_orbits = [subset_orbit_sizes(perms, k) for k in range(1, 5)]
    assert subset_orbits == [[n] for n in target_counts], subset_orbits

    gammas = gamma_model()
    identity = [[int(i == j) for j in range(16)] for i in range(16)]
    for i, gamma in enumerate(gammas):
        assert transpose(gamma) == gamma
        for j, other in enumerate(gammas):
            anticommutator = matadd(matmul(gamma, other), matmul(other, gamma))
            target = [[2 * int(a == b) if i == j else 0 for b in range(16)]
                      for a in range(16)]
            assert anticommutator == target

    lifts = []
    max_lift_denominator = 1
    max_swap_factors = 0
    for p in sorted(perms):
        assert permutation_parity(p) == 0
        max_swap_factors = max(max_swap_factors, len(transposition_factorization(p)))
        matrix, denominator = spin_lift_of_permutation(p, gammas, identity)
        gram = matmul(matrix, transpose(matrix))
        assert all(gram[i][j] == denominator * denominator * int(i == j)
                   for i in range(16) for j in range(16))
        for axis in range(9):
            conjugated = matmul(matmul(matrix, gammas[axis]), transpose(matrix))
            target = [[denominator * denominator * value
                       for value in row] for row in gammas[p[axis]]]
            assert conjugated == target, (p, axis)
        lifts.append((p, matrix, denominator))
        max_lift_denominator = max(max_lift_denominator, denominator)

    sign_actions = even_sign_monomials(gammas, identity)
    orbits = make_projector_orbits(lifts, sign_actions)
    expected_moments = {
        "v_H": (0, 1, 7, 7),
        "v_V": (1, 4, 4, 6),
        "v_R": (1, 0, 0, 14),
    }
    seed_indices = {"v_H": 8, "v_V": 1, "v_R": None}
    for label, y_index in seed_indices.items():
        got = seed_moments(gammas, y_index)
        assert got == expected_moments[label], (label, got)

    # Exact smoke replay of the common-mixture interface on a rational transfer.
    d = (9, 36, 84, 126)
    seed_vertices = ((0, 1, 7, 7), (1, 4, 4, 6), (1, 0, 0, 14))
    sample_q = (Fraction(1, 5), Fraction(3, 10), Fraction(1, 2))
    sample_lambda = tuple(sum(sample_q[i] * Fraction(seed_vertices[i][k], d[k])
                              for i in range(3)) for k in range(4))
    compiled_q = common_mixture_from_transfers(sample_lambda)
    assert compiled_q is not None
    assert all(sum(compiled_q[i] * Fraction(seed_vertices[i][k], d[k])
                   for i in range(3)) >= 2 * sample_lambda[k] - 1
                   for k in range(4))

    print("PGL(2,8) order:", len(perms))
    print("PGL permutation parity:", "all even; subgroup of A_9 and SO(9)")
    print("subset orbit sizes for k=1..4:", subset_orbits)
    print("signed SO(9) subgroup order:", GROUP_SO_ORDER)
    print("Spin(9) preimage order:", 2 * GROUP_SO_ORDER)
    print("maximum coordinate-swap reflection factors:", max_swap_factors)
    print("maximum reduced lift denominator:", max_lift_denominator)
    for label in ("v_H", "v_V", "v_R"):
        item = orbits[label]
        bits = item["coefficient_bits"]
        print(f"{label}: stabilizer={item['stabilizer']}, outcomes={item['outcomes']}, "
              f"effect weight={item['weight']}, coefficient bits <= "
              f"({bits[0]} numerator, {bits[1]} denominator), max denominator={bits[2]}")
        print("  exact seed moments:", expected_moments[label])
    print("PASS: lift orthogonality, Cl_9 relations, orbit stabilizers, rational effects,")
    print("      exact first moment I/16, and PGL(2,8) subset transitivity through k=4")
    print("PASS: exact rational common-mixture compiler")


if __name__ == "__main__":
    main()

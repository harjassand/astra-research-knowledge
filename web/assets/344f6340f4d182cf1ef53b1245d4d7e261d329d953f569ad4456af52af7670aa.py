"""Finite transcription checks for the conditional Hamming/rank argument.

These checks validate small matrix identities and bounds. They do not validate
the released construction or prove the unrestricted mathematical statements.
Uses only Python's standard library.
"""

from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path
import random


def compose(p, q):
    return tuple(p[q[k]] for k in range(len(p)))


def inverse(p):
    ans = [0] * len(p)
    for k, v in enumerate(p):
        ans[v] = k
    return tuple(ans)


def pmatrix(p):
    return [[int(p[j] == i) for j in range(len(p))] for i in range(len(p))]


def rank(matrix, prime=None):
    a = [[x % prime if prime else Fraction(x) for x in row] for row in matrix]
    pivot_row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(pivot_row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = pow(a[pivot_row][col], -1, prime) if prime else 1 / a[pivot_row][col]
        a[pivot_row] = [(x * scale) % prime if prime else x * scale for x in a[pivot_row]]
        for i in range(pivot_row + 1, len(a)):
            scale = a[i][col]
            if scale:
                a[i] = [(x - scale * y) % prime if prime else x - scale * y
                        for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def block_matrix(blocks):
    d = len(blocks[0][0])
    return [[blocks[u][v][i][j]
             for v in range(len(blocks[u])) for j in range(d)]
            for u in range(len(blocks)) for i in range(d)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def subtract(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def multiply(a, b):
    return [[sum(x * y for x, y in zip(ar, bc)) for bc in zip(*b)] for ar in a]


def zero(n, m=None):
    return [[0] * (m or n) for _ in range(n)]


def moved(p, q):
    return sum(x != y for x, y in zip(p, q))


def fixed(p):
    return sum(x == i for i, x in enumerate(p))


checks = {}
perms4 = list(permutations(range(4)))
support_cases = 0
for p, q in product(perms4, repeat=2):
    diff = subtract(pmatrix(p), pmatrix(q))
    for field_prime in (2, 3, 5):
        assert rank(diff, field_prime) <= moved(p, q)
        support_cases += 1
checks["permutation_support_rank_bound"] = {"cases": support_cases, "status": "PASS"}

perms3 = list(permutations(range(3)))
block_cases = 0
for ps in product(perms3, repeat=4):
    grid = [ps[:2], ps[2:]]
    y = block_matrix([[pmatrix(p) for p in row] for row in grid])
    gram = multiply(y, list(map(list, zip(*y))))
    first = sum(gram[i][i] for i in range(6))
    second = sum(x * x for row in gram for x in row)
    rectangle_fixed = []
    for u, up, v, vp in product(range(2), repeat=4):
        if u == up or v == vp:
            continue
        rect = compose(compose(compose(grid[u][v], inverse(grid[up][v])),
                               grid[up][vp]), inverse(grid[u][vp]))
        rectangle_fixed.append(fixed(rect))
    epsilon = Fraction(max(rectangle_fixed), 3)
    assert first == 4 * 3
    assert second == (2 * 2**3 - 2**2) * 3 + sum(rectangle_fixed)
    assert second <= ((2 * 2**3 - 2**2) + 4 * epsilon) * 3
    real_rank = rank(y)
    finite_rank = rank(y, 5)
    assert real_rank >= Fraction(first**2, second)
    assert 2 * finite_rank >= real_rank
    assert finite_rank >= Fraction(4 * 3, 2 * (3 + epsilon))
    block_cases += 1
checks["trace_rank_and_fixed_prime_reduction"] = {"cases": block_cases, "status": "PASS"}

local_cases = 0
rng = random.Random(25220261007)
perms5 = list(permutations(range(5)))
for _ in range(100):
    # One Cartesian block: r=2, s=2, t=3, D=5, characteristic 7.
    left = [[rng.choice(perms5) for _ in range(2)] for _ in range(2)]
    right = [[rng.choice(perms5) for _ in range(3)] for _ in range(2)]
    z = zero(10)
    exact_sum = zero(10)
    total_changed_columns = 0
    max_defect = Fraction(0)
    for alpha, beta in product(range(2), range(3)):
        exact = [[compose(inverse(left[u][(alpha + v) % 2]),
                          right[v][(beta + u) % 3]) for v in range(2)]
                 for u in range(2)]
        assigned = [[rng.choice(perms5) if rng.random() < .25 else exact[u][v]
                     for v in range(2)] for u in range(2)]
        for u, v in product(range(2), repeat=2):
            changed = moved(assigned[u][v], exact[u][v])
            total_changed_columns += changed
            max_defect = max(max_defect, Fraction(changed, 5))
        z = add(z, block_matrix([[pmatrix(p) for p in row] for row in assigned]))
        exact_sum = add(exact_sum, block_matrix([[pmatrix(p) for p in row] for row in exact]))
    a = [[sum(pmatrix(inverse(left[u][j]))[i][k] for j in range(2))
          for k in range(5)] for u in range(2) for i in range(5)]
    b = [[sum(pmatrix(right[v][k])[i][j] for k in range(3))
          for v in range(2) for j in range(5)] for i in range(5)]
    assert exact_sum == multiply(a, b)
    assert rank(exact_sum, 7) <= 5
    assert rank(subtract(z, exact_sum), 7) <= total_changed_columns
    assert rank(z, 7) <= 5 + 4 * 6 * max_defect * 5
    local_cases += 1
checks["shifted_cartesian_factorization_and_perturbation"] = {"cases": local_cases, "status": "PASS"}

tensor_cases = 0
for _ in range(30):
    # A small interpolation fixture only: q=7, two marks on one affine line.
    # It does not satisfy the source's girth or strict budget requirements.
    ys = [block_matrix([[pmatrix(rng.choice(perms3)) for _ in range(2)]
                        for _ in range(2)]) for _ in range(2)]
    certificate = zero(12)
    for z in range(7):
        f = [(1 - z) % 7, z % 7]
        hz = [[f[i] * f[j] % 7 for j in range(2)] for i in range(2)]
        zz = zero(6)
        for label, mark in enumerate((0, 1)):
            if z != mark:
                zz = add(zz, ys[label])
        for i, j, u, v in product(range(2), range(2), range(6), range(6)):
            certificate[i * 6 + u][j * 6 + v] += hz[i][j] * zz[u][v]
    expected = zero(12)
    for label, y in enumerate(ys):
        for u, v in product(range(6), repeat=2):
            expected[label * 6 + u][label * 6 + v] = -y[u][v]
    assert all((x - y) % 7 == 0 for ar, br in zip(certificate, expected)
               for x, y in zip(ar, br))
    tensor_cases += 1
checks["interpolation_identity_for_arbitrary_block_assignments"] = {"cases": tensor_cases, "status": "PASS"}

result = {"scope": "Finite transcription checks only; no source geometry or universal proof validation",
          "checks": checks}
out = Path(__file__).with_name("nonsofic_adversary_checks.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))

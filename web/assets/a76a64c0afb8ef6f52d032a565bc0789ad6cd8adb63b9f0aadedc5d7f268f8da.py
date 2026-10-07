"""Exact arithmetic fixtures for the number theory scout.

The universal arguments are in number_theory.md. These fixtures only check the
displayed matrices and CRT construction; they do not validate cited papers.
"""

import itertools
import json
from fractions import Fraction
from math import comb, isqrt, prod
from pathlib import Path


def dot(left, gram, right):
    return sum(left[i] * gram[i][j] * right[j] for i in range(2) for j in range(2))


def automorphisms(gram):
    """Complete exact finite search, using lambda_min >= det / trace."""
    trace = gram[0][0] + gram[1][1]
    det = gram[0][0] * gram[1][1] - gram[0][1] ** 2
    assert trace > 0 and det > 0
    columns = []
    for index in range(2):
        squared_bound = gram[index][index] * trace / det
        bound = isqrt(squared_bound.numerator // squared_bound.denominator)
        vectors = [
            vector
            for vector in itertools.product(range(-bound, bound + 1), repeat=2)
            if dot(vector, gram, vector) == gram[index][index]
        ]
        columns.append(vectors)
    result = []
    for left, right in itertools.product(*columns):
        if dot(left, gram, right) != gram[0][1]:
            continue
        determinant = left[0] * right[1] - left[1] * right[0]
        if determinant not in (-1, 1):
            continue
        result.append([[left[0], right[0]], [left[1], right[1]]])
    return result


def crt(word, primes):
    modulus = prod(primes)
    return sum(
        residue * (modulus // prime) * pow(modulus // prime, -1, prime)
        for residue, prime in zip(word, primes)
    ) % modulus


fixture_gram = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(3)]]
group = automorphisms(fixture_gram)
assert len(group) == 4
assert [[-1, -1], [0, 1]] in group
assert 0 < fixture_gram[0][0] <= fixture_gram[1][1]
assert abs(2 * fixture_gram[0][1]) <= fixture_gram[0][0]
assert fixture_gram[0][1] != 0
assert fixture_gram[0][0] != fixture_gram[1][1]
# The paper's cosine test is not +/- 1/2.
assert 4 * fixture_gram[0][1] ** 2 != fixture_gram[0][0] * fixture_gram[1][1]

equal_diagonal = [[Fraction(1), Fraction(1, 4)], [Fraction(1, 4), Fraction(1)]]
assert len(automorphisms(equal_diagonal)) == 4

primes = [3, 5, 7, 11]
words = [word for word in itertools.product([0, 1], repeat=4) if sum(word) == 2]
points = sorted(crt(word, primes) for word in words)
assert len(points) == comb(4, 2) == 6
rows = []
for anchor in points:
    allowed = [point for point in points if all((point - anchor + 1) % p for p in primes)]
    assert allowed == [anchor]
    rows.append({"anchor": anchor, "allowed": allowed})
assert Fraction(1, 6) < Fraction(2, 3) ** 4

output = {
    "scope": "Exact displayed fixtures only; universal proofs are separate.",
    "bravais_counterexample": {
        "gram": [[2, 1], [1, 3]],
        "is_gauss_reduced": True,
        "paper_oblique_conditions_hold": True,
        "exact_automorphism_group": group,
        "actual_group_order": len(group),
        "claimed_group_order_under_paper_test": 2,
    },
    "second_missing_symmetry_wall": {
        "gram": [["1", "1/4"], ["1/4", "1"]],
        "exact_group_order": len(automorphisms(equal_diagonal)),
    },
    "odd_prime_sieve_fixture": {
        "primes": primes,
        "modulus": prod(primes),
        "binary_words": words,
        "integer_points": points,
        "anchor_rows": rows,
        "optimal_anchor_retention": "1/6",
        "proposed_odd_prime_improvement": "(2/3)^4 = 16/81",
        "proposed_improvement_is_false": True,
    },
}
destination = Path(__file__).with_name("number_theory_data") / "exact_checks.json"
destination.write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps(output, indent=2))

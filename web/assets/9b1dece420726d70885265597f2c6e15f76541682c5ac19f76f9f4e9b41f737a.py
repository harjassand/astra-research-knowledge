"""Independent full-coefficient comparisons for filter_rank_recognizer.py."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import random
from filter_rank_recognizer import (recognize_complementary, recognize_direct,
                                    recognize_counting_pair)


def exact_inertia(matrix):
    a = [row[:] for row in matrix]
    positive = negative = zero = 0
    while a:
        n = len(a)
        pivot = next((i for i in range(n) if a[i][i]), None)
        if pivot is not None:
            perm = [pivot] + [i for i in range(n) if i != pivot]
            a = [[a[i][j] for j in perm] for i in perm]
            p = a[0][0]
            positive += p > 0
            negative += p < 0
            a = [[a[i][j] - a[i][0] * a[0][j] / p for j in range(1, n)]
                 for i in range(1, n)]
            continue
        pair = next(((i, j) for i in range(n) for j in range(i + 1, n) if a[i][j]), None)
        if pair is None:
            zero += n
            break
        perm = list(pair) + [i for i in range(n) if i not in pair]
        a = [[a[i][j] for j in perm] for i in perm]
        p = a[0][1]
        positive += 1
        negative += 1
        a = [[a[i][j] - (a[i][0] * a[1][j] + a[i][1] * a[0][j]) / p
              for j in range(2, n)] for i in range(2, n)]
    return positive, negative, zero


def full_coefficient_hessian(tables, forced, complementary=True):
    blocks = []
    start = 0
    for b in tables:
        blocks.append(set(range(start, start + len(b) - 1)))
        start += len(b) - 1
    residual = [i for i in range(start) if i not in forced]
    matrix = [[F(0) for j in residual] for i in residual]
    for a, i in enumerate(residual):
        for c, j in enumerate(residual):
            if i == j:
                continue
            variables = forced | {i, j}
            value = F(1)
            for b, block in zip(tables, blocks):
                k = len(block - variables) if complementary else len(block & variables)
                value *= b[k]
            matrix[a][c] = value
    return matrix


randomizer = random.Random(812)
recognitions = full_hessians = witness_checks = 0
accepted = rejected = 0
for case in range(90):
    sizes = randomizer.choice([(2, 2), (3, 2), (2, 2, 2), (3, 3)])
    tables = [[F(randomizer.randrange(1, 9), randomizer.randrange(1, 9))
               for _ in range(q + 1)] for q in sizes]
    m = sum(sizes)
    for complementary in [True, False]:
        expected = [True] * (m + 1)
        for count in range(m - 1):
            for c in combinations(range(m), count):
                forced = set(c)
                positive = exact_inertia(full_coefficient_hessian(tables, forced, complementary))[0]
                rank = m - count - 2 if complementary else count + 2
                expected[rank] = expected[rank] and positive <= 1
                full_hessians += 1
        for rank in range(m + 1):
            result = (recognize_complementary(tables, rank) if complementary else
                      recognize_direct(tables, rank))
            assert result["accepted"] == expected[rank], (tables, rank, complementary, result)
            recognitions += 1
            accepted += result["accepted"]
            rejected += not result["accepted"]
            if not result["accepted"]:
                forced = set()
                start = 0
                for q, n in zip(sizes, result["residual_counts"]):
                    forced.update(range(start, start + q - n))
                    start += q
                assert exact_inertia(full_coefficient_hessian(tables, forced, complementary))[0] >= 2
                witness_checks += 1

# Cases that exercise zero diagonals, exact threshold equality, compensation,
# and both global orientations.
cases = {
    "uniform_threshold": ([[1, 1, 2], [1, 1, 2]], 2),
    "uniform_violation": ([[1, 1, 3], [1, 1, 3]], 2),
    "heterogeneous_compensation": ([[1, 1, 4], [1, 1, 1]], 2),
    "heterogeneous_violation": ([[1, 1, 5], [1, 1, 1]], 2),
    "direct_only": ([[6, 2, 1, 1], [6, 2, 1, 1]], 4),
    "complement_only": ([[1, 1, 2, 6], [1, 1, 2, 6]], 2),
}
case_results = {name: recognize_counting_pair(tables, rank)
                for name, (tables, rank) in cases.items()}
assert case_results["uniform_threshold"]["accepted"]
assert not case_results["uniform_violation"]["accepted"]
assert case_results["heterogeneous_compensation"]["accepted"]
assert not case_results["heterogeneous_violation"]["accepted"]
assert case_results["complement_only"]["orientation"] == "complementary"
assert case_results["direct_only"]["orientation"] == "direct"
assert not recognize_direct(cases["complement_only"][0], 2)["accepted"]

large = recognize_complementary([[1, 1, F(1 + i % 5)] for i in range(60)], 60)
assert not large["accepted"]
large_forced = set()
for i, n in enumerate(large["residual_counts"]):
    large_forced.update(range(2 * i, 2 * i + 2 - n))
assert sum(large["residual_counts"]) == 62

result = {
    "status": "PASS",
    "scope": "Rational dynamic-program recognition compared with full coefficient Hessian inertia; no counting FPRAS or quantum compiler.",
    "random_positive_table_instances": 90,
    "orientation_rank_recognitions": recognitions,
    "full_coefficient_hessians": full_hessians,
    "accepted_recognitions": accepted,
    "rejected_recognitions": rejected,
    "reconstructed_rejection_witnesses": witness_checks,
    "named_cases": case_results,
    "large_120_mode_run": large,
}
destination = Path(__file__).with_name("filter_rank_recognizer_check_result.json")
destination.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({key: value for key, value in result.items() if key not in ["named_cases", "large_120_mode_run"]}, indent=2))
print(json.dumps({"large_120_mode": {key: large[key] for key in
                  ["accepted", "states", "transitions", "maximum_fraction_bits"]}}, indent=2))

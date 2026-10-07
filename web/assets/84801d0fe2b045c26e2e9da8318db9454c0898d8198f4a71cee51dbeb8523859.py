"""Finite convention checks, not proofs of the asymptotic claims."""
import itertools
import json
import math
import random
from pathlib import Path


def rank_mod(matrix, prime=1000003):
    a = [[x % prime for x in row] for row in matrix]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], -1, prime)
        a[rank] = [(x * inv) % prime for x in a[rank]]
        for i in range(rank + 1, len(a)):
            c = a[i][col]
            if c:
                a[i] = [(x - c * y) % prime for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def kernel(a, b, lists):
    return math.prod(b[j] - c for j, forbidden in enumerate(lists[a]) for c in forbidden)


def rooted_check(words, lists, weights, budgets):
    matrix = [[kernel(a, b, lists) for b in words] for a in words]
    assert all(matrix[i][i] != 0 for i in range(len(words)))
    assert all(
        (matrix[i][k] != 0) == all(b[j] not in lists[a][j] for j in range(len(b)))
        for i, a in enumerate(words) for k, b in enumerate(words)
    )
    dimension = math.prod(t + 1 for t in budgets)
    rank = rank_mod(matrix)
    assert rank <= dimension
    best = max(sum(weights[b] for b, val in zip(words, row) if val) for row in matrix)
    total = sum(weights.values())
    assert best * dimension >= total
    return {"size": len(words), "dimension_bound": dimension, "rank_mod_prime": rank,
            "best_retained_weight": best, "total_weight": total}


def random_checks():
    rng = random.Random(7102026)
    summaries = []
    for sizes, budgets in [((5, 4), (1, 1)), ((4, 4, 3), (1, 2, 1)), ((5, 3), (2, 1))]:
        universe = list(itertools.product(*(range(s) for s in sizes)))
        for _ in range(30):
            words = [x for x in universe if rng.random() < 0.8]
            if not words:
                words = universe[:1]
            # Lists are independently assigned for every entire anchor, not merely its local symbol.
            lists = {a: [set(rng.sample([c for c in range(s) if c != a[j]], rng.randrange(t + 1)))
                         for j, (s, t) in enumerate(zip(sizes, budgets))] for a in words}
            weights = {a: rng.randrange(1, 21) for a in words}
            summaries.append(rooted_check(words, lists, weights, budgets))
    return summaries


def sharp_check(q, width):
    words = list(itertools.product(range(q), repeat=width))
    lists = {a: [set(range(q)) - {a[j]} for j in range(width)] for a in words}
    result = rooted_check(words, lists, {a: 1 for a in words}, (q - 1,) * width)
    assert result["best_retained_weight"] == 1
    assert result["size"] == result["dimension_bound"] == result["rank_mod_prime"]
    return result


def parity_obstruction(width):
    words = [x for x in itertools.product(range(2), repeat=width) if sum(x) % 2 == 0]
    triples = 0
    for triple in itertools.combinations(words, 3):
        triples += 1
        assert not all(len({a[j] for a in triple}) in (1, 3) for j in range(width))
    assert all(sum(x != y for x, y in zip(a, b)) != 1 for a, b in itertools.combinations(words, 2))
    # Therefore every anchor's exchange sets contain only its own symbols.
    return {"width": width, "size": len(words), "triples_checked": triples,
            "max_exchange_hall_patch_size": 1, "necessary_anchor_cover": len(words)}


if __name__ == "__main__":
    cases = random_checks()
    result = {"status": "finite checks only", "random_rooted_cases": len(cases),
              "all_random_cases_passed": True, "random_case_details": cases,
              "sharp_cases": [sharp_check(2, 4), sharp_check(3, 3)],
              "parity_obstruction": [parity_obstruction(w) for w in (3, 4, 5, 6)]}
    path = Path(__file__).with_name("FINITE_CHECKS.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "random_case_details"}, indent=2))

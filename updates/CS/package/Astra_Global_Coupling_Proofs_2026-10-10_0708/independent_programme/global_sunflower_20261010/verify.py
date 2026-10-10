"""Standard-library checks for the positive-replica sunflower investigation."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import log
from pathlib import Path
import json
import random


def valid(a, b, c):
    return len({a, b, c}) != 2


def construct(q):
    assert q >= 4 and q & (q - 1) == 0
    return [tuple((b, min(h, h ^ d)) for d in range(1, q))
            for b in range(2) for h in range(q)]


out = {"incidence_codes": [], "cubic_tests": 0, "correlations": [],
       "asymptotic_accounting": []}
for q in (4, 8, 16):
    rows = construct(q)
    assert len(rows) == len(set(rows)) == 2 * q
    for i in range(q - 1):
        counts = Counter(row[i] for row in rows)
        assert len(counts) == q and set(counts.values()) == {2}
    triples = 0
    for x, y, z in combinations(rows, 3):
        assert any(not valid(a, b, c) for a, b, c in zip(x, y, z))
        triples += 1
    out["incidence_codes"].append({"q": q, "rank": q - 1,
                                    "rows": len(rows), "triples_checked": triples})

rng = random.Random(20261010)
for q in range(1, 12):
    for _ in range(30):
        weights = [rng.randint(0, 30) for _ in range(q)]
        if sum(weights) == 0:
            weights[0] = 1
        u = [Fraction(v, sum(weights)) for v in weights]
        direct = sum(u[a] * u[b] * u[c] for a, b, c in product(range(q), repeat=3)
                     if valid(a, b, c))
        formula = 1 - 3 * sum(x*x for x in u) + 3 * sum(x*x*x for x in u)
        assert direct == formula and direct >= Fraction(1, 4)
        out["cubic_tests"] += 1

for q in range(3, 11):
    D = q*q - 3*q + 3
    f = [Fraction(q-1)] + [Fraction(-1)] * (q-1)
    variance = sum(x*x for x in f) / q
    conditional_second = Fraction(0)
    for b, c in product(range(q), repeat=2):
        allowed = [a for a in range(q) if valid(a, b, c)]
        mean = sum(f[a] for a in allowed) / len(allowed)
        conditional_second += Fraction(len(allowed), q*D) * mean*mean
    rho2 = conditional_second / variance
    assert rho2 == Fraction(3, D)
    out["correlations"].append({"q": q, "rho_squared": str(rho2)})

for q in (4, 8, 16, 64, 256, 1024, 65536):
    D = q*q - 3*q + 3
    local_sum = (q-1) * log(q*q / D)
    global_cost = 2 * log(2*q)
    out["asymptotic_accounting"].append({
        "q": q, "rank": q-1, "sum_local_KL": local_sum,
        "global_KL": global_cost, "sum_rho_squared": 3*(q-1)/D,
        "total_correlation": (q-1)*log(q)-log(2*q),
    })

path = Path(__file__).with_name("verification.json")
path.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))

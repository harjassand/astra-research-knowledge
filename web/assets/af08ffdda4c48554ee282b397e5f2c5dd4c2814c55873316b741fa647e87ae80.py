"""Exact checks for identities used in LEAF_UNION_THEOREM.md.

These finite checks validate arithmetic and incidence formulas, not asymptotic
correctness of a general selective algorithm. No approximate rank is inferred.
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import json

out = Path(__file__).resolve().parent

# Determine the maximum fitting L entirely by integer powers.
checks = []
for m in range(8, 81):
    n = 4 ** (4 * m)
    ell = m
    while 3 ** (ell + 1 - m) <= n:
        ell += 1
    d = m // 4
    alpha = comb(m, d) * 9 ** d
    beta0 = comb(ell, m) * 9 ** (ell - m)
    beta = comb(ell, m - d) * 9 ** (ell - m + d)
    r = comb(ell - m + d, d)
    assert beta0 * alpha == beta * r
    assert Fraction(alpha, 2 ** m) >= 1
    assert beta >= beta0
    for h in range(1, d + 1):
        ratio = Fraction(9 * (m - h + 1), ell - m + h)
        assert ratio > Fraction(81, 67)
    d_star = next(h for h in range(m + 1)
                  if comb(m, h) * 9 ** h >= 2 ** m)
    alpha_star = comb(m, d_star) * 9 ** d_star
    assert d_star <= d
    assert d_star > Fraction(m, 100)
    assert 1 <= Fraction(alpha_star, 2 ** m) < 900
    beta_star = comb(ell, m - d_star) * 9 ** (ell - m + d_star)
    assert beta_star >= beta0
    checks.append({"m": m, "L_max": ell, "d": d,
                   "d_star": d_star,
                   "crossing_degree_bound_passed": True,
                   "p_alpha_ge_one": True, "beta_ge_beta0": True})

# An arbitrary proper active subset must still satisfy the incidence inequality.
# Symbols 0..8 are P_ij / z_ij, symbol9 is P_0 / z_0.
ell, m, d = 4, 2, 1
outputs = []
for q in combinations(range(ell), m):
    q = frozenset(q)
    outer = [i for i in range(ell) if i not in q]
    for labels in product(range(9), repeat=ell - m):
        w = [9] * ell
        for i, label in zip(outer, labels):
            w[i] = label
        outputs.append(tuple(w))
active = outputs[::5] + outputs[1::11]
active = sorted(set(active))
support_sizes = {}
for w in active:
    q = [i for i, x in enumerate(w) if x == 9]
    for changed in combinations(q, d):
        for labels in product(range(9), repeat=d):
            leaf = list(w)
            for i, label in zip(changed, labels):
                leaf[i] = label
            leaf = tuple(leaf)
            support_sizes[leaf] = support_sizes.get(leaf, 0) + 1

alpha = comb(m, d) * 9 ** d
r = comb(ell - m + d, d)
assert sum(support_sizes.values()) == len(active) * alpha
assert max(support_sizes.values()) <= r
p = Fraction(1, 8)
lhs = sum(min(p * s, Fraction(1)) for s in support_sizes.values())
rhs = len(active) * alpha * min(p, Fraction(1, r))
assert lhs >= rhs

# Exact fixed-size hit probabilities and the exp(-ps) step's preceding product
# bound are checked through its algebraic Bernoulli proxy.
universe = len(active)
mask_size = universe // 8
for s in set(support_sizes.values()):
    miss = Fraction(comb(universe - s, mask_size),
                    comb(universe, mask_size))
    bernoulli_bound = (1 - Fraction(mask_size, universe)) ** s
    assert miss <= bernoulli_bound

result = {
    "status": "PASS",
    "exact_parameter_checks": len(checks),
    "checked_m_range": [8, 80],
    "active_subset_fixture": {
        "L": ell, "m": m, "d": d,
        "active_outputs": len(active),
        "incident_leaves": len(support_sizes),
        "max_support": max(support_sizes.values()),
        "sum_support": sum(support_sizes.values()),
        "incidence_identity_passed": True,
        "arbitrary_active_subset_bound_passed": True,
        "fixed_size_probability_bound_passed": True,
    },
    "scope": "Exact formula and finite incidence checks; no general algorithm.",
    "parameter_checks": checks,
}
(out / "leaf_union_checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "parameter_checks"}, indent=2))

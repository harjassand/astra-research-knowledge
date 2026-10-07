"""Exact finite checks for the frontier TCS scope barriers.

The asymptotic statements are proved in frontier_tcs.md. This script verifies
the local characteristic, normalization, noise, and exchange identities only.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


def alt_pair(u, v, bits, dim):
    ans = 0
    for bit, (a, b) in zip(bits, combinations(range(dim), 2)):
        ans ^= bit & (((u >> a) & 1) * ((v >> b) & 1)
                      ^ ((u >> b) & 1) * ((v >> a) & 1))
    return ans


def wedge_zero(u, v, dim):
    return all((((u >> a) & 1) * ((v >> b) & 1)
                ^ ((u >> b) & 1) * ((v >> a) & 1)) == 0
               for a, b in combinations(range(dim), 2))


cases = [
    (2, [1, 2], [F(1, 2)] * 2),
    (2, [1, 2, 3], [F(1, 3)] * 3),
    (2, [1, 2, 3], [F(1, 2), F(1, 3), F(1, 6)]),
    (3, [1, 2, 4, 7], [F(1, 4)] * 4),
    (2, [1, 1, 2, 3], [F(1, 4)] * 4),
]
checks = 0
collision_cases = []
for dim, images, probs in cases:
    assert sum(probs) == 1
    gamma_latent = sum(p * p for p in probs)
    masses = {}
    for v, p in zip(images, probs):
        masses[v] = masses.get(v, F(0)) + p
    gamma_feature = sum(p * p for p in masses.values())
    assert gamma_feature >= gamma_latent >= F(1, len(probs))
    forms = list(product([0, 1], repeat=comb(dim, 2)))
    for s in [3, 4]:
        beta = F(0)
        for choices in product(range(len(images)), repeat=s + 2):
            vs = [images[i] for i in choices]
            weight = F(1)
            for i in choices:
                weight *= probs[i]
            u = vs[0] ^ vs[1]
            w = 0
            for v in vs[2:]:
                w ^= v
            direct = sum((-1) ** sum(alt_pair(vs[i], vs[j], b, dim)
                                       for i in [0, 1]
                                       for j in range(2, s + 2))
                         for b in forms)
            assert F(direct, len(forms)) == int(wedge_zero(u, w, dim))
            checks += 1
            beta += weight * F(direct, len(forms))
        assert beta >= gamma_feature
        checks += 1
        collision_cases.append({"dim": dim, "images": images,
                                "probabilities": list(map(str, probs)),
                                "s": s, "gamma_latent": str(gamma_latent),
                                "gamma_feature": str(gamma_feature),
                                "character_mean": str(beta)})


def biclique_masks(n, s):
    edge_idx = {e: i for i, e in enumerate(combinations(range(n), 2))}
    masks = []
    for u in combinations(range(n), 2):
        others = [x for x in range(n) if x not in u]
        for v in combinations(others, s):
            mask = 0
            for a in u:
                for b in v:
                    mask ^= 1 << edge_idx[tuple(sorted([a, b]))]
            masks.append(mask)
    return masks


biclique_cases = []
for n in [5, 6, 7]:
    masks = biclique_masks(n, 3)
    assert len(masks) == len(set(masks)) == comb(n, 2) * comb(n - 2, 3)
    assert all(m.bit_count() == 6 for m in masks)
    checks += 2
    if n == 5:
        vals = [sum((-1) ** ((x & m).bit_count()) for m in masks)
                for x in range(1 << comb(n, 2))]
        assert sum(vals) == 0
        assert F(sum(x * x for x in vals), len(vals)) == len(masks)
        checks += 2
    biclique_cases.append({"n": n, "s": 3, "characters": len(masks),
                           "degree": 6, "distinct": True})

eps = F(1, 3)
d = 6
channel_multiplier = F(0)
for replacement in range(1 << d):
    k = replacement.bit_count()
    mass = eps ** k * (1 - eps) ** (d - k)
    bit_average = F(sum((-1) ** sum(z)
                        for z in product([0, 1], repeat=k)), 1 << k)
    channel_multiplier += mass * bit_average
assert channel_multiplier == (1 - eps) ** d
checks += 1


def short_relation(points):
    # phi(x)=(1,x) has constant coordinate; odd relations are impossible.
    for t in range(1, 5):
        for c in combinations(points, t):
            total = 0
            for x in c:
                total ^= 64 | x
            if total == 0:
                return list(c)
    return None


A = [0, 1, 2, 4, 8, 16, 32, 63]
B = [0, 1, 2, 4, 8, 16, 32, 15, 51]
assert short_relation(A) is None
assert short_relation(B) is None
witnesses = {}
for x in range(64):
    if x not in A:
        witness = short_relation(A + [x])
        assert witness is not None and x in witness
        witnesses[x] = witness
        checks += 1
assert all(x in witnesses for x in B if x not in A)
checks += 3

result = {
    "status": "PASS finite identities only; asymptotic proofs are written",
    "assertion_groups": checks,
    "collision_cases": collision_cases,
    "biclique_cases": biclique_cases,
    "noise": {"replacement_rate": str(eps), "degree": d,
              "multiplier": str(channel_multiplier)},
    "girth_restriction_exchange_failure": {
        "ambient_dimension": 6, "feature_map": "phi(x)=(1,x)",
        "girth_constraint": "no relation of size at most 4",
        "A": A, "B": B, "A_size": len(A), "B_size": len(B),
        "A_maximal": True, "B_admissible": True,
        "excluded_point_relation_witnesses": witnesses,
        "interpretation": "the girth-restricted subset system is not a matroid",
    },
}
out = Path(__file__).with_name("frontier_tcs_checks.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "assertion_groups": checks,
                  "collision_cases": len(collision_cases),
                  "exchange_excluded_points": len(witnesses),
                  "result": str(out.resolve())}, indent=2))

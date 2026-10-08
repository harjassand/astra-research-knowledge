"""Exact normal-form checks in k<a,b | ab=1>, not finite truncations.

The irreducible word b^i a^j is represented by (i,j).  The only rewrite
ab -> 1 is terminating and has no self-overlap, so the normal forms form
a basis.  This script checks algebraic identities; it does not compute K0.
"""
import json
from pathlib import Path


def add(x, y, p):
    z = dict(x)
    for w, c in y.items():
        z[w] = (z.get(w, 0) + c) % p
        if not z[w]:
            del z[w]
    return z


def neg(x, p):
    return {w: (-c) % p for w, c in x.items() if c % p}


def mul(x, y, p):
    z = {}
    for (i, j), c in x.items():
        for (k, l), d in y.items():
            m = min(j, k)
            w = (i + k - m, j + l - m)
            z[w] = (z.get(w, 0) + c * d) % p
            if not z[w]:
                del z[w]
    return z


def monomial(i, j):
    return {(i, j): 1}


checks = []
for p in [2, 3, 5, 7, 11]:
    one = monomial(0, 0)
    a = monomial(0, 1)
    b = monomial(1, 0)
    e = add(one, neg(mul(b, a, p), p), p)
    assert mul(a, b, p) == one
    assert mul(b, a, p) != one
    assert e and e != one
    assert mul(e, e, p) == e
    assert mul(a, e, p) == {}
    assert e == add(mul(a, b, p), neg(mul(b, a, p), p), p)
    assert sum(e.values()) % p == 0
    units = {}
    for i in range(8):
        for j in range(8):
            units[i, j] = mul(mul(monomial(i, 0), e, p), monomial(0, j), p)
    total = 0
    for (i, j), x in units.items():
        for (k, l), y in units.items():
            expected = units[i, l] if j == k else {}
            assert mul(x, y, p) == expected
            total += 1
    for m in range(1, 9):
        q = {}
        for i in range(m):
            q = add(q, units[i, i], p)
        assert q == add(one, neg(monomial(m, m), p), p)
        assert mul(q, q, p) == q
        assert mul(monomial(0, m), monomial(m, 0), p) == one
        assert mul(monomial(m, 0), monomial(0, m), p) == add(one, neg(q, p), p)
    checks.append({"prime": p, "matrix_unit_products": total, "tail_pairs": 8,
                   "one_sided_inverse": True, "proper_zero_aug_idempotent": True})

result = {
    "status": "FINITE-EVIDENCE",
    "scope": "Exact identities in symbolic bicyclic algebra normal forms",
    "not_claimed": "No group-ring counterexample or K0 computation by the script",
    "checks": checks,
}
target = Path(__file__).with_suffix('.json')
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))

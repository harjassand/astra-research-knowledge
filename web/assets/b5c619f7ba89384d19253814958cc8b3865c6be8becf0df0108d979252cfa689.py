"""Exact auxiliary check for the universal h-product constant.

This checks one polynomial expansion, not the source probabilistic cone theorem
or the infinite-tree reconstruction theorem.
"""
import json
import sympy as sp

x = sp.symbols("x1:4")
y = sp.symbols("y1:4")
s = sum(x[i] * y[i] for i in range(3))
R = [
    x[1] * y[2] + x[2] * y[1],
    x[0] * y[2] + x[2] * y[0],
    x[0] * y[1] + x[1] * y[0],
]
N = [x[i] + y[i] + R[i] for i in range(3)]
poly = sp.Poly(sp.expand(sp.prod(N) * (1 - 2 * s)), *x, *y)
classes = {"pure": [], "linear": [], "mixed": []}
for exponents, coefficient in poly.terms():
    dx, dy = sum(exponents[:3]), sum(exponents[3:])
    kind = (
        "pure" if dx == 0 or dy == 0
        else "linear" if dx == 1 or dy == 1
        else "mixed"
    )
    classes[kind].append((exponents, int(coefficient)))
assert set(classes["pure"]) == {
    ((1, 1, 1, 0, 0, 0), 1),
    ((0, 0, 0, 1, 1, 1), 1),
}
assert all(sum(e[:3]) >= 2 and sum(e[3:]) >= 2
           for e, _ in classes["mixed"])
mixed_l1 = sum(abs(c) for _, c in classes["mixed"])
assert mixed_l1 == 364
result = {
    "sympy_version": sp.__version__,
    "scope": "exact h-product polynomial coefficient accounting only",
    "classes": {
        kind: {"count": len(terms), "coefficient_l1": sum(abs(c) for _, c in terms)}
        for kind, terms in classes.items()
    },
    "denominator_remainder_constant": 12,
    "universal_h_product_constant": 12 + mixed_l1,
    "all_terms": classes,
}
print(json.dumps(result, indent=2))

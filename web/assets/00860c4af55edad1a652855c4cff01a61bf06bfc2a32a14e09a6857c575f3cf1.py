#!/usr/bin/env python3
"""Exact polynomial expansion for the 2x2 Strassen escape witness.

Uses integer coefficient dictionaries, so the check is exact over Z and has
no dependency on a symbolic-algebra package.
"""
from __future__ import annotations

import json
from pathlib import Path

Poly = dict[tuple[str, ...], int]


def var(name: str) -> Poly:
    return {(name,): 1}


def add(*polys: Poly) -> Poly:
    out: Poly = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] = out.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def neg(poly: Poly) -> Poly:
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def sub(left: Poly, right: Poly) -> Poly:
    return add(left, neg(right))


def mul(left: Poly, right: Poly) -> Poly:
    out: Poly = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(sorted(lm + rm))
            out[monomial] = out.get(monomial, 0) + lc * rc
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def same(actual: Poly, expected: Poly) -> bool:
    return actual == expected


def main() -> None:
    a11, a12, a21, a22 = map(var, ("a11", "a12", "a21", "a22"))
    b11, b12, b21, b22 = map(var, ("b11", "b12", "b21", "b22"))

    p1 = mul(add(a11, a22), add(b11, b22))
    p2 = mul(add(a21, a22), b11)
    p3 = mul(a11, sub(b12, b22))
    p4 = mul(a22, sub(b21, b11))
    p5 = mul(add(a11, a12), b22)
    p6 = mul(sub(a21, a11), add(b11, b12))
    p7 = mul(sub(a12, a22), add(b21, b22))

    outputs = {
        "c11": add(p1, p4, neg(p5), p7),
        "c12": add(p3, p5),
        "c21": add(p2, p4),
        "c22": add(p1, neg(p2), p3, p6),
    }
    targets = {
        "c11": add(mul(a11, b11), mul(a12, b21)),
        "c12": add(mul(a11, b12), mul(a12, b22)),
        "c21": add(mul(a21, b11), mul(a22, b21)),
        "c22": add(mul(a21, b12), mul(a22, b22)),
    }
    assert all(same(outputs[name], targets[name]) for name in outputs)

    # Row supports on the X side and column supports on the Y side of each
    # Strassen factor. A gate is pair-local exactly when both sets are singletons.
    support = {
        "p1": ({1, 2}, {1, 2}),
        "p2": ({2}, {1}),
        "p3": ({1}, {2}),
        "p4": ({2}, {1}),
        "p5": ({1}, {2}),
        "p6": ({1, 2}, {1, 2}),
        "p7": ({1, 2}, {1, 2}),
    }
    local_products = sorted(
        name for name, (rows, columns) in support.items()
        if len(rows) == 1 and len(columns) == 1
    )
    mixed_products = sorted(set(support) - set(local_products))
    assert local_products == ["p2", "p3", "p4", "p5"]
    assert mixed_products == ["p1", "p6", "p7"]

    result = {
        "status": "PASS",
        "coefficient_domain": "Z",
        "outputs_checked": sorted(outputs),
        "products_in_strassen_witness": 7,
        "pair_local_strassen_products": local_products,
        "mixed_support_strassen_products": mixed_products,
        "pair_local_product_count_for_m4_D2": 8,
        "scope": "finite exact identity check only; does not prove arbitrary-mask claims",
    }
    path = Path(__file__).with_name("exact_check.json")
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact eventual-activity checker for rational Puiseux affine families.

This tool checks one *supplied* finite family. It does not synthesize the
family. Input and output formats are described in EFFECTIVE_FIXED_FAMILY.md.
Only Python's standard library is used.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Iterable


Q = Fraction
Poly = dict[int, Q]  # sparse polynomial in u, with nonnegative integer powers


def q(value: object) -> Q:
    if isinstance(value, int):
        return Q(value)
    if isinstance(value, str):
        return Q(value)
    raise TypeError(f"expected an integer or rational string, got {value!r}")


def vec(items: list[object]) -> tuple[Q, ...]:
    return tuple(q(x) for x in items)


def add_poly(a: Poly, b: Poly, factor: Q = Q(1)) -> Poly:
    out = dict(a)
    for e, c in b.items():
        out[e] = out.get(e, Q(0)) + factor * c
        if out[e] == 0:
            del out[e]
    return out


def scale_poly(a: Poly, factor: Q) -> Poly:
    if factor == 0:
        return {}
    return {e: factor * c for e, c in a.items() if factor * c}


def poly_terms(terms: list[dict[str, str]], n: int, shift: int) -> Poly:
    """Convert sum c*h^gamma to sum c*u^(shift+n*gamma)."""
    out: Poly = {}
    for term in terms:
        coefficient = q(term["coefficient"])
        exponent = Q(shift) + n * q(term["exponent"])
        if exponent.denominator != 1 or exponent < 0:
            raise ValueError(f"non-polynomial scaled exponent {exponent}")
        e = int(exponent)
        out[e] = out.get(e, Q(0)) + coefficient
        if out[e] == 0:
            del out[e]
    return out


def lead_sign(p: Poly) -> int:
    if not p:
        return 0
    c = p[min(p)]
    return 1 if c > 0 else -1


def stable_sign_exponent(p: Poly) -> int:
    """Return T>=1 so sign(p(u)) is its leading sign for 0<u<2^-T."""
    if not p:
        return 1
    e0 = min(p)
    lead = abs(p[e0])
    tail = sum((abs(c) for e, c in p.items() if e != e0), Q(0))
    if tail == 0:
        return 1
    ratio = lead / (2 * tail)
    t = 1
    while Q(1, 2**t) >= ratio:
        t += 1
    return t


def eventually_nonnegative(p: Poly) -> bool:
    return lead_sign(p) >= 0


def determinant(a: list[list[Q]]) -> Q:
    n = len(a)
    if n == 0:
        return Q(1)
    m = [row[:] for row in a]
    det = Q(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if m[r][col] != 0), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            det = -det
        p = m[col][col]
        det *= p
        for r in range(col + 1, n):
            f = m[r][col] / p
            if f:
                for k in range(col + 1, n):
                    m[r][k] -= f * m[col][k]
                m[r][col] = Q(0)
    return det


def inverse(a: list[list[Q]]) -> list[list[Q]]:
    n = len(a)
    m = [row[:] + [Q(i == j) for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if m[r][col] != 0), None)
        if pivot is None:
            raise ValueError("attempted to invert a singular matrix")
        m[col], m[pivot] = m[pivot], m[col]
        p = m[col][col]
        m[col] = [x / p for x in m[col]]
        for r in range(n):
            if r == col:
                continue
            f = m[r][col]
            if f:
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [row[n:] for row in m]


def common_denominator(values: Iterable[Q]) -> int:
    n = 1
    for value in values:
        n = math.lcm(n, value.denominator)
    return n


def ceil_fraction(x: Q) -> int:
    return -((-x.numerator) // x.denominator)


def build_comparison_vectors(diagram: dict, d: int) -> set[tuple[Q, ...]]:
    vectors = {tuple(Q(i == j) for i in range(d)) for j in range(d)}
    sources = [vec(row) for row in diagram["sources"]]
    targets = [vec(row) for row in diagram["targets"]]
    if len(sources) != len(targets) or any(len(v) != d for v in sources + targets):
        raise ValueError("diagram sources/targets must have matching dimension")
    for source, target in zip(sources, targets):
        nu = tuple(t - s for s, t in zip(source, target))
        if any(nu):
            vectors.add(nu)
    for y in sources:
        for z in sources:
            diff = tuple(zi - yi for yi, zi in zip(y, z))
            if any(diff):
                vectors.add(diff)
    return vectors


def point_tolerance(slope: tuple[Q, ...], directions: Iterable[tuple[Q, ...]]) -> Q:
    values = [Q(1, 2)]
    for v in directions:
        dot = sum((x * y for x, y in zip(slope, v)), Q(0))
        if dot:
            norm = sum((abs(x) for x in v), Q(0))
            values.append(abs(dot) / (2 * norm))
    return min(values)


def compute_tolerances(data: dict, dimension: int, labels: list[dict]) -> list[Q]:
    if "comparison_vectors" in data:
        directions = {vec(row) for row in data["comparison_vectors"]}
    elif "diagram" in data:
        directions = build_comparison_vectors(data["diagram"], dimension)
    else:
        raise ValueError("input must provide diagram or comparison_vectors")
    if any(len(v) != dimension for v in directions):
        raise ValueError("comparison vectors must match family dimension")
    return [point_tolerance(vec(label["slope"]), directions) for label in labels]


def validate_small_offsets(data: dict, labels: list[dict]) -> None:
    a = q(data.get("a", "-1"))
    for j, label in enumerate(labels):
        combined: dict[Q, Q] = {}
        for term in label.get("offset", []):
            exponent = q(term["exponent"])
            combined[exponent] = combined.get(exponent, Q(0)) + q(term["coefficient"])
        if any(coefficient and exponent <= a for exponent, coefficient in combined.items()):
            raise ValueError(f"label {j} offset is not o(h^a)")


def as_poly(terms: list[dict[str, str]], n: int, shift: int) -> Poly:
    return poly_terms(terms, n, shift)


def row_constraints(data: dict, n: int, shift: int, tolerances: list[Q]):
    labels = data["family"]
    d = len(labels[0]["slope"])
    a, b = q(data.get("a", "-1")), q(data.get("b", "1"))
    h_terms = lambda exponent: [{"coefficient": "1", "exponent": str(exponent)}]
    all_constraints = []
    for j, label in enumerate(labels):
        slope_j = vec(label["slope"])
        offset_j = as_poly(label.get("offset", []), n, shift)
        for i in range(d):
            for side in ("above", "below"):
                rows: list[tuple[tuple[Q, ...], Poly, str]] = []
                # h^b <= x_i <= h^a, where x_i=h^{p_i}.
                for k in range(d):
                    unit = tuple(Q(k == ell) for ell in range(d))
                    neg_unit = tuple(-v for v in unit)
                    rows.append((unit, as_poly(h_terms(a), n, shift), "cube-upper"))
                    rows.append((neg_unit, scale_poly(as_poly(h_terms(b), n, shift), Q(-1)), "cube-lower"))
                # The chosen label is active; weak rows deliberately retain ties.
                for k, other in enumerate(labels):
                    if k == j:
                        continue
                    slope_k = vec(other["slope"])
                    offset_k = as_poly(other.get("offset", []), n, shift)
                    lhs = tuple(x - y for x, y in zip(slope_j, slope_k))
                    rhs = add_poly(offset_k, offset_j, Q(-1))
                    rows.append((lhs, rhs, f"active-{k}"))
                e = tolerances[j]
                if side == "above":
                    # p_i-r_i >= E iff x_i <= h^(r_i+E).
                    rhs_exp = slope_j[i] + e
                    unit = tuple(Q(i == k) for k in range(d))
                    rows.append((unit, as_poly(h_terms(rhs_exp), n, shift), "bad-above"))
                else:
                    # r_i-p_i >= E iff x_i >= h^(r_i-E).
                    rhs_exp = slope_j[i] - e
                    unit = tuple(-Q(i == k) for k in range(d))
                    rows.append((unit, scale_poly(as_poly(h_terms(rhs_exp), n, shift), Q(-1)), "bad-below"))
                all_constraints.append((j, i, side, rows))
    return all_constraints


def poly_to_json(p: Poly) -> list[dict[str, str]]:
    return [{"power_u": str(e), "coefficient": str(p[e])} for e in sorted(p)]


def one_event_result(rows: list[tuple[tuple[Q, ...], Poly, str]], d: int):
    coefficients = [list(row) for row, _, _ in rows]
    rhs = [poly for _, poly, _ in rows]
    bases = []
    for indices in itertools.combinations(range(len(rows)), d):
        matrix = [coefficients[i] for i in indices]
        if determinant(matrix) == 0:
            continue
        inv = inverse(matrix)
        point = []
        for i in range(d):
            p: Poly = {}
            for k, row_idx in enumerate(indices):
                p = add_poly(p, scale_poly(rhs[row_idx], inv[i][k]))
            point.append(p)
        residuals = []
        for row, bound, tag in rows:
            value = dict(bound)
            for coeff, coord in zip(row, point):
                value = add_poly(value, scale_poly(coord, -coeff))
            residuals.append((tag, value))
        bases.append((indices, point, residuals))
    if not bases:
        raise RuntimeError("no full-rank basis; box constraints should span the space")

    feasible_bases = []
    for indices, point, residuals in bases:
        if all(eventually_nonnegative(p) for _, p in residuals):
            stable = max([stable_sign_exponent(p) for _, p in residuals] + [1])
            feasible_bases.append((stable, indices, point, residuals))
    if feasible_bases:
        stable, indices, point, residuals = min(feasible_bases, key=lambda x: x[0])
        return {
            "eventually_feasible": True,
            "T": stable,
            "basis_rows": list(indices),
            "vertex_y": [poly_to_json(p) for p in point],
            "residuals": [
                {"constraint": tag, "poly": poly_to_json(p), "eventual_sign": lead_sign(p)}
                for tag, p in residuals
            ],
        }

    basis_t = []
    for indices, point, residuals in bases:
        negative = [(tag, p) for tag, p in residuals if lead_sign(p) < 0]
        if not negative:
            raise RuntimeError("basis classification inconsistency")
        tag, witness = negative[0]
        basis_t.append((stable_sign_exponent(witness), indices, tag, witness))
    t = max(item[0] for item in basis_t)
    return {
        "eventually_feasible": False,
        "T": t,
        "basis_count": len(bases),
        "basis_negative_witnesses": [
            {"T": item[0], "basis_rows": list(item[1]), "constraint": item[2], "poly": poly_to_json(item[3])}
            for item in basis_t
        ],
    }


def verify(data: dict) -> dict:
    labels = data["family"]
    if not labels:
        raise ValueError("family must be nonempty")
    validate_small_offsets(data, labels)
    dimension = len(labels[0]["slope"])
    if dimension == 0:
        return {"status": "CERTIFIED_ACTIVITY_CUTOFF", "dimension": 0, "h_act": "1/2", "note": "vacuous zero-dimensional activity"}
    for label in labels:
        slope = vec(label["slope"])
        if len(slope) != dimension:
            raise ValueError("all slopes must have one common dimension")
        for s in slope:
            if s < q(data.get("a", "-1")) or s > q(data.get("b", "1")):
                raise ValueError("slope outside exponent cube")

    tolerances = compute_tolerances(data, dimension, labels)
    all_exponents: list[Q] = [q(data.get("a", "-1")), q(data.get("b", "1"))]
    for label, e in zip(labels, tolerances):
        slope = vec(label["slope"])
        all_exponents.extend([slope[i] + e for i in range(dimension)])
        all_exponents.extend([slope[i] - e for i in range(dimension)])
        all_exponents.extend(q(term["exponent"]) for term in label.get("offset", []))
    n = math.lcm(common_denominator(all_exponents), 2)
    min_exp = min(Q(0), *(all_exponents))
    shift = max(n, ceil_fraction(-n * min_exp))
    events = row_constraints(data, n, shift, tolerances)

    event_results = []
    for j, i, side, rows in events:
        result = one_event_result(rows, dimension)
        event_results.append(result)
        if result["eventually_feasible"]:
            return {
                "status": "NO_CUTOFF",
                "reason": "a bad active point exists at every sufficiently small scale",
                "dimension": dimension,
                "label": j,
                "coordinate": i,
                "bad_side": side,
                "tolerance": str(tolerances[j]),
                "h=u^N": n,
                "y=u^M*x": shift,
                "witness": result,
            }

    max_t = max((result["T"] for result in event_results), default=1)
    return {
        "status": "CERTIFIED_ACTIVITY_CUTOFF",
        "dimension": dimension,
        "label_count": len(labels),
        "comparison_direction_count": len(
            data.get("comparison_vectors", [])
            if "comparison_vectors" in data
            else build_comparison_vectors(data["diagram"], dimension)
        ),
        "tolerances": [str(x) for x in tolerances],
        "h=u^N": n,
        "y=u^M*x": shift,
        "T": max_t,
        "h_act": f"2^(-{n * max_t})",
        "basis_events": len(events),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="exact rational JSON input")
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    print(json.dumps(verify(data), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

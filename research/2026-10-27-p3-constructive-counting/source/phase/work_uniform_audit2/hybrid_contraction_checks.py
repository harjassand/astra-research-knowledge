#!/usr/bin/env python3
"""Exact small checks of the hybrid representation, not a fast SAT solver.

Only Python's standard library is used. The local parity summaries are actually
manufactured from raw 2-CNF by exhaustive unweighted greedy counts. The ensuing
lift and contraction are exact modulo 2**(n+1). Finite contractions are exhaustive.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
import random


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def poly_mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def lift_remainders(ell):
    # p_ell(Y)=(1-Y)^ell sum_{j<ell} binom(ell+j-1,j)Y^j.
    a = [(-1)**i * math.comb(ell, i) for i in range(ell+1)]
    b = [math.comb(ell+j-1, j) for j in range(ell)]
    p = poly_mul(a, b)
    out = []
    for _ in range(ell):
        q = [0] * max(1, len(p)-2)
        r = p[:]
        for d in range(len(r)-1, 1, -1):
            c = r[d]
            q[d-2] += c
            r[d] -= c
            r[d-1] += c  # Subtract c Y^(d-2)(Y^2-Y).
        out.append((r[0], r[1] if len(r)>1 else 0))
        p = trim(q)
    assert p == [0]
    return out


def ring_mul(a, b, modulus):
    ell = len(a)
    c = [0]*ell
    for i, x in enumerate(a):
        for j in range(ell-i):
            c[i+j] = (c[i+j] + x*b[j]) % modulus
    return c


def clause_value(clause, x):
    return any(bool((x >> (abs(lit)-1)) & 1) == (lit > 0)
               for lit in clause)


def formula_value(clauses, x):
    return all(clause_value(c, x) for c in clauses)


def gf2_product(a, b):
    out = set()
    for x in a:
        for y in b:
            z = x | y
            if z in out:
                out.remove(z)
            else:
                out.add(z)
    return out


def violation_polynomial(clause):
    p = {0}
    for lit in clause:
        bit = 1 << (abs(lit)-1)
        p = gf2_product(p, {0, bit} if lit > 0 else {bit})
    return p


def manufacture_rows(n, clauses):
    """Small exact analogue using all parity rows, each chosen by count only."""
    m = len(clauses)
    violations = [sum((not clause_value(c, x)) << i
                      for i, c in enumerate(clauses)) for x in range(1 << n)]
    accepted = list(range(1 << n))
    rows = []
    for _ in range(n+1):
        candidates = range(1 << m)
        best = min(candidates,
                   key=lambda row: (sum((violations[x]&row).bit_count()%2 == 0
                                         for x in accepted), row))
        rows.append(best)
        accepted = [x for x in accepted if (violations[x]&best).bit_count()%2 == 0]
    true = [x for x in range(1 << n) if violations[x] == 0]
    assert accepted == true
    rows = sorted(set(rows) - {0})
    equations = []
    vp = [violation_polynomial(c) for c in clauses]
    for row in rows:
        p = set()
        for i in range(m):
            if row >> i & 1:
                p ^= vp[i]
        if p:
            equations.append(sorted(p))
    return rows, equations, len(true)


def local_coefficients(n, equation, ell, modulus, ej):
    scope = sorted({v for mon in equation for v in range(n) if mon >> v & 1})
    coeff = []
    for mask in range(1 << len(scope)):
        x = sum((1 << v) for i, v in enumerate(scope) if mask >> i & 1)
        y = sum((mon & x) == mon for mon in equation)
        h = y*(y-1)
        coeff.append([((a+b*y)*pow(h, j, modulus)) % modulus
                      for j, (a, b) in enumerate(ej)])
    # Boolean Möbius inversion, over the entire truncated coefficient ring.
    for bit in range(len(scope)):
        for mask in range(1 << len(scope)):
            if mask >> bit & 1:
                lo = mask ^ (1 << bit)
                coeff[mask] = [(x-y) % modulus
                               for x, y in zip(coeff[mask], coeff[lo])]
    return scope, coeff


def rank_subset(selected, universe):
    choices = itertools.combinations(universe, len(selected))
    return next(i for i, choice in enumerate(choices) if tuple(selected) == choice)


def decode_subset(index, universe, size):
    return tuple(next(itertools.islice(itertools.combinations(universe, size), index, None)))


def run_fixture(n, binary, direct):
    ell = n+1
    modulus = 1 << ell
    ej = lift_remainders(ell)
    rows, equations, binary_count = manufacture_rows(n, binary)
    local = [local_coefficients(n, p, ell, modulus, ej) for p in equations]
    incidences = [(i, v) for i, (scope, _) in enumerate(local) for v in scope]
    if len(incidences) > 16:
        return None
    # Two groups on each side, independent of actual variable incidence.
    blocks = {(g, h): [j for j, (i, v) in enumerate(incidences)
                       if i % 2 == g and v % 2 == h]
              for g in range(2) for h in range(2)}
    direct_x = [x for x in range(1 << n) if formula_value(direct, x)]
    moments = [sum((x & mask) == mask for x in direct_x) for mask in range(1 << n)]
    direct_variables = {abs(lit)-1 for c in direct for lit in c}
    # Check the new boundary-port rule explicitly for every demanded monomial.
    boundary_checks = 0
    for demand in range(1 << n):
        val = 0
        free = [v for v in range(n) if v not in direct_variables]
        used = sorted(direct_variables)
        for bm in range(1 << len(used)):
            x = sum(1 << v for j, v in enumerate(used) if bm >> j & 1)
            if not formula_value(direct, x):
                continue
            coefficient = 1
            for v in used:
                if demand >> v & 1 and not x >> v & 1:
                    coefficient = 0
            coefficient *= 1 << sum(not (demand >> v & 1) for v in free)
            val += coefficient
        assert val == moments[demand]
        boundary_checks += 1

    total = [0]*ell
    codes = set()
    nonzero_terms = 0
    wire_roundtrips = 0
    signed_coefficients = 0
    for mask in range(1 << len(incidences)):
        arr = []
        indices = []
        for block in blocks.values():
            chosen = tuple(j for j in block if mask >> j & 1)
            index = rank_subset(chosen, block)
            decoded = decode_subset(index, block, len(chosen))
            assert decoded == chosen
            arr.append(len(chosen))
            indices.append(index)
            wire_roundtrips += 1
        code = (tuple(arr), tuple(indices))
        assert code not in codes
        codes.add(code)
        product = [1]+[0]*(ell-1)
        demanded = 0
        offset = 0
        for scope, coeff in local:
            choice = (mask >> offset) & ((1 << len(scope))-1)
            for j, v in enumerate(scope):
                if choice >> j & 1:
                    demanded |= 1 << v
            row = coeff[choice]
            signed_coefficients += sum(x > modulus//2 for x in row)
            product = ring_mul(product, row, modulus)
            offset += len(scope)
        if any(product):
            nonzero_terms += 1
        moment = moments[demanded]
        total = [(x+moment*y) % modulus for x, y in zip(total, product)]
    result = sum(total) % modulus
    expected = sum(formula_value(binary, x) and formula_value(direct, x)
                   for x in range(1 << n))
    eq_expected = sum(all(sum((mon & x) == mon for mon in p) % 2 == 0
                          for p in equations) and formula_value(direct, x)
                      for x in range(1 << n))
    assert result == expected == eq_expected
    return {"n":n, "binary_clauses":binary, "direct_clauses":direct,
            "manufactured_rows":rows, "binary_count":binary_count,
            "equation_count":len(equations), "test_incidences":len(incidences),
            "direct_incidences":sum(map(len, direct)), "count":result,
            "incidence_subsets":len(codes), "nonzero_terms":nonzero_terms,
            "wire_index_roundtrips":wire_roundtrips,
            "boundary_moment_checks":boundary_checks,
            "modular_negative_coefficient_occurrences":signed_coefficients}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="hybrid_contraction_results.json")
    args = parser.parse_args()
    rng = random.Random(27102026)
    fixtures = []
    # Include constants, empty direct lists, complementary and repeated literals,
    # dense binary restrictions, and wide direct clauses with overlapping inputs.
    fixed = [(2, [[1,2],[-1,-2]], [[1,-2]]),
             (3, [[1,2],[-2,3],[-3,-1]], [[1,2,3]]),
             (3, [], [[1,2,3],[-1,-2,-3]]),
             (2, [[1],[-1]], [[1,2]]),
             (3, [[1,-1],[2,2]], []),
             (3, [[1,2]], [[]]),
             (6, [[1,2],[3,4],[5,6]], [[1,3,5],[-2,-4,-6]]),
             (6, [[1,2],[-2,3],[-3,4],[-4,5],[-5,6],[-6,-1]],
                 [[1,2,3,4,5,6]]),
             (4, [[1,2],[2,3],[3,4],[-1,-4]], [[1,-2,3,-4]])]
    for n, binary, direct in fixed:
        fixtures.append(run_fixture(n, binary, direct))
    for n in range(1,7):
        accepted = 0
        while accepted < 8:
            binary = [[rng.choice((-1,1))*rng.randint(1,n)
                       for _ in range(rng.randint(1,2))]
                      for _ in range(rng.randint(1,4 if n<=5 else 2))]
            direct = [[rng.choice((-1,1))*v for v in rng.sample(range(1,n+1),
                       rng.randint(1,n))] for _ in range(rng.randint(0,3))]
            outcome = run_fixture(n, binary, direct)
            if outcome is not None:
                fixtures.append(outcome)
                accepted += 1
    assert all(x is not None for x in fixtures)
    summary = {"status":"all exact assertions passed", "fixtures":len(fixtures),
               "scope":"finite algebraic representation checks; exhaustive counters and contractions",
               "incidence_subsets":sum(f["incidence_subsets"] for f in fixtures),
               "wire_index_roundtrips":sum(f["wire_index_roundtrips"] for f in fixtures),
               "boundary_moment_checks":sum(f["boundary_moment_checks"] for f in fixtures),
               "modular_negative_coefficient_occurrences":sum(f["modular_negative_coefficient_occurrences"] for f in fixtures),
               "results":fixtures}
    Path(args.output).write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k != "results"}, indent=2))


if __name__ == "__main__":
    main()

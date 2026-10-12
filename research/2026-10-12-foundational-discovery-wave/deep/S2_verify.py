#!/usr/bin/env python3
"""Independent exact finite diagnostics for S2; no source-candidate sampler used.

Run: python3 research_wave_2026-10-12/deep/S2_verify.py
Only writes its adjacent S2_evidence.json. Finite checks are not theorem proofs.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from math import ceil
from pathlib import Path
import json
import random
import time


def rank(rows):
    basis = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    return len(basis)


def canonical_basis(rows):
    basis = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                for q in list(basis):
                    if (basis[q] >> p) & 1:
                        basis[q] ^= x
                basis[p] = x
                break
    for p in sorted(basis):
        for q in basis:
            if q > p and (basis[q] >> p) & 1:
                basis[q] ^= basis[p]
    return tuple(basis[p] for p in sorted(basis, reverse=True))


def in_span(x, rows):
    return rank([*rows, x]) == rank(rows)


def inconsistent(a, b, selected):
    r = rank(a[i] for i in selected)
    d = max((v.bit_length() for v in a), default=0)
    return rank(a[i] | (b[i] << d) for i in selected) > r


def witnesses(a, b):
    result = []
    for c in range(1 << len(a)):
        v = s = 0
        for i in range(len(a)):
            if c >> i & 1:
                v ^= a[i]
                s ^= b[i]
        if v == 0 and s == 1:
            result.append(c)
    return result


def dependency_blocks(a):
    """Fundamental-circuit partition, computed without enumerating dependencies."""
    parent = list(range(len(a)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    basis = {}
    for i, original in enumerate(a):
        value, combination = original, 0
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                row, mask = basis[pivot]
                value ^= row
                combination ^= mask
            else:
                basis[pivot] = value, combination ^ (1 << i)
                break
        if value == 0:
            for j in range(len(a)):
                if combination >> j & 1:
                    parent[find(j)] = find(i)
    groups = {}
    for i in range(len(a)):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def mass(mask, p):
    q = F(1)
    for i, z in enumerate(p):
        q *= z if mask >> i & 1 else 1 - z
    return q


def exact_diagnostic(a, b, p):
    ws = witnesses(a, b)
    U = Q = EY = EY2 = F(0)
    for c in ws:
        w = F(1)
        for i, z in enumerate(p):
            if c >> i & 1:
                w *= z
        Q += w
    for mask in range(1 << len(a)):
        selected = [i for i in range(len(a)) if mask >> i & 1]
        N = sum((c & mask) == c for c in ws)
        inc = inconsistent(a, b, selected)
        assert bool(N) == inc
        if N:
            assert N == 1 << (len(selected) - rank(a[i] for i in selected) - 1)
            u = mass(mask, p)
            U += u
            if Q:
                EY += u / Q
                EY2 += u / (Q * N)
    P = F(1)
    for z in p:
        P *= 1 + z
    assert Q <= P * U
    if Q:
        assert EY == U / Q
        relative_variance = (EY2 - EY * EY) / (EY * EY)
        assert relative_variance <= min(F(len(ws) - 1), P - 1)
    else:
        relative_variance = F(0)
    return U, Q, P, relative_variance


def nullspace(rows, n):
    rows = list(rows)
    pivots = []
    rr = 0
    for j in range(n):
        found = next((i for i in range(rr, len(rows)) if rows[i] >> j & 1), None)
        if found is None:
            continue
        rows[rr], rows[found] = rows[found], rows[rr]
        for i in range(len(rows)):
            if i != rr and rows[i] >> j & 1:
                rows[i] ^= rows[rr]
        pivots.append(j)
        rr += 1
    result = []
    for j in range(n):
        if j not in pivots:
            v = 1 << j
            for i, pivot in enumerate(pivots):
                if rows[i] >> j & 1:
                    v |= 1 << pivot
            result.append(v)
    return result


def connected(n, edges, removed, s=0, t=1):
    seen = {s}
    todo = [s]
    while todo:
        u = todo.pop()
        for i, (v, w) in enumerate(edges):
            if removed >> i & 1:
                continue
            if v == u and w not in seen:
                seen.add(w)
                todo.append(w)
            if w == u and v not in seen:
                seen.add(v)
                todo.append(v)
    return t in seen


def cographic_affine(n, edges):
    all_edges = [*edges, (0, 1)]
    incidence = [0] * n
    for i, (u, v) in enumerate(all_edges):
        incidence[u] ^= 1 << i
        incidence[v] ^= 1 << i
    cycles = nullspace(incidence, len(all_edges))
    columns = [sum(((row >> i) & 1) << j for j, row in enumerate(cycles))
               for i in range(len(all_edges))]
    t = columns[-1]
    assert t
    r = len(cycles)
    pivot = (t & -t).bit_length() - 1

    def swap(v):
        if ((v >> pivot) ^ (v >> (r - 1))) & 1:
            v ^= (1 << pivot) | (1 << (r - 1))
        return v

    t = swap(t)
    t_low = t ^ (1 << (r - 1))
    transformed = []
    for v in columns:
        v = swap(v)
        if v >> (r - 1) & 1:
            v ^= t_low
        transformed.append(v)
    assert transformed[-1] == 1 << (r - 1)
    a = [v & ((1 << (r - 1)) - 1) for v in transformed[:-1]]
    b = [v >> (r - 1) for v in transformed[:-1]]
    return a, b, columns


def prefix_compile(a, b, d):
    """Returns deterministic helpers, independent final rows, variable count."""
    helpers = []
    finals = []
    for v, rhs in zip(a, b):
        previous = d
        d += 1
        helpers.append((1 << previous, 0))
        for x in range(v.bit_length()):
            if v >> x & 1:
                current = d
                d += 1
                helpers.append(((1 << current) | (1 << previous) | (1 << x), 0))
                previous = current
        finals.append((1 << previous, rhs))
    return helpers, finals, d


def fair_helper_compile(helpers, finals, d, repeats=1):
    rows = list(finals)
    for v, rhs in helpers:
        support = [i for i in range(v.bit_length()) if v >> i & 1]
        assert 1 <= len(support) <= 3
        left, right = support[:min(2, len(support))], support[min(2, len(support)):]
        for _ in range(repeats):
            z = 1 << d
            d += 1
            rows.append((z | sum(1 << i for i in left), 0))
            rows.append((z | sum(1 << i for i in right), rhs))
    assert len(rows) == len(set(rows))
    assert all(v.bit_count() <= 3 for v, rhs in rows)
    return rows, d


def dp_partition(a, b, p, d):
    table = [[F(0)] * (1 << (d + 1))]
    table[0][0] = F(1)
    for v, rhs, z in zip(a, b, p):
        u = v | (rhs << d)
        previous = table[-1]
        table.append([previous[s] + z * previous[s ^ u]
                      for s in range(1 << (d + 1))])
    return table, table[-1][1 << d]


def sample_fraction(p, rng, cap=128):
    """Exact rational coin with a fixed rejection cap; failures are explicit."""
    if p <= 0:
        return False
    if p >= 1:
        return True
    bits = (p.denominator - 1).bit_length()
    for _ in range(cap):
        z = rng.getrandbits(bits)
        if z < p.denominator:
            return z < p.numerator
    raise RuntimeError("Rational-coin cap reached; this is a budgeted failure event.")


def sample_dp_witness(a, b, p, d, table, rng, cap):
    syndrome = 1 << d
    witness = []
    for j in reversed(range(len(a))):
        u = a[j] | (b[j] << d)
        total = table[j + 1][syndrome]
        included = p[j] * table[j][syndrome ^ u]
        if sample_fraction(included / total, rng, cap):
            witness.append(j)
            syndrome ^= u
    assert syndrome == 0
    return set(witness)


def estimate_dp(a, b, p, d, samples, seed):
    table, Q = dp_partition(a, b, p, d)
    rng = random.Random(seed)
    delta_for_coin_caps = F(1, 100)
    upper_coin_calls = 2 * len(a) * samples
    bound = ceil(F(2 * upper_coin_calls, 1) / delta_for_coin_caps)
    cap = max(1, (bound - 1).bit_length())
    value = F(0)
    max_selected = 0
    for _ in range(samples):
        selected = sample_dp_witness(a, b, p, d, table, rng, cap)
        for j, z in enumerate(p):
            if j not in selected and sample_fraction(z, rng, cap):
                selected.add(j)
        h = len(selected) - rank(a[j] for j in selected)
        assert h >= 1 and inconsistent(a, b, selected)
        value += F(1, 1 << (h - 1))
        max_selected = max(max_selected, len(selected))
    return Q * value / samples, Q, max_selected


def exact_span_dp(a, b, p, d):
    table = {(): F(1)}
    max_states = 1
    for v, rhs, z in zip(a, b, p):
        u = v | (rhs << d)
        new = {}
        for basis, w in table.items():
            new[basis] = new.get(basis, F(0)) + w * (1 - z)
            added = canonical_basis([*basis, u])
            new[added] = new.get(added, F(0)) + w * z
        table = new
        max_states = max(max_states, len(table))
    target = 1 << d
    return sum(w for basis, w in table.items() if in_span(target, basis)), max_states


def qstr(x):
    return str(x.numerator) + "/" + str(x.denominator)


def main():
    started = time.monotonic()
    evidence = {"status": "finite diagnostics, not proof certification", "seed": 71520261012}
    count = 0
    worst = (F(0), None)
    for m in range(1, 5):
        for encoded in product(range(8), repeat=m):
            a = [z & 3 for z in encoded]
            b = [z >> 2 for z in encoded]
            p = [F(1, 2)] * m
            U, Q, P, variance = exact_diagnostic(a, b, p)
            count += 1
            if U and Q / U / P > worst[0]:
                worst = (Q / U / P, {"a": a, "b": b, "U": qstr(U), "Q": qstr(Q), "P": qstr(P)})
    rng = random.Random(71520261012)
    for _ in range(200):
        m = rng.randrange(1, 9)
        a = [rng.randrange(16) for _ in range(m)]
        b = [rng.randrange(2) for _ in range(m)]
        p = [rng.choice([F(1, 1000), F(1, 5), F(1, 2), F(4, 5), F(999, 1000)]) for _ in range(m)]
        exact_diagnostic(a, b, p)
        count += 1
    evidence["certificate_identity_and_mass_bound"] = {"instances": count, "worst_Q_over_U_P": qstr(worst[0]), "worst_example": worst[1]}

    block_instances = 0
    for _ in range(100):
        m = rng.randrange(1, 9)
        a = [rng.randrange(8) for _ in range(m)]
        b = [rng.randrange(2) for _ in range(m)]
        p = [rng.choice([F(1, 7), F(1, 2), F(6, 7)]) for _ in range(m)]
        U = exact_diagnostic(a, b, p)[0]
        survival = F(1)
        for block in dependency_blocks(a):
            local_U = exact_diagnostic([a[i] for i in block], [b[i] for i in block], [p[i] for i in block])[0]
            survival *= 1 - local_U
        assert 1 - survival == U
        block_instances += 1
    union_checks = 0
    for _ in range(1000):
        u = [F(rng.randrange(0, 101), 100) for _ in range(rng.randrange(1, 21))]
        eps = F(rng.randrange(1, 101), 100)
        approx = [min(F(1), max(F(0), z * (1 + eps * F(rng.randrange(-100, 101), 100)))) for z in u]
        U = E = F(1)
        for z, q in zip(u, approx):
            U *= 1 - z
            E *= 1 - q
        U, E = 1 - U, 1 - E
        assert (1 - eps) * U <= E <= (1 + eps) * U
        union_checks += 1
    evidence["dependency_blocks_and_union_composition"] = {"exact_block_instances": block_instances, "no_error_accumulation_checks": union_checks}

    graphs = selections = 0
    pairs = [(u, v) for u in range(4) for v in range(u + 1, 4)]
    graph_inputs = [(4, [pairs[i] for i in range(6) if mask >> i & 1]) for mask in range(1 << 6)]
    graph_inputs += [(3, [(0, 1), (0, 1), (1, 2), (2, 2)]), (4, [(0, 2), (2, 1), (3, 3)])]
    for n, edges in graph_inputs:
        if not connected(n, edges, 0):
            continue
        a, b, columns = cographic_affine(n, edges)
        for S in range(1 << len(edges)):
            selected = [i for i in range(len(edges)) if S >> i & 1]
            lhs = not connected(n, edges, S)
            assert lhs == in_span(columns[-1], [columns[i] for i in selected])
            assert lhs == inconsistent(a, b, selected)
            selections += 1
        graphs += 1
    evidence["cographic_target_affine_reduction"] = {"graphs": graphs, "edge_selections": selections, "includes": ["loops", "parallel edges", "remote components"]}

    local_checks = 0
    for arity in (1, 2, 3):
        for rhs in (0, 1):
            helpers = [((1 << arity) - 1, rhs)]
            rows, d = fair_helper_compile(helpers, [], arity)
            for present in range(4):
                for assignment in range(1 << arity):
                    extends = any(all((((assignment | (z << arity)) & v).bit_count() & 1) == b
                                      for i, (v, b) in enumerate(rows) if present >> i & 1)
                                  for z in (0, 1))
                    imposed = present == 3
                    expected = (not imposed) or ((assignment.bit_count() & 1) == rhs)
                    assert extends == expected
                    local_checks += 1
    helpers, finals, d = prefix_compile([1, 1], [0, 1], 1)
    rows, d = fair_helper_compile(helpers, finals, d)
    a, b = map(list, zip(*rows))
    U_new = sum(mass(S, [F(1, 2)] * len(rows)) for S in range(1 << len(rows))
                if inconsistent(a, b, [i for i in range(len(rows)) if S >> i & 1]))
    U_old = F(1, 4)
    q = F(1, 4)
    assert q ** len(helpers) * U_old <= U_new <= U_old
    evidence["distinct_fair_helper_gadget"] = {"local_assignment_checks": local_checks, "compiled_rows": len(rows), "D": len(helpers), "q": qstr(q), "original_U": qstr(U_old), "compiled_U": qstr(U_new), "all_rows_distinct": True, "max_arity": max(v.bit_count() for v, _ in rows)}

    # One connected dependency block: all nonzero rank-five vectors plus a duplicate.
    # The one exceptional RHS creates an extremely rare contradictory pair.
    d = 5
    a = list(range(1, 1 << d)) + [1]
    b = [0] * 31 + [1]
    p = [F(1, 1 << 80)] * len(a)
    exact_U, exact_states = exact_span_dp(a, b, p, d)
    estimate, Q, max_selected = estimate_dp(a, b, p, d, 400, 71520261012)
    P = F(1)
    for z in p:
        P *= 1 + z
    assert Q <= P * exact_U
    assert abs(estimate / exact_U - 1) < F(1, 5)
    evidence["rare_low_rank_high_nullity_instance"] = {
        "m": len(a), "rank": rank(a), "nullity": len(a) - rank(a),
        "all_p": "2^-80", "contradictory_witness_count": 1 << (len(a) - rank(a) - 1),
        "syndrome_DP_states_per_layer": 1 << (d + 1), "samples": 400,
        "max_selected_in_diagnostic": max_selected, "U_decimal": float(exact_U),
        "Q_over_U": float(Q / exact_U), "estimate_over_U": float(estimate / exact_U),
        "exact_subspace_DP_max_states": exact_states,
        "matched_raw_MC_expected_draws_per_failure": float(1 / exact_U),
        "exact_U": qstr(exact_U), "exact_Q": qstr(Q),
    }
    evidence["elapsed_seconds"] = time.monotonic() - started
    output = Path(__file__).with_name("S2_evidence.json")
    output.write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps({k: v for k, v in evidence.items() if k != "rare_low_rank_high_nullity_instance"}, indent=2))
    print(json.dumps({k: v for k, v in evidence["rare_low_rank_high_nullity_instance"].items() if not k.startswith("exact_")}, indent=2))
    print("Evidence: " + str(output.resolve()))


if __name__ == "__main__":
    main()

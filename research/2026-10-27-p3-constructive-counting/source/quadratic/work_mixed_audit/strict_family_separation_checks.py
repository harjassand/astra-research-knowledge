#!/usr/bin/env python3
"""Exact finite certificates for mixed acquired-core family separation.

This executes support-cover, rank, distance, cut and finite rigidity checks.
It does not execute the asymptotic phase-counting engine.  No random graph in
the large certificate is asserted to be an asymptotic expander family.
"""

import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

from mixed_adversarial_checks import (
    alt, alt_check, bits, edge_weight, make_a, quadratic, rank, submatrix,
    transpose,
)


def symmetric(n, mask):
    rows = [0] * n
    for bit, (i, j) in enumerate(itertools.combinations_with_replacement(range(n), 2)):
        if mask >> bit & 1:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return rows


def offdiag_weight(a):
    return sum((row & ~(1 << i)).bit_count() for i, row in enumerate(a)) // 2


def support_cover(a, tau):
    """Construct the claimed cover; arbitrary diagonal is allowed."""
    n = len(a)
    assert tau >= 1
    full = (1 << n) - 1
    h = sum(1 << i for i, row in enumerate(a)
            if (row & ~(1 << i)).bit_count() >= tau)
    c = full ^ h
    pivots = {}
    basis_rows = []
    j = 0
    for i in bits(c):
        original = a[i] & c
        reduced = original
        while reduced:
            lead = reduced.bit_length() - 1
            if lead in pivots:
                reduced ^= pivots[lead]
            else:
                pivots[lead] = reduced
                basis_rows.append(i)
                j |= original
                break
    removed = h | j
    remaining = full ^ removed
    assert all(not (a[i] & remaining) for i in bits(remaining))
    q = rank(a)
    m = offdiag_weight(a)
    bound = 2 * m // tau + q * tau
    assert removed.bit_count() <= bound
    alternating = all(not (row >> i & 1) for i, row in enumerate(a))
    if alternating:
        assert removed.bit_count() <= 2 * m // tau + q * (tau - 1)
    return dict(removed=list(bits(removed)), high=list(bits(h)),
                basis_rows=basis_rows, rank=q, offdiag_edges=m,
                tau=tau, symmetric_bound=bound)


def cover_exhaustion():
    counts = {}
    total = 0
    for n in range(1, 6):
        calls = 0
        for mask in range(1 << (n * (n + 1) // 2)):
            a = symmetric(n, mask)
            for tau in range(1, n + 1):
                support_cover(a, tau)
                calls += 1
        counts[str(n)] = dict(symmetric_matrices=1 << (n * (n + 1) // 2),
                              threshold_checks=calls)
        total += calls
    # A diagonal matrix forces the additive rank term when M=0.
    diagonal = [1 << i if i in (0, 3, 7) else 0 for i in range(9)]
    diag_case = support_cover(diagonal, 1)
    assert len(diag_case['removed']) == 3 == diag_case['rank']
    return dict(exhaustive_by_n=counts, threshold_checks=total,
                diagonal_only_case=diag_case)


def codewords(feature_rows, r):
    columns = transpose(feature_rows, r)
    word = 0
    yield word
    for t in range(1, 1 << r):
        word ^= columns[(t & -t).bit_length() - 1]
        yield word


def code_distance(feature_rows, r):
    return min(word.bit_count() for word in list(codewords(feature_rows, r))[1:])


def random_code(n, r, rng):
    attempts = 0
    while True:
        attempts += 1
        u = [rng.randrange(1 << r) for _ in range(n)]
        distance = code_distance(u, r)
        a = make_a(u, r)
        if 4 * distance >= n and 4 * edge_weight(a) >= n * (n - 1) // 2:
            assert rank(u) == r
            return u, a, distance, attempts


def cube_graph():
    return alt(8, [(i, i ^ (1 << j)) for i in range(8) for j in range(3)
                   if i < (i ^ (1 << j))])


def petersen_graph():
    edges = [(i, (i + 1) % 5) for i in range(5)]
    edges += [(i, i + 5) for i in range(5)]
    edges += [(i + 5, (i + 2) % 5 + 5) for i in range(5)]
    return alt(10, edges)


def prism_graph(length):
    edges = [(j * length + i, j * length + (i + 1) % length)
             for j in range(2) for i in range(length)]
    edges += [(i, i + length) for i in range(length)]
    return alt(2 * length, edges)


def greedy_matching(s, x, y, block_of=None):
    """Induced cross matching, optionally using each cubic block at most once."""
    edges = [(i, j) for i in x for j in y if s[i] >> j & 1
             and (block_of is None or block_of[i] != block_of[j])]
    answer = []
    while edges:
        u, v = edges[0]
        answer.append((u, v))
        edges = [(i, j) for i, j in edges
                 if not (s[i] >> v & 1) and not (s[u] >> j & 1)
                 and (block_of is None or
                      (block_of[i] not in (block_of[u], block_of[v]) and
                       block_of[j] not in (block_of[u], block_of[v])))]
    selected = submatrix(s, [u for u, _ in answer], [v for _, v in answer])
    assert selected == [1 << i for i in range(len(answer))]
    if block_of is not None:
        assert len({block_of[v] for edge in answer for v in edge}) == 2 * len(answer)
    return answer


def rank_mod_prime(a, p=3):
    if not a:
        return 0
    a = [[x % p for x in row] for row in a]
    out = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(out, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[out], a[pivot] = a[pivot], a[out]
        factor = pow(a[out][j], -1, p)
        a[out] = [(factor * value) % p for value in a[out]]
        for i in range(out + 1, len(a)):
            factor = a[i][j]
            if factor:
                a[i] = [(value - factor * base) % p for value, base in zip(a[i], a[out])]
        out += 1
        if out == len(a):
            break
    return out


def small_cuts(rng):
    records = []
    phase_submatrix_checks = 0
    cases = [('cube', cube_graph(), 2), ('Petersen', petersen_graph(), 2),
             ('hexagonal prism', prism_graph(6), 2)]
    for name, s, r in cases:
        n = len(s)
        u, a, distance, attempts = random_code(n, r, rng)
        b = [x ^ y for x, y in zip(a, s)]
        degree = max(row.bit_count() for row in s)
        expansion = None
        min_s_rank = n
        min_b_rank = n
        balanced_cuts = 0
        min_phase_lower = None
        # The prism is bipartite; its two sides contain two independent triples.
        if n == 12:
            side0 = [i for i in range(6) if i % 2 == 0] + [i + 6 for i in range(6) if i % 2 == 1]
            side1 = [i for i in range(6) if i % 2 == 1] + [i + 6 for i in range(6) if i % 2 == 0]
            blocks = [side0[:3], side0[3:], side1[:3], side1[3:]]
            block_of = {v: j for j, block in enumerate(blocks) for v in block}
            assert all(not (s[i] >> j & 1) for block in blocks
                       for i, j in itertools.combinations(block, 2))
        else:
            blocks = None
            block_of = None
        for mask in range(1, 1 << n):
            size = mask.bit_count()
            if size > n // 2:
                continue
            x = list(bits(mask))
            y = [i for i in range(n) if not (mask >> i & 1)]
            sc = submatrix(s, x, y)
            edges = sum(row.bit_count() for row in sc)
            ratio = Fraction(edges, size)
            expansion = ratio if expansion is None else min(expansion, ratio)
            if 3 * size < n:
                continue
            balanced_cuts += 1
            sr = rank(sc)
            ar = rank(submatrix(a, x, y))
            br = rank(submatrix(b, x, y))
            assert ar <= r
            assert br >= sr - r
            matching = greedy_matching(s, x, y)
            assert 2 * degree * degree * len(matching) >= edges
            assert sr >= len(matching)
            min_s_rank = min(min_s_rank, sr)
            min_b_rank = min(min_b_rank, br)
            if blocks is not None:
                matching = greedy_matching(s, x, y, block_of)
                assert (2 * degree * degree + 6 * degree) * len(matching) >= edges
                left = [u0 for u0, _ in matching]
                right = [v0 for _, v0 in matching]
                t = len(matching)
                cross_rank = rank(submatrix(b, left, right))
                assert cross_rank >= t - r
                full = submatrix(b, left + right, left + right)
                phase = [[(-1) ** quadratic(full, xx | (yy << t))
                          for yy in range(1 << t)] for xx in range(1 << t)]
                measured_rank = rank_mod_prime(phase)
                assert measured_rank == 1 << cross_rank
                phase_submatrix_checks += 1
                min_phase_lower = measured_rank if min_phase_lower is None else min(min_phase_lower, measured_rank)
        assert expansion > 0
        records.append(dict(name=name, n=n, core_rank=r, code_distance=distance,
                            code_rows=u, code_sampling_attempts=attempts,
                            graph_rows=s, graph_degree=degree, graph_edges=edge_weight(s),
                            exact_edge_expansion=str(expansion), a_edges=edge_weight(a),
                            b_edges=edge_weight(b), b_rank=rank(b),
                            balanced_cuts_checked=balanced_cuts,
                            min_balanced_s_cutrank=min_s_rank,
                            min_balanced_b_cutrank=min_b_rank,
                            cubic_blocks=blocks,
                            minimum_certified_full_phase_flattening_rank=min_phase_lower))
    return dict(fixtures=records, full_phase_submatrix_checks=phase_submatrix_checks,
                note='Each small graph is exhaustively checked. These finite graphs do not establish an asymptotic expander family.')


def symmetric_rank_one_exhaustion():
    # Every symmetric rank-one matrix over F2 is vv^T, so this enumerates
    # all symmetric competitors of rank < 2, including arbitrary diagonals.
    n = 12
    u = [0, 1, 2, 3] * 3
    a = make_a(u, 2)
    rows = []
    for name, s in [('uncorrupted', [0] * n),
                    ('matching-corrupted', alt(n, [(i, i + 1) for i in range(0, n, 2)]))]:
        b = [x ^ y for x, y in zip(a, s)]
        best = n * n
        best_v = None
        for v in range(1 << n):
            alternative = [v if v >> i & 1 else 0 for i in range(n)]
            assert rank(alternative) <= 1
            errors = offdiag_weight([x ^ y for x, y in zip(b, alternative)])
            if errors < best:
                best = errors
                best_v = v
        rows.append(dict(name=name, n=n, core_rank=2, code_distance=code_distance(u, 2),
                         sparse_edges=edge_weight(s), symmetric_competitors=1 << n,
                         minimum_offdiag_errors_rank_below_two=best,
                         minimizer_vector=best_v))
    return rows


def large_rigidity_certificate(rng):
    n = 4098
    r = 6
    u, a, distance, attempts = random_code(n, r, rng)
    edges = set()
    for _ in range(4):
        order = list(range(n))
        rng.shuffle(order)
        for i, j in zip(order, order[1:] + order[:1]):
            edges.add((min(i, j), max(i, j)))
    s = alt(n, sorted(edges))
    b = [x ^ y for x, y in zip(a, s)]
    m = edge_weight(s)
    competitor_budget = 4 * n
    # Symmetric competitor rank < r implies rank(A+D') <= 2r-1.
    q_bound = 2 * r - 1
    difference_budget = m + competitor_budget
    best_bound, tau = min((2 * difference_budget // t + q_bound * t, t)
                          for t in range(1, n + 1))
    assert best_bound < distance
    assert m <= competitor_budget
    assert alt_check(a) and alt_check(s) and alt_check(b)
    assert rank(u) == r
    assert 4 * edge_weight(a) >= n * (n - 1) // 2
    return dict(n=n, core_rank=r, feature_rows=u, code_distance=distance,
                sampling_attempts=attempts, sparse_edges=sorted(edges),
                sparse_edge_count=m, sparse_max_degree=max(row.bit_count() for row in s),
                core_edge_count=edge_weight(a), observed_edge_count=edge_weight(b),
                symmetric_competitor_edge_budget=competitor_budget,
                difference_rank_bound=q_bound, difference_edge_budget=difference_budget,
                optimal_integer_threshold=tau, support_cover_upper_bound=best_bound,
                strict_margin=distance - best_bound,
                certified_statement='No symmetric core of rank below 6, with arbitrary diagonal, has this observed off-diagonal matrix within 4n unordered edge changes.',
                method='Exact codeword distances and support-cover inequality; not enumeration of all competing matrices.',
                limitation='The union of random cycles here is not certified as an expander. It is used only for the sparse-corruption/rank-rigidity certificate.')


def main():
    rng = random.Random(20261106)
    result = dict(
        support_cover=cover_exhaustion(),
        cuts=small_cuts(rng),
        small_symmetric_competitor_exhaustion=symmetric_rank_one_exhaustion(),
        large_symmetric_rigidity=large_rigidity_certificate(rng),
        all_assertions_passed=True,
        asymptotic_phase_engine_executed=False,
    )
    output = Path(__file__).with_name('strict_family_separation_results.json')
    output.write_text(json.dumps(result, indent=2) + '\n')
    concise = dict(support_cover_threshold_checks=result['support_cover']['threshold_checks'],
                   balanced_cut_checks=sum(x['balanced_cuts_checked'] for x in result['cuts']['fixtures']),
                   full_phase_submatrix_checks=result['cuts']['full_phase_submatrix_checks'],
                   rank_one_competitors_checked=sum(x['symmetric_competitors'] for x in result['small_symmetric_competitor_exhaustion']),
                   large_certificate={k: result['large_symmetric_rigidity'][k] for k in
                                      ['n', 'core_rank', 'code_distance', 'sparse_edge_count',
                                       'core_edge_count', 'observed_edge_count', 'symmetric_competitor_edge_budget',
                                       'optimal_integer_threshold', 'support_cover_upper_bound', 'strict_margin']},
                   all_assertions_passed=True,
                   asymptotic_phase_engine_executed=False)
    print(json.dumps(concise, indent=2))


if __name__ == '__main__':
    main()

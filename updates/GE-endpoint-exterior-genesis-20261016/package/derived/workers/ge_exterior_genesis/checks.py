#!/usr/bin/env python3
"""Original exact diagnostics for the exterior/Pfaffian receiving theorem.

Only Python's standard library is used. No supplied or acquired executable is
imported. The checks are finite diagnostics; PROOF.md contains the arguments.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import math
import platform
import time
from sampler import sample_integer_weights, sample_sorted_endpoints

HERE = Path(__file__).resolve().parent


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p) if p else (0,)


def padd(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def pneg(a):
    return tuple(-x for x in a)


def psub(a, b):
    return padd(a, pneg(b))


def pmul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def pdivexact(a, b):
    assert b != (0,)
    a = list(trim(a))
    if a == [0]:
        return (0,)
    assert len(a) >= len(b)
    q = [0] * (len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        shift = len(a) - len(b)
        z, rem = divmod(a[-1], b[-1])
        assert rem == 0, "nonintegral polynomial quotient"
        q[shift] += z
        for j, y in enumerate(b):
            a[shift + j] -= z * y
        a = list(trim(a))
    assert a == [0], "inexact polynomial division"
    return trim(q)


def pfaffian_bareiss(a):
    """Fraction-free skew elimination over Z[z], including zero-pivot swaps."""
    a = [[trim(x) for x in row] for row in a]
    n = len(a)
    assert n % 2 == 0
    if n == 0:
        return (1,)
    prev, sign = (1,), 1
    for h in range(0, n - 2, 2):
        j = next((j for j in range(h + 1, n) if a[h][j] != (0,)), None)
        if j is None:
            return (0,)
        if j != h + 1:
            a[h + 1], a[j] = a[j], a[h + 1]
            for row in a:
                row[h + 1], row[j] = row[j], row[h + 1]
            sign = -sign
        pivot = a[h][h + 1]
        for i in range(h + 2, n):
            for j in range(i + 1, n):
                num = padd(psub(pmul(pivot, a[i][j]),
                                 pmul(a[h][i], a[h + 1][j])),
                           pmul(a[h][j], a[h + 1][i]))
                a[i][j] = pdivexact(num, prev)
                a[j][i] = pneg(a[i][j])
        prev = pivot
    return tuple(sign * x for x in a[-2][-1])


def pfaffian_recursive(a):
    if not a:
        return (1,)
    out = (0,)
    for j in range(1, len(a)):
        ids = [i for i in range(1, len(a)) if i != j]
        term = pmul(a[0][j], pfaffian_recursive(
            [[a[i][l] for l in ids] for i in ids]))
        out = padd(out, term if j % 2 else pneg(term))
    return out


def pdet(a):
    k = len(a)
    out = (0,)
    for pi in permutations(range(k)):
        v = (1,)
        inv = sum(pi[i] > pi[j] for i in range(k) for j in range(i + 1, k))
        for i, j in enumerate(pi):
            v = pmul(v, a[i][j])
        out = padd(out, pneg(v) if inv % 2 else v)
    return out


def count_pf(rows, bin_sites):
    """Integer numerator of sum_Y det(rows_Y) z**|Y intersection B|."""
    k, n = len(rows), len(rows[0])
    size = k + k % 2
    a = [[(0,) for _ in range(size)] for _ in range(size)]
    prefix = [(0,) for _ in range(k)]
    for y in range(n):
        col = [(0, rows[i][y]) if y in bin_sites else (rows[i][y],)
               for i in range(k)]
        for i in range(k):
            for j in range(i + 1, k):
                a[i][j] = padd(a[i][j], psub(pmul(prefix[i], col[j]),
                                            pmul(col[i], prefix[j])))
                a[j][i] = pneg(a[i][j])
        prefix = [padd(prefix[i], col[i]) for i in range(k)]
    if k % 2:
        for i in range(k):
            a[i][k] = prefix[i]
            a[k][i] = pneg(prefix[i])
    return pfaffian_bareiss(a), a


def count_minors(rows, bin_sites):
    k, n = len(rows), len(rows[0])
    out = [0] * (k + 1)
    for y in combinations(range(n), k):
        det = pdet([[(rows[i][j],) for j in y] for i in range(k)])[0]
        out[sum(j in bin_sites for j in y)] += det
    return trim(out)


class PrefixMass:
    """Fixed-prefix/suffix mass numerator; precompute suffix skew blocks."""
    def __init__(self, rows):
        self.rows = rows
        self.k, self.n = len(rows), len(rows[0])
        k, n = self.k, self.n
        self.sums = [[0] * k for _ in range(n + 1)]
        self.skew = [[[0] * k for _ in range(k)] for _ in range(n + 1)]
        for y in range(n - 1, -1, -1):
            col = [rows[i][y] for i in range(k)]
            later = self.sums[y + 1]
            self.sums[y] = [col[i] + later[i] for i in range(k)]
            self.skew[y] = [[self.skew[y + 1][i][j] + col[i] * later[j] - later[i] * col[j]
                             for j in range(k)] for i in range(k)]

    def __call__(self, fixed, lower):
        k, n, s = self.k, self.n, len(fixed)
        assert 0 <= lower <= n and s <= k
        assert tuple(sorted(set(fixed))) == tuple(fixed)
        assert not fixed or fixed[-1] < lower
        if n - lower < k - s:
            return 0
        ghost = (k - s) % 2
        r = k + ghost
        a = [[(0,) for _ in range(r + s)] for _ in range(r + s)]
        for i in range(k):
            for j in range(k):
                a[i][j] = (self.skew[lower][i][j],)
        if ghost:
            for i in range(k):
                a[i][k] = (self.sums[lower][i],)
                a[k][i] = (-self.sums[lower][i],)
        for q, y in enumerate(fixed):
            for i in range(k):
                a[i][r + q] = (self.rows[i][y],)
                a[r + q][i] = (-self.rows[i][y],)
        sign = (-1) ** (s * (s - 1) // 2)
        return sign * pfaffian_bareiss(a)[0]


def explicit_prefix_mass(rows, fixed, lower):
    k, n = len(rows), len(rows[0])
    return sum(pdet([[(rows[i][y],) for y in fixed + tail] for i in range(k)])[0]
               for tail in combinations(range(lower, n), k - len(fixed)))


def exact_tree_law(n, k, mass, attempt_cap=None):
    """Independent exact probability-tree enumeration, small diagnostics only."""
    out = {}

    def visit(prefix, lo, hi, probability):
        if probability == 0:
            return
        if lo == hi:
            prefix = prefix + (lo,)
            if len(prefix) == k:
                out[prefix] = out.get(prefix, F(0)) + probability
            else:
                visit(prefix, lo + 1, n - (k - len(prefix)), probability)
            return
        mid = (lo + hi) // 2
        left = max(0, mass(prefix, lo) - mass(prefix, mid + 1))
        right = max(0, mass(prefix, mid + 1) - mass(prefix, hi + 1))
        total = left + right
        qleft = F(left, total) if total else F(1)
        if total and attempt_cap is not None:
            width = (total - 1).bit_length()
            failure = (1 - F(total, 1 << width)) ** attempt_cap
            qleft = failure + (1 - failure) * qleft
        visit(prefix, lo, mid, probability * qleft)
        visit(prefix, mid + 1, hi, probability * (1 - qleft))

    visit((), 0, n - k, F(1))
    assert sum(out.values()) == 1
    return out


def laplacian(n, edges, potential=None, negative=()):
    a = [[0] * n for _ in range(n)]
    potential = [0] * n if potential is None else potential
    negative = {frozenset(e) for e in negative}
    for i, v in enumerate(potential):
        a[i][i] += v
    for x, y, rate in edges:
        assert rate >= 0 and x != y
        a[x][x] += rate
        a[y][y] += rate
        sign = -1 if frozenset((x, y)) in negative else 1
        a[x][y] -= sign * rate
        a[y][x] -= sign * rate
    return a


def cover_laplacian(n, edges, potential, negative):
    negative = {frozenset(e) for e in negative}
    lifts = []
    for x, y, rate in edges:
        for layer in (0, 1):
            other = 1 - layer if frozenset((x, y)) in negative else layer
            lifts.append((x + layer * n, y + other * n, rate))
    return laplacian(2 * n, lifts, list(potential) * 2)


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def compound(a, k):
    n = len(a)
    states = list(combinations(range(n), k))
    ix = {x: i for i, x in enumerate(states)}
    h = [[0] * len(states) for _ in states]
    for x in states:
        h[ix[x]][ix[x]] = sum(a[u][u] for u in x)
        for p, u in enumerate(x):
            for v in range(n):
                if v in x or a[u][v] == 0:
                    continue
                changed = list(x)
                changed[p] = v
                inv = sum(changed[i] > changed[j] for i in range(k)
                          for j in range(i + 1, k))
                y = tuple(sorted(changed))
                h[ix[x]][ix[y]] += (-1 if inv % 2 else 1) * a[u][v]
    return states, h


def killed(n, edges, k, potential=None):
    a = laplacian(n, edges, potential)
    states = list(combinations(range(n), k))
    ix = {x: i for i, x in enumerate(states)}
    h = [[0] * len(states) for _ in states]
    for x in states:
        h[ix[x]][ix[x]] = sum(a[u][u] for u in x)
        for u in x:
            for v in range(n):
                if v not in x:
                    y = tuple(sorted(set(x) - {u} | {v}))
                    h[ix[x]][ix[y]] += a[u][v]
    return states, h


def swap_wedge(n, k, u, v):
    states = list(combinations(range(n), k))
    ix = {x: i for i, x in enumerate(states)}
    p = [[0] * len(states) for _ in states]
    for x in states:
        y0 = [v if a == u else u if a == v else a for a in x]
        inv = sum(y0[i] > y0[j] for i in range(k) for j in range(i + 1, k))
        p[ix[x]][ix[tuple(sorted(y0))]] = (-1 if inv % 2 else 1)
    return [[(1 if i == j else 0) - p[i][j] for j in range(len(states))]
            for i in range(len(states))]


def heat_rows(c, starts, m, p):
    n, steps, scale = len(c), 1 << m, 1 << p
    lam = max(c[i][i] for i in range(n))
    assert steps >= lam and p >= m
    mat = [[(scale if i == j else 0) - c[i][j] * (scale // steps)
            for j in range(n)] for i in range(n)]
    assert all(x >= 0 for row in mat for x in row)
    assert all(sum(row) <= scale for row in mat)
    for _ in range(m):
        mat = [[x // scale for x in row] for row in mm(mat, mat)]
        assert all(sum(row) <= scale for row in mat)
    eps = F(2 * lam * lam, steps) + F(n * steps, scale)
    return [mat[x] for x in starts], scale, eps


def direct_uniformization(h, start, states, bin_sites, terms, buckets=None, bucket_count=None):
    """Independent rational enclosure, including the whole Poisson tail."""
    d = len(h)
    lam = max(h[i][i] for i in range(d))
    buckets = [sum(u in bin_sites for u in state) for state in states] if buckets is None else buckets
    bucket_count = len(states[0]) + 1 if bucket_count is None else bucket_count
    if lam == 0:
        counts = [F(0)] * bucket_count
        counts[buckets[start]] = F(1)
        return [(x, x) for x in counts]
    assert terms + 2 > lam
    b = [[(lam if i == j else 0) - h[i][j] for j in range(d)] for i in range(d)]
    assert all(x >= 0 for row in b for x in row)
    row = [0] * d
    row[start] = 1
    partial = [F(0)] * bucket_count
    factorial, expsum, power = 1, F(0), 1
    sparse = [[(j, x) for j, x in enumerate(line) if x] for line in b]
    for r in range(terms + 1):
        expsum += F(power, factorial)
        for j, x in enumerate(row):
            partial[buckets[j]] += F(x, factorial)
        if r < terms:
            nxt = [0] * d
            for i, x in enumerate(row):
                if x:
                    for j, y in sparse[i]:
                        nxt[j] += x * y
            row = nxt
            factorial *= r + 1
            power *= lam
    nextterm = F(power * lam, factorial * (terms + 1))
    exptail = nextterm / (1 - F(lam, terms + 2))
    upperexp = expsum + exptail
    tail = exptail / expsum
    return [(x / upperexp, min(F(1), x / expsum + tail)) for x in partial]


def qstr(x):
    return {"numerator": str(x.numerator), "denominator": str(x.denominator),
            "decimal_diagnostic": float(x)}


def endpoint_case(name, n, edges, start, bin_sites, cycle=False, potential=None):
    potential = [0] * n if potential is None else potential
    k = len(start)
    neg = [(0, n - 1)] if cycle and k % 2 == 0 else []
    a = laplacian(n, edges, potential, neg)
    c = cover_laplacian(n, edges, potential, neg) if neg else a
    m, p = 35, 86
    begin = time.perf_counter()
    rows, scale, eps = heat_rows(c, start, m, p)
    if neg:
        rows = [[row[y] - row[y + n] for y in range(n)] for row in rows]
    assert all(sum(abs(x) for x in row) <= scale for row in rows)
    nums, pfmatrix = count_pf(rows, bin_sites)
    assert nums == count_minors(rows, bin_sites)
    assert nums == pfaffian_recursive(pfmatrix)
    den, delta = scale ** k, k * eps
    coeffs = [F(nums[j] if j < len(nums) else 0, den) for j in range(k + 1)]
    states, h = killed(n, edges, k, potential)
    assert compound(a, k)[1] == h
    direct = direct_uniformization(h, states.index(tuple(start)), states, bin_sites, 140)
    error_upper = sum(max(abs(x - lo), abs(x - hi)) for x, (lo, hi) in zip(coeffs, direct))
    assert error_upper <= delta
    s_hat = sum(coeffs)
    s_lower = max(F(0), s_hat - delta)
    negmass = sum(-x for x in coeffs if x < 0)
    weights = [max(0, x) for x in nums]
    width = (sum(weights) - 1).bit_length() if sum(weights) else None
    # Compare the whole ideal prefix receiver law, not just its count polynomial,
    # against a separately constructed physical killed-generator enclosure.
    full_direct = direct_uniformization(h, states.index(tuple(start)), states, bin_sites, 140,
                                       buckets=list(range(len(states))), bucket_count=len(states))
    direct_s_lower = sum(lo for lo, _ in full_direct)
    direct_s_upper = sum(hi for _, hi in full_direct)
    tree = exact_tree_law(n, k, PrefixMass(rows))
    full_tree_error = sum(max(abs(tree.get(y, F(0)) - lo / direct_s_upper),
                              abs(tree.get(y, F(0)) - hi / direct_s_lower))
                          for y, (lo, hi) in zip(states, full_direct)) / 2
    depth = k * (n - 1).bit_length()
    assert full_tree_error <= depth * delta / s_lower
    return {"name": name, "n": n, "k": k, "start": start,
            "edge_rates": edges, "site_killing_rates": potential, "cycle": cycle,
            "bin_sites": sorted(bin_sites), "cover_states": len(c),
            "m": m, "p": p, "one_row_error": qstr(eps),
            "coefficient_l1_error_bound": qstr(delta),
            "coefficient_integer_numerators": [str(x) for x in nums],
            "common_denominator": str(den),
            "coefficient_decimals_diagnostic": [float(x) for x in coeffs],
            "survival_lower_bound": qstr(s_lower),
            "conditional_count_TV_bound": qstr(delta / s_lower) if s_lower else None,
            "bounded_sampler_TV_bound_including_fallback": qstr(delta / s_lower + F(1, 1 << 32)) if s_lower else None,
            "sampler_attempt_cap": 32, "sampler_max_fair_bits": 32 * width if width is not None else None,
            "heat_squaring_scalar_integer_products": m * len(c) ** 3,
            "full_endpoint_decision_bound": k * (n - 1).bit_length(),
            "full_endpoint_sampler_TV_bound": qstr(k * (n - 1).bit_length() *
                    (delta / s_lower + F(1, 1 << 32))) if s_lower else None,
            "independent_whole_conditional_endpoint_TV_upper": qstr(full_tree_error),
            "negative_coefficient_mass": qstr(negmass),
            "independent_direct_enclosure_l1_upper": qstr(error_upper),
            "elapsed_seconds_diagnostic": time.perf_counter() - begin,
            "all_exact_comparisons_passed": True}


def parity_case(edges):
    n, start, bins, m, p = 4, (0, 1), {2, 3}, 35, 86
    k = len(start)
    rows, scale, eps = heat_rows(laplacian(n, edges), start, m, p)
    nums, _ = count_pf(rows, bins)
    coeffs = [F(nums[j] if j < len(nums) else 0, scale ** k) for j in range(k + 1)]
    states = list(permutations(range(n)))
    ix = {state: j for j, state in enumerate(states)}
    h = [[0] * len(states) for _ in states]
    total_rate = sum(r for _, _, r in edges)
    buckets = []
    for i, sigma in enumerate(states):
        h[i][i] = total_rate
        for u, v, rate in edges:
            after = tuple(v if x == u else u if x == v else x for x in sigma)
            h[i][ix[after]] -= rate
        images = [sigma[x] for x in start]
        parity = sum(images[i] > images[j] for i in range(k) for j in range(i + 1, k)) % 2
        count = sum(x in bins for x in images)
        buckets.append(count + parity * (k + 1))
    direct = direct_uniformization(h, ix[tuple(range(n))], states, set(), 140,
                                  buckets=buckets, bucket_count=2 * (k + 1))
    signed = [(direct[j][0] - direct[j + k + 1][1],
               direct[j][1] - direct[j + k + 1][0]) for j in range(k + 1)]
    err = sum(max(abs(a - lo), abs(a - hi)) for a, (lo, hi) in zip(coeffs, signed))
    assert err <= k * eps
    oddlo = sum(direct[j][0] for j in range(k + 1, 2 * (k + 1)))
    oddhi = sum(direct[j][1] for j in range(k + 1, 2 * (k + 1)))
    return {"n": n, "k": k, "starting_labels": start, "rates": edges,
            "graph": "branching star", "bin_sites": sorted(bins),
            "signed_bin_count_coefficient_diagnostics": [float(x) for x in coeffs],
            "order_sign_expectation_diagnostic": float(sum(coeffs)),
            "odd_order_probability_interval": [qstr(oddlo), qstr(oddhi)],
            "exact_l1_error_bound": qstr(k * eps),
            "independent_full_24_state_l1_enclosure": qstr(err),
            "all_exact_comparisons_passed": True}, rows, scale, eps, (oddlo, oddhi)


def main():
    begin = time.perf_counter()
    generator_checks = 0
    cover_checks = 0
    for n in range(2, 9):
        path = [(i, i + 1, (i % 3) + 1) for i in range(n - 1)]
        potential = [(i * i) % 3 for i in range(n)]
        for k in range(1, n + 1):
            a = laplacian(n, path, potential)
            assert compound(a, k)[1] == killed(n, path, k, potential)[1]
            generator_checks += 1
        if n >= 3:
            cyc = path + [(0, n - 1, 4)]
            for k in range(1, n + 1):
                neg = [(0, n - 1)] if k % 2 == 0 else []
                a = laplacian(n, cyc, potential, neg)
                assert compound(a, k)[1] == killed(n, cyc, k, potential)[1]
                generator_checks += 1
                if neg:
                    c = cover_laplacian(n, cyc, potential, neg)
                    t = [[(1 if i == j else -1 if i == j + n else 0)
                          for j in range(n)] for i in range(2 * n)]
                    assert mm(c, t) == mm(t, a)
                    cover_checks += 1

    swap_checks = 0
    for n in range(2, 8):
        for k in range(1, n + 1):
            for u, v in combinations(range(n), 2):
                assert compound(laplacian(n, [(u, v, 1)]), k)[1] == swap_wedge(n, k, u, v)
                swap_checks += 1

    pfchecks = 0
    for n in range(2, 9):
        for k in range(1, min(5, n) + 1):
            rows = [[((i + 3) * (j + 2) * (i - j) + 1) % 13 - 6
                     for j in range(n)] for i in range(k)]
            bins = {j for j in range(n) if j % 2}
            pf, a = count_pf(rows, bins)
            assert pf == count_minors(rows, bins)
            assert pf == pfaffian_recursive(a)
            pfchecks += 1
    # A zero pivot with a nonzero Pfaffian must be handled exactly.
    a = [[(0,), (0,), (1,), (0,)], [(0,), (0,), (0,), (1,)],
         [(-1,), (0,), (0,), (0,)], [(0,), (-1,), (0,), (0,)]]
    assert pfaffian_bareiss(a) == (-1,)
    pfchecks += 1

    prefix_checks = 0
    for n in range(2, 8):
        for k in range(1, min(4, n) + 1):
            rows = [[((i + 5) * (j + 2) * (i - j) + 1) % 11 - 5
                     for j in range(n)] for i in range(k)]
            oracle = PrefixMass(rows)
            for lower in range(n + 1):
                for s in range(min(k, lower) + 1):
                    for fixed in combinations(range(lower), s):
                        assert oracle(fixed, lower) == explicit_prefix_mass(rows, fixed, lower)
                        prefix_checks += 1
    # Exact probability tree on a rational nonnegative endpoint measure.
    rows = [[3, 1, 0, 0], [0, 1, 3, 0]]
    oracle = PrefixMass(rows)
    endpoint = sample_sorted_endpoints(4, 2, oracle, lambda b: 0)
    assert len(set(endpoint["endpoint"])) == 2
    assert endpoint["endpoint"] == sorted(endpoint["endpoint"])
    assert endpoint["decisions"] <= 2 * (4 - 1).bit_length()
    sampler_checks_extra = 1

    sampler_checks = 0
    for total in range(1, 33):
        weights = [total // 3, total // 4, total - total // 3 - total // 4]
        width = (total - 1).bit_length()
        observed = [0] * 3
        for u in range(1 << width):
            draw = sample_integer_weights(weights, lambda b, u=u: u, attempts=1)
            if not draw["fallback"]:
                observed[draw["count"]] += 1
        assert observed == weights
        sampler_checks += 1
    # Exercise the last success, fallback and zero-bit deterministic case.
    draws = iter([7] * 31 + [4])
    assert sample_integer_weights([2, 3], lambda b: next(draws))["count"] == 1
    assert sample_integer_weights([2, 3], lambda b: 7)["fallback"]
    assert sample_integer_weights([0, 1], lambda b: 0)["fair_bits"] == 0
    sampler_checks += 3
    sampler_checks += sampler_checks_extra

    # Audit signed-mass tree repair against a positive measure independently of
    # the determinant representation, including an actual negative leaf.
    repair_states = list(combinations(range(4), 2))
    target_weights = [1, 100, 200, 300, 400, 500]
    signed_weights = [-1, 102, 200, 300, 400, 500]
    total = sum(target_weights)
    assert total == sum(signed_weights)

    def fixture_mass(fixed, lower):
        return sum(weight for y, weight in zip(repair_states, signed_weights)
                   if y[:len(fixed)] == fixed and
                   all(v >= lower for v in y[len(fixed):]))

    repair_delta = F(sum(abs(a - b) for a, b in zip(target_weights, signed_weights)), total)
    repair_depth = 2 * (4 - 1).bit_length()
    repair_bounds = []
    for cap in (None, 8):
        law = exact_tree_law(4, 2, fixture_mass, attempt_cap=cap)
        tv = sum(abs(F(weight, total) - law.get(y, F(0)))
                 for y, weight in zip(repair_states, target_weights)) / 2
        bound = repair_depth * (repair_delta + (F(1, 1 << cap) if cap else 0))
        assert tv <= bound
        repair_bounds.append({"attempt_cap": cap, "exact_TV": qstr(tv),
                              "proved_TV_upper": qstr(bound)})

    # Pair exchange loop survives inside k-particle spaces with fixed spectators.
    loop_checks = []
    base = [(1, 2), (0, 2), (2, 3), (0, 3), (1, 3), (0, 1), (1, 2)]
    for k in range(2, 7):
        n = k + 2
        spectators = tuple(range(4, n))
        states = [tuple(sorted(x + spectators)) for x in base]
        product = 1
        traversals = {}
        for x, y in zip(states, states[1:]):
            u, = set(x) - set(y)
            v, = set(y) - set(x)
            changed = list(x)
            changed[changed.index(u)] = v
            inv = sum(changed[i] > changed[j] for i in range(k)
                      for j in range(i + 1, k))
            product *= -1 if inv % 2 else 1
            traversals[(u, v)] = traversals.get((u, v), 0) + 1
        assert product == -1
        assert all(traversals.get((v, u), 0) == count
                   for (u, v), count in traversals.items())
        loop_checks.append({"n": n, "k": k, "exterior_sign_product": product,
                            "all_edge_orientations_cancel": True})

    # The one-hole exceptional reduction works even on branching/nonbipartite graphs.
    hole_checks = 0
    for n in range(3, 9):
        edges = [(0, i, i) for i in range(1, n)] + [(1, 2, 2)]
        a = laplacian(n, edges, negative=[(u, v) for u, v, _ in edges])
        states, wedge = compound(a, n - 1)
        _, phys = killed(n, edges, n - 1)
        holes = [next(j for j in range(n) if j not in x) for x in states]
        gauged = [[((-1) ** (holes[i] + holes[j])) * wedge[i][j]
                   for j in range(n)] for i in range(n)]
        assert gauged == phys
        hole_checks += 1

    cases = [
        endpoint_case("path_k3_with_site_killing", 6,
                      [(0, 1, 1), (1, 2, 2), (2, 3, 1), (3, 4, 3), (4, 5, 1)],
                      (0, 2, 5), {3, 4, 5}, potential=[0, 1, 0, 0, 0, 1]),
        endpoint_case("cycle_k2_antiperiodic", 5,
                      [(0, 1, 1), (1, 2, 2), (2, 3, 1), (3, 4, 2), (4, 0, 1)],
                      (0, 2), {0, 1}, cycle=True),
        endpoint_case("cycle_k3_periodic", 6,
                      [(0, 1, 1), (1, 2, 2), (2, 3, 1), (3, 4, 1), (4, 5, 2), (5, 0, 1)],
                      (0, 2, 4), {0, 1, 2}, cycle=True),
        endpoint_case("cycle_k4_antiperiodic", 6,
                      [(0, 1, 1), (1, 2, 1), (2, 3, 2), (3, 4, 1), (4, 5, 1), (5, 0, 2)],
                      (0, 1, 3, 4), {0, 1, 2}, cycle=True),
    ]
    parity_r, rows_r, scale, eps_r, odd_r = parity_case([(0, 1, 1), (0, 2, 2), (0, 3, 3)])
    parity_q, rows_q, scale_q, eps_q, odd_q = parity_case([(0, 1, 1), (0, 2, 2), (0, 3, 4)])
    assert scale == scale_q
    theta = sum(F(sum(abs(a - b) for a, b in zip(rr, rq)), scale)
                for rr, rq in zip(rows_r, rows_q)) + 2 * (eps_r + eps_q)
    direct_tv_upper = max(abs(odd_r[i] - odd_q[j]) for i in (0, 1) for j in (0, 1))
    assert direct_tv_upper <= theta / 2
    perturbation = {"observable": "endpoint order parity of labels initially at 0 and 1",
                    "certificate_TV_upper": qstr(theta / 2),
                    "independent_full_permutation_TV_upper": qstr(direct_tv_upper),
                    "scope": "one binary observable, not full correlated endpoint TV",
                    "all_exact_comparisons_passed": True}
    sources = [HERE.parents[1] / "originals/exterior/interchange_path_exterior/EXTERIOR_CERTIFIER_REPORT.md",
               HERE.parents[1] / "originals/exterior/interchange_path_exterior/cycle_extension/PROOF.md",
               HERE.parents[1] / "originals/pair/PAIR_CERTIFIED_AVERAGING_REPORT.md"]
    receipt = {"status": "PASS", "python": platform.python_version(),
               "scope": "finite exact diagnostics, not independent theorem/novelty validation",
               "generator_identities": generator_checks, "positive_cover_identities": cover_checks,
               "rank_one_interchange_swap_identities": swap_checks,
               "polynomial_pfaffian_vs_explicit_minor_checks": pfchecks,
               "fixed_prefix_block_pfaffian_checks": prefix_checks,
               "bounded_integer_sampler_checks": sampler_checks,
               "signed_tree_repair_exact_distribution_checks": repair_bounds,
               "branching_obstruction_loops": loop_checks,
               "one_hole_exception_checks": hole_checks,
               "finite_bit_count_cases": cases,
               "arbitrary_graph_interchange_parity_cases": [parity_r, parity_q],
               "parity_rate_perturbation_certificate": perturbation,
               "input_sha256": {str(x.relative_to(HERE.parents[1])): hashlib.sha256(x.read_bytes()).hexdigest()
                                for x in sources},
               "elapsed_seconds_diagnostic": time.perf_counter() - begin,
               "inference_time_seconds": "UNKNOWN", "model_token_usage": "UNKNOWN"}
    (HERE / "checks_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"],
                      "generator_identities": generator_checks,
                      "swap_identities": swap_checks,
                      "pfaffian_checks": pfchecks,
                      "parity_perturbation_TV_bound": perturbation["certificate_TV_upper"]["decimal_diagnostic"],
                      "finite_bit_cases": [{"name": c["name"],
                                            "survival_lower": c["survival_lower_bound"]["decimal_diagnostic"],
                                            "conditional_count_TV_bound": c["conditional_count_TV_bound"]["decimal_diagnostic"]}
                                           for c in cases],
                      "elapsed_seconds_diagnostic": receipt["elapsed_seconds_diagnostic"]}, indent=2))


if __name__ == "__main__":
    main()

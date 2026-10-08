#!/usr/bin/env python3
"""Exact checks of all-arity factorial Walsh tensors and gadget obstructions.

Uses only Python standard library; no numerical solver or approximate counter.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations, product
from math import factorial
from pathlib import Path
import json


def factorial_table(n):
    values = []
    for at in range(4 ** n):
        counts = [0] * 4
        v = at
        for _ in range(n):
            counts[v % 4] += 1
            v //= 4
        a = 1
        for c in counts:
            a *= factorial(c)
        values.append(a)
    return values


def fwht(values):
    out = list(values)
    h = 1
    while h < len(out):
        for i in range(0, len(out), 2 * h):
            for j in range(i, i + h):
                a, b = out[j], out[j + h]
                out[j], out[j + h] = a + b, a - b
        h *= 2
    return out


def colors(at, n):
    z = []
    for _ in range(n):
        z.append(at % 4)
        at //= 4
    return tuple(z)


@lru_cache(None)
def permutation_cycles(n):
    all_cycles = []
    for pi in permutations(range(n)):
        seen = set()
        cycles = []
        for v in range(n):
            if v not in seen:
                cycle = []
                at = v
                while at not in seen:
                    seen.add(at)
                    cycle.append(at)
                    at = pi[at]
                cycles.append(tuple(cycle))
        all_cycles.append(tuple(cycles))
    return tuple(all_cycles)


@lru_cache(None)
def cycle_numerator(counts):
    z = tuple(c for c, k in enumerate(counts) for _ in range(k))
    out = 0
    for cycles in permutation_cycles(len(z)):
        good = True
        for block in cycles:
            xor = 0
            for t in block:
                xor ^= z[t]
            if xor:
                good = False
                break
        if good:
            out += 4 ** len(cycles)
    return out


def denominator_polynomial():
    """D=product_c(1-sum_z chi_z(c) X_z), with integer coefficients."""
    d = {(0, 0, 0, 0): 1}
    for c in range(4):
        e = defaultdict(int)
        for alpha, a in d.items():
            e[alpha] += a
            for z in range(4):
                beta = list(alpha)
                beta[z] += 1
                sign = -1 if (z & c).bit_count() % 2 == 0 else 1
                e[tuple(beta)] += sign * a
        d = {a: v for a, v in e.items() if v}
    return d


DENOM = denominator_polynomial()


@lru_cache(None)
def local_dp_numerator(counts):
    """2^n Fhat, via a four-variable degree-four rational generating function."""
    d = {(0, 0, 0, 0): 1}
    terms = [(b, a) for b, a in DENOM.items() if any(b)]
    for alpha in product(*(range(c + 1) for c in counts)):
        if not any(alpha):
            continue
        value = 0
        for beta, a in terms:
            if all(b <= x for b, x in zip(beta, alpha)):
                gamma = tuple(x - b for x, b in zip(alpha, beta))
                value -= a * d[gamma]
        d[alpha] = value
    value = d[counts]
    for c in counts:
        value *= factorial(c)
    return value


def port_value(bits):
    """Six grouped ports (three starts, then three ends)."""
    z = tuple(2 * bits[t] + bits[t + 3] for t in range(3))
    counts = tuple(z.count(c) for c in range(4))
    return F(cycle_numerator(counts), 8)


def pair_partitions(items, singletons=True):
    if not items:
        yield ()
        return
    first, *tail = items
    if singletons:
        for p in pair_partitions(tuple(tail), singletons):
            yield ((first,),) + p
    for t, other in enumerate(tail):
        rest = tuple(tail[:t] + tail[t + 1:])
        for p in pair_partitions(rest, singletons):
            yield ((first, other),) + p


def flip(x, block):
    out = list(x)
    for at in block:
        out[at] ^= 1
    return tuple(out)


def run():
    stats = Counter()
    for n in range(7):
        table = fwht(factorial_table(n))
        for at, integer in enumerate(table):
            z = colors(at, n)
            counts = tuple(z.count(c) for c in range(4))
            assert integer >= 0
            assert integer == cycle_numerator(counts)
            assert integer == local_dp_numerator(counts)
            stats['all_arity_walsh_cycle_dp_equalities'] += 1
            assert F(integer, 2 ** n) >= 0
            if n:
                # Pin one extra occurrence's two Fourier ports to zero.
                previous = tuple(z[:-1].count(c) for c in range(4))
                if z[-1] == 0:
                    assert F(integer, 2 ** n) == F(n + 3, 2) * F(cycle_numerator(previous), 2 ** (n - 1))
                    stats['zero_pair_pinning_recurrences'] += 1

    even = ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0))
    M = tuple(tuple(int(port_value(a + b)) for b in even) for a in even)
    expected = ((15, 3, 3, 3), (3, 3, 1, 1), (3, 1, 3, 1), (3, 1, 1, 3))
    assert M == expected
    for x in product((0, 1), repeat=6):
        assert (port_value(x) > 0) == (sum(x[:3]) % 2 == sum(x[3:]) % 2 == 0)
        stats['multiplicity_three_support_checks'] += 1

    x = (0,) * 6
    y = (1, 1, 0, 1, 1, 0)
    differences = (0, 1, 3, 4)
    surviving = []
    blocks = []
    for p in pair_partitions(differences):
        zero_blocks = [b for b in p if port_value(flip(x, b)) * port_value(flip(y, b)) == 0]
        if not zero_blocks:
            surviving.append(p)
            products = [port_value(flip(x, b)) * port_value(flip(y, b)) for b in p]
            assert products == [9, 9]
        blocks.append({'partition': p, 'zero_flips': zero_blocks})
    assert len(blocks) == 10 and surviving == [((0, 1), (3, 4))]
    assert port_value(x) * port_value(y) == 45

    mg_values = Counter()
    quartet_original = {0, 1, 3, 4}
    for order in permutations(range(6)):
        i, j, k, ell = [h for h, old in enumerate(order) if old in quartet_original]
        def sig(selected):
            original = [0] * 6
            for at in selected:
                original[order[at]] = 1
            return port_value(tuple(original))
        residual = (sig(()) * sig((i, j, k, ell))
                    - sig((i, j)) * sig((k, ell))
                    + sig((i, k)) * sig((j, ell))
                    - sig((i, ell)) * sig((j, k)))
        assert residual
        mg_values[str(residual)] += 1
        stats['matchgate_port_order_obstructions'] += 1

    encoding_witnesses = []
    for row in permutations(range(4)):
        for col in permutations(range(4)):
            def val(bits):
                return M[row[2 * bits[0] + bits[1]]][col[2 * bits[2] + bits[3]]]
            witness = None
            for i, j in combinations(range(4), 2):
                rest = [t for t in range(4) if t not in (i, j)]
                for ys in product((0, 1), repeat=2):
                    b = [0] * 4
                    for t, at in zip(rest, ys):
                        b[t] = at
                    f = []
                    for a, c in ((0, 0), (0, 1), (1, 0), (1, 1)):
                        b[i], b[j] = a, c
                        f.append(val(b))
                    aa, bb, cc, dd = f
                    if 3 * aa * dd <= bb * cc:
                        witness = {'varied_bits': [i, j], 'fixed_bits': list(zip(rest, ys)),
                                   'values_00_01_10_11': f,
                                   'diagonal_products': [aa * dd, bb * cc]}
                        break
                if witness:
                    break
            assert witness
            encoding_witnesses.append({'row_encoding': row, 'column_encoding': col, 'witness': witness})
            stats['all_two_bit_pattern_encoding_obstructions'] += 1

    row_denominator = [F(1, 2), F(1), F(1), F(1, 2)]
    row_walsh = [v / 2 for v in fwht(row_denominator)]
    assert row_walsh == [F(3, 2), F(0), F(0), F(-1, 2)]
    result = {'status': 'PASS', 'counts': dict(stats), 'arity3_matrix': M,
              'windability_witness': {'x': x, 'y': y, 'original_product': 45,
                                      'sole_surviving_matching': surviving[0],
                                      'required_flipped_product': 9, 'all_partitions': blocks},
              'matchgate_residuals': dict(mg_values),
              'row_denominator_walsh': list(map(str, row_walsh)),
              'scope': 'Exact local representation proofs only; no generic FPRAS or AP-hardness assertion'}
    root = Path(__file__).parent
    (root / 'CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    (root / 'ENCODING_CERTIFICATES.json').write_text(json.dumps(encoding_witnesses, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'counts': dict(stats)}, indent=2))


if __name__ == '__main__':
    run()

#!/usr/bin/env python3
"""Bounded exact token check of the all-length three-case proof.

Only standard-library symbolic permutations. Deep initial words represent
the exact bulk; no reflecting cutoff is used. The proof is in the sibling
Markdown source, not the finite count. Both original and reduced algorithms
retain explicit bath coordinates.
"""
from itertools import product, combinations
from collections import Counter
from pathlib import Path
import argparse
import json
import resource
import time


def call(ports, bath, j):
    if ports[j] is not None:
        bath.insert(0, ports[j])
        ports[j] = None
    else:
        assert bath, "This diagnostic is expressly on the deep bulk"
        ports[j] = bath.pop(0)


def toggle(ports, bath, j):
    for a in range(j):
        call(ports, bath, a)
    call(ports, bath, j)
    for a in reversed(range(j)):
        call(ports, bath, a)


def unmatched(bits, offset=0):
    pops, pushes = [], []
    for a, bit in enumerate(bits, offset):
        if bit:
            pushes.append(a)
        elif pushes:
            pushes.pop()
        else:
            pops.append(a)
    return pops, pushes


def direct(bits, i, j, order):
    ports = [f"I{a}" if bit else None for a, bit in enumerate(bits)]
    bath = [f"B{a}" for a in range(3 * len(bits))]
    for a in order:
        toggle(ports, bath, a)
    return ports, bath


def reduced(bits, i, j, first):
    """Equations (2)--(4), followed by the exact inverse-prefix queue."""
    ports = [f"I{a}" if bit else None for a, bit in enumerate(bits)]
    bath = [f"B{a}" for a in range(3 * len(bits))]
    pp, pu = unmatched(bits[:i])
    mp, mu = unmatched(bits[i + 1:j], i + 1)
    m, h, d = len(pp), len(pu), len(mp)
    w = ports[mu[0]] if mu else ports[j]
    for a, b in zip(mu, mu[1:] + [j]):
        ports[a] = ports[b]
    ports[j] = None
    stack = [f"I{a}" for a in reversed(pu)] + bath[m:]
    if first:
        stack.insert(d, w)
        ports[i] = stack.pop(0)
    else:
        ports[i] = stack.pop(0)
        stack.insert(d, w)
    for a in reversed(pu):
        ports[a] = stack.pop(0)
    return (ports, bath[:m] + stack), (m, h, d)


def run(max_k=9):
    started = time.perf_counter()
    rows = []
    for k in range(2, max_k + 1):
        counts = Counter()
        for bits in product((0, 1), repeat=k):
            for i, j in combinations(range(k), 2):
                if bits[i] or not bits[j]:
                    continue
                a, b = direct(bits, i, j, [i, j]), direct(bits, i, j, [j, i])
                aa, (m, h, d) = reduced(bits, i, j, True)
                bb, _ = reduced(bits, i, j, False)
                assert a == aa and b == bb, (bits, i, j, a, aa, b, bb)
                orig = [f"B{a}" for a in range(3 * k)]
                at = [x for x in a[0] if x] + a[1]
                bt = [x for x in b[0] if x] + b[1]
                changed = [(x, y) for x, y in zip(at, bt) if x != y]
                assert len(changed) == 2 and changed[0] == changed[1][::-1]
                types = ''.join(sorted(x[0] for x, _ in changed))
                if h > d:
                    assert types == 'II' and a[1] == orig and b[1] == orig
                    counts['h>d_input_only'] += 1
                elif h == d:
                    assert types == 'BI' and a[1] == orig and b[1] != orig
                    counts['h=d_one_bath_swap'] += 1
                else:
                    assert types == 'BI' and a[1] != orig and b[1] != orig
                    assert sum(x.startswith('I') for x in a[1]) == 1
                    assert sum(x.startswith('I') for x in b[1]) == 1
                    counts['h<d_both_export'] += 1
        rows.append({'k': k, 'oriented_endpoint_pattern_sectors': sum(counts.values()),
                     'counts': dict(counts), 'all_reduced_formulas_match': True})
    witnesses = []
    for bits, i, j in [((1,0,0,1,1,1),1,5), ((0,0,1),0,2)]:
        a, (m,h,d) = reduced(bits,i,j,True)
        b, _ = reduced(bits,i,j,False)
        witnesses.append({'bits': bits, 'i': i, 'j': j, 'm': m, 'h': h, 'd': d,
                          'first': a, 'second': b})
    return {'scope': 'Bounded exact diagnostic of the separately proved all-length classification',
            'max_k': max_k, 'rows': rows, 'omitted_premise_witnesses': witnesses,
            'wall_seconds': time.perf_counter() - started,
            'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'discovery_inference_review_cost': 'Unknown; replay does not measure discovery'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-k', type=int, default=9)
    parser.add_argument('--output', default=str(Path(__file__).with_suffix('.json')))
    args = parser.parse_args()
    result = run(args.max_k)
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k!='omitted_premise_witnesses'},indent=2))

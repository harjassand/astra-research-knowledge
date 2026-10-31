"""Shared-XOR compilation, exact recursion, and equally informed baselines.

Matrices are packed Python integer rows; all arithmetic is exact GF(2).
No downloaded libraries or candidate fast identities are used for acquisition.
The explicit Winograd baseline is separately supplied as established knowledge.
"""
import argparse
import gc
import hashlib
import itertools
import json
import math
import random
import statistics
import time
from pathlib import Path
from discover import verify, addition_count, schoolbook


def xor_compile(masks, d):
    """Greedy common-pair elimination; records every pair-scoring operation."""
    forms = [{j for j in range(d) if (m >> j) & 1} for m in masks]
    nodes = []
    checks = 0
    while True:
        counts = {}
        for f in forms:
            for p in itertools.combinations(sorted(f), 2):
                checks += 1
                counts[p] = counts.get(p, 0)+1
        if not counts or max(counts.values()) < 2:
            break
        pair = min(counts, key=lambda p: (-counts[p], p))
        index = d+len(nodes)
        nodes.append(pair)
        for f in forms:
            if set(pair) <= f:
                f.difference_update(pair)
                f.add(index)
    outputs = []
    # Finishing each target also reuses already available exact linear forms.
    value_masks = [1 << i for i in range(d)]
    for i, j in nodes:
        value_masks.append(value_masks[i] ^ value_masks[j])
    known = {m: i for i, m in enumerate(value_masks)}
    for mask, f in zip(masks, forms):
        if mask in known:
            outputs.append(known[mask])
            continue
        f = sorted(f)
        x = f[0]
        for y in f[1:]:
            v = value_masks[x] ^ value_masks[y]
            if v in known:
                x = known[v]
            else:
                nodes.append((x, y))
                x = len(value_masks)
                value_masks.append(v)
                known[v] = x
        outputs.append(x)
    for mask, out in zip(masks, outputs):
        assert value_masks[out] == mask
    return dict(inputs=d, nodes=nodes, outputs=outputs,
                pair_score_checks=checks, gates=len(nodes))


def compile_scheme(scheme):
    rank = len(scheme)
    return dict(left=xor_compile([t[0] for t in scheme], 4),
                right=xor_compile([t[1] for t in scheme], 4),
                output=xor_compile([sum(((t[2] >> k) & 1) << j
                                    for j, t in enumerate(scheme))
                                   for k in range(4)], rank))


def evaluate(circuit, inputs):
    vals = list(inputs)
    for a, b in circuit['nodes']:
        vals.append(add(vals[a], vals[b]))
    return [vals[i] for i in circuit['outputs']]


def add(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def split(a):
    h = len(a)//2
    mask = (1 << h)-1
    return (tuple(x & mask for x in a[:h]), tuple(x >> h for x in a[:h]),
            tuple(x & mask for x in a[h:]), tuple(x >> h for x in a[h:]))


def join(blocks):
    a, b, c, d = blocks
    h = len(a)
    return tuple(x | (y << h) for x, y in zip(a, b))+tuple(x | (y << h) for x, y in zip(c, d))


def classic(a, b):
    out = []
    for row in a:
        ans = 0
        while row:
            low = row & -row
            ans ^= b[low.bit_length()-1]
            row ^= low
        out.append(ans)
    return tuple(out)


def four_russians(a, b, k=None):
    n = len(a)
    if k is None:
        k = max(1, min(8, n.bit_length()-2))
    out = [0]*n
    for start in range(0, n, k):
        width = min(k, n-start)
        table = [0]*(1 << width)
        for index in range(1, 1 << width):
            low = index & -index
            table[index] = table[index ^ low] ^ b[start+low.bit_length()-1]
        mask = (1 << width)-1
        for i, row in enumerate(a):
            out[i] ^= table[(row >> start) & mask]
    return tuple(out)


def learned(a, b, circuits, cutoff=32):
    n = len(a)
    if n <= cutoff:
        return four_russians(a, b)
    if n & 1:
        raise ValueError('recursive size must be a power of two')
    aa = evaluate(circuits['left'], split(a))
    bb = evaluate(circuits['right'], split(b))
    products = [learned(x, y, circuits, cutoff) for x, y in zip(aa, bb)]
    return join(evaluate(circuits['output'], products))


def winograd(a, b, cutoff=32):
    if len(a) <= cutoff:
        return four_russians(a, b)
    a11, a12, a21, a22 = split(a)
    b11, b12, b21, b22 = split(b)
    s1 = add(a21, a22)
    s2 = add(s1, a11)
    s3 = add(a11, a21)
    s4 = add(a12, s2)
    t1 = add(b12, b11)
    t2 = add(b22, t1)
    t3 = add(b22, b12)
    t4 = add(t2, b21)
    p1 = winograd(a11, b11, cutoff)
    p2 = winograd(a12, b21, cutoff)
    p3 = winograd(s4, b22, cutoff)
    p4 = winograd(a22, t4, cutoff)
    p5 = winograd(s1, t1, cutoff)
    p6 = winograd(s2, t2, cutoff)
    p7 = winograd(s3, t3, cutoff)
    u1 = add(p1, p2)
    u2 = add(p1, p6)
    u3 = add(u2, p7)
    u4 = add(u2, p5)
    u5 = add(u4, p3)
    u6 = add(u3, p4)
    u7 = add(u3, p5)
    return join((u1, u5, u6, u7))


def random_matrix(n, rng):
    return tuple(rng.getrandbits(n) for _ in range(n))


def all_matrices_2():
    return [((v & 3), (v >> 2)) for v in range(16)]


def test(circuits, scheme):
    count = 0
    for a in all_matrices_2():
        for b in all_matrices_2():
            truth = classic(a, b)
            assert learned(a, b, circuits, 1) == truth
            assert winograd(a, b, 1) == truth
            count += 1
    rng = random.Random(19271)
    for n in [1, 2, 4, 8, 16, 32, 64]:
        cases = [random_matrix(n, rng) for _ in range(10)]
        cases += [(0,)*n, ((1 << n)-1,)*n, tuple(1 << i for i in range(n))]
        for a in cases:
            b = random_matrix(n, rng)
            truth = classic(a, b)
            assert learned(a, b, circuits, 1) == truth
            assert winograd(a, b, 1) == truth
            assert four_russians(a, b) == truth
            count += 1
    # Every individual bit in the acquired certificate is adversarially flipped.
    tamper_rejections = 0
    for t in range(len(scheme)):
        for axis in range(3):
            for bit in range(4):
                bad = [list(x) for x in scheme]
                bad[t][axis] ^= 1 << bit
                if not verify(bad):
                    tamper_rejections += 1
    assert tamper_rejections == 84
    # Find an explicit failure of a GF(2) certificate over a different field.
    char3_failure = None
    for ia in range(4):
        for ib in range(4):
            got = [sum(((u >> ia) & 1)*((v >> ib) & 1)*((w >> k) & 1)
                       for u, v, w in scheme) % 3 for k in range(4)]
            expected = [int(ia//2 == k//2 and ia%2 == ib//2 and ib%2 == k%2)
                        for k in range(4)]
            if got != expected:
                char3_failure = dict(left_basis=ia, right_basis=ib,
                                     got=got, expected=expected)
                break
        if char3_failure:
            break
    assert char3_failure is not None
    return dict(exact_cases=count, tamper_rejections=tamper_rejections,
                noncommuting_block_recursion_tested=True,
                characteristic_3_counterexample=char3_failure)


def timing(fn, repeats):
    runs = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        runs.append(time.perf_counter()-start)
    return dict(median_seconds=statistics.median(runs), all_seconds=runs)


def benchmark(circuits, sizes, repeats):
    rng = random.Random(81550)
    rows = []
    for n in sizes:
        a, b = random_matrix(n, rng), random_matrix(n, rng)
        truth = four_russians(a, b)
        methods = {'packed_classic': lambda: classic(a, b),
                   'four_russians': lambda: four_russians(a, b)}
        for cutoff in [16, 32, 64, 128, 256]:
            if cutoff < n:
                methods[f'acquired_cutoff_{cutoff}'] = lambda c=cutoff: learned(a, b, circuits, c)
                methods[f'winograd_cutoff_{cutoff}'] = lambda c=cutoff: winograd(a, b, c)
        row = dict(size=n, methods={})
        for name, fn in methods.items():
            assert fn() == truth, (n, name)
            row['methods'][name] = timing(fn, repeats)
        rows.append(row)
        print(json.dumps(row), flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scheme', default='acquired_scheme.json')
    ap.add_argument('--out', default='compiler_results.json')
    ap.add_argument('--sizes', default='32,64,128,256,512')
    ap.add_argument('--repeats', type=int, default=3)
    a = ap.parse_args()
    payload = json.loads(Path(a.scheme).read_text())
    scheme = payload['scheme']
    assert verify(scheme)
    start = time.perf_counter()
    circuits = compile_scheme(scheme)
    compile_seconds = time.perf_counter()-start
    Path('compiled_circuit.json').write_text(json.dumps(circuits, indent=2)+'\n')
    result = dict(compiled_gates={k: v['gates'] for k, v in circuits.items()},
                  compile_seconds=compile_seconds,
                  tests=test(circuits, scheme),
                  benchmark=benchmark(circuits, [int(n) for n in a.sizes.split(',')], a.repeats))
    Path(a.out).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'benchmark'}, indent=2))


if __name__ == '__main__':
    main()

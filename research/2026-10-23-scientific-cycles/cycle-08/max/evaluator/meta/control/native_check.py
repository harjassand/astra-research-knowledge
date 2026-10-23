"""Exact finite raw-stack checks. No sector normal form builds G1.

The only buffer is a coordinate core for evaluating finite words; all final
tails are checked unchanged. This is not a bath cutoff or a channel model.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import comb
import json
import time

START_WALL = time.monotonic()
START_CPU = time.process_time()


def toggle(ports, stack, i):
    a = list(ports)
    b = list(stack)
    for j in list(range(i)) + [i] + list(range(i - 1, -1, -1)):
        if a[j] == 0:
            a[j] = b.pop(0)
        else:
            b.insert(0, a[j])
            a[j] = 0
    return tuple(a), tuple(b)


def raw_g(d, k):
    ports = list(product(range(d + 1), repeat=k))
    prefixes = list(product(range(1, d + 1), repeat=k))
    pindex = {x: n for n, x in enumerate(ports)}
    findex = {x: n for n, x in enumerate(prefixes)}
    tail = (1,) * (4 * k)
    entries = defaultdict(int)
    for a, word in enumerate(ports):
        q0 = sum(x > 0 for x in word)
        for fin, prefix in enumerate(prefixes):
            for i in range(k):
                a1, b1 = toggle(word, prefix + tail, i)
                s = sum(x > 0 for x in a1) - q0
                assert s in (-1, 1)
                for j in range(k):
                    a2, b2 = toggle(a1, b1, j)
                    if sum(x > 0 for x in a2) != q0:
                        continue
                    assert len(b2) == 5 * k and b2[k:] == tail
                    entries[pindex[a2], findex[b2[:k]], a, fin] += s
    entries = {key: value for key, value in entries.items() if value}
    for (b, fout, a, fin), value in entries.items():
        assert entries.get((a, fin, b, fout)) == value
    return ports, prefixes, entries


def optimum(p):
    d = len(p)
    # Unique positive solution of sum (1-t/p_i)_+ = 1.
    for s in range(2, d + 1):
        active = sorted(range(d), key=lambda i: -p[i])[:s]
        t = F(s - 1) / sum((1 / p[i] for i in active), F(0))
        r = [max(1 - t / x, F(0)) for x in p]
        if sum(r) == 1:
            a = 2 * (1 - sum(x*x for x in p))
            b = sum(x * (1 - y)**2 for x, y in zip(p, r))
            return t, r, a, b
    raise AssertionError("No threshold")


def collision(k):
    return sum((F(k - 1 - 2*n) * F(comb(2*n, n), 4**n)
                for n in range((k - 2)//2 + 1)), F(0))


def weights(k):
    w = [F(0) for _ in range(k)]
    for i in range(k - 1):
        for r in range(k - 1 - i):
            for prefix in product((-1, 1), repeat=i):
                s = lo = 0
                for x in prefix:
                    s += x
                    lo = min(lo, s)
                m, h = -lo, s-lo
                for middle in product((-1, 1), repeat=r):
                    z = low = 0
                    for x in middle:
                        z += x
                        low = min(low, z)
                    if h == -low:
                        w[m] += F(1, 2**(i+r+1))
    assert sum(w) == collision(k)/2
    return w


def verify(p, k, raw):
    d = len(p)
    ports, prefixes, g = raw
    fidx = {x: i for i, x in enumerate(prefixes)}
    t, r, a, b = optimum(p)
    z = {fidx[(i+1,)*k]: r[i] for i in range(d) if r[i]}
    h = defaultdict(F)
    for (out, fout, inp, fin), value in g.items():
        if fout == fin and fin in z:
            h[out, inp] += z[fin] * value
    for n, word in enumerate(ports):
        h[n, n] += 2*sum(x > 0 for x in word)-k
    h = {key: value for key, value in h.items() if value}
    sigma = []
    for word in ports:
        x = F(1)
        for v in word:
            x *= F(1, 2) if v == 0 else p[v-1]/2
        sigma.append(x)
    for (out, inp), value in h.items():
        assert h.get((inp, out)) == value
        assert sigma[out] == sigma[inp]  # [sigma,H*]=0
    v = sum((sigma[inp]*value*value for (out, inp), value in h.items()), F(0))
    predicted = a*F(k*(k-1), 8)+(2*b-a)*collision(k)/4
    assert v == predicted
    dual = defaultdict(F)
    for (out, fout, inp, fin), value in g.items():
        if (inp, out) in h:
            dual[fout, fin] += sigma[inp]*h[inp, out]*value
    w = weights(k)
    gaps = [max(t-x, F(0)) for x in p]
    for fout in range(len(prefixes)):
        for fin in range(len(prefixes)):
            target = F(0)
            if fout == fin:
                target = v + sum((w[m]*gaps[c-1]
                                   for m, c in enumerate(prefixes[fin])), F(0))
            assert dual[fout, fin] == target
    spectrum = sorted(set(dual[n, n] for n in range(len(prefixes))))
    return {"d": d, "k": k, "p": list(map(str, p)), "threshold": str(t),
            "r": list(map(str, r)), "a": str(a), "b": str(b),
            "collision": str(collision(k)), "v": str(v),
            "critical_weights": list(map(str, w)),
            "dual_distinct_eigenvalues": list(map(str, spectrum)),
            "native_G1_nonzero_entries": len(g),
            "H_nonzero_entries": len(h), "all_exact_checks_passed": True}


if __name__ == "__main__":
    cases = [tuple(map(F, ("4/5", "3/20", "1/20"))),
             tuple(map(F, ("1/2", "1/3", "1/6"))),
             tuple(map(F, ("9/10", "1/10"))),
             tuple(map(F, ("2/5", "2/5", "1/5")))]
    records = []
    for d in (2, 3):
        for k in (2, 3, 4):
            raw = raw_g(d, k)
            for p in cases:
                if len(p) == d:
                    records.append(verify(p, k, raw))
    result = {"records": records,
              "elapsed_seconds": time.monotonic()-START_WALL,
              "cpu_seconds": time.process_time()-START_CPU,
              "construction": "Raw toggling words, integer G1; rational contractions and full dual matrices."}
    print(json.dumps(result, indent=2))

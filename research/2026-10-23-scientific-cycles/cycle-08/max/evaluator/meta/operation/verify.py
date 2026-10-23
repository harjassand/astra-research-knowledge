"""Bounded native stack-word checks; numpy is used only after constructing words.

No sector normal forms are used to construct G1.  Each C_i is evaluated as
U_0 ... U_{i-1} U_i U_{i-1} ... U_0 on input symbols and a deep finite word.
The final tail is checked unchanged.  This is a finite matrix check, not a
replacement for the all-k proof in REPORT.md.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from pathlib import Path
import json
import time
import numpy as np

wall_start = time.perf_counter()
cpu_start = time.process_time()


def waterfill(ps):
    for r in range(2, len(ps) + 1):
        active = sorted(range(len(ps)), key=lambda i: ps[i], reverse=True)[:r]
        t = F(r - 1) / sum((1 / ps[i] for i in active), F(0))
        zs = [max(F(0), 1 - t / p) for p in ps]
        if sum(zs) == 1:
            return t, zs, sum(p * (1 - z) ** 2 for p, z in zip(ps, zs))
    raise AssertionError("No threshold")


def toggle(inp, bath, i):
    inp, bath = list(inp), list(bath)
    if inp[i] == 0:
        assert bath
        inp[i] = bath.pop(0)
    else:
        bath.insert(0, inp[i])
        inp[i] = 0
    return tuple(inp), tuple(bath)


def ci(inp, bath, i):
    for a in list(range(i)) + [i] + list(range(i - 1, -1, -1)):
        inp, bath = toggle(inp, bath, a)
    return inp, bath


def native_g1(d, k):
    inputs = list(product(range(d + 1), repeat=k))
    baths = list(product(range(1, d + 1), repeat=k))
    input_index, bath_index = ({x: i for i, x in enumerate(v)} for v in (inputs, baths))
    nf = len(baths)
    g = defaultdict(int)
    tail = tuple(1 + i % d for i in range(3 * k + 3))
    for a, inp in enumerate(inputs):
        for gidx, prefix in enumerate(baths):
            column = a * nf + gidx
            g[column, column] += k - 2 * sum(x != 0 for x in inp)
            for i in range(k):
                for j in range(i + 1, k):
                    if inp[i] != 0 or inp[j] == 0:
                        continue
                    for first, second, sign in [(i, j, 1), (j, i, -1)]:
                        out, stack = ci(inp, prefix + tail, first)
                        out, stack = ci(out, stack, second)
                        assert len(stack) == k + len(tail)
                        assert stack[k:] == tail
                        row = input_index[out] * nf + bath_index[stack[:k]]
                        g[row, column] += sign
                        g[column, row] += sign
    return inputs, baths, [(row // nf, row % nf, col // nf, col % nf, val)
                           for (row, col), val in g.items() if val]


def contract(entries, zeta, na):
    out = np.zeros((na, na), dtype=complex)
    for b, f, a, g, val in entries:
        out[b, a] += val * zeta[g, f]
    return out


def dual(entries, x, nf):
    out = np.zeros((nf, nf), dtype=complex)
    for b, f, a, g, val in entries:
        out[f, g] += val * x[a, b]
    return out


def count_cm(k):
    cs = [F(0) for _ in range(k)]
    for bits in product((0, 1), repeat=k):
        for i in range(k):
            s = low = 0
            for bit in bits[:i]:
                s += 2 * bit - 1
                low = min(low, s)
            m, h = -low, s - low
            for j in range(i + 1, k):
                if bits[i] != 0 or bits[j] != 1:
                    continue
                s = low = 0
                for bit in bits[i + 1:j]:
                    s += 2 * bit - 1
                    low = min(low, s)
                if h == -low:
                    cs[m] += F(1, 2 ** (k - 1))
    return cs


def check(ps, k, seed):
    d = len(ps)
    t, zs, local = waterfill(ps)
    inputs, baths, entries = native_g1(d, k)
    na, nf = len(inputs), len(baths)
    zeta = np.zeros((nf, nf))
    for i, z in enumerate(zs, 1):
        index = baths.index((i,) * k)
        zeta[index, index] = float(z)
    weights = np.array([float(np.prod([F(1, 2) if a == 0 else ps[a - 1] / 2
                                      for a in inp])) for inp in inputs])
    diag = np.array([2 * sum(a != 0 for a in inp) - k for inp in inputs])
    h = contract(entries, zeta, na) + np.diag(diag)
    value = float(np.sum(weights[:, None] * abs(h) ** 2).real)
    cs = count_cm(k)
    collision = 2 * sum(cs)
    s = 1 - sum(p ** 2 for p in ps)
    expected = s * k * (k - 1) / 4 + (local - s) * collision / 2
    b = dual(entries, weights[:, None] * h, nf)
    r = [t - min(p, t) for p in ps]
    expected_b = np.array([float(expected + sum(cs[m] * r[color - 1]
                                                for m, color in enumerate(prefix)))
                           for prefix in baths])
    rng = np.random.default_rng(seed)
    vector = rng.normal(size=nf) + 1j * rng.normal(size=nf)
    vector /= np.linalg.norm(vector)
    coherent = np.outer(vector, vector.conj())
    hc = contract(entries, coherent, na) + np.diag(diag)
    vc = float(np.sum(weights[:, None] * abs(hc) ** 2).real)
    delta = hc - h
    rhs = float(expected) + 2 * np.trace(coherent @ (b - float(expected) * np.eye(nf))).real
    rhs += float(np.sum(weights[:, None] * abs(delta) ** 2).real)
    checks = {
        "objective_error": abs(value - float(expected)),
        "dual_matrix_error": float(np.max(abs(b - np.diag(expected_b)))),
        "distance_identity_error": abs(vc - rhs),
        "optimizer_commutator_norm": float(np.linalg.norm(weights[:, None] * h - h * weights[None, :])),
        "coherent_competitor_commutator_norm": float(np.linalg.norm(weights[:, None] * hc - hc * weights[None, :])),
        "dual_min_eigenvalue_error": abs(float(np.linalg.eigvalsh(b)[0]) - float(expected)),
        "coherent_competitor_gap": vc - float(expected),
    }
    for key in ("objective_error", "dual_matrix_error", "distance_identity_error",
                "optimizer_commutator_norm", "dual_min_eigenvalue_error"):
        assert checks[key] < 2e-12, (key, checks)
    assert checks["coherent_competitor_gap"] >= -2e-12
    return {"p": [str(p) for p in ps], "k": k, "threshold": str(t),
            "z": [str(z) for z in zs], "local_cost": str(local),
            "collision": str(collision), "critical_site_weights": [str(c) for c in cs],
            "exact_v": str(expected), "joint_dimension": na * nf,
            "nonzero_entries": len(entries), **checks}


examples = [[F(4, 5), F(3, 20), F(1, 20)],
            [F(1, 2), F(1, 3), F(1, 6)],
            [F(9, 10), F(1, 10)],
            [F(2, 5), F(2, 5), F(1, 5)]]
results = [check(ps, k, 20261022 + i * 10 + k)
           for i, ps in enumerate(examples) for k in (2, 3)]
payload = {"method": "Native deep-stack toggle words, then exact sector counts and floating contractions",
           "results": results,
           "script_cpu_seconds": time.process_time() - cpu_start,
           "script_wall_seconds": time.perf_counter() - wall_start}
out = Path(__file__).with_name("verification.json")
out.write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps(payload, indent=2))

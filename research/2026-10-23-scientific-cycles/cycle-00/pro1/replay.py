#!/usr/bin/env python3
"""Finite diagnostic replay for the recurrent-reservoir proof packet.

The proofs in RECURRENT_RESERVOIRS.tex establish the infinite-dimensional
claims. These finite computations check conventions and explicit examples;
their number is not evidence for a general theorem. No R1 replay is run.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import platform
import resource
import time
import numpy as np


def phase_bath():
    rows = []
    for L in range(1, 5):
        for n in range(1, 10):
            actual = Counter(tuple(bits[i % L] for i in range(n))
                             for bits in product((0, 1), repeat=L))
            dist = sum(abs(Fraction(actual[x], 2**L) - Fraction(1, 2**n))
                       for x in product((0, 1), repeat=n)) / 2
            expected = Fraction(0) if n <= L else 1 - Fraction(1, 2**(n-L))
            assert dist == expected
            rows.append({"L": L, "n": n, "half_trace_distance": str(dist)})
    return rows


def swap_choi():
    rows = []
    for n in range(1, 8):
        D = 4**n
        psi = np.zeros((D, 4), dtype=complex)
        for bits in product((0, 1), repeat=n+1):
            bath, inputs = bits[0], bits[1:]
            outputs = (bath,) + inputs[:-1]
            ext = 0
            for bit in outputs + inputs:
                ext = 2*ext + bit
            er = 2*inputs[-1] + bath
            psi[ext, er] = 2**(-(n+1)/2)
        ev = np.linalg.eigvalsh(psi.conj().T @ psi)
        assert np.max(np.abs(ev - .25)) < 1e-12
        half = .5*(sum(abs(ev - 1/D)) + (D-4)/D)
        expected = 1-4/D
        assert abs(half-expected) < 1e-12
        rows.append({"n": n, "external_dimension": D,
                     "choi_rank": 4, "half_trace_distance": half,
                     "full_trace_distance": 2*half})
    return rows


def purity_identity():
    rng = np.random.default_rng(20261021)
    a = rng.normal(size=(6, 6)) + 1j*rng.normal(size=(6, 6))
    u, _ = np.linalg.qr(a)
    k = [u.reshape(2, 3, 2, 3)[i, :, j, :]/np.sqrt(2)
         for i in range(2) for j in range(2)]
    a = rng.normal(size=(3, 3)) + 1j*rng.normal(size=(3, 3))
    x = a+a.conj().T
    y = sum(t@x@t.conj().T for t in k)
    lhs = sum(np.linalg.norm(t@x-y@t, 'fro')**2 for t in k)
    rhs = np.linalg.norm(x, 'fro')**2-np.linalg.norm(y, 'fro')**2
    assert abs(lhs-rhs) < 1e-10
    # A recurrent orbit which is not stationary, with entangling interaction.
    z = np.diag([1., -1.]); flip = np.array([[0., 1.], [1., 0.]])
    p0 = np.diag([1., 0.]); p1 = np.diag([0., 1.])
    u = np.kron(np.eye(2), flip) @ (np.kron(np.eye(2), p0)+np.kron(z, p1))
    tau = np.diag([.7, .3]); tau1 = flip@tau@flip
    defect = np.linalg.norm(u@np.kron(np.eye(2), tau)@u.conj().T-
                            np.kron(np.eye(2), tau1), 'fro')
    assert defect < 1e-12 and np.linalg.norm(tau-tau1) > .1
    return {"hs_identity_absolute_defect": float(abs(lhs-rhs)),
            "period_two_intertwining_defect": float(defect)}


def edge(a, v):
    """Return (output port, new vertex). Vertex is a finite tuple."""
    if v and a == 0:
        return v[-1], v[:-1]
    return 0, v+(a,)


def vertices(d, depth):
    out = [()]
    level = [()]
    for h in range(depth):
        level = [v+(a,) for v in level for a in
                 (range(d) if not v else range(1, d))]
        out += level
    return out


def stationary_weight(v, p, d):
    C = (2*p-1)/(2*p)
    probs = [p]+[(1-p)/(d-1)]*(d-1)
    ans = C
    for a in v:
        ans *= probs[a]/p
    return ans


def dyck_words(m, d):
    def grow(word, pushes, pops):
        if pushes == pops == m:
            yield tuple(word)
        if pushes < m:
            for a in range(1, d):
                yield from grow(word+[a], pushes+1, pops)
        if pops < pushes:
            yield from grow(word+[0], pushes, pops+1)
    return grow([], 0, 0)


def evolve(word, v):
    outs = []
    for a in word:
        b, v = edge(a, v)
        outs.append(b)
    return tuple(outs), v


def tree_checks():
    d, p = 3, Fraction(3, 4)
    q = (1-p)/p; b = d-1
    probs = [p]+[(1-p)/b]*b
    verts = vertices(d, 6)
    for v in verts:
        for a in range(d):
            o, w = edge(a, v)
            assert edge(o, w) == (a, v)
            assert stationary_weight(v, p, d)*probs[a] == stationary_weight(w, p, d)*probs[o]
    partial_mass = sum(stationary_weight(v, p, d) for v in verts)
    assert 1-partial_mass == q**6/(2*p)
    rho = 2*math.sqrt(b)/d
    walk_rows = []
    for n in range(1, 9):
        endpoint_outputs = defaultdict(set)
        endpoint_counts = Counter()
        for word in product(range(d), repeat=n):
            output, w = evolve(word, ())
            endpoint_outputs[w].add(output)
            endpoint_counts[w] += 1
        for w, count in endpoint_counts.items():
            assert len(endpoint_outputs[w]) == count
        max_rank = max(endpoint_counts.values())
        assert max_rank <= (d*rho)**n + 1e-9
        walk_rows.append({"n": n, "input_words": d**n,
                          "reachable_endpoints": len(endpoint_counts),
                          "max_kraus_rank": max_rank,
                          "proved_rank_upper_bound": (d*rho)**n})
    code_rows = []
    base_vertices = [(), (0,), (1,), (2, 1), (0, 2, 1)]
    for m in range(1, 6):
        images = set()
        count = 0
        for word in dyck_words(m, d):
            expected = None
            for v in base_vertices:
                output, final = evolve(word, v)
                assert final == v
                if expected is None: expected = output
                assert output == expected
            images.add(expected); count += 1
        catalan = math.comb(2*m, m)//(m+1)
        assert count == len(images) == catalan*b**m
        code_rows.append({"uses": 2*m, "exact_code_dimension": count,
                          "rate_qubits_per_use": math.log2(count)/(2*m)})
    return {"d": d, "p": str(p), "finite_local_vertices": len(verts),
            "stationary_tail_after_depth_6": str(1-partial_mass),
            "rho": rho,
            "exact_capacity_qubits_per_use": math.log2(2*math.sqrt(b)),
            "full_port_rate_qubits_per_use": math.log2(d),
            "walks": walk_rows, "dyck_codes": code_rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='replay_results.json')
    args = parser.parse_args()
    start = time.perf_counter()
    results = {"status": "finite_diagnostics_passed",
               "scope": "Finite examples and conventions; not a proof by testing.",
               "phase_bath": phase_bath(), "swap": swap_choi(),
               "purity": purity_identity(), "tree": tree_checks()}
    results['resources'] = {
        'wall_seconds': time.perf_counter()-start,
        'max_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'python': platform.python_version(), 'numpy': np.__version__,
        'hardware': platform.machine(),
        'cpu_gpu_cloud_cost': 'No GPU or external compute job used; model/tool energy and cost unavailable.'}
    Path(args.output).write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps({"status": results['status'], "output": args.output,
                      "resources": results['resources'],
                      "tree_capacity_qubits_per_use": results['tree']['exact_capacity_qubits_per_use']}, indent=2))


if __name__ == '__main__':
    main()

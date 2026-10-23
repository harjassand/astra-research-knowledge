#!/usr/bin/env python3
"""Finite admissions only: actual stock-clock probabilities and graph matrices.

No optimizer, parameter search, simulation of preparation, or lab measurement.
The universal statements are proved in PROOF.txt, not inferred from this check.
"""
import json
import math
import resource
import time
from pathlib import Path

import numpy as np


def entropy(x):
    vals = np.linalg.eigvalsh(x.conj().T @ x)
    vals = vals[vals > 1e-13]
    return float(-np.dot(vals, np.log(vals)))


def erase(x, d, nsites, sites):
    sites = list(sites)
    rest = [j for j in range(nsites) if j not in sites]
    order = sites + rest
    perm = order + [j + nsites for j in order]
    l, k = d ** len(sites), d ** len(rest)
    xp = x.reshape([d] * (2 * nsites)).transpose(perm).reshape(l, k, l, k)
    ptr = np.einsum("aiaj->ij", xp)
    yp = np.kron(np.eye(l) / l, ptr)
    inv = np.argsort(perm)
    return yp.reshape([d] * (2 * nsites)).transpose(inv).reshape(x.shape)


def shift(q):
    f = np.zeros((q, q))
    f[(np.arange(q) + 1) % q, np.arange(q)] = 1
    return f


def digits(j, q, r):
    out = []
    for _ in range(r):
        out.append(j % q)
        j //= q
    return out[::-1]


def graph_allowed(row, col, q, r):
    y, z = digits(row, q, r), digits(col, q, r)
    for a in range(r):
        pairs = [(y[b], z[b]) for b in range(r) if b != a]
        if not (all(v == w for v, w in pairs)
                or all(v == (w + 1) % q for v, w in pairs)):
            return False
    return True


def run():
    wall_start, cpu_start = time.perf_counter(), time.process_time()
    max_stock_error = 0.0
    stock_cases = 0
    for d, n in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3)]:
        q, f = d ** n, shift(d ** n)
        for k in range(n + 1):
            tail = d ** (n - k)
            observed = np.zeros(n)
            for t in range(tail):
                c = np.zeros(q)
                c[np.arange(q) % tail == t] = d ** (-k / 2)
                x = f @ np.diag(c)
                for i in range(1, n + 1):
                    y = erase(x, d, n, range(i))
                    observed[i - 1] += float(np.vdot(y, y).real) / tail
            p = np.array([1.0 if i <= k else d ** (k - i)
                          for i in range(1, n + 1)])
            expected = p * np.array([1 - d ** (-(n - i))
                                     for i in range(1, n + 1)])
            err = float(np.max(np.abs(observed - expected)))
            max_stock_error = max(max_stock_error, err)
            assert err < 2e-12, (d, n, k, observed, expected)
            assert float(np.sum(p - observed)) < d / (d - 1) + 1e-12
            stock_cases += 1

    rng = np.random.default_rng(20261022)
    graph_cases = 0
    min_witness_slack = math.inf
    max_nonnormality = 0.0
    exact_obstructions = []
    for n in [2, 3]:
        d, r, taskdim = 2, 2, 2 ** n
        q = taskdim ** r
        f = np.kron(shift(taskdim), shift(taskdim))
        allowed = np.array([[graph_allowed(y, z, taskdim, r)
                             for z in range(q)] for y in range(q)])
        assert np.all(allowed[np.arange(q), np.arange(q)])
        assert np.linalg.norm(f * (~allowed)) == 0
        assert abs(np.linalg.norm(f.conj().T * (~allowed)) ** 2 - q) < 1e-12
        # Every F_-a orbit is a complete taskdim-cycle. This is the exact
        # diagonal-block obstruction after commuting with distinct X*X.
        orbits = []
        todo = set(range(taskdim))
        while todo:
            a = min(todo)
            orb = [(a + j) % taskdim for j in range(taskdim)]
            todo.difference_update(orb)
            orbits.append(len(orb))
        assert orbits == [taskdim]
        exact_obstructions.append({"N": n, "minimum_old_block_rank": taskdim,
                                   "new_graph_row_dimension": 2,
                                   "F_star_completely_off_support": True})
        for _ in range(5):
            c0 = rng.normal(size=q) + 1j * rng.normal(size=q)
            c1 = rng.normal(size=q) + 1j * rng.normal(size=q)
            x = np.diag(c0) + f @ np.diag(c1)
            x /= np.linalg.norm(x)
            assert np.linalg.norm(x * (~allowed)) < 1e-13
            e = entropy(x)
            score = 0.0
            for a in range(r):
                for i in range(1, n + 1):
                    y = erase(x, d, r * n, range(a * n, a * n + i))
                    score += math.log(d) * float(np.vdot(y, y).real)
            c_d = 2 - math.log(2)
            rhs = score - r * c_d - r * math.log(2)
            min_witness_slack = min(min_witness_slack, e - rhs)
            assert e + 1e-11 >= rhs
            max_nonnormality = max(max_nonnormality,
                                  float(np.linalg.norm(x @ x.conj().T
                                                       - x.conj().T @ x)))
            graph_cases += 1

    return {"status": "PASS", "scope": "finite admission, not universal proof",
            "stock_cases": stock_cases,
            "max_stock_probability_identity_error": max_stock_error,
            "graph_cases": graph_cases,
            "minimum_graph_witness_slack": min_witness_slack,
            "maximum_tested_nonnormality_HS": max_nonnormality,
            "exact_structural_admissions": exact_obstructions,
            "wall_seconds": time.perf_counter() - wall_start,
            "process_cpu_seconds": time.process_time() - cpu_start,
            "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "total_discovery_cost": "UNKNOWN"}


if __name__ == "__main__":
    result = run()
    out = Path(__file__).with_name("RESULT.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

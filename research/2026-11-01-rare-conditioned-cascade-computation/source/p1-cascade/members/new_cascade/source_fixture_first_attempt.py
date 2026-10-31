"""Synthetic sources used only to exercise the clamped-experiment interface.

Ground truth lives here and is accessed by the test harness for evaluation.
The learner receives only experiment(), declared bounds, n, and the degree cap.
Aggregate binomial draws stand for m independent resets.  They are not actual
laboratory experiments, and their full represented cost must be reported.
"""
from __future__ import annotations
import math
import numpy as np


class ClampSource:
    def __init__(self, parents, tables, seed=90210, shapes=None):
        self.parents = [tuple(p) for p in parents]
        self.tables = [np.asarray(t, float) for t in tables]
        self.n = len(parents)
        self.shapes = np.ones(self.n) if shapes is None else np.asarray(shapes, float)
        self.rng = np.random.default_rng(seed)

    def truth_rate(self, v, mask):
        code = sum(int(bool(mask & (1 << u))) << j for j, u in enumerate(self.parents[v]))
        return float(self.tables[v][code])

    def experiment(self, v, mask, duration, resets):
        a = self.truth_rate(v, mask)
        probability = -math.expm1(-(a * duration) ** float(self.shapes[v]))
        return int(self.rng.binomial(int(resets), probability))


def scrambled_chain(n=8, rho=0.01, seed=771):
    rng = np.random.default_rng(seed)
    permutation = list(map(int, rng.permutation(n)))
    parents = [[] for _ in range(n)]
    tables = [None] * n
    tables[permutation[0]] = [0.7]
    for j in range(1, n):
        v = permutation[j]
        parents[v] = [permutation[j - 1]]
        tables[v] = [0.1 + 0.01 * j, 1.5 + 0.15 * j]
    # A real but unresolved extra influence.  Exact support recovery is neither
    # possible nor needed at a finite chosen resolution.
    v = permutation[-1]
    parents[v].append(permutation[0])
    weak = math.exp(rho / 8)
    tables[v] = [tables[v][0], tables[v][1], tables[v][0] * weak, tables[v][1] * weak]
    return ClampSource(parents, tables, seed=seed + 1), permutation


def or_cycle(seed=772, shapes=None):
    # Top-context marginal checks fail: either parent alone produces the boost.
    return ClampSource([(1, 2), (2,), (0,)],
                       [[0.2, 1.4, 1.4, 1.4], [0.4, 1.1], [0.3, 1.8]],
                       seed=seed, shapes=shapes)


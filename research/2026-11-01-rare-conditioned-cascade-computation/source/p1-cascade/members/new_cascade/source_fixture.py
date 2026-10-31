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
    def __init__(self, parents, tables, seed=90210, shapes=None, dense_beta=0.0):
        self.latent_parents = [tuple(p) for p in parents]
        self.tables = [np.asarray(t, float) for t in tables]
        self.n = len(parents)
        self.dense_beta = dense_beta
        self.parents = ([tuple(u for u in range(self.n) if u != v) for v in range(self.n)]
                        if dense_beta else self.latent_parents)
        self.shapes = np.ones(self.n) if shapes is None else np.asarray(shapes, float)
        self.rng = np.random.default_rng(seed)

    def truth_rate(self, v, mask):
        code = sum(int(bool(mask & (1 << u))) << j for j, u in enumerate(self.latent_parents[v]))
        count = (mask & ~(1 << v)).bit_count()
        return float(self.tables[v][code]) * math.exp(self.dense_beta * count / max(1, self.n - 1))

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
    # Every node now genuinely depends on every other node.  The exact graph
    # is complete; the learner is not given the nearby sparse graph.
    return ClampSource(parents, tables, seed=seed + 1, dense_beta=rho / 256), permutation


def or_cycle(seed=772, shapes=None):
    # Top-context marginal checks fail: either parent alone produces the boost.
    return ClampSource([(1, 2), (2,), (0,)],
                       [[0.2, 1.4, 1.4, 1.4], [0.4, 1.1], [0.3, 1.8]],
                       seed=seed, shapes=shapes)


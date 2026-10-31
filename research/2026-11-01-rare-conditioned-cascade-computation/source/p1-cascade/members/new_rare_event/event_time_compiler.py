"""Positive event-time compiler for attractive irreversible CTMCs.

This is a floating-point research implementation.  The mathematical error
bounds are proved separately; this program is not an interval-arithmetic or
finite-random-bit implementation.  It does not query a committor or enumerate
the 2**n state space in the compiler.  The optional small-system reference
calculator does enumerate that state space and is used only for comparison.

Dependencies: Python 3, numpy, scipy.
"""
from __future__ import annotations

from dataclasses import dataclass
import itertools
import math
from typing import Iterable

import numpy as np
from scipy.special import logsumexp


@dataclass(frozen=True)
class LocalRate:
    parents: tuple[int, ...]
    table: np.ndarray

    def __post_init__(self):
        table = np.asarray(self.table, dtype=float)
        if table.shape != (1 << len(self.parents),):
            raise ValueError("Rate table has the wrong length")
        if np.any(table < 0) or np.any(~np.isfinite(table)):
            raise ValueError("Rates must be finite and nonnegative")
        if len(set(self.parents)) != len(self.parents):
            raise ValueError("Repeated parent")
        for code in range(len(table)):
            for bit in range(len(self.parents)):
                if not (code & (1 << bit)):
                    if table[code | (1 << bit)] + 1e-14 < table[code]:
                        raise ValueError("Rate table is not attractive")
        object.__setattr__(self, "table", table)

    def at_state(self, state: np.ndarray) -> float:
        code = sum(int(state[p]) << k for k, p in enumerate(self.parents))
        return float(self.table[code])


@dataclass
class LogFactor:
    scope: tuple[int, ...]
    values: np.ndarray


def _aligned(factor: LogFactor, union: tuple[int, ...], q: int) -> np.ndarray:
    if not factor.scope:
        return np.asarray(factor.values).reshape((1,) * len(union))
    if tuple(sorted(factor.scope)) != factor.scope:
        raise ValueError("Factor scopes must be sorted")
    return factor.values.reshape(tuple(q if v in factor.scope else 1 for v in union))


def combine(factors: list[LogFactor], q: int) -> LogFactor:
    union = tuple(sorted(set().union(*(set(f.scope) for f in factors))))
    out = np.zeros((q,) * len(union), dtype=float)
    for factor in factors:
        out += _aligned(factor, union, q)
    return LogFactor(union, out)


def min_fill_order(scopes: Iterable[tuple[int, ...]], n: int) -> tuple[list[int], int]:
    """Construct and report an actual elimination order; no width oracle.

    This heuristic need not find optimal treewidth.  The measured returned
    width is the width actually used by this implementation.
    """
    graph = {v: set() for v in range(n)}
    for scope in scopes:
        for u, v in itertools.combinations(scope, 2):
            graph[u].add(v)
            graph[v].add(u)
    order, width = [], 0
    while graph:
        def key(v):
            neighbors = graph[v]
            fill = sum(b not in graph[a] for a, b in itertools.combinations(neighbors, 2))
            return fill, len(neighbors), v
        v = min(graph, key=key)
        neighbors = graph[v].copy()
        width = max(width, len(neighbors))
        for a, b in itertools.combinations(neighbors, 2):
            graph[a].add(b)
            graph[b].add(a)
        for a in neighbors:
            graph[a].remove(v)
        del graph[v]
        order.append(v)
    return order, width


@dataclass
class EliminationSampler:
    q: int
    n: int
    order: list[int]
    buckets: list[tuple[int, LogFactor]]
    log_probability: float
    width: int
    peak_entries: int

    def sample_assignment(self, rng: np.random.Generator) -> np.ndarray:
        assignment = np.full(self.n, -1, dtype=int)
        for v, bucket in reversed(self.buckets):
            index = tuple(slice(None) if u == v else int(assignment[u]) for u in bucket.scope)
            logits = np.asarray(bucket.values[index], dtype=float)
            normalizer = logsumexp(logits)
            if not np.isfinite(normalizer):
                raise RuntimeError("Backtracking entered a zero-probability separator")
            weights = np.exp(logits - normalizer)
            weights /= weights.sum()
            assignment[v] = int(rng.choice(self.q, p=weights))
        return assignment


def eliminate(factors: list[LogFactor], n: int, q: int,
              order: list[int] | None = None) -> EliminationSampler:
    if order is None:
        order, width = min_fill_order([f.scope for f in factors], n)
    else:
        if sorted(order) != list(range(n)):
            raise ValueError("Not an elimination permutation")
        width = 0
    live = list(factors)
    buckets = []
    peak_entries = 1
    for v in order:
        selected = [f for f in live if v in f.scope]
        live = [f for f in live if v not in f.scope]
        if not selected:
            selected = [LogFactor((v,), np.zeros(q))]
        joint = combine(selected, q)
        width = max(width, len(joint.scope) - 1)
        peak_entries = max(peak_entries, joint.values.size)
        buckets.append((v, joint))
        axis = joint.scope.index(v)
        remaining = tuple(u for u in joint.scope if u != v)
        marginal = logsumexp(joint.values, axis=axis)
        live.append(LogFactor(remaining, marginal))
    log_z = sum(float(f.values) for f in live)
    return EliminationSampler(q, n, list(order), buckets, log_z, width, peak_entries)


def make_event_time_factor(i: int, rate: LocalRate, n_bins: int, deadline: float) -> LogFactor:
    """Exact factor of the held-interaction process.

    A variable value z=0,...,N-1 means failure in time bin z; z=N means
    survival through the deadline.  Parents enter the rate only in bins
    strictly after their failure bin.  All arrays use log weights.
    """
    q = n_bins + 1
    dt = deadline / n_bins
    scope = tuple(sorted((i,) + rate.parents))
    shape = (q,) * len(scope)
    coordinates = np.ogrid[tuple(slice(0, q) for _ in scope)]
    own = coordinates[scope.index(i)]
    parent_bins = [coordinates[scope.index(p)] for p in rate.parents]
    # Integrate across epochs between parent updates.  Degree is the local
    # factor arity, not the number of global states or trajectory prefixes.
    # A vectorized sum over the at most 2**d parent configurations avoids an
    # additional N loop for every factor entry.
    cumulative = np.zeros(shape, dtype=float)
    current_code = np.zeros(shape, dtype=np.int64)
    for k, pb in enumerate(parent_bins):
        current_code += (pb < own).astype(np.int64) << k
    for code, lam in enumerate(rate.table):
        lower = np.zeros(shape, dtype=np.int64)
        upper = np.broadcast_to(own, shape).copy()
        for k, pb in enumerate(parent_bins):
            if code & (1 << k):
                lower = np.maximum(lower, pb + 1)
            else:
                upper = np.minimum(upper, pb + 1)
        count = np.maximum(upper - lower, 0)
        cumulative += dt * lam * count
    current_rate = rate.table[current_code]
    jump_log = np.full(shape, -np.inf, dtype=float)
    positive = current_rate > 0
    jump_log[positive] = np.log(-np.expm1(-dt * current_rate[positive]))
    values = -cumulative + np.where(own < n_bins, jump_log, 0.0)
    return LogFactor(scope, values)


def compile_model(rates: list[LocalRate], n_bins: int, deadline: float,
                  required: Iterable[int] | None = None) -> EliminationSampler:
    if n_bins < 1 or deadline <= 0:
        raise ValueError("Positive bin count and deadline required")
    n = len(rates)
    q = n_bins + 1
    required_set = set(range(n) if required is None else required)
    factors = [make_event_time_factor(i, rate, n_bins, deadline) for i, rate in enumerate(rates)]
    for i in required_set:
        mask = np.zeros(q)
        mask[-1] = -np.inf
        factors.append(LogFactor((i,), mask))
    return eliminate(factors, n, q)


def local_hazard_before(i: int, rate: LocalRate, bins: np.ndarray,
                        n_bins: int, deadline: float) -> tuple[float, float]:
    dt = deadline / n_bins
    own = int(bins[i])
    boundaries = sorted({0, own} | {int(bins[p]) + 1 for p in rate.parents
                                   if int(bins[p]) + 1 < own})
    hazard = 0.0
    for left, right in zip(boundaries, boundaries[1:]):
        code = sum(int(int(bins[p]) < left) << k for k, p in enumerate(rate.parents))
        hazard += dt * (right - left) * float(rate.table[code])
    code = sum(int(int(bins[p]) < own) << k for k, p in enumerate(rate.parents))
    return hazard, float(rate.table[code])


def thresholds_from_bins(rates: list[LocalRate], bins: np.ndarray,
                         n_bins: int, deadline: float,
                         rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Sample the original independent exponential drivers conditional on bins.

    This is the key pullback, not a replacement of a fine-time path by its
    discretized failure times.
    """
    dt = deadline / n_bins
    thresholds = np.empty(len(rates))
    held_times = np.full(len(rates), np.inf)
    for i, rate in enumerate(rates):
        before, lam = local_hazard_before(i, rate, bins, n_bins, deadline)
        z = int(bins[i])
        if z == n_bins:
            thresholds[i] = before + rng.exponential()
        else:
            if lam <= 0:
                raise RuntimeError("A zero-rate bin was sampled as a failure")
            increment = -np.log1p(-rng.random() * (-np.expm1(-lam * dt)))
            thresholds[i] = before + increment
            held_times[i] = z * dt + increment / lam
    return thresholds, held_times


def simulate_thresholds(rates: list[LocalRate], thresholds: np.ndarray) -> np.ndarray:
    """Undelayed CTMC from its exponential thresholds, at most n actual jumps."""
    n = len(rates)
    residual = np.array(thresholds, dtype=float, copy=True)
    failed = np.zeros(n, dtype=bool)
    times = np.full(n, np.inf)
    time = 0.0
    for _ in range(n):
        lambdas = np.array([0.0 if failed[i] else rate.at_state(failed)
                            for i, rate in enumerate(rates)])
        waits = np.divide(residual, lambdas, out=np.full(n, np.inf), where=lambdas > 0)
        waits[failed] = np.inf
        i = int(np.argmin(waits))
        duration = float(waits[i])
        if not np.isfinite(duration):
            break
        time += duration
        residual = np.maximum(0.0, residual - duration * lambdas)
        failed[i] = True
        times[i] = time
    return times


def sample_reactive(rates: list[LocalRate], compiler: EliminationSampler,
                    deadline: float, rng: np.random.Generator) -> dict:
    bins = compiler.sample_assignment(rng)
    thresholds, held_times = thresholds_from_bins(rates, bins, compiler.q - 1, deadline, rng)
    return {"bins": bins, "thresholds": thresholds, "held_times": held_times,
            "times": simulate_thresholds(rates, thresholds)}


def simulate_held_thresholds(rates: list[LocalRate], thresholds: np.ndarray,
                             step: float) -> np.ndarray:
    """Independent check of the delayed path coupling, skipping empty bins."""
    n = len(rates)
    residual = np.array(thresholds, dtype=float, copy=True)
    failed = np.zeros(n, dtype=bool)
    times = np.full(n, np.inf)
    bin_start = 0.0
    for _ in range(n):
        lambdas = np.array([0.0 if failed[i] else rate.at_state(failed)
                            for i, rate in enumerate(rates)])
        waits = np.divide(residual, lambdas, out=np.full(n, np.inf), where=lambdas > 0)
        waits[failed] = np.inf
        soonest = float(np.min(waits))
        if not np.isfinite(soonest):
            break
        skipped = max(0, int(np.floor(soonest / step)))
        if skipped:
            duration = skipped * step
            residual = np.maximum(0.0, residual - duration * lambdas)
            bin_start += duration
            waits = np.divide(residual, lambdas, out=np.full(n, np.inf), where=lambdas > 0)
            waits[failed] = np.inf
        now = (~failed) & (waits <= step * (1.0 + 1e-12))
        if not np.any(now):
            raise RuntimeError("Floating-point skip failed to locate next occupied bin")
        times[now] = bin_start + waits[now]
        residual = np.maximum(0.0, residual - step * lambdas)
        failed[now] = True
        bin_start += step
        if np.all(failed):
            break
    return times


def direct_held_probability(rates: list[LocalRate], n_bins: int, deadline: float,
                             required: Iterable[int] | None = None) -> float:
    """Exponential-state check, deliberately excluded from the compiler."""
    n = len(rates)
    required_mask = sum(1 << i for i in (range(n) if required is None else required))
    probabilities = np.zeros(1 << n)
    probabilities[0] = 1.0
    dt = deadline / n_bins
    for _ in range(n_bins):
        updated = np.zeros_like(probabilities)
        for state_code, weight in enumerate(probabilities):
            if weight == 0:
                continue
            state = np.array([bool(state_code & (1 << i)) for i in range(n)])
            alive = np.flatnonzero(~state)
            survival = np.array([np.exp(-rates[i].at_state(state) * dt) for i in alive])
            for outcome in range(1 << len(alive)):
                code, p = state_code, weight
                for k, i in enumerate(alive):
                    if outcome & (1 << k):
                        code |= 1 << int(i)
                        p *= 1.0 - survival[k]
                    else:
                        p *= survival[k]
                updated[code] += p
        probabilities = updated
    return float(sum(p for s, p in enumerate(probabilities) if s & required_mask == required_mask))


def exact_ctmc_probability(rates: list[LocalRate], deadline: float,
                           required: Iterable[int] | None = None) -> float:
    """Small-system positive uniformization reference, not the learned solver."""
    from scipy.sparse import csr_matrix
    from scipy.stats import poisson
    n = len(rates)
    required_set = set(range(n) if required is None else required)
    required_mask = sum(1 << i for i in required_set)
    rows, cols, data = [], [], []
    totals = np.zeros(1 << n)
    for code in range(1 << n):
        state = np.array([bool(code & (1 << i)) for i in range(n)])
        for i, rate in enumerate(rates):
            if not state[i]:
                lam = rate.at_state(state)
                rows.append(code)
                cols.append(code | (1 << i))
                data.append(lam)
                totals[code] += lam
    bound = float(np.max(totals))
    if bound == 0:
        return float(not required_set)
    rows.extend(range(1 << n))
    cols.extend(range(1 << n))
    data.extend((bound - totals).tolist())
    transition = csr_matrix((np.array(data) / bound, (rows, cols)), shape=(1 << n, 1 << n))
    lam = bound * deadline
    if lam > 500:
        raise ValueError("Reference uniformization restricted to moderate Poisson mean")
    target = np.array([code & required_mask == required_mask for code in range(1 << n)])
    log_lower = sum(math.log(-math.expm1(-rates[i].table[0] * deadline)) for i in required_set)
    cutoff = n
    while poisson.logsf(cutoff, lam) > log_lower + math.log(1e-13):
        cutoff += 1
    vector = np.zeros(1 << n)
    vector[0] = 1.0
    poisson_weight = math.exp(-lam)
    answer = poisson_weight * float(vector[target].sum())
    for count in range(1, cutoff + 1):
        vector = transition.T @ vector
        poisson_weight *= lam / count
        answer += poisson_weight * float(vector[target].sum())
    return float(answer)

"""Optional Weibull exposure-threshold extension of event_time_compiler.

The exponential implementation remains in its original module.  Here each
node has an independent known Weibull threshold, and cumulative exposure
is integrated using an attractive local rate table.  The state process is
generally not Markov.  All numerical caveats of the original module apply.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from event_time_compiler import (
    LocalRate, LogFactor, EliminationSampler, eliminate, local_hazard_before,
    simulate_thresholds,
)


@dataclass(frozen=True)
class WeibullThreshold:
    shape: float
    scale: float = 1.0

    def __post_init__(self):
        if self.shape < 1 or self.scale <= 0:
            raise ValueError("This theorem uses Weibull shape >=1 and scale >0")

    @property
    def scaling_dimension(self) -> float:
        return self.shape

    def log_survival(self, exposure):
        return -(np.asarray(exposure) / self.scale) ** self.shape

    def log_density(self, exposure):
        exposure = np.asarray(exposure)
        with np.errstate(divide="ignore", invalid="ignore"):
            return (np.log(self.shape / self.scale)
                    + (self.shape - 1) * np.log(exposure / self.scale)
                    - (exposure / self.scale) ** self.shape)

    def log_interval_mass(self, lower, increment):
        lower, increment = np.broadcast_arrays(lower, increment)
        u = (lower / self.scale) ** self.shape
        difference = np.zeros_like(u)
        positive = lower > 0
        difference[positive] = (u[positive] * np.expm1(
            self.shape * np.log1p(increment[positive] / lower[positive])))
        difference[~positive] = (increment[~positive] / self.scale) ** self.shape
        with np.errstate(divide="ignore"):
            return -u + np.log(-np.expm1(-difference))

    def sample(self, rng: np.random.Generator, size=None):
        return self.scale * rng.exponential(size=size) ** (1 / self.shape)

    def sample_interval(self, lower: float, increment: float | None,
                        rng: np.random.Generator) -> float:
        u = (lower / self.scale) ** self.shape
        if increment is None:
            y = u + rng.exponential()
        else:
            if lower > 0:
                difference = u * np.expm1(self.shape * np.log1p(increment / lower))
            else:
                difference = (increment / self.scale) ** self.shape
            y = u - np.log1p(-rng.random() * (-np.expm1(-difference)))
        return float(self.scale * y ** (1 / self.shape))


def make_threshold_factor(i: int, rate: LocalRate, clock: WeibullThreshold,
                          n_bins: int, deadline: float) -> LogFactor:
    q = n_bins + 1
    dt = deadline / n_bins
    scope = tuple(sorted((i,) + rate.parents))
    shape = (q,) * len(scope)
    coordinates = np.ogrid[tuple(slice(0, q) for _ in scope)]
    own = coordinates[scope.index(i)]
    parent_bins = [coordinates[scope.index(p)] for p in rate.parents]
    cumulative = np.zeros(shape, dtype=float)
    current_code = np.zeros(shape, dtype=np.int64)
    for k, pb in enumerate(parent_bins):
        current_code += (pb < own).astype(np.int64) << k
    for code, value in enumerate(rate.table):
        lower = np.zeros(shape, dtype=np.int64)
        upper = np.broadcast_to(own, shape).copy()
        for k, pb in enumerate(parent_bins):
            if code & (1 << k):
                lower = np.maximum(lower, pb + 1)
            else:
                upper = np.minimum(upper, pb + 1)
        cumulative += dt * value * np.maximum(upper - lower, 0)
    current_rate = rate.table[current_code]
    failure = clock.log_interval_mass(cumulative, dt * current_rate)
    survival = clock.log_survival(cumulative)
    values = np.where(own < n_bins, failure, survival)
    return LogFactor(scope, values)


def compile_aging_model(rates: list[LocalRate], clocks: list[WeibullThreshold],
                        n_bins: int, deadline: float,
                        required: Iterable[int] | None = None) -> EliminationSampler:
    n = len(rates)
    if len(clocks) != n:
        raise ValueError("One independent threshold law is required per node")
    q = n_bins + 1
    factors = [make_threshold_factor(i, rate, clocks[i], n_bins, deadline)
               for i, rate in enumerate(rates)]
    for i in set(range(n) if required is None else required):
        mask = np.zeros(q)
        mask[-1] = -np.inf
        factors.append(LogFactor((i,), mask))
    return eliminate(factors, n, q)


def sample_aging_reactive(rates: list[LocalRate], clocks: list[WeibullThreshold],
                          compiler: EliminationSampler, deadline: float,
                          rng: np.random.Generator) -> dict:
    bins = compiler.sample_assignment(rng)
    n_bins = compiler.q - 1
    dt = deadline / n_bins
    thresholds = np.empty(len(rates))
    held_times = np.full(len(rates), np.inf)
    for i, rate in enumerate(rates):
        before, value = local_hazard_before(i, rate, bins, n_bins, deadline)
        if bins[i] == n_bins:
            thresholds[i] = clocks[i].sample_interval(before, None, rng)
        else:
            thresholds[i] = clocks[i].sample_interval(before, dt * value, rng)
            held_times[i] = bins[i] * dt + (thresholds[i] - before) / value
    return {"bins": bins, "thresholds": thresholds, "held_times": held_times,
            "times": simulate_thresholds(rates, thresholds)}


def completed_path_log_density(rates: list[LocalRate], clocks: list[WeibullThreshold],
                                times: np.ndarray) -> float:
    """Evaluate the completed-path density on its fixed failure-order cone."""
    n = len(rates)
    if len(clocks) != n or np.any(~np.isfinite(times)):
        raise ValueError("Finite completed path required")
    total = 0.0
    for i, rate in enumerate(rates):
        stop = float(times[i])
        boundaries = sorted({0.0, stop} | {float(times[p]) for p in rate.parents
                                           if times[p] < stop})
        exposure = 0.0
        for left, right in zip(boundaries, boundaries[1:]):
            state = times <= left
            exposure += rate.at_state(state) * (right - left)
        rate_at_jump = rate.at_state(times < stop)
        total += np.log(rate_at_jump) + float(clocks[i].log_density(exposure))
    return total

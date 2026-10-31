"""Acquire monotone local exposure rates using noisy, clamped bit experiments.

The learner receives n, a degree bound, positive rate bounds, and a callable
experiment(v, state_mask, duration, number_of_resets).  The callable returns
only a binomial count.  No graph, local table, trajectory solver, or conditional
sampler is passed to the learner.

Statistical theorem: PROOF.txt.  This program uses ordinary floating arithmetic
and aggregate simulated binomial counts; it is not a validated interval code.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Callable

import numpy as np


@dataclass
class Observation:
    node: int
    mask: int
    duration: float
    trials: int
    failures: int
    phase: str


class RateAssay:
    """An explicit finite-bit observation protocol, with all resets charged.

    For a known Weibull threshold shape k, a clamped exposure a and duration t
    have success probability 1-exp(-(a*t)**k).  k=1 is the CTMC case.
    Shape is a declared noise-law contract; it is not inferred by this code.
    """

    def __init__(self, experiment: Callable, n: int, degree: int,
                 lower: float, upper: float, rho: float, delta: float,
                 shapes=None):
        if not (0 < lower <= upper and 0 < rho <= 1 and 0 < delta < 1):
            raise ValueError("Invalid bounds")
        self.experiment = experiment
        self.n, self.degree = n, degree
        self.lower, self.upper = lower, upper
        self.rho, self.delta = rho, delta
        self.shapes = np.ones(n) if shapes is None else np.asarray(shapes, float)
        if len(self.shapes) != n or np.any(self.shapes < 1):
            raise ValueError("Known Weibull shapes must be >=1")
        self.D = max(1, degree)
        self.a = rho / (64 * self.D)
        ell = max(1, math.ceil(math.log2(max(2, n - 1))))
        # Safe deterministic cap for the adaptive junta discovery protocol.
        self.max_calls = n * (2 ** (degree + 3) + 8 * self.D**2 * (ell + 1))
        self.stages = math.ceil(math.log2(upper / lower)) + 1
        self.cache: dict[tuple[int, int], float] = {}
        self.observations: list[Observation] = []
        self.trials = 0
        self.exposure_time = 0.0
        self.assays = 0

    def _shots(self, v, mask, t, m, phase):
        m = int(m)
        count = int(self.experiment(v, mask, float(t), m))
        if not 0 <= count <= m:
            raise RuntimeError("Invalid experiment count")
        self.observations.append(Observation(v, mask, float(t), m, count, phase))
        self.trials += m
        self.exposure_time += m * t
        return count / m

    def log_rate(self, v: int, mask: int) -> float:
        mask &= ~(1 << v)
        key = v, mask
        if key in self.cache:
            return self.cache[key]
        if self.assays >= self.max_calls:
            raise RuntimeError("Declared acquisition cap exhausted")
        self.assays += 1
        k = float(self.shapes[v])
        # Coarse probability accuracy 1/16.  This rational ratio has Weibull
        # dose growth at most exp(1/4)<2.  Thus the mathematical protocol does
        # not demand an exactly realized irrational exposure duration.
        exposure_ratio = 1 + 1 / (4 * math.ceil(k))
        jmax = math.ceil(math.log(self.upper / self.lower) / math.log(exposure_ratio)) + 1
        m0 = math.ceil(128 * math.log(4 * self.max_calls * (jmax + 1) / self.delta))
        t = 1 / self.upper
        for j in range(jmax + 1):
            p = self._shots(v, mask, t, m0, "bracket")
            if p >= 0.25:
                break
            t *= exposure_ratio
        else:
            raise RuntimeError("Rate bracketing failed")
        # On the bracketing confidence event the true probability lies between
        # 3/16 and 1-e^-1.  The log-rate inverse has derivative <=9/k on
        # [1/8,3/4].  Choosing b<=k*a/32 leaves numerical slack.
        b = min(1 / 64, k * self.a / 32)
        m1 = math.ceil(math.log(4 * self.max_calls / self.delta) / (2 * b * b))
        p = self._shots(v, mask, t, m1, "estimate")
        if not 0 < p < 1:
            raise RuntimeError("Extreme final estimate; confidence failed")
        h = math.log(-math.log1p(-p)) / k - math.log(t)
        self.cache[key] = h
        return h

    def summary(self):
        return {
            "distinct_configuration_assays": self.assays,
            "assay_cap": self.max_calls,
            "represented_independent_resets": self.trials,
            "represented_total_exposure_time": self.exposure_time,
            "configuration_calls_including_repetitions": len(self.observations),
            "log_rate_confidence_radius": self.a,
            "failure_probability_budget": self.delta,
            "precision_status": "ordinary floating simulation, not interval certification",
        }


def learn_local_scopes(assay: RateAssay):
    """Return parent subsets and one-sided monotone tables.

    All discovered parents have a witnessed nonzero true effect on the
    simultaneous confidence event.  There is no minimum-edge-strength
    assumption: weak undiscovered effects are enclosed uniformly.
    """
    n, d, rho, a = assay.n, assay.degree, assay.rho, assay.a
    result = []
    witnesses = []
    all_bits = (1 << n) - 1
    split_threshold = rho / (8 * max(1, d))

    for v in range(n):
        parents = []
        while True:
            parent_mask = sum(1 << u for u in parents)
            unknown = [u for u in range(n) if u != v and u not in parents]
            unknown_mask = all_bits & ~(parent_mask | (1 << v))
            trigger = None
            lows = []
            for local in range(1 << len(parents)):
                base = sum((1 << u) for j, u in enumerate(parents) if local & (1 << j))
                lo = assay.log_rate(v, base)
                hi = assay.log_rate(v, base | unknown_mask)
                lows.append(lo)
                if hi - lo > rho / 2:
                    trigger = base, lo, hi
                    break
            if trigger is None:
                # Maximal isotone minorant of the simultaneous lower bounds.
                log_table = np.asarray(lows) - a
                for bit in range(len(parents)):
                    for code in range(len(log_table)):
                        if code & (1 << bit):
                            log_table[code] = max(log_table[code], log_table[code ^ (1 << bit)])
                result.append({"parents": tuple(parents), "table": np.exp(log_table)})
                break
            if len(parents) >= d:
                raise RuntimeError("Degree promise or confidence event failed")
            base, _, _ = trigger
            # Monotone chain over unknown coordinates.  Positive differences
            # occur at at most d locations.  Search every significant interval;
            # selecting just the larger child can lose a weak witness.
            prefix = [base]
            for u in unknown:
                prefix.append(prefix[-1] | (1 << u))

            def find_effect(left, right):
                hl = assay.log_rate(v, prefix[left])
                hr = assay.log_rate(v, prefix[right])
                if hr - hl <= split_threshold:
                    return None
                if right == left + 1:
                    return unknown[left], prefix[left], hr - hl
                mid = (left + right) // 2
                hit = find_effect(left, mid)
                return hit if hit is not None else find_effect(mid, right)

            hit = find_effect(0, len(unknown))
            if hit is None:
                raise RuntimeError("A significant corner gap had no relevant-coordinate witness")
            u, context, observed_gap = hit
            parents.append(u)
            witnesses.append({"node": v, "parent": u, "context": context,
                              "observed_log_gap": observed_gap,
                              "positive_gap_lower_bound": observed_gap - 2 * a})
    return result, witnesses


def json_model(model):
    return [{"parents": list(item["parents"]), "table": item["table"].tolist()}
            for item in model]


def acquire_unknown_degree(experiment, n, lower, upper, rho, delta, shapes=None):
    """Discover the useful scope bound as well; charge failed smaller attempts.

    A returned certificate remains sound under the confidence event even if
    there is no nearby sparse model.  Approximate sparse locality proves a
    cost bound and successful completion, not correctness of a stopped model.
    """
    attempts = []
    for degree in range(n):
        assay = RateAssay(experiment, n, degree, lower, upper, rho,
                          delta / ((degree + 1) * (degree + 2)), shapes=shapes)
        try:
            model, witnesses = learn_local_scopes(assay)
        except RuntimeError as exc:
            attempts.append({"degree": degree, "status": "incomplete",
                             "reason": str(exc), "calibration": assay.summary()})
            continue
        attempts.append({"degree": degree, "status": "completed",
                         "calibration": assay.summary()})
        return model, witnesses, assay, attempts
    raise RuntimeError("No complete acquired model within n-1 parent scopes")


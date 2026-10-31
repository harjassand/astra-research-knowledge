"""Floating-point value-iteration diagnostic for the recovery-chain SSP.

The known-key value is independent of each known bit's identity.  A mask is
therefore a sufficient Bayesian model state.  For an unknown key, a button
trial succeeds with probability 1/2 and identifies the key in either case.
Root recovery is already known because both buttons return to the root.
The finite Bayesian state model is exact, but the solver uses NumPy floating
point and stops when successive iterates differ by less than 1e-11.  That
stopping residual is not a certified error bound on the optimal value.  This
is a numerical diagnostic, not an exact rational solve or proof certificate;
the analytic potential proof establishes the theorem independently.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

import numpy as np


def optimal_access(h: int, p: float = 0.5, targets: int = 1):
    m = 1 << max(h - 1, 0)
    # Columns g0,...,gH, f0,...,f(H-1).
    n = 2 * h + 1
    root_prior = np.zeros(m)
    values = None
    residual = math.inf
    iterations = 0
    for _ in range(targets):
        values = np.zeros((m, n))
        values[:, h] = 1 + root_prior
        for iterations in range(100000):
            prev = values.copy()
            for mask in range(m):
                for i in range(h):
                    f = h + 1 + i
                    forward = 1 + p * prev[mask, i + 1] + (1 - p) * prev[mask, f]
                    probe = 1 + prev[mask, f]
                    reset = 1 + prev[mask, 0]
                    values[mask, i] = min(forward, probe, reset)
                    if i == 0 or (mask & (1 << (i - 1))):
                        recover = 1 + prev[mask, i]
                    else:
                        learned_mask = mask | (1 << (i - 1))
                        recover = 1 + 0.5 * prev[learned_mask, i] + 0.5 * prev[learned_mask, 0]
                    values[mask, f] = min(recover, reset)
            residual = float(np.max(np.abs(values - prev)))
            if residual < 1e-11:
                break
        else:
            raise RuntimeError("SSP value iteration did not converge")
        root_prior = values[:, 0].copy()
    tau = (2 - p) / p
    acquired = h * tau + 2 * max(h - 1, 0) + tau * h * (h - 1) / 4
    lower = tau * (h + (1 - p) * h * (h - 1) / 4) + 1 + (targets - 1) * (h * tau + 1)
    upper = acquired + 1 + (targets - 1) * (h * tau + 1)
    approximate = float(values[0, 0])
    full_known = float(values[-1, 0])
    assert lower <= approximate + 1e-7, (h, lower, approximate)
    assert approximate <= upper + 1e-7, (h, approximate, upper)
    assert abs(full_known - targets * (h * tau + 1)) < 1e-7
    return dict(h=h, p=p, targets=targets, lower_bound=lower,
                optimal_bayes_total=approximate, explicit_acquisition_upper=upper,
                fully_known_total=full_known, residual=residual, iterations=iterations+1)


def sample_acquisition(h: int, p: float, rng: random.Random):
    """Sample the exact acquisition ledger using geometric layer costs."""
    def advance():
        c = 1
        while rng.random() >= p:
            c += 2  # one local recovery then another forward attempt
        return c

    total = 0
    for i in range(h):
        if i > 0:
            total += 2  # physical PROBE and one recovery-button test
            if rng.random() < 0.5:
                total += sum(advance() for _ in range(i))
        total += advance()
    return total


def main():
    rows = [optimal_access(h, p, targets=t)
            for p in (0.25, 0.5, 0.75)
            for h in range(1, 7)
            for t in (1, 3)]
    rng = random.Random(93417)
    mc = []
    for h in (2, 5, 12):
        p = 0.5
        values = np.array([sample_acquisition(h, p, rng) for _ in range(30000)])
        tau = (2 - p) / p
        theory = h * tau + 2 * (h - 1) + tau * h * (h - 1) / 4
        mc.append(dict(h=h, sample_mean=float(values.mean()),
                       theoretical_mean=theory, standard_error=float(values.std(ddof=1)/math.sqrt(len(values)))))
    result = dict(
        diagnostic_method={
            "solver": "NumPy floating-point value iteration on an exact finite Bayesian state model",
            "stopping_rule": "maximum absolute change between successive iterates < 1e-11",
            "certified_optimal_value_error_bound": False,
            "optimal_bayes_total_field": "approximate value-iteration estimate, not an exact or certified value",
            "proof_status": "analytic bounds are proved separately; these computations are diagnostic only",
        },
        floating_point_ssp_checks=rows,
        acquisition_monte_carlo=mc,
    )
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result, indent=2))
    print(json.dumps({"checks": len(rows), "monte_carlo": mc,
                      "p_half_h_six": [x for x in rows if x["p"] == 0.5 and x["h"] == 6]}, indent=2))


if __name__ == "__main__":
    main()

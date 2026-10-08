#!/usr/bin/env python3
"""Small planning calculator for the matched cell-associated clone-odds assay.

Inputs are independent marker opportunities and molecule-weighted marker fraction.
The calculation does not convert a VAF/marker fraction into cell fraction when
copy number is unknown, and it does not model overdispersion or background calls.
"""

from __future__ import annotations

import argparse
import math
from statistics import NormalDist


def logistic_odds_shift(p: float, beta: float) -> float:
    """Return p after a log-odds shift beta."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be strictly between zero and one")
    logit = math.log(p) - math.log1p(-p)
    shifted = logit + beta
    return 1.0 / (1.0 + math.exp(-shifted))


def approximate_opportunities_per_arm(p: float, beta: float,
                                      alpha: float = 0.05,
                                      power: float = 0.80) -> float:
    """Local two-sample log-odds design approximation.

    Uses Var(log-odds difference) ~= 2/(M p) for low p and small beta.
    The normal quantiles are kept as standard constants for the default design.
    """
    if not 0.0 < p < 1.0 or beta == 0.0:
        raise ValueError("p must be in (0,1) and beta must be nonzero")
    z_alpha = NormalDist().inv_cdf(1.0 - alpha / 2.0)
    z_power = NormalDist().inv_cdf(power)
    return 2.0 * (z_alpha + z_power) ** 2 / (p * beta * beta)


def opportunities_for_any_molecule(p: float, target: float = 0.95) -> int:
    """Exact binomial opportunity count for P(at least one) >= target."""
    if not 0.0 < p < 1.0 or not 0.0 < target < 1.0:
        raise ValueError("p and target must be strictly between zero and one")
    return math.ceil(math.log1p(-target) / math.log1p(-p))


def zero_probability(molecules: int, p: float) -> float:
    """Probability of a zero count under independent Bernoulli opportunities."""
    if molecules < 0 or not 0.0 <= p <= 1.0:
        raise ValueError("molecules must be nonnegative and p in [0,1]")
    return math.exp(molecules * math.log1p(-p)) if p < 1.0 else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=float, default=1e-2,
                        help="molecule-weighted marker fraction")
    parser.add_argument("--beta", type=float, default=0.4,
                        help="target treatment log-odds shift")
    parser.add_argument("--clinical-input", type=int, default=5531,
                        help="comparison input for zero-count probability")
    args = parser.parse_args()

    p1 = logistic_odds_shift(args.p, args.beta)
    m = approximate_opportunities_per_arm(args.p, args.beta)
    print(f"baseline marker fraction p={args.p:.8g}")
    print(f"shifted marker fraction={p1:.8g}")
    print(f"approx independent opportunities per arm={m:.1f}")
    print(f"input for 95% chance of >=1 molecule={opportunities_for_any_molecule(args.p)}")
    print(f"P(zero | input={args.clinical_input})={zero_probability(args.clinical_input, args.p):.6g}")


if __name__ == "__main__":
    main()

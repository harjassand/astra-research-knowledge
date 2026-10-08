#!/usr/bin/env python3
"""Exact one-type branching counterexample for clustered resistance events.

All biology-specific probabilities below are explicitly hypothetical. This is
an executable identifiability counterexample, not a fit to a cancer dataset.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class BranchingInputs:
    divide_rate: float
    death_rate: float
    resistance_event_per_division: float
    establishment_probability: float
    founders: int


def one_founder_escape_probability(x: BranchingInputs) -> float:
    """Return P(eventual established resistance) from one persister founder.

    A persister dies at rate d or divides at rate b. At each division, with
    probability u it produces one resistant daughter and one persister
    daughter; the resistant daughter establishes with probability q. Otherwise
    it produces two persister daughters. A failed resistant daughter leaves
    the persister daughter unaffected. Independent branching is assumed.

    The no-escape probability p solves
      p = [d + b ((1-u) p^2 + u (1-q) p)] / (b+d).
    The returned value is the corresponding root y=1-p in [0,1].
    """
    b, d, u, q = (
        x.divide_rate,
        x.death_rate,
        x.resistance_event_per_division,
        x.establishment_probability,
    )
    if b < 0 or d <= 0 or not (0 <= u <= 1) or not (0 <= q <= 1):
        raise ValueError("rates must be nonnegative, d positive, and u,q in [0,1]")
    if b + d == 0:
        raise ValueError("at least one of division or death rates must be positive")
    if b == 0 or u == 0 or q == 0:
        return 0.0

    # Substituting y=1-p gives a y^2 + A y - C = 0, with the positive root
    # evaluated in a numerically stable form.
    a = b * (1.0 - u)
    A = d - b + b * u * (1.0 + q)
    C = b * u * q
    if a == 0.0:
        # u=1: the equation is linear, A y = C; A is positive for d>0.
        return min(1.0, max(0.0, C / A))
    disc = A * A + 4.0 * a * C
    y = 2.0 * C / (A + math.sqrt(disc))
    return min(1.0, max(0.0, y))


def population_escape_probability(x: BranchingInputs) -> float:
    """Risk of at least one established resistant lineage from x.founders."""
    if x.founders < 0:
        raise ValueError("founders must be a nonnegative integer")
    y = one_founder_escape_probability(x)
    return -math.expm1(x.founders * math.log1p(-y)) if y < 1 else 1.0


def divisions_for_95pct_detection(u: float, q: float) -> int:
    """Fixed-exposure count for >=95% chance of >=1 established event.

    This is a sampling lower bound under independent Bernoulli event trials;
    it is separate from the random-exposure branching calculation above.
    """
    if not (0 < u <= 1) or not (0 < q <= 1):
        raise ValueError("u and q must be in (0,1]")
    success = u * q
    return math.ceil(math.log(0.05) / math.log1p(-success))


def main() -> None:
    burst_rate = 0.20
    per_locus_marginal = 0.01
    q = 0.80
    founders = 1000
    common = dict(divide_rate=0.10, death_rate=0.20, establishment_probability=q, founders=founders)

    # Both event laws have the same per-locus marginal (1%) and the same
    # expected total single-nucleotide burden (2%) conditional on a burst.
    pair_prob_clustered = per_locus_marginal
    pair_prob_independent = per_locus_marginal**2
    rows = [
        ("clustered", burst_rate * pair_prob_clustered),
        ("independent", burst_rate * pair_prob_independent),
    ]

    risks: dict[str, float] = {}
    for name, u in rows:
        x = BranchingInputs(resistance_event_per_division=u, **common)
        one = one_founder_escape_probability(x)
        risk = population_escape_probability(x)
        risks[name] = risk
        print(
            f"{name}: u={u:.8g}, one_founder_risk={one:.12g}, "
            f"risk_{founders}_founders={risk:.12g}, "
            f"divisions_for_95pct_established_event={divisions_for_95pct_detection(u, q)}"
        )

    print(f"risk_ratio_clustered_over_independent={risks['clustered'] / risks['independent']:.8g}")


if __name__ == "__main__":
    main()

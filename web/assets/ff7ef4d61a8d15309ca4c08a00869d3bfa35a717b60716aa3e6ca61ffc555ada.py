#!/usr/bin/env python3
"""Costed finite-population comparison of uniform and stratified FOV sampling.

Each stratum h contains M_h distinct, equal-cost FOV locations, K_h of which
would yield a detectable target-positive call under one fixed resolution,
exposure, spectral panel, and analysis threshold. Sampling is without
replacement. The scout/calibration cost is charged separately from confirmatory
high-resolution fields.

This is a transparent design calculation, not a biological data model.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb


def miss_fraction(population: int, positives: int, draws: int) -> Fraction:
    """Exact miss probability under simple random sampling without replacement."""
    if not (0 <= positives <= population):
        raise ValueError("positives must lie between zero and population")
    if not (0 <= draws <= population):
        raise ValueError("draws must lie between zero and population")
    if draws > population - positives:
        return Fraction(0, 1)
    return Fraction(comb(population - positives, draws), comb(population, draws))


@dataclass(frozen=True)
class Stratum:
    name: str
    population: int
    detectable_positive: int
    field_cost: int = 1


def miss_probability(strata: list[Stratum], allocation: list[int]) -> Fraction:
    if len(strata) != len(allocation):
        raise ValueError("one allocation count is required per stratum")
    result = Fraction(1, 1)
    for stratum, draws in zip(strata, allocation):
        result *= miss_fraction(stratum.population, stratum.detectable_positive, draws)
    return result


def best_allocation(
    strata: list[Stratum], field_budget: int, min_per_stratum: int = 0
) -> tuple[list[int], Fraction]:
    """Exhaustive integer allocation for a small number of strata.

    The objective is exact probability of at least one detectable hit, under
    independent simple-random samples within strata. Dynamic programming can
    replace this enumerator for many strata or large budgets.
    """
    if min_per_stratum < 0:
        raise ValueError("min_per_stratum must be nonnegative")
    if any(s.field_cost <= 0 for s in strata):
        raise ValueError("field costs must be positive")
    if min_per_stratum and any(s.population < min_per_stratum for s in strata):
        raise ValueError("a stratum is too small for its minimum allocation")

    best: tuple[Fraction, list[int]] | None = None

    def visit(i: int, remaining: int, prefix: list[int]) -> None:
        nonlocal best
        if i == len(strata):
            if remaining != 0:
                return
            miss = miss_probability(strata, prefix)
            if best is None or miss < best[0]:
                best = (miss, prefix.copy())
            return

        s = strata[i]
        lo = min_per_stratum
        hi = min(s.population, remaining // s.field_cost)
        for n in range(lo, hi + 1):
            visit(i + 1, remaining - n * s.field_cost, prefix + [n])

    visit(0, field_budget, [])
    if best is None:
        raise ValueError("field budget cannot satisfy allocation constraints exactly")
    return best[1], best[0]


def fmt_probability(value: Fraction) -> str:
    return f"{float(value):.6f}"


def main() -> None:
    # Illustrative calibration: 1,000 equal-cost candidate FOVs. A validated
    # coarse proxy partitions them into a 100-FOV high-risk stratum and a
    # 900-FOV lower-risk stratum. Positive counts refer to FOVs detectable by
    # the specified high-resolution assay, including its resolution/noise/
    # classification threshold.
    strata = [
        Stratum("high-risk", population=100, detectable_positive=10),
        Stratum("lower-risk", population=900, detectable_positive=1),
    ]
    scout_cost = 8  # high-resolution-FOV equivalents, including analysis
    total_cost = 28
    confirmatory_budget = total_cost - scout_cost

    uniform_n = total_cost  # no scout; all spend goes to high-resolution FOVs
    uniform_miss = miss_fraction(1000, 11, uniform_n)
    uniform20_miss = miss_fraction(1000, 11, confirmatory_budget)

    allocation, adaptive_miss = best_allocation(
        strata, field_budget=confirmatory_budget, min_per_stratum=1
    )

    print("Illustrative finite-population result (not biological evidence)")
    print(f"total budget: {total_cost} high-resolution-FOV equivalents")
    print(f"scout + calibration + analysis charge: {scout_cost}")
    print(f"confirmatory high-resolution budget: {confirmatory_budget}")
    print(
        "uniform, equal total cost: "
        f"n={uniform_n}, detection={fmt_probability(1 - uniform_miss)}, "
        f"miss={fmt_probability(uniform_miss)}"
    )
    print(
        "uniform, same number of confirmatory FOVs: "
        f"n={confirmatory_budget}, detection={fmt_probability(1 - uniform20_miss)}, "
        f"miss={fmt_probability(uniform20_miss)}"
    )
    print(
        "stratified, exact best allocation with >=1 FOV/stratum: "
        f"n={allocation}, detection={fmt_probability(1 - adaptive_miss)}, "
        f"miss={fmt_probability(adaptive_miss)}"
    )


if __name__ == "__main__":
    main()

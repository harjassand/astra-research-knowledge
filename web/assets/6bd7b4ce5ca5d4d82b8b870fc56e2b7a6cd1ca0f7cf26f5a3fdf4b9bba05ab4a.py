#!/usr/bin/env python3
"""Exact finite-partition calculations for redundant autocatalytic seed cores.

This is a mathematical model check, not a chemical simulation or empirical
validation.  Molecules are independently assigned to either daughter with
probability 1/2.  Each of r disjoint k-molecule cores is sufficient to
reconstruct the same catalytic state; a daughter is active iff it receives at
least one whole core.
"""

from __future__ import annotations

from math import comb, log
from typing import Dict, Tuple


def exact(k: int, r: int) -> Dict[str, float]:
    if k < 1 or r < 1:
        raise ValueError("k and r must be positive integers")
    a = 2.0 ** (-k)  # chance a specified core is assigned wholly to a specified daughter
    A = 1.0 - a
    B = 1.0 - 2.0 * a  # chance a specified core is split between daughters
    q = 1.0 - A**r
    p0 = B**r  # neither daughter gets a complete core
    p2 = 1.0 - 2.0 * A**r + B**r
    p1 = 2.0 * A**r - 2.0 * B**r
    mean = 2.0 * q
    if abs(mean - 1.0) < 1e-14 and abs(p1 - 1.0) < 1e-14:
        # Degenerate critical process: exactly one active daughter forever.
        surv = 1.0
    elif mean <= 1.0 or p2 == 0.0:
        surv = 0.0
    else:
        surv = (mean - 1.0) / p2
    # Exact expected number of activated fuel molecules needed to restore r
    # copies of each of the k catalyst species in every active daughter.
    fuel = k * r * (1.0 - A ** (r - 1))
    return {"q": q, "p0": p0, "p1": p1, "p2": p2,
            "mean": mean, "survival": surv, "fuel": fuel}


def enumerate_partition(k: int, r: int) -> Dict[str, float]:
    """Brute-force all 2**(k*r) assignments; used to check closed forms."""
    m = k * r
    count0 = count1 = count2 = 0
    fuel_sum = 0
    for mask in range(1 << m):
        v1 = v2 = False
        counts1 = [0] * k
        counts2 = [0] * k
        for core in range(r):
            intact1 = intact2 = True
            for species in range(k):
                pos = core * k + species
                in1 = (mask >> pos) & 1
                if in1:
                    counts1[species] += 1
                else:
                    counts2[species] += 1
                intact1 &= bool(in1)
                intact2 &= not bool(in1)
            v1 |= intact1
            v2 |= intact2
        active = int(v1) + int(v2)
        if active == 0:
            count0 += 1
        elif active == 1:
            count1 += 1
        else:
            count2 += 1
        if v1:
            fuel_sum += sum(r - c for c in counts1)
        if v2:
            fuel_sum += sum(r - c for c in counts2)
    den = float(1 << m)
    return {"p0": count0 / den, "p1": count1 / den, "p2": count2 / den,
            "fuel": fuel_sum / den}


def minimum_r(k: int, target_q: float) -> int:
    if not 0.0 < target_q < 1.0:
        raise ValueError("target_q must be between zero and one")
    r = 1
    while exact(k, r)["q"] < target_q:
        r += 1
    return r


def growth_exponent(q: float, tau: float, mutation_hazard: float = 0.0) -> float:
    """Per-time Malthus rate when wrong-state mutation is Poisson at rate mu."""
    if q <= 0.0 or tau <= 0.0:
        raise ValueError("q and tau must be positive")
    return (log(2.0 * q) - mutation_hazard * tau) / tau


def binomial_reporter_error(M: int, p_a: float, p_b: float) -> Tuple[float, float]:
    """Exact equal-prior Bayes error and Bhattacharyya upper bound.

    Each of M finite reporter precursors independently converts with
    probability p_a or p_b according to the state.  The observed product count
    is Binomial(M,p).  The exact optimal error is 1/2 sum_z min(P_a(z),P_b(z)).
    """
    if M < 0 or not (0.0 <= p_a <= 1.0 and 0.0 <= p_b <= 1.0):
        raise ValueError("invalid reporter parameters")
    pa = pb = 0.0
    for z in range(M + 1):
        c = comb(M, z)
        pa_z = c * p_a**z * (1.0 - p_a)**(M - z)
        pb_z = c * p_b**z * (1.0 - p_b)**(M - z)
        pa += min(pa_z, pb_z)
    exact_error = 0.5 * pa
    bc = (p_a * p_b) ** 0.5 + ((1.0 - p_a) * (1.0 - p_b)) ** 0.5
    return exact_error, 0.5 * bc**M


def main() -> None:
    print("k r q mean P0 P1 P2 survival expected_seed_fuel")
    for k, r in [(2, 1), (2, 2), (2, 3), (2, 4), (2, 17), (3, 6)]:
        d = exact(k, r)
        if k * r <= 20:
            brute = enumerate_partition(k, r)
            for key in ("p0", "p1", "p2", "fuel"):
                assert abs(d[key] - brute[key]) < 1e-12, (k, r, key, d[key], brute[key])
        print(k, r, *(f"{d[key]:.9g}" for key in
                      ("q", "mean", "p0", "p1", "p2", "survival", "fuel")))

    q = exact(2, 17)["q"]
    print("\n17 two-species alternative cores: per-daughter retention", q)
    print("10-generation tracked-lineage retention", q**10)
    print("same-state supercritical mutation limit at tau=1", log(2.0 * q))
    pe, bound = binomial_reporter_error(100, 0.60, 0.40)
    print("100-molecule reporter exact Bayes error", pe)
    print("100-molecule reporter Bhattacharyya bound", bound)
    print("example growth exponent q=0.578125, tau=10, mu=0.005",
          growth_exponent(exact(2, 3)["q"], 10.0, 0.005))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact-rational FPTAS certificate for a supplied fixed proposal and box.

All assumptions are supplied, not learned. This module never estimates local
second moments, acquires event masses, or optimizes the proposal q.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
import sys
import time
from typing import Iterable

F = Fraction


@dataclass(frozen=True)
class Coordinate:
    P: F
    q: F
    B: F
    lower: F
    upper: F

    @property
    def a(self) -> F:
        return self.P * self.lower

    @property
    def b(self) -> F:
        return self.P * self.upper

    @property
    def c(self) -> F:
        return self.B / self.q


@dataclass(frozen=True, slots=True)
class State:
    S: F
    V: F
    mask: int


def exact(value) -> F:
    """Reject binary floating inputs; strings, integers and Fractions are exact."""
    if isinstance(value, (float, bool)):
        raise ValueError("Use an integer or rational/decimal string, not float/bool")
    return F(value)


def read_coordinates(rows: list[dict]) -> tuple[Coordinate, ...]:
    return tuple(Coordinate(*(exact(row[k]) for k in
                             ("P", "q", "B", "lower", "upper")))
                 for row in rows)


def validate(coords: tuple[Coordinate, ...]) -> None:
    if not coords:
        raise ValueError("At least one coordinate is required")
    if any(not isinstance(x, F) for c in coords
           for x in (c.P, c.q, c.B, c.lower, c.upper)):
        raise ValueError("Coordinate values must be Fraction instances")
    for c in coords:
        if c.P < 0 or c.q <= 0 or c.B < 1:
            raise ValueError("Require P>=0, q>0, B>=1")
        if not 0 <= c.lower <= c.upper <= 1:
            raise ValueError("Require 0<=lower<=upper<=1")
    if sum((c.q for c in coords), F(0)) != 1:
        raise ValueError("Proposal probabilities q must sum exactly to one")


def objective(state: State) -> F:
    if state.S <= 0:
        raise ValueError("Objective undefined at zero event mass")
    return state.V / (state.S * state.S)


def reconstruct(coords: tuple[Coordinate, ...], mask: int) -> State:
    if not 0 <= mask < (1 << len(coords)):
        raise ValueError("Witness mask out of range")
    S, V = F(0), F(0)
    for i, c in enumerate(coords):
        x = c.b if (mask >> i) & 1 else c.a
        S += x
        V += c.c * x * x
    return State(S, V, mask)


def trim(states: Iterable[State], rho: F) -> list[State]:
    """Keep max V in each sorted bucket [first S, rho*first S).

    For every incoming positive state (S,V), a retained state satisfies
    S_rep < rho*S and V_rep >= V. Zero has V=0 and is kept separately.
    """
    ordered = sorted(states, key=lambda s: (s.S, -s.V, s.mask))
    retained: list[State] = []
    pos = 0
    while pos < len(ordered) and ordered[pos].S == 0:
        if ordered[pos].V != 0:
            raise ValueError("Invalid zero-mass state with nonzero numerator")
        if not retained:
            retained.append(ordered[pos])
        pos += 1
    while pos < len(ordered):
        best = ordered[pos]
        threshold = rho * best.S
        pos += 1
        while pos < len(ordered) and ordered[pos].S < threshold:
            candidate = ordered[pos]
            if (candidate.V > best.V or
                (candidate.V == best.V and
                 (candidate.S, candidate.mask) < (best.S, best.mask))):
                best = candidate
            pos += 1
        retained.append(best)
    return retained


def analytic_upper_bounds(coords: tuple[Coordinate, ...]) -> dict[str, F | None]:
    active = [c for c in coords if c.b > 0]
    if not active:
        return {"interval": None, "max_coefficient": None,
                "coordinate_fractions": None, "kantorovich": None, "best": None}
    A = sum((c.a for c in coords), F(0))
    numerator = sum((c.c * c.b * c.b for c in coords), F(0))
    interval = numerator / (A*A) if A > 0 else None
    max_coefficient = max(c.c for c in active)
    coordinate = sum((c.c * (c.b / (c.b + A - c.a))**2
                      for c in active), F(0))
    common = coords[0]
    kantorovich = None
    if (common.lower > 0 and
        all(c.P == c.q and c.B == 1 and
            c.lower == common.lower and c.upper == common.upper
            for c in coords)):
        kantorovich = ((common.lower+common.upper)**2 /
                       (4*common.lower*common.upper))
    best = min(x for x in (interval, max_coefficient, coordinate, kantorovich)
               if x is not None)
    return {"interval": interval, "max_coefficient": max_coefficient,
            "coordinate_fractions": coordinate, "kantorovich": kantorovich, "best": best}


def solve(coords: tuple[Coordinate, ...], epsilon=F(1, 4)) -> dict:
    validate(coords)
    epsilon = exact(epsilon)
    if not 0 < epsilon <= 1:
        raise ValueError("Require 0<epsilon<=1")
    started = time.perf_counter()
    d = len(coords)
    if all(c.b == 0 for c in coords):
        return {"status": "NO_POSITIVE_EVENT_MASS", "dimension": d,
                "reason": "The feasible positive-denominator domain is empty"}
    # Rational choice satisfying rho**(2*d) <= 1+epsilon; see proof.txt.
    rho = 1 + epsilon / (2*d*(1+epsilon))
    states = [State(F(0), F(0), 0)]
    layer_counts = []
    peak_expanded = 0
    for i, c in enumerate(coords):
        choices = [(c.a, c.c*c.a*c.a, 0)]
        if c.b != c.a:
            choices.append((c.b, c.c*c.b*c.b, 1 << i))
        expanded = [State(s.S+x, s.V+v, s.mask | bit)
                    for s in states for x, v, bit in choices]
        peak_expanded = max(peak_expanded, len(expanded))
        states = trim(expanded, rho)
        layer_counts.append(len(states))
    positive = [s for s in states if s.S > 0]
    winner = max(positive, key=lambda s: (objective(s), -s.mask))
    L = objective(winner)
    factor = rho ** (2*d)
    if factor > 1+epsilon:
        raise AssertionError("Internal error in approximation factor")
    baselines = analytic_upper_bounds(coords)
    U_dp = factor * L
    U = min(U_dp, baselines["best"])
    result = {
        "status": "CERTIFIED_FIXED_PROPOSAL_BOX",
        "dimension": d, "epsilon": str(epsilon), "rho": str(rho),
        "factor": str(factor), "lower_bound": str(L),
        "upper_bound_dp": str(U_dp), "upper_bound": str(U),
        "witness_mask": winner.mask,
        "witness_upper_indices": [i for i in range(d) if winner.mask >> i & 1],
        "witness_mass": str(winner.S), "witness_numerator": str(winner.V),
        "analytic_upper_bounds": {k: None if v is None else str(v)
                                   for k, v in baselines.items()},
        "layer_counts": layer_counts, "peak_expanded_states": peak_expanded,
        "elapsed_seconds": time.perf_counter()-started,
    }
    check_witness(coords, result)
    return result


def check_witness(coords: tuple[Coordinate, ...], result: dict) -> None:
    """Check exact witness and factor arithmetic, not the whole DP theorem."""
    if result["status"] != "CERTIFIED_FIXED_PROPOSAL_BOX":
        raise ValueError("Result has no positive-mass certificate")
    s = reconstruct(coords, result["witness_mask"])
    L, U = F(result["lower_bound"]), F(result["upper_bound"])
    epsilon, rho = F(result["epsilon"]), F(result["rho"])
    if s.S <= 0 or objective(s) != L:
        raise AssertionError("Witness objective mismatch")
    if s.S != F(result["witness_mass"]) or s.V != F(result["witness_numerator"]):
        raise AssertionError("Witness sums mismatch")
    factor = rho ** (2*len(coords))
    if factor != F(result["factor"]) or factor > 1+epsilon:
        raise AssertionError("Factor mismatch")
    if F(result["upper_bound_dp"]) != factor*L or not L <= U <= factor*L:
        raise AssertionError("Certificate arithmetic mismatch")


def exhaustive(coords: tuple[Coordinate, ...], max_dimension: int = 24) -> State:
    validate(coords)
    if len(coords) > max_dimension:
        raise ValueError("Exhaustive dimension limit exceeded")
    best = None
    # A simple independent implementation, intentionally not sharing DP state.
    for bits in product((0, 1), repeat=len(coords)):
        xs = [c.b if bit else c.a for c, bit in zip(coords, bits)]
        S = sum(xs, F(0))
        if S == 0:
            continue
        V = sum((c.B*x*x/c.q for c, x in zip(coords, xs)), F(0))
        candidate = State(S, V, sum(bit << i for i, bit in enumerate(bits)))
        if best is None or objective(candidate) > objective(best):
            best = candidate
    if best is None:
        raise ValueError("No positive-mass corner exists")
    return best


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON file, or - for stdin")
    parser.add_argument("--epsilon", default="1/4")
    parser.add_argument("--exhaustive", action="store_true")
    args = parser.parse_args()
    with (sys.stdin if args.input == "-" else open(args.input)) as handle:
        payload = json.load(handle)
    coords = read_coordinates(payload["coordinates"])
    result = solve(coords, exact(args.epsilon))
    if args.exhaustive and result["status"] == "CERTIFIED_FIXED_PROPOSAL_BOX":
        best = exhaustive(coords)
        result["exhaustive_optimum"] = str(objective(best))
        result["exhaustive_mask"] = best.mask
        result["exhaustive_containment_pass"] = (
            F(result["lower_bound"]) <= objective(best) <= F(result["upper_bound"]))
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()

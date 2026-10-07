#!/usr/bin/env python3
"""Exact rational robust hitting-time certificates for finite 2-species CRNs.

Admitted input: a fixed-total A+B=N class, integer complexes of total order at
most two, and independent rational rate intervals. Propensities are products
of falling factorials. The code either returns a checked rational potential,
an exact closed-set witness against uniform recovery, or UNKNOWN on scope or
resource limits. It makes no claim about unbounded classes.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from typing import Any


class ScopeError(Exception):
    pass


class BudgetExceeded(Exception):
    pass


class Infeasible(Exception):
    pass


def q(value: Any) -> Fraction:
    if isinstance(value, float):
        raise ScopeError("rational inputs must be integers or strings, not floats")
    return Fraction(value)


def qs(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def falling(n: int, order: int) -> int:
    if order < 0:
        raise ScopeError("negative reactant count")
    if n < order:
        return 0
    out = 1
    for j in range(order):
        out *= n - j
    return out


def propensity(state: tuple[int, int], reactants: tuple[int, int]) -> int:
    return falling(state[0], reactants[0]) * falling(state[1], reactants[1])


def validate(net: dict[str, Any]) -> tuple[int, int, list[dict[str, Any]], int]:
    total = net.get("total")
    core_min = net.get("core_min_each")
    cap = int(net.get("row_cap", 200_000))
    if not isinstance(total, int) or total < 0:
        raise ScopeError("total must be a nonnegative integer")
    if not isinstance(core_min, int) or core_min < 0:
        raise ScopeError("core_min_each must be a nonnegative integer")
    if cap < 1:
        raise ScopeError("row_cap must be positive")
    reactions = net.get("reactions")
    if not isinstance(reactions, list) or not reactions:
        raise ScopeError("a nonempty reaction list is required")
    checked: list[dict[str, Any]] = []
    for index, reaction in enumerate(reactions):
        name = str(reaction.get("name", f"r{index}"))
        reactants = tuple(reaction.get("reactants", ()))
        products = tuple(reaction.get("products", ()))
        if len(reactants) != 2 or len(products) != 2:
            raise ScopeError(f"{name}: exactly two species are required")
        if any(not isinstance(v, int) or v < 0 for v in reactants + products):
            raise ScopeError(f"{name}: complexes must be nonnegative integer pairs")
        if sum(reactants) > 2 or sum(products) > 2:
            raise ScopeError(f"{name}: complex molecularity exceeds two")
        if sum(reactants) != sum(products):
            raise ScopeError(f"{name}: reaction does not preserve A+B")
        low, high = q(reaction["rate_min"]), q(reaction["rate_max"])
        if low < 0 or high < low:
            raise ScopeError(f"{name}: invalid rational rate interval")
        checked.append({
            "name": name,
            "reactants": reactants,
            "products": products,
            "jump": (products[0] - reactants[0], products[1] - reactants[1]),
            "low": low,
            "high": high,
        })
    if total + 1 > 64:
        raise BudgetExceeded("state count exceeds the admitted cap of 64")
    return total, core_min, checked, cap


def states_and_target(total: int, core_min: int) -> tuple[list[tuple[int, int]], set[tuple[int, int]]]:
    states = [(a, total - a) for a in range(total + 1)]
    target = {x for x in states if min(x) >= core_min}
    return states, target


def rate_corners(reactions: list[dict[str, Any]]) -> list[tuple[Fraction, ...]]:
    choices = [(r["low"],) if r["low"] == r["high"] else (r["low"], r["high"]) for r in reactions]
    return list(itertools.product(*choices))


def next_state(state: tuple[int, int], reaction: dict[str, Any]) -> tuple[int, int] | None:
    if propensity(state, reaction["reactants"]) == 0:
        return None
    jump = reaction["jump"]
    out = (state[0] + jump[0], state[1] + jump[1])
    if min(out) < 0:
        raise AssertionError("enabled reaction produced a negative count")
    return out


def guaranteed_reachable(state: tuple[int, int], target: set[tuple[int, int]],
                         reactions: list[dict[str, Any]]) -> set[tuple[int, int]]:
    seen = {state}
    todo = [state]
    while todo:
        x = todo.pop()
        for r in reactions:
            if r["low"] <= 0:
                continue
            y = next_state(x, r)
            if y is not None and y != x and y not in seen:
                seen.add(y)
                todo.append(y)
    return seen


def normalize_row(row: tuple[tuple[Fraction, ...], Fraction]) -> tuple[tuple[Fraction, ...], Fraction] | None:
    coeff, rhs = row
    first = next((abs(c) for c in coeff if c), None)
    if first is None:
        if rhs > 0:
            raise Infeasible("constant contradiction 0 >= positive")
        return None
    return tuple(c / first for c in coeff), rhs / first


def deduplicate(rows: list[tuple[tuple[Fraction, ...], Fraction]], cap: int) -> list[tuple[tuple[Fraction, ...], Fraction]]:
    unique: dict[tuple[tuple[Fraction, ...], Fraction], None] = {}
    for row in rows:
        normalized = normalize_row(row)
        if normalized is not None:
            unique[normalized] = None
            if len(unique) > cap:
                raise BudgetExceeded(f"Fourier-Motzkin row cap {cap} exceeded")
    return list(unique)


def fm_solve(rows: list[tuple[tuple[Fraction, ...], Fraction]], nvars: int,
             cap: int) -> list[Fraction]:
    """Exact Fourier-Motzkin feasibility and rational back-substitution."""
    current = deduplicate(rows, cap)
    remaining = set(range(nvars))
    stages: list[tuple[int, list[tuple[tuple[Fraction, ...], Fraction]]]] = []
    while remaining:
        # Minimize the number of pairwise combinations at this elimination.
        def cost(j: int) -> tuple[int, int, int]:
            pos = sum(1 for c, _ in current if c[j] > 0)
            neg = sum(1 for c, _ in current if c[j] < 0)
            return (pos * neg, pos + neg, j)

        variable = min(remaining, key=cost)
        stages.append((variable, current))
        zero: list[tuple[tuple[Fraction, ...], Fraction]] = []
        positive = []
        negative = []
        for row in current:
            a = row[0][variable]
            (positive if a > 0 else negative if a < 0 else zero).append(row)
        generated = list(zero)
        if positive and negative:
            for p in positive:
                ap = p[0][variable]
                for n in negative:
                    an = n[0][variable]
                    mp, mn = -an, ap
                    coeff = tuple(mp * u + mn * v for u, v in zip(p[0], n[0]))
                    rhs = mp * p[1] + mn * n[1]
                    generated.append((coeff, rhs))
                    if len(generated) > cap * 4:
                        raise BudgetExceeded(f"Fourier-Motzkin generation cap {cap * 4} exceeded")
        current = deduplicate(generated, cap)
        remaining.remove(variable)
    # Any surviving constant contradiction is a genuine infeasibility result.
    for coeff, rhs in current:
        if any(coeff):
            raise AssertionError("elimination left a variable coefficient")
        if rhs > 0:
            raise Infeasible("eliminated system contains 0 >= positive")

    values = [Fraction(0) for _ in range(nvars)]
    for variable, stage_rows in reversed(stages):
        lower: list[Fraction] = []
        upper: list[Fraction] = []
        for coeff, rhs in stage_rows:
            a = coeff[variable]
            rest = sum((coeff[j] * values[j] for j in range(nvars) if j != variable), Fraction(0))
            if a > 0:
                lower.append((rhs - rest) / a)
            elif a < 0:
                upper.append((rhs - rest) / a)
            elif rest < rhs:
                raise AssertionError("back-substitution found an inconsistent eliminated row")
        lo = max(lower) if lower else None
        hi = min(upper) if upper else None
        if lo is not None and hi is not None:
            if lo > hi:
                raise AssertionError("Fourier-Motzkin back-substitution interval is empty")
            values[variable] = (lo + hi) / 2
        elif lo is not None:
            values[variable] = lo
        elif hi is not None:
            values[variable] = hi
        else:
            values[variable] = Fraction(0)
    # A final exact check protects the synthesizer itself against implementation errors.
    for coeff, rhs in rows:
        if sum((a * x for a, x in zip(coeff, values)), Fraction(0)) < rhs:
            raise AssertionError("exact back-substitution failed an original inequality")
    return values


def generator_rows(states: list[tuple[int, int]], target: set[tuple[int, int]],
                   reactions: list[dict[str, Any]]) -> tuple[list[tuple[tuple[Fraction, ...], Fraction]], list[tuple[int, int]]]:
    transient = [x for x in states if x not in target]
    index = {x: i for i, x in enumerate(transient)}
    rows: list[tuple[tuple[Fraction, ...], Fraction]] = []
    for x in transient:
        i = index[x]
        nonnegative = [Fraction(0)] * len(transient)
        nonnegative[i] = Fraction(1)
        rows.append((tuple(nonnegative), Fraction(0)))
        for action in rate_corners(reactions):
            coeff = [Fraction(0)] * len(transient)
            for r, rate in zip(reactions, action):
                p = propensity(x, r["reactants"])
                if not p:
                    continue
                y = next_state(x, r)
                if y is None or y == x:
                    continue
                intensity = rate * p
                coeff[i] += intensity
                if y not in target:
                    coeff[index[y]] -= intensity
            rows.append((tuple(coeff), Fraction(1)))
    return rows, transient


def verify_potential(states: list[tuple[int, int]], target: set[tuple[int, int]],
                     reactions: list[dict[str, Any]], h: dict[tuple[int, int], Fraction]) -> dict[str, Any]:
    worst: tuple[Fraction, tuple[int, int], tuple[Fraction, ...]] | None = None
    for x in states:
        if x in target:
            if h.get(x, Fraction(0)) != 0:
                return {"valid": False, "reason": "potential must be zero on target", "state": x}
            continue
        if h.get(x, Fraction(0)) < 0:
            return {"valid": False, "reason": "negative potential", "state": x}
        vals = []
        for action in rate_corners(reactions):
            drift = Fraction(0)
            for r, rate in zip(reactions, action):
                p = propensity(x, r["reactants"])
                if p:
                    y = next_state(x, r)
                    if y is not None and y != x:
                        drift += rate * p * (h.get(y, Fraction(0)) - h[x])
            vals.append((drift, action))
        drift, action = max(vals, key=lambda z: z[0])
        margin = -drift
        if worst is None or margin < worst[0]:
            worst = (margin, x, action)
    if worst is None:
        return {"valid": True, "minimum_negative_drift": "infinity", "max_h": "0"}
    return {
        "valid": worst[0] >= 1,
        "minimum_negative_drift": qs(worst[0]),
        "worst_state": list(worst[1]),
        "worst_rate_corner": [qs(v) for v in worst[2]],
        "max_h": qs(max((h[x] for x in states), default=Fraction(0))),
    }


def synthesize(net: dict[str, Any]) -> dict[str, Any]:
    try:
        total, core_min, reactions, cap = validate(net)
        states, target = states_and_target(total, core_min)
        if not target:
            return {"status": "REFUTED", "scope": "uniform recovery to requested core", "reason": "target core is empty"}
        transient = [x for x in states if x not in target]
        for source in transient:
            reachable = guaranteed_reachable(source, target, reactions)
            if not (reachable & target):
                return {
                    "status": "REFUTED",
                    "scope": "uniform recovery from every state to requested core",
                    "source": list(source),
                    "guaranteed_reachable_closed_set": [list(x) for x in sorted(reachable)],
                    "admissible_static_rate_choice": [qs(r["low"] if r["low"] > 0 else Fraction(0)) for r in reactions],
                    "reason": "under this allowed rate choice, no reaction path reaches the target",
                }
        if len(transient) > 20:
            raise BudgetExceeded("more than 20 transient states; exact elimination withheld")
        rows, transient = generator_rows(states, target, reactions)
        h_values = fm_solve(rows, len(transient), cap)
        h = {x: Fraction(0) for x in target}
        h.update({x: v for x, v in zip(transient, h_values)})
        checked = verify_potential(states, target, reactions, h)
        if not checked["valid"]:
            return {"status": "UNKNOWN", "reason": "synthesized candidate failed exact independent checker", "checker": checked}
        return {
            "status": "CERTIFIED",
            "scope": "uniform expected hitting time to requested core, from any state in fixed-total class",
            "network": net.get("name", "unnamed"),
            "model": "lambda_r(x,t)=k_r(t,past)*product_i (x_i)_{under y_ri}; rates independently in supplied rational intervals",
            "total": total,
            "target_min_each": core_min,
            "potential": {f"{x[0]},{x[1]}": qs(h[x]) for x in states},
            "expected_hitting_time_upper_by_state": {f"{x[0]},{x[1]}": qs(h[x]) for x in states},
            "checker": checked,
            "checked_rate_corners_per_transient_state": len(rate_corners(reactions)),
            "elimination_row_cap": cap,
        }
    except BudgetExceeded as exc:
        return {"status": "UNKNOWN", "reason": str(exc)}
    except ScopeError as exc:
        return {"status": "UNKNOWN", "reason": str(exc)}
    except Infeasible as exc:
        return {"status": "UNKNOWN", "reason": f"exact Foster system infeasible in admitted ansatz: {exc}"}


PAIR_EXCHANGE = {
    "name": "four-channel pair exchange, N=4",
    "total": 4,
    "core_min_each": 2,
    "row_cap": 200_000,
    "reactions": [
        {"name": "AB_to_2A", "reactants": [1, 1], "products": [2, 0], "rate_min": "1", "rate_max": "4"},
        {"name": "2A_to_AB", "reactants": [2, 0], "products": [1, 1], "rate_min": "1", "rate_max": "4"},
        {"name": "AB_to_2B", "reactants": [1, 1], "products": [0, 2], "rate_min": "1", "rate_max": "4"},
        {"name": "2B_to_AB", "reactants": [0, 2], "products": [1, 1], "rate_min": "1", "rate_max": "4"},
    ],
}

PARITY_TRAP = {
    "name": "pair transmutation parity trap, N=2",
    "total": 2,
    "core_min_each": 1,
    "reactions": [
        {"name": "2A_to_2B", "reactants": [2, 0], "products": [0, 2], "rate_min": "1", "rate_max": "1"},
        {"name": "2B_to_2A", "reactants": [0, 2], "products": [2, 0], "rate_min": "1", "rate_max": "1"},
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("network_json", nargs="?", help="optional JSON input; omit to emit the two exact examples")
    args = parser.parse_args()
    if args.network_json:
        with open(args.network_json, "r", encoding="utf-8") as stream:
            inputs = [json.load(stream)]
    else:
        inputs = [PAIR_EXCHANGE, PARITY_TRAP]
    print(json.dumps([synthesize(net) for net in inputs], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

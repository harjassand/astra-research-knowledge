"""Exact finite checks for the frozen-particle-rate driven tracer.

The state is the gap vector. Each physical particle and direction remains a
separate transition mark, including when distinct marks share endpoints.
No simulation, fitting, or assumption of microscopic equilibration is used.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def weights(native_rates, p, q):
    resistance = sum((1 / c for c in native_rates), Q(0))
    flux = (p - q) / (1 + q * resistance)
    result = [Q(1)]
    for c in native_rates:
        result.append(result[-1] + flux / c)
    return result, flux


def monomial(gaps, w):
    result = Q(1)
    for a, weight in zip(gaps, w):
        result *= weight**a
    return result


def one_case(n, holes, p, q):
    library = [Q(1, 3), Q(2, 5), Q(7, 4), Q(3), Q(5, 6)]
    native = [library[i % len(library)] for i in range(n - 1)]
    w, flux = weights(native, p, q)
    states = list(compositions(holes, n))
    raw = {g: monomial(g, w) for g in states}
    z = sum(raw.values(), Q(0))
    zm = sum((monomial(g, w) for g in compositions(holes - 1, n)), Q(0))
    pi = {g: value / z for g, value in raw.items()}
    t = zm / z
    incoming_minus_outgoing = {g: Q(0) for g in states}
    velocity = [Q(0) for _ in range(n)]
    marked_ep = 0.0
    marked_transitions = 0
    for g in states:
        for i in range(n):
            previous = (i - 1) % n
            right = p if i == 0 else native[i - 1]
            left = q if i == 0 else native[i - 1]
            for direction, source, target, rate, reverse in (
                (+1, i, previous, right, left),
                (-1, previous, i, left, right),
            ):
                if not g[source]:
                    continue
                destination = list(g)
                destination[source] -= 1
                destination[target] += 1
                destination = tuple(destination)
                flow = pi[g] * rate
                incoming_minus_outgoing[g] -= flow
                incoming_minus_outgoing[destination] += flow
                velocity[i] += direction * flow
                marked_ep += float(flow) * math.log(
                    float(flow / (pi[destination] * reverse))
                )
                marked_transitions += 1
    assert all(value == 0 for value in incoming_minus_outgoing.values())
    assert all(value == flux * t for value in velocity)
    for i in range(n):
        occupied_gap = sum((pi[g] for g in states if g[i]), Q(0))
        assert occupied_gap == w[i] * t
    lower = Q(holes, holes + n - 1) / max(w)
    upper = Q(holes, holes + n - 1) / min(w)
    assert lower <= t <= upper
    expected_ep = math.log(float(p / q)) * float(flux * t)
    ep_error = abs(marked_ep - expected_ep)
    assert ep_error < 2e-12
    return {
        "particles_including_tracer": n,
        "holes": holes,
        "states": len(states),
        "marked_transitions": marked_transitions,
        "stationarity_residual_exact": "0",
        "common_velocity_exact": str(flux * t),
        "partition_ratio_exact": str(t),
        "marked_entropy_work_error": ep_error,
    }


def main():
    cases = [
        one_case(n, holes, p, q)
        for n, holes in product(range(2, 6), range(1, 7))
        for p, q in ((Q(5, 3), Q(2, 3)), (Q(2, 3), Q(2, 3)))
    ]
    lam = math.log(1.5)
    result = {
        "kind": "exact finite population-model checks; no preparation or hydrodynamic test",
        "cases": len(cases),
        "total_states_checked": sum(case["states"] for case in cases),
        "total_marked_transitions": sum(case["marked_transitions"] for case in cases),
        "max_entropy_work_error": max(case["marked_entropy_work_error"] for case in cases),
        "concrete_macroscopic_example": {
            "affinity": math.log(2),
            "mean_density": 1 / (4 * lam),
            "density_just_ahead": 0.75,
            "density_just_behind": 0.5,
            "velocity_times_mean_resistance": lam,
            "native_total_current_times_mean_resistance": 0.25,
            "work_per_N_T_times_mean_resistance": math.log(2) * lam,
            "profile_free_energy_lower_bound_per_N": (5 * lam - 2) / (16 * lam * lam),
        },
        "details": cases,
        "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = Path(__file__).with_name("DRIVEN_TRACER_CHECK.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "details"}, indent=2))


if __name__ == "__main__":
    main()

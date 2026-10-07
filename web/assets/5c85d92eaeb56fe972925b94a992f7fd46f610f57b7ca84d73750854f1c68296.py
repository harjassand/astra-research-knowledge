"""Independent finite diagnostics; these are not a proof of a released PDE theorem.

Checks the rooted-three-vertex algebra and a dominated-CFTP construction against
the exact Gibbs law of the hard-core model on an eight-vertex cycle. Floating
random variates make the latter a distribution diagnostic, not a certified
random-bit implementation of exact continuum sampling.
"""
import itertools
import json
import math
import random
import time
from collections import Counter
from pathlib import Path

import sympy as sp


def symbolic():
    z, c = sp.symbols("z c")
    tau = sp.Rational(15, 32)
    a = sp.exp(z + c * z**2)
    density = a - z * a**2 + (3 - tau) / 2 * z**2 * a**3
    second = sp.expand(sp.series(density, z, 0, 3).removeO()).coeff(z, 2)
    assert second == c - tau / 2
    r = sp.symbols("r")
    intersection = sp.pi * (4 + r) * (2 - r) ** 2 / 12
    triangle = sp.integrate(4 * sp.pi * r**2 * intersection, (r, 0, 1))
    assert triangle == 5 * sp.pi**2 / 6
    assert sp.simplify(triangle / (4 * sp.pi / 3) ** 2) == tau
    # Two input arguments needed for the nonuniform second-order cancellation.
    q, s, j = sp.symbols("q s j")
    marker = sp.symbols("u")
    # q has degree one; s and j have degree two in packing.
    lhs = sp.exp(marker*q + marker**2*j) * (
        1 - marker*q - marker**2*s + marker**2*q**2/2
        + marker**2*s - marker**2*j)
    assert sp.series(lhs, marker, 0, 3).removeO().expand() == 1
    return {"triangle_volume": str(triangle), "triangle_ratio": str(tau),
            "second_chemical_potential_coefficient": str(tau/2),
            "nonuniform_second_order_cancellation": True}


def poisson(lam, rng):
    product, k = 1.0, 0
    stop = math.exp(-lam)
    while product > stop:
        product *= rng.random()
        k += 1
    return k - 1


def cftp_cycle(n, lam, rng):
    """Stationary free process backwards, then set bounds forwards.

    Maintain one common environment when extending backwards. Each reverse
    removal is a forward birth; each reverse insertion is a forward death.
    Keeping independent old histories at each extension would bias output.
    """
    assert isinstance(lam, int)  # exact event-choice ratio using randrange
    initial = [(i, rng.randrange(n)) for i in range(poisson(lam, rng))]
    alive = dict(initial)
    next_id = len(initial)
    events = []
    block = 8
    while True:
        if not events and not alive:
            return 0, 0
        for _ in range(block):
            if rng.randrange(lam + len(alive)) < lam:
                ident, position = next_id, rng.randrange(n)
                next_id += 1
                alive[ident] = position
                events.append(("death", ident, position))
            else:
                ident = rng.choice(tuple(alive))
                position = alive.pop(ident)
                events.append(("birth", ident, position))
        upper = dict(alive)
        lower = {}
        for kind, ident, position in reversed(events):
            if kind == "death":
                upper.pop(ident, None)
                lower.pop(ident, None)
                continue
            incompatible = {position, (position-1) % n, (position+1) % n}
            if not any(x in incompatible for x in upper.values()):
                upper[ident] = lower[ident] = position
            elif not any(x in incompatible for x in lower.values()):
                upper[ident] = position
        if upper == lower:
            positions = list(lower.values())
            assert len(positions) == len(set(positions))
            assert all((x+1) % n not in positions for x in positions)
            return len(positions), len(events)
        block *= 2


def distribution_diagnostic(samples=20000):
    n, lam = 8, 2
    weights = Counter()
    for bits in itertools.product([0, 1], repeat=n):
        if any(bits[i] and bits[(i+1) % n] for i in range(n)):
            continue
        weights[sum(bits)] += (lam/n)**sum(bits)
    norm = sum(weights.values())
    exact = {k: v/norm for k, v in sorted(weights.items())}
    rng = random.Random(7102026)
    observed, counts = Counter(), []
    for _ in range(samples):
        k, events = cftp_cycle(n, lam, rng)
        observed[k] += 1
        counts.append(events)
    diagnostic = {
        "samples": samples, "graph": "8-cycle", "total_activity": lam,
        "exact_cardinality_probabilities": exact,
        "observed_cardinality_probabilities": {k: observed[k]/samples for k in exact},
        "mean_reverse_events": sum(counts)/samples,
        "largest_reverse_event_count": max(counts),
        "max_absolute_frequency_error": max(abs(observed[k]/samples-exact[k]) for k in exact),
    }
    diagnostic["chi_square"] = sum((observed[k]-samples*p)**2/(samples*p) for k,p in exact.items())
    # A broad, preregistered numerical correctness check, not theorem validation.
    assert diagnostic["max_absolute_frequency_error"] < 0.025
    return diagnostic


if __name__ == "__main__":
    start = time.perf_counter()
    result = {"symbolic": symbolic(), "cftp_diagnostic": distribution_diagnostic(),
              "status": "finite diagnostic only"}
    result["elapsed_seconds"] = time.perf_counter()-start
    path = Path(__file__).with_name("kinetic_calibration_checks.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

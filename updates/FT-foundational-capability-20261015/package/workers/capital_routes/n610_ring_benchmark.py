"""Small exact-reference benchmark for the composite-modulus N610 extension."""
from __future__ import annotations

from collections import Counter
from math import lcm
from itertools import product
from pathlib import Path
import random
import sys
import time

import numpy as np

from n610_ring_sampler import (
    ModularModel,
    demo_model,
    implicit_model,
    dependency_cone_sample,
    sample_coordinates,
)

DEPENDENCY_DIR = Path(__file__).resolve().parent / "dependencies"
sys.path.insert(0, str(DEPENDENCY_DIR))
from stratified_entropy_sampler import StratifiedModel, sample_coordinates as sample_digit_coordinates


def full_state_cftp(model: ModularModel, targets, rng: random.Random):
    """Perfect sampler via the safe all-sites-Haar coalescence certificate."""
    n, c, mod = model.n, model.c, model.modulus
    assert all(t == 0 for _, t, _ in targets), "benchmark CFTP currently projects time zero"
    den = lcm(model.s.denominator, model.r.denominator)
    ns, nr = int(model.s * den), int(model.r * den)
    # Scan backward to a time at which every site is a Haar reset.
    events = {}
    times = []
    while True:
        t = -len(times)
        row = []
        for i in range(n):
            x = rng.randrange(den)
            kind = "haar" if x < ns else "residual" if x < ns + nr else "gate"
            row.append(kind)
            events[(i, t)] = kind
        times.append(t)
        if all(kind == "haar" for kind in row):
            break

    state = [[rng.randrange(mod) for _ in range(c)] for _ in range(n)]
    parent_lookups = forcing_calls = 0
    # The all-Haar row is the oldest sampled time; propagate to time zero.
    for t in reversed(times[:-1]):
        old = state
        state = []
        for i in range(n):
            kind = events[(i, t)]
            if kind == "haar":
                row = [rng.randrange(mod) for _ in range(c)]
            elif kind == "residual":
                row = list(model.residual_state(i))
            else:
                parents = model.parent_list(i)
                parent_rows = [old[p] for p in parents]
                parent_lookups += len(parents)
                row = []
                for ell in range(c):
                    same = sum(a * old[p][ell] for a, p in zip(model.layer_coeffs(i, ell, len(parents)), parents))
                    low = [tuple(pr[h] for h in range(ell)) for pr in parent_rows]
                    row.append((same + model.forcing(i, ell, low)) % mod)
                    forcing_calls += 1
            state.append(row)
    values = [state[i][ell] for i, t, ell in targets]
    return values, {"fresh_events": n * len(times), "parent_lookups": parent_lookups,
                    "forcing_calls": forcing_calls, "backward_steps": len(times)}


def pathwise_state_cftp(model: ModularModel, targets, rng: random.Random):
    """Exhaustive random-map CFTP; stop only when every initial state coalesces."""
    n, c, mod = model.n, model.c, model.modulus
    assert all(t == 0 for _, t, _ in targets), "benchmark CFTP currently projects time zero"
    den = lcm(model.s.denominator, model.r.denominator)
    ns, nr = int(model.s * den), int(model.r * den)
    states = list(product(range(mod), repeat=n * c))
    maps = []  # newest first; each map advances one state-time to the next
    parent_work = forcing_work = category_work = image_lookups = 0

    def make_map():
        nonlocal category_work
        choices = []
        for i in range(n):
            x = rng.randrange(den)
            kind = "haar" if x < ns else "residual" if x < ns + nr else "gate"
            reset = tuple(rng.randrange(mod) for _ in range(c)) if kind == "haar" else None
            choices.append((kind, reset))
        category_work += n

        def apply(flat):
            nonlocal parent_work, forcing_work
            old = [flat[i*c:(i+1)*c] for i in range(n)]
            out = []
            for i, (kind, reset) in enumerate(choices):
                if kind == "haar":
                    row = reset
                elif kind == "residual":
                    row = model.residual_state(i)
                else:
                    parents = model.parent_list(i)
                    prs = [old[p] for p in parents]
                    parent_work += len(parents)
                    row = []
                    for ell in range(c):
                        same = sum(a * old[p][ell] for a, p in zip(model.layer_coeffs(i, ell, len(parents)), parents))
                        low = [tuple(pr[h] for h in range(ell)) for pr in prs]
                        row.append((same + model.forcing(i, ell, low)) % mod)
                        forcing_work += 1
                out.extend(row)
            return tuple(out)

        return apply

    tables = []  # newest first
    steps = 0
    while True:
        new_map = make_map()  # earliest map in the enlarged time window
        table = {x: new_map(x) for x in states}
        image = set(table.values())
        for later_table in reversed(tables):
            image_lookups += len(image)
            image = {later_table[x] for x in image}
        tables.append(table)
        steps += 1
        if len(image) == 1:
            final = next(iter(image))
            rows = [final[i*c:(i+1)*c] for i in range(n)]
            values = [rows[i][ell] for i, _, ell in targets]
            return values, {
                "fresh_events": category_work,
                "parent_lookups": parent_work,
                "forcing_calls": forcing_work,
                "backward_steps": steps,
                "state_map_evaluations": len(states) * steps,
                "image_composition_lookups": image_lookups,
            }


def prime_power_digit_sampler(model: ModularModel, targets, rng: random.Random):
    """Run the producer's F_p sampler on base-p digit-expanded Z/p^a states."""
    p = next((q for q in range(2, model.modulus + 1)
              if model.modulus % q == 0 and all(q % d for d in range(2, int(q**0.5) + 1))), None)
    if p is None:
        raise ValueError("modulus has no prime divisor")
    a = 0
    temp = model.modulus
    while temp % p == 0:
        temp //= p
        a += 1
    if temp != 1 or a < 1:
        raise ValueError("digit incumbent currently requires a prime-power modulus")
    c0, m0 = model.c, model.modulus
    digits = c0 * a
    parent_cache, coefficient_cache, residual_cache, forcing_cache = {}, {}, {}, {}
    stats = {"original_forcing_evals": 0, "digit_forcing_calls": 0,
             "parent_descriptor_reads": 0, "coefficient_descriptor_reads": 0,
             "residual_descriptor_reads": 0}

    def parent_oracle(i):
        if i not in parent_cache:
            parent_cache[i] = model.parent_list(i)
            stats["parent_descriptor_reads"] += 1
        return parent_cache[i]

    def original_coefficients(i, ell):
        key = (i, ell)
        if key not in coefficient_cache:
            coefficient_cache[key] = model.layer_coeffs(i, ell, len(parent_oracle(i)))
            stats["coefficient_descriptor_reads"] += 1
        return coefficient_cache[key]

    def expanded_coefficients(i, e):
        ell, _ = divmod(e, a)
        return tuple(x % p for x in original_coefficients(i, ell))

    def expanded_residual(i):
        if i not in residual_cache:
            residual = model.residual_state(i)
            residual_cache[i] = tuple(
                (residual[ell] // (p ** d)) % p for ell in range(c0) for d in range(a)
            )
            stats["residual_descriptor_reads"] += 1
        return residual_cache[i]

    def digit_forcing(i, e, lower_vectors):
        stats["digit_forcing_calls"] += 1
        ell, d = divmod(e, a)
        lower_values = []
        for row in lower_vectors:
            lower_values.append(tuple(
                sum(row[h*a + z] * (p ** z) for z in range(a))
                for h in range(ell)
            ))
        key = (i, ell, tuple(lower_values))
        if key not in forcing_cache:
            forcing_cache[key] = model.forcing(i, ell, lower_values) % m0
            stats["original_forcing_evals"] += 1
        f = forcing_cache[key]
        same_low = [
            sum(row[ell*a + z] * (p ** z) for z in range(d))
            for row in lower_vectors
        ]
        carry = (sum(A * x for A, x in zip(original_coefficients(i, ell), same_low)) + f) // (p ** d)
        # The current digit's linear parent term is supplied by N610's
        # same-level coefficient map A mod p; only carry belongs here.
        return carry % p

    digit_model = StratifiedModel(
        n=model.n, c=digits, q=p, s=model.s, r=model.r, parents=parent_oracle,
        coeffs=expanded_coefficients, forcing=digit_forcing, residual=expanded_residual,
    )
    digit_targets = [
        (site, t, ell*a + d)
        for site, t, ell in targets
        for d in range(a)
    ]
    raw, info = sample_digit_coordinates(digit_model, digit_targets, rng, diagnostics=True)
    values = []
    for j in range(len(targets)):
        values.append(sum(raw[j*a + d] * (p ** d) for d in range(a)))
    info.update(stats)
    return values, info


def exact_stationary(model: ModularModel):
    """Numerical full-state stationary reference, independently forward-built."""
    n, c, mod = model.n, model.c, model.modulus
    states = list(product(range(mod), repeat=n * c))
    index = {x: j for j, x in enumerate(states)}
    P = np.zeros((len(states), len(states)), dtype=float)
    s, r = float(model.s), float(model.r)
    for old_ix, flat in enumerate(states):
        old = [flat[i*c:(i+1)*c] for i in range(n)]
        local = []
        for i in range(n):
            dist = Counter()
            for reset in product(range(mod), repeat=c):
                dist[tuple(reset)] += s / (mod**c)
            dist[model.residual_state(i)] += r
            parents = model.parent_list(i)
            prs = [old[p] for p in parents]
            gate = []
            for ell in range(c):
                same = sum(a * old[p][ell] for a, p in zip(model.layer_coeffs(i, ell, len(parents)), parents))
                low = [tuple(pr[h] for h in range(ell)) for pr in prs]
                gate.append((same + model.forcing(i, ell, low)) % mod)
            dist[tuple(gate)] += 1.0 - s - r
            local.append(dist)
        for choices in product(*(list(d.items()) for d in local)):
            next_rows = [x[0] for x in choices]
            prob = np.prod([x[1] for x in choices])
            new_flat = tuple(v for row in next_rows for v in row)
            P[old_ix, index[new_flat]] += prob
    vals, vecs = np.linalg.eig(P.T)
    j = int(np.argmin(np.abs(vals - 1)))
    pi = np.real(vecs[:, j])
    pi /= pi.sum()
    if pi.min() < -1e-8 or np.max(np.abs(pi @ P - pi)) > 1e-10:
        raise ArithmeticError("stationary reference failed numerical residual checks")
    return states, pi, P


def main(draws=3000):
    model = demo_model()
    targets = [(0, 0, 1), (1, 0, 0), (1, 0, 1)]
    states, pi, P = exact_stationary(model)
    target_prob = Counter()
    for state, weight in zip(states, pi):
        rows = [state[i*model.c:(i+1)*model.c] for i in range(model.n)]
        target_prob[(rows[0][1], rows[1][0], rows[1][1])] += weight

    algos = {
        "subgroup-local": lambda rng: sample_coordinates(model, targets, rng, diagnostics=True),
        "original-digit-expanded": lambda rng: prime_power_digit_sampler(model, targets, rng),
        "causal-cone": lambda rng: dependency_cone_sample(model, targets, rng, diagnostics=True),
        "pathwise-global-CFTP": lambda rng: pathwise_state_cftp(model, targets, rng),
        "all-site-Haar-CFTP": lambda rng: full_state_cftp(model, targets, rng),
    }
    for name, sampler in algos.items():
        rng = random.Random(61020261015 + len(name))
        hist, costs = Counter(), Counter()
        started = time.perf_counter()
        for _ in range(draws):
            values, info = sampler(rng)
            hist[tuple(values)] += 1
            for key, value in info.items():
                if isinstance(value, (int, float)):
                    costs[key] += value
        support = set(hist) | set(target_prob)
        tv = 0.5 * sum(abs(hist[x] / draws - target_prob[x]) for x in support)
        means = {k: round(v / draws, 3) for k, v in costs.items()}
        elapsed = time.perf_counter() - started
        print(name, "TV-to-full-state-reference=", round(tv, 4),
              "mean-counters=", means, "seconds=", round(elapsed, 3))
    print("states=", len(states), "stationarity-residual=", float(np.max(np.abs(pi @ P - pi))))
    large = implicit_model()
    rng = random.Random(61020261016)
    started = time.perf_counter()
    totals = Counter()
    reps = 60
    for _ in range(reps):
        _, info = sample_coordinates(large, [(3, 0, 1), (987654, 0, 1)], rng, diagnostics=True)
        for key, value in info.items():
            if isinstance(value, (int, float)):
                totals[key] += value
    print("implicit-N=1e6 local-oracle draws=", reps,
          "mean-counters=", {k: round(v/reps, 3) for k, v in totals.items()},
          "seconds=", round(time.perf_counter()-started, 3))


if __name__ == "__main__":
    main()

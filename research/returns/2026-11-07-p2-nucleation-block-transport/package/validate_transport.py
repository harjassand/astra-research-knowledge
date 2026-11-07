"""Finite implementation checks, not a proof of the nucleation endpoint."""

import hashlib
import itertools
import json
import random
import time
from fractions import Fraction
from pathlib import Path

from block_transport import (FrontierLaw, OrderedRegion, comparison_factor,
                             periodic_strip, precision_for_tv)


def fraction_record(value):
    value = Fraction(value)
    return {"numerator": str(value.numerator), "denominator": str(value.denominator),
            "approximate": float(value)}


def all_configurations(m):
    return [tuple((mask >> i) & 1 for i in range(m)) for mask in range(1 << m)]


def exact_linear_solve(matrix, rhs):
    n = len(rhs)
    a = [[Fraction(x) for x in row] + [Fraction(b)] for row, b in zip(matrix, rhs)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        scale = a[k][k]
        a[k] = [x / scale for x in a[k]]
        for i in range(n):
            if i != k and a[i][k]:
                multiplier = a[i][k]
                a[i] = [x - multiplier * y for x, y in zip(a[i], a[k])]
    return [a[i][-1] for i in range(n)]


def check_exact_frontier_and_paths():
    region = periodic_strip(4, 2, [0, 1, 1, 0], [1, 0, 1, 0],
                            Fraction(1, 4), Fraction(3, 4))
    law = FrontierLaw(region, magnetization=True)
    configurations = all_configurations(region.m)
    weights = [region.integer_weight(x) for x in configurations]
    z = sum(weights)
    coefficients = [0] * (region.m + 1)
    for x, w in zip(configurations, weights):
        coefficients[sum(x)] += w
    assert z == law.z_integer
    assert tuple(coefficients) == law.coefficients
    assert law.normalizer == Fraction(z, region.common_denominator)
    umbrella = [Fraction(1, j + 1) for j in range(region.m + 1)]
    enumerated_umbrella = sum((Fraction(w) * umbrella[sum(x)]
                              for x, w in zip(configurations, weights)), Fraction(0))
    assert law.umbrella_normalizer(umbrella) == enumerated_umbrella / region.common_denominator

    # Exact finite-bit output probabilities, with no Monte Carlo test.
    bit_budget = 10
    rounded = [law.rounded_probability(x, bit_budget) for x in configurations]
    assert sum(rounded) == 1
    tv = sum(abs(p - Fraction(w, z)) for p, w in zip(rounded, weights)) / 2
    assert tv <= Fraction(region.m, 1 << bit_budget)
    fixed_count = region.m // 2
    rounded_slice = [law.rounded_probability(x, bit_budget, fixed_count)
                     for x in configurations]
    assert sum(rounded_slice) == 1
    tv_slice = sum(abs(p - (Fraction(w, coefficients[fixed_count]) if sum(x) == fixed_count else 0))
                   for x, p, w in zip(configurations, rounded_slice, weights)) / 2
    assert tv_slice <= Fraction(region.m, 1 << bit_budget)

    # Enumerate all canonical ordered-pair paths.  Store unnormalized integer
    # pair weights; this avoids approximating extremely small probabilities.
    pair_load = {}
    length_load = {}
    exchange_bound = region.u ** (-2 * law.cutwidth)
    exchange_checks = 0
    for x_mask, x in enumerate(configurations):
        for y_mask, y in enumerate(configurations):
            product = weights[x_mask] * weights[y_mask]
            state = x_mask
            length = (x_mask ^ y_mask).bit_count()
            for k in range(region.m + 1):
                prefix = (1 << k) - 1
                hybrid = (y_mask & prefix) | (x_mask & ~prefix)
                companion = (x_mask & prefix) | (y_mask & ~prefix)
                assert product <= exchange_bound * weights[hybrid] * weights[companion]
                exchange_checks += 1
                if k < region.m and x[k] != y[k]:
                    nxt = state ^ (1 << k)
                    key = (state, nxt)
                    pair_load[key] = pair_load.get(key, 0) + product
                    length_load[key] = length_load.get(key, 0) + length * product
                    state = nxt
            assert state == y_mask
    max_directed_ratio = Fraction(0)
    max_path_bound = Fraction(0)
    for (a, b), load in pair_load.items():
        directed_ratio = Fraction(load, z * min(weights[a], weights[b]))
        assert directed_ratio <= exchange_bound
        max_directed_ratio = max(max_directed_ratio, directed_ratio)
        if a < b:
            total = length_load[(a, b)] + length_load.get((b, a), 0)
            congestion = Fraction(total * (weights[a] + weights[b]),
                                  2 * z * weights[a] * weights[b])
            max_path_bound = max(max_path_bound, congestion)
            assert congestion <= law.gamma
    return {
        "sites": region.m,
        "configurations_enumerated": len(configurations),
        "ordered_pairs_enumerated": len(configurations) ** 2,
        "exchange_checks": exchange_checks,
        "cutwidth": law.cutwidth,
        "frontier_width": law.frontier_width,
        "normalizer": fraction_record(law.normalizer),
        "magnetization_coefficients_match": True,
        "umbrella_normalizer_matches": True,
        "finite_bit_tv": fraction_record(tv),
        "finite_bit_conditioned_tv": fraction_record(tv_slice),
        "finite_bit_tv_upper": fraction_record(Fraction(region.m, 1 << bit_budget)),
        "max_directed_pair_ratio": fraction_record(max_directed_ratio),
        "proved_exchange_bound": fraction_record(exchange_bound),
        "exact_path_congestion": fraction_record(max_path_bound),
        "proved_inverse_gap_bound": fraction_record(law.gamma),
        "scope": "Exact finite checks of the formulas and implementation; not a full-size Ising prediction."
    }


def conditional_region(full, block, outside_configuration):
    position = {old: new for new, old in enumerate(block)}
    edges = []
    boundary = [list(full.boundary[i]) for i in block]
    for a, b in full.edges:
        a_in, b_in = a in position, b in position
        if a_in and b_in:
            edges.append((position[a], position[b]))
        elif a_in:
            boundary[position[a]].append(outside_configuration[b])
        elif b_in:
            boundary[position[b]].append(outside_configuration[a])
    return OrderedRegion(len(block), tuple(edges), tuple(map(tuple, boundary)), full.u, full.v)


def check_global_capacity_comparison():
    full = periodic_strip(3, 2, [0, 0, 0], [0, 0, 0],
                          Fraction(1, 8), Fraction(15, 16))
    m = full.m
    states = all_configurations(m)
    weights = [full.integer_weight(x) for x in states]
    count = len(states)
    physical = [[Fraction(0) for _ in range(count)] for _ in range(count)]
    for x in range(count):
        for i in range(m):
            y = x ^ (1 << i)
            physical[x][y] = Fraction(weights[y], weights[x] + weights[y])
        physical[x][x] = -sum(physical[x])
    augmented = [row[:] for row in physical]
    blocks = [(0, 1), (2, 3), (4, 5)]
    records = []
    for block in blocks:
        clock = Fraction(1, 3)
        sample_law = FrontierLaw(conditional_region(full, block, states[0]))
        records.append((block, clock, sample_law))
        mask = sum(1 << i for i in block)
        for x in range(count):
            possible = [y for y in range(count) if (x & ~mask) == (y & ~mask)]
            denominator = sum(weights[y] for y in possible)
            for y in possible:
                if y != x:
                    rate = clock * Fraction(weights[y], denominator)
                    augmented[x][y] += rate
                    augmented[x][x] -= rate
    lam = comparison_factor(m, records)
    for generator in (physical, augmented):
        for x in range(count):
            assert sum(generator[x]) == 0
            for y in range(count):
                assert weights[x] * generator[x][y] == weights[y] * generator[y][x]

    core = [x for x in range(count) if sum(states[x]) <= 1]
    transient = [x for x in range(count) if sum(states[x]) < 3]
    index = {x: i for i, x in enumerate(transient)}
    kappa = Fraction(1, 32)
    z_core = sum(weights[x] for x in core)
    result = []
    for generator in (physical, augmented):
        killed = [[-generator[x][y] for y in transient] for x in transient]
        source_matrix = [row[:] for row in killed]
        rhs = [kappa if x in core else Fraction(0) for x in transient]
        for x in core:
            source_matrix[index[x]][index[x]] += kappa
        psi = exact_linear_solve(source_matrix, rhs)
        means = exact_linear_solve(killed, [1] * len(transient))
        capacity = kappa * sum(weights[x] * (1 - psi[index[x]]) for x in core)
        rho = capacity / z_core
        q_at_minimum = 1 - psi[index[0]]
        assert q_at_minimum <= rho / kappa
        assert means[index[0]] == max(means)
        assert means[index[0]] >= 1 / rho - 1 / kappa
        result.append({"capacity": capacity, "rho": rho,
                       "soft_escape_at_minimum": q_at_minimum, "mean_from_minimum": means[index[0]]})
    assert result[0]["capacity"] <= result[1]["capacity"] <= lam * result[0]["capacity"]
    assert result[1]["soft_escape_at_minimum"] <= lam * result[0]["rho"] / kappa
    scaled_clock = kappa / lam
    scaled_matrix = [[-physical[x][y] for y in transient] for x in transient]
    scaled_rhs = [scaled_clock if x in core else Fraction(0) for x in transient]
    for x in core:
        scaled_matrix[index[x]][index[x]] += scaled_clock
    scaled_psi = exact_linear_solve(scaled_matrix, scaled_rhs)
    scaled_capacity = scaled_clock * sum(weights[x] * (1 - scaled_psi[index[x]]) for x in core)
    assert result[1]["capacity"] <= lam * scaled_capacity
    assert result[1]["soft_escape_at_minimum"] <= lam * scaled_capacity / (kappa * z_core)
    return {
        "sites": m, "states": count, "transient_states": len(transient),
        "weight_normalization": "Integer weights D*w; capacities are multiplied by D, while C/Z_A and physical times are invariant.",
        "common_weight_multiplier_D": str(full.common_denominator),
        "core": "at most one plus spin", "target": "at least three plus spins",
        "per_site_proposal_rate": 1, "block_clocks": "three fixed two-site blocks, rate 1/3 each",
        "kappa": fraction_record(kappa), "Lambda": fraction_record(lam),
        "physical": {k: fraction_record(v) for k, v in result[0].items()},
        "augmented": {k: fraction_record(v) for k, v in result[1].items()},
        "capacity_ratio": fraction_record(result[1]["capacity"] / result[0]["capacity"]),
        "rescaled_physical_source_clock": fraction_record(scaled_clock),
        "rescaled_physical_capacity": fraction_record(scaled_capacity),
        "rescaled_source_comparison_checked": True,
        "scope": "Six-site cylinder with pinned exterior, not the growing-volume torus endpoint."
    }


def check_long_strip():
    length, width = 128, 3
    region = periodic_strip(length, width,
                            [(i // 7) % 2 for i in range(length)],
                            [((i + 3) // 11) % 2 for i in range(length)],
                            Fraction(1, 4096), Fraction(255, 256))
    start = time.perf_counter()
    law = FrontierLaw(region)
    construction_seconds = time.perf_counter() - start
    eta = Fraction(1, 10 ** 6)
    b = precision_for_tv(region.m, eta)
    rng = random.Random(20261107)
    start = time.perf_counter()
    sample = law.sample(rng.getrandbits, b)
    sample_seconds = time.perf_counter() - start
    assert len(sample) == region.m
    assert law.cutwidth <= 2 * width + 1
    assert law.frontier_width <= 2 * width
    assert law.z_integer.bit_length() <= region.integer_bit_bound
    payload = law.z_integer.to_bytes((law.z_integer.bit_length() + 7) // 8, "big")
    return {
        "length": length, "width": width, "sites": region.m,
        "configurations_represented": "2^384",
        "supplied_frozen_boundary": "explicit mixed top and bottom spins; generated deterministically in this test",
        "u": "1/4096", "v": "255/256",
        "cutwidth": law.cutwidth, "frontier_width": law.frontier_width,
        "number_of_scalar_messages": sum(map(len, law.messages)),
        "normalizer_integer_bits": law.z_integer.bit_length(),
        "normalizer_integer_sha256": hashlib.sha256(payload).hexdigest(),
        "proved_integer_bit_bound": region.integer_bit_bound,
        "random_bits_per_sample": region.m * b,
        "tv_error_bound": fraction_record(Fraction(region.m, 1 << b)),
        "sample_plus_count": sum(sample),
        "construction_seconds_observed": construction_seconds,
        "sampling_seconds_observed": sample_seconds,
        "scope": "A representation check under frozen exterior; PRNG values are not scientific randomness or physical trajectories."
    }


def check_count_conditioned_strip():
    length, width = 16, 3
    region = periodic_strip(length, width, [0] * length, [1] * length,
                            Fraction(1, 4096), Fraction(255, 256))
    start = time.perf_counter()
    law = FrontierLaw(region, magnetization=True)
    construction_seconds = time.perf_counter() - start
    count = 24
    eta = Fraction(1, 10 ** 8)
    bits = precision_for_tv(region.m, eta)
    rng = random.Random(1722)
    samples = [law.sample(rng.getrandbits, bits, count) for _ in range(16)]
    assert all(sum(x) == count for x in samples)
    exact_samples = [law.sample_exact(rng.getrandbits, count) for _ in range(16)]
    assert all(sum(x) == count for x in exact_samples)
    assert all(x > 0 for x in law.coefficients)
    return {
        "length": length, "width": width, "sites": region.m,
        "cutwidth": law.cutwidth, "frontier_width": law.frontier_width,
        "number_of_integer_coefficient_entries": sum(len(p) for layer in law.count_messages for p in layer),
        "conditioned_plus_count": count,
        "conditioned_event_probability": fraction_record(law.count_probability([count])),
        "sample_count": len(samples), "all_counts_exact": True,
        "exact_expected_work_sampler_count": len(exact_samples),
        "random_bits_per_sample": region.m * bits,
        "tv_error_bound": fraction_record(Fraction(region.m, 1 << bits)),
        "construction_seconds_observed": construction_seconds,
        "scope": "An exactly normalized fixed-magnetization law on a supplied strip; no claim about physical relaxation of that constrained ensemble."
    }


def main():
    start = time.perf_counter()
    validation = {
        "status": "All listed checks passed; central 2D predictor remains unresolved",
        "exact_frontier_and_path_checks": check_exact_frontier_and_paths(),
        "global_comparison_check": check_global_capacity_comparison(),
        "long_strip": check_long_strip(),
        "count_conditioned_strip": check_count_conditioned_strip(),
    }
    validation["total_seconds_observed"] = time.perf_counter() - start
    destination = Path(__file__).with_name("VALIDATION.json")
    destination.write_text(json.dumps(validation, indent=2) + "\n")
    print(json.dumps({
        "status": validation["status"],
        "total_seconds_observed": validation["total_seconds_observed"],
        "path_checks": validation["exact_frontier_and_path_checks"]["exchange_checks"],
        "long_strip_sites": validation["long_strip"]["sites"],
        "scalar_messages": validation["long_strip"]["number_of_scalar_messages"],
        "capacity_ratio": validation["global_comparison_check"]["capacity_ratio"]["approximate"],
        "output": str(destination),
    }, indent=2))


if __name__ == "__main__":
    main()


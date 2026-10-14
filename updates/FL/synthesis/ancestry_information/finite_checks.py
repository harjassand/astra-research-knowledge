#!/usr/bin/env python3
"""Exact finite checks for the four-carbon E/O ancestry witness.

Uses only Python's standard library. This is a derived fixture, not copied from
the source packet and not an experimental model.
"""
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from math import comb, exp, log
from pathlib import Path


def parity_vectors(parity):
    return [x for x in product((0, 1), repeat=4) if sum(x) % 2 == parity]


def count_law(bits, parity, contrast):
    """Whole-product K law for a five-node normalized input mask."""
    u = [Fraction(2 * bit - 1) for bit in bits]
    out = [Fraction(0) for _ in range(5)]
    histories = parity_vectors(parity)
    for x in histories:
        pmf = [Fraction(1)]
        for j, bit in enumerate(x):
            p = (1 + contrast * u[j + bit]) / 2
            next_pmf = [Fraction(0) for _ in range(len(pmf) + 1)]
            for k, mass in enumerate(pmf):
                next_pmf[k] += mass * (1 - p)
                next_pmf[k + 1] += mass * p
            pmf = next_pmf
        for k, mass in enumerate(pmf):
            out[k] += mass / len(histories)
    return out


def marginal_laws():
    laws = []
    for parity in (0, 1):
        law = {}
        xs = parity_vectors(parity)
        for size in (1, 2, 3):
            for coordinates in combinations(range(4), size):
                for values in product((0, 1), repeat=size):
                    count = sum(
                        tuple(x[j] for j in coordinates) == values for x in xs
                    )
                    law[(coordinates, values)] = Fraction(count, len(xs))
        laws.append(law)
    assert laws[0] == laws[1]
    assert len(laws[0]) == 8 + 24 + 32
    return len(laws[0])


def permutation_parity(values):
    locations = {value: index for index, value in enumerate((0, 1, 5))}
    perm = [locations[value] for value in values]
    inversions = sum(
        perm[i] > perm[j]
        for i in range(len(perm))
        for j in range(i + 1, len(perm))
    )
    return inversions % 2


def count_law_from_occupancies(occupancies, high_mask, p_low, p_high):
    out = [Fraction(0) for _ in range(7)]
    for counts in occupancies:
        pmf = [Fraction(1)]
        for node, count in enumerate(counts):
            p = p_high if (high_mask >> node) & 1 else p_low
            for _ in range(count):
                next_pmf = [Fraction(0) for _ in range(len(pmf) + 1)]
                for k, mass in enumerate(pmf):
                    next_pmf[k] += mass * (1 - p)
                    next_pmf[k + 1] += mass * p
                pmf = next_pmf
        for k, mass in enumerate(pmf):
            out[k] += mass / len(occupancies)
    return out


def adjacent_pair_length(counts):
    ages = [node for node, count in enumerate(counts) for _ in range(count)]
    return sum(ages[j + 1] - ages[j] for j in range(0, len(ages), 2))


def main():
    contrast = Fraction(49, 50)
    equal_masks = []
    different_masks = []
    pulse_masks = []
    for integer in range(32):
        bits = tuple((integer >> j) & 1 for j in range(5))
        switches = sum(bits[j] != bits[j + 1] for j in range(4))
        if switches <= 2:
            pulse_masks.append("".join(map(str, bits)))
        e = count_law(bits, 0, contrast)
        o = count_law(bits, 1, contrast)
        (equal_masks if e == o else different_masks).append("".join(map(str, bits)))

    assert len(equal_masks) == 30
    assert len(different_masks) == 2
    assert len(pulse_masks) == 22
    assert set(different_masks) == {"01010", "10101"}
    assert all(mask in equal_masks for mask in pulse_masks)
    assert marginal_laws() == 64

    square_bits = (0, 1, 0, 1, 0)
    e = count_law(square_bits, 0, contrast)
    o = count_law(square_bits, 1, contrast)
    delta = [x - y for x, y in zip(e, o)]
    tv = sum(abs(x) for x in delta) / 2
    raw_parity_gap = sum(((-1) ** k) * x for k, x in enumerate(delta))
    assert sum(e) == sum(o) == 1
    assert tv == contrast**4
    assert raw_parity_gap == 2 * contrast**4
    assert (1 - tv) / 2 == (1 - contrast**4) / 2

    occupancy_even = [
        values for values in permutations((0, 1, 5))
        if permutation_parity(values) == 0
    ]
    occupancy_odd = [
        values for values in permutations((0, 1, 5))
        if permutation_parity(values) == 1
    ]
    low = Fraction(1, 100)
    high = Fraction(99, 100)
    binary_control_equal = []
    for mask in range(8):
        e_binary = count_law_from_occupancies(occupancy_even, mask, low, high)
        o_binary = count_law_from_occupancies(occupancy_odd, mask, low, high)
        binary_control_equal.append(e_binary == o_binary)
    assert all(binary_control_equal)
    assert len(occupancy_even) == len(occupancy_odd) == 3
    assert (0, 1, 5) in occupancy_even
    assert (0, 1, 5) not in occupancy_odd
    even_lengths = sorted(adjacent_pair_length(v) for v in occupancy_even)
    odd_lengths = sorted(adjacent_pair_length(v) for v in occupancy_odd)
    assert even_lengths == odd_lengths

    tau = 1
    r = 2
    x = exp(-2 * r * tau)
    q_even = (1 + 6 * x**2 + x**4) / 8
    q_odd = (x + x**3) / 2
    q_gap = q_even - q_odd

    n = 4
    grid_nodes = 5
    ancestry_atoms = comb(grid_nodes + n - 1, n)
    independent_bins_per_readout = n
    min_readouts = (ancestry_atoms - 1 + n - 1) // n

    # Two deterministic histories wholly before a finite observation start.
    # Their K laws are identical whenever the pre-start feed is constant.
    q_old_near = exp(-2 * r * (2 * tau))
    q_old_far = exp(-2 * r * (20 * tau))

    results = {
        "schema": "fl-ancestry-identifiability-checks/1",
        "scope": "Exact finite support and arithmetic fixtures only; not experimental data or an external proof review.",
        "assumptions": {
            "atom_count": 4,
            "ages": "A_j = C + j*tau + tau*X_j for j=0,1,2,3",
            "models": "X uniform on even or odd four-bit parity class",
            "label_model": "conditional independent Bernoulli labels with p=(1+a*u)/2",
            "contrast": str(contrast),
            "common_delay": "arbitrary and common to the four atoms",
        },
        "proper_coordinate_subsets_checked": 14,
        "low_order_marginal_pattern_probabilities_checked": marginal_laws(),
        "five_node_binary_masks_checked": 32,
        "masks_with_identical_whole_product_count_laws": equal_masks,
        "masks_with_different_whole_product_count_laws": different_masks,
        "masks_with_at_most_two_internal_switches": len(pulse_masks),
        "all_masks_with_at_most_two_switches_are_indistinguishable": True,
        "square_wave_even_count_probabilities": [str(v) for v in e],
        "square_wave_odd_count_probabilities": [str(v) for v in o],
        "square_wave_count_probability_difference": [str(v) for v in delta],
        "square_wave_total_variation_exact": str(tv),
        "square_wave_total_variation_float": float(tv),
        "square_wave_raw_parity_gap_exact": str(raw_parity_gap),
        "square_wave_raw_parity_gap_float": float(raw_parity_gap),
        "square_wave_corrected_parity_gap_exact": str(raw_parity_gap / contrast**4),
        "one_product_even_odd_classifier_error_exact": str((1 - tv) / 2),
        "one_product_even_odd_classifier_error_float": float((1 - tv) / 2),
        "square_wave_kl_even_to_odd_nats_float": sum(
            float(pk) * log(float(pk / qk)) for pk, qk in zip(e, o)
        ),
        "two_level_full_law_witness": {
            "atom_count": 6,
            "age_grid_tau_units": [0, 1, 2],
            "even_permutation_occupancies": [list(v) for v in occupancy_even],
            "odd_permutation_occupancies": [list(v) for v in occupancy_odd],
            "binary_waveforms_checked": 8,
            "all_binary_waveforms_give_same_whole_count_laws": all(binary_control_equal),
            "history_event_probability_even": "1/3",
            "history_event_probability_odd": "0",
            "target": "indicator of the occupancy history (0,1,5)",
            "L6_values_tau_units_even": even_lengths,
            "L6_values_tau_units_odd": odd_lengths,
            "telegraph_Q6_distribution_is_same": even_lengths == odd_lengths,
        },
        "telegraph_at_rtau_2": {
            "switch_rate": 2.0,
            "q_even_float": q_even,
            "q_odd_float": q_odd,
            "corrected_parity_gap_float": q_gap,
        },
        "finite_grid_full_law_lower_bound": {
            "grid_nodes": grid_nodes,
            "unordered_histories": ancestry_atoms,
            "independent_probabilities_per_full_count_histogram": independent_bins_per_readout,
            "minimum_one_time_readouts_by_dimension": min_readouts,
            "formula": "J*n >= binomial(q+n-1,n)-1",
        },
        "finite_prehistory_witness": {
            "histories_tau_units": [[-4, -3, -2, -1], [-40, -30, -20, -10]],
            "same_observed_count_law_if_all_entries_precede_control": "Binomial(4,p0)",
            "L4_tau_units": [2, 20],
            "Q4_at_rtau_2_float": [q_old_near, q_old_far],
        },
        "checks": {
            "parity_laws_sum_to_one": True,
            "rectangular_single_pulse_masks_indistinguishable": True,
            "alternating_masks_distinguishable": True,
            "square_wave_total_variation_equals_a4": True,
        },
    }
    output = Path(__file__).with_name("finite_results.json")
    output.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reproducible finite checks for the R1 prefix-Bell reservoir calculations.

Run with Python 3.9 or newer; no third-party packages are required:
    python3 verify_finite_models.py

The default JSON output is verification_results.json next to this script.
All phase probabilities and trace distances below use fractions.Fraction.
Entropies use double-precision natural logarithms and an explicit tolerance.
These finite checks are not a proof of the universal resource theorem, the
formula for relative entropy of entanglement, or historical novelty.

Model: rho_k = Phi_d**tensor(k) tensor chi_d**tensor(M-k), where chi_d
is the uniform maximally correlated dephased state.  In the orthonormal
Bell-phase basis z in {0,...,d-1}**M,
    p(z) = sum_k w_k d**(-(M-k)) 1[z_1=...=z_k=0].
The shift emits the first j sites, shifts the rest left, and appends j chi_d
sites.  E_R is evaluated from the proved maximally correlated identity
E_R = M log(d) - H(p); it is not obtained by a numerical optimization.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys


TOL = 2e-10
CHECKS = Counter()


def require(condition, name):
    CHECKS[name] += 1
    if not condition:
        raise AssertionError(name)


def close(left, right, name, tolerance=TOL):
    require(abs(left - right) <= tolerance, name)


def encode_fraction(value):
    value = Fraction(value)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def uniform_weights(prefixes):
    prefixes = list(prefixes)
    require(len(prefixes) > 0, "nonempty_prefix_family")
    weight = Fraction(1, len(prefixes))
    result = defaultdict(Fraction)
    for prefix in prefixes:
        result[prefix] += weight
    return dict(result)


def leading_zeros(z):
    result = 0
    for value in z:
        if value:
            break
        result += 1
    return result


def validate_weights(d, memory_sites, weights):
    require(d >= 2, "valid_local_dimension")
    require(all(0 <= k <= memory_sites for k in weights), "valid_prefix_lengths")
    require(all(value >= 0 for value in weights.values()), "nonnegative_weights")
    require(sum(weights.values(), Fraction()) == 1, "normalized_weights")


def phase_distribution(d, memory_sites, weights):
    """Direct exact enumeration, independent of the grouped-spectrum method."""
    validate_weights(d, memory_sites, weights)
    result = {}
    for z in itertools.product(range(d), repeat=memory_sites):
        zeros = leading_zeros(z)
        probability = sum(
            (weight / d ** (memory_sites - k)
             for k, weight in weights.items() if k <= zeros),
            Fraction(),
        )
        if probability:
            result[z] = probability
    require(sum(result.values(), Fraction()) == 1, "enumerated_spectrum_normalized")
    return result


def grouped_spectrum(d, memory_sites, weights):
    """Exact eigenvalue multiplicities, grouped by the initial zero run."""
    validate_weights(d, memory_sites, weights)
    result = Counter()
    for zeros in range(memory_sites + 1):
        count = 1 if zeros == memory_sites else (d - 1) * d ** (memory_sites - zeros - 1)
        probability = sum(
            (weight / d ** (memory_sites - k)
             for k, weight in weights.items() if k <= zeros),
            Fraction(),
        )
        if probability:
            result[probability] += count
    require(sum((p * count for p, count in result.items()), Fraction()) == 1,
            "grouped_spectrum_normalized")
    return result


def entropy_distribution(distribution):
    return math.fsum(-float(p) * math.log(float(p)) for p in distribution.values() if p)


def entropy_spectrum(spectrum):
    return math.fsum(-count * float(p) * math.log(float(p))
                     for p, count in spectrum.items() if p)


def entanglement_and_conditional_entropy(d, memory_sites, weights, spectrum):
    hz = entropy_spectrum(spectrum)
    hk = entropy_distribution(weights)
    mean_prefix = sum((k * w for k, w in weights.items()), Fraction())
    h_z_given_k = float(memory_sites - mean_prefix) * math.log(d)
    h_k_given_z = hk + h_z_given_k - hz
    relative_entropy = memory_sites * math.log(d) - hz
    close(relative_entropy, float(mean_prefix) * math.log(d) - hk + h_k_given_z,
          "relative_entropy_conditional_identity")
    require(h_k_given_z >= -TOL, "conditional_entropy_nonnegative")
    return relative_entropy, h_k_given_z


def conditional_entropy_direct(d, memory_sites, weights, distribution):
    """Compute H(K|Z) from posteriors, rather than by the entropy identity."""
    result = 0.0
    for z, pz in distribution.items():
        zeros = leading_zeros(z)
        for k, weight in weights.items():
            if k <= zeros:
                joint = weight / d ** (memory_sites - k)
                result -= float(joint) * math.log(float(joint / pz))
    return result


def half_trace_distance(left, right):
    """Commuting density operators: exactly the classical total variation."""
    return sum((abs(left.get(z, Fraction()) - right.get(z, Fraction()))
                for z in set(left) | set(right)), Fraction()) / 2


def shift_memory_distribution(d, memory_sites, distribution, emitted_sites):
    require(0 <= emitted_sites <= memory_sites, "valid_shift_size")
    result = defaultdict(Fraction)
    divisor = d ** emitted_sites
    tails = list(itertools.product(range(d), repeat=emitted_sites))
    for z, probability in distribution.items():
        for tail in tails:
            result[z[emitted_sites:] + tail] += probability / divisor
    return dict(result)


def shifted_weights(weights, emitted_sites):
    result = defaultdict(Fraction)
    for k, weight in weights.items():
        result[max(k - emitted_sites, 0)] += weight
    return dict(result)


def joint_output_memory_distribution(d, distribution, emitted_sites):
    result = defaultdict(Fraction)
    tails = list(itertools.product(range(d), repeat=emitted_sites))
    for z, probability in distribution.items():
        for tail in tails:
            result[(z[:emitted_sites], z[emitted_sites:] + tail)] += probability / d ** emitted_sites
    require(sum(result.values(), Fraction()) == 1, "joint_state_normalized")
    return dict(result)


def marginal(joint, position):
    result = defaultdict(Fraction)
    for key, probability in joint.items():
        result[key[position]] += probability
    return dict(result)


def product_distribution(left, right):
    return {(a, b): pa * pb for a, pa in left.items() for b, pb in right.items()}


def conditional_bound(d):
    return -math.log(1 - 1 / d) + math.log(d) / (d - 1)


def lower_resource_check(relative_entropy, bell_block_dimension, delta):
    require(0 < delta <= 1, "return_error_in_range")
    block_log_dimension = math.log(bell_block_dimension)
    n = (delta.denominator + delta.numerator - 1) // delta.numerator
    mass_sum = sum((max(Fraction(), 1 - i * delta) for i in range(n)), Fraction())
    triangular_sum = n - delta * n * (n - 1) / 2
    require(mass_sum == triangular_sum, "positive_triangular_mass_sum")
    require(all(1 - i * delta > 0 for i in range(n)), "positive_retained_masses")
    require(1 - n * delta <= 0, "first_nonpositive_mass_after_ceiling")
    lower_bound = block_log_dimension * float(mass_sum) - math.log(n)
    require(relative_entropy + TOL >= lower_bound, "resource_lower_bound_on_finite_model")
    optimized_bound = -math.inf
    optimizing_n = None
    for trial_n in range(1, n + 1):
        trial_sum = trial_n - delta * trial_n * (trial_n - 1) / 2
        penalty_argument = 1 + (trial_n - 1) * (1 - Fraction(1, bell_block_dimension))
        trial_bound = block_log_dimension * float(trial_sum) - math.log(float(penalty_argument))
        require(relative_entropy + TOL >= trial_bound,
                "stronger_nested_projector_resource_lower_bound")
        if trial_bound > optimized_bound:
            optimized_bound, optimizing_n = trial_bound, trial_n
    require(optimized_bound + TOL >= block_log_dimension,
            "optimized_bound_retains_exact_first_block_resource")
    return {
        "N_ceiling_inverse_return_error": n,
        "triangular_mass_sum": encode_fraction(mass_sum),
        "lower_bound_nats": lower_bound,
        "slack_nats": relative_entropy - lower_bound,
        "stronger_optimized_lower_bound_nats": optimized_bound,
        "stronger_optimizing_N": optimizing_n,
        "stronger_optimized_slack_nats": relative_entropy - optimized_bound,
    }


def check_repeated_output_masses(d, block_size, weights, delta):
    """Check the joint prefix-success mass, including all output correlations."""
    n = (delta.denominator + delta.numerator - 1) // delta.numerator
    success_masses = []
    for block_count in range(1, n + 1):
        total_output_sites = block_count * block_size
        success = sum((weight / d ** max(total_output_sites - k, 0)
                       for k, weight in weights.items()), Fraction())
        lower = 1 - (block_count - 1) * delta
        require(success >= lower, "joint_prefix_Bell_mass_above_linear_return_bound")
        if success_masses:
            require(success <= success_masses[-1], "joint_prefix_Bell_masses_nested")
        success_masses.append(success)
    require(success_masses[0] == 1, "first_block_Bell_mass_exactly_one")
    return {
        "tested_block_counts": n,
        "last_joint_prefix_success_mass": encode_fraction(success_masses[-1]),
        "last_linear_lower_mass": encode_fraction(1 - (n - 1) * delta),
    }


def check_block_family(d, block_size, rung_count, enumerate_phases=True):
    memory_sites = block_size * rung_count
    weights = uniform_weights(block_size * i for i in range(1, rung_count + 1))
    spectrum = grouped_spectrum(d, memory_sites, weights)
    relative_entropy, hcond = entanglement_and_conditional_entropy(d, memory_sites, weights, spectrum)
    effective_d = d ** block_size
    delta_formula = Fraction(1 - Fraction(1, effective_d ** rung_count), rung_count)
    if enumerate_phases:
        distribution = phase_distribution(d, memory_sites, weights)
        require(Counter(distribution.values()) == spectrum, "block_grouping_matches_enumeration")
        shifted = shift_memory_distribution(d, memory_sites, distribution, block_size)
        target = phase_distribution(d, memory_sites, shifted_weights(weights, block_size))
        require(shifted == target, "block_shift_matches_prefix_law")
        require(half_trace_distance(distribution, shifted) == delta_formula,
                "block_return_formula_exact")
        close(hcond, conditional_entropy_direct(d, memory_sites, weights, distribution),
              "block_conditional_entropy_direct")
    close(relative_entropy, (rung_count + 1) * math.log(effective_d) / 2
          - math.log(rung_count) + hcond, "block_resource_formula")
    require(hcond <= conditional_bound(effective_d) + TOL, "block_geometric_conditional_bound")
    resource_lower = lower_resource_check(relative_entropy, effective_d, delta_formula)
    repeated_masses = check_repeated_output_masses(d, block_size, weights, delta_formula)
    return {
        "d": d, "J": block_size, "rung_count": rung_count,
        "memory_sites": memory_sites, "phase_enumeration": enumerate_phases,
        "half_return_error": encode_fraction(delta_formula),
        "E_R_nats": relative_entropy,
        "H_K_given_Z_nats": hcond,
        "conditional_entropy_bound_nats": conditional_bound(effective_d),
        "resource_lower_bound_check": resource_lower,
        "joint_repeated_output_mass_check": repeated_masses,
    }


def check_contiguous_family(d, block_size, prefix_count):
    require(prefix_count >= block_size, "contiguous_L_at_least_J")
    memory_sites = block_size + prefix_count - 1
    weights = uniform_weights(range(block_size, block_size + prefix_count))
    spectrum = grouped_spectrum(d, memory_sites, weights)
    distribution = phase_distribution(d, memory_sites, weights)
    require(Counter(distribution.values()) == spectrum, "contiguous_grouping_matches_enumeration")
    relative_entropy, hcond = entanglement_and_conditional_entropy(d, memory_sites, weights, spectrum)
    close(hcond, conditional_entropy_direct(d, memory_sites, weights, distribution),
          "contiguous_conditional_entropy_direct")
    close(relative_entropy, (block_size + (prefix_count - 1) / 2) * math.log(d)
          - math.log(prefix_count) + hcond, "contiguous_resource_formula")
    require(hcond <= conditional_bound(d) + TOL, "contiguous_geometric_conditional_bound")
    returns = []
    for emitted in range(1, block_size + 1):
        shifted = shift_memory_distribution(d, memory_sites, distribution, emitted)
        target = phase_distribution(d, memory_sites, shifted_weights(weights, emitted))
        require(shifted == target, "contiguous_shift_matches_prefix_law")
        delta = half_trace_distance(distribution, shifted)
        expected = Fraction(emitted, prefix_count) - Fraction(
            d ** emitted - 1, prefix_count * (d - 1) * d ** prefix_count)
        require(delta == expected, "contiguous_return_formula_exact")
        # The positive spectral part is on this precise common-prefix event.
        positive_event_length = block_size + prefix_count - emitted
        for z in set(distribution) | set(shifted):
            difference = distribution.get(z, Fraction()) - shifted.get(z, Fraction())
            event = all(value == 0 for value in z[:positive_event_length])
            require((difference >= 0 if event else difference <= 0),
                    "contiguous_positive_spectral_event")
        returns.append({"emitted_sites": emitted, "half_return_error": encode_fraction(delta)})
    resource_lower = lower_resource_check(relative_entropy, d ** block_size, delta)
    repeated_masses = check_repeated_output_masses(d, block_size, weights, delta)
    return {
        "d": d, "J": block_size, "L": prefix_count, "memory_sites": memory_sites,
        "E_R_nats": relative_entropy, "H_K_given_Z_nats": hcond,
        "conditional_entropy_bound_nats": conditional_bound(d), "returns": returns,
        "resource_lower_bound_check": resource_lower,
        "joint_repeated_output_mass_check": repeated_masses,
    }


def check_joint_correlations():
    d, block_size, rung_count = 2, 1, 4
    memory_sites = block_size * rung_count
    weights = uniform_weights(range(1, rung_count + 1))
    distribution = phase_distribution(d, memory_sites, weights)
    results = []
    for emitted in (1, 2, 3):
        joint = joint_output_memory_distribution(d, distribution, emitted)
        output = marginal(joint, 0)
        memory = marginal(joint, 1)
        expected_memory = shift_memory_distribution(d, memory_sites, distribution, emitted)
        require(memory == expected_memory, "joint_memory_marginal_matches_shift")
        output_error = half_trace_distance(output, {(0,) * emitted: Fraction(1)})
        expected_fidelity = sum(
            (weight / d ** max(emitted - k, 0) for k, weight in weights.items()), Fraction())
        require(output_error == 1 - expected_fidelity, "joint_output_Bell_error_exact")
        correlation = half_trace_distance(joint, product_distribution(output, memory))
        site_marginals = []
        for site in range(emitted):
            values = defaultdict(Fraction)
            for z, probability in output.items():
                values[z[site]] += probability
            site_marginals.append(dict(values))
        independent_output = {}
        for z in itertools.product(range(d), repeat=emitted):
            probability = Fraction(1)
            for site, value in enumerate(z):
                probability *= site_marginals[site].get(value, Fraction())
            if probability:
                independent_output[z] = probability
        inter_output_correlation = half_trace_distance(output, independent_output)
        if emitted <= block_size:
            require(output_error == 0 and correlation == 0,
                    "first_J_outputs_exact_pure_and_decoupled")
        if emitted == 3:
            require(correlation > 0, "later_output_memory_correlations_present")
            require(inter_output_correlation > 0, "later_inter_output_correlations_present")
        results.append({
            "emitted_sites": emitted, "joint_output_Bell_half_error": encode_fraction(output_error),
            "output_memory_half_distance_from_product": encode_fraction(correlation),
            "inter_output_half_distance_from_product": encode_fraction(inter_output_correlation),
        })
    return {"d": d, "J": block_size, "rung_count": rung_count, "results": results}


def check_false_candidate():
    """The c_2 bound gives an exact rational disproof of m <= 2 delta R."""
    result = []
    for exponent in (3, 4, 5, 7):
        rung_count = 2 ** exponent
        row = check_block_family(2, 1, rung_count, enumerate_phases=(rung_count <= 8))
        delta = Fraction(1 - Fraction(1, 2 ** rung_count), rung_count)
        # c_2 = 2 log 2 and log(rung_count) = exponent log 2.
        upper_R_over_log2 = Fraction(rung_count + 5, 2) - exponent
        upper_ratio = 2 * delta * upper_R_over_log2
        require(upper_ratio < 1, "false_candidate_violated_by_exact_rational_upper_bound")
        actual_ratio = 2 * float(delta) * row["E_R_nats"] / math.log(2)
        require(actual_ratio <= float(upper_ratio) + TOL,
                "actual_counterexample_below_certified_upper_ratio")
        result.append({
            "d": 2, "J": 1, "rung_count": rung_count,
            "half_return_error": encode_fraction(delta), "E_R_nats": row["E_R_nats"],
            "actual_2_delta_R_over_m": actual_ratio,
            "exact_upper_bound_2_delta_R_over_m": encode_fraction(upper_ratio),
            "upper_E_R_over_log2": encode_fraction(upper_R_over_log2),
        })
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().with_name("verification_results.json"))
    args = parser.parse_args()
    blocks = []
    for d in (2, 3):
        for block_size in (1, 2):
            for rung_count in (1, 2, 3, 4):
                if d ** (block_size * rung_count) <= 20000:
                    blocks.append(check_block_family(d, block_size, rung_count))
    contiguous = []
    for d in (2, 3):
        for block_size in (1, 2, 3):
            for prefix_count in range(block_size, 7):
                if d ** (block_size + prefix_count - 1) <= 20000:
                    contiguous.append(check_contiguous_family(d, block_size, prefix_count))
    joint = check_joint_correlations()
    false_candidate = check_false_candidate()
    result = {
        "status": "PASS",
        "scope": "Finite-model arithmetic checks; not a universal proof or novelty assessment.",
        "conventions": {
            "return_error": "one half of trace norm",
            "entanglement_units": "nats; natural logarithms",
            "resource": "E_R across all retained Alice and Bob reservoir registers",
            "probability_arithmetic": "exact fractions.Fraction",
            "entropy_arithmetic": "Python float with absolute tolerance 2e-10 nats",
            "relative_entropy_identity": "E_R=M ln d-H(Bell-phase spectrum), from the maximally correlated theorem",
        },
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": sys.version.split()[0],
        "total_assertions": sum(CHECKS.values()),
        "assertions_by_type": dict(sorted(CHECKS.items())),
        "enumerated_block_family_count": len(blocks),
        "enumerated_contiguous_family_count": len(contiguous),
        "block_families": blocks,
        "contiguous_families": contiguous,
        "full_joint_output_memory_check": joint,
        "false_candidate_m_le_2_delta_R_counterexamples": false_candidate,
        "limitations": [
            "Finite enumeration does not prove claims for arbitrary reservoirs or LOCC devices.",
            "The maximally correlated E_R identity and universal lower bound require separate analytic proofs.",
            "Only the first J outputs are exactly Bell for each starting reservoir; later outputs can correlate with one another and memory.",
            "No experimental accessibility, energy constraint, efficient implementation, or historical novelty is established.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"], "total_assertions": result["total_assertions"],
        "block_families": len(blocks), "contiguous_families": len(contiguous),
        "output": str(args.output.resolve()),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

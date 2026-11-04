#!/usr/bin/env python3
"""Counterfactual phase scheduling of measured Fig. 6 minute profiles.

This does not simulate independent observed UPS devices. The input contains
three building-level, clock-aligned weekly mean profiles over sixteen weeks.
All shifts are integer multiples of the observed 3 s sample spacing. The
200-profile calculation is explicitly a fabricated fleet made by replicating
the measured templates; it is not a measured contemporaneous population.

Dependencies: Python 3 and NumPy. Run this file with no arguments to reproduce
harmonic_results.json beside it. No source data are modified.
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

import numpy as np


DEFAULT_INPUT = Path(__file__).resolve().parent / 'data' / 'building_measured_minute_waveforms.csv'
if not DEFAULT_INPUT.exists():
    DEFAULT_INPUT = Path(__file__).resolve().parent.parent / 'grid_observations_data' / 'building_measured_minute_waveforms.csv'
DEFAULT_OUTPUT = Path(__file__).with_name("harmonic_results.json")
PERIOD_S = 60.0
SAMPLES = 20
SLOT_S = 3.0
HARMONICS = 3
REPLICA_COUNT = 200
REPLICA_SEED = 20261105


def summary(values):
    a = np.asarray(list(values), dtype=float)
    return {
        "minimum": float(a.min()),
        "median": float(np.median(a)),
        "mean": float(a.mean()),
        "maximum": float(a.max()),
    }


def load_profiles(path):
    groups = collections.defaultdict(list)
    with path.open(newline="") as stream:
        for row in csv.DictReader(stream):
            key = (row["week"], row["meter"])
            groups[key].append(
                (float(row["second"]), float(row["periodic_active_power_W"]))
            )
    profiles = {}
    raw_means = []
    for key, observations in sorted(groups.items()):
        observations = sorted(observations)
        seconds = np.array([a for a, _ in observations])
        if len(seconds) != SAMPLES or not np.allclose(
            seconds, SLOT_S * np.arange(SAMPLES), atol=0, rtol=0
        ):
            raise ValueError(f"Unexpected time samples for {key}")
        power = np.array([b for _, b in observations], dtype=float)
        raw_means.append(float(power.mean()))
        # Remove only numerical DC residues (~1e-10 W in this file).
        profiles[key] = power - power.mean()
    weeks = sorted({key[0] for key in profiles})
    meters = sorted({key[1] for key in profiles})
    if len(weeks) != 16 or len(meters) != 3 or len(profiles) != 48:
        raise ValueError("Expected 16 weeks x 3 building meters")
    if any((week, meter) not in profiles for week in weeks for meter in meters):
        raise ValueError("Missing building/week profile")
    return profiles, weeks, meters, raw_means


def coefficients(profile_matrix, harmonics=HARMONICS):
    return np.fft.fft(profile_matrix, axis=-1)[..., 1 : harmonics + 1] / SAMPLES


def phase_characters(harmonics=HARMONICS):
    return np.exp(
        -2j
        * np.pi
        * np.arange(SAMPLES)[:, None]
        * np.arange(1, harmonics + 1)[None, :]
        / SAMPLES
    )


def shifted_total(profile_matrix, slots):
    return sum(
        (np.roll(profile, int(slot)) for profile, slot in zip(profile_matrix, slots)),
        np.zeros(SAMPLES),
    )


def metrics(profile_matrix, slots, harmonics=HARMONICS):
    total = shifted_total(profile_matrix, slots)
    c = np.fft.fft(total) / SAMPLES
    coeff_square = float(np.sum(np.abs(c[1 : harmonics + 1]) ** 2))
    full_square = float(np.mean(total**2))
    parseval_square = float(
        abs(c[0]) ** 2
        + 2 * np.sum(np.abs(c[1 : SAMPLES // 2]) ** 2)
        + abs(c[SAMPLES // 2]) ** 2
    )
    if not math.isclose(full_square, parseval_square, rel_tol=2e-12, abs_tol=1e-8):
        raise AssertionError("Parseval factor/Nyquist check failed")
    return {
        "phase_slots": [int(x) for x in slots],
        "phase_offsets_seconds": [float(SLOT_S * x) for x in slots],
        "retained_coefficient_square_sum_W2": coeff_square,
        "retained_band_RMS_W": math.sqrt(2 * coeff_square),
        "fundamental_complex_coefficient_W": [float(c[1].real), float(c[1].imag)],
        "fundamental_coefficient_magnitude_W": float(abs(c[1])),
        "fundamental_sinusoidal_peak_W": float(2 * abs(c[1])),
        "full_sampled_waveform_RMS_W": math.sqrt(full_square),
        "full_sampled_waveform_maximum_absolute_W": float(np.max(np.abs(total))),
        "full_sampled_waveform_peak_to_peak_W": float(np.ptp(total)),
        "sampled_aggregate_waveform_W": [float(x) for x in total],
        "parseval_squared_residual_W2": float(full_square - parseval_square),
    }


def weekly_exhaustive(profiles, weeks, meters):
    phase = phase_characters()
    candidate_slots = np.array(
        [(0, a, b) for a, b in itertools.product(range(SAMPLES), repeat=2)],
        dtype=int,
    )
    rows = []
    for week in weeks:
        waveforms = np.array([profiles[(week, meter)] for meter in meters])
        c = coefficients(waveforms)
        resultant = np.array(
            [np.sum(c * phase[slots], axis=0) for slots in candidate_slots]
        )
        scores = np.sum(np.abs(resultant) ** 2, axis=1)
        fundamental_scores = np.abs(resultant[:, 0]) ** 2
        best_k = candidate_slots[int(np.argmin(scores))]
        best_1 = candidate_slots[int(np.argmin(fundamental_scores))]
        random_expected_square = float(np.sum(np.abs(c) ** 2))
        if not math.isclose(
            float(scores.mean()), random_expected_square, rel_tol=2e-12, abs_tol=1e-8
        ):
            raise AssertionError("Uniform-phase expectation check failed")
        amplitudes = np.abs(c[:, 0])
        continuous_floor = float(max(0.0, 2 * amplitudes.max() - amplitudes.sum()))
        achieved_discrete = math.sqrt(float(fundamental_scores.min()))
        if achieved_discrete + 1e-8 < continuous_floor:
            raise AssertionError("Discrete optimum below continuous polygon bound")
        baseline = metrics(waveforms, [0, 0, 0])
        optimized = metrics(waveforms, best_k)
        rows.append(
            {
                "week_UTC": week,
                "meters_in_phase_vector_order": meters,
                "observed_individual_fundamental_magnitudes_W": {
                    meter: float(amp) for meter, amp in zip(meters, amplitudes)
                },
                "continuous_phase_fundamental_polygon_lower_bound_W": continuous_floor,
                "unshifted_measured_profile_sum": baseline,
                "exact_20_slot_optimum_K3": optimized,
                "exact_20_slot_optimum_K1": metrics(waveforms, best_1),
                "uniform_independent_random_phase_reference": {
                    "expected_retained_coefficient_square_sum_W2": random_expected_square,
                    "sqrt_expected_retained_band_RMS_squared_W": math.sqrt(
                        2 * random_expected_square
                    ),
                    "exact_expected_retained_band_RMS_W": float(
                        np.mean(np.sqrt(2 * scores))
                    ),
                    "expectation_check_residual_W2": float(
                        scores.mean() - random_expected_square
                    ),
                },
                "K3_RMS_ratio_to_unshifted": float(
                    optimized["retained_band_RMS_W"] / baseline["retained_band_RMS_W"]
                ),
                "K3_RMS_ratio_to_random_root_mean_square_reference": float(
                    optimized["retained_band_RMS_W"]
                    / math.sqrt(2 * random_expected_square)
                ),
                "K1_discrete_excess_above_continuous_floor_W": float(
                    achieved_discrete - continuous_floor
                ),
            }
        )
    # A genuine out-of-week counterfactual check: freeze the earliest week's
    # optimum, then use the other fifteen measured weeks without retuning.
    # These remain repeated observations of the same buildings, not fifteen
    # independent randomized hardware interventions.
    frozen_slots = rows[0]["exact_20_slot_optimum_K3"]["phase_slots"]
    holdout_rows = []
    for week, row in zip(weeks[1:], rows[1:]):
        waveforms = np.array([profiles[(week, meter)] for meter in meters])
        frozen = metrics(waveforms, frozen_slots)
        holdout_rows.append({
            "week_UTC": week,
            "frozen_schedule_metrics": frozen,
            "retained_band_RMS_ratio_to_unshifted": frozen["retained_band_RMS_W"]
                / row["unshifted_measured_profile_sum"]["retained_band_RMS_W"],
            "retained_band_RMS_ratio_to_week_specific_optimum": frozen["retained_band_RMS_W"]
                / row["exact_20_slot_optimum_K3"]["retained_band_RMS_W"],
        })
    aggregate = {
        "continuous_fundamental_polygon_floor_W": summary(
            row["continuous_phase_fundamental_polygon_lower_bound_W"] for row in rows
        ),
        "unshifted_retained_band_RMS_W": summary(
            row["unshifted_measured_profile_sum"]["retained_band_RMS_W"] for row in rows
        ),
        "exact_20_slot_K3_retained_band_RMS_W": summary(
            row["exact_20_slot_optimum_K3"]["retained_band_RMS_W"] for row in rows
        ),
        "exact_20_slot_K1_fundamental_magnitude_W": summary(
            row["exact_20_slot_optimum_K1"]["fundamental_coefficient_magnitude_W"]
            for row in rows
        ),
        "K3_RMS_ratio_to_unshifted": summary(row["K3_RMS_ratio_to_unshifted"] for row in rows),
        "K3_RMS_ratio_to_random_root_mean_square_reference": summary(
            row["K3_RMS_ratio_to_random_root_mean_square_reference"] for row in rows
        ),
        "K1_discrete_excess_above_continuous_floor_W": summary(
            row["K1_discrete_excess_above_continuous_floor_W"] for row in rows
        ),
        "number_of_week_specific_K3_optima_increasing_full_sampled_RMS": sum(
            row["exact_20_slot_optimum_K3"]["full_sampled_waveform_RMS_W"]
            > row["unshifted_measured_profile_sum"]["full_sampled_waveform_RMS_W"]
            for row in rows
        ),
        "number_of_week_specific_K3_optima_increasing_full_sampled_absolute_peak": sum(
            row["exact_20_slot_optimum_K3"]["full_sampled_waveform_maximum_absolute_W"]
            > row["unshifted_measured_profile_sum"]["full_sampled_waveform_maximum_absolute_W"]
            for row in rows
        ),
    }
    return {
        "interpretation": "Counterfactual shifts of the three measured building profiles, separately within each measured week.",
        "harmonic_objective_K": HARMONICS,
        "phase_slots": SAMPLES,
        "phase_spacing_seconds": SLOT_S,
        "candidates_per_week": len(candidate_slots),
        "global_phase_fixed_to_zero_for_meter": meters[0],
        "global_phase_fix_is_exact": "Every common integer-slot shift rotates each harmonic but leaves the objective invariant.",
        "summary_across_16_weeks": aggregate,
        "weekly_results": rows,
        "frozen_first_week_schedule_holdout": {
            "calibration_week_UTC": weeks[0],
            "phase_slots": frozen_slots,
            "phase_offsets_seconds": [float(SLOT_S * slot) for slot in frozen_slots],
            "holdout_weeks": len(holdout_rows),
            "status": "Out-of-week template-shift evaluation without retuning; not a physical intervention and not an independent-fleet experiment.",
            "retained_band_RMS_ratio_to_unshifted_summary": summary(
                row["retained_band_RMS_ratio_to_unshifted"] for row in holdout_rows
            ),
            "retained_band_RMS_ratio_to_week_specific_optimum_summary": summary(
                row["retained_band_RMS_ratio_to_week_specific_optimum"] for row in holdout_rows
            ),
            "weeks_worse_than_unshifted": sum(
                row["retained_band_RMS_ratio_to_unshifted"] > 1 for row in holdout_rows
            ),
            "interpretation": "A calibrated fixed schedule is not shown to remain beneficial as the measured building signatures change. The worst-case stationarity/error bill cannot be omitted.",
            "weekly_results": holdout_rows,
        },
    }


def deterministic_harmonic_assignment(c, weight_tolerance=1e-12):
    """Floating-variable elimination followed by conditional-expectation rounding.

    Exact real arithmetic gives the theorem. This implementation reports all
    numerical constraint drift and uses the final normalized fractional point
    as its rounding target, so drift is measured rather than silently ignored.
    """
    started = time.perf_counter()
    n, k = c.shape
    d = 2 * k
    phase = phase_characters(k)
    complex_vectors = c[:, None, :] * phase[None, :, :]
    v = np.empty((n, SAMPLES, d), dtype=float)
    v[:, :, 0::2] = complex_vectors.real
    v[:, :, 1::2] = complex_vectors.imag
    x = np.full((n, SAMPLES), 1 / SAMPLES)
    eliminations = 0
    largest_null_residual = 0.0
    while True:
        fractional = np.flatnonzero(np.sum(x > weight_tolerance, axis=1) > 1)
        if len(fractional) <= d:
            break
        indices = fractional[: d + 1]
        pairs = [np.flatnonzero(x[index] > weight_tolerance)[:2] for index in indices]
        matrix = np.stack(
            [v[index, pair[0]] - v[index, pair[1]] for index, pair in zip(indices, pairs)],
            axis=1,
        )
        alpha = np.linalg.svd(matrix, full_matrices=True)[2][-1]
        largest_null_residual = max(largest_null_residual, float(np.linalg.norm(matrix @ alpha)))
        upper = []
        for index, (a, b), direction in zip(indices, pairs, alpha):
            if direction > 0:
                upper.append(x[index, b] / direction)
            elif direction < 0:
                upper.append(x[index, a] / -direction)
        step = min(upper)
        for index, (a, b), direction in zip(indices, pairs, alpha):
            x[index, a] += step * direction
            x[index, b] -= step * direction
        if float(x.min()) < -1e-10:
            raise ArithmeticError("Elimination produced a materially negative weight")
        x[x < weight_tolerance] = 0.0
        eliminations += 1
        if eliminations > n * (SAMPLES - 1):
            raise ArithmeticError("Support elimination did not terminate at its bound")
    before_normalization_row_error = float(np.max(np.abs(x.sum(axis=1) - 1)))
    x /= x.sum(axis=1)[:, None]
    fractional = np.flatnonzero(np.sum(x > 0, axis=1) > 1)
    if len(fractional) > d:
        raise AssertionError("Too many fractional rows")
    b = np.einsum("nm,nmd->nd", x, v)
    target_drift = b.sum(axis=0)
    mean_squares = np.einsum("nm,nmd,nmd->n", x, v, v)
    row_variances = mean_squares - np.einsum("nd,nd->n", b, b)
    variance_sum = float(np.maximum(row_variances[fractional], 0).sum())
    rounding_bound_square = float(target_drift @ target_drift + variance_sum)
    accumulated = target_drift.copy()
    choices = np.argmax(x, axis=1)
    for index in fractional:
        options = np.flatnonzero(x[index] > 0)
        candidates = accumulated[None, :] + v[index, options] - b[index][None, :]
        winner = int(np.argmin(np.sum(candidates**2, axis=1)))
        choice = int(options[winner])
        choices[index] = choice
        accumulated = candidates[winner]
    final_vector = v[np.arange(n), choices].sum(axis=0)
    final_square = float(final_vector @ final_vector)
    verification_allowance = 1e-7 + 1e-10 * max(1.0, rounding_bound_square)
    if final_square > rounding_bound_square + verification_allowance:
        raise AssertionError("Conditional-expectation rounding certificate failed")
    individual_squares = np.sum(np.abs(c) ** 2, axis=1)
    theorem_bound_square = float(np.sort(individual_squares)[-min(n, d) :].sum())
    return choices, {
        "algorithm": "Nullspace support elimination then deterministic conditional-expectation rounding",
        "N": n,
        "K": k,
        "M": SAMPLES,
        "coupling_dimension": d,
        "support_eliminations": eliminations,
        "support_elimination_upper_bound": n * (SAMPLES - 1),
        "remaining_fractional_devices_before_rounding": int(len(fractional)),
        "fractional_device_indices": [int(x) for x in fractional],
        "maximum_row_sum_error_before_final_normalization": before_normalization_row_error,
        "maximum_nullspace_equation_residual_W": largest_null_residual,
        "fractional_aggregate_numerical_drift_W": float(np.linalg.norm(target_drift)),
        "actual_rounding_variance_sum_W2": variance_sum,
        "rounding_bound_including_numerical_target_drift_W2": rounding_bound_square,
        "coarse_largest_2K_device_theorem_bound_W2": theorem_bound_square,
        "final_coefficient_square_sum_W2": final_square,
        "final_retained_band_RMS_W": math.sqrt(2 * final_square),
        "rounding_certificate_passed": True,
        "floating_verification_allowance_W2": verification_allowance,
        "wall_time_seconds_descriptive_only": time.perf_counter() - started,
        "real_arithmetic_operation_bound": "O((N M)^2 + N M (2K)^3) for this implementation, including repeated full support scans. Maintaining an active support list reduces the scans and recovers O(N M (2K)^3) arithmetic. Neither is an exact bit-complexity claim.",
    }


def fabricated_replica_fleet(profiles):
    keys = sorted(profiles)
    indices = np.arange(REPLICA_COUNT) % len(keys)
    np.random.default_rng(REPLICA_SEED).shuffle(indices)
    waveforms = np.array([profiles[keys[int(index)]] for index in indices])
    c = coefficients(waveforms)
    phases, certificate = deterministic_harmonic_assignment(c)
    baseline = metrics(waveforms, np.zeros(REPLICA_COUNT, dtype=int))
    round_robin = metrics(waveforms, np.arange(REPLICA_COUNT) % SAMPLES)
    optimized = metrics(waveforms, phases)
    if not math.isclose(
        optimized["retained_coefficient_square_sum_W2"],
        certificate["final_coefficient_square_sum_W2"],
        rel_tol=5e-11,
        abs_tol=1e-6,
    ):
        raise AssertionError("Time-shift replay does not match Fourier-phase construction")
    expected_square = float(np.sum(np.abs(c) ** 2))
    expected_full_square = float(np.sum(np.mean(waveforms**2, axis=1)))
    counts = collections.Counter(int(index) for index in indices)
    return {
        "status": "FABRICATED COUNTERFACTUAL POPULATION; NOT AN OBSERVED FLEET",
        "construction": "Balanced replication of all 48 measured building/week templates to N=200, followed by a fixed-seed permutation. Different weeks of the same meter are reused as if independent controllable devices solely for a numerical construction check.",
        "claims_excluded": [
            "No claim that 200 such devices were measured simultaneously.",
            "No claim that a building-level profile can actually be shifted by firmware.",
            "No claim that the 48 templates are independent experimental units.",
            "No subsecond interpolation or inferred subsecond waveform structure.",
            "No physical clock/calibration uncertainty is included in this ideal template replay.",
        ],
        "N": REPLICA_COUNT,
        "shuffle_seed": REPLICA_SEED,
        "template_catalogue": [
            {
                "template_index": index,
                "week_UTC": key[0],
                "meter": key[1],
                "replica_count": counts[index],
            }
            for index, key in enumerate(keys)
        ],
        "device_template_indices_in_schedule_order": [int(x) for x in indices],
        "unshifted_template_sum": baseline,
        "equal_count_round_robin_20_slots": round_robin,
        "deterministic_harmonic_schedule": optimized,
        "algorithm_certificate": certificate,
        "uniform_independent_random_phase_reference": {
            "expected_retained_coefficient_square_sum_W2": expected_square,
            "sqrt_expected_retained_band_RMS_squared_W": math.sqrt(2 * expected_square),
            "sqrt_expected_full_sampled_waveform_RMS_squared_W": math.sqrt(expected_full_square),
            "expected_RMS_itself_not_claimed": True,
        },
        "retained_band_RMS_ratios": {
            "deterministic_to_unshifted": optimized["retained_band_RMS_W"] / baseline["retained_band_RMS_W"],
            "deterministic_to_round_robin": optimized["retained_band_RMS_W"] / round_robin["retained_band_RMS_W"],
            "deterministic_to_random_root_mean_square_reference": optimized["retained_band_RMS_W"] / math.sqrt(2 * expected_square),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    source_bytes = args.input.read_bytes()
    input_hash = hashlib.sha256(source_bytes).hexdigest()
    profiles, weeks, meters, means = load_profiles(args.input)
    results = {
        "title": "Three-second-grid counterfactual harmonic scheduling of measured minute profiles",
        "input": {
            "path": str(args.input),
            "sha256": input_hash,
            "primary_measurement_source": "Hartmann et al., Nature Energy (2026), DOI 10.1038/s41560-026-02144-0, Source Data Fig. 6, extracted to CSV by the root workflow.",
            "measured_units": "Three building-level meters; sixteen weekly mean profiles per meter; twenty samples per minute.",
            "meter_identifiers": meters,
            "weeks": weeks,
            "mean_power_removed_W": summary(means),
            "sample_period_seconds": SLOT_S,
            "routine_period_seconds": PERIOD_S,
        },
        "conventions": {
            "complex_coefficient": "c_k = FFT(profile)[k]/20",
            "real_waveform": "p(t)=c_0+2 Re sum_{k>=1} c_k exp(i k omega t), except that the discrete Nyquist coefficient is unpaired.",
            "retained_band_RMS": "sqrt(2 sum_{k=1}^3 |S_k|^2)",
            "random_comparator": "The square root of expected squared RMS is distinguished from the expectation of RMS. Both are computed exactly for the three-meter case.",
            "admissible_offsets": "0,3,...,57 seconds only; first-meter offset is fixed to zero in exhaustive search by global phase invariance.",
            "counterfactual_boundary": "Only circular shifts of the observed twenty-sample profiles are evaluated. Actual firmware access, inter-test deadlines, state-dependent waveform changes, clock/calibration errors, and between-sample extrema are not validated.",
        },
        "three_measured_locations": weekly_exhaustive(profiles, weeks, meters),
        "fabricated_200_template_replica_fleet": fabricated_replica_fleet(profiles),
    }
    if hashlib.sha256(args.input.read_bytes()).hexdigest() != input_hash:
        raise AssertionError("Input data changed during calculation")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "three_location_summary": results["three_measured_locations"]["summary_across_16_weeks"],
        "replica_algorithm_certificate": results["fabricated_200_template_replica_fleet"]["algorithm_certificate"],
        "replica_RMS_ratios": results["fabricated_200_template_replica_fleet"]["retained_band_RMS_ratios"],
    }, indent=2))


if __name__ == "__main__":
    main()

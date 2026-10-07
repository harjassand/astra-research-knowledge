"""Small reproducible deterministic and sampler demonstrations.

Run: python3 run_experiment.py
The mathematical certificates use standard-library integer arithmetic only.
mpmath is a separate high-precision cross-check; seeded sample summaries are
illustrations and never used to establish KL, TV, or compiler accuracy.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from fractions import Fraction as F
import random
import resource
import sys
import time
import tracemalloc

import mpmath as mp

from archive import (Archive, Axis, axis_kl, axis_tv, compile_dyadic_cdf,
                     dyadic_cell_probabilities, make_archive,
                     rounded_decoder_table, sample_dyadic_cdf)
from certified import (BITS, SCALE, IV, interval_json, log_interval, normal_cdf,
                       normal_constant, normal_mass, normal_pdf, pi_interval,
                       exp_neg)

BASE = Path(__file__).resolve().parent
mp.mp.dps = 400


def mpf(x):
    x = F(x)
    return mp.mpf(x.numerator) / x.denominator


def mp_mass(left, right, mean=0):
    def cdf(x):
        return mp.erfc(-(mpf(x) - mpf(mean)) / mp.sqrt(2)) / 2
    def sf(x):
        return mp.erfc((mpf(x) - mpf(mean)) / mp.sqrt(2)) / 2
    if left is None:
        return cdf(right)
    if right is None:
        return sf(left)
    if left >= mean:
        return sf(left) - sf(right)
    return cdf(right) - cdf(left)


def mp_contained(enclosure, point):
    return mpf(F(enclosure.lo, SCALE)) <= point <= mpf(F(enclosure.hi, SCALE))


def json_fraction(x):
    x = F(x)
    return f"{x.numerator}/{x.denominator}"


def simplified_interval(x):
    return {"decimal_interval": x.decimal_bounds(45), "width_decimal": mp.nstr(mpf(x.width()), 12)}


def verify_certified_primitives():
    assertions = 0
    for v in [F(-7, 3), F(-1, 7), F(0), F(1, 9), F(7, 3)]:
        for w in [F(-8, 5), F(-1, 13), F(1, 11), F(11, 5)]:
            for op, truth in [(IV.exact(v) + IV.exact(w), v + w),
                              (IV.exact(v) - IV.exact(w), v - w),
                              (IV.exact(v) * IV.exact(w), v * w),
                              (IV.exact(v) / IV.exact(w), v / w)]:
                assert op.contains(truth)
                assertions += 1
    assert mp_contained(pi_interval(), mp.pi)
    assertions += 1
    assert mp_contained(normal_constant(), 1 / mp.sqrt(2 * mp.pi))
    assertions += 1
    for x in [F(-20), F(-8), F(-3), F(-1, 7), F(0), F(1, 7), F(3), F(8), F(20)]:
        assert mp_contained(normal_cdf(x), mp.erfc(-mpf(x) / mp.sqrt(2)) / 2)
        assert mp_contained(normal_pdf(x), mp.exp(-mpf(x)**2 / 2) / mp.sqrt(2 * mp.pi))
        assertions += 2
    for x in [F(1, 1000000), F(1, 3), F(1), F(2), F(1000000)]:
        assert mp_contained(log_interval(IV.exact(x)), mp.log(mpf(x)))
        assertions += 1
    for z in [F(0), F(1, 3), F(1), F(7), F(200)]:
        assert mp_contained(exp_neg(z), mp.exp(-mpf(z)))
        assertions += 1
    # Meaningful boundary regression: outward printed CDF upper/lower values
    # must enclose an extremely small right tail, rather than both print 1.
    low, high = normal_cdf(20).decimal_bounds(20)
    assert F(low) <= F(1) - F(1, 10**90) < F(high)
    assertions += 1
    return assertions


def scalar_cases():
    cases = []
    for a, eps in [(F(3, 10), F(1, 4)), (F(1, 2), F(1, 4)),
                   (F(1), F(1, 4)), (F(2), F(1, 4)),
                   (F(4), F(1, 4)), (F(8), F(1, 2))]:
        axis = make_archive(a, 1, eps, 1).axes[0]
        for fraction in [F(1, 4), F(1, 2), F(1)]:
            theta = a * fraction
            kl, bins = axis_kl(axis, theta)
            independent = mpf(theta * theta / 2) - sum(
                mp_mass(b["left"], b["right"], theta) *
                mp.log(mp_mass(b["left"], b["right"], theta) /
                       mp_mass(b["left"], b["right"], 0)) for b in bins)
            assert mp_contained(kl, independent)
            assert kl.hi <= IV.exact(theta * theta * axis.h**2 / 4).lo
            weighted = sum((b["weighted_conditional_kl"] for b in bins), IV.exact(0))
            assert weighted.lo <= kl.hi and kl.lo <= weighted.hi
            for b in bins:
                assert b["conditional_kl"].hi <= IV.exact(b["conditional_bound"]).lo
                assert mp_contained(b["p_theta"], mp_mass(b["left"], b["right"], theta))
                assert mp_contained(b["p_reference"], mp_mass(b["left"], b["right"], 0))
            tail = normal_mass(None, -axis.T, theta) + normal_mass(axis.T, None, theta)
            assert tail.hi <= IV.exact(axis.h**2 / 4).lo
            tv = axis_tv(axis, theta) if a <= 1 else None
            cases.append({"a": json_fraction(a), "eps": json_fraction(eps),
                          "theta": json_fraction(theta), "T": json_fraction(axis.T),
                          "M": axis.M, "labels": axis.labels,
                          "width": json_fraction(axis.width),
                          "KL": simplified_interval(kl),
                          "KL_bound": json_fraction(theta * theta * axis.h**2 / 4),
                          "scalar_TV": None if tv is None else simplified_interval(tv),
                          "tail_probability": simplified_interval(tail),
                          "tail_bound": json_fraction(axis.h**2 / 4),
                          "minimum_reference_bin_mass": simplified_interval(
                              min((b["p_reference"] for b in bins), key=lambda z: z.lo)),
                          "checked_bins": len(bins)})
            print(f"scalar a={a} eps={eps} theta={theta}: {len(bins)} bins; KL={float(kl.midpoint()):.9g}", flush=True)
    return cases


def size_experiment():
    rows = []
    for alpha in [1, 2]:
        for A in [F(1), F(4)]:
            for eps in [F(1, 2), F(1, 4), F(1, 8), F(1, 16), F(1, 32)]:
                d = 256
                archive = make_archive(A, alpha, eps, d)
                k = archive.k
                # Equally informed comparator: exact same k and outer radii,
                # a common width eps/A, conditional-reference decoding.
                # This over-resolves weak retained coordinates; it too obeys
                # the same KL budget. It does not know theta.
                common_h = eps / A
                uniform_axes = []
                for axis in archive.axes:
                    from certified import sqrt_log_upper_endpoint, ceil_div
                    T = sqrt_log_upper_endpoint(axis.a, common_h)
                    quotient = 2 * T / common_h
                    M = ceil_div(quotient.numerator, quotient.denominator)
                    uniform_axes.append(Axis(axis.j, axis.a, common_h, T, M))
                uniform = Archive(A, alpha, eps, d, tuple(uniform_axes))
                # A 64-bit raw register comparator is only a storage reference,
                # not a continuous-TV theorem for floating-point output.
                raw_truncated_bits = 64 * k
                # Keep all d coordinates with common-resolution bins: same
                # blind mechanism and no theta access, but unnecessary storage.
                full_axes = []
                for j in range(1, d + 1):
                    a = A / j**alpha
                    from certified import sqrt_log_upper_endpoint, ceil_div
                    T = sqrt_log_upper_endpoint(a, common_h)
                    quotient = 2 * T / common_h
                    M = ceil_div(quotient.numerator, quotient.denominator)
                    full_axes.append(Axis(j, a, common_h, T, M))
                full = Archive(A, alpha, eps, d, tuple(full_axes))
                rows.append({"A": str(A), "alpha": alpha, "eps": str(eps), "d": d, "k": k,
                             "adaptive_mixed_radix_bits": archive.mixed_radix_bits,
                             "adaptive_vector_bits": archive.vector_bits,
                             "uniform_prefix_bits": uniform.mixed_radix_bits,
                             "full_uniform_bits": full.mixed_radix_bits,
                             "raw_float64_prefix_bits": raw_truncated_bits,
                             "effective_cutoff_scale": float((mpf(A) / mpf(eps))**(mp.mpf(1) / alpha)),
                             "TV_analytic_upper": float(eps / 2)})
    with (BASE / "memory_comparison.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    return rows


def finite_sampler_experiment():
    # A=1, alpha=1, eps=.25, d=8 has k=3. No simulation of an enormous alphabet.
    archive = make_archive(1, 1, F(1, 4), 8)
    boundaries = tuple(F(-6) + F(i, 8) for i in range(97))
    representatives = (boundaries[0],) + tuple((a + b) / 2 for a, b in zip(boundaries, boundaries[1:])) + (boundaries[-1],)
    rbits = 40
    reference = rounded_decoder_table(None, None, boundaries)
    ref_cutoffs, ref_error = compile_dyadic_cdf(reference, rbits)
    tables = {"reference": list(ref_cutoffs), "axes": {}}
    max_errors = []
    total_table_entries = len(ref_cutoffs)
    cuts_by_axis = []
    for axis in archive.axes:
        cuts = []
        errors = []
        for label in range(axis.labels):
            probabilities = rounded_decoder_table(axis, label, boundaries)
            cutoffs, tv_error = compile_dyadic_cdf(probabilities, rbits)
            cuts.append(cutoffs)
            errors.append(tv_error)
            # Independent normalization and certified L1 check of generated
            # cell masses, rather than relying only on a generic CDF bound.
            generated = dyadic_cell_probabilities(cutoffs, rbits)
            assert sum(generated) == 1 and all(p >= 0 for p in generated)
            direct_error = sum(max(abs(m - F(p.lo, SCALE)), abs(m - F(p.hi, SCALE)))
                               for m, p in zip(generated, probabilities)) / 2
            assert direct_error <= tv_error + F(len(probabilities), SCALE)
        cuts_by_axis.append(tuple(cuts))
        tables["axes"][str(axis.j)] = [list(x) for x in cuts]
        max_errors.append(max(errors))
        total_table_entries += sum(map(len, cuts))
    max_kernel_error = sum(max_errors) + (archive.d - archive.k) * ref_error
    tables.update({"random_bits_per_coordinate": rbits,
                   "grid_boundaries": [json_fraction(x) for x in boundaries],
                   "representatives": [json_fraction(x) for x in representatives],
                   "public_design": {"A": "1", "alpha": 1, "eps": "1/4", "d": 8,
                                     "axes": [{"j": a.j, "T": json_fraction(a.T), "M": a.M,
                                               "labels": a.labels} for a in archive.axes]}})
    (BASE / "sampler_tables.json").write_text(json.dumps(tables, indent=2) + "\n")
    # Fully deterministic rounded-law calculation at a few valid theta vectors.
    theta_vectors = [tuple(F(0) for _ in range(8)),
                     (F(1),) + tuple(F(0) for _ in range(7)),
                     (F(1, 2), F(1, 4), F(1, 6)) + tuple(F(0) for _ in range(5)),
                     tuple(F(1, 4 * j) for j in range(1, 9))]
    law_results = []
    output_cells = tuple(zip((None,) + boundaries, boundaries + (None,)))
    for theta in theta_vectors:
        assert sum((t * j)**2 for j, t in enumerate(theta, 1)) <= 1
        coordinate_tvs = []
        total_kl = IV.exact(0)
        for j, t in enumerate(theta):
            target = tuple(normal_mass(l, u, t) for l, u in output_cells)
            if j < archive.k:
                axis = archive.axes[j]
                weights = tuple(normal_mass(*axis.bounds(label), t) for label in range(axis.labels))
                generated = [IV.exact(0) for _ in target]
                for weight, cutoffs in zip(weights, cuts_by_axis[j]):
                    for z, prob in enumerate(dyadic_cell_probabilities(cutoffs, rbits)):
                        generated[z] += weight * prob
                total_kl += axis_kl(axis, t)[0]
            else:
                generated = tuple(IV.exact(p) for p in dyadic_cell_probabilities(ref_cutoffs, rbits))
                total_kl += t * t / 2
            # Certified TV interval for the rounded marginal law.
            abs_low = abs_high = 0
            for p, q in zip(target, generated):
                delta = p - q
                abs_low += 0 if delta.lo <= 0 <= delta.hi else min(abs(delta.lo), abs(delta.hi))
                abs_high += max(abs(delta.lo), abs(delta.hi))
            coordinate_tvs.append(IV(abs_low // 2, (abs_high + 1) // 2))
        # Product TV is bounded above by sum of coordinate TV; no use of
        # coordinate independence to replace this by an unproved max.
        product_tv_upper = min(F(1), sum(F(x.hi, SCALE) for x in coordinate_tvs))
        pinsker_upper = (total_kl / 2).sqrt() + max_kernel_error
        law_results.append({"theta": [json_fraction(t) for t in theta],
                            "exact_ideal_KL": simplified_interval(total_kl),
                            "rounded_marginal_TV": [simplified_interval(v) for v in coordinate_tvs],
                            "rounded_product_TV_upper_by_coordinate_sum": json_fraction(product_tv_upper),
                            "rounded_product_TV_upper_by_Pinsker_plus_compiler": simplified_interval(pinsker_upper)})
    # Encode/pack/unpack and decode one actual small input, preserving no X or
    # theta in the returned archive object. This uses a seeded Python RNG only
    # for reproduction; the formal bit sampler assumes independent fair bits.
    rng = random.Random(20261007)
    observations = iter([F(13, 10), F(-2, 5), F(1, 10)])
    labels = archive.encode(observations)
    message = archive.pack(labels)
    assert archive.unpack(message) == labels
    decoded_cells = tuple(sample_dyadic_cdf(cuts_by_axis[j][labels[j]], rbits, rng)
                          if j < archive.k else sample_dyadic_cdf(ref_cutoffs, rbits, rng)
                          for j in range(archive.d))
    return {"A": "1", "alpha": 1, "eps": "1/4", "d": 8, "k": archive.k,
            "alphabet_size": str(archive.alphabet_size),
            "mixed_radix_bits": archive.mixed_radix_bits, "fixed_vector_bits": archive.vector_bits,
            "output_cells_per_coordinate": len(representatives),
            "random_bits_per_coordinate": rbits, "random_bits_per_output": archive.d * rbits,
            "table_entries": total_table_entries,
            "table_integer_bits_packed": total_table_entries * (rbits + 1),
            "worst_case_kernel_TV_error": json_fraction(max_kernel_error),
            "worst_case_kernel_TV_error_float": float(max_kernel_error),
            "per_axis_max_TV_error": [json_fraction(e) for e in max_errors],
            "reference_TV_error": json_fraction(ref_error),
            "finite_sample": {"labels": list(labels), "packed_message": message,
                              "output_cell_indices": list(decoded_cells),
                              "output_values": [json_fraction(representatives[z]) for z in decoded_cells]},
            "deterministic_law_results": law_results,
            "compiler_table_file_bytes": (BASE / "sampler_tables.json").stat().st_size}


def main():
    started = time.monotonic()
    tracemalloc.start()
    assertions = verify_certified_primitives()
    print(f"Certified-primitives cross-checks: {assertions}", flush=True)
    scalars = scalar_cases()
    print("Memory-size comparisons", flush=True)
    sizes = size_experiment()
    print("Compiling and checking rounded-output tables", flush=True)
    sampler = finite_sampler_experiment()
    current, peak = tracemalloc.get_traced_memory()
    elapsed = time.monotonic() - started
    report = {"status": "finite_diagnostic_and_certified_arithmetic_not_external_theorem_validation",
              "interval_precision_bits": BITS,
              "primitive_cross_checks": assertions,
              "scalar_cases": scalars,
              "scalar_bin_checks": sum(x["checked_bins"] for x in scalars),
              "memory_comparisons": sizes,
              "finite_grid_sampler": sampler,
              "resources": {"wall_seconds": elapsed, "peak_tracemalloc_bytes": peak,
                            "maxrss_platform_units": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                            "python": sys.version, "mpmath": mp.__version__},
              "limitations": ["Finite random-bit output has TV=1 against unrounded continuous target.",
                              "Compiler here targets the common finite rounding/clipping map.",
                              "The experiment covers alpha=1,2, finite d, and the listed means only.",
                              "Supplied ellipsoid and independent Gaussian reference are public inputs.",
                              "No acquisition of axes/covariance, no MSE preservation, and no novelty clearance."]}
    (BASE / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    files = ["certified.py", "archive.py", "run_experiment.py", "results.json", "memory_comparison.csv", "sampler_tables.json"]
    manifest = {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest() for name in files}
    (BASE / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Complete in {elapsed:.3f}s; peak traced bytes={peak}; compiler TV={sampler['worst_case_kernel_TV_error_float']:.3g}", flush=True)


if __name__ == "__main__":
    main()

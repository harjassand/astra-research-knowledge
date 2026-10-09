#!/usr/bin/env python3
"""Exact clone and trace-curvature diagnostics for union-closed families.

Uses only the Python standard library.  The exhaustive mode checks every
nontrivial union-closed family on [4] and every separating subset of its
distinct nonconstant coordinate traces.  This is finite evidence only.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from itertools import combinations

from finite_profiles import enumerate_families


def pair_counts(members: tuple[int, ...]) -> dict[int, int]:
    counts = {s: 0 for s in members}
    for a in members:
        for b in members:
            counts[a | b] += 1
    return counts


def mixed_curvature(
    members: tuple[int, ...], counts: dict[int, int], bit: int
) -> tuple[float, float, float]:
    """Return (p, Delta, M), M=E[(X-p)(Y-p) log r(A|B)].

    Delta is the conditional mixed difference c_11-c_10-c_01+c_00.
    It is defined only for a nonconstant coordinate trace, so all four
    conditioning events have positive probability.
    """
    n = len(members)
    ones = sum((a >> bit) & 1 for a in members)
    if not 0 < ones < n:
        raise ValueError("mixed curvature requires a nonconstant trace")
    sums = [[0.0, 0] for _ in range(4)]
    for a in members:
        x = (a >> bit) & 1
        for b in members:
            y = (b >> bit) & 1
            q = 2 * x + y
            sums[q][0] += math.log(counts[a | b])
            sums[q][1] += 1
    means = [total / count for total, count in sums]
    delta = means[3] - means[2] - means[1] + means[0]
    p = ones / n
    m_value = p * p * (1 - p) * (1 - p) * delta
    return p, delta, m_value


def trace_representatives(
    members: tuple[int, ...], n: int
) -> dict[tuple[int, ...], int]:
    """Map each distinct nonconstant coordinate column to one bit index."""
    result: dict[tuple[int, ...], int] = {}
    N = len(members)
    for bit in range(n):
        trace = tuple((a >> bit) & 1 for a in members)
        if 0 < sum(trace) < N:
            result.setdefault(trace, bit)
    return result


def separating_subset_stats(
    members: tuple[int, ...], n: int, counts: dict[int, int]
) -> dict:
    reps = trace_representatives(members, n)
    traces = list(reps)
    bits = [reps[t] for t in traces]
    deltas = [mixed_curvature(members, counts, bit)[1] for bit in bits]
    N = len(members)
    top = 0
    for a in members:
        top |= a
    r_top = counts[top]
    min_gap = math.inf
    min_curvature = math.inf
    separating_subsets = 0
    for size in range(1, len(traces) + 1):
        for chosen in combinations(range(len(traces)), size):
            signatures = {
                tuple(traces[j][row] for j in chosen)
                for row in range(N)
            }
            if len(signatures) != N:
                continue
            separating_subsets += 1
            curvature = -sum(deltas[j] for j in chosen)
            min_curvature = min(min_curvature, curvature)
            min_gap = min(min_gap, curvature - math.log(r_top))
    if separating_subsets == 0:
        raise AssertionError("the full coordinate trace family must separate")
    return {
        "distinct_nonconstant_traces": len(traces),
        "separating_subsets": separating_subsets,
        "r_top": r_top,
        "min_separating_curvature": min_curvature,
        "min_gap_over_log_r_top": min_gap,
    }


def clone_profile(m: int, clone_count: int, direct: bool = True) -> dict:
    """Analyze 2^[m] plus a new top carrying clone_count identical elements.

    The extra elements are represented by one marker bit because their
    incidence columns are identical.  This preserves all union fibers and
    represents one clone trace; clone_count affects only the raw coordinate
    sum.
    """
    if m < 2 or clone_count < 0:
        raise ValueError("require m>=2 and clone_count>=0")
    s = 1 << m
    N = s + 1
    top = (1 << (m + 1)) - 1
    members = tuple(range(s)) + (top,)
    counts = pair_counts(members)
    old_bit = 0
    clone_bit = m
    p_old, delta_old_direct, M_old_direct = mixed_curvature(
        members, counts, old_bit
    )
    p_clone, delta_clone_direct, M_clone_direct = mixed_curvature(
        members, counts, clone_bit
    )
    log_top_mult = math.log(2 * s + 1)
    M_old_formula = (
        s**2
        * (
            (-s**2 - 4 * s + 3 * m - 3) * math.log(3)
            - 4 * log_top_mult
        )
        / (16 * N**4)
    )
    M_clone_formula = (
        s**2
        / N**4
        * (3 * m / 4 * math.log(3) - log_top_mult)
    )
    K_base = -m * M_old_formula
    K_clone = -M_clone_formula
    K_raw = K_base + clone_count * K_clone
    K_trace_quotient = K_base + K_clone
    positive_clone_delta = 3 * m / 4 * math.log(3) - log_top_mult
    threshold = (
        K_base / (-K_clone) if positive_clone_delta > 0 and K_clone < 0 else None
    )
    return {
        "m": m,
        "clone_count": clone_count,
        "N": N,
        "p_old": p_old,
        "p_clone": p_clone,
        "r_top": counts[top],
        "M_old_direct": M_old_direct,
        "M_old_formula": M_old_formula,
        "M_clone_direct": M_clone_direct,
        "M_clone_formula": M_clone_formula,
        "delta_old_direct": delta_old_direct,
        "delta_clone_direct": delta_clone_direct,
        "K_base": K_base,
        "K_clone_per_clone": K_clone,
        "K_raw": K_raw,
        "K_trace_quotient": K_trace_quotient,
        "C_trace_quotient": -m * delta_old_direct - delta_clone_direct,
        "log_r_top": log_top_mult,
        "clone_delta_before_p2q2": positive_clone_delta,
        "strict_negative_threshold_for_clone_count": threshold,
        "exact_m6_22000_certificate": exact_m6_22000_certificate()
        if m == 6 and clone_count == 22000
        else None,
    }


def exact_m6_22000_certificate() -> dict:
    """Integer-power certificate that the raw size potential is negative."""
    # For m=6, s=64, N=65, and M=22000:
    # K = (q^2 p^2/16) * (-1,557,978 ln 3 + 352,024 ln 129).
    # 129^40 < 3^177 implies ln(129)/ln(3) < 177/40, and
    # 177/40 < 1,557,978/352,024, proving the parenthesis is < 0.
    power_test = 129**40 < 3**177
    rational_test = 177 * 352024 < 40 * 1557978
    return {
        "factor": "(q^2 p^2)/16, with p=1/65 and q=64/65",
        "log_expression": "-1557978*ln(3) + 352024*ln(129)",
        "integer_power_test_129^40_lt_3^177": power_test,
        "integer_cross_product_test": rational_test,
        "negative_proved": power_test and rational_test,
    }


def auxiliary_mean_bound_failure() -> dict:
    """Exact counterexample to E log r(U) <= log r(T), a discarded route."""
    members = (
        2, 3, 5, 7, 20, 21, 22, 23, 33, 34,
        35, 37, 39, 49, 51, 53, 54, 55, 63,
    )
    present = set(members)
    union_closed = all((a | b) in present for a in members for b in members)
    counts = pair_counts(members)
    top = 0
    for a in members:
        top |= a
    N = len(members)
    left = math.prod(v**v for v in counts.values())
    right = counts[top] ** (N * N)
    mean_log_r = sum(v * math.log(v) for v in counts.values()) / (N * N)
    return {
        "family_masks": list(members),
        "N": N,
        "union_closed_exactly": union_closed,
        "top_mask": top,
        "r_top": counts[top],
        "mean_log_r": mean_log_r,
        "log_r_top": math.log(counts[top]),
        "mean_exceeds_top_log_numerically": mean_log_r > math.log(counts[top]),
        "integer_certificate_product_rS_to_rS_gt_rT_to_N2": left > right,
        "certificate_digits_left_right": [len(str(left)), len(str(right))],
    }


def exhaustive_n4() -> dict:
    family_count = 0
    subset_count = 0
    min_gap = math.inf
    min_curvature = math.inf
    min_example = None
    raw_type_min = math.inf
    rare_non_singleton_count = 0
    rare_non_singleton_min = math.inf
    rare_negative_count = 0
    for members in enumerate_families(4):
        if len(members) < 2:
            continue
        family_count += 1
        counts = pair_counts(members)
        stats = separating_subset_stats(members, 4, counts)
        subset_count += stats["separating_subsets"]
        if stats["min_gap_over_log_r_top"] < min_gap:
            min_gap = stats["min_gap_over_log_r_top"]
            min_example = list(members)
        min_curvature = min(
            min_curvature, stats["min_separating_curvature"]
        )
        reps = trace_representatives(members, 4)
        values = [mixed_curvature(members, counts, bit) for bit in reps.values()]
        raw_type_min = min(raw_type_min, -sum(m[2] for m in values))
        N = len(members)
        for bit in range(4):
            ones = sum((a >> bit) & 1 for a in members)
            if 1 < ones < N / 2:
                rare_non_singleton_count += 1
                k_i = -mixed_curvature(members, counts, bit)[2]
                rare_non_singleton_min = min(rare_non_singleton_min, k_i)
                if k_i < -1e-12:
                    rare_negative_count += 1
    return {
        "ground_set_size": 4,
        "nontrivial_union_closed_families": family_count,
        "separating_subsets_checked": subset_count,
        "minimum_over_I_of_C_I_minus_ln_r_top": min_gap,
        "family_attaining_minimum": min_example,
        "minimum_over_I_of_C_I": min_curvature,
        "minimum_raw_trace_quotient_K": raw_type_min,
        "rare_non_singleton_coordinate_cases": rare_non_singleton_count,
        "minimum_K_i_for_2_le_frequency_below_half": rare_non_singleton_min,
        "negative_K_i_cases_in_that_restriction": rare_negative_count,
        "constant_coordinates_excluded_from_I": True,
    }


def all_nonconstant_join_homomorphisms(
    members: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """Enumerate every homomorphism (F, union)->({0,1}, OR).

    The output is a trace family on the abstract join-semilattice, so it may
    include prime filters that are not among the original ground-set columns.
    Constant traces are omitted because they never separate two elements and
    their four conditional quadrants are undefined.
    """
    n = len(members)
    index = {a: j for j, a in enumerate(members)}
    union_indices = [index[a | b] for a in members for b in members]
    pair_indices = [(j, k) for j in range(n) for k in range(n)]
    result = []
    for code in range(1 << n):
        trace = tuple((code >> j) & 1 for j in range(n))
        if not 0 < sum(trace) < n:
            continue
        if all(
            trace[out] == (trace[j] | trace[k])
            for out, (j, k) in zip(union_indices, pair_indices)
        ):
            result.append(trace)
    return result


def arbitrary_homomorphism_scan(max_members: int = 8) -> dict:
    """Check all separating subfamilies of all join homomorphisms for n<=4.

    We cap family cardinality, not the ground-set dimension.  Every candidate
    trace is tested against the union operation itself, rather than assumed to
    be an original coordinate projection.
    """
    family_count = 0
    homomorphism_count = 0
    separating_count = 0
    min_gap = math.inf
    min_record = None
    max_homomorphisms = 0
    skipped = 0
    for n in range(1, 5):
        for members in enumerate_families(n):
            if not 2 <= len(members) <= max_members:
                continue
            family_count += 1
            counts = pair_counts(members)
            top = 0
            for a in members:
                top |= a
            log_r_top = math.log(counts[top])
            traces = all_nonconstant_join_homomorphisms(members)
            homomorphism_count += len(traces)
            max_homomorphisms = max(max_homomorphisms, len(traces))
            if len(traces) > 18:
                skipped += 1
                continue
            deltas = []
            N = len(members)
            for trace in traces:
                sums = [[0.0, 0] for _ in range(4)]
                for j, a in enumerate(members):
                    x = trace[j]
                    for k, b in enumerate(members):
                        y = trace[k]
                        q = 2 * x + y
                        sums[q][0] += math.log(counts[a | b])
                        sums[q][1] += 1
                means = [total / count for total, count in sums]
                deltas.append(means[3] - means[2] - means[1] + means[0])
            for size in range(1, len(traces) + 1):
                for chosen in combinations(range(len(traces)), size):
                    signatures = {
                        tuple(traces[j][row] for j in chosen)
                        for row in range(N)
                    }
                    if len(signatures) != N:
                        continue
                    separating_count += 1
                    curvature = -sum(deltas[j] for j in chosen)
                    gap = curvature - log_r_top
                    if gap < min_gap:
                        min_gap = gap
                        min_record = {
                            "n": n,
                            "family": list(members),
                            "N": N,
                            "homomorphisms": len(traces),
                            "chosen_indices": list(chosen),
                            "C_I": curvature,
                            "r_top": counts[top],
                        }
    return {
        "ground_set_sizes": "1 through 4",
        "family_size_cap": max_members,
        "families_checked": family_count,
        "nonconstant_join_homomorphisms_total": homomorphism_count,
        "maximum_homomorphisms_in_a_family": max_homomorphisms,
        "separating_subfamilies_checked": separating_count,
        "skipped_families_due_to_homomorphism_cap": skipped,
        "minimum_C_I_minus_ln_r_top": min_gap,
        "minimum_example": min_record,
        "constant_homomorphisms_excluded": True,
    }


def boolean_cube_homomorphism_scan(n: int = 4) -> dict:
    """Check every separating subfamily of every prime filter of 2^[n].

    A join homomorphism on the Boolean cube is OR over a support S subset [n],
    so there are exactly 2^n-1 nonconstant traces.  The default n=4 scan is
    small enough to enumerate all subfamilies, including nonminimal ones.
    """
    if n < 1 or n > 5:
        raise ValueError("cube homomorphism scan is capped at 1<=n<=5")
    members = tuple(range(1 << n))
    N = len(members)
    counts = {s: 3 ** s.bit_count() for s in members}
    traces = [
        tuple(int(bool(a & support)) for a in members)
        for support in range(1, 1 << n)
    ]
    deltas = []
    for trace in traces:
        sums = [[0.0, 0] for _ in range(4)]
        for j, a in enumerate(members):
            for k, b in enumerate(members):
                q = 2 * trace[j] + trace[k]
                sums[q][0] += math.log(counts[a | b])
                sums[q][1] += 1
        means = [total / count for total, count in sums]
        deltas.append(means[3] - means[2] - means[1] + means[0])
    min_gap = math.inf
    min_curvature = math.inf
    separating_count = 0
    for mask in range(1, 1 << len(traces)):
        chosen = [j for j in range(len(traces)) if mask >> j & 1]
        signatures = {
            tuple(traces[j][row] for j in chosen)
            for row in range(N)
        }
        if len(signatures) != N:
            continue
        separating_count += 1
        curvature = -sum(deltas[j] for j in chosen)
        min_curvature = min(min_curvature, curvature)
        min_gap = min(min_gap, curvature - math.log(counts[members[-1]]))
    return {
        "cube_dimension": n,
        "family_size": N,
        "nonconstant_join_homomorphisms": len(traces),
        "separating_subfamilies_checked": separating_count,
        "r_top": counts[members[-1]],
        "minimum_C_I": min_curvature,
        "minimum_C_I_minus_ln_r_top": min_gap,
    }


def random_generated_tests(samples_per_n: int, seed: int) -> dict:
    """Sample union closures of random generators; check every separating I."""
    rng = random.Random(seed)
    results = []
    for n in (5, 6, 7, 8):
        tested = 0
        minimum_gap = math.inf
        minimum_record = None
        for _ in range(samples_per_n):
            generator_count = rng.randint(2, min(14, 1 << n))
            generators = [rng.randrange(1 << n) for _ in range(generator_count)]
            family = set(generators)
            stack = list(family)
            while stack:
                a = stack.pop()
                for b in tuple(family):
                    u = a | b
                    if u not in family:
                        family.add(u)
                        stack.append(u)
            members = tuple(sorted(family))
            if len(members) < 2 or len(members) > 40:
                continue
            counts = pair_counts(members)
            stats = separating_subset_stats(members, n, counts)
            tested += 1
            gap = stats["min_gap_over_log_r_top"]
            if gap < minimum_gap:
                minimum_gap = gap
                minimum_record = {
                    "family": list(members),
                    "N": len(members),
                    "distinct_nonconstant_traces": stats[
                        "distinct_nonconstant_traces"
                    ],
                    "r_top": stats["r_top"],
                }
        results.append(
            {
                "n": n,
                "accepted_families": tested,
                "minimum_gap": minimum_gap,
                "minimum_record": minimum_record,
            }
        )
    return {"seed": seed, "samples_per_n": samples_per_n, "results": results}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clone-m", type=int, default=6)
    parser.add_argument("--clones", type=int, default=22000)
    parser.add_argument("--n4", action="store_true")
    parser.add_argument("--homomorphisms-small", action="store_true")
    parser.add_argument("--cube-homomorphisms", action="store_true")
    parser.add_argument("--random-samples", type=int, default=0)
    parser.add_argument("--seed", type=int, default=939697)
    args = parser.parse_args()
    result = {
        "clone_profile": clone_profile(args.clone_m, args.clones),
        "failed_auxiliary_mean_bound": auxiliary_mean_bound_failure(),
    }
    if args.n4:
        result["exhaustive_n4"] = exhaustive_n4()
    if args.homomorphisms_small:
        result["abstract_join_homomorphism_scan"] = arbitrary_homomorphism_scan()
    if args.cube_homomorphisms:
        result["boolean_cube_homomorphism_scan"] = boolean_cube_homomorphism_scan()
    if args.random_samples:
        result["random_generated"] = random_generated_tests(
            args.random_samples, args.seed
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

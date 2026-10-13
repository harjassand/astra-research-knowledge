"""Independent bounded checks for the Sol03 sequential ordinal flag draft.

Uses only the standard library. The finite checks are diagnostics of the
displayed formulas, not a proof of the algorithm for arbitrary n.
"""
from fractions import Fraction
from math import ceil, comb, exp, log
import json
from pathlib import Path


def cdf_median_numerator(r, N, m):
    """Numerator of P[discrete sample median <= r], denominator N**m."""
    threshold = (m + 1) // 2
    p_num = r + 1
    q_num = N - p_num
    return sum(comb(m, k) * p_num**k * q_num**(m-k)
               for k in range(threshold, m + 1))


def exact_discrete_median_error(N, m):
    """Exact E |median/N - 1/2| for m iid ranks in {0,...,N-1}."""
    denominator = N**m
    previous = 0
    absolute_numerator = 0
    half = Fraction(N, 2)
    for r in range(N):
        current = cdf_median_numerator(r, N, m)
        mass_numerator = current - previous
        absolute_numerator += mass_numerator * abs(Fraction(r, 1) - half)
        previous = current
    return Fraction(absolute_numerator, denominator * N)


def gf2_inverse(rows, n):
    aug = [rows[i] | (1 << (n + i)) for i in range(n)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if (aug[r] >> col) & 1), None)
        if pivot is None:
            raise ValueError("matrix is singular")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for r in range(n):
            if r != col and ((aug[r] >> col) & 1):
                aug[r] ^= aug[col]
    return [row >> n for row in aug]


def mat_vec(rows, x):
    return sum(((row & x).bit_count() & 1) << i for i, row in enumerate(rows))


def flag_projection_check(n=6, k=3):
    """Exhaust a hidden-affine triangular quadratic example and all prefixes."""
    # A nontrivial invertible upper-triangular affine coordinate change.
    A = [(1 << i) | ((1 << (i + 1)) if i + 1 < n else 0)
         for i in range(n)]
    Ainv = gf2_inverse(A, n)
    offset = 0b101011 & ((1 << n) - 1)
    v = [mat_vec(Ainv, 1 << j) for j in range(n)]

    def outputs(x):
        u = mat_vec(A, x) ^ offset
        out = 0
        for j in range(n):
            bit = (u >> j) & 1
            if j >= 2:
                bit ^= ((u >> (j - 2)) & 1) & ((u >> (j - 1)) & 1)
            out |= bit << (n - 1 - j)
        return out

    def q(j, x):
        return (outputs(x) >> (n - 1 - j)) & 1

    # The output list is triangular in u, hence a bijection. Verify the exact
    # common-radical toggle identities directly on all x for every j.
    flag_checks = 0
    for j in range(n):
        for i in range(j + 1):
            expected = int(i == j)
            for x in range(1 << n):
                assert q(i, x ^ v[j]) ^ q(i, x) == expected
                flag_checks += 1

    def project(x, b):
        for j in range(k):
            if q(j, x) != ((b >> (k - 1 - j)) & 1):
                x ^= v[j]
        return x

    # W is the image under A^{-1} of the last n-k coordinate directions.
    W = []
    for mask in range(1 << (n - k)):
        u_mask = mask << k
        W.append(mat_vec(Ainv, u_mask))
    projection_cases = 0
    enumerated_fibers = 0
    for b in range(1 << k):
        images = [project(x, b) for x in range(1 << n)]
        counts = {}
        for y in images:
            counts[y] = counts.get(y, 0) + 1
            assert (outputs(y) >> (n - k)) == b
        assert len(counts) == 1 << (n - k)
        assert set(counts.values()) == {1 << k}
        representatives = [project(w, b) for w in W]
        assert len(set(representatives)) == len(W)
        assert set(representatives) == set(counts)
        # Exact local ordinal rank within each acquired prefix fiber.
        for x in counts:
            rank = sum(outputs(y) < outputs(x) for y in counts)
            expected = outputs(x) & ((1 << (n - k)) - 1)
            assert rank == expected
            projection_cases += 1
        enumerated_fibers += len(counts)
    return {
        "n": n,
        "acquired_prefix_length": k,
        "output_map_bijective_by_triangular_construction": True,
        "flag_toggle_checks": flag_checks,
        "prefix_projection_points_checked": projection_cases,
        "fiber_representatives_checked": enumerated_fibers,
        "all_prefix_projections_exact_uniform": True,
        "complement_parameterizes_every_prefix_fiber": True,
        "local_ordinal_rank_equals_suffix_integer": True,
    }


def main():
    m = 127
    a_m = Fraction(comb(m + 1, (m + 1) // 2), 2 ** (m + 2))
    N = 256
    eta = a_m + Fraction(1, N)
    gap = Fraction(1, 2) - 7 * eta
    exact_actual_median = exact_discrete_median_error(N, m)
    assert eta < Fraction(1, 14)
    assert exact_actual_median <= eta

    sizes = []
    for n in (8, 16, 32, 64, 128, 256):
        M = 1 + n + n * (n - 1) // 2
        stages = max(0, n - 7)
        stage_rows = []
        comparisons = 0
        for k in range(stages):
            residual = 1 << (n - k)
            eta_k = float(a_m) + 1 / residual
            gap_k = 0.5 - 7 * eta_k
            t = ceil(log(n * M / 0.01) / (2 * gap_k * gap_k))
            if t % 2 == 0:
                t += 1
            stage_calls = 7 * m * t * M
            comparisons += stage_calls
            stage_rows.append({"stage": k, "residual_size": residual,
                               "odd_t": t, "stage_comparisons": stage_calls,
                               "stage_failure_bound": M * exp(-2 * t * gap_k * gap_k)})
        tail_r = min(n, 7)
        comparisons += M * ((1 << tail_r) - 1)
        t_max = max((s["odd_t"] for s in stage_rows), default=0)
        worst_gap = min((0.5 - 7 * (float(a_m) + 1 / s["residual_size"])
                         for s in stage_rows), default=float(gap))
        sizes.append({
            "n": n,
            "M": M,
            "randomized_stages": stages,
            "maximum_odd_t": t_max,
            "comparison_upper_bound": comparisons,
            "query_argument_bits_upper_bound": 2 * n * comparisons,
            "worst_stage_majority_bound": exp(-2 * t_max * worst_gap * worst_gap),
            "per_stage_failure_bounds": [s["stage_failure_bound"] for s in stage_rows],
            "tail_comparisons": M * ((1 << tail_r) - 1),
            "stages": stage_rows,
        })
    result = {
        "median": {
            "m": m,
            "continuous_beta_mean_absolute_deviation": str(a_m),
            "continuous_beta_mean_absolute_deviation_decimal": float(a_m),
            "N_min": N,
            "eta_upper_bound": str(eta),
            "eta_upper_bound_decimal": float(eta),
            "7_eta_upper_bound": float(7 * eta),
            "rm_majority_gap_lower_bound": str(gap),
            "rm_majority_gap_lower_bound_decimal": float(gap),
            "exact_finite_N_median_error": str(exact_actual_median),
            "exact_finite_N_median_error_decimal": float(exact_actual_median),
            "verified_eta_below_1_over_14": True,
        },
        "query_cost_examples_beta_0_01": sizes,
        "projection_exhaustion": flag_projection_check(),
        "scope": "Exact formula arithmetic and a finite triangular example only; not an algorithm implementation, scaling experiment, or proof of novelty.",
    }
    path = Path(__file__).with_name("analytic_check.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

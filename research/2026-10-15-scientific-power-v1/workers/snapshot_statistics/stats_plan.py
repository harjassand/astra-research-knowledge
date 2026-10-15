#!/usr/bin/env python3
"""Finite-sample planning for the fixed three-snapshot score fixture.

The exact triplet probabilities and rational certificate are recomputed with
the operational-closure fixture checker.  A floating-point uniformization scan
only selects a candidate lag and e-process stake; the selected exact rational
lag is then rechecked by the source checker.

This is a model-fixture planning calculation, not acquired physical data.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKER_PATH = HERE / "source/verify_snapshot_operation.py"
spec = importlib.util.spec_from_file_location("snapshot_fixture_checker", CHECKER_PATH)
checker = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(checker)
F = checker.F

Q_TARGET = [
    [F(-21, 20), F(1), F(1, 20)],
    [F(1, 20), F(-21, 20), F(1)],
    [F(1), F(1, 20), F(-21, 20)],
]
Q_EQUILIBRIUM = [
    [F(-28, 25), F(14, 25), F(14, 25)],
    [F(14, 25), F(-28, 25), F(14, 25)],
    [F(14, 25), F(14, 25), F(-28, 25)],
]
PI = [F(1, 3)] * 3
LABELS = [0, 1, 1]
R_SCORE = 0.9
LAMBDA = 1 / 3
ALPHA = 0.05
BETA = 0.05
TRIPLES = [f"{x}{y}{z}" for x in (0, 1) for y in (0, 1) for z in (0, 1)]


def exact_cells(q, t):
    """Eight rational-enclosure probabilities for one fixed equal gap."""
    pmat = checker.transition(q, t)
    result = {}
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                value = checker.Interval.point(0)
                for i in range(3):
                    for j in range(3):
                        for k in range(3):
                            if (LABELS[i], LABELS[j], LABELS[k]) == (x, y, z):
                                value += PI[i] * pmat[i][j] * pmat[j][k]
                result[f"{x}{y}{z}"] = value
    return result


def interval_midpoint(value):
    return float((value.lo + value.hi) / 2)


def score_values(r=R_SCORE):
    """W=Y0(Y_-−r)(Y_+−r), ordered as 000,...,111."""
    return [
        0.0,
        0.0,
        r * r,
        -r * (1 - r),
        0.0,
        0.0,
        -r * (1 - r),
        (1 - r) * (1 - r),
    ]


def score_values_exact():
    return [F(0), F(0), F(81, 100), F(-9, 100), F(0), F(0), F(-9, 100), F(1, 100)]


def moments(probabilities, values):
    mean = sum(p * x for p, x in zip(probabilities, values))
    variance = sum(p * (x - mean) ** 2 for p, x in zip(probabilities, values))
    return mean, variance


def matrix_multiply(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def float_transition(t):
    """Uniformization for lag scan; exact selected lag is checked separately."""
    rate = 1.05
    q = [[-1.05, 1.0, 0.05], [0.05, -1.05, 1.0], [1.0, 0.05, -1.05]]
    uniformizer = [
        [float(i == j) + q[i][j] / rate for j in range(3)] for i in range(3)
    ]
    x = rate * t
    power = [[float(i == j) for j in range(3)] for i in range(3)]
    weight = math.exp(-x)
    result = [[weight * power[i][j] for j in range(3)] for i in range(3)]
    last = int(x + 20 * math.sqrt(x + 1) + 50)
    for k in range(1, last + 1):
        power = matrix_multiply(power, uniformizer)
        weight *= x / k
        for i in range(3):
            for j in range(3):
                result[i][j] += weight * power[i][j]
    return result


def float_cells(t):
    pmat = float_transition(t)
    result = {key: 0.0 for key in TRIPLES}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                key = f"{LABELS[i]}{LABELS[j]}{LABELS[k]}"
                result[key] += pmat[i][j] * pmat[j][k] / 3
    return [result[key] for key in TRIPLES]


def e_process_design(probabilities, values, lam=LAMBDA, null_mean=0.0):
    increments = [math.log1p(-lam * (w - null_mean)) for w in values]
    growth = sum(p * z for p, z in zip(probabilities, increments))
    variance = sum(p * (z - growth) ** 2 for p, z in zip(probabilities, increments))
    width = max(increments) - min(increments)
    return growth, variance, width


def sufficient_power_n(growth, variance, width, alpha=ALPHA, beta=BETA):
    """Bernstein lower-tail sufficient n for P_alt(log E_n >= log(1/alpha)) >= 1-beta."""
    if growth <= 0:
        return None
    a = math.log(1 / alpha)
    b = math.log(1 / beta)
    c = a + width * b / 3
    root = (
        growth * c
        + variance * b
        + math.sqrt(variance * b * (2 * growth * c + variance * b))
    ) / (growth * growth)
    n = max(2, math.ceil(root))

    def passes(m):
        return (
            m * growth - a
            >= math.sqrt(2 * m * variance * b) + width * b / 3
        )

    while not passes(n):
        n += 1
    while n > 2 and passes(n - 1):
        n -= 1
    return n


def rational_log_interval(value, terms=80):
    """Rigorous rational enclosure for log(value), using the atanh series."""
    value = F(value)
    if value <= 0:
        raise ValueError("log argument must be positive")
    z = (value - 1) / (value + 1)
    partial = sum(
        (2 * z ** (2 * k + 1) / (2 * k + 1) for k in range(terms)), F(0)
    )
    tail = 2 * abs(z) ** (2 * terms + 1) / (
        (2 * terms + 1) * (1 - z * z)
    )
    if z < 0:
        return checker.Interval(partial - tail, partial)
    return checker.Interval(partial, partial + tail)


def interval_square(value):
    """Square an interval with exact rational endpoints."""
    lo, hi = value.lo, value.hi
    lower = F(0) if lo <= 0 <= hi else min(lo * lo, hi * hi)
    return checker.Interval(lower, max(lo * lo, hi * hi))


def exact_eprocess_moments(probability_intervals, values, lam, null_mean):
    """Enclose iid log-e mean/variance/range from exact cell intervals."""
    lam, null_mean = F(lam), F(null_mean)
    log_intervals = []
    for value in values:
        factor = 1 - lam * (F(str(value)) - null_mean)
        if factor <= 0:
            raise ValueError("e-process factor must be strictly positive")
        log_intervals.append(rational_log_interval(factor))

    mean_interval = sum(
        (p * z for p, z in zip(probability_intervals, log_intervals)),
        checker.Interval.point(0),
    )
    second_moment = sum(
        (p * interval_square(z) for p, z in zip(probability_intervals, log_intervals)),
        checker.Interval.point(0),
    )
    mean_square = interval_square(mean_interval)
    variance_interval = checker.Interval(
        max(F(0), second_moment.lo - mean_square.hi),
        max(F(0), second_moment.hi - mean_square.lo),
    )
    range_width = max(z.hi for z in log_intervals) - min(z.lo for z in log_intervals)
    return {
        "mean": mean_interval,
        "variance": variance_interval,
        "range_width": range_width,
        "log_increment_intervals": log_intervals,
    }


def outward_float(value, direction):
    rounded = float(value)
    return math.nextafter(rounded, direction)


def exact_interval_power_n(moments_enclosure, alpha=ALPHA, beta=BETA):
    """Sufficient n using outward-rounded interval moments plus a guard."""
    mean = moments_enclosure["mean"]
    variance = moments_enclosure["variance"]
    growth = max(0.0, outward_float(mean.lo, -math.inf) * (1 - 1e-12) - 1e-15)
    var_hi = outward_float(variance.hi, math.inf) * (1 + 1e-12) + 1e-15
    width = outward_float(moments_enclosure["range_width"], math.inf)
    width = width * (1 + 1e-12) + 1e-15
    log_alpha_hi = outward_float(rational_log_interval(F(1, 1) / F(str(alpha)), terms=200).hi, math.inf)
    log_beta_hi = outward_float(rational_log_interval(F(1, 1) / F(str(beta)), terms=200).hi, math.inf)
    if growth <= 0:
        return None, {"growth_lower_guarded": growth}

    def slack(n):
        lhs = n * growth - log_alpha_hi
        rhs = math.sqrt(2 * n * var_hi * log_beta_hi) + width * log_beta_hi / 3
        # This explicit extra slack is far above double-precision roundoff here.
        return lhs - rhs - 1e-10

    low, high = 2, 2
    while slack(high) < 0:
        high *= 2
    low = high // 2
    while low < high:
        mid = (low + high) // 2
        if slack(mid) >= 0:
            high = mid
        else:
            low = mid + 1
    raw_n = low
    reported_n = math.ceil((raw_n * 1.01) / 1000) * 1000
    return reported_n, {
        "raw_sufficient_triplets_before_rounding": raw_n,
        "reported_triplets_after_at_least_one_percent_upward_pad_and_rounding_to_thousand": reported_n,
        "bernstein_inequality_slack_at_reported_count_after_numeric_guard": slack(reported_n),
        "guarded_growth_lower": growth,
        "guarded_variance_upper": var_hi,
        "guarded_log_range_upper": width,
        "log_alpha_upper": log_alpha_hi,
        "log_beta_upper": log_beta_hi,
        "cell_probability_and_log_moment_intervals": "exact rational intervals; atanh-log remainder bounded analytically",
        "float_arithmetic_guard": "outward nextafter conversion, 1e-12 relative moment padding, 1e-15 absolute padding, and 1e-10 Bernstein slack reserve",
    }


def hoeffding_planning_n(d, values, alpha=ALPHA):
    width = max(values) - min(values)
    return math.ceil(width * width * math.log(1 / alpha) / (2 * (d / 2) ** 2))


def empirical_bernstein_planning_n(d, variance, values, alpha=ALPHA):
    """Plug-in sizing only; theorem is valid, but this is not a power guarantee."""
    width = max(values) - min(values)
    logterm = math.log(2 / alpha)
    low, high = 2, 10**9
    while low < high:
        n = (low + high) // 2
        margin = math.sqrt(2 * variance * logterm / n) + (
            7 * width * logterm / (3 * (n - 1))
        )
        if margin <= d / 2:
            high = n
        else:
            low = n + 1
    return low


def multinomial_lr_tail_threshold(k=8, alpha=ALPHA):
    """Finite-n threshold from Guo-Richardson's G_{k,n} <= (1-lambda)^-(k-1)."""
    d = k - 1
    low, high = d + 1e-12, 100.0
    for _ in range(100):
        t = (low + high) / 2
        tail = math.exp(-t + d + d * math.log(t / d))
        if tail > alpha:
            low = t
        else:
            high = t
    return high


def lr_projected_mean(phat, values, kl_radius):
    """Maximize q·values subject to KL(phat||q) <= kl_radius.

    The exact KKT form is q_i proportional to phat_i/(nu-values_i). The fixture
    has positive mass in all eight cells, so the scalar root below is regular.
    """
    assert all(p > 0 for p in phat)

    def at(nu):
        unnormalized = [p / (nu - w) for p, w in zip(phat, values)]
        total = sum(unnormalized)
        q = [v / total for v in unnormalized]
        kl = sum(p * math.log(p / qi) for p, qi in zip(phat, q))
        mean = sum(qi * w for qi, w in zip(q, values))
        return kl, mean

    low = max(values) + 1e-14
    high = 1e8
    for _ in range(200):
        nu = (low + high) / 2
        kl, _ = at(nu)
        if kl > kl_radius:
            low = nu
        else:
            high = nu
    return at(high)


def multinomial_lr_planning_n(phat, mean, d, values, alpha=ALPHA):
    threshold = multinomial_lr_tail_threshold(len(phat), alpha)
    low, high = 2, 10**8
    target_shift = d / 2
    while low < high:
        n = (low + high) // 2
        _, upper = lr_projected_mean(phat, values, threshold / n)
        if upper - mean <= target_shift:
            high = n
        else:
            low = n + 1
    return low, threshold


def kl(p, q):
    return sum(a * math.log(a / b) for a, b in zip(p, q) if a > 0)


def lower_bound_triplets(kl_per_triplet, alpha=ALPHA, power=0.8):
    """Binary data-processing lower bound for one fixed null alternative pair."""
    beta = 1 - power
    binary_kl = power * math.log(power / alpha) + beta * math.log(
        beta / (1 - alpha)
    )
    return binary_kl / kl_per_triplet, binary_kl


def scan_lags():
    """Fixture-only scan minimizing the count for a half-deficit certificate."""
    best = None
    for ti in range(10, 901):
        t = ti / 1000
        p = float_cells(t)
        mean, _ = moments(p, score_values())
        deficit = -mean
        if deficit <= 0:
            continue
        null_mean = -deficit / 2
        for li in range(1, 247):
            lam = li / 200
            if lam >= 1 / (max(score_values()) - null_mean):
                continue
            growth, variance, width = e_process_design(
                p, score_values(), lam, null_mean
            )
            n = sufficient_power_n(growth, variance, width)
            if n is None:
                continue
            candidate = (n, t, lam, growth, variance, width)
            if best is None or candidate[0] < best[0]:
                best = candidate
    return best


def main():
    selected_t = F(1, 4)
    t_float = float(selected_t)
    exact_target = exact_cells(Q_TARGET, selected_t)
    exact_equilibrium = exact_cells(Q_EQUILIBRIUM, selected_t)
    p = [interval_midpoint(exact_target[key]) for key in TRIPLES]
    p_intervals = [exact_target[key] for key in TRIPLES]
    q0 = [interval_midpoint(exact_equilibrium[key]) for key in TRIPLES]
    values = score_values()
    exact_values = score_values_exact()
    mean, variance = moments(p, values)
    d = -mean
    exact_mean_interval = sum(
        (cell * value for cell, value in zip(p_intervals, exact_values)),
        checker.Interval.point(0),
    )
    exact_deficit_interval = -exact_mean_interval
    half_margin_exact = F(-20503, 10_000_000)
    if half_margin_exact > -exact_deficit_interval.hi / 2:
        raise ValueError("fixed half-deficit test threshold is weaker than D_fixture/2")
    half_margin_floor = checker.negative_log_one_minus(
        checker.Interval.point((-half_margin_exact) / (F(9, 10) * F(1, 10)))
    ) * F(4)

    ring_check, _, _ = checker.certificate(
        Q_TARGET, PI, list(map(F, [0, 1, 1])), F(9, 10), [(F(1), selected_t)]
    )
    noise5_check, _, _ = checker.certificate(
        Q_TARGET,
        PI,
        [F(1, 20), F(19, 20), F(19, 20)],
        F(9, 10),
        [(F(1), selected_t)],
    )
    noise2_check, _, _ = checker.certificate(
        Q_TARGET,
        PI,
        [F(1, 50), F(49, 50), F(49, 50)],
        F(9, 10),
        [(F(1), selected_t)],
    )
    equilibrium_check, _, _ = checker.certificate(
        Q_EQUILIBRIUM,
        PI,
        list(map(F, [0, 1, 1])),
        F(9, 10),
        [(F(1), selected_t)],
    )

    grid_best = scan_lags()
    zero_growth, zero_log_variance, zero_log_width = e_process_design(
        p, values, LAMBDA, 0.0
    )
    zero_exact_moments = exact_eprocess_moments(
        p_intervals, exact_values, F(1, 3), F(0)
    )
    n_zero_power, zero_power_diagnostics = exact_interval_power_n(zero_exact_moments)
    half_margin = float(half_margin_exact)
    half_lambda = 1 / 5
    half_growth, half_log_variance, half_log_width = e_process_design(
        p, values, half_lambda, half_margin
    )
    half_exact_moments = exact_eprocess_moments(
        p_intervals, exact_values, F(1, 5), half_margin_exact
    )
    n_half_power, half_power_diagnostics = exact_interval_power_n(
        half_exact_moments
    )
    width_score = max(values) - min(values)
    log_alpha = math.log(1 / ALPHA)
    log_beta = math.log(1 / BETA)

    # Directly reconcile the earlier 3/10-gap, r=9/10 Hoeffding planning
    # number with a valid same-threshold test at that exact legacy design.
    legacy_t = F(3, 10)
    legacy_cells = exact_cells(Q_TARGET, legacy_t)
    legacy_p_intervals = [legacy_cells[key] for key in TRIPLES]
    legacy_mean_interval = sum(
        (cell * value for cell, value in zip(legacy_p_intervals, exact_values)),
        checker.Interval.point(0),
    )
    legacy_deficit_interval = -legacy_mean_interval
    legacy_half_threshold = F(-2241, 1_000_000)
    if legacy_half_threshold > -legacy_deficit_interval.hi / 2:
        raise ValueError("legacy comparison threshold is weaker than D_legacy/2")
    legacy_e_moments = exact_eprocess_moments(
        legacy_p_intervals, exact_values, F(33, 200), legacy_half_threshold
    )
    legacy_e_n, legacy_e_diagnostics = exact_interval_power_n(legacy_e_moments)
    legacy_d_lower = max(
        0.0,
        outward_float(legacy_deficit_interval.lo, -math.inf) * (1 - 1e-12) - 1e-15,
    )
    legacy_radius_n = hoeffding_planning_n(legacy_d_lower, values)
    legacy_gap_to_null = max(
        0.0,
        outward_float(legacy_deficit_interval.lo + legacy_half_threshold, -math.inf)
        * (1 - 1e-12)
        - 1e-15,
    )
    legacy_hoeffding_power_n = math.ceil(
        width_score**2
        * (math.sqrt(log_alpha) + math.sqrt(log_beta)) ** 2
        / (2 * legacy_gap_to_null**2)
    )

    conservative_d = outward_float(exact_deficit_interval.lo, -math.inf)
    conservative_d = max(0.0, conservative_d * (1 - 1e-12) - 1e-15)
    n_hoeffding = hoeffding_planning_n(conservative_d, values)
    n_eb = empirical_bernstein_planning_n(d, variance, values)
    n_lr, lr_threshold = multinomial_lr_planning_n(p, mean, d, values)
    half_gap_to_null = max(
        0.0,
        outward_float(exact_deficit_interval.lo + half_margin_exact, -math.inf)
        * (1 - 1e-12)
        - 1e-15,
    )
    hoeffding_half_margin_power_n = math.ceil(
        width_score**2
        * (math.sqrt(log_alpha) + math.sqrt(log_beta)) ** 2
        / (2 * half_gap_to_null**2)
    )

    kl_pq = kl(p, q0)
    n_lb_real, binary_kl = lower_bound_triplets(kl_pq)

    result = {
        "schema": "astra.snapshot-statistics.plan.v1",
        "scope": "iid stationary mathematical fixture only; no device, detector, bandwidth, dependence, or model validation was acquired",
        "fixture": {
            "target_generator": [[str(v) for v in row] for row in Q_TARGET],
            "stationary_distribution": list(map(str, PI)),
            "binary_labels": LABELS,
            "fixed_gap": str(selected_t),
            "predeclared_score_center_r": "9/10",
            "triplet_order": TRIPLES,
            "score_values": values,
            "exact_target_triplet_probabilities": {
                key: checker.show(exact_target[key]) for key in TRIPLES
            },
            "exact_score_mean": ring_check["mean_score"],
            "exact_score_deficit_D": ring_check["D"],
            "exact_all_even_floor_nats_per_time": ring_check["certified_floor"],
            "score_variance_from_exact_fixture_midpoints": variance,
            "exact_score_mean_interval_used_for_power": checker.show(exact_mean_interval),
            "exact_deficit_interval_used_for_power": checker.show(exact_deficit_interval),
        },
        "lag_and_stake_selection": {
            "method": "floating uniformization planning scan; selected rational lag then recomputed by exact checker",
            "lag_grid": "0.010 through 0.900 by 0.001",
            "stake_grid": "0.005 through 1.230 by 0.005, with lambda < 1/r^2",
            "best_grid_candidate": {
                "triplets": grid_best[0],
                "lag": grid_best[1],
                "lambda": grid_best[2],
                "expected_log_e_growth": grid_best[3],
                "log_e_variance": grid_best[4],
                "log_e_range_width": grid_best[5],
            },
            "selected_predeclared_values": {
                "lag": str(selected_t),
                "r": "9/10",
                "half_margin_test_lambda": "1/5",
                "zero_threshold_test_lambda": "1/3",
                "reason": "simple rational settings near the fixture-only grid minima; fixed before acquisition",
            },
        },
        "fixed_score_e_process": {
            "general_factor_for_candidate_null_mean_u": "1 - lambda*(W-u)",
            "validity": "for each predeclared u and lambda with nonnegative factors, E[W_i | past] >= u makes the product a nonnegative supermartingale; Ville gives P(sup_n E_n(u) >= 1/alpha) <= alpha",
            "zero_mean_test": {
                "u": 0,
                "lambda": "1/3",
                "factor": "1-W/3",
                "alternative_log_growth_per_triplet": zero_growth,
                "alternative_log_variance_per_triplet": zero_log_variance,
                "alternative_log_increment_range_width": zero_log_width,
                "sufficient_iid_triplets_for_95_percent_power": n_zero_power,
            },
            "half_deficit_test": {
                "u": half_margin,
                "lambda": "1/5",
                "null_mean_threshold_u": str(half_margin_exact),
                "implied_all_even_floor_if_test_rejects_nats_per_time": checker.show(half_margin_floor),
                "factor": "1-(W-u)/5",
                "alternative_log_growth_per_triplet": half_growth,
                "alternative_log_variance_per_triplet": half_log_variance,
                "alternative_log_increment_range_width": half_log_width,
                "sufficient_iid_triplets_for_95_percent_power": n_half_power,
                "interpretation": "rejecting E[W] >= u certifies a score deficit strictly larger than D_fixture/2 because fixed rational u is slightly more negative than -D_fixture/2; test error is 5 percent and fixture-specific power bound is 95 percent",
            },
            "alpha": ALPHA,
            "beta_power_error_bound_under_exact_fixture": BETA,
            "power_argument": "Bernstein lower-tail bound for the log e-process under the exact fixture iid law; each tested threshold u is fixed before acquisition",
            "interval_power_diagnostics": {
                "zero_mean_test": zero_power_diagnostics,
                "half_deficit_test": half_power_diagnostics,
            },
        },
        "sample_count_comparison": {
            "legacy_fixed_gap_3_over_10_like_for_like": {
                "exact_score_deficit_D": checker.show(legacy_deficit_interval),
                "fixed_rational_null_mean_threshold_u": str(legacy_half_threshold),
                "e_process_lambda": "33/200",
                "e_process_raw_sufficient_triplets": legacy_e_diagnostics["raw_sufficient_triplets_before_rounding"],
                "e_process_reported_triplets_with_upward_pad": legacy_e_n,
                "e_process_bernstein_slack_after_guard": legacy_e_diagnostics["bernstein_inequality_slack_at_reported_count_after_numeric_guard"],
                "old_hoeffding_half_radius_triplets": legacy_radius_n,
                "hoeffding_same_threshold_5_percent_test_and_95_percent_fixture_power_triplets": legacy_hoeffding_power_n,
                "status": "same fixed gap and r as prior 241709 radius-only calculation; u is a fixed rational slightly more negative than -D/2; test counts have separate size and fixture-power guarantees under iid draws",
            },
            "old_hoeffding_half_deficit_planning": {
                "triplets": n_hoeffding,
                "status": "sets the one-sided Hoeffding radius to D/2; it is a planning radius, not a 95 percent power guarantee for the resulting confidence endpoint",
            },
            "hoeffding_formal_half_deficit_test": {
                "triplets": hoeffding_half_margin_power_n,
                "status": "finite-sample 5 percent test error and at least 95 percent fixture-specific power for the same fixed rational u; calculation uses a conservative lower bound on the exact fixture-to-threshold mean gap",
            },
            "empirical_bernstein_population_variance_plugin": {
                "triplets": n_eb,
                "status": "plug-in sizing only; fixed-score EB upper confidence bound is valid, but this number is not a formal power guarantee",
            },
            "full_8_cell_multinomial_lr_projection_plugin": {
                "triplets": n_lr,
                "lr_deviance_threshold": lr_threshold,
                "status": "finite-sample valid confidence region projected to the same score; expected table substituted for random counts, so planning geometry only",
            },
            "fixed_score_e_process_sufficient_power": {
                "triplets": n_half_power,
                "status": "valid 5 percent half-deficit test with a separate 95 percent fixture-specific power guarantee under iid fixture draws",
            },
        },
        "same_snapshot_likelihood_comparator": {
            "all_eight_cell_confidence_region": "C={q: n KL(p_hat||q) <= t}; optimize q dot w over C, without collapsing the eight observable cells",
            "finite_sample_tail_bound": "Guo-Richardson Chernoff bound using G_{k,n}(lambda) <= (1-lambda)^-(k-1); no Wilks approximation used",
            "strongest_model_comparator": "profile the complete eight-cell likelihood over all compatible all-even hidden-CTMC/readout laws, and compare against reflected-moment or other same-snapshot methods at equal preparation/calibration/analysis budget",
            "unresolved": "unbounded hidden-state model class is not characterized computationally here; this worker does not establish superiority over that comparator",
        },
        "information_lower_bound_separate_from_planning": {
            "null_model": "three-state complete-graph equilibrium CTMC, each off-diagonal rate 14/25, uniform stationary law, same labels and lag",
            "null_score_mean": equilibrium_check["mean_score"],
            "null_triplet_probabilities": {
                key: checker.show(exact_equilibrium[key]) for key in TRIPLES
            },
            "kl_target_to_this_null_nats_per_triplet": kl_pq,
            "kl_numerics": "computed from exact-rationally enclosed cell probabilities using double-precision natural logarithms; the analytic lower bound is n >= kl(0.8||0.05)/D(p||q) and is reported to nearest integer",
            "test_size_alpha": ALPHA,
            "target_power": 0.8,
            "binary_kl_required_nats": binary_kl,
            "necessary_triplets_for_any_test_of_this_pair": math.ceil(n_lb_real),
            "scope": "data-processing lower bound for this specified exact alternative versus this one explicit valid equilibrium null; not a universal lower bound over every hidden model or physical acquisition design",
        },
        "physical_gates": {
            "5_percent_iid_symmetric_readout_error_exact_score_mean": noise5_check["mean_score"],
            "5_percent_iid_symmetric_readout_error_result": "positive population score; this selected r/law has no negative-mean certificate even with infinitely many iid triplets",
            "2_percent_iid_symmetric_readout_error_exact_score_mean": noise2_check["mean_score"],
            "real_readout_noise_or_bandwidth": "not measured; snapshot impulse response, missed-state errors, memory, and back-action remain unacquired",
            "dependence": "no independent-preparation or dependence-control interface acquired; overlapping windows do not meet the e-process iid plan",
            "physical_model": "the all-even CTMC and physical time-reversal premises remain unvalidated; no physical reversal/energy ledger was acquired",
        },
        "exact_fixture_checker": {
            "checker_path": str(CHECKER_PATH),
            "selected_lag_certificate_status": "PASS via imported exact rational checker",
            "noise_falsifier_status": "exact rational calculation; no experiment",
            "source_checker_sha256": "02c76587799b84c5c3c8573e797fdf0a8f2b5aaaebad8e8d6f56488b80eacee1",
            "source_checker_provenance": "byte-identical copy from research/2026-10-15-operational-closure-v1/root/verify_snapshot_operation.py; verified with cmp and sha256sum",
        },
        "sources": [
            "https://arxiv.org/abs/0907.3740",
            "https://arxiv.org/abs/2003.08614",
            "https://doi.org/10.1214/20-AOS1991",
        ],
        "status": "SCOPED_STATISTICAL_PLANNING_ONLY",
    }
    out = HERE / "RESULTS.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "best_grid": result["lag_and_stake_selection"]["best_grid_candidate"],
        "e_process_zero_test_n": n_zero_power,
        "e_process_half_deficit_n": n_half_power,
        "hoeffding_half_deficit_power_n": hoeffding_half_margin_power_n,
        "hoeffding_n": n_hoeffding,
        "empirical_bernstein_plugin_n": n_eb,
        "multinomial_lr_plugin_n": n_lr,
        "info_lower_bound_n_for_selected_pair": math.ceil(n_lb_real),
        "results": str(out),
    }, indent=2))


if __name__ == "__main__":
    main()

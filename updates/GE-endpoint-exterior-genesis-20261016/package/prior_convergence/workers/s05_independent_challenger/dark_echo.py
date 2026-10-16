"""Finite-time one-channel loss-echo replay (synthetic, no physical data).

The script tests exact two-state echo algebra, a drift-robust binary assay for
the two one-pulse aliases, and a gain-free three-setting dark-rate estimator.
Only NumPy is required.  All probabilities are per independently reset sample.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ALIASES = ((2.0, 1.0, 2.0, 3.0), (1.0, 1.0, 2.0, 4.0))


def expm2(B: np.ndarray, t: float) -> np.ndarray:
    """Analytic real 2x2 exponential for the Metzler matrices used here."""
    m = np.trace(B) / 2.0
    X = B - m * np.eye(2)
    k2 = X[0, 0] ** 2 + X[0, 1] * X[1, 0]
    k = math.sqrt(max(0.0, k2))
    if k < 1e-12:
        return math.exp(m * t) * (np.eye(2) + t * X)
    return math.exp(m * t) * (
        math.cosh(k * t) * np.eye(2) + math.sinh(k * t) / k * X
    )


def matrices(par: tuple[float, float, float, float], u: float = 1.0):
    a, r, d1, d2 = par
    A = np.array([[-a, r], [a, -r]], dtype=float)
    M = A - u * np.diag([d1, d2])
    return A, M


def survival(
    par: tuple[float, float, float, float],
    t1: float,
    wait: float,
    t2: float,
    u: float = 1.0,
) -> float:
    A, M = matrices(par, u)
    b = np.array([1.0, 0.0])
    x = expm2(M, t2) @ expm2(A, wait) @ expm2(M, t1) @ b
    return float(np.sum(x))


def dark_contrast(par, t1, wait, t2, u=1.0):
    return survival(par, t1, wait, t2, u) - survival(par, t1, 0.0, t2, u)


def binlog(k: int, n: int, p: float) -> float:
    return k * math.log(p) + (n - k) * math.log1p(-p)


def envelope_profile_loglik(k_e, k_r, n, p_r_range, ratio_range):
    """Best joint binomial likelihood over a convex probability envelope.

    This is the strongest likelihood fit using only the same two counts and
    the published reference/echo probability interval bounds.  The envelope
    relaxes correlations among dose, gain, and the physical model, so it is
    conservative relative to a fully constrained physical GLRT.
    """
    lo, hi = p_r_range
    rlo, rhi = ratio_range

    def objective(p_r):
        p_e = min(max(k_e / n, rlo * p_r), rhi * p_r)
        return binlog(k_r, n, p_r) + binlog(k_e, n, p_e)

    # The profile is concave because the feasible region in (p_r,p_e) is a
    # convex wedge and binomial log likelihood is jointly concave.
    invphi = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c = b - invphi * (b - a)
    d = a + invphi * (b - a)
    fc, fd = objective(c), objective(d)
    for _ in range(150):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - invphi * (b - a)
            fc = objective(c)
        else:
            a, c, fc = c, d, fd
            d = a + invphi * (b - a)
            fd = objective(d)
    return max(fc, fd, objective(lo), objective(hi))


def certified_alias_design():
    """Monotone-endpoint bounds for independent dose drift in two assay arms."""
    t = 0.275
    wait = 2.0
    dose_min, dose_max = 0.995, 1.005
    relative_readout_drift = 0.005
    q_ref_min = 0.75
    rows = []
    for par in ALIASES:
        # Survival is decreasing in dose by the pathwise killing formula.
        e_min = survival(par, 0, wait, t, dose_max)
        e_max = survival(par, 0, wait, t, dose_min)
        r_min = survival(par, 0, 0, t, dose_max)
        r_max = survival(par, 0, 0, t, dose_min)
        rows.append(
            dict(
                echo_nominal=survival(par, 0, wait, t),
                reference_nominal=survival(par, 0, 0, t),
                echo_range=[e_min, e_max],
                reference_range=[r_min, r_max],
                ratio_range=[e_min / r_max, e_max / r_min],
            )
        )
    # World 0 has the higher echo/reference ratio.
    lower_world0 = (1 - relative_readout_drift) * rows[0]["ratio_range"][0]
    upper_world1 = (1 + relative_readout_drift) * rows[1]["ratio_range"][1]
    gap = lower_world0 - upper_world1
    assert gap > 0
    threshold = (lower_world0 + upper_world1) / 2
    reference_min = min(row["reference_range"][0] for row in rows)
    alpha = 0.05
    # Hoeffding for T = mean(echo) - threshold * mean(reference).
    n_each = math.ceil(
        2
        * (1 + threshold**2)
        * math.log(1 / alpha)
        / (q_ref_min**2 * reference_min**2 * gap**2)
    )
    rng = np.random.default_rng(59125)
    nominal_q = 0.8
    draws = []
    for row in rows:
        p_e = nominal_q * row["echo_nominal"]
        p_r = nominal_q * row["reference_nominal"]
        k_e = int(rng.binomial(n_each, p_e))
        k_r = int(rng.binomial(n_each, p_r))
        statistic = (k_e - threshold * k_r) / n_each
        draws.append(
            dict(
                echo_successes=k_e,
                reference_successes=k_r,
                statistic=statistic,
                classifier="world0" if statistic > 0 else "world1",
            )
        )
    assert draws[0]["classifier"] == "world0"
    assert draws[1]["classifier"] == "world1"
    # Same-information incumbent: profile the *joint* binomial likelihood
    # over each hypothesis' allowed nuisance envelope, with both counts.
    for draw in draws:
        loglikes = []
        for row in rows:
            ref_range = [q_ref_min * row["reference_range"][0],
                         row["reference_range"][1]]
            ratio_range = [
                (1 - relative_readout_drift) * row["ratio_range"][0],
                (1 + relative_readout_drift) * row["ratio_range"][1],
            ]
            loglikes.append(
                envelope_profile_loglik(
                    draw["echo_successes"], draw["reference_successes"],
                    n_each, ref_range, ratio_range
                )
            )
        draw["same_information_profile_loglik_difference_world0_minus_world1"] = (
            loglikes[0] - loglikes[1]
        )
        draw["same_information_profile_classifier"] = (
            "world0" if loglikes[0] > loglikes[1] else "world1"
        )
        assert draw["same_information_profile_classifier"] == draw["classifier"]
    # Small seeded stress comparison; this is a simulation, not a guarantee.
    stress_rng = np.random.default_rng(22510)
    stress = []
    for n_stress in (3000, 10000, 30000):
        for h, row in enumerate(rows):
            p_r = nominal_q * row["reference_nominal"]
            p_e = nominal_q * row["echo_nominal"]
            threshold_errors = 0
            profile_errors = 0
            for _ in range(300):
                k_r = int(stress_rng.binomial(n_stress, p_r))
                k_e = int(stress_rng.binomial(n_stress, p_e))
                threshold_guess = 0 if k_e - threshold * k_r > 0 else 1
                likes = []
                for candidate in rows:
                    ref_range = [
                        q_ref_min * candidate["reference_range"][0],
                        candidate["reference_range"][1],
                    ]
                    ratio_range = [
                        (1 - relative_readout_drift)
                        * candidate["ratio_range"][0],
                        (1 + relative_readout_drift)
                        * candidate["ratio_range"][1],
                    ]
                    likes.append(
                        envelope_profile_loglik(
                            k_e, k_r, n_stress, ref_range, ratio_range
                        )
                    )
                profile_guess = 0 if likes[0] > likes[1] else 1
                threshold_errors += threshold_guess != h
                profile_errors += profile_guess != h
            stress.append(
                dict(
                    n_each=n_stress,
                    true_world=h,
                    repetitions=300,
                    threshold_errors=threshold_errors,
                    profile_likelihood_errors=profile_errors,
                )
            )
    return dict(
        t=t,
        wait=wait,
        dose_interval=[dose_min, dose_max],
        relative_readout_drift=relative_readout_drift,
        q_reference_lower=q_ref_min,
        worlds=rows,
        robust_ratio_gap=gap,
        statistic_threshold=threshold,
        reference_survival_lower=reference_min,
        n_each_for_error_at_most_0p05=n_each,
        nominal_synthetic_draws=draws,
        synthetic_stress=stress,
    )


def quotient_replay():
    """Three-setting dark-rate extraction with unknown common detector gain."""
    t = 0.31
    wait = 0.525
    q = 0.8
    alpha = 0.05
    n_each = 10_000_000
    rng = np.random.default_rng(8749)
    results = []
    for par in ALIASES:
        true_p = [q * survival(par, 0, j * wait, t) for j in (0, 1, 2)]
        true_c1 = true_p[1] - true_p[0]
        true_c2 = true_p[2] - true_p[0]
        true_ratio = true_c2 / true_c1
        true_g = par[0] + par[1]
        assert abs(true_ratio - (1 + math.exp(-true_g * wait))) < 2e-14
        z = true_ratio - 1
        held_out_p3 = q * survival(par, 0, 3 * wait, t)
        predicted_p3 = true_p[0] + true_c1 * (1 + z + z * z)
        assert abs(held_out_p3 - predicted_p3) < 2e-14
        counts = [int(rng.binomial(n_each, p)) for p in true_p]
        phat = [k / n_each for k in counts]
        c1 = abs(phat[1] - phat[0])
        c2 = abs(phat[2] - phat[0])
        epsilon = math.sqrt(math.log(6 / alpha) / (2 * n_each))
        assert c1 > 2 * epsilon and c2 > 2 * epsilon
        ratio_lo = (c2 - 2 * epsilon) / (c1 + 2 * epsilon)
        ratio_hi = (c2 + 2 * epsilon) / (c1 - 2 * epsilon)
        assert 1 < ratio_lo < ratio_hi < 2
        g_lo = -math.log(ratio_hi - 1) / wait
        g_hi = -math.log(ratio_lo - 1) / wait
        g_hat = -math.log(c2 / c1 - 1) / wait
        assert g_lo < true_g < g_hi
        results.append(
            dict(
                true_g=true_g,
                true_probabilities=true_p,
                true_ratio=true_ratio,
                held_out_p3=held_out_p3,
                predicted_p3_from_three_settings=predicted_p3,
                counts=counts,
                estimated_g=g_hat,
                hoeffding_95pct_interval=[g_lo, g_hi],
            )
        )
    return dict(
        t=t,
        wait=wait,
        detector_gain=q,
        n_each=n_each,
        total_trials=3 * n_each,
        alpha=alpha,
        per_setting_error_radius=epsilon,
        worlds=results,
    )


def theorem_checks():
    rng = np.random.default_rng(12605)
    max_error = 0.0
    for _ in range(100):
        a, r = rng.uniform(0.2, 5, 2)
        d1, d2 = rng.uniform(0.3, 6, 2)
        if abs(d1 - d2) < 0.05:
            d2 += 0.1
        par = (a, r, d1, d2)
        t1, t2, wait = rng.uniform(0.05, 1, 3)
        c1 = dark_contrast(par, t1, wait, t2)
        c2 = dark_contrast(par, t1, 2 * wait, t2)
        if abs(c1) > 1e-10:
            err = abs(c2 / c1 - (1 + math.exp(-(a + r) * wait)))
            max_error = max(max_error, err)
            # A common affine terminal readout p=f+q*S cancels in the same
            # contrast quotient, even with both offset and unknown gain.
            offset, gain = 0.03, 0.8
            p0 = offset + gain * survival(par, t1, 0, t2)
            p1 = offset + gain * survival(par, t1, wait, t2)
            p2 = offset + gain * survival(par, t1, 2 * wait, t2)
            affine_err = abs((p2 - p0) / (p1 - p0)
                             - (1 + math.exp(-(a + r) * wait)))
            max_error = max(max_error, affine_err)
    assert max_error < 1e-10
    # s04's exact one-pulse aliases have the same on-only survival at u=1.
    for t in np.linspace(0, 2, 21):
        assert abs(survival(ALIASES[0], 0, 0, t) - survival(ALIASES[1], 0, 0, t)) < 2e-14
    return dict(randomized_exact_echo_checks=100, max_quotient_error=max_error)


def main():
    out = dict(
        theorem_checks=theorem_checks(),
        robust_alias_design=certified_alias_design(),
        dark_rate_quotient=quotient_replay(),
    )
    (HERE / "FOLLOWUP_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

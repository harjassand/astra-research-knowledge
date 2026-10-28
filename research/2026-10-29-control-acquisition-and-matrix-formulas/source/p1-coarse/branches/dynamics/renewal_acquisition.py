"""Membership-only acquisition of a reversible rank-one residual certificate.

The private backend has two live states plus cemetery. The learner receives
only first-step membership and the time/parity of the first subsequent
return. Absorbed updates may be skipped computationally but are CHARGED
through the censoring horizon, since the observer cannot recognize cemetery.
"""
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
import argparse
import json
import math
from pathlib import Path
import numpy as np

getcontext().prec = 80
SLACK = D("1e-40")


def dec(x):
    if isinstance(x, F):
        return D(x.numerator) / D(x.denominator)
    return D(int(x))


def binomial_interval(x, n, ell):
    x, n, ell = dec(x), dec(n), dec(ell)
    lo = max(D(0), (x - (2 * ell * x).sqrt()) / n - SLACK)
    hi = min(D(1), (x + ell + (ell*ell + 2*ell*x).sqrt()) / n + SLACK)
    return lo, hi


def source_parameters(inv_g, label):
    if label == 0:
        den, self0, cross, self1 = inv_g, inv_g-1, 1, inv_g//4
    else:
        den, self0, cross, self1 = 3*inv_g, 3*inv_g-6, 3, inv_g
    assert inv_g % 4 == 0
    return {"den": den, "self0": self0, "cross": cross, "self1": self1,
            "g": F(1, inv_g), "t": F(self0, den), "fast": F(self1, den),
            "a": 1-F(1, 2*inv_g)}


def first_return_trials(rng, p, n, horizon):
    # Only the aggregate observations below are supplied to the learner.
    first = rng.integers(p["den"], size=n)
    departures = int(np.count_nonzero(first >= p["self0"]))
    live = int(np.count_nonzero((first >= p["self0"]) &
                               (first < p["self0"] + p["cross"])))
    hist = {}
    backend_draws = n
    for time in range(2, horizon+1):
        if live == 0:
            break  # Unobservable absorption still receives the full charge below.
        draws = rng.integers(p["den"], size=live)
        returned = int(np.count_nonzero(draws < p["cross"]))
        if returned:
            hist[time] = returned
        backend_draws += live
        live = int(np.count_nonzero((draws >= p["cross"]) &
                                   (draws < p["cross"] + p["self1"])))
    returns = sum(hist.values())
    even = sum(count for time, count in hist.items() if time % 2 == 0)
    charged = n + (horizon-1)*departures - sum(
        (horizon-time)*count for time, count in hist.items())
    return {"trials": n, "horizon": horizon, "departures": departures,
            "returns": returns, "even": even, "odd": returns-even,
            "return_time_histogram": hist, "charged_primitive_steps": charged,
            "charged_membership_readings": charged,
            "backend_rng_draws": backend_draws}


def one_step_trials(rng, p, n):
    departures = 0
    remaining = n
    while remaining:
        count = min(remaining, 1_000_000)
        departures += int(np.count_nonzero(
            rng.integers(p["den"], size=count) >= p["self0"]))
        remaining -= count
    return departures


def choose_horizon(a, d2_upper, tolerance):
    aa = dec(a)
    horizon = max(2, math.ceil(math.log(float(
        tolerance * (1-aa) / d2_upper)) / math.log(float(aa))) + 1)
    while aa**(horizon-1)*d2_upper/(1-aa) + SLACK > tolerance:
        horizon += 1
    tail = aa**(horizon-1)*d2_upper/(1-aa) + SLACK
    return horizon, tail


def acquired_certificate(a, pilot, main, departures, total, ell, tail):
    qlo, qhi = binomial_interval(departures, total, ell)
    tlo, thi = 1-qhi, 1-qlo
    that = 1-dec(departures)/dec(total)
    delta = max(that-tlo, thi-that) + SLACK
    _, rhi0 = binomial_interval(main["returns"], main["trials"], ell)
    _, ehi0 = binomial_interval(main["even"], main["trials"], ell)
    olo, _ = binomial_interval(main["odd"], main["trials"], ell)
    rhi, ehi = min(D(1), rhi0+tail), min(D(1), ehi0+tail)
    shi = max(D(0), min(rhi, ehi0-olo+tail))
    gap = 1-dec(a)
    den_plus = max(gap, 1-thi-rhi)
    den_minus = max(gap, 1+tlo-shi)
    q_upper = ehi + rhi*rhi/(2*den_plus) + shi*shi/(2*den_minus) + SLACK
    q_model_upper = (q_upper.sqrt() + delta/(1-dec(a)**2).sqrt())**2 + SLACK
    loss = 1-that*that
    theta2 = q_model_upper/loss + SLACK
    correction_noise = delta/loss + SLACK
    return {"t_estimate": str(that), "t_lower": str(tlo), "t_upper": str(thi),
            "t_error_upper": str(delta), "return_total_upper": str(rhi),
            "return_even_upper": str(ehi), "return_signed_upper": str(shi),
            "missed_return_tail_upper": str(tail),
            "true_Galerkin_weighted_residual_upper": str(q_upper),
            "estimated_model_weighted_residual_upper": str(q_model_upper),
            "coefficient_dissipation": str(loss),
            "theta_squared_upper": str(theta2),
            "correction_noise_upper": str(correction_noise)}


def run_source(inv_g, label, pilot_n, main_n, total, ell, tail_divisor, seed):
    p = source_parameters(inv_g, label)
    a, t, c, g = (p[key] for key in ("a", "t", "fast", "g"))
    # Check the fixture's advertised cap; this is not learner acquisition.
    assert a >= t and a >= c and (a-t)*(a-c) >= g*g
    assert t*c >= g*g
    rng = np.random.default_rng(seed)
    pilot = first_return_trials(rng, p, pilot_n, 2)
    _, d2_upper = binomial_interval(pilot["returns"], pilot_n, ell)
    tolerance = dec(g*g)/dec(tail_divisor)
    horizon, tail = choose_horizon(a, d2_upper, tolerance)
    main = first_return_trials(rng, p, main_n, horizon)
    extra = total-pilot_n-main_n
    assert extra >= 0
    extra_departures = one_step_trials(rng, p, extra)
    departures = pilot["departures"]+main["departures"]+extra_departures
    cert = acquired_certificate(a, pilot, main, departures, total, ell, tail)
    r, s = g*g/(1-c), g*g/(1+c)
    even = (r+s)/2
    true_q = even + r*r/(2*(1-t-r)) + s*s/(2*(1+t-s))
    truth_contained = (D(cert["t_lower"]) <= dec(t) <= D(cert["t_upper"])
                       and dec(true_q) <= D(cert["true_Galerkin_weighted_residual_upper"]))
    assert truth_contained
    steps = pilot["charged_primitive_steps"] + main["charged_primitive_steps"] + extra
    return {"source": label, "source_cap_premise": str(a),
            "pilot": pilot, "first_return": main,
            "extra_one_step_calibration": {"trials": extra, "departures": extra_departures},
            "pooled_first_step_calibration": {"trials": total, "departures": departures},
            "certificate": cert,
            "oracle_validation_only": {
                "t": str(t), "two_step_depart_return_probability": str(g*g),
                "first_return_probability": str(r),
                "first_return_even_probability": str(even),
                "weighted_residual": str(true_q),
                "weighted_residual_float": float(true_q),
                "oracle_inside_acquired_bounds": truth_contained},
            "charged_cost": {"logical_trials": total,
                             "physical_preparations_upper": 1+departures-pilot["returns"]-main["returns"],
                             "primitive_steps": steps,
                             "membership_readings": steps,
                             "longest_trajectory": horizon},
            "seed": seed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inverse-g", type=int, default=20)
    parser.add_argument("--pilot", type=int, default=20_000)
    parser.add_argument("--returns", type=int, default=100_000)
    parser.add_argument("--total-calibration", type=int, default=2_000_000)
    parser.add_argument("--ell", type=int, default=10)
    parser.add_argument("--tail-divisor", type=int, default=20)
    args = parser.parse_args()
    sources = [run_source(args.inverse_g, i, args.pilot, args.returns,
                          args.total_calibration, args.ell, args.tail_divisor,
                          2026102800+1000*args.inverse_g+i) for i in range(2)]
    theta2 = max(D(s["certificate"]["theta_squared_upper"]) for s in sources)
    noise = max(D(s["certificate"]["correction_noise_upper"]) for s in sources)
    result = {
        "method": "Positive first-return parity observations with finite censoring",
        "g": str(F(1, args.inverse_g)), "arguments": vars(args),
        "observation_contract": (
            "Reset at b; membership predicate only. Stop at time-1 self-loop "
            "or first return. Cemetery is unobserved and censored trials "
            "are charged through their full horizon."
        ),
        "sources": sources,
        "joint_failure_probability_upper": 12*math.exp(-args.ell),
        "all_words_same_calibration": {
            "twice_theta_squared_upper": str(2*theta2),
            "correction_noise_upper": str(noise),
            "total_scalar_output_error_upper": str(2*theta2+noise+SLACK)},
        "total_charged_cost": {
            key: sum(s["charged_cost"][key] for s in sources)
            for key in ("logical_trials", "physical_preparations_upper",
                        "primitive_steps", "membership_readings")},
        "arithmetic": "80-digit Decimal confidence envelopes, 1e-40 outward slack; exact rational oracle.",
        "no_hidden_rank_used_by_certificate": True}
    path = Path(__file__).with_name(
        f"RENEWAL_RESULTS_g{args.inverse_g}_n{args.returns}_cal{args.total_calibration}.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "g": result["g"],
        "joint_failure_probability_upper": result["joint_failure_probability_upper"],
        "horizons": [s["first_return"]["horizon"] for s in sources],
        "return_counts": [s["first_return"]["returns"] for s in sources],
        "Q_upper": [float(D(s["certificate"]["true_Galerkin_weighted_residual_upper"]))
                    for s in sources],
        "all_word_error_upper": float(2*theta2+noise),
        "cost": result["total_charged_cost"],
        "output": str(path)}, indent=2))


if __name__ == "__main__":
    main()

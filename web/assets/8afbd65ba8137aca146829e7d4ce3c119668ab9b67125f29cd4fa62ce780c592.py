#!/usr/bin/env python3
"""Reproduce the finite-volume guarded-relay calculations in CYCLE2_ADDENDUM.md.

Uses only Python's standard library. Exact gambler's-ruin and infinite-wait
resolvent quantities use fractions.Fraction. Timed probability, occupancy,
and reward values use floating-point uniformization; Poisson bounds control
series truncation but do not certify floating-point roundoff.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction as F

V = 100
LOWER_SAFE = 10
UPPER_GUARD = 55
START_H = 45
TRANSIENT = tuple(range(LOWER_SAFE + 1, UPPER_GUARD))
OMEGA = 200
DEADLINE = 1.0


def rates_h(n: int) -> tuple[F, F]:
    """(birth, death) molecule-event rates in mode H."""
    return F(2 * (V - n)), F(n)


def fmt_fraction(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def solve_tridiagonal(lower: list[F], diagonal: list[F], upper: list[F], rhs: list[F]) -> list[F]:
    """Exact Thomas algorithm; lower[0] and upper[-1] are ignored."""
    n = len(diagonal)
    assert n and len(lower) == len(diagonal) == len(upper) == len(rhs)
    cprime = [F(0)] * n
    dprime = [F(0)] * n
    denominator = diagonal[0]
    assert denominator != 0
    cprime[0] = upper[0] / denominator
    dprime[0] = rhs[0] / denominator
    for i in range(1, n):
        denominator = diagonal[i] - lower[i] * cprime[i - 1]
        assert denominator != 0
        cprime[i] = upper[i] / denominator if i < n - 1 else F(0)
        dprime[i] = (rhs[i] - lower[i] * dprime[i - 1]) / denominator
    solution = [F(0)] * n
    solution[-1] = dprime[-1]
    for i in range(n - 2, -1, -1):
        solution[i] = dprime[i] - cprime[i] * solution[i + 1]
    return solution


def resolvent_expectation(reward) -> F:
    """Return E_45[int_0^T reward(N_s) ds], T=hit{10,55}."""
    lower, diagonal, upper, rhs = [], [], [], []
    for n in TRANSIENT:
        birth, death = rates_h(n)
        lower.append(-death)
        diagonal.append(birth + death)
        upper.append(-birth)
        rhs.append(F(reward(n)))
    values = solve_tridiagonal(lower, diagonal, upper, rhs)
    return values[START_H - TRANSIENT[0]]


def safe_target_probability_exact() -> F:
    """Birth-death scale-function/gambler's-ruin probability, exactly."""
    # Harmonic increments d_m = h(m)-h(m-1) obey d_(n+1)=mu_n/lambda_n*d_n.
    increment = F(1)
    increments = {LOWER_SAFE + 1: increment}
    for n in range(LOWER_SAFE + 1, UPPER_GUARD):
        birth, death = rates_h(n)
        increment *= death / birth
        increments[n + 1] = increment
    numerator = sum((increments[m] for m in range(LOWER_SAFE + 1, START_H + 1)), F(0))
    denominator = sum((increments[m] for m in range(LOWER_SAFE + 1, UPPER_GUARD + 1)), F(0))
    return numerator / denominator


def uniformization_probability(t: float) -> dict:
    """Floating-point P(hit 55 by t before 10) via full-chain uniformization."""
    # Keep n=10 and n=55 as absorbing states. These are the 44 transient
    # states plus both absorbing states: 46 coordinates total.
    states = tuple(range(LOWER_SAFE, UPPER_GUARD + 1))
    index = {n: i for i, n in enumerate(states)}
    p = [0.0] * len(states)
    p[index[START_H]] = 1.0
    mean = OMEGA * t
    # This is deliberately wider than needed at mean 200; the omitted right
    # tail starts at K+1. The bound below is for P(Poisson(mean)>K).
    K = int(mean + 12 * math.sqrt(mean + 1) + 80)
    weight = math.exp(-mean)
    probability = 0.0
    for k in range(K + 1):
        probability += weight * p[index[UPPER_GUARD]]
        if k == K:
            break
        q = [0.0] * len(states)
        q[index[LOWER_SAFE]] = p[index[LOWER_SAFE]]
        q[index[UPPER_GUARD]] = p[index[UPPER_GUARD]]
        for n in TRANSIENT:
            i = index[n]
            birth, death = rates_h(n)
            birth_p = float(birth / OMEGA)
            death_p = float(death / OMEGA)
            stay_p = 1.0 - birth_p - death_p
            q[index[n + 1]] += p[i] * birth_p
            q[index[n - 1]] += p[i] * death_p
            q[i] += p[i] * stay_p
        p = q
        weight *= mean / (k + 1)
    # For X~Poisson(mean), P(X>=K+1) <= exp(-mean+(K+1)(1+ln(mean/(K+1))))
    # when K+1 > mean. This controls truncation only, not float roundoff.
    cutoff = K + 1
    tail_bound = math.exp(-mean + cutoff * (1.0 + math.log(mean / cutoff)))
    return {
        "probability_float_truncated": probability,
        "poisson_mean": mean,
        "uniformization_rate_per_second": OMEGA,
        "last_included_poisson_index": K,
        "first_omitted_poisson_index": cutoff,
        "omitted_poisson_mass_chernoff_upper_bound": tail_bound,
        "roundoff_certified": False,
    }


def uniformization_occupancy(t: float, P_hold: F, E_obs: F, E_cpu: F,
                             E_birth: F, E_death: F, E_sw: F) -> dict:
    """One-leg deadline occupancy/cost, with a truncation bound, in float.

    The transient embedded chain is substochastic: moves into 10 or 55 leave
    its 44 coordinates. Uniformization gives
      o(t) = sum_k P(Poisson(Omega*t)>k)/Omega * e_45^T P^k.
    The Poisson weights are evaluated by a backward tail sum. Both this
    evaluation and the matrix recursion use binary64, so roundoff is not
    certified; the reported bounds cover only omitted series terms.
    """
    mean = OMEGA * t
    K = int(mean + 12 * math.sqrt(mean + 1) + 80)
    # A finite table suffices to evaluate weights through K. The remaining
    # tail above MAX_POISSON is itself bounded and negligible at this scale.
    max_poisson = max(2000, K + 500)
    pmf = [math.exp(-mean + k * math.log(mean) - math.lgamma(k + 1))
           for k in range(max_poisson + 1)]
    tail_ge = [0.0] * (max_poisson + 2)
    for k in range(max_poisson, -1, -1):
        tail_ge[k] = tail_ge[k + 1] + pmf[k]

    p = [0.0] * len(TRANSIENT)
    p[START_H - TRANSIENT[0]] = 1.0
    occupancy = [0.0] * len(TRANSIENT)
    for k in range(K + 1):
        occupancy_weight = tail_ge[k + 1] / OMEGA
        for i, mass in enumerate(p):
            occupancy[i] += occupancy_weight * mass
        if k == K:
            break
        q = [0.0] * len(TRANSIENT)
        for n in TRANSIENT:
            i = n - TRANSIENT[0]
            birth, death = rates_h(n)
            bp, dp = float(birth / OMEGA), float(death / OMEGA)
            q[i] += p[i] * (1.0 - bp - dp)
            if n + 1 in TRANSIENT:
                q[i + 1] += p[i] * bp
            if n - 1 in TRANSIENT:
                q[i - 1] += p[i] * dp
        p = q

    probability_result = uniformization_probability(t)
    p_hit = probability_result["probability_float_truncated"]
    births = sum(occupancy[i] * float(rates_h(n)[0]) for i, n in enumerate(TRANSIENT))
    deaths = sum(occupancy[i] * float(rates_h(n)[1]) for i, n in enumerate(TRANSIENT))
    elapsed = sum(occupancy)
    observed_events = births + deaths
    H_chemical_cost = float(E_birth) * births + float(E_death) * deaths
    L_chemical_cost = float(E_birth) * deaths + float(E_death) * births
    common_non_switch = float(P_hold) * elapsed + float(E_obs + E_cpu) * observed_events
    H_cost = common_non_switch + H_chemical_cost + float(E_sw) * p_hit
    L_cost = common_non_switch + L_chemical_cost + float(E_sw) * p_hit

    # If X~Poisson(mean), omitted occupancy coefficients after k=K sum to
    # sum_{m=K+2}^inf P(X>=m). A geometric tail-ratio bound gives this <=
    # P(X>=K+1)/(1-mean/(K+3)); use the Chernoff bound for the numerator.
    cutoff = K + 1
    poisson_tail = math.exp(-mean + cutoff * (1.0 + math.log(mean / cutoff)))
    occupancy_tail_bound = poisson_tail / (1.0 - mean / (K + 3)) / OMEGA
    max_rate_cost = max(
        float((E_obs + E_cpu) * sum(rates_h(n)) + E_birth * rates_h(n)[0] + E_death * rates_h(n)[1])
        for n in TRANSIENT
    )
    max_reflected_rate_cost = max(
        float((E_obs + E_cpu) * sum(rates_h(n)) + E_birth * rates_h(n)[1] + E_death * rates_h(n)[0])
        for n in TRANSIENT
    )
    cost_tail_bound = (float(P_hold) + max(max_rate_cost, max_reflected_rate_cost)) * occupancy_tail_bound
    cost_tail_bound += float(E_sw) * poisson_tail
    # The PMF table omits X>max_poisson. Bound this omitted weight separately.
    table_tail_cut = max_poisson + 1
    table_poisson_tail = math.exp(-mean + table_tail_cut * (1.0 + math.log(mean / table_tail_cut)))
    if table_poisson_tail > 0.0:
        # Each required upper-tail weight can be off by at most this mass.
        # Summed over k<=K and divided by Omega gives a conservative addition.
        table_occupancy_error = (K + 1) * table_poisson_tail / OMEGA
        occupancy_tail_bound += table_occupancy_error
        cost_tail_bound += (float(P_hold) + max(max_rate_cost, max_reflected_rate_cost)) * table_occupancy_error

    return {
        "deadline_seconds": t,
        "transient_expected_occupation_seconds_sum": elapsed,
        "H_expected_birth_events_before_stop": births,
        "H_expected_death_events_before_stop": deaths,
        "expected_observed_events_before_stop": observed_events,
        "H_expected_cost_joules": H_cost,
        "L_expected_cost_joules": L_cost,
        "switch_cost_included_as_Esw_times_p_hit": True,
        "H_and_L_switch_charge_joules": float(E_sw) * p_hit,
        "holding_power_included_through_absorption_or_deadline": True,
        "per_leg_success_probability_float_truncated": p_hit,
        "per_leg_probability_poisson_truncation_bound": poisson_tail,
        "occupancy_L1_poisson_truncation_bound_seconds": occupancy_tail_bound,
        "per_leg_cost_poisson_truncation_bound_joules": cost_tail_bound,
        "roundoff_certified": False,
    }


def main() -> None:
    p_hit = safe_target_probability_exact()
    expected_time = resolvent_expectation(lambda _n: F(1))
    expected_births = resolvent_expectation(lambda n: rates_h(n)[0])
    expected_deaths = resolvent_expectation(lambda n: rates_h(n)[1])
    timed = uniformization_probability(DEADLINE)
    timed_M_survival = timed["probability_float_truncated"]**20
    timed_M_tail_bound = 20 * timed["omitted_poisson_mass_chernoff_upper_bound"]

    # Example costs in SI units. P_m is active mode-hold power; E_sw is an
    # additional instantaneous switch charge, so these are distinct terms.
    P_s, P_c, P_m = F(20, 1000), F(5, 1000), F(100, 1000)  # watts
    E_obs, E_cpu = F(1, 1000), F(2, 10000)  # joules per observed event
    E_birth, E_death, E_sw = F(5, 10000), F(2, 10000), F(5, 100)  # joules
    timed_costs = uniformization_occupancy(
        DEADLINE, P_s + P_c + P_m, E_obs, E_cpu, E_birth, E_death, E_sw
    )
    holding_cost = expected_time * (P_s + P_c + P_m)
    observe_process_cost = (E_obs + E_cpu) * (expected_births + expected_deaths)
    switch_cost = E_sw * p_hit

    def expected_leg_cost(births: F, deaths: F) -> tuple[F, F, F, F]:
        reaction_cost = E_birth * births + E_death * deaths
        return holding_cost, observe_process_cost, reaction_cost, holding_cost + observe_process_cost + reaction_cost + switch_cost

    h_cost_parts = expected_leg_cost(expected_births, expected_deaths)
    # Under n -> 100-n reflection, an L birth is an H death and vice versa.
    l_cost_parts = expected_leg_cost(expected_deaths, expected_births)
    h_total, l_total = h_cost_parts[-1], l_cost_parts[-1]
    legs = 20
    alternating_expected_total = F(0)
    continuation_probability = F(1)
    for leg in range(legs):
        alternating_expected_total += continuation_probability * (h_total if leg % 2 == 0 else l_total)
        continuation_probability *= p_hit
    timed_alternating_expected_total = 0.0
    timed_continuation = 1.0
    for leg in range(legs):
        timed_alternating_expected_total += timed_continuation * (
            timed_costs["H_expected_cost_joules"] if leg % 2 == 0 else timed_costs["L_expected_cost_joules"]
        )
        timed_continuation *= timed_costs["per_leg_success_probability_float_truncated"]

    result = {
        "model": {
            "volume": V,
            "mode_H_birth_rate": "2*(100-n)",
            "mode_H_death_rate": "n",
            "safe_lower_absorbing_state": LOWER_SAFE,
            "target_upper_absorbing_state": UPPER_GUARD,
            "start_state": START_H,
            "transient_state_count": len(TRANSIENT),
        },
        "exact_infinite_wait_until_target_or_safe_exit": {
            "safe_target_probability": fmt_fraction(p_hit),
            "safe_exit_probability": fmt_fraction(1 - p_hit),
            "expected_duration_seconds": fmt_fraction(expected_time),
            "expected_birth_events": fmt_fraction(expected_births),
            "expected_death_events": fmt_fraction(expected_deaths),
            "expected_total_events": fmt_fraction(expected_births + expected_deaths),
            "reflected_L_expected_birth_events": fmt_fraction(expected_deaths),
            "reflected_L_expected_death_events": fmt_fraction(expected_births),
        },
        "twenty_leg_no_deadline_relay": {
            "all_legs_success_probability_formula": "p_infinity^20 using the exact p_infinity fraction above",
            "at_least_one_leg_failure_probability_float": float(1 - p_hit**legs),
            "success_probability_float_note": "The exact success probability rounds to 1.0 in binary64 because its complement is about 4.50e-25; use the exact fraction or failure complement.",
            "expected_total_energy_until_first_failed_leg_or_20_successes_joules_float": float(alternating_expected_total),
            "expected_total_energy_computed_with_exact_fraction_intermediates": True,
            "leg_order": "H,L,H,L,...",
            "note": "Per-leg expected costs differ because the illustrative birth and death event charges differ; continuation probability is p_hit after each leg.",
        },
        "one_second_deadline": timed,
        "twenty_legs_one_second_per_leg": {
            "success_probability_float_truncated": timed_M_survival,
            "propagated_poisson_truncation_error_upper_bound": timed_M_tail_bound,
            "roundoff_certified": False,
            "note": "M=20 times the one-leg absolute tail bound is valid by |a^M-b^M|<=M|a-b| for a,b in [0,1]; floating-point roundoff remains unbounded here.",
        },
        "one_second_deadline_expected_cost_and_occupancy": timed_costs,
        "twenty_legs_one_second_per_leg_expected_cost": {
            "expected_energy_until_first_failed_leg_or_20_successes_joules_float": timed_alternating_expected_total,
            "failure_shutdown_cost_included": False,
            "uses_H_L_asymmetric_costs": True,
            "roundoff_certified": False,
        },
        "illustrative_unbounded_leg_expected_cost": {
            "units": "joules",
            "holding_power_watts": {
                "sensor": float(P_s),
                "controller_clock": float(P_c),
                "active_mode_hold": float(P_m),
                "combined": float(P_s + P_c + P_m),
            },
            "H_leg_cost_exact": {
                "holding": fmt_fraction(h_cost_parts[0]),
                "observed_and_processed_events": fmt_fraction(h_cost_parts[1]),
                "chemical_birth_death_events": fmt_fraction(h_cost_parts[2]),
                "successful_switch": fmt_fraction(switch_cost),
                "total": fmt_fraction(h_total),
                "total_float": float(h_total),
            },
            "L_leg_cost_exact": {
                "holding": fmt_fraction(l_cost_parts[0]),
                "observed_and_processed_events": fmt_fraction(l_cost_parts[1]),
                "chemical_birth_death_events": fmt_fraction(l_cost_parts[2]),
                "successful_switch": fmt_fraction(switch_cost),
                "total": fmt_fraction(l_total),
                "total_float": float(l_total),
            },
            "switch_charge_exact": fmt_fraction(switch_cost),
            "switch_charge_rule": "E_sw * p_hit for the mode's target-before-unsafe hit by its deadline; failed/unsafe legs incur no successful-switch charge",
            "scope": "No deadline; each leg stops at target or unsafe boundary. No fault-shutdown fee is included.",
        },
        "finite_deadline_cost_identity": (
            "For deadline t, transient occupancy o_n(t)=E[time spent in transient state n before min(t,tau_10,tau_55)]. "
            "Charge (P_s+P_c+P_m)*sum_n o_n plus rate-weighted event costs using the same o_n; "
            "charge E_sw*p_H(t), where p_H(t)=P(tau_55<=t,tau_55<tau_10). "
            "This occupancy includes holding power through target hit, unsafe hit, or the deadline. "
            "If fault shutdown costs E_fault, add E_fault*(1-p_H(t)) when every non-success is fault-stopped."
        ),
        "limitations": [
            "One-second probability is floating-point uniformization; its Poisson-tail bound excludes floating-point roundoff.",
            "Example energy parameters are illustrative, not measured hardware values.",
            "The infinite-wait expected cost is for one attempted H-leg and is not an infinite-horizon safe-operating guarantee.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

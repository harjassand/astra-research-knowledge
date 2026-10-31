"""Complete bivariate factory, executed through an acquired address dictionary.

Target f(p,q)=1/4+p^8 q^8/4. The numerical source means are visible only to
the fixture's independent validator. The factory uses dictionary.flip(address)
and fresh auxiliary fair bits. This elementary target has a much cheaper
ordinary sixteen-coin construction; it tests the acquired representation and
the exact multivariate correction, not a practical advantage.

Mathematical certificate:
  u_n(t)=(nt)_8/(n)_8, g_n(x,y)=1/4+u_n(x)u_n(y)/4.
The Bernstein expectation of g_n is exactly f, and H_n g_n=g_2n. Use
coefficient envelopes g_n +/- c/n^3, n0=64, c=n0^3/16. Count-grid values of
g_n are in [1/4,1/2]; every envelope coefficient is in [0,1]. Both shrinkage
masses are 7c/(8n^3), and the new continuation mass is c/(4n^3).

Write d0=(n0)_8/n0^8. For n>=n0, |u_n^(k)(t)|<=(8)_k/d0 on [0,1], because
each factor |t-j/n|<=1. Therefore, for
  T=max_{a+b=8}(8)_a(8)_b/[4*8!*d0^2],
the degree-seven Taylor remainder is bounded by T(|Y1|+|Y2|)^8 and hence by
E(Y)=128T(Y1^8+Y2^8). Its expectation is at most 768T/n^4. The exact
rational assertion below verifies 768T/n0^4 <=7c/(16n0^3), so 2E0 is at
most the shrinkage mass at every later doubled level too. This proves
nonnegativity and the common mass bound 2c/n^3. No empirical constants are
used in this certificate.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, factorial
from pathlib import Path
import json
import random
import sys
import time

from randomized_elevation import (
    RationalOracle, ProductEnvelope, ElevationRace, FairBits,
    falling, integerize_rationals,
)


N0 = 64
CWIDTH = F(N0 ** 3, 16)
D0 = F(falling(N0, 8), N0 ** 8)
TAYLOR_BOUND = max(
    F(falling(8, a) * falling(8, 8 - a), 4 * factorial(8)) / D0 ** 2
    for a in range(9)
)
ENVELOPE_SCALE = 2 ** 7 * TAYLOR_BOUND
assert 6 * ENVELOPE_SCALE / N0 ** 4 <= 7 * CWIDTH / (16 * N0 ** 3)


def coefficient_oracle(n, direction):
    coeffs = [F(1)]
    for j in range(8):
        nxt = [F(0)] * (len(coeffs) + 1)
        for k, val in enumerate(coeffs):
            nxt[k] -= j * val
            nxt[k + 1] += n * val
        coeffs = nxt
    coeffs = tuple(c / falling(n, 8) for c in coeffs)

    @lru_cache(maxsize=None)
    def univariate_derivative(t, order):
        return sum(coeffs[k] * falling(k, order) * t ** (k - order)
                   for k in range(order, len(coeffs)))

    def derivative(point, beta):
        assert len(point) == len(beta) == 2
        value = univariate_derivative(point[0], beta[0]) * univariate_derivative(point[1], beta[1]) / 4
        if beta == (0, 0):
            value += F(1, 4) + direction * CWIDTH / n ** 3
        return value

    return RationalOracle(lambda point: derivative(point, (0, 0)), derivative)


def factory(dictionary, addresses, bits, diagnostics):
    """No source probabilities, tables, or hidden scopes enter this function."""
    if len(addresses) != 2:
        raise ValueError("two acquired addresses are required")
    n = N0
    counts = [sum(dictionary.flip(address) for _ in range(n)) for address in addresses]
    diagnostics["source_flips"] += 2 * n
    point = tuple(F(s, n) for s in counts)
    low = coefficient_oracle(n, -1).value(point)
    high = coefficient_oracle(n, 1).value(point)
    decision = bits.integer_weighted(integerize_rationals((low, 1 - high, high - low)))
    if decision != 2:
        return (1, 0)[decision]
    while True:
        for i, address in enumerate(addresses):
            counts[i] += sum(dictionary.flip(address) for _ in range(n))
        diagnostics["source_flips"] += 2 * n
        point = tuple(F(s, 2 * n) for s in counts)
        envelope = ProductEnvelope(n, counts, r=4, K=0, scale=ENVELOPE_SCALE)
        race = ElevationRace(
            coefficient_oracle(n, -1), coefficient_oracle(n, 1),
            coefficient_oracle(2 * n, -1).value(point),
            coefficient_oracle(2 * n, 1).value(point),
            envelope, common_bound=2 * CWIDTH / n ** 3,
        )
        outcome = race.sample(bits)
        diagnostics["elevation_stages"] += 1
        diagnostics["race_attempts"] += race.attempts
        diagnostics["tilted_draws"] += envelope.draws
        diagnostics["support_terms"] += envelope.support_terms
        diagnostics["max_source_level_per_coordinate"] = max(
            diagnostics["max_source_level_per_coordinate"], 2 * n
        )
        if outcome is not None:
            return outcome
        n *= 2


def exhaustive_transition_check(n=64, totals=(95, 111)):
    point = tuple(F(s, 2 * n) for s in totals)
    env = ProductEnvelope(n, totals, r=4, K=0, scale=ENVELOPE_SCALE)
    race = ElevationRace(
        coefficient_oracle(n, -1), coefficient_oracle(n, 1),
        coefficient_oracle(2 * n, -1).value(point),
        coefficient_oracle(2 * n, 1).value(point), env, 2 * CWIDTH / n ** 3,
    )
    plus = minus = total_Q = F(0)
    smallest = race.bound
    largest = F(0)
    checked = 0
    nonzero_remainders = 0
    for ks in product(*env.supports):
        y = tuple(F(2 * k - s, 2 * n) for k, s in zip(ks, totals))
        bound = env.value(y)
        if not bound:
            continue
        probability = F(1)
        for k, s in zip(ks, totals):
            probability *= F(comb(s, k) * comb(2 * n - s, n - k), comb(2 * n, n))
        tilted = probability * bound / env.expectation
        total_Q += tilted
        newpoint = tuple(F(k, n) for k in ks)
        rlow = race.lower.oracle.value(newpoint) - race.lower.evaluate(y)
        rhigh = race.upper.oracle.value(newpoint) - race.upper.evaluate(y)
        assert abs(rlow) <= bound and abs(rhigh) <= bound
        nonzero_remainders += int(rlow != 0 or rhigh != 0)
        up = race.lower_next - race.lower.expectation - env.expectation * rlow / bound
        um = race.upper.expectation + env.expectation * rhigh / bound - race.upper_next
        assert 0 <= up <= race.bound and 0 <= um <= race.bound
        smallest = min(smallest, up, um)
        largest = max(largest, up, um)
        plus += tilted * up
        minus += tilted * um
        checked += 1
    desired = 7 * CWIDTH / (8 * n ** 3)
    assert total_Q == 1
    assert plus == minus == desired
    width = race.upper_next - race.lower_next
    assert width == CWIDTH / (4 * n ** 3)
    old_width = 2 * CWIDTH / n ** 3
    assert (plus / old_width, minus / old_width, width / old_width) == (F(7, 16), F(7, 16), F(1, 8))
    return {
        "n": n, "totals": list(totals), "dimension": 2,
        "vectors_exhaustively_checked_validation_only": checked,
        "nonzero_taylor_remainders": nonzero_remainders,
        "univariate_support_terms_production": env.support_terms,
        "accept_one": "7/16", "accept_zero": "7/16", "continue": "1/8",
        "exact_mass_equalities_and_pointwise_bounds_passed": True,
        "smallest_increment_estimator": float(smallest),
        "largest_increment_estimator": float(largest),
        "envelope_expectation": str(env.expectation),
    }


def main(draws=500):
    started = time.monotonic()
    control_path = Path(__file__).resolve().parent.parent / "broad_control"
    sys.path.insert(0, str(control_path))
    from acquisition_fixture_demo import run_demo

    dictionary, validation_truth, acquisition_result = run_demo()
    # Select by acquired symbolic labels; no response value is inspected.
    addresses = tuple(
        next(a for a in dictionary.addresses()
             if a.component == component and sum(a.assignment) == 1)
        for component in (0, 1)
    )
    initial_source_ledger = dictionary.source.represented_bit_trials
    bits = FairBits(random.Random(178833).getrandbits)
    diagnostics = {
        "source_flips": 0, "elevation_stages": 0, "race_attempts": 0,
        "tilted_draws": 0, "support_terms": 0,
        "max_source_level_per_coordinate": N0,
    }
    outputs = [factory(dictionary, addresses, bits, diagnostics) for _ in range(draws)]
    execution_ledger = dictionary.source.represented_bit_trials - initial_source_ledger
    assert execution_ledger == diagnostics["source_flips"]
    # Only the validator now reads the source's hidden numerical truth.
    actual_means = tuple(validation_truth.mean(a.component, dictionary.canonical_context(a))
                         for a in addresses)
    target = F(1, 4) + actual_means[0] ** 8 * actual_means[1] ** 8 / 4
    exact_check = exhaustive_transition_check()
    result = {
        "purpose": "Acquisition-to-exact-multivariate-execution fixture; ordinary sixteen-coin construction is much cheaper for this target.",
        "source_access": "The factory receives only dictionary.flip(address); hidden means are used after execution by the validator.",
        "learned_scopes": [list(s) for s in dictionary.scopes],
        "dictionary_entries": len(dictionary.addresses()),
        "selected_addresses": [a.label() for a in addresses],
        "charged_acquisition_bit_trials": acquisition_result["charged_acquisition_physical_bit_trials"],
        "charged_acquisition_input_setting_bit_work": acquisition_result["acquisition"]["input_setting_bit_work"],
        "separate_acquisition_demo_adaptive_calls": acquisition_result["adaptive_fresh_dictionary_calls"],
        "scope_failure_budget": acquisition_result["scope_failure_budget"],
        "draws": draws,
        "hidden_means_validation_only": list(map(str, actual_means)),
        "exact_target_probability_validation_only": str(target),
        "target_probability_float_for_display": float(target),
        "observed_success_fraction": sum(outputs) / draws,
        "observed_mean_execution_source_flips": execution_ledger / draws,
        "theorem_expected_execution_source_flips": 7 * N0 / 3,
        "execution_input_setting_bit_work": execution_ledger * dictionary.source.input_dimension,
        "auxiliary_fair_bits_seeded_PRNG_for_demo": bits.bits,
        "taylor_bound_T": str(TAYLOR_BOUND),
        "certified_envelope_mean_bound_at_start": str(6 * ENVELOPE_SCALE / N0 ** 4),
        "half_shrinkage_mass_at_start": str(7 * CWIDTH / (16 * N0 ** 3)),
        "certificate_inequality_verified_by_exact_rational_arithmetic": True,
        "exact_transition_check": exact_check,
        **diagnostics,
        "elapsed_seconds_nonportable": time.monotonic() - started,
        "limits": "Simulation counts represent independent trials and charge them all. The large sufficient discovery bill is not a practical or minimal cost claim. Mathematical factory exactness is conditional on correct acquired scopes and stationary independent source laws; the empirical frequency is only a Monte Carlo check.",
    }
    Path(__file__).with_name("multivariate_factory_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

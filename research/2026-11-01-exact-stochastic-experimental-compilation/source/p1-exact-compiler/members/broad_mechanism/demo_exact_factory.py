"""End-to-end exact factory fixture exercising randomized degree elevation.

Target f(p)=1/4+p^8/4 is intentionally elementary: an ordinary eight-coin
construction is much cheaper. This is a correctness/implementation fixture,
not evidence of practical advantage. The factory receives only source.flip.

Proof: g_n(x)=1/4+(nx)_8/[4(n)_8] is an exact Bernstein coefficient function
for f. Therefore H_n g_n=g_2n. Let a_n=g_n-c/n^3, b_n=g_n+c/n^3,
n0=64,c=n0^3/16. On every count grid g_n lies in [1/4,1/2], so the bounds
lie in [0,1]. Each shrinkage mass is 7c/(8n^3); the new width is c/(4n^3).
The degree-seven Taylor remainder is exactly C_n Y^8, where
C_n=n^8/[4(n)_8]<=C=C_n0. The envelope C Y^8(1+|Y|) dominates it.
E envelope <= (9/2)C/n^4, by the eighth-moment Hoeffding bound. Thus all
increment estimators are nonnegative and <=2c/n^3 when n>=72C/(7c), which
holds at n0 and all doubled levels. Exactness follows from the elevation
race lemma. Expected source flips are n0+8c/(3n0^2)=7n0/6.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import random
import time

from randomized_elevation import (
    RationalOracle, ProductEnvelope, ElevationRace, FairBits,
    falling, integerize_rationals,
)


N0 = 64
CWIDTH = F(N0 ** 3, 16)
CREMAINDER = F(N0 ** 8, 4 * falling(N0, 8))
assert N0 >= 72 * CREMAINDER / (7 * CWIDTH)


def coefficient_oracle(n, direction):
    coeffs = [F(1)]
    for j in range(8):
        nxt = [F(0)] * (len(coeffs) + 1)
        for k, val in enumerate(coeffs):
            nxt[k] -= j * val
            nxt[k + 1] += n * val
        coeffs = nxt
    coeffs = [c / (4 * falling(n, 8)) for c in coeffs]
    coeffs[0] += F(1, 4) + direction * CWIDTH / n ** 3

    def derivative(point, beta):
        assert len(point) == len(beta) == 1
        order = beta[0]
        return sum(coeffs[k] * falling(k, order) * point[0] ** (k - order)
                   for k in range(order, len(coeffs)))

    return RationalOracle(lambda point: derivative(point, (0,)), derivative)


class SimulatedSource:
    def __init__(self, probability, bits):
        self._probability = F(probability)
        self._bits = bits
        self.calls = 0

    def flip(self):
        self.calls += 1
        return self._bits.bernoulli(self._probability)


def factory(source, bits, diagnostics):
    n = N0
    s = sum(source.flip() for _ in range(n))
    low = coefficient_oracle(n, -1).value((F(s, n),))
    high = coefficient_oracle(n, 1).value((F(s, n),))
    decision = bits.integer_weighted(integerize_rationals((low, 1 - high, high - low)))
    if decision != 2:
        return (1, 0)[decision]
    while True:
        s += sum(source.flip() for _ in range(n))
        point = (F(s, 2 * n),)
        envelope = ProductEnvelope(n, (s,), r=4, K=1, scale=CREMAINDER)
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
        diagnostics["max_source_level"] = max(diagnostics["max_source_level"], 2 * n)
        if outcome is not None:
            return outcome
        n *= 2


def exhaustive_transition_check(n=64, total=75):
    point = (F(total, 2 * n),)
    env = ProductEnvelope(n, (total,), r=4, K=1, scale=CREMAINDER)
    race = ElevationRace(
        coefficient_oracle(n, -1), coefficient_oracle(n, 1),
        coefficient_oracle(2 * n, -1).value(point),
        coefficient_oracle(2 * n, 1).value(point), env, 2 * CWIDTH / n ** 3,
    )
    plus = minus = total_Q = F(0)
    min_mass = race.bound
    max_mass = F(0)
    for k in env.supports[0]:
        y = (F(2 * k - total, 2 * n),)
        B = env.value(y)
        if not B:
            continue
        P = F(comb(total, k) * comb(2 * n - total, n - k), comb(2 * n, n))
        Q = P * B / env.expectation
        total_Q += Q
        newpoint = (F(k, n),)
        rem_low = race.lower.oracle.value(newpoint) - race.lower.evaluate(y)
        rem_high = race.upper.oracle.value(newpoint) - race.upper.evaluate(y)
        up = race.lower_next - race.lower.expectation - env.expectation * rem_low / B
        um = race.upper.expectation + env.expectation * rem_high / B - race.upper_next
        assert 0 <= up <= race.bound and 0 <= um <= race.bound
        min_mass = min(min_mass, up, um)
        max_mass = max(max_mass, up, um)
        plus += Q * up
        minus += Q * um
    desired = 7 * CWIDTH / (8 * n ** 3)
    assert total_Q == 1
    assert plus == minus == desired
    continuation = race.upper_next - race.lower_next
    assert continuation == CWIDTH / (4 * n ** 3)
    old_width = 2 * CWIDTH / n ** 3
    assert plus / old_width == F(7, 16)
    assert minus / old_width == F(7, 16)
    assert continuation / old_width == F(1, 8)
    return {
        "n": n, "total": total,
        "support_terms": env.support_terms,
        "all_mass_estimators_nonnegative_and_bounded": True,
        "accept_one": "7/16", "accept_zero": "7/16", "continue": "1/8",
        "exact_equality_verified": True,
        "minimum_estimator": float(min_mass), "maximum_estimator": float(max_mass),
        "envelope_mean": float(env.expectation),
    }


def main(draws=1000):
    started = time.monotonic()
    exact_check = exhaustive_transition_check()
    rows = []
    for j, p in enumerate((F(0), F(1, 3), F(2, 3), F(1))):
        rng = random.Random(9401 + j)
        bits = FairBits(rng.getrandbits)
        source = SimulatedSource(p, bits)
        diagnostics = {"elevation_stages": 0, "race_attempts": 0,
                       "tilted_draws": 0, "support_terms": 0,
                       "max_source_level": N0}
        successes = sum(factory(source, bits, diagnostics) for _ in range(draws))
        target = F(1, 4) + p ** 8 / 4
        rows.append({
            "input_probability": str(p), "draws": draws,
            "target_probability": str(target),
            "observed_success_fraction": successes / draws,
            "source_flips": source.calls,
            "mean_source_flips": source.calls / draws,
            "theorem_expected_source_flips": 7 * N0 / 6,
            "ideal_fair_bit_calls_replaced_by_seeded_PRNG_for_demo": bits.bits,
            **diagnostics,
        })
    result = {
        "purpose": "Exact-bit implementation validation; the direct eight-coin factory is cheaper for this toy target.",
        "exact_transition_check": exact_check,
        "end_to_end": rows,
        "elapsed_seconds_nonportable": time.monotonic() - started,
    }
    Path(__file__).with_name("exact_factory_demo_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

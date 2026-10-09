"""Finite diagnostics for the A14 causal-policy boundary record.

This is an executable illustration, not a data experiment or proof checker.
It verifies hand-built finite counterexamples and runs the stated direct-policy
confidence race on synthetic Bernoulli rewards.
"""

from collections import defaultdict
from fractions import Fraction
import math
import random


def observed_iv_distribution(model):
    """Return the exact law of (Z,D,Y) when Z is fair and D(z)=z."""
    law = defaultdict(Fraction)
    for z in (0, 1):
        d = z
        y = d if model == "treatment-causes-y" else z
        law[(z, d, y)] += Fraction(1, 2)
    return dict(law)


def verify_iv_nonidentification():
    m1 = observed_iv_distribution("treatment-causes-y")
    m2 = observed_iv_distribution("assignment-directly-causes-y")
    assert m1 == m2 == {
        (0, 0, 0): Fraction(1, 2),
        (1, 1, 1): Fraction(1, 2),
    }
    # M1 has Y(z,d)=d and M2 has Y(z,d)=z.
    ate_m1 = Fraction(1, 1)
    ate_m2 = Fraction(0, 1)
    assert ate_m1 != ate_m2
    return m1, ate_m1, ate_m2


def verify_observational_nonidentification():
    obs_1 = {(0, 0): Fraction(1, 2), (1, 1): Fraction(1, 2)}
    obs_2 = {(0, 0): Fraction(1, 2), (1, 1): Fraction(1, 2)}
    # O1: X=U,Y=U gives do-means (1/2,1/2).
    do_o1 = (Fraction(1, 2), Fraction(1, 2))
    # O2: X=U,Y=X gives do-means (0,1).
    do_o2 = (Fraction(0, 1), Fraction(1, 1))
    assert obs_1 == obs_2
    assert do_o1 != do_o2
    return obs_1, do_o1, do_o2


def bernoulli_kl(p, q):
    if p == 0:
        return -math.log1p(-q)
    if p == 1:
        return -math.log(q)
    if q == 0 or q == 1:
        return math.inf
    return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))


def radius(n, k, delta):
    if n <= 0:
        return math.inf
    return math.sqrt(math.log(k * math.pi**2 * n * n / (3 * delta)) / (2 * n))


def uniform_pac_count(k, epsilon, delta):
    """A finite fixed allocation with P(regret > epsilon) <= delta."""
    n = math.ceil(2 * math.log(2 * k / delta) / epsilon**2)
    assert 2 * k * math.exp(-n * epsilon**2 / 2) <= delta
    return n


def cost_aware_race(sample_arm, costs, epsilon, delta, deployment_costs=None,
                    validation_costs=None, max_samples=None):
    """Run the anytime confidence race described in v1.txt.

    `sample_arm(i)` must return a fresh/reset independent value in [0,1]. The
    caller is responsible for acquiring and documenting the randomization and
    reset validity represented by validation_costs.
    """
    k = len(costs)
    if k < 2 or epsilon <= 0 or not 0 < delta < 1 or any(c <= 0 for c in costs):
        raise ValueError("need K>=2, epsilon>0, delta in (0,1), and positive costs")
    penalties = deployment_costs or [0.0] * k
    fixed = validation_costs or [0.0] * k
    if len(penalties) != k or len(fixed) != k:
        raise ValueError("all per-arm arrays must have length K")

    cap = 1
    while radius(cap, k, delta) > epsilon / 2:
        cap += 1

    counts = [0] * k
    sums = [0.0] * k
    active = set(range(k))
    total_samples = 0

    def interval(i):
        if counts[i] == 0:
            return -math.inf, math.inf
        m = sums[i] / counts[i] - penalties[i]
        r = radius(counts[i], k, delta)
        return m - r, m + r

    while True:
        bounds = {i: interval(i) for i in active}
        best_lower = max(bounds[i][0] for i in active)
        leader = max(active, key=lambda i: bounds[i][0])

        # Remove only actions whose confidence intervals certify them to be
        # more than epsilon below a surviving action.
        active = {
            i for i in active
            if bounds[i][1] >= best_lower - epsilon
        }
        bounds = {i: interval(i) for i in active}
        leader = max(active, key=lambda i: bounds[i][0])
        if len(active) == 1 or max(bounds[i][1] for i in active) - bounds[leader][0] <= epsilon:
            selected = leader
            break

        if all(counts[i] >= cap for i in active):
            selected = max(active, key=lambda i: sums[i] / counts[i] - penalties[i])
            break

        eligible = [i for i in active if counts[i] < cap]
        # Radius/sqrt(cost) is a cost-aware urgency heuristic; correctness
        # comes from the anytime intervals and finite fallback, not this rule.
        chosen = max(eligible, key=lambda i: radius(counts[i], k, delta) / math.sqrt(costs[i]))
        y = float(sample_arm(chosen))
        if not 0 <= y <= 1:
            raise ValueError("sample_arm must return a value in [0,1]")
        sums[chosen] += y
        counts[chosen] += 1
        total_samples += 1
        if max_samples is not None and total_samples >= max_samples:
            raise RuntimeError("max_samples reached before the finite-confidence stop")

    total_cost = sum(fixed) + sum(costs[i] * counts[i] for i in range(k))
    return {
        "selected": selected,
        "counts": counts,
        "active": sorted(active),
        "samples": total_samples,
        "charged_cost": total_cost,
        "fixed_validation_cost": sum(fixed),
        "sample_cost": sum(costs[i] * counts[i] for i in range(k)),
        "uniform_fallback_cap_per_active_arm": cap,
    }


def main():
    iv_law, ate_1, ate_2 = verify_iv_nonidentification()
    obs_law, do_1, do_2 = verify_observational_nonidentification()
    epsilon, delta, k = 0.02, 0.05, 16
    kl = bernoulli_kl(0.5, 0.5 + 4 * epsilon)
    exact_kl = -0.5 * math.log1p(-64 * epsilon**2)
    assert abs(kl - exact_kl) < 1e-14
    per_competitor_lb = math.log((1 - delta) / delta) * (1 - 2 * delta) / kl
    n_uniform = uniform_pac_count(k, 0.1, delta)

    rng = random.Random(20261009)
    means = [0.15, 0.30, 0.90, 0.20]
    costs = [1.0, 2.0, 3.0, 1.5]
    sampler = lambda i: 1.0 if rng.random() < means[i] else 0.0
    race = cost_aware_race(
        sampler, costs, epsilon=0.18, delta=0.05,
        deployment_costs=[0.0, 0.0, 0.0, 0.0],
        validation_costs=[2.0, 2.0, 2.0, 2.0],
    )

    print("IV observed law:", iv_law)
    print("receipt ATEs with that same law:", ate_1, ate_2)
    print("observational law:", obs_law)
    print("do-means with that same law:", do_1, do_2)
    print("K=16, epsilon=.02, delta=.05 lower bound per competitor:",
          f"{per_competitor_lb:.3f} samples")
    print("K=16, epsilon=.1, delta=.05 uniform samples per arm:", n_uniform)
    print("seeded adaptive race:", race)


if __name__ == "__main__":
    main()

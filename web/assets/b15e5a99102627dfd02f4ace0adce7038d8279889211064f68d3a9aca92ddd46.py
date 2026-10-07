"""Completely capped no-field-balancing count for the symmetric trace lift.

All-size confidence remains conditional on Chen--Liu Lemma 5.5. No generic
FPRAS is called. Conservative default admission refuses prohibitive work
BEFORE any random bit/chain step; the saved run does not claim a full FPRAS.
"""
from dataclasses import dataclass
from fractions import Fraction as F

from xxz_local_chain import (CoinTape, LocalExchange, TapeAbort, ceil_log2_fraction,
                             mixing_steps, product_fraction)


class ResourceRefusal(RuntimeError):
    def __init__(self, plan):
        self.plan = plan
        super().__init__(f"planned {plan['total_steps']} steps exceeds supplied admission")


def ceiling(x):
    x = F(x)
    return (x.numerator + x.denominator - 1) // x.denominator


def acquired_complement_ratio(instance):
    """Finite rational bound mu(S)/mu(S^c); raises on asymmetric support.

    The other factor must have half-size disjoint quotas, as in trace counts.
    This is a NUMERIC bias parameter, not a free logarithmic-range substitute.
    """
    if (2 * instance.mu_degree != instance.n or 2 * instance.nu_degree != instance.n or
            any(2 * rank != len(coordinates) for coordinates, rank in instance.groups)):
        raise ValueError("half-degree complement-invariant quota support required")
    ratio = F(1)
    for factor in instance.factors:
        full = (1 << len(factor.coordinates)) - 1
        if any((full ^ mask) not in factor.table for mask in factor.table):
            raise ValueError("mu support is not complement invariant")
        ratio *= max(value / factor.table[full ^ mask] for mask, value in factor.table.items())
    assert ratio >= 1
    return ratio


def nofield_plan(instance, rho=F(1, 10), delta=F(1, 4), *, allow_bounded_bias=False):
    rho, delta = F(rho), F(delta)
    if not instance.complement_symmetric() and not allow_bounded_bias:
        raise ValueError("default no-balancing interface requires complement symmetry")
    bias_ratio = acquired_complement_ratio(instance)
    if not 0 < rho <= 1 or not 0 < delta <= F(1, 4):
        raise ValueError("invalid relative accuracy or confidence")
    n = instance.n
    if n < 1:
        return {"n": 0, "total_steps": 0, "total_samples": 0,
                "trivial_count": 1 << instance.inactive_qubits}
    t = F(1, 256 * n * n) / bias_ratio
    alpha = rho / (128 * n)
    # Binary logs overcount natural logs, avoiding a floating/log oracle.
    M = ceiling(2 / (alpha * alpha) * max(1, ceil_log2_fraction(16 * n / delta)))
    ac = rho / 64
    Mc = ceiling(2 / (ac * ac) * max(1, ceil_log2_fraction(8 / delta)))
    J = mixing_steps(instance, t, [F(1)] * n, alpha / 2)
    samples = 2 * n * M + Mc
    height = max(1, (n - 1).bit_length())
    choices = samples * J * (2 * height + 2)
    bits_per_choice = max(1, ceil_log2_fraction(F(4 * choices) / delta))
    return {"n": n, "t": t, "alpha": alpha, "rho": rho, "delta": delta,
            "complement_ratio": bias_ratio, "numeric_bias_parameter_charged": True,
            "mass_samples_per_stage": M, "complement_samples": Mc,
            "steps_per_sample": J, "total_samples": samples,
            "total_steps": samples * J, "choice_cap": choices,
            "bits_per_choice": bits_per_choice, "random_bits_cap": choices * bits_per_choice}


def count_nofield(instance, rho=F(1, 10), delta=F(1, 4), *, max_steps=1000000, seed=0,
                  allow_bounded_bias=False):
    """Whole count, or supported zero abort; raises before unaffordable work.

    A seeded PRNG is supplied for reproducibility. The confidence theorem
    assumes independent fair coin input, the usual randomized algorithm model.
    Tiny/coherent tapes do not get silently retried after an abort.
    """
    plan = nofield_plan(instance, rho, delta, allow_bounded_bias=allow_bounded_bias)
    if plan["n"] == 0:
        return {"estimate": F(plan["trivial_count"]), "plan": plan, "aborted": False,
                "coin_choices": 0, "coin_bits": 0, "executed_steps": 0}
    if plan["total_steps"] > max_steps:
        raise ResourceRefusal(plan)
    tape = CoinTape(seed, plan["bits_per_choice"], plan["choice_cap"])
    n, t, J = plan["n"], plan["t"], plan["steps_per_sample"]
    mu_in, mu_out, nu_in, nu_out = set(), set(), set(), set()
    witness = instance.seed()
    empirical_product = F(1)
    executed_steps = 0

    def sample(pins, start):
        nonlocal executed_steps
        chain = LocalExchange(instance, t=t, pins=pins, state=start)
        for _ in range(J):
            chain.step(tape)
            executed_steps += 1
        return frozenset(chain.S), frozenset(chain.T)

    try:
        M = plan["mass_samples_per_stage"]
        for side in (0, 1):
            for u in range(n):
                first = {}
                count_one = 0
                pins = tuple(map(frozenset, (mu_in, mu_out, nu_in, nu_out)))
                for _ in range(M):
                    state = sample(pins, witness)
                    bit = int(u in state[side])
                    count_one += bit
                    first.setdefault(bit, state)
                chosen_bit = int(2 * count_one >= M)
                frequency = count_one if chosen_bit else M - count_one
                assert frequency * 2 >= M and chosen_bit in first
                empirical_product *= F(frequency, M)
                witness = first[chosen_bit]
                included, excluded = (mu_in, mu_out) if side == 0 else (nu_in, nu_out)
                (included if chosen_bit else excluded).add(u)
        S, T = witness
        exact_weight = instance.mu(S) * instance.nu(T) * t ** len(S & T)
        assert exact_weight > 0 and len(mu_in) == instance.mu_degree and len(nu_in) == instance.nu_degree
        soft_estimate = exact_weight / empirical_product
        complement_count = 0
        start = instance.seed()
        empty_pins = tuple(frozenset() for _ in range(4))
        for _ in range(plan["complement_samples"]):
            S, T = sample(empty_pins, start)
            complement_count += int(S.isdisjoint(T))
        estimate = (soft_estimate * F(complement_count, plan["complement_samples"]) *
                    (1 << instance.inactive_qubits))
        return {"estimate": estimate, "plan": plan, "aborted": False,
                "coin_choices": tape.choices, "coin_bits": tape.bits,
                "executed_steps": executed_steps}
    except TapeAbort as error:
        return {"estimate": F(0), "plan": plan, "aborted": True,
                "abort_reason": str(error), "coin_choices": tape.choices,
                "coin_bits": tape.bits, "executed_steps": executed_steps}

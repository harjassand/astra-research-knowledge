"""Ordinary exact factory with a margin-sensitive finite expected bit cost.

Requires persistent classical X, a stationary iid cheap stream during the block,
and independent unbiased bits. Proxy records AND degree remain private: degree
independent of X does not give joint equivalence of (Y, degree) with an ideal
Y and an independent cost record.
"""
from fractions import Fraction as F
import random
import factory
from operation import exact_choice


def ceil_log2_fraction(value):
    value = F(value)
    if value <= 0:
        raise ValueError("positive value required")
    guess = value.numerator.bit_length() - value.denominator.bit_length()
    if guess >= 0:
        if value.numerator > (value.denominator << guess):
            guess += 1
    elif (value.numerator << (-guess)) > value.denominator:
        guess += 1
    return guess


def predraw_degree(rng):
    initial_continue = 2 * factory.radius(factory.START)
    if exact_choice([1 - initial_continue, initial_continue], rng) == 0:
        return factory.START
    degree = 4 * factory.START
    while rng.getrandbits(3) == 0:
        degree *= 4
    return degree


def compare_uniform_prefix(probability, prefix, bits, rng, stats):
    probability = F(probability)
    denominator = 1 << bits
    while True:
        lower = prefix * probability.denominator
        threshold = probability.numerator * denominator
        if lower >= threshold:
            return False
        if (prefix + 1) * probability.denominator <= threshold:
            return True
        prefix = (prefix << 1) | rng.getrandbits(1)
        denominator <<= 1
        bits += 1
        stats["uniform_bits"] += 1


def close_half_decision(exponent, exact_probability, rng, stats):
    """Use |q-1/2|<=2^-exponent, allocating no enormous tiny denominator."""
    if exponent < 2:
        stats["exact_elevations"] += 1
        probability = exact_probability()
        return exact_choice([probability, 1 - probability], rng) == 0
    first = rng.getrandbits(1)
    stats["uniform_bits"] += 1
    prefix, bits = first, 1
    for _ in range(1, exponent):
        bit = rng.getrandbits(1)
        stats["uniform_bits"] += 1
        if bit == first:
            stats["lazy_resolutions"] += 1
            return first == 0
        prefix = (prefix << 1) | bit
        bits += 1
    stats["exact_elevations"] += 1
    return compare_uniform_prefix(exact_probability(), prefix, bits, rng, stats)


def conditional_stop_probability(degree, total_heads):
    if degree == factory.START:
        lower, upper = factory.coefficient_envelope(degree, total_heads)
        return lower / (1 - (upper - lower))
    previous = degree // 4
    denominator = 2 * (factory.radius(previous) - factory.radius(degree))
    return F(1, 2) + (factory.center(degree, total_heads)
                       - factory.elevated_center(previous, degree, total_heads)) / denominator


def stop_coin(degree, total_heads, rng, stats):
    def exact_probability():
        value = conditional_stop_probability(degree, total_heads)
        if not 0 <= value <= 1:
            raise AssertionError("stop probability outside [0,1]")
        return value
    if degree == factory.START:
        probability = exact_probability()
        return exact_choice([probability, 1 - probability], rng) == 0
    previous = degree // 4
    empirical = F(total_heads, degree)
    if empirical <= F(1, 4):
        gap = F(1, 4) - empirical
    elif empirical >= F(7, 12):
        gap = empirical - F(7, 12)
    else:
        gap = F(0)
    if not gap:
        stats["exact_elevations"] += 1
        probability = exact_probability()
        return exact_choice([probability, 1 - probability], rng) == 0
    # One-sided hypergeometric Hoeffding and exp(-s)<=2^-floor(s).
    ratio = (F(11, 40) + F(297, 8) / (8 * previous)) / (
        2 * (factory.radius(previous) - factory.radius(degree)))
    power = 2 * previous * gap**2
    exponent = power.numerator // power.denominator - ceil_log2_fraction(ratio)
    stats["last_interval_exponent"] = exponent
    return close_half_decision(exponent, exact_probability, rng, stats)


def factory_coin(coin_callback, rng=None, *, degree_override=None, stats=None):
    """Predraw private terminal degree; draw that count; simulate its stop coin.

    degree_override is a path-testing hook, not an f(p) sampler by itself.
    """
    rng = rng or random.SystemRandom()
    if stats is None:
        stats = {}
    stats.update({"uniform_bits": 0, "exact_elevations": 0,
                  "lazy_resolutions": 0})
    degree = degree_override if degree_override is not None else predraw_degree(rng)
    level = degree // factory.START
    while level > 1 and level % 4 == 0:
        level //= 4
    if degree < factory.START or degree % factory.START or level != 1:
        raise ValueError("degree must be START times a power of four")
    total_heads = sum(bool(coin_callback()) for _ in range(degree))
    stats.update({"degree": degree, "heads": total_heads})
    return stop_coin(degree, total_heads, rng, stats)


def factory_output(proxy_callback, rng=None, *, degree_override=None, stats=None):
    def coin():
        z = proxy_callback()
        if z not in (0, 1, 2):
            raise ValueError("proxy record outside source alphabet")
        return z == 0
    rng = rng or random.SystemRandom()
    if factory_coin(coin, rng, degree_override=degree_override, stats=stats):
        return 0
    return 1 + exact_choice([F(1, 2), F(1, 2)], rng)

#!/usr/bin/env python3
"""Exact long-time iteration of a finite Abelian translation with sparse defects.

State space is G = product_i Z/moduli[i]. The default local operation adds
delta[i] modulo moduli[i]. A dictionary of exceptional states gives their
replacement one-step destinations. Event times are solved by congruences,
without enumerating the product state space or the default orbit.
"""

from math import gcd, lcm, prod
from random import Random
from time import perf_counter


def combine(r: int, m: int, c: int, n: int) -> tuple[int, int] | None:
    """Solve t = r (mod m), t = c (mod n), allowing noncoprime moduli."""
    g = gcd(m, n)
    if (c - r) % g:
        return None
    new_modulus = m * (n // g)
    reduced_n = n // g
    multiplier = 0 if reduced_n == 1 else (
        ((c - r) // g) * pow(m // g, -1, reduced_n)
    ) % reduced_n
    return (r + m * multiplier) % new_modulus, new_modulus


def hit_time(
    x: tuple[int, ...],
    e: tuple[int, ...],
    moduli: tuple[int, ...],
    delta: tuple[int, ...],
) -> int | None:
    """First t >= 0 with x + t delta = e, or None if no such t exists."""
    r, period = 0, 1
    for xi, ei, modulus, step in zip(x, e, moduli, delta, strict=True):
        diff = (ei - xi) % modulus
        g = gcd(step, modulus)
        if diff % g:
            return None
        reduced_modulus = modulus // g
        c = 0 if reduced_modulus == 1 else (
            (diff // g) * pow(step // g, -1, reduced_modulus)
        ) % reduced_modulus
        merged = combine(r, period, c, reduced_modulus)
        if merged is None:
            return None
        r, period = merged
    return r


def jump(
    moduli: tuple[int, ...],
    delta: tuple[int, ...],
    exceptions: dict[tuple[int, ...], tuple[int, ...]],
    start: tuple[int, ...],
    steps: int,
) -> tuple[int, ...]:
    if not moduli or len(moduli) != len(delta) or len(start) != len(moduli):
        raise ValueError("dimension mismatch")
    if any(modulus < 1 for modulus in moduli) or steps < 0:
        raise ValueError("invalid modulus or time")
    if any(not 0 <= coordinate < modulus
           for coordinate, modulus in zip(start, moduli)):
        raise ValueError("invalid initial state")
    for e, redirect in exceptions.items():
        if len(e) != len(moduli) or len(redirect) != len(moduli):
            raise ValueError("invalid exception dimension")
        if any(not 0 <= coordinate < modulus
               for state in (e, redirect)
               for coordinate, modulus in zip(state, moduli)):
            raise ValueError("invalid exception coordinate")

    def translate(x: tuple[int, ...], t: int) -> tuple[int, ...]:
        return tuple((xi + step * t) % modulus
                     for xi, step, modulus in zip(x, delta, moduli))

    sites = tuple(exceptions)

    def next_event(x: tuple[int, ...]) -> tuple[tuple[int, ...], int] | None:
        candidates = ((e, t) for e in sites
                      if (t := hit_time(x, e, moduli, delta)) is not None)
        return min(candidates, key=lambda pair: pair[1], default=None)

    first = next_event(start)
    if first is None or steps <= first[1]:
        return translate(start, steps)
    at, initial_distance = first
    steps -= initial_distance

    # One exceptional edge, then a default run until the next exception.
    edge = {}
    for e, redirect in exceptions.items():
        successor = next_event(redirect)
        edge[e] = None if successor is None else (successor[0], 1 + successor[1])

    seen: dict[tuple[int, ...], int] = {}
    vertices: list[tuple[int, ...]] = []
    prefix: list[int] = [0]
    terminal = False
    while at not in seen:
        seen[at] = len(vertices)
        vertices.append(at)
        next_edge = edge[at]
        if next_edge is None:
            remaining = steps - prefix[-1]
            if remaining == 0:
                return at
            if remaining > 0:
                return translate(exceptions[at], remaining - 1)
            terminal = True
            break
        at, weight = next_edge
        prefix.append(prefix[-1] + weight)

    if not terminal:
        cycle_start = seen[at]
        duration = prefix[-1] - prefix[cycle_start]
        if steps >= prefix[cycle_start]:
            steps = prefix[cycle_start] + (steps - prefix[cycle_start]) % duration

    # At most k event edges remain after the cycle reduction.
    for j, e in enumerate(vertices):
        if steps == prefix[j]:
            return e
        if j + 1 < len(prefix) and steps < prefix[j + 1]:
            return translate(exceptions[e], steps - prefix[j] - 1)
    raise AssertionError("unreachable event phase")


def direct(moduli, delta, exceptions, start, steps):
    x = start
    for _ in range(steps):
        x = exceptions.get(x, tuple((xi + d) % m
                                    for xi, d, m in zip(x, delta, moduli)))
    return x


def self_test() -> None:
    rng = Random(0xBEEFBABE)
    cases = 0
    terminal_example = {(0, 0): (1, 1), (1, 1): (0, 1)}
    for steps in range(30):
        assert jump((4, 4), (1, 1), terminal_example, (0, 0), steps) == direct(
            (4, 4), (1, 1), terminal_example, (0, 0), steps
        )
        cases += 1
    for _ in range(3000):
        dimension = rng.randrange(1, 5)
        moduli = tuple(rng.randrange(2, 8) for _ in range(dimension))
        delta = tuple(rng.randrange(m) for m in moduli)
        state = lambda: tuple(rng.randrange(m) for m in moduli)
        exceptions = {state(): state() for _ in range(rng.randrange(5))}
        start = state()
        steps = rng.randrange(220)
        got = jump(moduli, delta, exceptions, start, steps)
        want = direct(moduli, delta, exceptions, start, steps)
        assert got == want, (moduli, delta, exceptions, start, steps, got, want)
        cases += 1

    # A product of pairwise coprime local counters is one cycle of length
    # their product. Two swapped successor edges break that cycle into two.
    primes = (1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049,
              1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097,
              1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163,
              1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223)
    assert len(primes) == len(set(primes))
    assert all(gcd(p, q) == 1 for i, p in enumerate(primes) for q in primes[i+1:])
    moduli = primes
    delta = (1,) * len(moduli)
    orbit_length = prod(moduli)
    assert orbit_length == lcm(*moduli)
    a = orbit_length // 3
    zero = (0,) * len(moduli)
    site_a = tuple(a % m for m in moduli)
    exceptions = {zero: tuple((a + 1) % m for m in moduli),
                  site_a: tuple(1 % m for m in moduli)}
    steps = (1 << 4096) + 3141592653
    tic = perf_counter()
    got = jump(moduli, delta, exceptions, zero, steps)
    seconds = perf_counter() - tic
    remainder = steps % (orbit_length - a)
    phase = 0 if remainder == 0 else a + remainder
    want = tuple(phase % m for m in moduli)
    assert got == want

    print(f"random_small_cases={cases}")
    print(f"local_counters={len(moduli)}")
    print(f"implicit_state_count_bits={orbit_length.bit_length()}")
    print(f"huge_time_bits={steps.bit_length()}")
    print(f"huge_answer={got}")
    print(f"huge_seconds={seconds:.6f}")


if __name__ == "__main__":
    self_test()

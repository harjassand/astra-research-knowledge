#!/usr/bin/env python3
"""Exact iteration of a cyclic successor with a finite list of changed edges.

The input is M, an exception dictionary e -> F(e), a start x, and a time T.
Only integer arithmetic on O(log M) and O(log T) bit operands is used.
"""

from bisect import bisect_left, bisect_right
from random import Random
from time import perf_counter


def jump(modulus: int, exceptions: dict[int, int], start: int, steps: int) -> int:
    if modulus < 1 or not 0 <= start < modulus or steps < 0:
        raise ValueError("invalid modulus, start, or steps")
    if any(not 0 <= e < modulus or not 0 <= r < modulus
           for e, r in exceptions.items()):
        raise ValueError("exception outside the state space")
    if not exceptions:
        return (start + steps) % modulus

    sites = sorted(exceptions)
    k = len(sites)

    def next_event(x: int) -> tuple[int, int]:
        i = bisect_left(sites, x)
        if i == k:
            return sites[0], sites[0] + modulus - x
        return sites[i], sites[i] - x

    first, initial_distance = next_event(start)
    if steps <= initial_distance:
        return (start + steps) % modulus
    steps -= initial_distance

    # From an exception: one exceptional edge, then successor edges to the
    # next exception. The edge duration includes that first exceptional step.
    edge: dict[int, tuple[int, int]] = {}
    for e, r in exceptions.items():
        successor, distance = next_event(r)
        edge[e] = (successor, 1 + distance)

    seen: dict[int, int] = {}
    vertices: list[int] = []
    prefix: list[int] = [0]
    v = first
    while v not in seen:
        seen[v] = len(vertices)
        vertices.append(v)
        successor, duration = edge[v]
        prefix.append(prefix[-1] + duration)
        v = successor

    cycle_start = seen[v]
    cycle_duration = prefix[-1] - prefix[cycle_start]
    if steps >= prefix[cycle_start]:
        steps = prefix[cycle_start] + (
            (steps - prefix[cycle_start]) % cycle_duration
        )

    j = bisect_right(prefix, steps) - 1
    at = vertices[j]
    remainder = steps - prefix[j]
    if remainder == 0:
        return at
    return (exceptions[at] + remainder - 1) % modulus


def direct(modulus: int, exceptions: dict[int, int], start: int, steps: int) -> int:
    x = start
    for _ in range(steps):
        x = exceptions.get(x, (x + 1) % modulus)
    return x


def self_test() -> None:
    rng = Random(0xC0DE)
    cases = 0
    for modulus in range(1, 65):
        for _ in range(24):
            k = rng.randrange(min(7, modulus) + 1)
            exceptions = {e: rng.randrange(modulus)
                          for e in rng.sample(range(modulus), k)}
            for _ in range(8):
                x = rng.randrange(modulus)
                steps = rng.randrange(4 * modulus + 1)
                got = jump(modulus, exceptions, x, steps)
                want = direct(modulus, exceptions, x, steps)
                assert got == want, (modulus, exceptions, x, steps, got, want)
                cases += 1

    n = 256
    modulus = 1 << n
    a = modulus // 3
    # Swap the successor edges of 0 and a. This gives a long cycle of
    # length M-a containing 0, with explicit closed-form verification.
    exceptions = {0: a + 1, a: 1}
    steps = (1 << 4096) + 11235813
    tic = perf_counter()
    got = jump(modulus, exceptions, 0, steps)
    seconds = perf_counter() - tic
    remainder = steps % (modulus - a)
    want = 0 if remainder == 0 else a + remainder
    assert got == want

    print(f"random_small_cases={cases}")
    print(f"huge_modulus_bits={modulus.bit_length() - 1}")
    print(f"huge_time_bits={steps.bit_length()}")
    print(f"cycle_length_bits={(modulus - a).bit_length()}")
    print(f"huge_answer_hex={got:x}")
    print(f"huge_seconds={seconds:.6f}")


if __name__ == "__main__":
    self_test()

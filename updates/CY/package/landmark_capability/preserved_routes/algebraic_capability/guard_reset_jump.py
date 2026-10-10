#!/usr/bin/env python3
"""Exact fast forwarding of local modular counters with prioritized guard resets.

Each guard fixes selected counter coordinates. On a matching state, the first
matching rule resets the entire state to its rule-specific constant; otherwise
one step adds the specified local increments. All arithmetic is exact.
"""

from math import gcd, prod
from random import Random
from time import perf_counter


def crt_merge(r: int, m: int, c: int, n: int) -> tuple[int, int] | None:
    g = gcd(m, n)
    if (c - r) % g:
        return None
    quotient = n // g
    multiplier = 0 if quotient == 1 else (
        ((c - r) // g) * pow(m // g, -1, quotient)
    ) % quotient
    modulus = m * quotient
    return (r + m * multiplier) % modulus, modulus


def guard_hit_time(
    x: tuple[int, ...],
    guard: dict[int, int],
    moduli: tuple[int, ...],
    increments: tuple[int, ...],
) -> int | None:
    r, period = 0, 1
    for j, target in sorted(guard.items()):
        modulus = moduli[j]
        increment = increments[j]
        diff = (target - x[j]) % modulus
        common = gcd(increment, modulus)
        if diff % common:
            return None
        reduced_modulus = modulus // common
        residue = 0 if reduced_modulus == 1 else (
            (diff // common) * pow(increment // common, -1, reduced_modulus)
        ) % reduced_modulus
        result = crt_merge(r, period, residue, reduced_modulus)
        if result is None:
            return None
        r, period = result
    return r


def jump(
    moduli: tuple[int, ...],
    increments: tuple[int, ...],
    rules: tuple[tuple[dict[int, int], tuple[int, ...]], ...],
    start: tuple[int, ...],
    steps: int,
) -> tuple[int, ...]:
    d = len(moduli)
    if d == 0 or len(increments) != d or len(start) != d or steps < 0:
        raise ValueError("invalid dimension or time")
    if any(m < 1 for m in moduli):
        raise ValueError("moduli must be positive")

    def validate_state(x: tuple[int, ...]) -> None:
        if len(x) != d or any(not 0 <= xi < m for xi, m in zip(x, moduli)):
            raise ValueError("state coordinate out of range")

    validate_state(start)
    for guard, reset in rules:
        validate_state(reset)
        if any(not 0 <= j < d or not 0 <= target < moduli[j]
               for j, target in guard.items()):
            raise ValueError("guard coordinate out of range")

    def advance(x: tuple[int, ...], t: int) -> tuple[int, ...]:
        return tuple((xi + t * increment) % modulus for xi, increment, modulus
                     in zip(x, increments, moduli))

    def next_rule(x: tuple[int, ...]) -> tuple[int, int] | None:
        candidates = ((i, t) for i, (guard, _) in enumerate(rules)
                      if (t := guard_hit_time(x, guard, moduli, increments))
                      is not None)
        # Priority is rule index, after first-hit time.
        return min(candidates, key=lambda pair: (pair[1], pair[0]), default=None)

    first = next_rule(start)
    if first is None or steps <= first[1]:
        return advance(start, steps)

    initial_rule, initial_wait = first
    steps -= initial_wait + 1
    node = initial_rule  # State is now exactly reset[node].
    if steps == 0:
        return rules[node][1]

    # A graph on rule indices. Each edge is a default run ending with one reset.
    edges = []
    for _, reset in rules:
        next_hit = next_rule(reset)
        edges.append(None if next_hit is None else (next_hit[0], next_hit[1] + 1))

    seen: dict[int, int] = {}
    vertices: list[int] = []
    prefix: list[int] = [0]
    terminal = False
    while node not in seen:
        seen[node] = len(vertices)
        vertices.append(node)
        next_edge = edges[node]
        if next_edge is None:
            terminal = True
            break
        node, weight = next_edge
        prefix.append(prefix[-1] + weight)

    if not terminal:
        cycle_start = seen[node]
        cycle_duration = prefix[-1] - prefix[cycle_start]
        if steps >= prefix[cycle_start]:
            steps = prefix[cycle_start] + (
                (steps - prefix[cycle_start]) % cycle_duration
            )

    for j, i in enumerate(vertices):
        if steps == prefix[j]:
            return rules[i][1]
        if terminal and j == len(vertices) - 1:
            return advance(rules[i][1], steps - prefix[j])
        if steps < prefix[j + 1]:
            return advance(rules[i][1], steps - prefix[j])
    raise AssertionError("unreachable rule phase")


def direct(moduli, increments, rules, start, steps):
    x = start
    for _ in range(steps):
        for guard, reset in rules:
            if all(x[j] == target for j, target in guard.items()):
                x = reset
                break
        else:
            x = tuple((xi + inc) % m for xi, inc, m
                      in zip(x, increments, moduli))
    return x


def self_test() -> None:
    rng = Random(0x1234ABC)
    cases = 0
    for _ in range(5000):
        dimension = rng.randrange(1, 5)
        moduli = tuple(rng.randrange(2, 8) for _ in range(dimension))
        increments = tuple(rng.randrange(m) for m in moduli)
        state = lambda: tuple(rng.randrange(m) for m in moduli)
        rules = []
        for _ in range(rng.randrange(5)):
            indices = rng.sample(range(dimension), rng.randrange(dimension + 1))
            guard = {j: rng.randrange(moduli[j]) for j in indices}
            rules.append((guard, state()))
        start = state()
        steps = rng.randrange(180)
        got = jump(moduli, increments, tuple(rules), start, steps)
        want = direct(moduli, increments, tuple(rules), start, steps)
        assert got == want, (moduli, increments, rules, start, steps, got, want)
        cases += 1

    primes = (1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049,
              1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097,
              1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163,
              1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223)
    assert all(gcd(p, q) == 1 for i, p in enumerate(primes) for q in primes[i+1:])
    moduli = primes
    increments = (1,) * len(moduli)
    zero = (0,) * len(moduli)
    guard = {j: j + 1 for j in range(16)}
    rules = ((guard, zero),)
    wait = guard_hit_time(zero, guard, moduli, increments)
    assert wait is not None and wait > 0
    steps = (1 << 4096) + 2718281828
    tic = perf_counter()
    got = jump(moduli, increments, rules, zero, steps)
    seconds = perf_counter() - tic
    phase = steps % (wait + 1)
    want = tuple(phase % m for m in moduli)
    assert got == want

    # Independent closed-form check of a two-rule event cycle. Starting at
    # zero, guard B fires at t=5 and resets at t=6. From reset B, A fires
    # after 10 default steps (weight 11); from reset A, B fires after 5
    # default steps (weight 6). The post-reset cycle has weight 17.
    reset_a = (11, 0) + (0,) * 30
    reset_b = (0, 6) + (0,) * 30
    two_rules = (({0: 10}, reset_a), ({1: 5}, reset_b))
    two_steps = (1 << 4096) + 1618033988
    got_two = jump(moduli, increments, two_rules, zero, two_steps)
    two_phase = (two_steps - 6) % 17
    if two_phase <= 10:
        want_two = tuple((r + two_phase) % m for r, m in zip(reset_b, moduli))
    else:
        want_two = tuple((r + two_phase - 11) % m
                         for r, m in zip(reset_a, moduli))
    assert got_two == want_two

    print(f"random_small_cases={cases}")
    print(f"local_counters={len(moduli)}")
    print(f"implicit_state_count_bits={prod(moduli).bit_length()}")
    print(f"guard_set_size_bits={prod(moduli[16:]).bit_length()}")
    print(f"first_guard_hit_bits={wait.bit_length()}")
    print(f"huge_time_bits={steps.bit_length()}")
    print(f"huge_answer={got}")
    print(f"huge_seconds={seconds:.6f}")
    print(f"two_rule_huge_answer={got_two}")


if __name__ == "__main__":
    self_test()

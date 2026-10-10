#!/usr/bin/env python3
"""Exact jump compiler for guarded counters with a retained affine payload.

The control state is a product of modular counters. Guards inspect control
coordinates only; a fired rule resets control to a constant but applies an
affine map to a retained payload. Ordinary steps translate both control and
payload. This is a skew-product system: the event schedule is independent of
the payload, while the payload keeps information through all event cycles.
"""

from math import gcd, prod
from random import Random
from time import perf_counter

from guard_reset_jump import guard_hit_time


def compose(f: tuple[int, int], g: tuple[int, int], modulus: int) -> tuple[int, int]:
    """Affine map f after affine map g."""
    fa, fb = f
    ga, gb = g
    return (fa * ga) % modulus, (fa * gb + fb) % modulus


def affine_power(a: int, b: int, power: int, modulus: int) -> tuple[int, int]:
    result = (1 % modulus, 0)
    base = (a % modulus, b % modulus)
    while power:
        if power & 1:
            result = compose(base, result, modulus)
        base = compose(base, base, modulus)
        power >>= 1
    return result


def jump(
    moduli: tuple[int, ...],
    increments: tuple[int, ...],
    rules: tuple[tuple[dict[int, int], tuple[int, ...], int, int], ...],
    active_start: tuple[int, ...],
    payload_start: int,
    payload_modulus: int,
    payload_increment: int,
    steps: int,
) -> tuple[tuple[int, ...], int]:
    d = len(moduli)
    if d == 0 or len(increments) != d or len(active_start) != d or steps < 0:
        raise ValueError("invalid dimension or time")
    if payload_modulus < 1 or any(m < 1 for m in moduli):
        raise ValueError("moduli must be positive")
    if not 0 <= payload_start < payload_modulus:
        raise ValueError("invalid payload")

    def valid_active(x: tuple[int, ...]) -> bool:
        return len(x) == d and all(0 <= xi < m for xi, m in zip(x, moduli))

    if not valid_active(active_start):
        raise ValueError("invalid initial control state")
    for guard, reset, _, _ in rules:
        if not valid_active(reset) or any(
            not 0 <= j < d or not 0 <= value < moduli[j]
            for j, value in guard.items()
        ):
            raise ValueError("invalid guard or reset")

    def translate(x: tuple[int, ...], t: int) -> tuple[int, ...]:
        return tuple((xi + t * inc) % m for xi, inc, m
                     in zip(x, increments, moduli))

    def next_rule(x: tuple[int, ...]) -> tuple[int, int] | None:
        candidates = ((i, t) for i, (guard, _, _, _) in enumerate(rules)
                      if (t := guard_hit_time(x, guard, moduli, increments))
                      is not None)
        return min(candidates, key=lambda pair: (pair[1], pair[0]), default=None)

    first = next_rule(active_start)
    if first is None or steps <= first[1]:
        return translate(active_start, steps), (
            payload_start + steps * payload_increment
        ) % payload_modulus

    rule_index, first_wait = first
    _, reset, a, b = rules[rule_index]
    payload = (a * (payload_start + first_wait * payload_increment) + b) % payload_modulus
    steps -= first_wait + 1
    if steps == 0:
        return reset, payload

    # Each edge starts just after a reset and ends just after the next one.
    # Its payload action is the next rule's affine map after ordinary steps.
    edges: list[tuple[int, int, tuple[int, int]] | None] = []
    for _, source_reset, _, _ in rules:
        hit = next_rule(source_reset)
        if hit is None:
            edges.append(None)
        else:
            target, wait = hit
            _, _, target_a, target_b = rules[target]
            edges.append((target, wait + 1, (
                target_a % payload_modulus,
                (target_a * wait * payload_increment + target_b) % payload_modulus,
            )))

    path: list[int] = []
    seen: dict[int, int] = {}
    node = rule_index
    terminal = False
    while node not in seen:
        seen[node] = len(path)
        path.append(node)
        edge = edges[node]
        if edge is None:
            terminal = True
            break
        node = edge[0]

    def partial(i: int, p: int, t: int) -> tuple[tuple[int, ...], int]:
        return translate(rules[i][1], t), (p + t * payload_increment) % payload_modulus

    def traverse(indices: list[int], p: int, t: int):
        for i in indices:
            edge = edges[i]
            if edge is None:
                return partial(i, p, t), p, t
            target, weight, transform = edge
            if t < weight:
                return partial(i, p, t), p, t
            p = (transform[0] * p + transform[1]) % payload_modulus
            t -= weight
        return None, p, t

    if terminal:
        answer, _, _ = traverse(path, payload, steps)
        assert answer is not None
        return answer

    cycle_start = seen[node]
    answer, payload, steps = traverse(path[:cycle_start], payload, steps)
    if answer is not None:
        return answer

    cycle = path[cycle_start:]
    cycle_duration = sum(edges[i][1] for i in cycle)  # type: ignore[index]
    full_cycles, steps = divmod(steps, cycle_duration)
    macro = (1 % payload_modulus, 0)
    for i in cycle:
        macro = compose(edges[i][2], macro, payload_modulus)  # type: ignore[index]
    powered = affine_power(*macro, full_cycles, payload_modulus)
    payload = (powered[0] * payload + powered[1]) % payload_modulus
    answer, _, _ = traverse(cycle, payload, steps)
    assert answer is not None
    return answer


def direct(moduli, increments, rules, x, p, pmod, pinc, steps):
    for _ in range(steps):
        for guard, reset, a, b in rules:
            if all(x[j] == value for j, value in guard.items()):
                x, p = reset, (a * p + b) % pmod
                break
        else:
            x = tuple((xi + inc) % m for xi, inc, m
                      in zip(x, increments, moduli))
            p = (p + pinc) % pmod
    return x, p


def self_test() -> None:
    rng = Random(0xFEEDCAFE)
    for case in range(5000):
        dimension = rng.randrange(1, 5)
        moduli = tuple(rng.randrange(2, 8) for _ in range(dimension))
        increments = tuple(rng.randrange(m) for m in moduli)
        state = lambda: tuple(rng.randrange(m) for m in moduli)
        rules = []
        for _ in range(rng.randrange(5)):
            indices = rng.sample(range(dimension), rng.randrange(dimension + 1))
            guard = {j: rng.randrange(moduli[j]) for j in indices}
            rules.append((guard, state(), rng.randrange(21), rng.randrange(21)))
        x = state()
        pmod = rng.randrange(2, 51)
        p = rng.randrange(pmod)
        pinc = rng.randrange(21)
        steps = rng.randrange(180)
        got = jump(moduli, increments, tuple(rules), x, p, pmod, pinc, steps)
        want = direct(moduli, increments, tuple(rules), x, p, pmod, pinc, steps)
        assert got == want, (case, moduli, increments, rules, x, p,
                             pmod, pinc, steps, got, want)

    primes = (1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049,
              1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097,
              1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163,
              1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223)
    assert all(gcd(p, q) == 1 for i, p in enumerate(primes) for q in primes[i+1:])
    moduli = primes
    increments = (1,) * len(moduli)
    zero = (0,) * len(moduli)
    guard = {j: j + 1 for j in range(16)}
    wait = guard_hit_time(zero, guard, moduli, increments)
    assert wait is not None and wait > 0
    pmod = (1 << 521) - 1
    p0, pinc, a, b = 123456789, 7, 3, 11
    rules = ((guard, zero, a, b),)
    steps = (1 << 4096) + 2718281828
    tic = perf_counter()
    got_x, got_p = jump(moduli, increments, rules, zero, p0, pmod, pinc, steps)
    seconds = perf_counter() - tic

    # Closed-form scalar check, independent of the affine-composition routine.
    cycle_length = wait + 1
    cycles, phase = divmod(steps, cycle_length)
    macro_b = a * wait * pinc + b
    a_power = pow(a, cycles, pmod)
    p_cycles = (a_power * p0 + macro_b * (a_power - 1) * pow(a - 1, -1, pmod)) % pmod
    expected_p = (p_cycles + phase * pinc) % pmod
    expected_x = tuple(phase % m for m in moduli)
    assert (got_x, got_p) == (expected_x, expected_p)

    # Two distinct, noncommuting affine rules in a 17-step event cycle.
    reset_a = (11, 0) + (0,) * 30
    reset_b = (0, 6) + (0,) * 30
    two_rules = (({0: 10}, reset_a, 2, 3),
                 ({1: 5}, reset_b, 5, 11))
    two_steps = (1 << 4096) + 1618033988
    got_two_x, got_two_p = jump(
        moduli, increments, two_rules, zero, p0, pmod, pinc, two_steps
    )
    cycles, phase = divmod(two_steps - 6, 17)
    initial_after_b = (5 * (p0 + 5 * pinc) + 11) % pmod
    cycle_b = 125 * pinc + 26
    ten_power = pow(10, cycles, pmod)
    post_b = (ten_power * initial_after_b
              + cycle_b * (ten_power - 1) * pow(9, -1, pmod)) % pmod
    if phase <= 10:
        expected_two_x = tuple((r + phase) % m for r, m in zip(reset_b, moduli))
        expected_two_p = (post_b + phase * pinc) % pmod
    else:
        expected_two_x = tuple((r + phase - 11) % m
                               for r, m in zip(reset_a, moduli))
        after_a = (2 * (post_b + 10 * pinc) + 3) % pmod
        expected_two_p = (after_a + (phase - 11) * pinc) % pmod
    assert (got_two_x, got_two_p) == (expected_two_x, expected_two_p)

    print("random_small_cases=5000")
    print(f"active_state_count_bits={prod(moduli).bit_length()}")
    print(f"guard_set_size_bits={prod(moduli[16:]).bit_length()}")
    print(f"first_guard_hit_bits={wait.bit_length()}")
    print(f"payload_modulus_bits={pmod.bit_length()}")
    print(f"huge_time_bits={steps.bit_length()}")
    print(f"huge_payload_hex={got_p:x}")
    print(f"huge_seconds={seconds:.6f}")
    print(f"two_rule_huge_payload_hex={got_two_p:x}")


if __name__ == "__main__":
    self_test()

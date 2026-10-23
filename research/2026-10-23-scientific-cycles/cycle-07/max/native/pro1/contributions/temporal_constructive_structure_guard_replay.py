#!/usr/bin/env python3
"""Exact symbolic replay of the guard/meander word identity.

Standalone, standard library only. Distinct color-wire symbols expose the
entire permutation, including the bath, without replacing it by a finite
reflecting chain. Vacuum calls use the actual seed exchange.
This bounded replay is evidence for, not the proof of, the all-length theorem.
"""
from itertools import product, combinations
from fractions import Fraction
from math import comb
from pathlib import Path
import argparse
import json
import platform
import resource
import time


def call(ports, bath, seed, j):
    if ports[j] is not None:
        bath.insert(0, ports[j])
        ports[j] = None
    elif bath:
        ports[j] = bath.pop(0)
    else:
        seed ^= 1
    return seed


def toggle(ports, bath, seed, j):
    for a in range(j):
        seed = call(ports, bath, seed, a)
    seed = call(ports, bath, seed, j)
    for a in reversed(range(j)):
        seed = call(ports, bath, seed, a)
    return seed


def run_order(bits, i, j, order, bath_depth, seed=0):
    ports = [f"I{a}" if bit else None for a, bit in enumerate(bits)]
    bath = [f"B{a}" for a in range(bath_depth)]
    for a in order:
        seed = toggle(ports, bath, seed, a)
    return ports, bath, seed


def meander(bits):
    depth = 0
    for bit in bits:
        depth += 1 if bit else -1
        if depth < 0:
            return False
    return True


def unmatched_positions(bits, i, j):
    stack = []
    for a in range(i + 1, j):
        if bits[a]:
            stack.append(a)
        else:
            assert stack
            stack.pop()
    return stack


def expected_orders(bits, i, j):
    ports = [f"I{a}" if bit else None for a, bit in enumerate(bits)]
    guard = i - 1
    positions = unmatched_positions(bits, i, j) + [j]
    forward = ports.copy()
    forward[i] = ports[positions[0]]
    for a, b in zip(positions, positions[1:]):
        forward[a] = ports[b]
    forward[j] = None
    reverse = forward.copy()
    reverse[guard], reverse[i] = reverse[i], reverse[guard]
    return forward, reverse


def witness(bits, i, j):
    depth = 3 * len(bits)
    a = run_order(bits, i, j, [i, j], depth)
    b = run_order(bits, i, j, [j, i], depth)
    initial_bath = [f"B{r}" for r in range(depth)]
    return {
        "bits": list(bits),
        "i": i,
        "j": j,
        "guard_present": i > 0 and bool(bits[i - 1]),
        "middle_meander": meander(bits[i + 1:j]),
        "middle_net": sum(1 if x else -1 for x in bits[i + 1:j]),
        "initial_ports": [f"I{a}" if bit else None for a, bit in enumerate(bits)],
        "initial_bath": initial_bath,
        "Cj_Ci": {"ports": a[0], "bath": a[1], "seed": a[2]},
        "Ci_Cj": {"ports": b[0], "bath": b[1], "seed": b[2]},
        "first_bath_unchanged": a[1] == initial_bath,
        "second_bath_unchanged": b[1] == initial_bath,
    }


def run(max_k=8):
    started = time.perf_counter()
    by_k = []
    for k in range(3, max_k + 1):
        patterns = 0
        configurations = 0
        for bits in product((0, 1), repeat=k):
            for i, j in combinations(range(1, k), 2):
                if not (bits[i - 1] == 1 and bits[i] == 0 and bits[j] == 1):
                    continue
                if not meander(bits[i + 1:j]):
                    continue
                expected_a, expected_b = expected_orders(bits, i, j)
                for depth, seed in ((0, 0), (0, 1), (3 * k, 0), (3 * k, 1)):
                    a = run_order(bits, i, j, [i, j], depth, seed)
                    b = run_order(bits, i, j, [j, i], depth, seed)
                    bath = [f"B{r}" for r in range(depth)]
                    assert a == (expected_a, bath, seed), (bits, i, j, a)
                    assert b == (expected_b, bath, seed), (bits, i, j, b)
                    configurations += 1
                patterns += 1
        # Every full bit pattern has mass 2^-k, and the adjoint doubles.
        lower = Fraction(2 * patterns, 2 ** k)
        analytic = sum(
            Fraction((k - r - 2) * comb(r, r // 2), 4 * 2 ** r)
            for r in range(k - 2)
        )
        assert lower == analytic
        if k >= 4:
            # The weaker rational squared comparison avoids float rounding.
            assert lower * lower * 1024 >= k ** 3
        by_k.append({
            "k": k,
            "guard_meander_pattern_pair_count": patterns,
            "exact_symbolic_configurations": configurations,
            "all_whole_bath_identities": True,
            "all_predicted_transpositions": True,
            "lower_v": str(lower),
        })

    missing_guard = witness((0, 1, 1), 0, 2)
    assert missing_guard["middle_meander"]
    assert not missing_guard["guard_present"]
    assert not (
        missing_guard["first_bath_unchanged"]
        and missing_guard["second_bath_unchanged"]
    )
    missing_meander = witness((1, 0, 0, 1, 1, 1), 1, 5)
    assert missing_meander["guard_present"]
    assert missing_meander["middle_net"] > 0
    assert not missing_meander["middle_meander"]
    assert not (
        missing_meander["first_bath_unchanged"]
        and missing_meander["second_bath_unchanged"]
    )
    return {
        "scope": "Bounded exact token replay; all-length proof is in temporal_constructive_structure.md",
        "actual_root_rule": "Zero port at empty bath exchanges the seed",
        "max_k": max_k,
        "by_k": by_k,
        "omitted_guard_counterexample": missing_guard,
        "omitted_meander_counterexample": missing_meander,
        "wall_seconds": time.perf_counter() - started,
        "max_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "python": platform.python_version(),
        "discovery_and_review_cost": "Unknown; replay time is not discovery cost",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=8)
    parser.add_argument("--output", default=str(Path(__file__).with_suffix(".json")))
    args = parser.parse_args()
    result = run(args.max_k)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        k: v for k, v in result.items()
        if k not in ("omitted_guard_counterexample", "omitted_meander_counterexample")
    }, indent=2))

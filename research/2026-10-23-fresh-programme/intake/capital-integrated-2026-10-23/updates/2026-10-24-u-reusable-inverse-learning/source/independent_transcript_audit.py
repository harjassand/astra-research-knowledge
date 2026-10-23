"""Independent exact evaluator of the finite replay's observation interface.

This audit deliberately enumerates all 256 forward responses and charges that
as evaluator work. It is NOT imported by any learner and its table is never
passed to one. No benchmark code, private seed, or saved response table is read.
The independent arithmetic checks containment and the actual acceptance tape.
"""

from fractions import Fraction as F
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent
DATA = HERE / "luna_batched_mean"
DEPTH, STEPS, COUNT = 4, 6, 8
EPS = F(1, 8)


def rational(encoded):
    return F(int(encoded[0]), int(encoded[1]))


def point_value(i, j):
    a = F(97 + 2 * i, 32)
    u = F(19 + 6 * j, 128)
    for _ in range(STEPS):
        u = a * u * (1 - u)
    return u


def likelihood(value, s):
    p = EPS + (1 - 2 * EPS) * value
    return p ** s * (1 - p) ** (COUNT - s)


def expected_likelihood_bounds(interval, s):
    low, high = interval
    p0 = EPS + (1 - 2 * EPS) * low
    p1 = EPS + (1 - 2 * EPS) * high
    endpoints = [likelihood(low, s), likelihood(high, s)]
    upper = max(endpoints)
    if p0 <= F(s, COUNT) <= p1:
        p = F(s, COUNT)
        upper = max(upper, p ** s * (1 - p) ** (COUNT - s))
    return min(endpoints), upper


def bit_prefix(tape, start, length):
    bitstr = tape[start:start + length]
    assert len(bitstr) == length
    return int(bitstr or "0", 2), 1 << length


def verify_comparison(tape, origin, comparison):
    threshold = rational(comparison["threshold"])
    prefix, denominator = bit_prefix(tape, origin, comparison["bits_after"])
    if comparison["result_uniform_lt"]:
        assert F(prefix + 1, denominator) <= threshold
    else:
        assert F(prefix, denominator) >= threshold


def verify_category(tape, info, selected, masses):
    total = sum(masses, F(0))
    lower = sum(masses[:selected], F(0)) / total
    upper = sum(masses[:selected + 1], F(0)) / total
    prefix, denominator = bit_prefix(tape, info["start"], info["end"] - info["start"])
    assert lower <= F(prefix, denominator) < F(prefix + 1, denominator) <= upper


def audit_method(name, values):
    raw = json.loads((DATA / f"{name.upper()}_PUBLIC_TRANSCRIPT.json").read_text())
    tape = raw["bit_tape"]
    nodes = {}
    node_masses = {}
    active = set()
    bounds = {}
    pending = None
    total = {
        "nodes_checked": 0, "pointwise_containments": 0,
        "paid_point_values_checked": 0, "likelihood_intervals_checked": 0,
        "pinned_final_decisions_checked": 0, "exact_tape_comparisons_checked": 0,
        "posterior_outputs_checked": 0,
        "exact_proposal_categories_checked": 0,
    }
    for event in raw["events"]:
        kind = event["kind"]
        if kind == "node_created":
            key = tuple(event["node"])
            interval = tuple(map(rational, event["parent_intersected"]))
            raw_range = tuple(map(rational, event["raw"]))
            assert 0 <= interval[0] <= interval[1] <= 1
            assert raw_range[0] <= interval[0] <= interval[1] <= raw_range[1]
            if event["parent"] is not None:
                parent = nodes[tuple(event["parent"])]
                assert parent[0] <= interval[0] <= interval[1] <= parent[1]
            i0, i1 = event["grid_rows"]
            j0, j1 = event["grid_cols"]
            for i in range(i0, i1):
                for j in range(j0, j1):
                    assert interval[0] <= values[i, j] <= interval[1]
                    total["pointwise_containments"] += 1
            if key[0] == DEPTH:
                assert interval[0] == interval[1] == values[i0, j0]
            nodes[key] = interval
            node_masses[key] = F((i1 - i0) * (j1 - j0), 256)
            if event["parent"] is None:
                active.add(key)
            total["nodes_checked"] += 1
        elif kind == "split":
            active.remove(tuple(event["parent"]))
            active.update(tuple(key) for key in event["children"])
        elif kind == "point_evaluation":
            i, j = event["point"]
            assert rational(event["value"]) == values[i, j]
            total["paid_point_values_checked"] += 1
        elif kind == "likelihood_bound":
            key, s = tuple(event["node"]), event["s"]
            expected = expected_likelihood_bounds(nodes[key], s)
            got = rational(event["lower"]), rational(event["upper"])
            assert expected == got
            bounds[key, s] = got
            total["likelihood_intervals_checked"] += 1
        elif kind == "proposal":
            assert name == "lead"
            assert pending is None
            key, s = tuple(event["cell"]), event["s"]
            old = rational(event["pinned_u_old"])
            assert old == bounds[key, s][1]
            origin = event["point_draw"]["end"]
            pending = {"old": old, "point": tuple(event["point"]),
                       "origin": origin, "s": s}
            keys = sorted(active, key=lambda node: (node[1], node[2], node[0]))
            masses = [node_masses[node] * bounds[node, s][1] for node in keys]
            idx = keys.index(key)
            assert idx == event["proposal_cdf"]["selected_index"]
            verify_category(tape, event["proposal_cdf"], idx, masses)
            total["exact_proposal_categories_checked"] += 1
            for comparison in event["proposal_cdf"]["comparisons"]:
                verify_comparison(tape, event["proposal_cdf"]["start"], comparison)
                total["exact_tape_comparisons_checked"] += 1
        elif kind in ("threshold_refine", "threshold_decision"):
            assert pending is not None
            for comparison in event["comparisons"]:
                verify_comparison(tape, pending["origin"], comparison)
                total["exact_tape_comparisons_checked"] += 1
            if kind == "threshold_refine":
                continue
            assert rational(event["pinned_u_old"]) == pending["old"]
            lo = rational(event["lower_ratio"])
            hi = rational(event["upper_ratio"])
            i, j = pending["point"]
            actual = likelihood(values[i, j], pending["s"]) / pending["old"]
            assert lo <= actual <= hi
            length = event["bits_end"] - pending["origin"]
            prefix, denominator = bit_prefix(tape, pending["origin"], length)
            if event["decision"] == "accept":
                assert F(prefix + 1, denominator) <= actual
            else:
                assert F(prefix, denominator) >= actual
            total["pinned_final_decisions_checked"] += 1
            pending = None
        elif kind == "osstar_trial":
            i, j = event["point"]
            s = event["s"]
            weight = likelihood(values[i, j], s)
            assert weight == rational(event["exact_likelihood"])
            ratio = weight / rational(event["upper"])
            assert ratio == rational(event["acceptance_ratio"])
            assert 0 <= ratio <= 1
            key = tuple(event["cell"])
            keys = sorted(active, key=lambda node: (node[1], node[2], node[0]))
            masses = [node_masses[node] * bounds[node, s][1] for node in keys]
            idx = keys.index(key)
            assert idx == event["proposal_cdf"]["selected_index"]
            verify_category(tape, event["proposal_cdf"], idx, masses)
            total["exact_proposal_categories_checked"] += 1
            for comparison in event["comparisons"]:
                verify_comparison(tape, event["bits_start"], comparison)
                total["exact_tape_comparisons_checked"] += 1
        elif kind == "posterior_output":
            i, j = event["point"]
            assert event["row_major_index"] == 16 * i + j
            if name == "fullgrid":
                s = event["task_s"]
                masses = [likelihood(values[row, col], s)
                          for row in range(16) for col in range(16)]
                verify_category(tape, {"start": event["bits_start"], "end": event["bits_end"]},
                                event["row_major_index"], masses)
                total["exact_proposal_categories_checked"] += 1
            total["posterior_outputs_checked"] += 1
    assert pending is None
    assert total["posterior_outputs_checked"] == 128
    if name == "fullgrid":
        table = raw["control_paid_grid_table"]
        for i in range(16):
            for j in range(16):
                assert rational(table[i][j]) == values[i, j]
        total["paid_point_values_checked"] += 256
    return total


def main():
    start = time.perf_counter()
    values = {(i, j): point_value(i, j) for i in range(16) for j in range(16)}
    methods = {name: audit_method(name, values) for name in ("lead", "osstar", "fullgrid")}
    report = {
        "status": "PASS", "arithmetic": "independent exact Fraction evaluation",
        "scope": "finite source containment, likelihood bounds, pinned decisions and public tape comparisons; not an empirical sampling-law test",
        "evaluator_only_point_calls": 256,
        "evaluator_only_recurrence_steps": 256 * STEPS,
        "evaluator_point_arithmetic": {"subtractions": 256 * STEPS,
                                      "multiplications": 2 * 256 * STEPS},
        "evaluator_table_not_passed_to_any_learner": True,
        "maximum_exact_forward_denominator_bits": max(v.denominator.bit_length() for v in values.values()),
        "methods": methods, "wall_seconds": time.perf_counter() - start,
        "proof_companion": "exact_adaptive_law_check.py checks sampling laws by exact finite-state absorption",
    }
    (HERE / "independent_transcript_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

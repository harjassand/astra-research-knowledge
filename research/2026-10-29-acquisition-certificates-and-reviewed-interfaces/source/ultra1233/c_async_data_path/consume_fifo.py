"""One whole finite native consumer, with independent reference definitions.

The target FIFO class is imported to exercise its actual operations. Queue,
edit distance, work, enabling predicates and scalar-receiver checks below
do NOT call the target's corresponding helper functions for their reference.
No all-size claim is inferred by extrapolating this finite execution.
"""
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import resource
import sys
import time

from fifo import FIFO


def edit(a, b):
    row = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        new = [i]
        for j, y in enumerate(b, 1):
            new.append(min(new[-1] + 1, row[j] + 1, row[j - 1] + (x != y)))
        row = new
    return row[-1]


def read_state(s, M, B):
    payload = [(s >> (B * j)) % (1 << B) for j in range(M)]
    tags = [(s >> (B * M + j)) % 2 for j in range(M + 1)]
    occupied = [int(tags[j] != tags[j + 1]) for j in range(M)]
    queue = tuple(payload[j] for j in range(M - 1, -1, -1) if occupied[j])
    work = sum((M - j) * occupied[j] for j in range(M))
    return payload, tags, occupied, queue, work


def main():
    root = Path(__file__).resolve().parent
    packet = json.loads((root / "DEADLINE.json").read_text())
    M, B, q = (packet["inputs"][key]
               for key in ["capacity", "packet_bits", "fault_support_bits"])
    N = (B + 1) * M + 1
    if N > 16 or q > 3:
        raise ValueError("finite consumer budget is explicit: N<=16,q<=3")
    device = FIFO(M, B)
    masks = [sum(1 << j for j in positions)
             for size in range(q + 1)
             for positions in itertools.combinations(range(N), size)]
    start = time.perf_counter()
    nominal = 0
    fault_checks = 0
    max_edits = 0
    max_work_increase = 0
    positive_states = 0
    for state in range(1 << N):
        values, tags, e, word, work = read_state(state, M, B)
        assert device.queue(state) == word
        assert device.workload(state) == work
        enabled = [j for j in range(1, M) if e[j - 1] and not e[j]]
        if work:
            positive_states += 1
            assert enabled or e[-1]
        else:
            assert all(tag == tags[0] for tag in tags)
        for value in range(1 << B):
            out, accepted = device.input_capture(state, value)
            _, _, _, after, _ = read_state(out, M, B)
            assert accepted == (not e[0])
            assert after == (word + (value,) if accepted else word)
            nominal += 1
        for site in range(1, M):
            out, moved = device.internal(state, site)
            _, _, _, after, new_work = read_state(out, M, B)
            assert moved == (site in enabled)
            assert after == word
            assert new_work == work - int(moved)
            nominal += 1
        out, delivered = device.output_commit(state)
        _, _, _, after, new_work = read_state(out, M, B)
        assert delivered == (word[0] if e[-1] else None)
        assert after == (word[1:] if e[-1] else word)
        assert new_work == work - int(bool(e[-1]))
        nominal += 1
        for mask in masks:
            out = device.fault(state, mask)
            _, _, _, after, new_work = read_state(out, M, B)
            distance = edit(word, after)
            bits = mask.bit_count()
            assert distance <= 2 * bits
            assert new_work - work <= 2 * M * bits
            max_edits = max(max_edits, distance)
            max_work_increase = max(max_work_increase, new_work - work)
            fault_checks += 1

    # Independent exact scalar intake; no compile_deadline import.
    width = 2 * (16 * M - 1).bit_length()
    W, C = M * (M + 1) // 2, 2 * M * q
    lam = F(1, 16 * N * (C + 1) * width)
    actual = packet["noise"]["per_bit_rate_upper"]
    assert lam == F(int(actual["numerator"]), int(actual["denominator"]))
    p = F(M, 1 << (width // 2))
    assert p <= F(1, 16)
    assert (C + 1) * N * lam * width + p <= F(1, 8)
    assert (-F(1, 2 * (C + 1)) + p / (C + 1)
            + 2 * N * lam * width) <= -F(5, 16 * (C + 1))
    bits = packet["all_future_selected_starts"]["paid_tail_bits"]
    rounds = -(-(16 * (W + (C + 1) * bits)) // 5)
    assert width * (rounds + 1) == packet["all_future_selected_starts"]["latency_upper"]
    roots = packet["all_future_selected_starts"]["candidate_fixed_boundaries"]
    assert F(roots, 1 << bits) <= F(1, 1 << packet["inputs"]["requested_tail_bits"])
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != "darwin":
        rss *= 1024
    report = {
        "status": "PASS_ALL_DECLARED_NATIVE_STATES_AND_SCALAR_RECEIVER",
        "native_parameters": {"capacity": M, "packet_bits": B, "q": q,
                              "physical_bits_all_noisy": N},
        "physical_states": 1 << N, "nonempty_states_with_enabled_move": positive_states,
        "nominal_transition_checks": nominal, "fault_mask_checks": fault_checks,
        "max_literal_queue_edits": max_edits,
        "max_literal_positive_work_change": max_work_increase,
        "independent_queue_edit_work_references": True,
        "target_class_imported_to_exercise_actual_program": True,
        "producer_scalar_functions_imported": False,
        "all_size_theorem_inferred_by_finite_extrapolation": False,
        "stochastic_trajectories": 0, "physical_experiments": 0,
        "seconds_after_imports": time.perf_counter() - start,
        "peak_rss_bytes": rss,
        "source_sha256": {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                          for name in ["fifo.py", "compile_deadline.py", "consume_fifo.py"]}}
    (root / "NATIVE_REPLAY.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ["status", "physical_states", "fault_mask_checks", "seconds_after_imports"]}))


if __name__ == "__main__":
    main()

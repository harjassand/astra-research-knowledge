"""Finite classical receiver and fault-containment checks.

The fault model is deterministic, synchronous and spatially local. No iid
probability, perfect voter, reliable final decoder, or probabilistic hardware
number is supplied. Bit checks allow a faulty source to equivocate separately
to each receiving voter; their universal per-receiver property proves the
whole-word statement by applying it to each bit.
"""

from dataclasses import asdict, dataclass, replace
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def majority5(a, b, c, d, e):
    """Twelve two-input AND/OR gates, maximum combinational depth five."""
    p, q, r, s = a | b, a & b, c | d, c & d  # four gates
    at_least_three_of_four = (q & r) | (p & s)  # three gates
    at_least_two_of_four = (q | s) | (p & r)  # three gates
    return at_least_three_of_four | (e & at_least_two_of_four)  # two


def odd_even_majority(bits):
    """An explicit N-layer sorting network; each comparator is AND plus OR."""
    bits = list(bits)
    n = len(bits)
    assert n % 2 == 1
    for layer in range(n):
        for j in range(layer % 2, n - 1, 2):
            bits[j], bits[j + 1] = bits[j] & bits[j + 1], bits[j] | bits[j + 1]
    return bits[n // 2]


def voter_truth_tables():
    for bits in product((0, 1), repeat=5):
        assert majority5(*bits) == (sum(bits) >= 3)
    for n in (5, 7):
        for bits in product((0, 1), repeat=n):
            assert odd_even_majority(bits) == (sum(bits) > n // 2)
    return {
        "majority5_truth_table_cases": 32,
        "majority5_two_input_AND_OR_gates": 12,
        "majority5_gate_depth": 5,
        "majority7_sort_network_truth_table_cases": 128,
        "majority7_two_input_AND_OR_gates": 42,
        "majority7_gate_depth": 7,
        "global_gate_minimality_claimed": False,
    }


def refresh_invariant(n, permanent_count):
    """Old residual state error plus one new arbitrary whole-pod fault.

    A fresh pod fault may corrupt its source value AND its own voter/output.
    Persistent bad pods may do both on every update. Each nonfaulty receiver
    is tested against every possible value from all bad source channels,
    which permits arbitrary per-destination equivocation without enumerating
    a redundant Cartesian product of the different receiving voters.
    """
    voter = (lambda xs: majority5(*xs)) if n == 5 else odd_even_majority
    cases, violations = 0, []
    for correct in (0, 1):
        for permanent_tuple in combinations(range(n), permanent_count):
            permanent = set(permanent_tuple)
            for old in (None,) + tuple(i for i in range(n) if i not in permanent):
                for fresh in (None,) + tuple(range(n)):
                    bad_sources = permanent | ({old} if old is not None else set())
                    bad_sources |= ({fresh} if fresh is not None else set())
                    bad_outputs = permanent | ({fresh} if fresh is not None else set())
                    assert len(bad_outputs) <= permanent_count + 1
                    ordered_bad = sorted(bad_sources)
                    for receiver in range(n):
                        if receiver in bad_outputs:
                            continue
                        for bad_values in product((0, 1), repeat=len(ordered_bad)):
                            inputs = [correct] * n
                            for source, value in zip(ordered_bad, bad_values):
                                inputs[source] = value
                            actual = int(voter(inputs))
                            cases += 1
                            if actual != correct and len(violations) < 5:
                                violations.append({
                                    "correct": correct,
                                    "permanent": list(permanent_tuple),
                                    "old_bad_state": old,
                                    "fresh_fault_pod": fresh,
                                    "receiving_voter": receiver,
                                    "input_values": inputs,
                                    "wrong_output": actual,
                                })
    return {
        "replicas": n,
        "permanently_bad_pods": permanent_count,
        "old_transient_bad_states": 1,
        "fresh_fault_domains_per_update": 1,
        "per_receiver_exhaustive_cases": cases,
        "first_violations": violations,
        "boundary_bad_state_bound": permanent_count + 1,
        "arbitrary_whole_words_follow_bitwise": not violations,
        "per_destination_equivocation_included": True,
    }


def rep_syndrome(v, n):
    return sum((((v >> j) ^ (v >> (j + 1))) & 1) << j for j in range(n - 1))


def decode_repetition(syndrome, n):
    v, current = 0, 0
    for j in range(1, n):
        current ^= (syndrome >> (j - 1)) & 1
        v |= current << j
    if v.bit_count() > n // 2:
        v ^= (1 << n) - 1
    assert rep_syndrome(v, n) == syndrome
    return v


def path_snapshot_syndrome(edge_bits, n):
    """n rows/columns, with n-1 path edges in each; no majority oracle."""
    assert len(edge_bits) == n * (n - 1)
    answer = 0
    for j in range(n - 1):
        bit = 0
        for r in range(n):
            bit ^= edge_bits[r * (n - 1) + j]
        answer |= bit << j
    return answer


@dataclass(frozen=True)
class ReceiverState:
    axis: int = 0  # zero reads XX and corrects Z; one reads ZZ and corrects X
    rounds: int = 0
    streak: int = 0
    last: int = 0
    have_last: bool = False
    x_frame: int = 0
    z_frame: int = 0
    flag: bool = False


def receiver_update(state, physical_syndrome, n=5, s=1):
    """The actual finite deterministic state machine replicated in every pod.

    A physical pulse sequencer performs the H/sample/phase-control operations
    already declared in the quantum contract. This function handles their
    finite measurement reports, agreement history and Pauli frame. Returning
    a command leaves it encoded across pods until local physical actuation.
    """
    if state.flag:
        return state, "FLAG"
    frame = state.z_frame if state.axis == 0 else state.x_frame
    syndrome = physical_syndrome ^ rep_syndrome(frame, n)
    rounds = state.rounds + 1
    streak = state.streak + 1 if state.have_last and syndrome == state.last else 1
    updated = replace(state, rounds=rounds, streak=streak, last=syndrome,
                      have_last=True)
    if streak >= s + 1:
        correction = decode_repetition(syndrome, n)
        if state.axis == 0:
            updated = replace(updated, z_frame=state.z_frame ^ correction,
                              axis=1)
            command = "RESTORE_H_THEN_READ_ZZ"
        else:
            updated = replace(updated, x_frame=state.x_frame ^ correction,
                              axis=0)
            command = "NEXT_CYCLE_H_THEN_READ_XX"
        return replace(updated, rounds=0, streak=0, last=0, have_last=False), command
    if rounds >= (s + 1) ** 2:
        return replace(updated, flag=True), "FLAG"
    return updated, "REPEAT_SAME_AXIS"


def finite_receiver_check():
    cases = 0
    # Every syndrome and every stored component frame, for n=5 and n=7.
    for n in (5, 7):
        for axis in (0, 1):
            for frame in range(1 << n):
                for residual in range(1 << n):
                    if residual.bit_count() > n // 2:
                        continue
                    state = ReceiverState(axis=axis,
                                          x_frame=frame if axis else 0,
                                          z_frame=0 if axis else frame)
                    physical = rep_syndrome(frame ^ residual, n)
                    first, command = receiver_update(state, physical, n)
                    assert command == "REPEAT_SAME_AXIS"
                    second, command = receiver_update(first, physical, n)
                    corrected_frame = second.x_frame if axis else second.z_frame
                    assert corrected_frame == frame ^ residual
                    assert second.axis == 1 - axis and not second.flag
                    cases += 1
    # An observed disagreement flag, not an ideal physical-fault detector.
    state = ReceiverState()
    commands = []
    for syndrome in (0, 1, 0, 1):
        state, cmd = receiver_update(state, syndrome)
        commands.append(cmd)
    assert state.flag and commands[-1] == "FLAG"
    return {"frame_and_syndrome_update_cases": cases,
            "violations": [],
            "observed_cap_failure": {"syndromes": [0, 1, 0, 1],
                                     "commands": commands,
                                     "final_state": asdict(state)}}


def insufficient_redundancy_counterexamples():
    examples = []
    for n, permanent, old, fresh in ((3, [], 0, 1), (5, [0], 1, 2)):
        bad = set(permanent) | {old, fresh}
        inputs = [int(i in bad) for i in range(n)]
        output = int(sum(inputs) > n // 2)
        assert output == 1
        examples.append({"replicas": n, "correct": 0, "permanent": permanent,
                         "old_bad_state": old, "fresh_fault_pod": fresh,
                         "voter_inputs": inputs, "wrong_majority": output})
    return examples


def resource_contract():
    return {
        "five_replica_case": {
            "decoder_state_machine_copies": 5,
            "state_plus_candidate_bits_per_logical_state_bit": 10,
            "refresh_two_input_gates_per_logical_state_bit": 60,
            "refresh_gate_depth": 5,
            "distinct_source_to_voter_input_paths_per_logical_state_bit": 25,
            "final_logical_bit_remains_five_bit_encoded": True,
        },
        "seven_replica_one_persistent_pod_case": {
            "decoder_state_machine_copies": 7,
            "state_plus_candidate_bits_per_logical_state_bit": 14,
            "refresh_two_input_gates_per_logical_state_bit": 294,
            "refresh_gate_depth": 7,
            "distinct_source_to_voter_input_paths_per_logical_state_bit": 49,
            "final_logical_bit_remains_seven_bit_encoded": True,
        },
        "receiver_only_state_example": {
            "n5_state_bits_including_three_bit_pulse_phase": 25,
            "n7_state_bits_including_three_bit_pulse_phase": 31,
            "excludes": "ADC precision words, pulse-duration counters, physical calibration tables, program memory, extra queues and application payload; their actual stored bits and computation must also be replicated.",
        },
        "important_budget_separation": "One corrected internal pod fault per update does not authorize one actuator failure at every update: failed final local actuator voters are quantum physical faults and count against the complete quantum cycle budget.",
    }


def main():
    result = {
        "voter_circuits": voter_truth_tables(),
        "five_replica_refresh": refresh_invariant(5, 0),
        "seven_replica_refresh_with_one_persistent_pod": refresh_invariant(7, 1),
        "insufficient_redundancy_counterexamples": insufficient_redundancy_counterexamples(),
        "actual_finite_receiver": finite_receiver_check(),
        "resources": resource_contract(),
        "scope": "Synchronous deterministic local fault domains, with real finite logic. No hardware failure probabilities, no perfect final voter, no asynchronous Byzantine consensus, and no tolerance of arbitrary shared global faults."
    }
    assert not result["five_replica_refresh"]["first_violations"]
    assert not result["seven_replica_refresh_with_one_persistent_pod"]["first_violations"]
    path = HERE / "classical_refresh_checks.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Finite logical-interface checks for a framed quantum-transfer transaction.

This is NOT a physical fault-tolerant code implementation, a Poisson-noise
simulation, or a threshold estimate.  Protected copies, counters, normalizers,
and conditional couplers have their analytically proved logical actions.
All physical bulk/controller faults remain in the analytical error budget.

The classical check exhausts M=3, J=3 transcripts with at most one erroneous
sample per frame.  It includes fixed request frames, no request, and every
map from the four possible first-frame records to requesting frame 2 or 3.
Those adaptive policies see ONLY completed prior records.  Giving such a
record to a test policy exercises the causal quantifier; any physical
feedback/observation mechanism furnishing it must itself be charged.

The quantum check uses six qubits in this order:
  I_source, D_source, Ref, I_receiver, D_receiver, Env.
It tests the selected transfer chain
  D_source -> I_source -> I_receiver -> D_receiver
at its stipulated phase, with arbitrary correlated initial junk and
selected CPTP maps on the two sacrificial ports and environment.
Wrong-frame port channels and the always-applied raw port SWAP do not
couple to retained data when the protected guards are false.

The selected quantum transfer interface is successful in these tests;
its physical failure probability is paid once in the theorem.  No
unprotected output is claimed to survive later raw-port noise.

Run: python framed_transfer.py --self-test
Requires Python 3 and NumPy.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import itertools
import json
import math
from typing import Callable

import numpy as np


TOLERANCE = 1.0e-10
M = 3
J = 3
QUBIT_ORDER = (
    "I_source", "D_source", "Ref", "I_receiver", "D_receiver", "Env"
)
IS, DS, REF, IR, DR, ENV = range(6)
N_QUBITS = len(QUBIT_ORDER)
SWAP = np.array(
    [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]],
    dtype=complex,
)


@dataclass(frozen=True)
class Policy:
    name: str
    choose_now: Callable[[int, tuple[tuple[int, ...], ...]], bool]


def fixed_policy(frame: int | None) -> Policy:
    return Policy(
        "never" if frame is None else f"fixed_frame_{frame}",
        lambda current, past, requested=frame: current == requested,
    )


def adaptive_policy(mask: int) -> Policy:
    # Frame 1 is a null frame.  Its four permissible received records
    # have Hamming weight <=1.  A four-bit mask chooses frame 2 vs 3.
    records = (
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
    )

    def choose(current: int, past: tuple[tuple[int, ...], ...]) -> bool:
        if current == 1:
            assert not past
            return False
        if current == 2:
            assert len(past) == 1
            index = records.index(past[0])
            return bool((mask >> index) & 1)
        assert current == 3 and len(past) == 2
        return True  # Used only if no earlier request was selected.

    return Policy(f"adaptive_first_record_mask_{mask:04b}", choose)


def error_patterns(m: int = M, frames: int = J):
    # A marked bad sample may be replaced by either bit.  Replacing it
    # by the correct bit is already covered by the all-zero flip mask.
    choices = [tuple(0 for _ in range(m))]
    choices += [tuple(int(i == j) for i in range(m)) for j in range(m)]
    return itertools.product(choices, repeat=frames)


def transaction(
    policy: Policy, flips: tuple[tuple[int, ...], ...], m: int = M
) -> dict:
    """Run complete framed logic; the store never sees selected_frame."""
    if m % 2 != 1:
        raise ValueError("This finite harness uses odd frame length.")
    frames = len(flips)
    selected_frame = None       # Requester's protected record.
    sender_snapshot = 0
    store_done = False
    receiver_done = False
    phase = ones = 0
    past: list[tuple[int, ...]] = []
    releases: list[tuple[int, int]] = []
    admissions: list[tuple[int, int]] = []
    trace = []
    mutable_controller_writes = 0
    request_policy_evaluations = 0
    raw_symbols = nonidle_symbols = 0
    partial_frame_checks = 0

    for frame, error_mask in enumerate(flips, start=1):
        assert len(error_mask) == m and sum(error_mask) <= 1
        if selected_frame is None:
            request_policy_evaluations += 1
            # ONLY completed past records, with no current/future error input.
            if policy.choose_now(frame, tuple(past)):
                selected_frame = frame
        sender_snapshot = int(selected_frame == frame)
        mutable_controller_writes += 1
        received = []
        for slot, flip in enumerate(error_mask, start=1):
            symbol = sender_snapshot ^ flip
            raw_symbols += 1
            nonidle_symbols += sender_snapshot
            received.append(symbol)
            phase += 1
            ones += symbol
            mutable_controller_writes += 2
            if slot < m:
                # No release or admission is evaluated before frame end.
                assert all(f != frame for f, _ in releases)
                assert all(f != frame for f, _ in admissions)
                partial_frame_checks += 1

        assert phase == m
        majority = int(2 * ones > m)
        release = bool(majority and not store_done)
        store_done = store_done or release
        accept = bool(selected_frame == frame and not receiver_done)
        receiver_done = receiver_done or accept
        # majority, release, store_done, accept, receiver_done: five writes.
        mutable_controller_writes += 5
        if release:
            releases.append((frame, m))
        if accept:
            admissions.append((frame, m))
        trace.append(
            dict(
                frame=frame,
                sent_bit=sender_snapshot,
                received_bits=received,
                phase_of_decision=phase,
                majority=majority,
                release=release,
                requester_admission=accept,
            )
        )
        past.append(tuple(received))
        phase = ones = 0
        mutable_controller_writes += 2

    expected = [] if selected_frame is None else [(selected_frame, m)]
    assert releases == admissions == expected
    assert raw_symbols == m * frames
    assert nonidle_symbols == (0 if selected_frame is None else m)
    assert mutable_controller_writes == 2 * m * frames + 8 * frames
    return dict(
        policy=policy.name,
        selected_frame=selected_frame,
        release_events=releases,
        admission_events=admissions,
        known_delivery_tick=None if selected_frame is None else selected_frame * m,
        trace=trace,
        costs=dict(
            raw_classical_symbols_sent=raw_symbols,
            nonidle_classical_symbols_sent=nonidle_symbols,
            logical_mutable_controller_writes=mutable_controller_writes,
            logical_policy_evaluations=request_policy_evaluations,
            frame_end_decisions=frames,
            always_scheduled_raw_port_swaps=frames,
            selected_quantum_transfer_chains=len(releases),
        ),
        no_partial_frame_release_checks=partial_frame_checks,
    )


def exhaustive_classical_checks() -> dict:
    policies = [fixed_policy(None)] + [fixed_policy(j) for j in range(1, J + 1)]
    policies += [adaptive_policy(mask) for mask in range(16)]
    patterns = tuple(error_patterns())
    summaries = []
    examples = []
    total_partial_checks = 0
    for policy in policies:
        histogram = {"none": 0, "1": 0, "2": 0, "3": 0}
        for flips in patterns:
            result = transaction(policy, flips)
            key = "none" if result["selected_frame"] is None else str(result["selected_frame"])
            histogram[key] += 1
            total_partial_checks += result["no_partial_frame_release_checks"]
        summaries.append(
            dict(policy=policy.name, transcript_count=len(patterns),
                 selected_frame_histogram=histogram)
        )
    representative_flips = (
        (0, 1, 0), (1, 0, 0), (0, 0, 1)
    )
    for policy in (
        fixed_policy(None), fixed_policy(1), fixed_policy(2), fixed_policy(3),
        adaptive_policy(0b0100), adaptive_policy(0b0001),
    ):
        examples.append(transaction(policy, representative_flips))
    assert len(policies) == 20 and len(patterns) == 64
    return dict(
        M=M,
        J=J,
        policy_count=len(policies),
        bad_sample_pattern_count=len(patterns),
        exhaustive_case_count=len(policies) * len(patterns),
        no_partial_frame_release_checks=total_partial_checks,
        every_case_has_at_most_one_wrong_sample_per_frame=True,
        every_release_and_admission_is_at_selected_frame_end=True,
        adaptive_policy_access="Completed prior frame records only; any physical feedback supplying them must be charged separately.",
        per_case_costs=examples[0]["costs"],
        policy_summaries=summaries,
        representative_cases=examples,
    )


def apply_operator(
    rho: np.ndarray, operator: np.ndarray, targets: tuple[int, ...]
) -> np.ndarray:
    n = rho.shape[0].bit_length() - 1
    assert rho.shape == (1 << n, 1 << n)
    assert len(set(targets)) == len(targets)
    rest = tuple(q for q in range(n) if q not in targets)
    order = targets + rest
    axes = order + tuple(n + q for q in order)
    small, other = 1 << len(targets), 1 << len(rest)
    assert operator.shape == (small, small)
    a = rho.reshape((2,) * (2 * n)).transpose(axes)
    a = a.reshape(small, other, small, other)
    a = np.einsum("ai,irjs,bj->arbs", operator, a, operator.conj(), optimize=True)
    return a.reshape((2,) * (2 * n)).transpose(np.argsort(axes)).reshape(rho.shape)


def reduced_state(rho: np.ndarray, keep: tuple[int, ...]) -> np.ndarray:
    n = rho.shape[0].bit_length() - 1
    rest = tuple(q for q in range(n) if q not in keep)
    order = keep + rest
    a = rho.reshape((2,) * (2 * n)).transpose(
        order + tuple(n + q for q in order)
    )
    a = a.reshape(1 << len(keep), 1 << len(rest),
                  1 << len(keep), 1 << len(rest))
    return np.einsum("aibi->ab", a)


def trace_distance(left: np.ndarray, right: np.ndarray) -> float:
    difference = left - right
    difference = (difference + difference.conj().T) / 2
    return float(np.abs(np.linalg.eigvalsh(difference)).sum() / 2)


def random_unitary(dimension: int, rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    q, r = np.linalg.qr(raw)
    diagonal = np.diag(r)
    result = q * (diagonal / np.abs(diagonal)).conj()
    assert np.max(np.abs(result.conj().T @ result - np.eye(dimension))) < TOLERANCE
    return result


def reset_qubit(rho: np.ndarray, target: int, state: np.ndarray) -> np.ndarray:
    state = state / np.linalg.norm(state)
    k0 = np.outer(state, np.array([1.0, 0.0]))
    k1 = np.outer(state, np.array([0.0, 1.0]))
    return apply_operator(rho, k0, (target,)) + apply_operator(rho, k1, (target,))


class PortCorruption:
    """Selected CPTP channels on ports + common environment; never on D or Ref."""

    def __init__(self, rng: np.random.Generator, allow_resets: bool):
        self.rng = rng
        self.allow_resets = allow_resets
        self.calls = 0
        self.resets = 0
        self.max_retained_marginal_change = 0.0

    def __call__(self, rho: np.ndarray) -> np.ndarray:
        before_source = reduced_state(rho, (DS, REF))
        before_receiver = reduced_state(rho, (DR, REF))
        targets = (IS, IR, ENV)
        u = random_unitary(8, self.rng)
        v = random_unitary(8, self.rng)
        weight = float(self.rng.uniform(0.1, 0.9))
        rho = weight * apply_operator(rho, u, targets) + (
            1.0 - weight
        ) * apply_operator(rho, v, targets)
        self.calls += 1
        if self.allow_resets and self.calls % 2 == 0:
            state = self.rng.normal(size=2) + 1j * self.rng.normal(size=2)
            rho = reset_qubit(rho, IS if self.calls % 4 == 0 else IR, state)
            self.resets += 1
        self.max_retained_marginal_change = max(
            self.max_retained_marginal_change,
            trace_distance(before_source, reduced_state(rho, (DS, REF))),
            trace_distance(before_receiver, reduced_state(rho, (DR, REF))),
        )
        assert self.max_retained_marginal_change < TOLERANCE
        return rho


def initial_state(kind: str, rng: np.random.Generator) -> np.ndarray:
    if kind == "bell_payload_entangled_junk":
        bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2.0)
        junk = rng.normal(size=16) + 1j * rng.normal(size=16)
        junk /= np.linalg.norm(junk)
        order = (DS, REF, IS, IR, DR, ENV)
        vector = np.kron(bell, junk).reshape((2,) * N_QUBITS)
        vector = vector.transpose(tuple(order.index(q) for q in range(N_QUBITS)))
        vector = vector.reshape(-1)
    elif kind == "fully_correlated_six_qubit_state":
        vector = rng.normal(size=64) + 1j * rng.normal(size=64)
        vector /= np.linalg.norm(vector)
    else:
        raise ValueError(kind)
    return np.outer(vector, vector.conj())


def density_errors(rho: np.ndarray) -> dict:
    hermitian = (rho + rho.conj().T) / 2
    return dict(
        trace_error=float(abs(np.trace(rho) - 1.0)),
        hermiticity_error=float(np.max(np.abs(rho - rho.conj().T))),
        negative_eigenvalue_error=float(max(0.0, -np.linalg.eigvalsh(hermitian).min())),
    )


def quantum_case(
    classical: dict, kind: str, allow_resets: bool, rng: np.random.Generator
) -> dict:
    rho = initial_state(kind, rng)
    intended = reduced_state(rho, (DS, REF))
    initial_receiver = reduced_state(rho, (DR, REF))
    port_noise = PortCorruption(rng, allow_resets)
    selected = classical["selected_frame"]
    source_releases = receiver_admissions = raw_swaps = 0
    captured_error = None
    stage_errors = []
    post_delivery_error = 0.0
    source_preservation_before_release = 0.0

    # Continue for two extra frames.  All their port contents are arbitrary;
    # both protected one-shot guards remain false.
    for frame in range(1, J + 3):
        rho = port_noise(rho)
        release = frame <= J and classical["trace"][frame - 1]["release"]
        accept = frame <= J and classical["trace"][frame - 1]["requester_admission"]
        assert release == accept
        if not source_releases:
            source_preservation_before_release = max(
                source_preservation_before_release,
                trace_distance(reduced_state(rho, (DS, REF)), intended),
            )

        # Protected release; its decoded action is exact on the favorable event.
        if release:
            rho = apply_operator(rho, SWAP, (DS, IS))
            source_releases += 1
            stage_errors.append(
                dict(stage="source_D_to_source_I",
                     error=trace_distance(reduced_state(rho, (IS, REF)), intended))
            )

        # Same raw port SWAP at every frame's stipulated phase.
        # On the selected frame this interface is one of the paid successes.
        rho = apply_operator(rho, SWAP, (IS, IR))
        raw_swaps += 1
        if release:
            stage_errors.append(
                dict(stage="raw_source_I_to_receiver_I",
                     error=trace_distance(reduced_state(rho, (IR, REF)), intended))
            )
        else:
            # A wrong-frame raw transfer may be arbitrarily corrupted.
            rho = port_noise(rho)

        # The requester knows its chosen frame, so it needs no herald search.
        if accept:
            rho = apply_operator(rho, SWAP, (IR, DR))
            receiver_admissions += 1
            captured_error = trace_distance(reduced_state(rho, (DR, REF)), intended)
            stage_errors.append(dict(stage="receiver_I_to_receiver_D", error=captured_error))
            assert frame == selected

        rho = port_noise(rho)
        if receiver_admissions:
            post_delivery_error = max(
                post_delivery_error,
                trace_distance(reduced_state(rho, (DR, REF)), intended),
            )
        else:
            assert trace_distance(reduced_state(rho, (DR, REF)), initial_receiver) < TOLERANCE

    expected_count = int(selected is not None)
    assert source_releases == receiver_admissions == expected_count
    if selected is None:
        captured_error = trace_distance(reduced_state(rho, (DS, REF)), intended)
    errors = density_errors(rho)
    all_errors = [
        captured_error, post_delivery_error,
        source_preservation_before_release, port_noise.max_retained_marginal_change,
        *errors.values(), *(x["error"] for x in stage_errors),
    ]
    assert max(all_errors) < TOLERANCE
    return dict(
        policy=classical["policy"],
        initial_state=kind,
        resets_in_adversarial_port_channels=allow_resets,
        selected_frame=selected,
        known_delivery_tick=classical["known_delivery_tick"],
        selected_transfer_chains=source_releases,
        receiver_admissions=receiver_admissions,
        raw_port_swaps_including_extra_frames=raw_swaps,
        arbitrary_port_channel_calls=port_noise.calls,
        port_reset_count=port_noise.resets,
        reference_inclusive_delivery_error=captured_error,
        post_delivery_protected_memory_error=post_delivery_error,
        source_preservation_before_release_error=source_preservation_before_release,
        maximum_port_only_retained_marginal_change=port_noise.max_retained_marginal_change,
        selected_chain_stage_checks=stage_errors,
        density_errors=errors,
    )


def binomial_examples(q: float = 0.05) -> dict:
    divergence = 0.5 * math.log(0.25 / (q * (1.0 - q)))
    rows = []
    for m in (3, 9, 21, 43):
        exact = sum(
            math.comb(m, k) * q**k * (1.0 - q)**(m - k)
            for k in range(m // 2 + 1, m + 1)
        )
        chernoff = math.exp(-m * divergence)
        assert exact <= chernoff + 1.0e-15
        rows.append(
            dict(
                samples_per_frame=m,
                exact_BSC_frame_majority_error=exact,
                chernoff_source_count_upper_bound=chernoff,
                exact_any_error_in_three_independent_frames=-math.expm1(
                    3 * math.log1p(-exact)
                ),
                three_frame_union_bound=min(1.0, 3 * exact),
                three_frame_chernoff_union_bound=min(1.0, 3 * chernoff),
            )
        )
    return dict(
        q=q,
        q_status="Illustrative certified per-sample bound; not inferred from a physical simulation.",
        exact_model="Independent BSC(q). The theorem only needs independent geometric bad-sample indicators and arbitrary fault values.",
        D_half_given_q=divergence,
        rows=rows,
    )


def self_test(seed: int = 20261105) -> dict:
    classical = exhaustive_classical_checks()
    rng = np.random.default_rng(seed)
    quantum = []
    for example in classical["representative_cases"]:
        for kind in (
            "bell_payload_entangled_junk", "fully_correlated_six_qubit_state"
        ):
            for allow_resets in (False, True):
                quantum.append(quantum_case(example, kind, allow_resets, rng))
    maximum_error = max(
        max(
            item["reference_inclusive_delivery_error"],
            item["post_delivery_protected_memory_error"],
            item["source_preservation_before_release_error"],
            item["maximum_port_only_retained_marginal_change"],
            *item["density_errors"].values(),
        )
        for item in quantum
    )
    return dict(
        artifact="framed_transfer.py",
        passed=True,
        seed=seed,
        tolerance=TOLERANCE,
        scope="Finite logical-interface and causal-frame checks; not a physical code implementation or noise-threshold simulation.",
        assumptions=[
            "All bulk and controller rectangles have their proved ideal actions on the favorable event; their physical failures are counted analytically.",
            "Each tested frame has at most one incorrect sample out of three.",
            "The selected quantum descent, bounded-distance raw transfer, and ascent succeed; this interface failure is paid once analytically.",
            "Intermediate port CPTP maps are confined to I_source, I_receiver, and Env; faults reaching protected D records belong in the bulk budget.",
            "A request frame is chosen from past information only. Its future transfer window is predetermined by that choice, not selected after observing future faults.",
            "The same fixed microscopic synchronous timing premise is retained; protected frame counters are not a proof of asynchronous hardware.",
            "Logical integer counters in this harness stand for encoded words. Physical bit/code expansion and circuit costs are part of the analytical theorem.",
            "Every physical feedback or observation supplying an adaptive policy record must be charged; the harness does not provide a free feedback link.",
        ],
        qubit_order=QUBIT_ORDER,
        classical=classical,
        quantum=dict(case_count=len(quantum), maximum_numerical_error=maximum_error,
                     cases=quantum),
        probability_examples=binomial_examples(),
        numpy_version=np.__version__,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--seed", type=int, default=20261105)
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(args.seed), indent=2, sort_keys=True))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

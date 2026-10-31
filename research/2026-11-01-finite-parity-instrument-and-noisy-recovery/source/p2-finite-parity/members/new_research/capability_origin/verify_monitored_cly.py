"""Independent checks for a monitored, constant-excitation bosonic CZ.

Run with the primary runtime Python. Dependencies: numpy only.
All numerical examples are illustrative design points, not fitted hardware.
"""
from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
BASIS = list(itertools.product(range(5), repeat=4))
INDEX = {state: index for index, state in enumerate(BASIS)}
N = np.asarray(BASIS, dtype=float)
DIM = len(BASIS)


def code_matrix():
    single = [[((4, 0), 1 / np.sqrt(2)), ((0, 4), 1 / np.sqrt(2))],
              [((2, 2), 1.0)]]
    out = np.zeros((DIM, 4), complex)
    for logical, (i, j) in enumerate(itertools.product(range(2), repeat=2)):
        for a, aa in single[i]:
            for b, bb in single[j]:
                out[INDEX[a + b], logical] = aa * bb
    return out


P = code_matrix()
CZ = np.diag([1, 1, 1, -1])


def loss(v, mode):
    out = np.zeros_like(v)
    for row, n in enumerate(BASIS):
        if n[mode]:
            dest = list(n)
            dest[mode] -= 1
            out[INDEX[tuple(dest)]] += np.sqrt(n[mode]) * v[row]
    return out


def integrated_after(t, gate_time, chi, echo):
    """Integrated quadratic interaction after time t, as a 4x4 matrix."""
    out = np.zeros((4, 4))
    if not echo:
        out[0, 2] = out[2, 0] = chi * (gate_time - t)
    else:
        out[0, 2] = out[2, 0] = chi * max(gate_time / 2 - t, 0)
        out[1, 3] = out[3, 1] = chi * (gate_time - max(t, gate_time / 2))
    return out


def segment(v, left, right, gate_time, chi, kappas, echo):
    if right <= left:
        return v
    midpoint = (left + right) / 2
    perm = [1, 0, 3, 2] if echo and midpoint >= gate_time / 2 else [0, 1, 2, 3]
    pair = (1, 3) if echo and midpoint >= gate_time / 2 else (0, 2)
    energy = chi * N[:, pair[0]] * N[:, pair[1]]
    damping = N @ np.asarray(kappas)[perm]
    return np.exp((-1j * energy - damping / 2) * (right - left))[:, None] * v


def trajectory(events, kappas, echo=False, gate_time=1.0):
    """Unnormalized no-jump/jump trajectory in the rail-swap toggling frame."""
    chi = np.pi / (4 * gate_time)
    v = P.copy()
    events = sorted(events)
    boundaries = sorted(set([0.0, gate_time] + [t for t, _ in events]
                            + ([gate_time / 2] if echo else [])))
    event_map = dict(events)
    for left, right in zip(boundaries[:-1], boundaries[1:]):
        v = segment(v, left, right, gate_time, chi, kappas, echo)
        if right in event_map:
            mode = event_map[right]
            perm = [1, 0, 3, 2] if echo and right >= gate_time / 2 else [0, 1, 2, 3]
            v = np.sqrt(kappas[perm[mode]]) * loss(v, mode)
    # The timestamp correction is linear in the occupations. For two jumps,
    # commuting this correction through the second jump changes only a scalar.
    phases = np.zeros(4)
    for t, mode in events:
        phases += integrated_after(t, gate_time, chi, echo)[mode]
    v *= np.exp(-1j * (N @ phases))[:, None]
    logical_gate = np.diag([1, -1, -1, -1]) if echo else CZ
    ref = P @ logical_gate
    for _, mode in events:
        ref = loss(ref, mode)
    coeff = np.vdot(ref, v) / np.vdot(ref, ref)
    residual = np.linalg.norm(v - coeff * ref) / np.linalg.norm(v)
    gram = v.conj().T @ v
    scalar = np.trace(gram) / 4
    gram_error = np.linalg.norm(gram - scalar * np.eye(4)) / abs(scalar)
    return residual, gram_error


WORDS = {
    "0": [[(4, 0), (0, 4)], [(2, 2)]],
    "a": [[(3, 0)], [(1, 2)]],
    "b": [[(0, 3)], [(2, 1)]],
}


def constraints(both):
    sectors = [(a, b) for a in WORDS for b in WORDS
               if both or a == "0" or b == "0"]
    rows = []
    for sector in sectors:
        for i, j in itertools.product(range(2), repeat=2):
            for na in WORDS[sector[0]][i]:
                for nb in WORDS[sector[1]][j]:
                    rows.append((na + nb, i * j, sector))
    return sectors, rows


def exact_rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        val = a[row][col]
        a[row] = [x / val for x in a[row]]
        for i in range(row + 1, len(a)):
            if a[i][col]:
                val = a[i][col]
                a[i] = [x - val * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def degree_test(degree, both):
    sectors, rows = constraints(both)
    exponents = [e for e in itertools.product(range(degree + 1), repeat=4)
                 if sum(e) <= degree]
    a, b = [], []
    # Allow an arbitrary, logically irrelevant scalar energy in every error
    # sector. The code sector's offset is already the constant monomial.
    offsets = sectors[1:]
    for n, target, sector in rows:
        a.append([math.prod(x ** power for x, power in zip(n, e)) for e in exponents]
                 + [-int(sector == s) for s in offsets])
        b.append(target)
    rank = exact_rank(a)
    augmented_rank = exact_rank([row + [target] for row, target in zip(a, b)])
    return {"degree": degree, "one_loss_per_block": both,
            "rank": rank, "augmented_rank": augmented_rank,
            "feasible": rank == augmented_rank}


def polynomial_check(both):
    _, rows = constraints(both)
    worst = 0
    for (a, b, c, d), target, _ in rows:
        if both:
            value = (5 - a - b) * (5 - c - d) * a * b * c * d / 16
        else:
            value = (9 - a - b - c - d) * a * b * c * d / 16
        worst = max(worst, abs(value - target))
    return worst


def resource_example(chi_hz, lifetime=0.001, eta=0.9, recovery_error=0.01):
    chi = 2 * np.pi * chi_hz
    gate_time = np.pi / (4 * chi)
    x = gate_time / lifetime
    p0 = np.exp(-4 * x)
    p1 = 4 * np.exp(-3 * x) * (-np.expm1(-x))
    accepted = (p0 + eta * p1) ** 2
    with_recovery = accepted - p0 ** 2
    return {"chi_over_2pi_hz": chi_hz, "single_photon_lifetime_s": lifetime,
            "gate_time_s": gate_time, "eight_photon_exposure_s": 8 * gate_time,
            "any_loss_probability": 1 - p0 ** 2,
            "two_or_more_losses_in_a_block": 1 - (p0 + p1) ** 2,
            "accepted_with_90pct_timestamp_coverage": accepted,
            "accepted_fraction_needing_recovery": with_recovery / accepted,
            "expected_number_of_block_recoveries_per_accepted_gate":
                2 * eta * p1 / (p0 + eta * p1),
            "conditional_error_if_each_block_recovery_error_is_1pct":
                1 - ((p0 + eta * p1 * (1 - recovery_error)) / (p0 + eta * p1)) ** 2}


def main():
    rng = np.random.default_rng(110503)
    checks = []
    for echo, rates in [(False, [0.02] * 4), (True, [0.01, 0.04, 0.017, 0.031])]:
        for _ in range(24):
            chosen = []
            for block in [(0, 1), (2, 3)]:
                if rng.uniform() > 0.25:
                    chosen.append((rng.uniform(0.01, 0.99), int(rng.choice(block))))
            checks.append(trajectory(chosen, rates, echo))
    mismatch = trajectory([], [0.01, 0.04, 0.017, 0.031], False)
    sigma = 0.002
    angles = np.linspace(-np.sqrt(3) * sigma, np.sqrt(3) * sigma, 100001)
    # Entanglement fidelity of a physical phase rotation on one CLY block.
    timing_infidelity = np.mean(1 - ((1 + np.cos(2 * angles)) / 2) ** 2)
    report = {
        "maximum_corrected_trajectory_relative_residual": max(x[0] for x in checks),
        "maximum_information_leakage_gram_relative_residual": max(x[1] for x in checks),
        "unequal_rates_without_echo_gram_residual": mismatch[1],
        "degree_tests": [degree_test(4, False), degree_test(5, False),
                         degree_test(5, True), degree_test(6, True)],
        "degree5_explicit_polynomial_max_residual": polynomial_check(False),
        "degree6_explicit_polynomial_max_residual": polynomial_check(True),
        "uniform_timing_angle_variance": sigma ** 2,
        "timing_entanglement_infidelity": timing_infidelity,
        "timing_small_angle_prediction": 2 * sigma ** 2,
        "illustrative_resource_examples": [resource_example(1e4), resource_example(1e5)],
    }
    (ROOT / "verification_results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

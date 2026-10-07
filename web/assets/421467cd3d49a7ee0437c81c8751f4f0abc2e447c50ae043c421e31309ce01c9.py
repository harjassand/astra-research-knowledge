#!/usr/bin/env python3
"""Scoped diagnostics of the acquisition_attack.md constructions.

The decoder receives only the episode callable, d, a bias bound and confidence.
Target masks are used only by the auditor outside the decoder.
"""
import json
import math
import random
from fractions import Fraction
from pathlib import Path


def parity(mask, bits):
    return (mask & bits).bit_count() & 1


def solve_gf2(rows, d):
    basis = {}
    xors = 0
    for bits, label in rows:
        while bits:
            pivot = bits.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (bits, label)
                break
            bits ^= basis[pivot][0]
            label ^= basis[pivot][1]
            xors += 1
        if not bits and label:
            raise ValueError('inconsistent labels')
    if len(basis) < d:
        raise ValueError('rank deficient input matrix')
    solution = 0
    for pivot in sorted(basis):
        bits, label = basis[pivot]
        other = bits & ~(1 << pivot)
        if label ^ parity(other, solution):
            solution |= 1 << pivot
    return solution, xors


def decode_repeated(episode, d, beta, delta):
    count = d + math.ceil(math.log2(3 / delta))
    repeats = math.ceil(2 * math.log(3 * count / delta) / (beta * beta))
    if repeats % 2 == 0:
        repeats += 1
    rows = []
    for _ in range(count):
        inputs, outputs = episode(repeats)
        label = int(sum(outputs) > repeats // 2)
        rows.append((inputs, label))
    recovered, xors = solve_gf2(rows, d)
    return recovered, {
        'episodes': count, 'repeats_per_episode': repeats,
        'observed_symbols': count * (d + repeats),
        'gf2_row_xors': xors, 'hidden_mask_read_by_decoder': False,
    }


def episode_interface(d, mask, eta, seed):
    rng = random.Random(seed)
    def observe(repeats):
        a = rng.randrange(1 << d)
        truth = parity(mask, a)
        return a, [truth ^ int(rng.random() < eta) for _ in range(repeats)]
    return observe


def validate_frozen_mask(episode, d, candidate, beta, delta):
    count = math.ceil(32 * math.log(6 / delta) / (beta * beta))
    signs = 0
    for _ in range(count):
        a, outputs = episode(1)
        signs += -1 if outputs[0] ^ parity(candidate, a) else 1
    empirical = signs / count
    radius = math.sqrt(2 * math.log(6 / delta) / count)
    lower = empirical - radius
    return lower >= beta / 2, {
        'validation_episodes': count,
        'validation_observed_symbols': count * (d + 1),
        'bias_confidence_lower_bound': lower,
        'active_cut_margin_lower_bound_if_accepted': lower / 2,
    }


def exact_cut_moment(d, mask, cut, eta):
    prefix_mask = mask & ((1 << cut) - 1)
    if not prefix_mask:
        return None
    suffix_mask = mask ^ prefix_mask
    matrix = [[Fraction(0) for _ in range(2)] for _ in range(2)]
    for a in range(1 << d):
        u = parity(prefix_mask, a)
        truth = parity(mask, a)
        for b in (0, 1):
            probability = (1 - eta if b == truth else eta) / (1 << d)
            v = parity(suffix_mask, a) ^ b
            matrix[u][v] += probability
    return matrix


def bucket_identity(g, d, k, prefix):
    coefficients = []
    for suffix in range(1 << (d - k)):
        mask = prefix | (suffix << k)
        coefficients.append(sum(g[a] * (-1 if parity(mask, a) else 1)
                                for a in range(1 << d)) / (1 << d))
    fourier_energy = sum(v * v for v in coefficients)
    shared_suffix_average = Fraction(0)
    for z in range(1 << (d - k)):
        inner = sum(g[a | (z << k)] * (-1 if parity(prefix, a) else 1)
                    for a in range(1 << k)) / (1 << k)
        shared_suffix_average += inner * inner / (1 << (d - k))
    assert fourier_energy == shared_suffix_average


def run():
    exact_count = 0
    for d in range(1, 7):
        for mask in range(1, 1 << d):
            for eta in (Fraction(0), Fraction(1, 8), Fraction(1, 4), Fraction(3, 8)):
                theta = 1 - 2 * eta
                expected = [[(1 + theta) / 4, (1 - theta) / 4],
                            [(1 - theta) / 4, (1 + theta) / 4]]
                for cut in range(1, d + 1):
                    matrix = exact_cut_moment(d, mask, cut, eta)
                    if matrix is not None:
                        assert matrix == expected
                        assert matrix[0][0] + matrix[0][1] == Fraction(1, 2)
                        assert matrix[0][0] - matrix[0][1] == theta / 2
                        exact_count += 1
    rng = random.Random(91007)
    bucket_count = 0
    for d in range(1, 7):
        g = [Fraction(rng.randrange(-8, 9), 8) for _ in range(1 << d)]
        for k in range(d + 1):
            for prefix in range(1 << k):
                bucket_identity(g, d, k, prefix)
                bucket_count += 1
    trials = []
    for d in (4, 8, 16, 32, 64):
        for trial in range(4):
            mask = rng.randrange(1, 1 << d)
            observe = episode_interface(d, mask, 0.25, 137 * d + trial)
            recovered, cost = decode_repeated(observe, d, 0.5, 0.01)
            assert recovered == mask
            accepted, certificate = validate_frozen_mask(observe, d, recovered, 0.5, 0.01)
            assert accepted
            assert certificate['active_cut_margin_lower_bound_if_accepted'] >= 0.125
            wrong_accepted, wrong_certificate = validate_frozen_mask(observe, d, recovered ^ 1, 0.5, 0.01)
            assert not wrong_accepted
            trials.append({'d': d, 'fixture': trial, 'exact_mask_recovered': True,
                           'correct_mask_certificate_accepted': accepted,
                           'wrong_mask_certificate_accepted': wrong_accepted,
                           'wrong_mask_validation_observed_symbols': wrong_certificate['validation_observed_symbols'],
                           **cost, **certificate})
    result = {
        'status': 'PASS',
        'scope': 'Finite diagnostics; not a proof, LPN solver, novelty claim or comparative speed benchmark.',
        'exact_adaptive_cut_moments_checked': exact_count,
        'exact_fourier_bucket_identities_checked': bucket_count,
        'decoder_trials': trials,
        'total_decoder_observed_symbols': sum(t['observed_symbols'] for t in trials),
        'total_correct_mask_validation_symbols': sum(t['validation_observed_symbols'] for t in trials),
        'total_wrong_mask_validation_symbols': sum(t['wrong_mask_validation_observed_symbols'] for t in trials),
        'decoder_uses': 'Only reset episodes, d, beta and delta; no target-state tables.',
    }
    output = Path(__file__).with_name('acquisition_attack_check.json')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'decoder_trials'}, indent=2))


if __name__ == '__main__':
    run()

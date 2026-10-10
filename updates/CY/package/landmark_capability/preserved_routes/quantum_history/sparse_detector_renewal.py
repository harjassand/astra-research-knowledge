#!/usr/bin/env python3
"""Exact matrix-valued renewal for sparse monitored targets on a hypercube.

The free one-step unitary is u^{tensor n}, u=(3 I-4 i X)/5. After each step,
P measures whether the position is in a supplied set of k basis strings.
This program computes first-detection probabilities from k-by-k free kernels
without making a 2^n state. Small cases are checked against direct evolution.
The construction is a scoped candidate, not a new-prior-art claim.
"""

from dataclasses import dataclass
from fractions import Fraction
import json
import math
import sys
import time


@dataclass(frozen=True)
class G:
    re: Fraction = Fraction(0)
    im: Fraction = Fraction(0)

    def __add__(self, other):
        return G(self.re + other.re, self.im + other.im)

    def __sub__(self, other):
        return G(self.re - other.re, self.im - other.im)

    def __mul__(self, other):
        return G(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    def __pow__(self, exponent):
        result = ONE
        base = self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent >>= 1
        return result

    def abs2(self):
        return self.re * self.re + self.im * self.im


ZERO = G()
ONE = G(Fraction(1))
A = G(Fraction(3, 5))
B = G(Fraction(0), Fraction(-4, 5))


def free_coefficients(horizon):
    """u^t=a_t I+b_t X for t=0,...,horizon."""
    result = [(ONE, ZERO)]
    for _ in range(horizon):
        a, b = result[-1]
        result.append((A * a + B * b, B * a + A * b))
    return result


def free_kernel(n, x, y, coeff):
    a, b = coeff
    hamming = (x ^ y).bit_count()
    return (a ** (n - hamming)) * (b ** hamming)


def renewal(n, start, targets, horizon):
    coeffs = free_coefficients(horizon)
    k = len(targets)
    start_distances = [(a ^ start).bit_count() for a in targets]
    target_distances = [[(a ^ b).bit_count() for b in targets]
                        for a in targets]
    distances = set(start_distances)
    distances.update(h for row in target_distances for h in row)
    kernels = [None]
    for t in range(1, horizon + 1):
        a, b = coeffs[t]
        a_powers, b_powers = [ONE], [ONE]
        for _ in range(n):
            a_powers.append(a_powers[-1] * a)
            b_powers.append(b_powers[-1] * b)
        kernels.append({h: a_powers[n - h] * b_powers[h]
                        for h in distances})
    detected = [[ZERO] * k for _ in range(horizon + 1)]
    probabilities = []
    for t in range(1, horizon + 1):
        for a in range(k):
            amplitude = kernels[t][start_distances[a]]
            for s in range(1, t):
                for b in range(k):
                    amplitude = amplitude - (
                        kernels[t - s][target_distances[a][b]] * detected[s][b]
                    )
            detected[t][a] = amplitude
        probabilities.append(sum((z.abs2() for z in detected[t]), Fraction()))
    return detected[1:], probabilities


def direct(n, start, targets, horizon):
    d = 1 << n
    state = [ZERO] * d
    state[start] = ONE
    target_set = set(targets)
    detected = []
    probabilities = []
    for _ in range(horizon):
        for wire in range(n):
            next_state = list(state)
            for x in range(d):
                if x & (1 << wire):
                    continue
                y = x | (1 << wire)
                next_state[x] = A * state[x] + B * state[y]
                next_state[y] = B * state[x] + A * state[y]
            state = next_state
        layer = [state[target] for target in targets]
        detected.append(layer)
        probabilities.append(sum((z.abs2() for z in layer), Fraction()))
        for target in target_set:
            state[target] = ZERO
    return detected, probabilities


def check_fixture(n, start, targets, horizon):
    boundary_amp, boundary_p = renewal(n, start, targets, horizon)
    direct_amp, direct_p = direct(n, start, targets, horizon)
    assert boundary_amp == direct_amp
    assert boundary_p == direct_p
    return {
        "n": n,
        "start": start,
        "targets": targets,
        "horizon": horizon,
        "hilbert_dimension": 1 << n,
        "boundary_dimension": len(targets),
        "first_detection_probabilities": [str(p) for p in boundary_p],
        "cumulative_detection_probability": str(sum(boundary_p, Fraction())),
        "exact_agreement_with_dense": True,
    }


if __name__ == "__main__":
    if sys.argv[1:] == ["--benchmark"]:
        n, horizon = 100, 20
        targets = [
            (1 << 50) - 1,
            ((1 << 50) - 1) << 50,
            ((1 << 25) - 1) | (((1 << 25) - 1) << 50),
        ]
        start_time = time.perf_counter()
        _, probabilities = renewal(n, 0, targets, horizon)
        elapsed = time.perf_counter() - start_time
        cumulative = sum(probabilities, Fraction())
        print(json.dumps({
            "n": n,
            "k": len(targets),
            "horizon": horizon,
            "all_target_hamming_distances": [a.bit_count() for a in targets],
            "elapsed_seconds_local_observation": round(elapsed, 6),
            "first_probability_log10": round(math.log10(float(probabilities[0])), 3),
            "cumulative_probability_log10": round(math.log10(float(cumulative)), 3),
            "cumulative_exact_numerator_bits": cumulative.numerator.bit_length(),
            "cumulative_exact_denominator_bits": cumulative.denominator.bit_length(),
        }, indent=2))
    else:
        cases = [
            (3, 0, [3, 7], 5),
            (4, 0, [3, 10, 15], 5),
            (6, 0, [7, 19, 55], 5),
        ]
        print(json.dumps([check_fixture(*case) for case in cases], indent=2))

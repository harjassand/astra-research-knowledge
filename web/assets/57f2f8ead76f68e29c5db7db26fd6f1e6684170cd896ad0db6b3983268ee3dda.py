#!/usr/bin/env python3
"""Owned finite-bit sampler with exact integer thresholds and rational rays.

The small demonstrations use a seeded PRNG only to make their transcripts
replayable. The sampling-law theorem assumes the bit source supplies unbiased
independent bits. No quantum preparation or large-N state construction occurs.
"""
from fractions import Fraction as F
import json
import math
import pathlib
import random
import time

ROOT = pathlib.Path(__file__).resolve().parent

class Bits:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.used = 0
    def take(self, count):
        self.used += count
        return self.rng.getrandbits(count)
    def below(self, n):
        assert n >= 1
        if n == 1:
            return 0
        width = (n-1).bit_length()
        while True:
            x = self.take(width)
            if x < n:
                return x

def dyadic_precision(tolerance):
    n = 0
    while F(1, 1 << n) > tolerance:
        n += 1
    return n

def sqrt_down(x, tolerance):
    assert 0 <= x <= 1
    width = dyadic_precision(tolerance)
    integer = math.isqrt((x.numerator << (2*width)) // x.denominator)
    return F(integer, 1 << width), width

def certified_pi(tolerance):
    # Machin identity, with alternating-series bound <=20/5^(2m+1).
    terms = 1
    while F(20, 5**(2*terms+1)) > tolerance:
        terms += 1
    def atan_inverse(base):
        return sum((F((-1)**k, (2*k+1)*base**(2*k+1)) for k in range(terms)), F(0))
    value = 16*atan_inverse(5)-4*atan_inverse(239)
    return value, F(20, 5**(2*terms+1)), terms

def certified_phase(theta, tolerance):
    assert 0 <= theta <= 8
    order, remainder = 0, F(8)
    while remainder > tolerance:
        order += 1
        remainder *= F(8, order+1)
    real, imag, term = F(0), F(0), F(1)
    for degree in range(order+1):
        if degree:
            term *= theta/degree
        if degree % 4 == 0:
            real += term
        elif degree % 4 == 1:
            imag += term
        elif degree % 4 == 2:
            real -= term
        else:
            imag -= term
    return real, imag, remainder, order

def local_rational_ray(x, q, n, epsilon):
    tau = epsilon/(32*n)
    delta = tau/16
    a = 1-(1-q)*x
    amp0, width0 = sqrt_down((1-x)/a, delta)
    amp1, width1 = sqrt_down(q*x/a, delta)
    def at_phase_index(phase_index, phase_size):
        pi, pi_error, pi_terms = certified_pi(delta/4)
        theta = 2*pi*phase_index/phase_size
        real, imag, phase_error, phase_order = certified_phase(theta, delta)
        z0, zr, zi = amp0, amp1*real, amp1*imag
        norm2 = z0*z0+zr*zr+zi*zi
        assert norm2 > 0
        p00 = z0*z0/norm2
        p01r = z0*zr/norm2
        p01i = -z0*zi/norm2
        p11 = (zr*zr+zi*zi)/norm2
        assert p00+p11 == 1
        assert p00*p11-p01r*p01r-p01i*p01i == 0
        assert p00 >= 0 and p11 >= 0
        # Euclidean vector error <=5*delta <tau; all errors are certified.
        assert 2*pi_error+phase_error <= F(3, 2)*delta
        return {
            "vector": [[str(z0), "0"], [str(zr), str(zi)]],
            "projector": [[[str(p00), "0"], [str(p01r), str(p01i)]],
                          [[str(p01r), str(-p01i)], [str(p11), "0"]]],
            "certificate": {"vector_error_upper": str(5*delta), "target_tau": str(tau),
                            "sqrt_bits": max(width0, width1), "pi_terms": pi_terms,
                            "phase_taylor_degree": phase_order, "rank_one_PSD_trace_one": True},
        }
    return at_phase_index

def sample(n, q, weights, epsilon, bits):
    assert n >= 1 and 0 <= q <= 1 and 0 < epsilon <= 1
    assert len(weights) == n//2+1 and sum(weights) == 1
    assert all(v >= 0 for v in weights)
    denominator = math.lcm(*(v.denominator for v in weights))
    counts = [v.numerator*(denominator//v.denominator) for v in weights]
    choose = bits.below(denominator)
    cumulative, b = 0, 0
    for b, count in enumerate(counts):
        cumulative += count
        if choose < cumulative:
            break
    labels = list(range(n))
    for k in range(n-1, 0, -1):
        j = bits.below(k+1)
        labels[k], labels[j] = labels[j], labels[k]
    pairs = [labels[2*k:2*k+2] for k in range(b)]
    rest = labels[2*b:]
    K = len(rest)
    assert len({v for pair in pairs for v in pair} | set(rest)) == n
    result = {"N": n, "q": str(q), "b": b, "K": K, "singlet_pairs": pairs,
              "rest_labels": rest, "epsilon": str(epsilon),
              "weight_common_denominator_bits": denominator.bit_length()}
    if K == 0 or q == 0:
        result.update({"proposal_trials": 0, "timeout": False,
                       "local_ray": {"vector": [["1", "0"], ["0", "0"]]}})
        return result
    target = (160*n*(n+1)/epsilon)**2
    ell = 0
    while (1 << ell) < target:
        ell += 1
    M = 1 << ell
    S = dyadic_precision(epsilon/(64*(n+1)))
    logarithm_upper = 0
    while (1 << logarithm_upper) < 16/epsilon:
        logarithm_upper += 1
    T = 2*(n+1)*logarithm_upper  # >= the natural-log cap in the proof
    result.update({"grid_bits": ell, "acceptance_threshold_bits": S, "proposal_cap": T})
    for trial in range(1, T+1):
        x_index = bits.take(ell)
        x = F(2*x_index+1, 2*M)
        a = 1-(1-q)*x
        weight = a**K
        count = (weight.numerator << S)//weight.denominator
        if bits.take(S) < count:
            phase_index = bits.take(ell)  # phase can be drawn after acceptance
            ray = local_rational_ray(x, q, n, epsilon)(phase_index, M)
            result.update({"proposal_trials": trial, "timeout": False,
                           "x_index": x_index, "phase_index": phase_index, "local_ray": ray,
                           "largest_power_integer_bits": max(weight.numerator.bit_length(),
                                                            weight.denominator.bit_length())})
            return result
    result.update({"proposal_trials": T, "timeout": True,
                   "local_ray": {"vector": [["1", "0"], ["0", "0"]]}})
    return result

def acquire_gibbs_weights(n, alpha, delta, h, epsilon):
    """Positive dyadic lower sums with a proved l1 error <=epsilon/8."""
    exponents = []
    for b in range(n//2+1):
        j = F(n-2*b, 2)
        db = math.comb(n, b)-(math.comb(n, b-1) if b else 0)
        for r in range(n-2*b+1):
            m = r-j
            exponent = alpha*j*(j+1)/n-delta*m*m/n+h*m
            exponents.append((b, db, exponent))
    L = len(exponents)
    zeta = epsilon/(16*L*(1 << n))
    R = dyadic_precision(zeta)
    precision = dyadic_precision(zeta/2)
    order, remainder = 0, F(R)
    while remainder > zeta/4:
        order += 1
        remainder *= F(R, order+1)
    largest = max(v[2] for v in exponents)
    integer_sums = [0]*(n//2+1)
    clipped = 0
    for b, db, exponent in exponents:
        x = exponent-largest
        if x == 0:
            numerator = 1 << precision
        elif x <= -R:
            numerator = 0
            clipped += 1
        else:
            term, series = F(1), F(1)
            for degree in range(1, order+1):
                term *= x/degree
                series += term
            lower = max(F(0), series-remainder)
            numerator = (lower.numerator << precision)//lower.denominator
            assert numerator >= 0
        integer_sums[b] += db*numerator
    total = sum(integer_sums)
    assert total >= 1 << precision
    weights = [F(v, total) for v in integer_sums]
    return weights, {"terms": L, "exponential_taylor_degree": order,
                     "dyadic_bits": precision, "clipped_terms": clipped,
                     "sum_weighted_error_upper": str(L*(1 << n)*zeta),
                     "sector_l1_error_upper": str(2*L*(1 << n)*zeta),
                     "normalized_positive_rational": True}

def main():
    started = time.monotonic()
    epsilon = F(1, 8)
    weights, acquisition = acquire_gibbs_weights(4, F(2), F(-1, 3), F(1, 5), epsilon)
    samples = []
    for n, q, chosen_weights, seed in [
        (4, F(1, 3), weights, 37),
        (4, F(0), [F(5,16), F(9,16), F(2,16)], 38),
        (32, F(1, 3), [F(1,17)]*17, 39),
        (32, F(1), [F(1,17)]*17, 40),
    ]:
        bits = Bits(seed)
        result = sample(n, q, chosen_weights, epsilon, bits)
        result["random_bits_requested"] = bits.used
        samples.append(result)
    output = {"scope": "Four deterministic small sampler transcripts; unbiased-bit theorem is analytic",
              "gibbs_N4_acquisition": acquisition, "samples": samples,
              "seconds": time.monotonic()-started, "status": "PASS"}
    (ROOT/"charged_qubit_sampler_check.json").write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({"status": output["status"], "seconds": output["seconds"],
                      "sample_sizes": [s["N"] for s in samples],
                      "proposal_trials": [s["proposal_trials"] for s in samples],
                      "random_bits": [s["random_bits_requested"] for s in samples]}))

if __name__ == "__main__":
    main()

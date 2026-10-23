#!/usr/bin/env python3
"""Finite diagnostic for the independently reconstructed commuting reservoir.

This verifies finite identities; it does not certify the asymptotic theorem.
Standard library only. Entry point: python3 work/loglaw_replay.py
"""
from fractions import Fraction
import json
import math


def phase_law(m, start, length):
    weights = []
    for y in range(1 << m):
        weight = Fraction(0)
        for k in range(start, start + length):
            if y & ((1 << k) - 1) == 0:
                weight += Fraction(1, length * (1 << (m-k)))
        weights.append(weight)
    assert sum(weights) == 1
    return weights


def entropy(weights):
    return -sum(float(p) * math.log(float(p)) for p in weights if p)


def posterior_entropy(j, length):
    m = j + length - 1
    result = 0.0
    for t in range(j, m + 1):
        if t < m:
            pt = Fraction(1, length) * (1 - Fraction(1, 1 << (t-j+1)))
        else:
            pt = Fraction(1, length) * (2 - Fraction(1, 1 << (length-1)))
        unnormalized = [Fraction(1, 1 << z) for z in range(t-j+1)]
        norm = sum(unnormalized)
        posterior = [p/norm for p in unnormalized]
        result += float(pt) * entropy(posterior)
    return result


def run():
    cases = []
    for j, length in [(1, 1), (1, 4), (2, 4), (3, 6), (4, 7)]:
        m = j + length - 1
        initial = phase_law(m, j, length)
        er = m * math.log(2) - entropy(initial)
        h = posterior_entropy(j, length)
        predicted = (j + (length-1)/2) * math.log(2) - math.log(length) + h
        assert abs(er-predicted) < 2e-12
        assert -1e-12 <= h <= 2*math.log(2) + 1e-12
        returns = []
        for t in range(1, j+1):
            evolved = phase_law(m, j-t, length)
            half_error = sum(abs(p-q) for p,q in zip(initial,evolved))/2
            assert half_error <= Fraction(t,length)
            er_t = m*math.log(2)-entropy(evolved)
            assert abs(er-er_t-t*math.log(2)) < 2e-12
            returns.append({'use': t, 'half_error_exact': str(half_error),
                            'bound_exact': str(Fraction(t,length))})
        cases.append({'J':j,'L':length,'M':m,'E_R_nats':er,
                      'conditional_entropy_nats':h,'returns':returns})
    print(json.dumps({'status':'passed_finite_diagnostics',
                      'proof_status':'finite checks do not certify universal law',
                      'cases':cases}, indent=2))


if __name__ == '__main__':
    run()

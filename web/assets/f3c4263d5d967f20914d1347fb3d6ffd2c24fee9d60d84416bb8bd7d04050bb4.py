"""Finite diagnostics for the PCP/operator scout; proofs are in the report."""
from fractions import Fraction
from itertools import combinations, product
from math import sqrt, cos, sin
from pathlib import Path
import json
import random

OUT = Path(__file__).with_suffix('.json')
rng = random.Random(10072026)

# Exact sharpness: a uniformly chosen r-subset detects any nonzero string,
# and its smallest rejection is r/t, attained at every singleton.
sharp = []
for t in range(1, 10):
    for r in range(1, t + 1):
        subsets = list(combinations(range(t), r))
        values = []
        for x in product((0, 1), repeat=t):
            if any(x):
                values.append(Fraction(sum(any(x[i] for i in S) for S in subsets), len(subsets)))
        assert min(values) == Fraction(r, t)
        sharp.append({'t': t, 'r': r, 'c': str(min(values))})

# Noncommuting two-dimensional auxiliaries. Every zero-input local effect
# annihilates |0>; other effects are arbitrary rank-one PSD contractions.
random_cases = 0
for t in range(2, 9):
    for r in range(1, t + 1):
        for trial in range(12):
            terms = []
            for _ in range(17):
                S = tuple(sorted(rng.sample(range(t), rng.randrange(r + 1))))
                values = {}
                for z in product((0, 1), repeat=len(S)):
                    lam = rng.random()
                    angle = 0.0 if not any(z) else rng.random() * 6.283185307179586
                    # v=(sin(angle), cos(angle)); at z=0, v=|1>.
                    a, b = sin(angle), cos(angle)
                    values[z] = (lam * a * a, lam * a * b, lam * b * b)
                terms.append((S, values))
            minima = []
            for i in range(t):
                x = [int(j == i) for j in range(t)]
                a = b = d = 0.0
                for S, values in terms:
                    u, v, w = values[tuple(x[j] for j in S)]
                    a += u / len(terms)
                    b += v / len(terms)
                    d += w / len(terms)
                minima.append((a + d - sqrt((a - d)**2 + 4*b*b)) / 2)
            assert min(minima) <= r / t + 1e-12
            random_cases += 1

# The exact five-qubit projector OR Pauli l1 formula, reconstructed by
# tensoring the coefficient list rather than from the claimed formula.
pauli = []
for k in range(1, 6):
    base = [Fraction(2**k - 1, 2**k)] + [-Fraction(1, 2**k)] * (2**k - 1)
    coeffs = [Fraction(1)]
    for t in range(1, 4):
        coeffs = [a*b for a in coeffs for b in base]
        h = [-c for c in coeffs]
        h[0] += 1
        exact = sum(abs(c) for c in h)
        formula = 1 + (2 - Fraction(1, 2**(k-1)))**t - 2*(1 - Fraction(1, 2**k))**t
        assert exact == formula
        pauli.append({'k': k, 't': t, 'pauli_l1': str(exact)})

# Erasure exponent optimization: f(q)=(1-q)q^6/2, derivative zero at 6/7.
qopt = Fraction(6, 7)
fopt = (1 - qopt) * qopt**6 / 2
fhalf = Fraction(1, 256)
fwire = (1 - Fraction(7, 8)) * Fraction(7, 8)**6 / 2
assert fopt > fwire > fhalf

result = {
    'scope': 'Finite implementation checks only; no formal or external proof validation.',
    'sharp_subset_cases': len(sharp),
    'sharp_subset_data': sharp,
    'noncommuting_auxiliary_cases': random_cases,
    'pauli_exact_cases': len(pauli),
    'pauli_data': pauli,
    'optimal_erasure_survival': str(qopt),
    'optimal_rate_factor': str(fopt),
    'gain_over_half_erasure': float(fopt/fhalf),
    'three_bit_wrapper_gain': float(fwire/fhalf),
    'three_bit_ratio_to_optimum': float(fwire/fopt),
}
OUT.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if not k.endswith('_data')}, indent=2))

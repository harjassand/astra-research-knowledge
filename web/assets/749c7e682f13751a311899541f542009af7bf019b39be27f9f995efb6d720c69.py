"""Small exact-interface checks for the deterministic symmetric compiler.

This is a classical amplitude emulator, not a gate-level or hardware run.
The large-qutrit scores use Python integers; random matrix checks use float64.
"""
import itertools
import json
import math
from pathlib import Path

import numpy as np


def types(n, d):
    if d == 1:
        yield (n,)
    else:
        for first in range(n + 1):
            for rest in types(n - first, d - 1):
                yield (first,) + rest


def tensor_power(a, n):
    out = np.ones((1, 1), complex)
    for _ in range(n):
        out = np.kron(out, a)
    return out


def occupations(word, d):
    return tuple(word.count(j) for j in range(d))


def dicke(k):
    d, n = len(k), sum(k)
    out = np.zeros(d ** n, complex)
    multiplicity = math.factorial(n) // math.prod(math.factorial(x) for x in k)
    for i, word in enumerate(itertools.product(range(d), repeat=n)):
        if occupations(word, d) == k:
            out[i] = 1 / math.sqrt(multiplicity)
    return out


def occupation_coefficients(b, k):
    d = len(k)
    coeffs = {(0,) * d: 1 + 0j}
    for column in range(d):
        for _ in range(k[column]):
            nxt = {}
            for count, weight in coeffs.items():
                # Structural zeros remain exact, not angle-rounded.
                for row in range(column + 1):
                    if b[row, column] == 0:
                        continue
                    new = list(count)
                    new[row] += 1
                    new = tuple(new)
                    nxt[new] = nxt.get(new, 0j) + weight * b[row, column]
            coeffs = nxt
    denominator = math.prod(math.factorial(x) for x in k)
    return {ell: z * math.sqrt(math.prod(math.factorial(x) for x in ell) / denominator)
            for ell, z in coeffs.items()}


def sequential_expand(k, angle_bits=None):
    """Amplitude emulator of coherent sampling without replacement.

    Each step splits only categories whose remaining count is positive.
    Approximate rotations therefore cannot create an invalid occupation.
    """
    d, n = len(k), sum(k)
    out = np.zeros(d ** n, complex)

    def visit(word, left, amplitude):
        m = sum(left)
        if m == 0:
            index = 0
            for a in word:
                index = index * d + a
            out[index] = amplitude
            return
        active = [a for a in range(d) if left[a] > 0]
        remainder = amplitude
        remaining_mass = m
        for index, a in enumerate(active):
            if index == len(active) - 1:
                factor = remainder
            else:
                angle = math.asin(math.sqrt(left[a] / remaining_mass))
                if angle_bits is not None:
                    scale = 2 ** angle_bits
                    angle = round(angle * scale) / scale
                factor = remainder * math.sin(angle)
                remainder *= math.cos(angle)
            nxt = list(left)
            nxt[a] -= 1
            visit(word + (a,), tuple(nxt), factor)
            remaining_mass -= left[a]

    visit((), k, 1)
    return out


def score_qutrit(r, i):
    return 2 ** (r - i) * sum(math.comb(i, t) * math.comb(r - i, i - t) * 3 ** t
                             for t in range(max(0, 2 * i - r), i + 1))


rng = np.random.default_rng(20261007)
compressed_count = coefficient_count = expansion_count = support_count = 0
max_compressed_error = max_coefficient_error = max_expansion_error = 0.0
for d in (2, 3, 4):
    for fixture in range(8):
        x = rng.normal(size=(d - 1, d - 1)) + 1j * rng.normal(size=(d - 1, d - 1))
        eplus = x.conj().T @ x + 0.4 * np.eye(d - 1)
        eplus = eplus / (1.2 * np.linalg.eigvalsh(eplus)[-1])
        e = np.zeros((d, d), complex)
        e[0, 0] = 1
        e[1:, 1:] = eplus
        t = np.linalg.cholesky(e).conj().T
        b = np.linalg.inv(t)
        h = tuple(range(d))
        for n in (1, 2, 3):
            en = tensor_power(e, n)
            bn = tensor_power(b, n)
            words = list(itertools.product(range(d), repeat=n))
            energy = np.array([sum(h[a] for a in word) for word in words])
            for q in range(n * (d - 1) + 1):
                legal = np.flatnonzero(energy <= q)
                compressed = en[np.ix_(legal, legal)]
                minimum = np.linalg.eigvalsh(compressed)[0]
                inverse_norm = np.linalg.norm(bn[:, legal], 2) ** -2
                max_compressed_error = max(max_compressed_error, abs(minimum - inverse_norm))
                assert abs(minimum - inverse_norm) < 2e-12
                compressed_count += 1
            for k in types(n, d):
                coefficients = occupation_coefficients(b, k)
                via_polynomial = sum((a * dicke(ell) for ell, a in coefficients.items()),
                                     np.zeros(d ** n, complex))
                dense = bn @ dicke(k)
                error = np.linalg.norm(via_polynomial - dense)
                max_coefficient_error = max(max_coefficient_error, error)
                assert error < 2e-10
                coefficient_count += 1
                q = sum(k[a] * h[a] for a in range(d))
                illegal = np.flatnonzero(energy > q)
                assert np.count_nonzero(via_polynomial[illegal]) == 0
                norm2 = float(np.vdot(dense, dense).real)
                chi = dense / math.sqrt(norm2)
                miss = float(np.vdot(chi, en @ chi).real)
                assert abs(miss - 1 / norm2) < 2e-12
                support_count += 1
                exact_expansion = sequential_expand(k)
                max_expansion_error = max(max_expansion_error, np.linalg.norm(exact_expansion - dicke(k)))
                assert np.linalg.norm(exact_expansion - dicke(k)) < 1e-12
                rounded_expansion = sequential_expand(k, angle_bits=8)
                assert abs(np.linalg.norm(rounded_expansion) - 1) < 1e-12
                for index, word in enumerate(words):
                    if occupations(word, d) != k:
                        assert rounded_expansion[index] == 0
                expansion_count += 1

ep = np.array([[0.5, math.sqrt(2) / 4], [math.sqrt(2) / 4, 0.75]])
bp = np.array([[math.sqrt(2), -1], [0, math.sqrt(2)]])
qutrit_count = 0
for r in range(1, 9):
    bn = tensor_power(bp, r)
    for i in range(r + 1):
        vec = bn @ dicke((r - i, i))
        formula = np.zeros(2 ** r, complex)
        for j in range(i + 1):
            a = (-1) ** j * math.comb(i, j) * 2 ** (-(i - j) / 2) / math.sqrt(math.comb(r, j))
            formula += a * dicke((r - j, j))
        # Compare rays; an overall factor and phase are irrelevant.
        formula /= np.linalg.norm(formula)
        vec /= np.linalg.norm(vec)
        overlap = abs(np.vdot(formula, vec))
        assert abs(overlap - 1) < 2e-12
        norm2 = np.linalg.norm(bn @ dicke((r - i, i))) ** 2
        assert abs(norm2 - score_qutrit(r, i)) / max(1, norm2) < 2e-12
        qutrit_count += 1

s = math.log((1 + math.sqrt(17)) / 2)
rows = []
for q in (10, 20, 50, 100, 200, 500):
    candidates = [(score_qutrit(r, q - r), r, q - r)
                  for r in range((q + 1) // 2, q + 1)]
    score, r, i = max(candidates)
    rows.append(dict(Q=q, uses=r, high_count=i, score_bits=score.bit_length(),
                     exponent_per_energy=math.log(score) / q,
                     exponent_deficit=s * q - math.log(score),
                     crude_required_angle_bits=score.bit_length() + math.ceil(math.log2(2 * r * r)) + 3))

# Same E,H, different finite-false-alarm behavior: coherent measure/prepare.
e = np.eye(3)
e[1:, 1:] = ep
values, vectors = np.linalg.eigh(e)
projected_effect = np.zeros((3, 3), complex)
for lam, eigenvector in zip(values, vectors.T):
    psi = np.array([math.sqrt(max(0, lam)), math.sqrt(max(0, 1 - lam))])
    kraus = np.outer(psi, eigenvector.conj())
    projected_effect += kraus.conj().T @ np.diag([1, 0]) @ kraus
assert np.linalg.norm(projected_effect - e) < 1e-12
psi = np.array([0.5, math.sqrt(3) / 2])
alternative = np.kron(np.kron(psi, psi), psi)
vacuum = np.zeros(8)
vacuum[0] = 1
accept_null = np.eye(8) - np.outer(alternative, alternative)
fa = 1 - float(vacuum @ accept_null @ vacuum)
miss = float(alternative @ accept_null @ alternative)
assert abs(fa - 1 / 64) < 1e-12
assert abs(miss) < 1e-12

result = {
    "scope": "Classical polynomial coefficient and count-expansion emulator; no hardware or gate-level synthesis.",
    "compressed_identities": compressed_count,
    "coefficient_identities": coefficient_count,
    "exact_and_rounded_expansions": expansion_count,
    "hard_support_and_miss_checks": support_count,
    "qutrit_amplitude_score_checks": qutrit_count,
    "max_compressed_error": max_compressed_error,
    "max_coefficient_error": max_coefficient_error,
    "max_exact_expansion_error": max_expansion_error,
    "qutrit_integer_scores": rows,
    "finite_FA_same_effect": {"hard_Q": 6, "uses": 3, "coherent_FA": fa,
                               "coherent_miss": miss,
                               "binary_miss_lower_bound": (63 / 64) * math.exp(-6 * s)},
}
out = Path(__file__).with_name("energy_detection_checks.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))

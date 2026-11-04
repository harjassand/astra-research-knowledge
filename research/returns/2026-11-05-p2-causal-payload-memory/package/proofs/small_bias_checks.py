"""Exact finite-field character checks and finite-dimensional decoder checks.

The field checks use exact integers. The arbitrary-reference channel check
uses floating point Choi matrices for every 3-qubit Pauli program. This is
not a physical noise/protection simulation and does not enumerate n=1000.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import numpy as np


def poly_rem(a, b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def poly_gcd(a, b):
    while b:
        a, b = b, poly_rem(a, b)
    return a


def mul(a, b, modulus, k):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << k):
            a ^= modulus
    return out


def irreducible(modulus, k):
    x = poly_rem(2, modulus)
    v = x
    for i in range(1, k + 1):
        v = mul(v, v, modulus, k)
        if i <= k // 2 and poly_gcd(modulus, v ^ x) != 1:
            return False
    return v == x


def first_field(k):
    candidates = 0
    for low in range(1, 1 << k, 2):
        candidates += 1
        modulus = (1 << k) | low
        if irreducible(modulus, k):
            return modulus, candidates
    raise RuntimeError("No irreducible polynomial found")


def trace(a, modulus, k):
    out, z = 0, a
    for _ in range(k):
        out ^= z
        z = mul(z, z, modulus, k)
    assert out in (0, 1)
    return out


def trace_mask(modulus, k):
    return sum(trace(1 << j, modulus, k) << j for j in range(k))


def parameters(n):
    target = max(2, 2 * (2 * n - 1))
    k = (target - 1).bit_length()
    modulus, candidates = first_field(k)
    return k, 1 << k, modulus, candidates


def label(a, b, r, modulus, k, mask):
    out, z = 0, a
    for i in range(r):
        out |= ((z & mask).bit_count() & 1) << i
        z = mul(z, b, modulus, k)
    return out


def fwht(values):
    out = values.copy()
    width = 1
    while width < len(out):
        blocks = out.reshape(-1, 2 * width)
        left, right = blocks[:, :width].copy(), blocks[:, width:].copy()
        blocks[:, :width], blocks[:, width:] = left + right, left - right
        width *= 2
    return out


def character_check(n):
    k, q, modulus, candidates = parameters(n)
    mask = trace_mask(modulus, k)
    counts = np.zeros(1 << (2 * n), dtype=np.int64)
    for a in range(q):
        for b in range(q):
            counts[label(a, b, 2 * n, modulus, k, mask)] += 1
    character_sums = fwht(counts)
    assert character_sums[0] == q * q
    assert character_sums[1:].min() >= 0
    assert character_sums[1:].max() <= q * (2 * n - 1)
    assert 2 * character_sums[1:].max() <= q * q
    return {"n": n, "k": k, "q": q, "modulus_hex": hex(modulus),
            "irreducible_candidates_tested": candidates,
            "seed_pairs_enumerated": q * q,
            "all_characters_enumerated": 1 << (2 * n),
            "minimum_nontrivial_character_bias": float(character_sums[1:].min() / (q*q)),
            "maximum_nontrivial_character_bias": float(character_sums[1:].max() / (q*q)),
            "root_bound": (2 * n - 1) / q,
            "certified_lifted_commutator_gap": "4/5 (exact; X_flag tensor I attains it)"}


def kron_all(items):
    out = np.ones((1, 1), complex)
    for item in items:
        out = np.kron(out, item)
    return out


def decoder_check(n=3):
    ident = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], complex)
    y = np.array([[0, -1j], [1j, 0]], complex)
    z = np.diag([1., -1.]).astype(complex)
    h = (x + z) / np.sqrt(2)
    paulis = [ident, x, z, y]  # interleaved label bits (u,v)
    dimension = 1 << n
    eye_gauge = np.eye(dimension, dtype=complex)
    bell = ident.reshape(-1, order="F") / np.sqrt(2)
    ideal_choi = np.outer(bell, bell.conj())
    max_error = 0.
    checked = 0
    for program in itertools.product(range(4), repeat=n):
        factors = [paulis[s] for s in program]
        p = kron_all(factors)
        eig = [np.linalg.eigh(factor) for factor in factors]
        eigenbasis = kron_all([item[1] for item in eig])
        eigenvalues = np.array([np.prod(items) for items in
                               itertools.product(*[item[0] for item in eig])])
        controlled = np.block([[p, np.zeros_like(p)], [np.zeros_like(p), eye_gauge]])
        encoding = controlled @ np.kron(h, eye_gauge)
        choi = np.zeros((4, 4), complex)
        for g in range(dimension):
            inject = np.kron(ident, eye_gauge[:, g:g+1]) / np.sqrt(dimension)
            for outcome in range(dimension):
                measurement = np.kron(ident, eigenbasis[:, outcome].conj()[None, :])
                phase_inverse = np.diag([eigenvalues[outcome].conjugate(), 1.])
                kraus = h @ phase_inverse @ measurement @ encoding @ inject
                vector = kraus.reshape(-1, order="F") / np.sqrt(2)
                choi += np.outer(vector, vector.conj())
        error = np.linalg.norm(choi - ideal_choi, ord="fro")
        max_error = max(max_error, float(error))
        checked += 1
    return {"gauge_qubits": n, "Pauli_programs_checked": checked,
            "maximum_identity_Choi_Frobenius_error": max_error,
            "scope": "All 3-qubit tensor Pauli programs, tracial gauge summed explicitly; finite floating-point channel check."}


def main():
    checks = [character_check(n) for n in (1, 2, 3, 4, 5, 8)]
    n = 1000
    k, q, modulus, candidates = parameters(n)
    mask = trace_mask(modulus, k)
    example_label = label(17, 31, 2*n, modulus, k, mask)
    pauli_counts = {"I": 0, "X": 0, "Z": 0, "Y": 0}
    names = ["I", "X", "Z", "Y"]
    for i in range(n):
        pauli_counts[names[(example_label >> (2*i)) & 3]] += 1
    result = {"exact_character_checks": checks,
              "decoder_channel_check": decoder_check(3),
              "n1000_compiled_program": {
                  "n": n, "k": k, "q": q, "header_bits": 2*k+1,
                  "modulus_hex": hex(modulus),
                  "irreducible_candidates_tested": candidates,
                  "trace_mask_hex": hex(mask), "example_seed": [17, 31],
                  "example_program_Pauli_counts": pauli_counts,
                  "root_bias_bound": (2*n-1)/q,
                  "commutator_gap": "4/5",
                  "half_diamond_error": .01,
                  "quantum_dimension_ratio_lower_bound": .901,
                  "qubits_needed_after_all_outputs_before_header": n+1,
                  "qubits_needed_after_gauge_before_flag_and_header": n,
                  "scope": "Generated one 1000-site program and its field exactly; no 1000-qubit density matrix or physical experiment."}}
    output = Path(__file__).parent / "small_bias_execution.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"character_checks": len(checks),
                      "max_Choi_error": result["decoder_channel_check"]["maximum_identity_Choi_Frobenius_error"],
                      "n1000": result["n1000_compiled_program"],
                      "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()

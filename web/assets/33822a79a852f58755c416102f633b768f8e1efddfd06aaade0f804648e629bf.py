"""Owned bounded exact fixtures for the spin projection posterior compiler.

No peer imports, network, numerical solvers or scientific dependencies.
Writes only a JSON receipt beside this script. All arithmetic is exact.
The fixture checks transcription; the text proof supplies all-N claims.
"""
from collections import defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import time


ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))


def gauss_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gauss_mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gauss_scale(a, s):
    return (a[0] * s, a[1] * s)


def gauss_pow(a, n):
    out = ONE
    for _ in range(n):
        out = gauss_mul(out, a)
    return out


def gauss_abs2(a):
    return a[0] * a[0] + a[1] * a[1]


def z_formula(m, r, b, x):
    return sum(
        (Q(comb(r, t) ** 2, comb(m, b + t)) * x ** t * (1 - x) ** (r - t)
         for t in range(r + 1)), Q(0)
    )


def arrangement_count(m, r, b):
    return comb(m, r) * comb(m - r, b)


@lru_cache(maxsize=None)
def direct_local(pattern, amp0, amp1, phase):
    """Enumerate every bit string and its original product amplitude.

    Symbol C is coherent, O computational one, Z computational zero.
    The returned Dicke-sum overlap numerators still need 1/sqrt(C(m,l)).
    This avoids irrational arithmetic without replacing the projection.
    """
    m = len(pattern)
    sums = [ZERO for _ in range(m + 1)]
    for bits in product((0, 1), repeat=m):
        amplitude = ONE
        for symbol, bit in zip(pattern, bits):
            if symbol == "C":
                local = (amp0, Q(0)) if bit == 0 else gauss_scale(phase, amp1)
            elif symbol == "O":
                local = ONE if bit == 1 else ZERO
            elif symbol == "Z":
                local = ONE if bit == 0 else ZERO
            else:
                raise AssertionError(symbol)
            amplitude = gauss_mul(amplitude, local)
        l = sum(bits)
        sums[l] = gauss_add(sums[l], amplitude)
    norm = sum((gauss_abs2(a) / comb(m, l) for l, a in enumerate(sums)), Q(0))
    return tuple(sums), norm


def dp_tables(blocks, x):
    tables = [{(0, 0): Q(1)}]
    for m in blocks:
        nxt = defaultdict(Q)
        for (k, u), old in tables[-1].items():
            for r in range(m + 1):
                for b in range(m - r + 1):
                    nxt[(k + r, u + b)] += (
                        old * arrangement_count(m, r, b) * z_formula(m, r, b, x)
                    )
        tables.append(dict(nxt))
    return tables


def split_assignment(blocks, assignment):
    out = []
    offset = 0
    for m in blocks:
        out.append(assignment[offset:offset + m])
        offset += m
    assert offset == len(assignment)
    return out


def exact_ensemble_checks(blocks, amp0, amp1, phase, stats):
    assert amp0 ** 2 + amp1 ** 2 == 1
    x = amp1 ** 2
    M = sum(blocks)
    tables = dp_tables(blocks, x)
    enumeration_totals = defaultdict(Q)
    enumeration_profiles = defaultdict(Q)
    enumeration_counts = defaultdict(int)

    # Explicit ALL uniform ternary arrangements, once, with no count formula.
    for assignment in product(("C", "O", "Z"), repeat=M):
        patterns = split_assignment(blocks, assignment)
        k, u = assignment.count("C"), assignment.count("O")
        profile = tuple((p.count("C"), p.count("O")) for p in patterns)
        raw_mass = Q(1)
        for pattern in patterns:
            _, direct_norm = direct_local(tuple(pattern), amp0, amp1, phase)
            raw_mass *= direct_norm
        enumeration_totals[(k, u)] += raw_mass
        enumeration_profiles[profile] += raw_mass
        enumeration_counts[profile] += 1
        stats["ternary_assignments_enumerated"] += 1

    assert set(tables[-1]) == set(enumeration_totals)
    for (k, u), mass in enumeration_totals.items():
        H = comb(M, k) * comb(M - k, u)
        assert tables[-1][(k, u)] == mass
        success = mass / H
        assert Q(1, 2 ** M) <= success <= 1
        stats["terminal_mass_equalities"] += 1

    for profile, direct_mass in enumeration_profiles.items():
        formula_mass = Q(1)
        formula_count = 1
        k = u = 0
        for m, (r, b) in zip(blocks, profile):
            k += r
            u += b
            c = arrangement_count(m, r, b)
            formula_count *= c
            formula_mass *= c * z_formula(m, r, b, x)
        assert enumeration_counts[profile] == formula_count
        assert direct_mass == formula_mass

        # Multiplication of every exact backward transition must telescope.
        posterior = Q(1)
        remain_k, remain_u = k, u
        for i in range(len(blocks), 0, -1):
            m = blocks[i - 1]
            r, b = profile[i - 1]
            numerator = (
                arrangement_count(m, r, b) * z_formula(m, r, b, x)
                * tables[i - 1].get((remain_k - r, remain_u - b), Q(0))
            )
            denominator = tables[i][(remain_k, remain_u)]
            assert denominator > 0
            posterior *= numerator / denominator
            remain_k -= r
            remain_u -= b
        assert (remain_k, remain_u) == (0, 0)
        assert posterior == direct_mass / tables[-1][(k, u)]
        stats["profile_count_and_posterior_equalities"] += 1

    for i, m in enumerate(blocks, 1):
        for (k, u), denominator in tables[i].items():
            transition_sum = Q(0)
            for r in range(m + 1):
                for b in range(m - r + 1):
                    transition_sum += (
                        arrangement_count(m, r, b) * z_formula(m, r, b, x)
                        * tables[i - 1].get((k - r, u - b), Q(0)) / denominator
                    )
            assert transition_sum == 1
            stats["transition_normalization_equalities"] += 1

    return {
        "blocks": list(blocks), "M": M, "x": str(x),
        "phase": [str(phase[0]), str(phase[1])],
        "minimum_label_success": str(min(
            mass / (comb(M, k) * comb(M - k, u))
            for (k, u), mass in tables[-1].items()
        )),
        "labels_checked": len(tables[-1]),
        "count_profiles_checked": len(enumeration_profiles),
    }


def sparse_add(v, w, scale=Q(1)):
    out = dict(v)
    for key, val in w.items():
        out[key] = out.get(key, Q(0)) + scale * val
        if out[key] == 0:
            del out[key]
    return out


def virtual_action(vector, M, kind):
    out = {}
    for word, value in vector.items():
        if kind == "z":
            out = sparse_add(out, {word: Q(M, 2) - word.bit_count()}, value)
        else:
            for site in range(M):
                bit = (word >> site) & 1
                if (kind == "+" and bit == 1) or (kind == "-" and bit == 0):
                    new = word ^ (1 << site)
                    out[new] = out.get(new, Q(0)) + value
    return {key: value for key, value in out.items() if value}


def embedding(blocks, weights):
    """Unnormalized Dicke isometry columns; Gram factors tracked exactly."""
    words = {0: Q(1)}
    offset = 0
    for m, k in zip(blocks, weights):
        local_words = [w for w in range(2 ** m) if w.bit_count() == k]
        words = {old | (w << offset): Q(1) for old in words for w in local_words}
        offset += m
    return words


def physical_action_embedded(blocks, weights, kind):
    if kind == "z":
        eig = sum((Q(m, 2) - k for m, k in zip(blocks, weights)), Q(0))
        return {word: value * eig for word, value in embedding(blocks, weights).items() if eig}
    out = {}
    for i, (m, k) in enumerate(zip(blocks, weights)):
        if kind == "+" and k > 0:
            changed = list(weights)
            changed[i] -= 1
            out = sparse_add(out, embedding(blocks, changed), Q(m - k + 1))
        if kind == "-" and k < m:
            changed = list(weights)
            changed[i] += 1
            out = sparse_add(out, embedding(blocks, changed), Q(k + 1))
    return out


def intertwiner_checks(stats):
    cases = [(1, 2), (2, 2), (1, 1, 2), (3, 2), (0, 2, 1), (0, 0)]
    for blocks in cases:
        M = sum(blocks)
        for weights in product(*(range(m + 1) for m in blocks)):
            column = embedding(blocks, weights)
            gram = sum(value ** 2 for value in column.values())
            assert gram == product_binom(blocks, weights)
            for kind in ("+", "-", "z"):
                assert virtual_action(column, M, kind) == physical_action_embedded(blocks, weights, kind)
                stats["exact_spin_generator_intertwinings"] += 1
            for m, k in zip(blocks, weights):
                if k > 0:
                    assert Q((m - k + 1) ** 2 * comb(m, k - 1), comb(m, k)) == k * (m - k + 1)
                    stats["normalized_ladder_coefficient_checks"] += 1
            stats["exact_embedding_gram_checks"] += 1


def product_binom(blocks, weights):
    out = 1
    for m, k in zip(blocks, weights):
        out *= comb(m, k)
    return out


def common_denominator_check(blocks, x, stats):
    B = x.denominator
    prefix_den = 1
    integer_tables = [{(0, 0): 1}]
    rational_tables = dp_tables(blocks, x)
    max_bits = 0
    for i, m in enumerate(blocks, 1):
        Qi = B ** m
        for l in range(m + 1):
            Qi *= comb(m, l)
        local = {}
        for r in range(m + 1):
            for b in range(m - r + 1):
                v = Qi * arrangement_count(m, r, b) * z_formula(m, r, b, x)
                assert v.denominator == 1
                local[(r, b)] = v.numerator
                stats["integer_local_weight_checks"] += 1
        nxt = defaultdict(int)
        for (k, u), old in integer_tables[-1].items():
            for (r, b), v in local.items():
                nxt[(k + r, u + b)] += old * v
        integer_tables.append(dict(nxt))
        prefix_den *= Qi
        prefix_size = sum(blocks[:i])
        for key, value in nxt.items():
            assert Q(value, prefix_den) == rational_tables[i][key]
            assert value <= 3 ** prefix_size * prefix_den
            max_bits = max(max_bits, value.bit_length(), prefix_den.bit_length())
            stats["integer_dp_equalities"] += 1
    return max_bits


def main():
    start = time.perf_counter()
    stats = defaultdict(int)
    populations = [(Q(1), Q(0)), (Q(4, 5), Q(3, 5)),
                   (Q(3, 5), Q(4, 5)), (Q(0), Q(1))]
    phases = [ONE, (Q(0), Q(1)), (Q(-1), Q(0))]

    # Independent bitstring amplitudes, norm and floor for all tiny blocks.
    for amp0, amp1 in populations:
        x = amp1 ** 2
        for phase in phases:
            for m in range(6):
                for r in range(m + 1):
                    for b in range(m - r + 1):
                        pattern = ("Z",) * (m - r - b) + ("C",) * r + ("O",) * b
                        sums, norm = direct_local(pattern, amp0, amp1, phase)
                        formula = z_formula(m, r, b, x)
                        assert norm == formula
                        assert Q(1, 2 ** m) <= norm <= 1
                        for l in range(m + 1):
                            t = l - b
                            if 0 <= t <= r:
                                coefficient = Q(comb(r, t)) * amp1 ** t * amp0 ** (r - t)
                                expected = gauss_scale(gauss_pow(phase, t), coefficient)
                            else:
                                expected = ZERO
                            assert sums[l] == expected
                            stats["exact_dicke_amplitude_equalities"] += 1
                        stats["local_norm_and_floor_checks"] += 1

    fixtures = []
    block_cases = [(1, 2), (2, 2), (1, 2, 3), (0, 2, 1), (3, 3), (0, 0)]
    max_bits = 0
    for blocks in block_cases:
        for amp0, amp1 in populations:
            max_bits = max(max_bits, common_denominator_check(blocks, amp1 ** 2, stats))
            for phase in phases:
                fixtures.append(exact_ensemble_checks(blocks, amp0, amp1, phase, stats))
    intertwiner_checks(stats)

    # A two-label acquired rational posterior, not just isolated labels.
    blocks = (1, 2, 3)
    M = sum(blocks)
    labels = [(Q(1, 3), 2, 1, Q(9, 25)), (Q(2, 3), 4, 1, Q(16, 25))]
    masses = [dp_tables(blocks, x)[-1][(k, u)] / (comb(M, k) * comb(M - k, u))
              for _, k, u, x in labels]
    S = sum((label[0] * s for label, s in zip(labels, masses)), Q(0))
    posterior = [label[0] * s / S for label, s in zip(labels, masses)]
    assert sum(posterior, Q(0)) == 1 and Q(1, 2 ** M) <= S <= 1
    stats["outer_posterior_normalization_checks"] += 1

    receipt = {
        "worker": "c05_s02", "status": "PASS_EXACT_BOUNDED_TRANSCRIPTION_CHECKS",
        "arithmetic": "Python Fraction and integer; complex Gaussian rationals; no floats",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": time.perf_counter() - start,
        "max_virtual_qubits": 6, "max_local_block_fixture": 5,
        "largest_common_denominator_fixture_bits": max_bits,
        "counts": dict(stats), "ensemble_fixtures": fixtures,
        "two_label_fixture": {"mass": str(S), "posterior": [str(v) for v in posterior]},
        "scope": "Exact local amplitudes/norm/floor; uniform arrangement mass; posterior profile and transition laws; common integer denominators; spin intertwiners.",
        "nonclaims": ["all-N proof from finite checks", "asymptotic runtime benchmark", "full sharp-domain Gibbs front-end execution", "physical hardware", "priority"],
        "file_effects": "This script writes only its own adjacent JSON receipt.",
    }
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({key: receipt[key] for key in
          ("status", "elapsed_seconds", "max_virtual_qubits", "counts")}, indent=2))


if __name__ == "__main__":
    main()

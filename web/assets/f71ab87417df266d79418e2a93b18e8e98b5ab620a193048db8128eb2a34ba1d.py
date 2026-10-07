#!/usr/bin/env python3
"""Independent exact complex-phase and physical-prefix audit of copied code."""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "low_sector_sampler_copied", ROOT / "low_sector_sampler_copied.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
LowSector = mod.LowSector


def zadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def zneg(a):
    return (-a[0], -a[1])


def zmul(a, b):
    return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])


def zabs2(a):
    return a[0]*a[0] + a[1]*a[1]


def perm_sign(p):
    return -1 if sum(p[i] > p[j] for i in range(len(p))
                     for j in range(i+1, len(p))) % 2 else 1


def detz(A):
    n = len(A)
    if n == 0:
        return (Q(1), Q(0))
    total = (Q(0), Q(0))
    for p in permutations(range(n)):
        v = (Q(perm_sign(p)), Q(0))
        for i in range(n):
            v = zmul(v, A[i][p[i]])
        total = zadd(total, v)
    return total


def brute_prefix(F, k, up=(), down=(), empty=()):
    n = len(F)
    up, down, empty = set(up), set(down), set(empty)
    total = Q(0)
    for I in combinations(range(n), k):
        I = set(I)
        if not up <= I or I & (down | empty):
            continue
        for J0 in combinations(range(n), k):
            J = set(J0)
            if I & J or not down <= J or J & (up | empty):
                continue
            if (I | J) & empty:
                continue
            rows, cols = sorted(I), sorted(J)
            value = detz([[F[i][j] for j in cols] for i in rows])
            total += zabs2(value)
    return total


def site_reorder_sign(I, J):
    # Convert canonical up-then-down Fock order to site-interleaved order.
    n = 4
    seq = []
    for i in range(n):
        if i in I:
            seq.append(i)
        if i in J:
            seq.append(n+i)
    # The sign to sort the occupied canonical mode indices.
    inversions = sum(seq[a] > seq[b] for a in range(len(seq))
                     for b in range(a+1, len(seq)))
    return -1 if inversions % 2 else 1


def direct_pair_expansion(F, I, J):
    # Multiply pair creators in increasing row order and sort wedge generators.
    n = len(F)
    I, J = sorted(I), sorted(J)
    total = (Q(0), Q(0))
    for p in permutations(range(len(I))):
        modes = []
        value = (Q(1), Q(0))
        for r, i in enumerate(I):
            j = J[p[r]]
            value = zmul(value, F[i][j])
            modes.extend((i, n+j))
        inversions = sum(modes[a] > modes[b] for a in range(len(modes))
                         for b in range(a+1, len(modes)))
        if inversions % 2:
            value = zneg(value)
        total = zadd(total, value)
    return total


def phase_input(F, I, J):
    det = detz([[F[i][j] for j in sorted(J)] for i in sorted(I)])
    common_pair_order = -1 if (len(I)*(len(I)-1)//2) % 2 else 1
    sign = common_pair_order * site_reorder_sign(I, J)
    return (sign*det[0], sign*det[1])



def phased_skew(G, signs, phased=True):
    n = len(G)
    phases = [((s, 0) if (not phased or i % 2 == 0) else (0, s))
              for i, s in enumerate(signs)]
    A = []
    for i in range(n):
        row = []
        for j in range(n):
            first = mod.mul(phases[i], G[i][j])
            second = mod.mul(phases[j], G[j][i])
            row.append(mod.add(first, (-second[0], -second[1])))
        A.append(row)
    assert all(A[i][j] == (-A[j][i][0], -A[j][i][1])
               for i in range(n) for j in range(n))
    return A


def check_phased_unbiased(F, k):
    solver = LowSector(F)
    target = brute_prefix(F, k) * solver.denominator**(2*k)
    total = 0
    words = 0
    for signs in product((-1, 1), repeat=len(F)):
        x = mod.pfaffian_norm_coefficient(phased_skew(solver.g, signs), k)
        assert x >= 0
        total += x
        words += 1
    assert Q(total, words) == target
    return {"k": k, "sign_words": words, "scaled_target": str(target),
            "mean_matches_target": True}


def check_phase_matched_baselines():
    rows = []
    for k in (1, 2, 3):
        n = 2*k
        G = [[(0, 0) for _ in range(n)] for _ in range(n)]
        for i in range(0, n, 2):
            G[i][i+1] = (1, 0)
            G[i+1][i] = (1, 0)
        target = 2**k
        raw_values, phased_values = [], []
        for signs in product((-1, 1), repeat=n):
            raw = mod.pfaffian_norm_coefficient(phased_skew(G, signs, False), k)
            phased = mod.pfaffian_norm_coefficient(phased_skew(G, signs, True), k)
            assert phased == target
            raw_values.append(raw)
            phased_values.append(phased)
        raw_second = Q(sum(x*x for x in raw_values), len(raw_values)) / (target*target)
        assert raw_second == 2**k
        assert all(x == target for x in phased_values)
        rows.append({"k": k, "target_norm": target,
                     "phased_all_signs_constant": True,
                     "unphased_relative_second_moment": str(raw_second)})
    return rows


def fixture4():
    return [[(Q(i+2*j+1, 17), Q(((-1)**(i+j))*(2*i+j+1), 19))
             for j in range(4)] for i in range(4)]


def run_prefix_suite(F, k):
    n = len(F)
    solver = LowSector(F)
    cases = 0
    free_words = 0
    scale = solver.denominator ** (2*k)
    # All physical prefixes of lengths 0, 1, 2 and 3, in site order.
    for depth in range(n):
        for states in product((0, 1, 2), repeat=depth):
            up = {i for i, state in enumerate(states) if state == 1}
            down = {i for i, state in enumerate(states) if state == 2}
            empty = {i for i, state in enumerate(states) if state == 0}
            mass = brute_prefix(F, k, up, down, empty)
            free = sorted(set(range(n)) - up - down - empty)
            total = 0
            rho = 0
            if len(up) <= k and len(down) <= k:
                rho = mod.comb(2*k-len(up)-len(down), k-len(up))
            for word in product((-1, 1), repeat=len(free)):
                signs = [1] * n
                for site, sign in zip(free, word):
                    signs[site] = sign
                sample = solver.prefix_draw_integer(k, signs, up, down, empty)
                assert sample >= 0
                assert sample <= rho * mass * scale
                if mass == 0:
                    assert sample == 0
                total += sample
            assert Q(total, (1 << len(free))*scale) == mass, (
                k, states, Q(total, (1 << len(free))*scale), mass)
            cases += 1
            free_words += 1 << len(free)
    return {"sector_k": k, "prefixes_checked": cases,
            "exhausted_sign_words": free_words,
            "result": "PASS"}


def check_phase_formula(F):
    n = len(F)
    cases = 0
    for k in range(n//2 + 1):
        for I in combinations(range(n), k):
            for J in combinations(range(n), k):
                if set(I) & set(J):
                    continue
                direct = direct_pair_expansion(F, I, J)
                det = detz([[F[i][j] for j in sorted(J)] for i in sorted(I)])
                canonical_sign = -1 if (k*(k-1)//2) % 2 else 1
                canonical = (canonical_sign*det[0], canonical_sign*det[1])
                claimed = phase_input(F, I, J)
                assert direct == canonical, ("up-down order", k, I, J, direct, canonical)
                site_amp = tuple(site_reorder_sign(I, J)*x for x in direct)
                assert site_amp == claimed, ("site-interleaved order", k, I, J, site_amp, claimed)
                # For every nonzero determinant, max-component scaling keeps
                # the normalization denominator in [1,sqrt(2)].
                alpha = max(abs(claimed[0]), abs(claimed[1]))
                if alpha:
                    scaled_norm2 = zabs2((claimed[0]/alpha, claimed[1]/alpha))
                    assert 1 <= scaled_norm2 <= 2
                cases += 1
    return {"disjoint_amplitudes_checked": cases, "result": "PASS"}


def main():
    F = fixture4()
    prefix = [run_prefix_suite(F, 1), run_prefix_suite(F, 2)]
    phase = check_phase_formula(F)
    phased_unbiased = [check_phased_unbiased(F, k) for k in (1, 2)]
    phase_matched = check_phase_matched_baselines()
    diag = [[(Q(i+1), Q(0)) if i == j else (Q(0), Q(0))
             for j in range(4)] for i in range(4)]
    root_solver = LowSector(F)
    exact_estimate = root_solver.estimate(2, Q(1, 2), Q(1, 2))
    target_norm = brute_prefix(F, 2) 
    assert exact_estimate == target_norm
    legal_samples = 0
    for seed in range(32):
        sample = LowSector(F).born_sample(2, Q(1, 2), random.Random(80400 + seed))
        assert sample['status'] == 'OK'
        I, J = set(sample['I']), set(sample['J'])
        assert len(I) == len(J) == 2 and not (I & J)
        assert zabs2(detz([[F[i][j] for j in sorted(J)] for i in sorted(I)])) > 0
        legal_samples += 1
    zero_solver = LowSector(diag)
    zero_words = 0
    for k in (1, 2):
        for signs in product((-1, 1), repeat=4):
            assert zero_solver.prefix_draw_integer(k, signs) == 0
            zero_words += 1
        assert zero_solver.estimate(k, Q(1, 2), Q(1, 2)) == 0
    out = {
        "status": "PASS",
        "source_copy_sha256": "1aa9cc863942a6ba10acd7af6656a1c134ea895b09e2dc450b8df4bd804cd769",
        "complex_fixture": "dense nonsymmetric 4x4 over Q(i), nonzero diagonal",
        "prefix_suites": prefix,
        "phase_formula": phase,
        "unit_modulus_phase_unbiasedness": phased_unbiased,
        "phase_matched_baseline": phase_matched,
        "complex_root_estimate": str(exact_estimate),
        "complex_root_norm": str(target_norm),
        "legal_complex_born_samples": legal_samples,
        "exact_zero_diagonal_fixture_sign_words": zero_words,
        "scope": "Finite exact audit only; no compiler gate synthesis."
    }
    (ROOT / "complex_audit_checks.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()


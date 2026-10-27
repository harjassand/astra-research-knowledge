#!/usr/bin/env python3
"""Independent focused audit of root's diagonal-completion compiler.

Checks raw acquisition, retained certificates, rejection paths, quadratic
refinement, Z4 Gaussian coefficients, and exact sums at orders 2, 4, and 8.
Finite sums are exhaustive; this does not execute the asymptotic counter.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import sys

from lowrank_sparse_audit_checks import (
    bits, xor, independent, codewords, restrict_column, alternating,
    qvalue, transpose, matmul, error_graph,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'work_mixed_root/diagonal_completion_compiler.py'
sys.path.insert(0, str(SOURCE.parent))
spec = importlib.util.spec_from_file_location('root_diagonal_audit_target', SOURCE)
target = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target)


def q4(A, x):
    diagonal = sum((A[i] >> i & 1)*(x >> i & 1) for i in range(len(A)))
    edges = sum((A[i] >> j & 1)*(x >> i & 1)*(x >> j & 1)
                for i in range(len(A)) for j in range(i))
    return (diagonal+2*edges) % 4


def literal_sum(B, terms, b):
    n, half = len(B), 1 << (b-1)
    answer = [0]*half
    for x in range(1 << n):
        exponent = sum(c for s, c in terms if x & s == s)
        exponent += half*sum((B[i] >> j & 1)*(x >> i & 1)*(x >> j & 1)
                             for i in range(n) for j in range(i))
        residue = exponent % (2*half)
        answer[residue % half] += 1 if residue < half else -1
    return answer


def brute_gauss(K, character):
    answer = [0, 0]
    for x in range(1 << len(K)):
        e = (q4(K, x)+2*((x & character).bit_count() & 1)) % 4
        answer[e % 2] += 1 if e < 2 else -1
    return tuple(answer)


def nullspace(rows, n):
    reduced = list(rows)
    pivots = []
    for column in range(n):
        pivot = next((i for i in range(len(pivots), len(reduced))
                      if reduced[i] >> column & 1), None)
        if pivot is None:
            continue
        position = len(pivots)
        reduced[pivot], reduced[position] = reduced[position], reduced[pivot]
        for i in range(len(reduced)):
            if i != position and reduced[i] >> column & 1:
                reduced[i] ^= reduced[position]
        pivots.append(column)
    basis = []
    for free in range(n):
        if free not in pivots:
            vector = 1 << free
            for i, pivot in enumerate(pivots):
                vector |= (reduced[i] >> free & 1) << pivot
            basis.append(vector)
    assert len(pivots)+len(basis) == n
    assert all(all((row & x).bit_count() % 2 == 0 for row in rows) for x in basis)
    return basis


def replay(B, certificate, radius):
    E = set(certificate['initially_removed'])
    I = certificate['pivots']
    for step in certificate['punctures']:
        R = [i for i in range(len(B)) if i not in E]
        U = independent([restrict_column(B, R, j) for j in I])
        support = set(step['support'])
        assert support <= set(R) and 0 < len(support) <= 2*radius
        word = sum((i in support) << j for j, i in enumerate(R))
        assert len(independent(U+[word])) == len(U)
        assert len(U) == step['rank_before']
        E |= support
        R = [i for i in range(len(B)) if i not in E]
        rank_after = len(independent([restrict_column(B, R, j) for j in I]))
        assert rank_after == step['rank_after'] < step['rank_before']
    assert sorted(E) == certificate['removed']
    R = [i for i in range(len(B)) if i not in E]
    assert R == certificate['retained']
    U = independent([restrict_column(B, R, j) for j in I])
    assert U == certificate['code_generators']
    D, S = certificate['low_rank_matrix'], certificate['sparse_matrix']
    assert target.symmetric(D) and alternating(S)
    raw = [restrict_column(B, R, i) for i in R]
    assert [(d & ~(1 << i)) ^ s for i, (d, s) in enumerate(zip(D, S))] == raw
    assert len(independent(D)) == certificate['low_rank'] <= len(U)
    assert all(len(independent(U+[row])) == len(U) for row in D)
    assert sum(row.bit_count() for row in S)//2 == certificate['residual_edges']
    if 'method' not in certificate:
        minimum = min((word.bit_count() for a, word in codewords(U) if a),
                      default=len(R)+1)
        assert minimum == certificate['minimum_code_distance']
        if U:
            assert minimum > 2*radius
        assert [(d ^ b).bit_count() for d, b in zip(D, raw)] == certificate['decoded_column_distances']
        assert all((d ^ b).bit_count() <= radius for d, b in zip(D, raw))


def witness(D, S, radius):
    H = {i for i, row in enumerate(S) if row.bit_count() >= radius}
    allowed = [i for i in range(len(D)) if i not in H]
    columns, I = [], []
    for j in allowed:
        column = restrict_column(D, allowed, j)
        if len(independent(columns+[column])) > len(columns):
            columns.append(column)
            I.append(j)
    J = {j for i in I for j in allowed if S[i] >> j & 1}
    return I, sorted(H | J | set(I))


def check_refinement(D, U, rng):
    K, ell = target.compact_symmetric(D, U)
    n = len(D)
    samples = range(1 << n) if n <= 10 else [rng.randrange(1 << n) for _ in range(96)]
    checked = 0
    for x in samples:
        z = sum(((u & x).bit_count() & 1) << j for j, u in enumerate(U))
        assert q4(D, x) == (q4(K, z)+2*((ell & x).bit_count() & 1)) % 4
        checked += 1
    return checked, ell


def random_symmetric(n, rng):
    rows = [0]*n
    for i in range(n):
        for j in range(i+1):
            if rng.randrange(2):
                rows[i] |= 1 << j
                rows[j] |= 1 << i
    return rows


def run():
    rng = random.Random(2710202611)
    records, refinement_checks, exact_checks, boundary_punctures = [], 0, 0, 0
    for n in (4, 6, 8, 10, 12, 16, 24, 32):
        B = [((1 << n)-1) ^ (1 << i) for i in range(n)]
        assert len(independent(B)) == n
        certificate = target.acquire_symmetric(B, 1, 0)
        assert certificate is not None
        assert len(certificate['removed']) == 1
        assert certificate['low_rank'] == 1 and certificate['residual_edges'] == 0
        assert certificate['low_rank_matrix'] == [(1 << (n-1))-1]*(n-1)
        replay(B, certificate, 1)
        checks, ell = check_refinement(certificate['low_rank_matrix'], certificate['code_generators'], rng)
        refinement_checks += checks
        # Giving the unreduced full-rank code still punctures every coordinate.
        full = target.candidate_symmetric(B, tuple(range(n)), (), 0, 0)
        assert full['removed'] == list(range(n))
        replay(B, full, 1)
        boundary_punctures += len(full['punctures'])
        sums = {}
        if n <= 10:
            for b in (1, 2, 3):
                terms = [(0, -1), (0, 0), (1, -3)]
                terms += [(sum(1 << i for i in rng.sample(range(n), 3)), rng.randrange(-9, 10))
                          for _ in range(n)]
                actual, metadata = target.exact_compiled_symmetric(B, terms, b, certificate)
                assert actual == literal_sum(B, terms, b)
                assert metadata['effective_phase_order'] == 1 << max(2, b)
                sums[str(1 << b)] = actual
                exact_checks += 1
        records.append(dict(family='raw full-rank J+I', n=n, raw_rank=n,
                            erased=len(certificate['removed']), completion_rank=1,
                            candidates=certificate['candidates_examined'], ell=ell,
                            exact_sums=sums))

    hidden_fixtures = 0
    for n, r, M, radius in [(9, 3, 2, 1), (10, 3, 3, 2),
                             (24, 3, 5, 2), (40, 4, 10, 3)]:
        for repetition in range(3):
            while True:
                rows = [rng.randrange(1 << r) for _ in range(n)]
                if len(independent(rows)) == r:
                    break
            D = matmul(rows, transpose(rows, r))
            S, M0 = error_graph(n, M, rng)
            B = [(d & ~(1 << i)) ^ s for i, (d, s) in enumerate(zip(D, S))]
            I, E0 = witness(D, S, radius)
            assert len(E0) <= 2*M0//radius+r*radius
            certificate = target.candidate_symmetric(B, I, E0, radius-1, M0)
            assert certificate is not None
            replay(B, certificate, radius)
            R = certificate['retained']
            assert certificate['low_rank_matrix'] == [restrict_column(D, R, i) for i in R]
            assert len(certificate['removed']) <= 2*M0//radius+3*r*radius
            checks, ell = check_refinement(certificate['low_rank_matrix'], certificate['code_generators'], rng)
            refinement_checks += checks
            if n <= 10:
                for b in (1, 3):
                    terms = [(0, 2)] + [(sum(1 << i for i in rng.sample(range(n), 3)),
                                        rng.randrange(-7, 8)) for _ in range(n)]
                    actual, _ = target.exact_compiled_symmetric(B, terms, b, certificate)
                    assert actual == literal_sum(B, terms, b)
                    exact_checks += 1
            hidden_fixtures += 1
            records.append(dict(family='symmetric hidden witness', n=n, r=r, M=M0,
                                radius=radius, erased=len(certificate['removed']),
                                retained_rank=certificate['low_rank'], ell=ell))

    star = [14, 1, 1, 1]
    assert target.candidate_symmetric(star, (0,), (), 0, 3) is None  # nonsymmetric decode
    assert target.candidate_symmetric(star, (), (), 0, 3) is None  # radius failure
    assert target.candidate_symmetric([2, 1, 0], (), (), 0, 0) is None  # global edge budget
    assert target.acquire_symmetric([14, 13, 11, 7], 1, 0, total_removal_cap=0) is None
    # Code dimension can exceed actual recovered rank; K need not be nonsingular.
    redundant = target.candidate_symmetric(star, (0,), (0,), 0, 0)
    assert redundant is not None and redundant['final_code_dimension'] == 1 and redundant['low_rank'] == 0
    replay(star, redundant, 1)
    for b in (1, 2, 3):
        terms = [(0, -1), (1, 3), (14, -5)]
        actual, _ = target.exact_compiled_symmetric(star, terms, b, redundant)
        assert actual == literal_sum(star, terms, b)
        exact_checks += 1

    gauss_checks = 0
    for n in range(5, 11):
        for repetition in range(3):
            K = random_symmetric(n, rng)
            for a in rng.sample(range(1 << n), 8):
                assert target.gaussian_i_sum(K, a) == brute_gauss(K, a)
                gauss_checks += 1
    magnitude_checks = 0
    for n in (24, 40, 64):
        for lowrank in (False, True):
            if lowrank:
                rows = [rng.randrange(32) for _ in range(n)]
                K = matmul(rows, transpose(rows, 5))
            else:
                K = random_symmetric(n, rng)
            radical = nullspace(K, n)
            for a in [0]+[rng.randrange(1 << n) for _ in range(7)]:
                re, im = target.gaussian_i_sum(K, a)
                obstructed = any((q4(K, z)+2*((a & z).bit_count() & 1)) % 4 for z in radical)
                expected_square = 0 if obstructed else 1 << (n+len(radical))
                assert re*re+im*im == expected_square
                magnitude_checks += 1

    published = json.loads((SOURCE.parent / 'diagonal_completion_results.json').read_text())
    for record in published['fixtures']:
        b = record['phase_order'].bit_length()-1
        assert literal_sum(record['raw_matrix'], record['terms'], b) == record['exact_sum']
        replay(record['raw_matrix'], record['certificate'], record['certificate']['decoding_radius'])
        exact_checks += 1

    return dict(status='all independent diagonal-completion checks passed',
                source=str(SOURCE.relative_to(ROOT)),
                source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                raw_full_rank_searches=8, full_code_boundary_punctures=boundary_punctures,
                hidden_witness_fixtures=hidden_fixtures,
                exact_phase_sums=exact_checks, quadratic_refinement_checks=refinement_checks,
                additional_exact_gaussian_checks=gauss_checks,
                large_gaussian_magnitude_checks=magnitude_checks,
                rejection_paths_checked=4, records=records,
                limitation='Exhaustive finite sums validate representation identities, not practical speed or the asymptotic counter.')


if __name__ == '__main__':
    result = run()
    path = Path(__file__).with_name('diagonal_completion_focus_results.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}))

#!/usr/bin/env python3
"""Test the distance-pruning obstruction and its diagonal repair.

The block fixtures are existence-witness comparisons, not complete searches.
The separate diagonal_completion_focus_checks.py performs raw searches.
"""
from pathlib import Path
import json
import random

from lowrank_sparse_audit_checks import independent, codewords, matmul, transpose
from diagonal_completion_focus_checks import target, check_refinement
import mixed_quadratic_compiler as old


def block_code_prune(r, block_length, radius):
    n = r*block_length
    original = [((1 << block_length)-1) << (j*block_length) for j in range(r)]
    retained = list(range(n))
    steps = []
    while True:
        code = independent([old.pack(word, retained) for word in original])
        short = next((word for _, word in codewords(code)
                      if word and word.bit_count() <= 2*radius), None)
        if short is None:
            break
        support = {retained[i] for i in range(len(retained)) if short >> i & 1}
        before = len(code)
        retained = [i for i in retained if i not in support]
        after = len(independent([old.pack(word, retained) for word in original]))
        assert after < before
        steps.append(dict(erased=len(support), rank_before=before, rank_after=after))
    return retained, steps


def run():
    code_records, repair_records = [], []
    for r in (2, 4, 8):
        for radius in (1, 2, 4):
            length = 2*radius
            remaining, steps = block_code_prune(r, length, radius)
            assert not remaining
            assert sum(step['erased'] for step in steps) == 2*r*radius
            code_records.append(dict(rank=r, radius=radius, n=r*length,
                                     erased=r*length, steps=len(steps)))
    rng = random.Random(2710202612)
    identity_checks = 0
    for r in (4, 6):
        for length in (4, 8, 16):
            n = r*length
            rows = [1 << (i//length) for i in range(n)]
            K = old.matrix_from_edges(r, [(i, i+1) for i in range(r-1)])
            assert len(independent(K)) == r
            A = matmul(matmul(rows, K), transpose(rows, r))
            S = [(((1 << length)-1) << ((i//length)*length)) ^ (1 << i)
                 for i in range(n)]
            B = [a ^ s for a, s in zip(A, S)]
            I = tuple(i*length for i in range(r))
            E0 = tuple(i for i in range(n) if i not in I)
            M = r*length*(length-1)//2
            old_certificate = old.candidate(B, I, E0, length-1, M)
            assert old_certificate is not None
            assert old_certificate['removed'] == list(range(n))
            D = [row ^ (1 << i) for i, row in enumerate(B)]
            completed_K = [row ^ (1 << i) for i, row in enumerate(K)]
            assert D == matmul(matmul(rows, completed_K), transpose(rows, r))
            assert len(independent(D)) <= r
            new_certificate = target.candidate_symmetric(B, I, I, 0, 0)
            assert new_certificate is not None
            assert new_certificate['removed'] == list(I)
            assert not any(new_certificate['sparse_matrix'])
            assert new_certificate['low_rank_matrix'] == old.restrict(D, new_certificate['retained'])
            checks, ell = check_refinement(new_certificate['low_rank_matrix'],
                                          new_certificate['code_generators'], rng)
            identity_checks += checks
            repair_records.append(dict(n=n, blocks=r, block_length=length,
                                       old_sparse_edges=M, old_rank_error_product=r*M,
                                       old_erased=len(old_certificate['removed']),
                                       new_sparse_edges=0, new_rank=new_certificate['low_rank'],
                                       new_erased=len(new_certificate['removed']),
                                       unary_correction=ell))
    return dict(status='all puncturing-boundary and repair assertions passed',
                code_obstruction_fixtures=len(code_records),
                block_clique_repair_fixtures=len(repair_records),
                sampled_refinement_identities=identity_checks,
                code_obstructions=code_records, diagonal_repairs=repair_records,
                scope='Exact mechanism tests; block comparisons use existence witnesses, not hidden-decomposition-free full searches.')


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('puncture_boundary_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('code_obstructions', 'diagonal_repairs')}))

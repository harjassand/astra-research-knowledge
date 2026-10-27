#!/usr/bin/env python3
"""Raw symmetric row-cluster acquisition; exact finite validation only.

One-swap metric k-median is established prior work (Arya et al., 2004).
No asymptotic phase engine or practical speed claim is implemented here.
"""
from itertools import combinations, product
from pathlib import Path
import importlib.util
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_mixed_root'))
from mixed_quadratic_compiler import independent, exact_original, matrix_from_edges, edge_count
from diagonal_completion_compiler import symmetric, off_diagonal, exact_compiled_symmetric


def acquire(B, c):
    n = len(B)
    if not 1 <= c <= n or not symmetric(B) or any(row>>i&1 for i,row in enumerate(B)):
        raise ValueError('Require a nonempty alternating matrix and 1<=c<=n')
    distances = [[(a ^ b).bit_count() for b in B] for a in B]
    facilities = list(range(c))
    history = []
    candidates = 0
    while True:
        best_two = []
        for i in range(n):
            ordered = sorted((distances[i][f], f) for f in facilities)
            first = ordered[0]
            second = ordered[1][0] if len(ordered)>1 else n+1
            best_two.append((first[0],first[1],second))
        objective = sum(t[0] for t in best_two)
        history.append(objective)
        best = (objective,None,None)
        open_set = set(facilities)
        for old in facilities:
            for new in range(n):
                if new in open_set:
                    continue
                value = sum(min(distances[i][new], second if assigned==old else first)
                            for i,(first,assigned,second) in enumerate(best_two))
                candidates += 1
                if value < best[0]:
                    best = (value,old,new)
        if best[1] is None:
            break
        facilities[facilities.index(best[1])] = best[2]
        facilities.sort()
    assignments = [min(facilities,key=lambda f:(distances[i][f],f)) for i in range(n)]
    classes = [[i for i in range(n) if assignments[i]==f] for f in facilities]
    classes = [A for A in classes if A]
    C = [0]*n
    H = [0]*len(classes)
    for a,A in enumerate(classes):
        for b in range(a,len(classes)):
            T=classes[b]
            ones=sum((B[i]>>j)&1 for i in A for j in T)
            bit = int(2*ones>len(A)*len(T))
            if bit:
                H[a] |= 1<<b
                H[b] |= 1<<a
                for i in A:
                    C[i] |= sum(1<<j for j in T)
                for j in T:
                    C[j] |= sum(1<<i for i in A)
    sparse=[a^b for a,b in zip(off_diagonal(B),off_diagonal(C))]
    U=[sum(1<<i for i in A) for A in classes]
    assert symmetric(C) and symmetric(sparse)
    assert len(set(C))<=c
    rank=len(independent(C))
    assert rank<=c
    assert edge_count(sparse)<=2*objective
    assert all(B[i] == (C[i]&~(1<<i))^sparse[i] for i in range(n))
    return dict(classes=classes,facilities=facilities,objective=objective,
                objective_history=history,candidates_examined=candidates,
                quotient=H,removed=[],retained=list(range(n)),
                code_generators=U,low_rank_matrix=C,sparse_matrix=sparse,
                low_rank=rank,residual_edges=edge_count(sparse))


def input_optimum(B,c):
    return min(sum(min((B[i]^B[j]).bit_count() for j in F) for i in range(len(B)))
               for F in combinations(range(len(B)),c))


def block_matrix(labels,H):
    return [sum(((H[labels[i]]>>labels[j])&1)<<j for j in range(len(labels)))
            for i in range(len(labels))]


def test():
    rng=random.Random(270926)
    small_checks=0
    approx_checks=0
    rounding_checks=0
    maximum_ratio=(0,1)
    # Every simple graph through n=5, every nonzero facility budget.
    for n in range(1,6):
        slots=list(combinations(range(n),2))
        for mask in range(1<<len(slots)):
            B=matrix_from_edges(n,[e for h,e in enumerate(slots) if mask>>h&1])
            for c in range(1,n+1):
                got=acquire(B,c)
                optimum=input_optimum(B,c)
                assert got['objective']<=5*optimum
                assert got['residual_edges']<=2*got['objective']
                if optimum and got['objective']*maximum_ratio[1] > maximum_ratio[0]*optimum:
                    maximum_ratio=(got['objective'],optimum)
                small_checks+=1
                approx_checks+=1
                rounding_checks+=1
    fixtures=[]
    exact_phase_checks=0
    for n,c,M in [(8,1,0),(9,3,2),(10,3,6),(12,4,12),
                  (16,4,30),(24,6,70),(36,9,160),(48,12,300)]:
        labels=[i%c for i in range(n)]
        rng.shuffle(labels)
        H=[0]*c
        for a in range(c):
            for b in range(a,c):
                bit=rng.randrange(2)
                H[a]|=bit<<b
                H[b]|=bit<<a
        if n==8:
            H=[1]
        D=block_matrix(labels,H)
        edges=rng.sample(list(combinations(range(n),2)),M)
        S=matrix_from_edges(n,edges)
        B=[a^b for a,b in zip(off_diagonal(D),S)]
        got=acquire(B,c)
        assert got['residual_edges']<=40*M+20*n
        assert got['objective']<=10*(2*M+n)
        record=dict(n=n,hidden_types=len(set(D)),budget=c,hidden_rank=len(independent(D)),
                    original_errors=M,raw_rank=len(independent(B)),
                    raw_edges=edge_count(B),acquired_rank=got['low_rank'],
                    acquired_types=len(got['classes']),residual_edges=got['residual_edges'],
                    objective=got['objective'],swaps=len(got['objective_history'])-1,
                    product_cM=c*M,n_squared=n*n)
        if n<=12:
            supports=[sum(1<<j for j in group) for group in
                      [rng.sample(range(n),3) for _ in range(n//3)]]
            terms=[(s,1) for s in supports]
            record['phase_results']=[]
            for b in (1,2,3):
                original=exact_original(B,terms,b)
                reconstructed=exact_compiled_symmetric(B,terms,b,got)
                if isinstance(reconstructed,tuple):
                    result=reconstructed[0]
                else:
                    result=reconstructed
                # The common compiler promotes internally, then projects back.
                assert list(result)==list(original)
                exact_phase_checks+=1
                record['phase_results'].append(dict(root_order=1<<b,exact=list(original)))
        fixtures.append(record)
    # A compile-only larger matrix, with natural cM exceeding n^2.
    n,c,M=240,24,3000
    labels=[i%c for i in range(n)]
    rng.shuffle(labels)
    H=[0]*c
    for a in range(c):
        for b in range(a,c):
            bit=rng.randrange(2)
            H[a]|=bit<<b
            H[b]|=bit<<a
    D=block_matrix(labels,H)
    S=matrix_from_edges(n,rng.sample(list(combinations(range(n),2)),M))
    B=[a^b for a,b in zip(off_diagonal(D),S)]
    got=acquire(B,c)
    assert got['objective']<=10*(2*M+n)
    assert got['residual_edges']<=40*M+20*n
    fixtures.append(dict(n=n,budget=c,hidden_types=len(set(D)),hidden_rank=len(independent(D)),
                         original_errors=M,raw_rank=len(independent(B)),raw_edges=edge_count(B),
                         acquired_rank=got['low_rank'],acquired_types=len(got['classes']),
                         residual_edges=got['residual_edges'],objective=got['objective'],
                         swaps=len(got['objective_history'])-1,product_cM=c*M,n_squared=n*n,
                         compile_only=True))
    failures=[]
    for d in range(2,9):
        n=1<<d
        D=[sum(((i&j).bit_count()%2)<<j for j in range(n)) for i in range(n)]
        B=off_diagonal(D)
        assert len(independent(D))==d and len(set(D))==n
        got=acquire(B,d)
        # Every two distinct latent-code rows have Hamming distance n/2.
        assert all((D[0]^D[j]).bit_count()==n//2 for j in range(1,n))
        lower_numerator=max(0,n*(n-d-4))
        assert 8*got['residual_edges']>=lower_numerator
        failures.append(dict(n=n,hidden_binary_rank=d,hidden_row_types=n,
                             attempted_types=d,residual_edges=got['residual_edges'],
                             guaranteed_edge_lower_bound_numerator=lower_numerator,
                             guaranteed_edge_lower_bound_denominator=8))
    return dict(status='all exact assertions passed',
                exhaustive_graph_budget_checks=small_checks,
                optimum_metric_comparisons=approx_checks,
                symmetric_rounding_checks=rounding_checks,
                largest_observed_local_search_ratio=list(maximum_ratio),
                exact_mixed_phase_checks=exact_phase_checks,fixtures=fixtures,
                generic_lowrank_failure_examples=failures,
                ancestry='Classical one-swap metric k-median; symmetric rounding and phase composition.',
                scope='Small hidden row diversity, not arbitrary small GF2 rank.',
                backend='Finite phase sums exhaustive; large fixture acquisition only; no speed claim.')


if __name__=='__main__':
    result=test()
    Path(__file__).with_name('row_cluster_acquisition_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

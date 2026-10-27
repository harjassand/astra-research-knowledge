#!/usr/bin/env python3
"""Complete six-variable alternating-cubic rank-two certificate.

Products are taken over F2 and only the squarefree degree-three part is
retained. Lower-degree corrections may be arbitrary and cost-free.
"""
import itertools
import json
from collections import Counter
from pathlib import Path


def cubic_product(u,v,w,triples):
    result=0
    for t,(i,j,k) in enumerate(triples):
        coefficient=0
        for a,b,c in itertools.permutations((i,j,k)):
            coefficient ^= ((u>>a)&1)*((v>>b)&1)*((w>>c)&1)
        result |= coefficient<<t
    return result


def binary_rank(rows,n):
    basis={}
    for row in rows:
        while row:
            p=(row&-row).bit_length()-1
            if p in basis: row^=basis[p]
            else: basis[p]=row;break
    return len(basis)


def contraction_distribution(terms,n):
    counts=Counter()
    for v in range(1,1<<n):
        rows=[0]*n
        for a,b,c in terms:
            for i,j,k in ((a,b,c),(a,c,b),(b,c,a)):
                if v>>k&1: rows[i]^=1<<j;rows[j]^=1<<i
        counts[binary_rank(rows,n)]+=1
    return dict(sorted(counts.items()))


def main():
    n=6
    triples=list(itertools.combinations(range(n),3))
    rank_one={}
    for u,v,w in itertools.combinations(range(1,1<<n),3):
        if w == u^v:
            continue
        p=cubic_product(u,v,w,triples)
        assert p
        rank_one.setdefault(p,(u,v,w))
    assert len(rank_one)==1395
    one=sorted(rank_one)
    rank_at_most_two={0,*one}
    for i,u in enumerate(one):
        rank_at_most_two.update(u^v for v in one[i:])
    target=next(p for p in range(1<<len(triples)) if p not in rank_at_most_two)
    decomposition=None
    for u in one:
        remainder=target^u
        if remainder not in rank_at_most_two:
            continue
        for v in one:
            w=remainder^v
            if w in rank_one:
                decomposition=[rank_one[z] for z in (u,v,w)]
                break
        if decomposition:
            break
    assert decomposition is not None
    reconstructed=0
    for u,v,w in decomposition:
        reconstructed ^= cubic_product(u,v,w,triples)
    assert reconstructed==target
    terms=[[i+1 for i in triple] for j,triple in enumerate(triples) if target>>j&1]
    target_distribution=contraction_distribution([tuple(i-1 for i in t) for t in terms],n)
    two_disjoint_distribution=contraction_distribution([(0,1,2),(3,4,5)],n)
    assert target_distribution=={2:7,4:56}
    assert two_disjoint_distribution=={2:14,4:49}
    out=dict(status='all assertions passed',variables=n,
             cubic_coefficient_dimension=len(triples),
             complete_rank_one_dictionary_size=len(rank_one),
             complete_rank_at_most_two_count=len(rank_at_most_two),
             all_cubic_parts=1<<len(triples),
             first_missing_integer=target,cubic_terms=terms,
             certified_alternating_rank=3,
             rank_three_linear_form_masks=decomposition,
             contraction_rank_distribution=target_distribution,
             two_disjoint_products_distribution=two_disjoint_distribution,
             interpretation='No sum of two products of three affine forms, even with any quadratic correction, has this cubic part.')
    Path(__file__).with_name('affine_cubic_rank_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()

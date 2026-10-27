#!/usr/bin/env python3
"""Exact finite checks of the raw-column-span obstruction.

The proof applies to all sublinear raw column subsets; finite tests enumerate
all small subsets and sample larger ones. Coding distances are computed exactly.
"""
from itertools import combinations
from pathlib import Path
import json
import random
from annihilator_acquisition import (
    independent, codewords, alternating_form, matching, matvec, transpose,
)


def gf_mul(a,b,modulus,m):
    result=0
    while b:
        if b&1:
            result ^= a
        b >>= 1
        a <<= 1
        if (a >> m)&1:
            a ^= modulus
    return result


def gf_pow(a,p,modulus,m):
    result=1
    while p:
        if p&1:
            result=gf_mul(result,a,modulus,m)
        a=gf_mul(a,a,modulus,m)
        p >>= 1
    return result


def bch_labels(m,t,modulus):
    # Nonzero field elements except 1 give an even number of coordinates.
    return [sum(gf_pow(a,2*j+1,modulus,m) << (m*j) for j in range(t))
            for a in range(2,1 << m)]


def exact_dual_distance(labels,half_bound):
    table={0:0}
    n=len(labels)
    for size in range(1,half_bound+1):
        for indices in combinations(range(n),size):
            mask=sum(1 << j for j in indices)
            value=0
            for j in indices:
                value ^= labels[j]
            assert value not in table, 'a dependency of at most twice the half bound exists'
            table[value]=mask
    # All dependencies up to 2*half_bound excluded. Search the next weight.
    for indices in combinations(range(n),half_bound+1):
        mask=sum(1 << j for j in indices)
        value=0
        for j in indices:
            value ^= labels[j]
        if value in table:
            combined=mask ^ table[value]
            if combined.bit_count()==2*half_bound+1:
                return combined.bit_count(),combined,len(table)
    raise AssertionError('next-weight witness absent')


def fixture(m,t,modulus,seed):
    labels=bch_labels(m,t,modulus)
    n=len(labels)
    columns=independent(transpose(labels,m*t))
    r=len(columns)
    assert r%2==0 and r==m*t
    distance=min(word.bit_count() for a,word in codewords(columns) if a)
    dual,dual_witness,syndrome_count=exact_dual_distance(labels,t)
    D=alternating_form(columns,n)
    P=matching(n)
    B=[a ^ b for a,b in zip(D,P)]
    assert len(independent(D))==r
    assert len(independent(B)) >= n-r
    rng=random.Random(seed)
    checks=0
    total_subset_checks=0
    records=[]
    if n<=14:
        specs=[(k,list(combinations(range(n),k))) for k in range(3)]
    elif n<=100:
        specs=[(k,[tuple(sorted(rng.sample(range(n),k))) for _ in range(40)])
               for k in [2,4,6]]
    else:
        specs=[(k,[tuple(sorted(rng.sample(range(n),k)))]) for k in [8,12,16]]
    for k,subsets in specs:
        bound=max(0,min(dual,distance-k-1))
        minimum_actual=n
        minimum_total=n*n
        for I in subsets:
            selected=set(I)
            span=list(word for _,word in codewords([B[i] for i in I]))
            total=0
            for j in range(n):
                observed=min((B[j]^v).bit_count() for v in span)
                total += observed
                if j not in selected:
                    assert observed >= bound
                    minimum_actual=min(minimum_actual,observed)
                    checks += 1
            assert total >= (n-k)*bound
            minimum_total=min(minimum_total,total)
            total_subset_checks += 1
        records.append(dict(selected_columns=k,subsets=len(subsets),
                            lower_bound_per_unselected_column=bound,
                            minimum_observed_column_error=minimum_actual,
                            certified_total_error_lower_bound=(n-k)*bound,
                            minimum_observed_total_error=minimum_total))
    return dict(n=n,r=r,code_distance=distance,dual_distance=dual,
                dual_distance_witness=dual_witness,
                checked_small_subset_syndromes=syndrome_count,
                true_sparse_edges=n//2,true_directed_error=n,
                raw_matrix=B,latent_columns=columns,
                column_subset_checks=total_subset_checks,
                unselected_column_checks=checks,records=records)


def main():
    records=[fixture(4,1,0b10011,1),fixture(5,2,0b100101,2),
             fixture(6,3,0b1000011,3),fixture(8,1,0b100011011,4)]
    result=dict(status='all exact assertions passed',records=records,
                total_column_subsets=sum(x['column_subset_checks'] for x in records),
                total_unselected_column_checks=sum(x['unselected_column_checks'] for x in records),
                practical_speed_claim=False)
    Path(__file__).with_name('raw_column_failure_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
    print(json.dumps([{k:x[k] for k in ('n','r','code_distance','dual_distance','records')}
                      for x in records],indent=2))


if __name__=='__main__':
    main()

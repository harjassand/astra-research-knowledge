#!/usr/bin/env python3
"""Small exact recognition/validation checks; no compiler performance reruns."""
from __future__ import annotations
from bisect import bisect_left
from fractions import Fraction
import hashlib
from itertools import permutations
import json
from pathlib import Path
import random

import validation as val
fd,ac=val.fd,val.ac
HERE=Path(__file__).resolve().parent


def anf_degree(table,n):
    coefficients=list(table)
    for bit in range(n):
        for x in range(1 << n):
            if x >> bit & 1:coefficients[x]^=coefficients[x^(1 << bit)]
    return max((x.bit_count() for x,c in enumerate(coefficients) if c),default=-1)


def identity_model(n,d):
    return [fd.Polynomial(n,d,{1 << (n-i-1)}) for i in range(n)]


def rank_from_model(model,x):
    out=0
    for q in model:out=(out << 1)|q(x)
    return out


def lis_length(values):
    tails=[]
    for x in values:
        j=bisect_left(tails,x)
        if j==len(tails):tails.append(x)
        else:tails[j]=x
    return len(tails)


def exact_prefix_rejection(permutation,n,h):
    # Candidate order is raw numeric order. Every pair has a unique first
    # differing candidate bit/stage and hence one explicit probe weight.
    numerator=0
    N=1 << n
    for x in range(N):
        for y in range(x+1,N):
            stage=n-(x^y).bit_length()
            if stage<h and permutation[x]>permutation[y]:numerator+=1 << (stage+2)
    return Fraction(numerator,h*N*N) if h else Fraction(0)


def ancestor_good(permutation,n,i):
    low,high=0,1 << n
    while True:
        pivot=(low+high)//2
        if pivot==i:return True
        if (permutation[i]<permutation[pivot])!=(i<pivot):return False
        if i<pivot:high=pivot
        else:low=pivot+1


def adjacent_needles():
    records=[]
    for n in range(2,9):
        N=1 << n
        boundaries=[0]*(n+1)
        comparisons=0
        for j in range(N-1):
            table=[int(x==j or x==j+1) for x in range(N)]
            assert anf_degree(table,n)==n-1
            # Adjacent swaps change exactly one unordered comparison. Check
            # every pair for small n; the larger cases check the unique pair
            # plus all comparisons involving either endpoint.
            p=list(range(N));p[j],p[j+1]=p[j+1],p[j]
            pairs=[(x,y) for x in range(N) for y in range(x+1,N)] if n<=5 else [
                (x,y) for x in range(N) for y in range(x+1,N) if x in (j,j+1) or y in (j,j+1)]
            changed=[(x,y) for x,y in pairs if (p[x]<p[y])!=(x<y)]
            comparisons+=len(pairs)
            assert changed==[(j,j+1)]
            for h in range(1,n+1):
                r=n-h
                changes=(j >> r)!=((j+1) >> r)
                boundaries[h]+=int(changes)
        assert all(boundaries[h]==(1 << h)-1 for h in range(1,n+1))
        records.append(dict(n=n,adjacent_swaps=N-1,all_delta_pair_degrees=n-1,
                            prefix_changed_adjacent_counts=boundaries[1:],pair_checks=comparisons))
    return records


def sharp_budget_checks():
    rows=[]
    for M in (1,3,7,15,31,255):
        for beta in (Fraction(0),Fraction(1,10),Fraction(1,4),Fraction(1,3)):
            expected_one=(1-beta)*M
            expected_two=(1-2*beta)*M
            conditional_two=Fraction(M)*(1-2*beta)/(1-beta)
            ceil=lambda q:(q.numerator+q.denominator-1)//q.denominator
            T_one,T_two=ceil(expected_one),ceil(conditional_two)
            assert Fraction(M-T_one,M)<=beta
            assert (1-beta)*Fraction(M-T_two,M)<=beta
            # Randomize between floor/ceil subset sizes to meet the exact null
            # expected lower bounds rather than merely the worst-cap versions.
            assert (1-beta)*(1-conditional_two/M)==beta
            rows.append(dict(M=M,beta=str(beta),perfect_complete_cap=T_one,
                two_sided_cap=T_two,perfect_complete_null_expected=str(expected_one),
                two_sided_null_expected=str(expected_two)))
    return rows


def exhaustive_three_bit():
    n,N,d=3,8,2
    count=0
    minima={h:Fraction(1) for h in (1,2,3)}
    min_deletion=Fraction(1)
    for p in permutations(range(N)):
        count+=1
        degrees=[anf_degree([(p[x] >> (n-i-1))&1 for x in range(N)],n) for i in range(n)]
        assert max(degrees)<=d  # Every balanced three-bit coordinate has no cubic term.
        if p==tuple(range(N)):continue
        deletion=Fraction(N-lis_length(p),N)
        min_deletion=min(min_deletion,deletion)
        assert deletion>=Fraction(1,1 << (d+1))
        for h in (1,2,3):
            wrong=any((p[x] >> (n-h))!=(x >> (n-h)) for x in range(N))
            rejection=exact_prefix_rejection(p,n,h)
            if wrong:
                minima[h]=min(minima[h],rejection)
                assert rejection>=Fraction(1,h*(1 << (2*d)))
            else:assert rejection==0
        good=[i for i in range(N) if ancestor_good(p,n,i)]
        assert all(p[x]<p[y] for a,x in enumerate(good) for y in good[a+1:])
        assert len(good)<=lis_length(p)
    return dict(n=n,degree=d,permutations=count,
                minimum_distinct_model_deletion=str(min_deletion),
                prefix_rejection_minima={str(h):str(v) for h,v in minima.items()},
                all_ancestor_good_sets_increasing=True)


def executable_validators():
    records=[]
    n,d=4,2
    linear=[fd.Polynomial(n,d,{1 << i}) for i in range(n)]
    actual=[fd.Polynomial(n,d,{1,4|8})]+linear[1:]
    actual_rank=lambda x:rank_from_model(actual,x)
    compare=lambda x,y:int(actual_rank(x)<actual_rank(y))
    # Explicit candidates for unknown-r selection. This tests new validation,
    # not acquisition or a claim that the compiler generated these candidates.
    for r in (0,1,2):
        model=linear if r<2 else actual
        out=val.degree_promised_validate(n,d,model,[1 << i for i in range(n-r)],
                                         compare,seed=991200+r,eta=.001)
        assert out['status']==('REJECT' if r<2 else 'ACCEPT_UNDER_TRUE_DEGREE_PROMISE')
        records.append(dict(scope='degree-only validator with supplied candidate; not acquisition',
                            assumed_r=r,actual_valid_partial_flag_r=2,result=out))
    # A candidate need NOT be bijective for the full tail validator's soundness.
    n,d,h=5,3,3
    model=identity_model(n,d)
    nonbijective=model[:h]+[fd.Polynomial(n,d,set()) for _ in range(n-h)]
    out=val.degree_promised_validate(n,d,nonbijective,[1 << (n-i-1) for i in range(h)],
                                    lambda x,y:int(x<y),seed=881119,eta=.001)
    assert out['status']=='REJECT'
    records.append(dict(scope='nonbijective candidate rejected without a global candidate bijectivity test',result=out))
    # Exact prefix equality check admits arbitrary within-block source order.
    n,d,h=5,2,2
    model=identity_model(n,d)
    r=n-h
    p=[((x >> r) << r)|(((x&((1 << r)-1))*5+3)&((1 << r)-1)) for x in range(1 << n)]
    cmp=lambda x,y:int(p[x]<p[y])
    exact=val.exact_prefix_validate(n,d,model[:h],[1 << (n-i-1) for i in range(h)],cmp)
    assert exact['status']=='EXACT_PREFIX_MATCH'
    whole=val.chain_validate(n,lambda i:i,cmp)
    assert whole['status']=='REJECT'
    records.append(dict(scope='prefix exact equality accepts arbitrary suffix; whole equality rejects',
                        prefix=exact,whole=whole))
    return records


def off_promise_misses():
    n,d,h=8,2,6
    N=1 << n
    model=identity_model(n,d)
    toggles=[1 << (n-i-1) for i in range(h)]
    p=list(range(N));j=N//2-1;p[j],p[j+1]=p[j+1],p[j]
    exact_rejection=exact_prefix_rejection(p,n,h)
    assert exact_rejection==Fraction(4,h*N*N)<Fraction(1,h*(1 << (2*d)))
    out=val.degree_promised_validate(n,d,model[:h],toggles,lambda x,y:int(p[x]<p[y]),
                                    seed=0,eta=.01,prefix_only=True)
    assert out['status']=='ACCEPT_UNDER_TRUE_DEGREE_PROMISE'
    cap=out['prefix_test']['test_cap']
    return dict(status='EXPECTED_OFF_PROMISE_FALSE_ACCEPT',n=n,d=d,h=h,
        source_modification='one adjacent swap across midpoint',source_coordinate_degree=n-1,
        exact_rejection_per_prefix_probe=str(exact_rejection),
        degree_promised_rejection_lower_bound=str(Fraction(1,h*(1 << (2*d)))),
        actual_miss_probability=float((1-exact_rejection)**cap),
        promised_error_budget=.01,result=out,
        interpretation='true degree promise fails; this validation is not exact promise recognition')


def main():
    receipt=dict(status='PASS_WITH_EXPECTED_OFF_PROMISE_MISS',
        scope='exact finite algebra and new validator execution; no compiler performance rerun',
        adjacent_needles=adjacent_needles(),sharp_budgets=sharp_budget_checks(),
        exhaustive_three_bit=exhaustive_three_bit(),validators=executable_validators(),
        off_promise=off_promise_misses(),
        source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (HERE/'validation.py',Path(__file__))})
    (HERE/'recognition_fixture.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status=receipt['status'],
        adjacent_swaps=sum(row['adjacent_swaps'] for row in receipt['adjacent_needles']),
        exact_permutations=receipt['exhaustive_three_bit']['permutations'],
        validator_cases=len(receipt['validators']),
        off_promise_miss_probability=receipt['off_promise']['actual_miss_probability'])))

if __name__=='__main__':main()

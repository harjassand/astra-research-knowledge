#!/usr/bin/env python3
"""Execute exact certificates for the block-orbit representation boundary."""
from itertools import combinations, product
from pathlib import Path
import json
import random
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'work_mixed_root'))
from mixed_quadratic_compiler import independent, multiply


def rref(vectors):
    basis={}
    for original in vectors:
        x=original
        for p in sorted(basis,reverse=True):
            if x>>p&1: x^=basis[p]
        if not x: continue
        p=x.bit_length()-1
        for q in list(basis):
            if basis[q]>>p&1: basis[q]^=x
        basis[p]=x
    return tuple(basis[p] for p in sorted(basis,reverse=True))


def qbinomial(r,b):
    num=den=1
    for j in range(b):
        num*=((1<<r)-(1<<j)); den*=((1<<b)-(1<<j))
    assert num%den==0
    return num//den


def pairing(A,V):
    return [sum(((a&v).bit_count()%2)<<j for j,v in enumerate(V)) for a in A]


def run():
    b=3
    group=[list(g) for g in product(range(1<<b),repeat=b) if len(independent(g))==b]
    assert len(group)==168
    rng=random.Random(2710202657)
    records=[]
    alignments=0
    for r,samples in [(4,None),(5,20),(6,5)]:
        spaces=sorted(set(rref(v) for v in combinations(range(1,1<<r),b)
                          if len(independent(v))==b))
        s=len(spaces); s0=qbinomial(r-1,b)
        assert s==qbinomial(r,b)
        assert len(independent([row for V in spaces for row in V]))==r
        for v in range(1,1<<r):
            count=sum(all((v&u).bit_count()%2==0 for u in V) for V in spaces)
            assert count==s0
        pairs=list(combinations(range(s),2))
        if samples is not None: pairs=rng.sample(pairs,samples)
        distances=[]
        for a,z in pairs:
            best=None
            for G in group:
                Delta=[x^y for x,y in zip(multiply(G,spaces[a]),spaces[z])]
                assert any(Delta)
                cost=sum(len(independent(pairing(Delta,V))) for V in spaces)
                assert cost>=s-s0
                best=cost if best is None else min(best,cost)
                alignments+=1
            distances.append(best)
        c=max(1,s//10)
        lower_num=(s-c)*(s-s0)-2*b*s
        records.append(dict(ambient_rank=r,block_width=b,blocks=s,variables=b*s,
                            hyperplane_subspaces=s0,pairwise_orbit_distance_lower_bound=s-s0,
                            tested_pairs=len(pairs),smallest_exact_tested_distance=min(distances),
                            type_budget_example=c,residual_edge_lower_bound_numerator=lower_num,
                            residual_edge_lower_bound_denominator=4))
    return dict(status='all exact assertions passed',group_order=len(group),
                exact_alignment_checks=alignments,fixtures=records,
                scope='Representation obstruction; generic low-rank compiler still handles this family.')


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('grassmann_orbit_boundary_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

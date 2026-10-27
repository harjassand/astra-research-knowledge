#!/usr/bin/env python3
"""Acquire cubic blocks from dense input, then compile fixed-arity phases.

All count checks use exhaustive truth vectors. The asymptotic phase
counter is not implemented here. No forest restriction is imposed.
"""
import itertools
import json
import random
from pathlib import Path
from cubic_structure_compiler import (
    apply, centroid_blocks, compose, eliminate_radical, indices, phase,
    random_invertible, substitute,
)


def truth_sum(poly,n):
    """Parallel exhaustive truth-table evaluation with exact big integers."""
    size=1<<n
    universe=(1<<size)-1
    variables=[]
    for i in range(n):
        run=1<<i
        word=((1<<run)-1)<<run
        length=2*run
        while length<size:
            word |= word<<length
            length*=2
        variables.append(word)
    truth=0
    for term in poly:
        value=universe
        for i in indices(term): value &= variables[i]
        truth ^= value
    return size-2*truth.bit_count()


def edge_expansion(vertices,edges):
    if vertices<2: return None
    best=None
    for mask in range(1,1<<vertices):
        s=mask.bit_count()
        if s>vertices//2: continue
        cut=sum(((mask>>i)^(mask>>j))&1 for i,j in edges)
        if best is None or cut*best[1]<best[0]*s: best=(cut,s)
    return {'numerator':best[0],'denominator':best[1]}


def acquire(poly,n):
    zero_certificate={}
    reduction=eliminate_radical(poly,n,zero_certificate)
    if reduction is None:
        return dict(zero_certificate=zero_certificate,count=0)
    core,d,e,rounds=reduction
    blocks,meta=centroid_blocks(core,d)
    columns=[v for block in blocks for v in block]
    transformed=substitute(core,d,columns)
    sizes=list(map(len,blocks))
    owner={};start=0
    for block,size in enumerate(sizes):
        for v in range(start,start+size): owner[v]=block
        start+=size
    edges=set()
    for term in transformed:
        touched={owner[v] for v in indices(term)}
        if len(touched)>1:
            assert term.bit_count()==2 and len(touched)==2
            edges.add(tuple(sorted(touched)))
    nonconstant=transformed-{0}
    detailed_bound=sum(s+s*(s-1)//2+s*(s-1)*(s-2)//6 for s in sizes)
    detailed_bound+=sum(sizes[i]*sizes[j] for i,j in edges)
    weight=d+sum(s**3 for s in sizes)+sum(sizes[i]*sizes[j] for i,j in edges)
    assert len(nonconstant)<=detailed_bound
    phases=[dict(variables=[i for i in indices(s)],coefficient=1)
            for s in sorted(nonconstant)]
    assert all(len(g['variables'])<=3 for g in phases)
    return dict(original_variables=n,core_variables=d,factor_exponent=e,
                radical_rounds=rounds,block_sizes=sizes,
                acquired_columns=columns,quadratic_edges=sorted(edges),
                transformed_polynomial=sorted(transformed),
                phase_monomials=phases,constant_phase=int(0 in transformed),
                actual_phase_factors=len(phases),weighted_bound=weight,
                detailed_monomial_bound=detailed_bound,**meta)


def phases_at(record,x):
    parity=record['constant_phase']
    for g in record['phase_monomials']:
        parity ^= int(all(x>>i&1 for i in g['variables']))
    return -1 if parity else 1


def build_instance(block_polys,sizes,edges,rng):
    offsets=[];s=0
    base=set()
    for poly,size in zip(block_polys,sizes):
        offsets.append(s)
        base.symmetric_difference_update({mask<<s for mask in poly})
        s+=size
    for i,j in edges:
        terms=[(1<<(offsets[i]+u))|(1<<(offsets[j]+v))
               for u in range(sizes[i]) for v in range(sizes[j])
               if rng.randrange(2)]
        if not terms: terms=[(1<<offsets[i])|(1<<offsets[j])]
        base.symmetric_difference_update(terms)
    hidden=random_invertible(s,rng)
    raw=substitute(base,s,hidden)
    return base,raw,hidden,s


def main():
    rng=random.Random(20261103)
    cycle=[(0,1),(1,2),(2,3),(0,3)]
    clique=list(itertools.combinations(range(4),2))
    bipartite=[(i,j) for i in range(3) for j in range(3,6)]
    indecomposable6={(1<<0)|(1<<1)|(1<<5),
                    (1<<0)|(1<<2)|(1<<4),
                    (1<<1)|(1<<2)|(1<<3)}
    descriptions=[
        ('hidden four-cycle',[{7}]*4,[3]*4,cycle),
        ('hidden four-clique',[{7}]*4,[3]*4,clique),
        ('hidden K3,3',[{7}]*6,[3]*6,bipartite),
        ('hidden two six-dimensional primitive blocks',
         [indecomposable6]*2,[6,6],[(0,1)]),
    ]
    records=[];identities=0
    for name,block_polys,sizes,edges in descriptions:
        base,raw,hidden,n=build_instance(block_polys,sizes,edges,rng)
        rec=acquire(raw,n)
        assert not rec.get('zero_certificate')
        assert rec['core_variables']==n and rec['factor_exponent']==0
        assert sorted(rec['block_sizes'])==sorted(sizes)
        # Verify which original hidden block each acquired image spans.
        change=compose(hidden,rec['acquired_columns'])
        old_owner={};start=0
        for i,size in enumerate(sizes):
            for v in range(start,start+size): old_owner[v]=i
            start+=size
        block_map={};cursor=0
        for i,size in enumerate(rec['block_sizes']):
            touched={old_owner[v] for col in change[cursor:cursor+size]
                     for v in indices(col)}
            assert len(touched)==1
            block_map[i]=next(iter(touched));cursor+=size
        mapped_edges={tuple(sorted((block_map[i],block_map[j])))
                      for i,j in rec['quadratic_edges']}
        assert mapped_edges==set(edges)
        dense_count=truth_sum(raw,n)
        base_count=truth_sum(base,n)
        phase_count=truth_sum(set(rec['transformed_polynomial']),n)
        assert dense_count==base_count==phase_count
        assignments=range(1<<n) if n<=12 else [rng.randrange(1<<n) for _ in range(4096)]
        checked=0
        for y in assignments:
            assert phase(raw,apply(rec['acquired_columns'],y))==phases_at(rec,y)
            checked+=1
        identities+=checked
        # Exhaustive expansion is a SMALL-FIXTURE diagnostic, never acquisition work.
        rec.update(edge_expansion=edge_expansion(len(rec['block_sizes']),rec['quadratic_edges']),
                   family=name,raw_polynomial=sorted(raw),
                   raw_cubic_monomials=sum(s.bit_count()==3 for s in raw),
                   exact_phase_sum=dense_count,
                   original_zero_count=((1<<n)+dense_count)//2,
                   explicit_identity_checks=checked,
                   identity_check_scope='all assignments' if n<=12 else '4096 fixed-seed assignments',
                   exhaustive_count_assignments=1<<n)
        records.append(rec)
    out=dict(status='all assertions passed',raw_fixtures=len(records),
             exact_pointwise_identity_checks=identities,
             exact_count_method='exhaustive bit-vector truth tables for raw, hidden, and compiled polynomials',
             asymptotic_counter_executed=False,records=records)
    Path(__file__).with_name('acquired_block_phase_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
    for r in records:
        print(json.dumps({k:r[k] for k in ['family','original_variables','raw_cubic_monomials',
                         'block_sizes','actual_phase_factors','weighted_bound',
                         'edge_expansion','exact_phase_sum']},sort_keys=True))


if __name__=='__main__':
    main()

#!/usr/bin/env python3
"""Exact hardness embedding in the same J-pair family at d=3, e=2.

The 42-bit case independently scans all residue vectors, not all ring
assignments. The 66-bit case scans the independently parameterized critical
chart. Both then acquire and count the raw affinely disguised Boolean ANF.
"""
from acquired_contact_counter import *
from field_descent import extract_anf,random_invertible
import random
import numpy as np


def exponent(b,indices):
    a=[0]*b
    for i in indices:a[i]+=1
    return tuple(a)


def toggle(P,a,c):
    P[a]=P.get(a,0)^c
    if not P[a]:del P[a]


def manufacture(source,N):
    if N<2 or N%2:raise ValueError('source dimension must be positive and even')
    h=11;F=ChainRing(h,1);R=ChainRing(h,2);r=N+1;b=2*r+1;z=b-1
    alpha=2;alpha2=F.mul(alpha,alpha);alpha4=F.mul(alpha2,alpha2)
    ua,va=next((u,v) for u in range(8) for v in range(8)
        if F.mul(u,alpha2)^F.mul(v,alpha)==1
        and F.mul(u,alpha4)^F.mul(v,alpha2)==0)
    P={};G={}
    for pair in range(r):
        x,y=2*pair,2*pair+1
        for indices in ([x,x,x],[x,y,y],[y,y,y],[z,x,y]):
            toggle(P,exponent(b,indices),1)
    for mask in source:
        if mask.bit_count()>3 or mask>>N:raise ValueError('not an N-bit cubic ANF')
        term={exponent(b,[z]*(3-mask.bit_count())):1}
        for i in bits(mask):
            linear={exponent(b,[2*i]):ua,exponent(b,[2*i+1]):va}
            term=poly_mul(F,term,linear)
        for a,c in term.items():toggle(G,a,c)
    for a,c in G.items():toggle(P,a,c<<3)
    for a in (0,1):
        for bb in (0,1):
            y=F.mul(a,alpha)^F.mul(bb,alpha2);x=F.mul(y,y)
            assert F.mul(ua,x)^F.mul(va,y)==a
            assert F.mul(x,y)==F.mul(a,alpha)^F.mul(bb,alpha2)^(a^bb^(a&bb))
    return R,P,G,dict(source_dimension=N,pairs=r,module_rank=b,
        alpha=alpha,a_extractor=[ua,va])


def independent_chart_sum(R,G,source,N):
    F=ChainRing(R.h,1);r=N+1;b=2*r+1
    critical=0;signed=0;radial=1
    for packed in range(1<<(2*r)):
        aa=[(packed>>(2*i))&1 for i in range(r)]
        bb=[(packed>>(2*i+1))&1 for i in range(r)]
        if sum(aa)%2 or sum(bb)%2 or sum(a*c for a,c in zip(aa,bb))%2:continue
        point=[]
        for a,c in zip(aa,bb):
            y=(2 if a else 0)^(4 if c else 0);point.extend([F.mul(y,y),y])
        point.append(1);value=ring_polynomial(F,G,point)
        encoded=sum(a<<i for i,a in enumerate(aa[:N]))
        assert value==polynomial_value(source,encoded)
        critical+=1;signed+=1-2*value
        for u in range(1,8):
            scaled=[F.mul(u,x) for x in point]
            radial+=1-2*F.functional(ring_polynomial(F,G,scaled))
    return (8**b)*radial,critical,signed,1<<(2*r)


def independent_full_residues(R,P,b):
    """Top-digit orthogonality, with no chart or ray formula reused."""
    q=8;F=ChainRing(R.h,1)
    mul=np.array([[F.mul(x,y) for y in range(q)] for x in range(q)],dtype=np.uint8)
    ids=np.arange(q**b,dtype=np.uint32)
    coords=[((ids>>(3*i))&7).astype(np.uint8) for i in range(b)]
    z=coords[-1];valid=np.ones(q**b,dtype=np.bool_);gz=np.zeros(q**b,dtype=np.uint8)
    for i in range(0,b-1,2):
        x,y=coords[i:i+2];x2=mul[x,x];y2=mul[y,y]
        valid&=(x2^y2^mul[z,y])==0
        valid&=(y2^mul[z,x])==0
        gz^=mul[x,y]
    valid&=gz==0
    selected=ids[valid];G={a:c>>3 for a,c in P.items() if c>>3};total=0
    for encoded in selected:
        point=[(int(encoded)>>(3*i))&7 for i in range(b)]
        total+=1-2*F.functional(ring_polynomial(F,G,point))
    return q**b*total,len(selected),q**b


def run():
    cases=[];rng=random.Random(19271027)
    for N,source in [(2,{0,1,3}),(4,{0,1,2,3,7,11,13})]:
        started=time.perf_counter();R,P,G,meta=manufacture(source,N)
        b=meta['module_rank'];n=6*b;source_sum=sum(
            1-2*polynomial_value(source,x) for x in range(1<<N))
        source_zero_sign=1-2*int(0 in source)
        critical=(1<<(N-1))*((1<<N)+1)
        critical_signed=(1<<(N-1))*(source_sum+source_zero_sign)
        expected=8**b*(1+3*critical+4*critical_signed)
        reference,actual_critical,actual_signed,chart_points=independent_chart_sum(R,G,source,N)
        assert (reference,actual_critical,actual_signed)==(expected,critical,critical_signed)
        oracle=dict(method='independent binary critical-chart parameterization and explicit radial field scan',
            chart_candidates_enumerated=chart_points,radial_field_values=7*critical)
        if N==2:
            full,critical_points,points=independent_full_residues(R,P,b)
            assert full==expected and critical_points==1+7*critical
            oracle.update(all_residue_vectors_enumerated=points,residue_critical_points=critical_points)
        columns=random_invertible(n,rng);offset=rng.randrange(1<<n)
        def phase(x):
            y=linear_apply(columns,x)^offset
            return R.functional(ring_polynomial(R,P,[(y>>(6*i))&63 for i in range(b)]))
        print(json.dumps(dict(stage='extracting affinely disguised raw ANF',n=n,source=N)),flush=True)
        raw=extract_anf(phase,n)
        input_path=Path(__file__).with_name(f'pair_boundary_raw_{n}.json')
        input_path.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),separators=(',',':'))+'\n')
        result=compile_contact(raw,n)
        assert result['signed_count']==expected
        assert result['centroid_dimension']==6
        assert result['count_certificate']['projective_ray_count']==critical
        assert result['count_certificate']['geometry']['critical_kernel_dimension']==2*(N+1)
        for _ in range(256):
            x=rng.randrange(1<<n);assert polynomial_value(raw,x)==phase(x)
        recovered=((result['signed_count']//8**b-1-3*critical)//(4*(1<<(N-1))))-source_zero_sign
        assert recovered==source_sum
        result.update(meta,source_anf=sorted(source),source_signed_count=source_sum,
            recovered_source_signed_count=recovered,expected_signed_count=expected,
            critical_signed_count=critical_signed,reference_oracle=oracle,
            raw_input_file=input_path.name,planted_polynomial=[dict(exponents=a,coefficient=c) for a,c in P.items()],
            planted_binary_columns=columns,planted_binary_offset=offset,representation_checks=256,
            total_test_seconds=time.perf_counter()-started)
        cases.append(result)
        Path(__file__).with_name('pair_divisibility_boundary_results.json').write_text(json.dumps(dict(
            status='all completed assertions passed',cases=cases,practical_speed_claim=False,
            full_ring_truth_table_enumerated=False),indent=2)+'\n')
        print(json.dumps(dict(n=n,source_signed=source_sum,ring_signed=expected,rays=critical,
            kernel=2*(N+1),seconds=result['total_test_seconds'])),flush=True)


if __name__=='__main__':run()

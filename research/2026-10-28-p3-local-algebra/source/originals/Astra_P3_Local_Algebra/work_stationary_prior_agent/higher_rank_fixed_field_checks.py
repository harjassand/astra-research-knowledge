#!/usr/bin/env python3
"""Independent F8 obstruction checks and acquired one-ray kernel checks.

At depth two, the higher field digits are eliminated by character
orthogonality.  Every residue assignment is enumerated independently;
this is explicitly not a full binary truth table of the ring polynomial.
"""
from higher_rank_boundary_checks import *
import numpy as np


def reduced_critical_sum(P, b, h):
    d=h.bit_length()-1; q=1<<d; m=b-1
    table=np.array([[gf_mul(x,y,h) for y in range(q)] for x in range(q)],dtype=np.uint8)
    indices=np.arange(q**b,dtype=np.uint32)
    coordinates=[((indices>>(d*i))&(q-1)).astype(np.uint8) for i in range(b)]
    z=coordinates[-1]; valid=np.ones(q**b,dtype=np.bool_); gz=np.zeros(q**b,dtype=np.uint8)
    for i in range(0,m,2):
        x,y=coordinates[i:i+2]
        valid &= table[y,y^z]==0
        valid &= table[x,x^z]==0
        gz ^= table[x,y]
    valid &= gz==0
    selected=indices[valid]
    field=ChainRing(h,1)
    G={a:c>>d for a,c in P.items() if c>>d}
    signs=[]
    for point in selected:
        values=[(int(point)>>(d*i))&(q-1) for i in range(b)]
        signs.append(1-2*field.functional(ring_polynomial(field,G,values)))
    return q**b*sum(signs),len(selected),q**b


def fixed_field_hardness_checks(rng):
    cases=[]; h=11; d=3; q=8; R=ChainRing(h,2)
    for N in [2,4]:
        b=N+3; m=b-1; n=6*b; z=m
        F={mask for mask in range(1<<N) if mask.bit_count()<=3 and rng.randrange(2)}
        if N>=3:F.add(7)
        P={}
        for i in range(0,m,2):
            for indices in [(z,i,i+1),(i,i,i+1),(i,i+1,i+1)]:
                add(P,exponent(b,indices),1)
        G=set(F)
        for i in range(0,N,2):
            mask=(1<<i)|(1<<(i+1))
            if mask in G:G.remove(mask)
            else:G.add(mask)
        G.add(1<<N)
        for mask in G:
            support=[i for i in range(m) if (mask>>i)&1]
            add(P,exponent(b,support+[z]*(3-len(support))),q)
        actual,critical_count,points=reduced_critical_sum(P,b,h)
        source=sum(1-2*polynomial_value(F,u) for u in range(1<<N))
        critical_rays=((1<<m)+(1<<(m//2)))//2
        expected=q**b*(1+(q//2)*source+(q//2-1)*critical_rays)
        assert actual==expected,(N,F,actual,expected)
        assert critical_count==1+(q-1)*critical_rays
        columns=random_invertible(n,rng);offset=rng.randrange(1<<n)
        def phase(x):
            y=linear_apply(columns,x)^offset
            return R.functional(ring_polynomial(R,P,[(y>>(6*i))&63 for i in range(b)]))
        raw=extract_anf(phase,n)
        algebra,_,_=centroid(raw,n)
        assert len(algebra)==6
        # Verify the acquired cubic ANF against independent evaluations after
        # the affine disguise.  This is not another enumeration of ring inputs.
        for _ in range(256):
            x=rng.randrange(1<<n)
            assert polynomial_value(raw,x)==phase(x)
        cases.append(dict(field_modulus=h,field_degree=d,depth=2,source_variables=N,
            ring_variables=b,original_binary_variables=n,source_anf=sorted(F),
            source_signed_count=source,ring_signed_count=actual,expected=expected,
            residue_points_enumerated=points,residue_critical_points=critical_count,
            projective_critical_rays=critical_rays,chart_kernel_dimension=m,
            full_binary_centroid_dimension=len(algebra),
            ring_polynomial=[dict(exponents=a,coefficient=c) for a,c in P.items()],
            raw_anf=sorted(raw),binary_disguise_columns=columns,binary_disguise_offset=offset,
            verification='all residue points; exact higher-digit orthogonality; 256 ANF spot checks'))
    return cases


def one_ray_kernel_checks():
    cases=[]
    for d in range(1,13):
        h=next(h for h in range((1<<d)|1,1<<(d+1),2) if irreducible_binary(h))
        q=1<<d; mask=q-1
        def gradient(packed):
            x=packed&mask; y=packed>>d
            x2=gf_mul(x,x,h); y2=gf_mul(y,y,h)
            return (x2^y2^y)|((y2^x)<<d)
        columns=[gradient(1<<j) for j in range(2*d)]
        kernel=kernel_columns(columns)
        # Independent one-variable enumeration is only a small-field oracle.
        roots=[y for y in range(q) if gf_mul(gf_mul(y,y,h),gf_mul(y,y,h),h)^gf_mul(y,y,h)^y==0]
        assert len(kernel)==(2 if d%3==0 else 0)
        assert len(roots)==1<<len(kernel)
        assert all(gradient(gf_mul(y,y,h)|(y<<d))==0 for y in roots)
        cases.append(dict(field_degree=d,field_modulus=h,per_pair_binary_kernel_dimension=len(kernel),
            independent_polynomial_roots=roots,oracle_field_points=q,
            no_missing_infinity_rays=True,one_ray_for_any_number_of_pairs=d%3!=0))
    return cases


def run():
    rng=random.Random(721398)
    hardness=fixed_field_hardness_checks(rng); one_ray=one_ray_kernel_checks()
    result=dict(status='all assertions passed',fixed_field_hardness_cases=hardness,
        one_ray_kernel_cases=one_ray,
        total_hardness_residue_points=sum(x['residue_points_enumerated'] for x in hardness),
        total_one_ray_oracle_field_points=sum(x['oracle_field_points'] for x in one_ray),
        practical_speed_claim=False)
    Path(__file__).with_name('higher_rank_fixed_field_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],hardness_cases=len(hardness),
        original_binary_dimensions=[x['original_binary_variables'] for x in hardness],
        acquired_centroid_dimensions=[x['full_binary_centroid_dimension'] for x in hardness],
        total_hardness_residue_points=result['total_hardness_residue_points'],
        one_ray_kernel_cases=len(one_ray))))


if __name__=='__main__':run()

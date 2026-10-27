#!/usr/bin/env python3
"""Independent finite algebra and critical-fiber audit of fixed J hardness.

These tests enumerate the manufactured critical chart, not all original
ring inputs; highest-digit orthogonality is proved in the adjacent note.
"""
from homogeneous_chain_counter import *
import itertools,json,random


def run():
    h=11;q=8;alpha=2;alpha2=gf_mul(alpha,alpha,h);alpha4=gf_mul(alpha2,alpha2,h)
    roots=[]
    for a,b in itertools.product((0,1),repeat=2):
        y=(alpha if a else 0)^(alpha2 if b else 0);x=gf_mul(y,y,h)
        y3=gf_mul(y,x,h)
        assert gf_mul(x,x,h)^x^y==0
        assert y3==((alpha if a else 0)^(alpha2 if b else 0)^a^b^(a*b))
        assert gf_mul(alpha2,x,h)^gf_mul(alpha4,y,h)==a
        assert gf_mul(alpha,x,h)^gf_mul(alpha2,y,h)==b
        roots.append((a,b,x,y,y3))
    assert len({row[3] for row in roots})==4
    assert sorted(gf_pow(z,3,h) for z in range(1,q))==list(range(1,q))
    rng=random.Random(88127);cases=[]
    for N in (2,4,6):
        r=N+1;b=2*r+1
        p={mask for mask in range(1<<N) if mask.bit_count()<=3 and rng.randrange(2)}
        if N>=3:p.add(7)
        source=sum(1-2*polynomial_value(p,a) for a in range(1<<N));s0=1-2*int(0 in p)
        rays=0;weighted=0;radial=0;a_fibers={}
        for rows in itertools.product(roots,repeat=r):
            critical_value=0
            for row in rows:critical_value^=row[4]
            avec=sum(row[0]<<i for i,row in enumerate(rows))
            bvec=sum(row[1]<<i for i,row in enumerate(rows))
            assert (critical_value==0)==(avec.bit_count()%2==0 and bvec.bit_count()%2==0 and (avec&bvec).bit_count()%2==0)
            if critical_value:continue
            rays+=1;a_fibers[avec]=a_fibers.get(avec,0)+1
            phase=polynomial_value(p,avec&((1<<N)-1));weighted+=1-2*phase
            radial+=sum(1-2*gf_trace(gf_pow(z,3,h) if phase else 0,h) for z in range(1,q))
        ncrit=(1<<(N-1))*((1<<N)+1)
        expected_weight=(1<<(N-1))*(source+s0)
        assert rays==ncrit and weighted==expected_weight
        assert radial==3*ncrit+4*expected_weight
        assert all(count==(1<<N if a==0 else 1<<(N-1)) for a,count in a_fibers.items())
        signed=q**b*(1+radial)
        recovered=((signed//q**b-1-3*ncrit)//(4*(1<<(N-1))))-s0
        assert recovered==source
        cases.append(dict(source_variables=N,ring_pairs=r,ring_variables=b,
            original_binary_variables=6*b,source_anf=sorted(p),source_signed_count=source,
            critical_candidates_enumerated=4**r,critical_rays=rays,
            weighted_critical_sum=weighted,radial_character_sum=radial,
            ring_signed_count=signed,recovered_source_signed_count=recovered,
            count_oracle_scope='critical chart plus exact highest-digit orthogonality; not full ring enumeration'))
    result=dict(status='all assertions passed',field_modulus=h,alpha=alpha,
        extractor_coefficients=[alpha2,alpha4],root_table=roots,cases=cases,
        total_critical_candidates_enumerated=sum(c['critical_candidates_enumerated'] for c in cases),
        practical_speed_claim=False)
    Path(__file__).with_name('j_residue_hardness_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],cases=len(cases),
        original_binary_dimensions=[c['original_binary_variables'] for c in cases],
        total_critical_candidates_enumerated=result['total_critical_candidates_enumerated'])))


if __name__=='__main__':run()

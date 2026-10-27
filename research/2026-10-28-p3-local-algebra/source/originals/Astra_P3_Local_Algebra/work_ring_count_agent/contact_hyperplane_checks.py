#!/usr/bin/env python3
"""Exact geometry, Hensel, nullity, and all-field-count audits."""
from contact_hyperplane_audit import *
import numpy as np
from field_kloosterman import irreducible_binary


def truth_sum(P,R):
    b=len(next(iter(P)));n=b*R.m;mask=(1<<R.m)-1
    def value(x):return R.functional(ring_polynomial(R,P,[(x>>(R.m*i))&mask for i in range(b)]))
    anf=extract_anf(value,n);table=np.zeros(1<<n,dtype=np.uint8);table[list(anf)]=1
    for i in range(n):
        view=table.reshape(-1,2,1<<i);view[:,1,:]^=view[:,0,:]
    return (1<<n)-2*int(table.sum()),len(anf)


def random_field_columns(b,h,rng):
    q=1<<(h.bit_length()-1)
    while True:
        columns=[[rng.randrange(q) for _ in range(b)] for _ in range(b)]
        if field_matrix_rank(columns,h)==b:return columns


def run():
    rng=random.Random(2026102817);geometry=[];nullities=[];truth=[]
    for h,e,pairs,family in [(7,3,2,'uniform'),(11,4,2,'nine'),(19,3,3,'unique')]:
        R=ChainRing(h,e);b=2*pairs+1
        if family=='unique':P=unique_ray_polynomial(pairs);expected=1
        elif family=='nine':
            P=uniform_contact_polynomial(2);P[(1,2,0,0,0)]=gf_pow(2,6,h)
            P[(0,0,1,2,0)]=gf_pow(gf_mul(2,2,h),6,h);expected=9
        else:P=uniform_contact_polynomial(pairs);expected=(4**pairs+2**pairs)//2
        columns=random_field_columns(b,h,rng);P=substitute_ring_polynomial(R,P,columns)
        for ex in degree_monomials(b,3):P[ex]=P.get(ex,0)^(rng.randrange(1<<(R.m-R.d))<<R.d)
        P={ex:c for ex,c in P.items() if c}
        transformed,rays,certificate=acquire_lifted_rays(R,P)
        assert len(rays)==expected
        expected_ell=[column[-1] for column in columns]
        nonzero=next(c for c in expected_ell if c);inverse=gf_pow(nonzero,(1<<R.d)-2,h)
        expected_ell=[gf_mul(inverse,c,h) for c in expected_ell]
        assert certificate['hyperplane']==expected_ell
        geometry.append(dict(h=h,e=e,b=b,family=family,polynomial=[dict(exponents=list(a),coefficient=c)
            for a,c in sorted(P.items())],rays=rays,certificate=certificate))
    for h in [3,7,11,19,37,67]:
        assert irreducible_binary(h);R=ChainRing(h,1);d=R.d
        for pairs in [2,3]:
            _,rays,certificate=acquire_lifted_rays(R,unique_ray_polynomial(pairs))
            expected_nullity=2*pairs if d%3==0 else 0
            assert certificate['binary_root_kernel_dimension']==expected_nullity
            if d%3:
                assert len(rays)==1 and all(c==0 for c in rays[0]['center'])
            else:
                expected=(4**pairs+3*2**pairs+(-2)**pairs)//8
                assert len(rays)==expected
            assert all(r['critical_value']==0 and r['arf_bit']==0 for r in rays)
            nullities.append(dict(d=d,pair_count=pairs,nullity=expected_nullity,
                                   critical_rays=len(rays),certificate=certificate))
    # Variable module rank with one acquired residue root: no fixed-rank matrix.
    R=ChainRing(19,2);_,rays,certificate=acquire_lifted_rays(R,unique_ray_polynomial(5))
    assert certificate['binary_root_kernel_dimension']==0 and len(rays)==1
    nullities.append(dict(d=4,pair_count=5,nullity=0,critical_rays=1,certificate=certificate))
    for h,e,pairs in [(3,2,2),(7,2,2),(3,3,2),(3,2,3),(11,1,2),(7,1,3),(19,1,2)]:
        R=ChainRing(h,e);actual,terms=truth_sum(uniform_contact_polynomial(pairs),R)
        expected=uniform_chain_sum(h,e,pairs);assert actual==expected
        truth.append(dict(family='uniform',h=h,e=e,b=2*pairs+1,n=(2*pairs+1)*R.m,
                          signed_count=actual,reference=expected,anf_terms=terms,
                          assignments=1<<((2*pairs+1)*R.m)))
    for h,e,pairs in [(7,2,2),(3,3,2),(3,2,3)]:
        R=ChainRing(h,e);actual,terms=truth_sum(unique_ray_polynomial(pairs),R)
        q=1<<R.d;b=2*pairs+1
        expected=q**(b*(e-1))+(q-1)*q**((pairs+1)*e-1)
        assert actual==expected
        truth.append(dict(family='unique',h=h,e=e,b=b,n=b*R.m,signed_count=actual,
                          reference=expected,anf_terms=terms,assignments=1<<(b*R.m)))
    # A global contact factorization actually fails at first nilpotent order.
    R=ChainRing(7,2);P=uniform_contact_polynomial(3);ex=(1,0,1,0,1,0,0);P[ex]=1<<R.d
    _,rays,certificate=acquire_lifted_rays(R,P)
    assert len(rays)==36
    T={tuple(i for i,x in enumerate(a) if x):c&R.mask for a,c in P.items()
       if max(a)==1 and c&R.mask}
    rows=[];rhs=[]
    for four in itertools.combinations(range(7),4):
        rows.append([T.get(tuple(i for i in four if i!=j),0) if j in four else 0 for j in range(7)])
        rhs.append(int(four==(0,2,4,6)))
    assert field_linear_solve(rows,rhs,R.h) is None
    obstruction=dict(h=R.h,e=2,b=7,nilpotent_monomial=list(ex),
        global_contact_lift_exists=False,lifted_critical_rays=len(rays),rays=rays,
        nonzero_critical_values=sum(r['critical_value']!=0 for r in rays),certificate=certificate)
    # An inconsistent additive chart system contributes no nonzero rays.
    R=ChainRing(7,2);P=uniform_contact_polynomial(2);P[(1,0,0,0,2)]=2
    _,rays,empty_certificate=acquire_lifted_rays(R,P)
    assert len(rays)==0 and empty_certificate['transverse_roots']==0
    actual,terms=truth_sum(P,R);assert actual==4**5
    truth.append(dict(family='no_rational_ray',h=7,e=2,b=5,n=20,signed_count=actual,
                      reference=4**5,anf_terms=terms,assignments=1<<20))
    P={(1,1,0,0,1):1,(0,0,1,1,1):1}
    try:acquire_lifted_rays(R,P)
    except ValueError as exc:singular_hyperplane_rejection=str(exc)
    else:raise AssertionError('singular hyperplane restriction was accepted')
    out=dict(geometry=geometry,unique_ray_nullities=nullities,full_truth_cases=truth,
             full_truth_assignments=sum(t['assignments'] for t in truth),
             global_contact_obstruction=obstruction,empty_chart=empty_certificate,
             singular_hyperplane_rejection=singular_hyperplane_rejection)
    Path(__file__).with_name('contact_hyperplane_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(geometry_cases=len(geometry),nullity_cases=len(nullities),
        truth_cases=len(truth),truth_assignments=out['full_truth_assignments'],
        full_contact_lift_obstruction=True)),flush=True)
    return out


if __name__=='__main__':run()

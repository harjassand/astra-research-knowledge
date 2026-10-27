#!/usr/bin/env python3
"""Exact field leaf for acquired contact cubics by 2**d Gaussian sums.

The transverse dimension is not enumerated. This is a callback for
acquired_contact_counter.weighted_contact_sum(field_terminal=...).
"""
from pathlib import Path
import itertools,json,random,sys,time

ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_local_algebra_agent','work_ring_count_agent','work_chain_root'):
    sys.path.insert(0,str(ROOT/folder))
from acquired_contact_counter import (
    ChainRing,contact_geometry,polynomial_linear_change,ring_polynomial,
    quadratic_sum,weighted_contact_sum,degree_exponents,polynomial_value,
    gf_mul)
from field_descent import extract_anf


def contact_field_sum(h,b,H,*,details=False):
    """Return sum_x (-1)^Tr H(x), in 2**d poly(b,d) time and polynomial space.

    Exactly b-1 field variables are eliminated by each binary Gaussian;
    only the acquired contact coordinate has its 2**d values enumerated.
    The contact_geometry gates are the same as the parent chain counter.
    """
    F=ChainRing(h,1);geometry=contact_geometry(F,H,b)
    # Homogeneity makes dehomogenization injective on coefficient vectors.
    changed={alpha+(3-sum(alpha),):c for alpha,c in geometry['chart_polynomial'].items()}
    if any(len(a)!=b or sum(a)!=3 or c&~F.mask for a,c in changed.items()):
        raise ValueError('not a field-valued homogeneous cubic')
    if any(a[-1]==0 and max(a)==1 and c for a,c in changed.items()):
        raise ValueError('transverse field slice contains a binary cubic')
    n=(b-1)*F.d;answer=0;samples=[]
    for z in range(1<<F.d):
        def phase(x,z=z):
            values=[(x>>(F.d*i))&F.mask for i in range(b-1)]+[z]
            return F.functional(ring_polynomial(F,changed,values))
        value=quadratic_sum(phase,n);answer+=value
        if len(samples)<8:samples.append(dict(contact_value=z,gaussian_sum=value))
    evidence=dict(field_degree=F.d,module_dimension=b,
        contact_values_enumerated=1<<F.d,quadratic_variables_per_slice=n,
        transverse_assignments_enumerated=0,full_field_points_enumerated=0,
        contact_covector=geometry['covector'],sample_slices=samples,
        all_slices_streamed=True,method='acquired contact-coordinate conditioning and exact binary Gaussian sums')
    return (answer,evidence) if details else answer


def fixture(F,b,rng,*,disguise=True):
    """M=I, symplectic B; independent of the parent's kappa=0 fixtures."""
    H={};m=b-1
    def add(indices,c=1):
        a=[0]*b
        for i in indices:a[i]+=1
        a=tuple(a);H[a]=H.get(a,0)^c
    for i in range(m):
        add([i,i,i])
        add([i,i,m],rng.randrange(1<<F.d))
        add([i,m,m],rng.randrange(1<<F.d))
    for i in range(0,m,2):add([i,i+1,m])
    add([m,m,m],rng.randrange(1<<F.d))
    H={a:c for a,c in H.items() if c}
    if disguise:
        columns=[[int(i==j) for i in range(b)] for j in range(b)]
        for _ in range(5*b):
            i,j=rng.sample(range(b),2);c=rng.randrange(1,1<<F.d)
            columns[i]=[x^gf_mul(c,y,F.h) for x,y in zip(columns[i],columns[j])]
        H=polynomial_linear_change(F,H,columns)
    return H


def run():
    from top_digit_deflation_audit import brute_sum
    rng=random.Random(233457);field_cases=[];cached={}
    for h,b in ((3,5),(7,5),(11,5),(19,5),(7,7),(11,7)):
        F=ChainRing(h,1);H=fixture(F,b,rng);n=b*F.d
        began=time.perf_counter();actual,evidence=contact_field_sum(h,b,H,details=True)
        elapsed=time.perf_counter()-began
        def phase(x):
            return F.functional(ring_polynomial(F,H,[(x>>(F.d*i))&F.mask for i in range(b)]))
        raw=extract_anf(phase,n);expected=brute_sum(raw,n)
        assert actual==expected,(h,b,actual,expected)
        cached[h,b]=(H,expected)
        field_cases.append(dict(d=F.d,b=b,n=n,signed_sum=actual,
            exhaustive_assignments=1<<n,seconds=elapsed,evidence=evidence))

    chain_cases=[]
    for h,b,e in ((3,5,4),(11,5,4),(11,7,7)):
        R=ChainRing(h,e);F=ChainRing(h,1);H,field_expected=cached[h,b]
        # Higher coefficients include unrestricted squarefree transverse cubics.
        H={a:H.get(a,0)^(rng.randrange(1<<(R.m-R.d))<<R.d)
           for a in degree_exponents(b,3)}
        H={a:c for a,c in H.items() if c}
        height=(e+1)//3;ids=[i*R.m+j for i in range(b) for j in range(R.d*height)]
        Q={0} if rng.randrange(2) else set()
        for i in ids:
            if rng.randrange(2):Q.add(1<<i)
        for i,j in itertools.combinations(ids,2):
            if rng.randrange(2):Q.add((1<<i)|(1<<j))
        actual,certificate=weighted_contact_sum(h,e,H,Q,b,terminal_bit_budget=0,
            field_terminal=contact_field_sum)
        # The callback competitor is the independently exhausted field leaf.
        expected,reference=weighted_contact_sum(h,e,H,Q,b,terminal_bit_budget=0,
            field_terminal=lambda leaf_h,leaf_b,leaf_H:field_expected)
        assert actual==expected
        case=dict(d=R.d,b=b,e=e,n=b*R.m,signed_sum=actual,
            candidate_count=certificate['candidate_count'],projective_rays=certificate['projective_ray_count'],
            field_leaf_exhaustively_verified=True,field_terminal=certificate['terminal'],
            parent_terminal_point_budget=0)
        if b*R.m<=22:
            mask=(1<<R.m)-1
            def phase(x):
                return R.functional(ring_polynomial(R,H,[(x>>(R.m*i))&mask for i in range(b)]))^polynomial_value(Q,x)
            raw=extract_anf(phase,b*R.m);truth=brute_sum(raw,b*R.m)
            assert actual==truth
            case['independent_full_chain_truth_assignments']=1<<(b*R.m)
        chain_cases.append(case)
    # Exercise the terminal in a recursion with actual nonzero critical rays.
    h,b,e=3,5,4;R=ChainRing(h,e);F=ChainRing(h,1);H={}
    for i in range(b-1):
        a=[0]*b;a[i]=3;H[tuple(a)]=1
    for i in range(0,b-1,2):
        a=[0]*b;a[i]=a[i+1]=a[-1]=1;H[tuple(a)]=1
    Q={1<<(R.m*(b-1))}
    actual,certificate=weighted_contact_sum(h,e,H,Q,b,terminal_bit_budget=0,
        field_terminal=contact_field_sum)
    mask=(1<<R.m)-1
    def phase(x):
        return R.functional(ring_polynomial(R,H,[(x>>(R.m*i))&mask for i in range(b)]))^polynomial_value(Q,x)
    raw=extract_anf(phase,b*R.m);expected=brute_sum(raw,b*R.m)
    assert actual==expected and certificate['projective_ray_count']>0
    chain_cases.append(dict(d=R.d,b=b,e=e,n=b*R.m,signed_sum=actual,
        candidate_count=certificate['candidate_count'],projective_rays=certificate['projective_ray_count'],
        field_terminal=certificate['terminal'],parent_terminal_point_budget=0,
        independent_full_chain_truth_assignments=1<<(b*R.m)))
    result=dict(status='all exact assertions passed',field_cases=field_cases,
        chain_callback_cases=chain_cases,practical_speed_claim=False)
    Path(__file__).with_name('contact_field_terminal_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],field_cases=len(field_cases),
        field_truth_assignments=sum(x['exhaustive_assignments'] for x in field_cases),
        chain_callback_cases=len(chain_cases))))
    return result


if __name__=='__main__':run()

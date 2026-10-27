#!/usr/bin/env python3
"""Disguised raw contact cubics and independent residue-fiber counting oracles."""
from acquired_contact_counter import *
from field_descent import extract_anf,random_invertible
from stationary_counter_checks import truth_sum
import random


def contact_polynomial(R,b,kind,rng=None):
    P={};k=(b-1)//2
    def add(indices,c=1):
        a=[0]*b
        for i in indices:a[i]+=1
        P[tuple(a)]=P.get(tuple(a),0)^c
    for i in range(k):
        x,y=2*i,2*i+1;add([x,y,b-1])
        if kind=='one-ray':
            add([x,x,x]);add([x,y,y]);add([y,y,y])
        elif kind=='many-rays':
            if R.d<2:raise ValueError('many-ray fixture needs a nonbinary field element')
            c=2 if k!=2 or R.d!=3 else gf_pow(2,i+1,R.h)
            add([x,x,y]);add([x,y,y],gf_pow(c,(1<<R.d)-2,R.h))
        else:raise ValueError('unknown contact fixture')
    if rng is not None and R.e>1:
        for a in degree_exponents(b,3):
            P[a]=P.get(a,0)^(rng.randrange(1<<(R.m-R.d))<<R.d)
    return {a:c for a,c in P.items() if c}


def compatible_noise(R,b,rng,constant):
    height=(R.e+1)//3;qn=b*R.d*height;rank=qn-qn%2
    columns=random_invertible(qn,rng) if qn else []
    factors=[sum(((a>>(R.d*height*i))&((1<<(R.d*height))-1))<<(R.m*i)
                 for i in range(b)) for a in columns[:rank]]
    def phase(x):
        return constant^sum(((u&x).bit_count()&1)*((v&x).bit_count()&1)
                            for u,v in zip(factors[::2],factors[1::2]))%2
    return quadratic_coefficients(phase,b*R.m),factors,rank


def residue_fiber_oracle(R,P,Q,b):
    """Independent field scan plus exact Gaussian of each complete residue fiber.

    Used only for depths2/3. No projective chart, ray lift, or transverse
    formula is reused; the entire tA fiber is binary quadratic at these depths.
    """
    if R.e not in (2,3):raise ValueError('oracle depth must be two or three')
    F=ChainRing(R.h,1);P0={a:c&R.mask for a,c in P.items() if c&R.mask}
    derivatives=[derivative(P0,i) for i in range(b)]
    free_m=R.d*(R.e-1);free_mask=(1<<free_m)-1;total=0;critical=0
    for encoded in range(1<<(b*R.d)):
        a=[(encoded>>(R.d*i))&R.mask for i in range(b)]
        if any(ring_polynomial(F,g,a) for g in derivatives):continue
        critical+=1
        def value(y):
            values=[a[i]^(((y>>(free_m*i))&free_mask)<<R.d) for i in range(b)]
            x=sum(v<<(R.m*i) for i,v in enumerate(values))
            return R.functional(ring_polynomial(R,P,values))^polynomial_value(Q,x)
        total+=quadratic_sum(value,b*free_m)
    return total,dict(method='all residue vectors and complete quadratic fibers',
        residue_vectors_enumerated=1<<(b*R.d),critical_residue_vectors=critical,
        fiber_binary_variables=b*free_m)


def one_ray_depth_two_oracle(R,P,Q,b):
    """For the explicit κ=0 family, enumerate its q critical residues directly."""
    if R.e!=2 or R.d%3==0:raise ValueError('one-ray depth-two oracle scope')
    total=0
    for z in range(1<<R.d):
        values=[0]*(b-1)+[z];x=z<<(R.m*(b-1))
        phase=R.functional(ring_polynomial(R,P,values))^polynomial_value(Q,x)
        total+=1-2*phase
    return total*(1<<(b*R.d)),dict(method='direct highest-digit orthogonality on the proved critical line',
        critical_residues_enumerated=1<<R.d,free_highest_digit_bits=b*R.d)


def flat_one_ray_oracle(R,Q,b):
    """Closed original-coordinate ray, with direct low-prefix enumeration."""
    if R.d%3==0:raise ValueError('flat one-ray oracle needs d not divisible by three')
    total=0;multiplier=1;depth=R.e;states=[]
    while depth>=2:
        current=ChainRing(R.h,depth);height=quotient_height_rank(Q,current,b)
        # The ray is the exact Z axis and H vanishes on it at every depth.
        visible=max(1,height);units=0
        for r in range(1<<(R.d*visible)):
            if not r&current.mask:continue
            units+=1-2*polynomial_value(Q,r<<(current.m*(b-1)))
        units<<=R.d*(depth-visible)
        contribution=(1<<(R.d*(b-1)*depth//2))*units
        total+=multiplier*contribution
        states.append(dict(depth=depth,low_prefix_assignments=1<<(R.d*visible),unit_sum=units))
        if depth<=3:
            total+=multiplier*(1-2*int(0 in Q))*(1<<(R.d*b*(depth-1)))
            return total,dict(method='flat ray and direct low-prefix sums',states=states)
        Q=restrict_origin_quadratic(Q,current,depth-3);depth-=3;multiplier<<=2*b*R.d
    raise ValueError('oracle deliberately excludes field-terminal depths')


def raw_fixture(h,e,b,kind,seed,deform=True):
    R=ChainRing(h,e);n=b*R.m;rng=random.Random(seed)
    P=contact_polynomial(R,b,kind,rng if deform else None)
    Q,factors,rank=compatible_noise(R,b,rng,seed&1)
    if b==5 and R.d==3 and e in (2,3):reference,oracle=residue_fiber_oracle(R,P,Q,b)
    elif kind=='one-ray' and e==2:reference,oracle=one_ray_depth_two_oracle(R,P,Q,b)
    elif kind=='one-ray' and not deform:reference,oracle=flat_one_ray_oracle(R,Q,b)
    else:raise ValueError('no independent oracle assigned to this fixture')
    columns=random_invertible(n,rng);offset=rng.randrange(1<<n);mask=(1<<R.m)-1
    def evaluate(x):
        y=linear_apply(columns,x)^offset
        return R.functional(ring_polynomial(R,P,[(y>>(R.m*i))&mask for i in range(b)]))^polynomial_value(Q,y)
    raw=extract_anf(evaluate,n)
    metadata=dict(seed=seed,kind=kind,planted_field_modulus=h,planted_chain_length=e,
        planted_module_rank=b,planted_error_rank=rank,planted_higher_deformations=deform,
        planted_polynomial=[dict(exponents=list(a),coefficient=c) for a,c in P.items()],
        planted_quadratic=sorted(Q),planted_binary_columns=columns,planted_binary_offset=offset,
        planted_error_factors=factors,reference=reference,reference_oracle=oracle)
    return raw,n,evaluate,metadata


def run_raw():
    cases=[]
    specifications=[(11,2,5,'many-rays',11002,True),(11,3,5,'many-rays',11003,True),
                    (19,2,9,'one-ray',11092,True),(19,5,5,'one-ray',11055,False)]
    for h,e,b,kind,seed,deform in specifications:
        print(json.dumps(dict(stage='manufacture raw input and independent oracle',d=h.bit_length()-1,e=e,b=b)),flush=True)
        raw,n,evaluate,metadata=raw_fixture(h,e,b,kind,seed,deform)
        source=Path(__file__).with_name(f'contact_raw_{n}_{seed}.json')
        source.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),separators=(',',':'))+'\n')
        result=compile_contact(raw,n)
        assert result['signed_count']==metadata['reference'],(result['signed_count'],metadata['reference'])
        assert result['module_dimension']==b
        R=ChainRing(result['field_modulus'],e);mask=(1<<R.m)-1
        H={tuple(a['exponents']):a['coefficient'] for a in result['homogeneous_cubic']}
        Q=set(result['quotient_quadratic']);center=sum(a<<(R.m*i) for i,a in enumerate(result['fit']['acquired_center']))
        rng=random.Random(seed+1000000)
        for _ in range(1024):
            y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y);z=y^center
            phase=R.functional(ring_polynomial(R,H,[(z>>(R.m*i))&mask for i in range(b)]))^polynomial_value(Q,z)
            assert phase==evaluate(x)
        result.update(metadata,raw_input_file=source.name,pointwise_checks=1024)
        cases.append(result)
        Path(__file__).with_name('contact_counter_results.json').write_text(json.dumps(dict(
            status='all completed assertions passed',raw_cases=cases,practical_speed_claim=False),indent=2)+'\n')
        print(json.dumps(dict(n=n,b=b,rank=metadata['planted_error_rank'],signed=result['signed_count'],
            kernel=result['count_certificate']['geometry']['critical_kernel_dimension'],
            rays=result['count_certificate']['projective_ray_count'],seconds=result['seconds'])),flush=True)
    return cases


def run_small():
    cases=[]
    for h,e,b,seed in [(3,2,5,12002),(3,3,5,12003),(7,2,5,12004),(3,2,7,12007)]:
        R=ChainRing(h,e);n=b*R.m;rng=random.Random(seed)
        P=contact_polynomial(R,b,'one-ray',rng);Q,_,rank=compatible_noise(R,b,rng,seed&1)
        count,certificate=weighted_contact_sum(h,e,P,Q,b);mask=(1<<R.m)-1
        def evaluate(x):return R.functional(ring_polynomial(R,P,[(x>>(R.m*i))&mask for i in range(b)]))^polynomial_value(Q,x)
        raw=extract_anf(evaluate,n);reference=truth_sum(raw,n);assert count==reference
        cases.append(dict(n=n,d=R.d,e=e,b=b,rank=rank,signed_count=count,
                          exhaustive_assignments=1<<n,certificate=certificate))
    Path(__file__).with_name('contact_small_results.json').write_text(json.dumps(dict(
        coefficient_cases=cases,total_truth_assignments=sum(a['exhaustive_assignments'] for a in cases)),indent=2)+'\n')
    print(json.dumps(dict(small_cases=len(cases),truth_assignments=sum(a['exhaustive_assignments'] for a in cases))),flush=True)


if __name__=='__main__':run_small();run_raw()

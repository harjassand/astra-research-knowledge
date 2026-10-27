#!/usr/bin/env python3
"""Executed acquisition and counting oracles for the repeated-pair terminal."""
from acquired_pair_terminal import *
from field_kloosterman import irreducible_binary
import json,random
import numpy as np


def field_modulus(d):
    return next(h for h in range((1<<d)|1,1<<(d+1),2) if irreducible_binary(h))


def base_polynomial(b,negative_pairs):
    P={};m=b-1
    for pair,i in enumerate(range(0,m,2)):
        for indices in [(i,i,i),(i,i+1,i+1),(i+1,i+1,i+1),(i,i+1,m)]:
            add_coefficient(P,exponent(b,indices),1)
        if pair<negative_pairs:
            for indices in [(i,i,m),(i+1,i+1,m)]:add_coefficient(P,exponent(b,indices),1)
    return P


def random_invertible_field(b,h,rng):
    B=identity(b);q=1<<(h.bit_length()-1)
    for _ in range(10*b):
        i,j=rng.sample(range(b),2);c=rng.randrange(1,q)
        B[i]=[x^gf_mul(c,y,h) for x,y in zip(B[i],B[j])]
    return B


def full_field_sum(h,P):
    b=len(next(iter(P)));d=h.bit_length()-1;q=1<<d
    table=np.array([[gf_mul(x,y,h) for y in range(q)] for x in range(q)],dtype=np.uint8)
    points=np.arange(q**b,dtype=np.uint32)
    coordinates=[((points>>(d*i))&(q-1)).astype(np.uint8) for i in range(b)]
    accumulator=np.zeros(q**b,dtype=np.uint8)
    for a,c in P.items():
        term=np.full(q**b,c,dtype=np.uint8)
        for i,power in enumerate(a):
            for _ in range(power):term=table[term,coordinates[i]]
        accumulator^=term
    trace=np.array([gf_trace(x,h) for x in range(q)],dtype=np.uint8)
    ones=int(np.sum(trace[accumulator],dtype=np.int64))
    return q**b-2*ones,q**b


def moment_expansion_check(h,gamma,tau,i,j,moment):
    d=h.bit_length()-1;q=1<<d;count=i+j;total=0
    for packed in range(q**(2*count+1)):
        z=packed&(q-1);remaining=packed>>d
        phase=gf_trace(gf_mul(tau,gf_mul(z,gf_mul(z,z,h),h),h),h)
        for pair in range(count):
            value=remaining&((1<<(2*d))-1);remaining>>=2*d
            phase^=pair_phase(h,gamma,z,pair>=i,value)
        total+=1-2*phase
    assert total==moment
    # Adding the Artin--Schreier coordinate produces q^variables+total zeros.
    return dict(positive_exponent=i,negative_exponent=j,
        character_points=q**(2*count+1),character_moment=total,
        artin_schreier_point_count=q**(2*count+1)+total)


def run():
    rng=random.Random(701245);cases=[];moment_checks=[]
    for d,b,negative,tau in [(1,5,0,0),(1,7,1,1),(2,5,0,0),(2,7,2,2),(4,5,0,0),(4,5,2,5)]:
        h=field_modulus(d);q=1<<d;P=base_polynomial(b,negative)
        if tau:add_coefficient(P,exponent(b,[b-1,b-1,b-1]),tau)
        B=random_invertible_field(b,h,rng);theta=rng.randrange(1,q)
        disguised={a:gf_mul(theta,c,h) for a,c in substitute(P,B,h).items()}
        certificate=acquire_pair_template(h,disguised)
        count,terminal=enumerated_terminal(certificate)
        oracle,points=full_field_sum(h,disguised)
        assert count==oracle,(d,b,negative,certificate,count,oracle)
        if d<=2:
            for i,j in [(1,0),(0,1),(1,1),(2,0),(0,2)]:
                moment_checks.append(dict(field_degree=d,gamma=certificate['gamma'],
                    **moment_expansion_check(h,certificate['gamma'],certificate['radial_cubic'],i,j,terminal['exact_joint_moments'][i][j])))
        cases.append(dict(field_degree=d,ring_variables=b,source_negative_pairs=negative,source_radial_cubic=tau,
            exact_signed_count=count,full_field_oracle_points=points,certificate=certificate,
            terminal=terminal,field_disguise=B,scalar=theta,
            input_polynomial=[dict(exponents=a,coefficient=c) for a,c in disguised.items()]))
    # A genuinely non-binary square coefficient keeps contact geometry and
    # the unique ray, but must fail this additional template certificate.
    bad=base_polynomial(5,0)
    bad[exponent(5,[0,0,4])]=2
    try:acquire_pair_template(7,bad)
    except ValueError as error:
        rejection=str(error)
        assert rejection=='quadratic square coefficients do not descend to F2'
    else:raise AssertionError('non-descending residue was accepted')
    # Larger fields validate acquisition only; no q-sized terminal is used.
    large=[]
    for d,b in [(5,9),(7,11),(8,9),(10,7),(11,7)]:
        h=field_modulus(d);q=1<<d;P=base_polynomial(b,0)
        B=random_invertible_field(b,h,rng);theta=rng.randrange(1,q)
        disguised={a:gf_mul(theta,c,h) for a,c in substitute(P,B,h).items()}
        certificate=acquire_pair_template(h,disguised)
        assert certificate['field_elements_enumerated_during_acquisition']==0
        large.append(dict(field_degree=d,ring_variables=b,original_binary_variables=b*d,
            certificate=certificate))
    result=dict(status='all assertions passed',counting_cases=cases,
        acquired_large_field_cases=large,moment_expansion_checks=moment_checks,
        rejected_nonbinary_square_coefficient=rejection,
        full_field_oracle_points=sum(c['full_field_oracle_points'] for c in cases),
        expanded_moment_character_points=sum(c['character_points'] for c in moment_checks),
        general_fixed_variable_point_count_backend_implemented=False,
        practical_speed_claim=False)
    Path(__file__).with_name('acquired_pair_terminal_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],counting_cases=len(cases),
        large_acquisition_cases=len(large),full_field_oracle_points=result['full_field_oracle_points'],
        moment_checks=len(moment_checks),expanded_moment_character_points=result['expanded_moment_character_points'],
        largest_binary_acquisition=max(c['original_binary_variables'] for c in large))))


if __name__=='__main__':run()

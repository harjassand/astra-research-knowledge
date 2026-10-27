#!/usr/bin/env python3
"""Independent polar, order-three sign, and moment-matrix audit.

All field scans are explicit small test oracles, not a point-count backend.
"""
from pathlib import Path
from fractions import Fraction
import json,sys
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_chain_root','work_stationary_prior_agent'):
    sys.path.insert(0,str(ROOT/folder))
from field_descent import gf_mul,gf_trace,span,linear_apply
from acquired_pair_terminal import (EIGHT_MOMENT_INDICES,symmetry_state_nodes,
    reconstruct_from_eight_moments,moment_terminal_eight,moment_terminal_reference49)


def det(matrix):
    A=[[Fraction(x) for x in row] for row in matrix];value=Fraction(1)
    for j in range(len(A)):
        p=next(i for i in range(j,len(A)) if A[i][j])
        if p!=j:A[p],A[j]=A[j],A[p];value=-value
        c=A[j][j];value*=c;A[j]=[x/c for x in A[j]]
        for i in range(j+1,len(A)):
            if A[i][j]:
                c=A[i][j];A[i]=[x-c*y for x,y in zip(A[i],A[j])]
    assert value.denominator==1
    return int(value)


def run():
    groups=[];nullities={};instances=0;truth_points=0
    for d,h in ((1,3),(2,7),(3,11),(4,19),(5,37)):
        q=1<<d;n=2*d
        gammas=list(range(1,q)) if d<=4 else [1,7,19]
        nodes=symmetry_state_nodes(d)
        matrix=[[u**i*v**j for u,v in nodes] for i,j in EIGHT_MOMENT_INDICES]
        determinant=det(matrix)
        assert abs(determinant)==2**15*3**7*q**14
        for gamma in gammas:
            fibers=[]
            for z in range(q):
                def phase(packed,minus):
                    x,y=packed&(q-1),packed>>d
                    x2,y2=gf_mul(x,x,h),gf_mul(y,y,h)
                    G=gf_mul(x2,x,h)^gf_mul(x,y2,h)^gf_mul(y2,y,h)
                    Q=gf_mul(x,y,h)^(x2^y2 if minus else 0)
                    return gf_trace(gf_mul(gamma,G^gf_mul(z,Q,h),h),h)
                tables=[[phase(x,minus) for x in range(q*q)] for minus in (False,True)]
                polars=[]
                for table in tables:
                    polars.append([sum((table[(1<<i)^(1<<j)]^table[1<<i]^table[1<<j])<<j
                                       for j in range(n)) for i in range(n)])
                assert polars[0]==polars[1]
                k=n-len(span(polars[0]));assert k in (0,2,4)
                nullities[k]=nullities.get(k,0)+1
                for packed in range(q*q):
                    x,y=packed&(q-1),packed>>d
                    rotated=y|((x^y)<<d)
                    assert tables[1][rotated]==tables[1][packed]
                    kernel=linear_apply(polars[0],packed)==0
                    if kernel:assert tables[1][packed]==0
                    x2,y2=gf_mul(x,x,h),gf_mul(y,y,h)
                    x4,y4=gf_mul(x2,x2,h),gf_mul(y2,y2,h);z2=gf_mul(z,z,h)
                    first=gf_mul(gamma,x4,h)^x^gf_mul(gamma,y4,h)^gf_mul(gamma,gf_mul(z2,y2,h),h)
                    second=x^gf_mul(gamma,y4,h)^y^gf_mul(gamma,gf_mul(z2,x2,h),h)
                    assert kernel==(first==0 and second==0)
                values=[q*q-2*sum(table) for table in tables]
                expected=(-1)**(d-k//2)*(q<<(k//2))
                assert values[1]==expected and tuple(values) in nodes
                fibers.append(values);instances+=1;truth_points+=2*q*q
            tau=gamma^1
            weights=[1-2*gf_trace(gf_mul(tau,gf_mul(z,gf_mul(z,z,h),h),h),h) for z in range(q)]
            moments={index:sum(w*a**index[0]*b**index[1] for w,(a,b) in zip(weights,fibers))
                     for index in EIGHT_MOMENT_INDICES}
            for positive,negative in ((0,0),(1,0),(0,1),(3,5),(20,31)):
                actual,counts=reconstruct_from_eight_moments(d,moments,positive,negative,signed=bool(tau))
                expected=sum(w*a**positive*b**negative for w,(a,b) in zip(weights,fibers))
                assert actual==expected
                for row in counts:
                    expected_mass=sum(w for w,pair in zip(weights,fibers)
                        if pair==[row['positive_value'],row['negative_value']])
                    assert row['signed_multiplicity']==expected_mass
            groups.append(dict(d=d,gamma=gamma,tau=tau,field_values_scanned=q,
                signed_zeroth_moment=moments[(0,0)],exact_evaluation_determinant=determinant))
    # Replay the completed deep-chain certificate with the new eight-moment
    # interface, independently comparing the retained 49-moment interface.
    path=Path(__file__).with_name('pair_terminal_deep_audit_results.json')
    result=json.loads(path.read_text());record=result['acquired_pair_records'][0]
    certificate=record['certificate'];moments=record['reference_scan']['exact_joint_moments']
    def backend(h,gamma,tau,i,j):
        assert (h,gamma,tau)==(certificate['field_modulus'],certificate['gamma'],certificate['radial_cubic'])
        return moments[i][j]
    reduced,counts=moment_terminal_eight(certificate,backend)
    full,_=moment_terminal_reference49(certificate,backend)
    assert reduced==full
    record['executed_eight_moment_replay']=dict(field_terminal_value=reduced,states=counts,
        exact_moment_backend='test-only replay of the explicit 16-element field scan',
        agrees_with_retained_49_moment_reconstruction=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    audit=dict(status='all exact assertions passed',gaussian_instances=instances,
        exhaustive_pair_phase_evaluations=truth_points,polar_nullity_histogram=nullities,
        gamma_and_signed_moment_groups=groups,
        evaluation_determinant_absolute_formula='2^15 * 3^7 * q^14',
        deep_chain_eight_moment_replay=True,general_point_count_backend_implemented=False)
    Path(__file__).with_name('eight_state_audit_results.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps({k:v for k,v in audit.items() if k!='gamma_and_signed_moment_groups'}))


if __name__=='__main__':run()

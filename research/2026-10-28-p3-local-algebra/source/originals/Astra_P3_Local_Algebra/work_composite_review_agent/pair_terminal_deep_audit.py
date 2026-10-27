#!/usr/bin/env python3
"""Audit the pair certificate after a raw deep-chain affine disguise.

The test moment oracle scans 16 field values. It is not an implementation
or execution of the polynomial-time Lauder--Wan backend.
"""
from pathlib import Path
import itertools,json,random,sys,time
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_chain_root','work_stationary_prior_agent'):
    sys.path.insert(0,str(ROOT/folder))
from acquired_contact_counter import (
    ChainRing,compile_contact,weighted_contact_sum,degree_exponents,quadratic_coefficients,
    ring_polynomial,polynomial_value,linear_apply,gf_mul)
from acquired_pair_terminal import acquire_pair_template,enumerated_terminal,moment_terminal_eight
from acquired_pair_terminal_checks import base_polynomial,full_field_sum
from field_descent import extract_anf,random_invertible


def run():
    h,d,e,b=19,4,4,5;R=ChainRing(h,e);n=b*R.m;rng=random.Random(259421)
    residue=base_polynomial(b,1)
    residue={alpha:gf_mul(7,c,h) for alpha,c in residue.items()}
    H={alpha:residue.get(alpha,0)^(rng.getrandbits(R.m-d)<<d)
       for alpha in degree_exponents(b,3)}
    H={alpha:c for alpha,c in H.items() if c}
    qn=b*d;factors=random_invertible(qn,rng)
    def low_phase(x):
        z=sum(((x>>(R.m*i))&R.mask)<<(d*i) for i in range(b))
        return 1^(sum(((a&z).bit_count()&1)*((c&z).bit_count()&1)
                      for a,c in zip(factors[::2],factors[1::2]))&1)
    Q=quadratic_coefficients(low_phase,n)
    field_truth,field_points=full_field_sum(h,residue)
    reference,reference_certificate=weighted_contact_sum(h,e,H,Q,b,terminal_bit_budget=0,
        field_terminal=lambda leaf_h,leaf_b,leaf_H:field_truth)
    columns=random_invertible(n,rng);offset=rng.getrandbits(n);mask=(1<<R.m)-1
    def evaluator(x):
        y=linear_apply(columns,x)^offset
        values=[(y>>(R.m*i))&mask for i in range(b)]
        return R.functional(ring_polynomial(R,H,values))^polynomial_value(Q,y)
    print(json.dumps(dict(stage='manufacturing raw affine-disguised ANF',n=n)),flush=True)
    raw=extract_anf(evaluator,n)
    records=[]
    def terminal(field_h,module_rank,field_H):
        certificate=acquire_pair_template(field_h,field_H)
        exact,scan=enumerated_terminal(certificate)
        moments=scan['exact_joint_moments']
        def replay(h1,gamma,tau,i,j):
            assert (h1,gamma,tau)==(field_h,certificate['gamma'],certificate['radial_cubic'])
            return moments[i][j]
        reconstructed,distribution=moment_terminal_eight(certificate,replay)
        assert reconstructed==exact
        assert distribution==scan['eight_state_multiplicities']
        records.append(dict(certificate=certificate,reference_scan=scan,
            exact_moment_backend='test-only explicit field-scan replay'))
        return reconstructed
    print(json.dumps(dict(stage='acquiring raw chain and pair terminal',raw_terms=len(raw))),flush=True)
    started=time.perf_counter()
    result=compile_contact(raw,n,terminal_bit_budget=0,field_terminal=terminal)
    assert result['signed_count']==reference and len(records)==1
    assert result['field_degree']==d and result['chain_length']==e and result['module_dimension']==b
    assert result['count_certificate']['geometry']['critical_kernel_dimension']==0
    # Verify the manufactured ordinary field coefficient identity directly,
    # including the phase scale and all transformed square coefficients.
    assert records[0]['certificate']['field_elements_enumerated_during_acquisition']==0
    result.update(status='all exact assertions passed',planted_quadratic_rank=qn,
        planted_higher_coefficients_arbitrary=True,planted_field_scale=7,
        raw_binary_affine_disguise=True,independent_field_truth_assignments=field_points,
        reference_signed_count=reference,reference_chain_certificate=reference_certificate,
        acquired_pair_records=records,original_chain_count_exhaustively_enumerated=False,
        general_point_count_backend_implemented=False,practical_speed_claim=False,
        audit_seconds=time.perf_counter()-started)
    Path(__file__).with_name('pair_terminal_deep_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(n=n,d=d,e=e,b=b,noise_rank=qn,signed_count=result['signed_count'],
        candidate_count=result['count_certificate']['candidate_count'],
        projective_rays=result['count_certificate']['projective_ray_count'],
        acquired_gamma=records[0]['certificate']['gamma'],
        moment_field_values_enumerated=records[0]['reference_scan']['field_elements_enumerated'],
        audit_seconds=result['audit_seconds'])),flush=True)


if __name__=='__main__':run()

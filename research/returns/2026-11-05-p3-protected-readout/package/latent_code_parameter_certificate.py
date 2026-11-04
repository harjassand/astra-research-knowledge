"""Exact rational certificate for one finite acquired-code learning point.

This is an analytic parameter check, not a simulation or hardware benchmark.
The separate specimen-source preparation failure budget delta_src is excluded.
Local source faults may already be counted in q; uncounted logical/nonlocal
source failures must be added separately as delta_src.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json


def certify():
    k,d,R,S=32,19,74,260000
    n=k*d*d
    q=F(3,1000);qc=q
    r_upper=F(329,1000)
    assert 36*q<r_upper*r_upper and r_upper<1
    g=F(1,2)-8*qc
    assert g>0
    M=sum(3**w*comb(n,w) for w in range(1,5))
    all_rows=R*F(8*n,3)*r_upper**d/(1-r_upper)
    rank_failure=F(1,2**(R-1-2*k))
    t=S*g*g/1296
    # exp(t) >= sum_{j=0}^m t^j/j!, with every operation exact.
    term=F(1);exp_lower=F(1);m=0
    calibration_target=F(3274,1000000)
    while 3*M/exp_lower>=calibration_target:
        m+=1
        assert m<1000
        term*=t/m;exp_lower+=term
    calibration=3*M/exp_lower
    assert calibration<calibration_target
    assert all_rows<F(2280,1000000)
    assert rank_failure<F(1954,1000000)
    total=calibration+all_rows+rank_failure
    assert total<F(7508,1000000)<F(1,100)
    return {
        'arithmetic':'fractions.Fraction; no floating-point comparison enters any assertion',
        'acquisition_method':'Sample-minimizing all-candidate product-measurement bound; this is not the sparse collision learner',
        'logical_qubits':k,'distance':d,'physical_qubits_per_copy':n,
        'q':str(q),'q_c':str(qc),'six_sqrt_q_rational_upper':str(r_upper),
        'calibration_copies':S,'Bell_rows':R,'total_source_copies':S+2*R,
        'physical_Bell_gates':n*R,'calibration_wire_readouts':n*S,
        'candidate_Paulis':M,'calibration_gap':str(g),
        'exp_lower_bound_Taylor_degree':m,
        'calibration_failure_upper_rational':str(calibration),
        'all_rows_failure_upper_rational':str(all_rows),
        'rank_failure_upper_rational':str(rank_failure),
        'total_failure_upper_rational':str(total),
        'decimal_display_only':{
            'calibration_failure_upper':float(calibration),
            'all_rows_failure_upper':float(all_rows),
            'rank_failure_upper':float(rank_failure),
            'total_failure_upper':float(total)},
        'specimen_source_failure_delta_src_included':False,
        'full_failure_bound':'the reported learning/readout bound plus the separately supplied delta_src',
        'scope':'This point is not the smaller finite simulation. It certifies the stated stochastic-support model and does not certify a physical device or specimen preparation.'}


if __name__=='__main__':
    result=certify()
    Path(__file__).with_name('latent_code_parameter_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    short={k:v for k,v in result.items() if not k.endswith('_rational')}
    print(json.dumps(short,indent=2))

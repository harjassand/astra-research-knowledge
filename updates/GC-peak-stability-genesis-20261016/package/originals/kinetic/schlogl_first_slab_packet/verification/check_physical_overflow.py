#!/usr/bin/env python3
"""Independently reconstruct the same-model Lyapunov cap bound, exactly.

No acquired producer or audit code is imported or executed. See REPORT.md for
the all-state diffusion inequality and localized Dynkin/nonexplosion argument.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse
import hashlib
import json
import verify_slab as v

def run(a):
    r=F(161,100)
    b=[F('108.102'),-F('2.676'),F('2.676'),F(0)]
    d=[F(0),F('37.961'),-F('0.120'),F('0.040')]
    c=[b[k]*(r-1)+d[k]*(1/r-1) for k in range(4)]
    c[1]+=3*v.DIFF*(r+1/r-2)
    tail=[sum((c[k]*comb(k,j)*111**(k-j) for k in range(j,4)),F(0)) for j in range(4)]
    assert all(x<0 for x in tail) # F_r(111+k)<0 for all real k>=0.
    def rate(m): return sum((c[k]*m**k for k in range(4)),F(0))
    assert all(rate(m)==v.birth(m)*(r-1)+v.death(m)*(1/r-1)+3*v.DIFF*m*(r+1/r-2) for m in range(111))
    vals=[r**m*rate(m) for m in range(111)]
    K=max(vals); argmax=[m for m,z in enumerate(vals) if z==K]
    assert argmax==[103]
    assert max(sum(i in e for e in v.EDGES) for i in range(8))==3
    epsilon=lambda t: (8*r**50+8*K*t)/r**163
    eps1=epsilon(F(1)); assert eps1<F('1e-9')
    source=json.loads(Path(a.source_audit).read_text())
    assert source['source_mapping']['coefficients']['C1']['rational']==str(F('2.676'))
    assert source['source_mapping']['coefficients']['C2']['rational']==str(F('0.040'))
    assert source['source_mapping']['coefficients']['C3']['rational']==str(F('108.102'))
    assert source['source_mapping']['coefficients']['C4']['rational']==str(F('37.881'))
    assert source['source_mapping']['coefficients']['D']['rational']==str(v.DIFF)
    assert set(map(tuple,source['source_mapping']['directed_edges']))==set((a,b) for i,j in v.EDGES for a,b in ((i,j),(j,i)))
    assert F(source['certificate']['K']['rational'])==K
    assert F(source['certificate']['epsilon']['rational'])==eps1
    s=v.Slab(a.manifest)
    assert s.a==0
    endpoint=v.p_eval(s.overflow_power(),F(1)); epsh=epsilon(s.h)
    lower=max(F(0),endpoint.lo-epsh)
    report={
        'status':'PASS_EXACT_PHYSICAL_STATE_ERROR_REJECTION',
        'r_exact':str(r),
        'F_coefficients_low_to_high':list(map(str,c)),
        'F_at_111_plus_k_coefficients_low_to_high':list(map(str,tail)),
        'tail_coefficients_strictly_negative':True,
        'finite_maximization_counts':111,
        'maximizers':argmax,
        'K_exact':str(K),
        'overflow_bound_T1':v.fraction_json(eps1),
        'overflow_bound_slab_h':v.fraction_json(epsh),
        'exported_overflow_endpoint':v.interval_json(endpoint),
        'actual_augmented_state_l1_error_lower':v.fraction_json(lower),
        'actual_augmented_state_l1_error_lower_using_T1_bound':v.fraction_json(max(F(0),endpoint.lo-eps1)),
        'success_coordinate_error_lower_claimed':False,
        'applies_to':'Same eight-site decimal generator and initial all 50. Unconditional first crossing of count 163 upper-bounds overflow before target absorption.',
        'proof':'Symmetric-edge exponential inequality; degree <= 3; all-real polynomial tail negativity; exact finite maximum; localized stopped finite-chain Dynkin; coercive bound implies nonexplosion.',
        'source_audit_path':str(Path(a.source_audit)),
        'source_audit_sha256':hashlib.sha256(Path(a.source_audit).read_bytes()).hexdigest(),
        'candidate_sha256':hashlib.sha256(s.npz_path.read_bytes()).hexdigest(),
        'source_exact_numbers_matched':True,
        'acquired_code_executed':False,
        'new_simulation_or_fit':False,
    }
    Path(a.output).write_text(json.dumps(report,indent=2))
    print(json.dumps({k:z for k,z in report.items() if k!='K_exact'},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest');p.add_argument('--source-audit',required=True);p.add_argument('--output',required=True);run(p.parse_args())

#!/usr/bin/env python3
"""Exact unit/integration checks, deliberately a small CPU workload."""
import hashlib,json,random,time
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp
from probability_budget import build_budget,assert_budget,is_psd,determinant,enc
from certified_normal import CertifiedNormal,selftest
HERE=Path(__file__).resolve().parent

def main():
    started=time.perf_counter();rows=[]
    for p,n,m,r in [(128,128,2,62),(64,64,1,16),(128,140,3,64)]:
        h=[[Q((i+1)*3) if i==j else Q(0) for j in range(m)] for i in range(m)]
        for eps in [Q(1,2),Q(1,16),Q(1,1<<24)]:
            b=build_budget(h,p,n,r,eps);assert assert_budget(b)
            rows.append({'m':m,'p':p,'n':n,'r':r,'epsilon':str(eps),
              'rho_bits':b['primitive_error_bits'],'uniform_bits':b['normal_uniform_bits'],
              'trial_cap':b['trial_cap']})
    # PSD tests include semidefinite zero pivots and an indefinite zero pivot.
    assert is_psd([[0,0],[0,1]]) and not is_psd([[0,1],[1,1]])
    assert is_psd([[2,1],[1,2]]) and not is_psd([[1,2],[2,1]])
    assert determinant([[2,1],[1,2]])==3
    bad_inputs=0
    for h,p,n,r,eps in [([[1,1],[1,1]],128,128,62,Q(1,16)),
                        ([[1,0],[0,1]],64,64,16,Q(1,16)),
                        ([[1]],16,16,16,Q(1))]:
        try:build_budget(h,p,n,r,eps)
        except AssertionError:bad_inputs+=1
        else:raise AssertionError('Invalid theorem input was accepted')
    assert bad_inputs==3
    normal=selftest();boundary=[]
    tiny=CertifiedNormal(20,2)
    low,high=tiny.cdf(Q(1,1<<10000))
    assert low<=Q(1,2)<=high
    majorant=tiny.majorant_proof
    assert majorant['tail_at_cap_upper']<=majorant['tail_stop_threshold']
    assert majorant['final_CDF_width_upper']<=majorant['required_CDF_width']
    # Cells nearest the analyzed tail boundary must still certify. The bracket
    # itself is proved by exact CDF inequalities; mp merely chooses test inputs.
    for bits,L0 in [(20,2),(80,6),(280,9),(553,13)]:
        g=CertifiedNormal(bits,L0)
        for sign in (-1,1):
            with mp.workprec(g.uniform_bits+100):
                u=(1+mp.erf(mp.mpf(sign*L0)/mp.sqrt(2)))/2
                k=int(mp.floor(u*(1<<g.uniform_bits)))
            c=g.from_cell(k);assert not c['fallback']
            lo,hi=c['interval'];assert c['cdf_upper_at_lower']<=Q(k,1<<g.uniform_bits)
            assert c['cdf_lower_at_upper']>=Q(k+1,1<<g.uniform_bits)
            boundary.append({'rho_bits':bits,'L0':L0,'sign':sign,'passed':True})
    result={'exact_budget_tests_passed':True,'budget_cases':rows,'invalid_inputs_rejected':bad_inputs,
      'normal_tests':normal,'analyzed_tail_boundary_cells':boundary,
      'runtime_seconds':time.perf_counter()-started,
      'source_sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in
         ['probability_budget.py','certified_normal.py','test_probability_budget.py','check_global_contract.py']},
      'scope':'Tests establish stated exact inequalities, not empirical evidence of the output distribution.'}
    (HERE/'PROBABILITY_BUDGET_TESTS.json').write_text(json.dumps(enc(result),indent=2)+'\n')
    print(json.dumps({'exact_budget_tests_passed':True,'budget_cases':len(rows),
      'normal_cells':12+len(boundary),'invalid_inputs_rejected':bad_inputs,'runtime_seconds':result['runtime_seconds']},indent=2))
if __name__=='__main__':main()

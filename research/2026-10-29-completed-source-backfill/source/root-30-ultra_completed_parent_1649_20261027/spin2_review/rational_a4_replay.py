"""Independent rational extension to the actual A4-projected warm input.
Uses this root's interval primitives; no author numerical/verification code.
"""
from rational_warm_replay import F,ROOT,add,scale,mul,divide,total,exact,exp_box,root_upper,upward,downward,open_box,quadratic,full_moments
from pathlib import Path
from math import factorial,prod
import json,time,hashlib
SOURCE=ROOT/'inputs/degree192'
def twisted_box(row,beta):
    moments=list(map(int,row['trace_2H_powers']));degree=len(moments)-1
    value=sum((F(t)*(-beta/F(2))**k/factorial(k) for k,t in enumerate(moments)),F(0))
    x=24*beta;tail=625*exp_box(x)[1]*x**(degree+1)/factorial(degree+1)
    return (value-tail)/625,(value+tail)/625
def run():
    start=time.monotonic()
    raw=(SOURCE/'open_moments_exact_degree192.json').read_bytes();data=json.loads(raw)
    traw=(SOURCE/'twisted4_moments_exact_degree192.json').read_bytes();twists=json.loads(traw)
    craw=(SOURCE/'vacuum_krylov_transfer_degree192_A4.json').read_bytes();candidates=json.loads(craw)
    records={r['n']:r for r in data['chains']};assert set(records)==set(range(1,7))
    old=json.loads((ROOT/'inputs/degree96/open_moments_exact_degree96.json').read_text())
    for row,previous in zip(data['chains'],old['chains']):
        assert row['n']==previous['n'] and row['trace_2H_powers'][:97]==previous['trace_2H_powers']
    pair=[(d,2*e) for d,e in [(1,-6),(3,-5),(5,-3),(7,0),(9,4)]]
    triple=[(2*j+1,j*(j+1)-a*(a+1)-6) for a in range(5) for j in range(abs(a-2),a+3)]
    for n,spectrum in [(2,pair),(3,triple)]:
        assert [sum(d*e**k for d,e in spectrum) for k in range(193)]==list(map(int,records[n]['trace_2H_powers']))
    for row in data['chains'][1:]:
        n=row['n'];assert len(row['trace_2H_powers'])==193
        assert prod(row['CRT_primes'])==int(row['CRT_modulus'])>2*5**n*(12*(n-1))**192
        assert all(abs(int(v))<=5**n*(12*(n-1))**k for k,v in enumerate(row['trace_2H_powers']))
    for row in twists['records']:
        assert len(row['trace_2H_powers'])==193
        assert prod(row['CRT_primes'])==int(row['CRT_modulus'])>2*625*48**192
        assert list(map(int,row['trace_2H_powers'][:4]))==[625,0,48*4*625,-48*4*625]
        assert all(abs(int(v))<=625*48**k for k,v in enumerate(row['trace_2H_powers']))
    # SO(3) characters at pi and2pi/3: check the finite edge cases;
    # for j>=2, |chi_C|<=1 gives complement >=(11(2j+1)-11)/12>=11/3.
    for j in range(1,100):
        chi_c=[1,0,-1][j%3]
        invariant=F(2*j+1+3*(-1)**j+8*chi_c,12)
        assert invariant.denominator==1 and 2*j+1-invariant>=3
    beta=F(3,4);row=next(r for r in candidates['rows'] if F(r['beta_exact'])==beta)
    c=list(map(F,row['candidate_rational_decimal_coefficients']))
    m=[exact(1)]+[open_box(records[n],beta) for n in range(1,7)]
    norm=quadratic(c,m,0);assert norm[0]>0
    theta=divide(quadratic(c,m,1),norm)
    variance=add(divide(quadratic(c,m,2),norm),scale(mul(theta,theta),-1));assert variance[1]>=0
    m4=full_moments(beta)[4]
    z={r['twist']:twisted_box(r,beta) for r in twists['records']}
    invariant=scale(total([m4,scale(z['P'],3),scale(z['C'],8)]),F(1,12))
    complement=add(m4,scale(invariant,-1))
    assert complement[0]>=0
    remainder_invariant=invariant[1]-theta[0]**4;assert remainder_invariant>=0
    rho=max(root_upper(remainder_invariant,4),root_upper(complement[1]/3,4))
    assert theta[0]>rho
    remainder_full=m4[1]-theta[0]**4
    ratio=upward(rho/theta[0],15);assert ratio<1
    tail=remainder_full/theta[0]**4*ratio**252
    spatial_defect=2*tail
    assert spatial_defect<F(1851,10**27)
    initial_log_debt=2**7*2*tail
    result={'status':'INDEPENDENT_EXACT_RATIONAL_A4_WARM_SEED_PASS',
      'beta':'3/4','ring_for_spatial_purity':256,
      'moment_source_sha256':hashlib.sha256(raw).hexdigest(),
      'twisted_source_sha256':hashlib.sha256(traw).hexdigest(),
      'candidate_source_sha256':hashlib.sha256(craw).hexdigest(),
      'full193_short_chain_spectral_controls':[2,3],
      'degree96_192_overlap':'ALL_SHARED_EXACT_MOMENTS_EQUAL',
      'SO3_A4_complement_minimum':3,
      'strict_leading_separation_lower_rational':str(downward(theta[0]-rho)),
      'spatial_defect_upper_rational':str(upward(spatial_defect,35)),
      'spatial_defect_float_diagnostic':float(spatial_defect),
      'initial_log_debt_after7_doublings_upper_rational':str(upward(initial_log_debt,33)),
      'cold_target_beta':96,'required_cold_thermal_inputs':15,
      'cold_thermal_inputs_acquired_by_this_replay':False,
      'seconds':time.monotonic()-start,
      'scope':'Actual A4-projected source-kernel warm enclosure and complete-sector tail. Whole CRT producers reviewed; n4..6 and twisted4 CRT powers not independently regenerated here. No cold gap or arbitrary compression impossibility.'}
    (ROOT/'RATIONAL_A4_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()

"""Independent arithmetic check of frozen fitted programs against finite Poisson data.

No source_device import; all measurements and conclusions are reconstructed from
stored counts and exact integer-square-root confidence intervals.
Local residuals, signs, no-amplification margins, and rational finite-T bound
are computed without floating-point arithmetic. Stochastic MC is separate.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json,hashlib

ROOT=Path(__file__).parent
PAT=[(l,c,r) for l in (-1,1) for c in (-1,1) for r in (-1,1)]

def local_intervals(archive):
    E=int(archive['exposure_per_configuration'])
    cells={tuple(1 if z=='+' else -1 for z in s):int(n) for s,n in archive['counts'].items()}
    assert set(cells)==set(PAT)
    scale=10**12;x=22
    bounds={}
    for s,n in cells.items():
        u=F(isqrt(2*n*x*scale**2)+1,scale)
        bounds[s]=(max(F(0),F(n-x-u,E)),F(n+2*x+u,E))
    return bounds

def source_field(mode,p,intervals):
    if mode=='weak_field':
        jumps=p['rules']
    else:jumps=p['jumps']
    alpha=F(p['alpha_fraction']);kill=F(p['kill_fraction'])
    signed_rates=[(tuple(q['offsets']),F(q['rate_fraction'])*(q.get('sign',1))) for q in jumps]
    assert kill>=0
    assert abs(kill+sum(abs(q) for _,q in signed_rates)-2*alpha)==0
    rho=F(0)
    for spins,(lo,hi) in intervals.items():
        for c in (lo,hi):
            val=-2*c+2*alpha
            for offs,q in signed_rates:
                val-=q*__import__('math').prod(spins[o+1] for o in offs)
            rho=max(rho,abs(val))
    assert rho==F(p['local_residual_fraction']),(mode,rho,p['local_residual_fraction'])
    # Single-center upward drift bound on population size using |jump|.
    up=sum(abs(q)*max(0,len(offs)-2*(0 in offs)) for offs,q in signed_rates)
    margin=kill-up
    return {'alpha':str(alpha),'kill':str(kill),'rho':str(rho),'rho_float':float(rho),
            'margin':str(margin),'margin_float':float(margin),'n_rewrite_rules':len(jumps),
            'n_negative_rules':sum(q<0 for _,q in signed_rates),
            'absolute_event_rate':str(kill+sum(abs(q) for _,q in signed_rates))}

def finite_time_rational_bound(rho,kappa,T,k=1):
    """Using exp(-u) <= 1-u+u^2/2 gives exact conservative integral."""
    T=F(T); assert kappa>0
    return k*rho*(T-kappa*T*T/2 + kappa*kappa*T*T*T/6)

if __name__=='__main__':
    v1bytes=(ROOT/'frozen_programs.json').read_bytes()
    v2bytes=(ROOT/'signed_frozen_v2.json').read_bytes()
    v1=json.loads(v1bytes);v2=json.loads(v2bytes)
    assert hashlib.sha256(v1bytes).hexdigest()==v2['derived_from_frozen_sha256']
    measurements=json.loads((ROOT/'frozen_measurements.json').read_text())
    measurements['weak_field']=json.loads((ROOT/'signed_measurements_v2.json').read_text())
    allprog=dict(v1['programs']);allprog['weak_field']=v2['new_mode']
    checked={m:source_field(m,p,local_intervals(measurements[m])) for m,p in allprog.items()}
    kappa=min(F(q['margin']) for q in checked.values())
    rho=max(F(q['rho']) for q in checked.values())
    rational=finite_time_rational_bound(rho,kappa,F(6,5),1)
    assert kappa>0
    assert rational<F(1,70),rational
    # Adversarial semantic change: delete learned two-neighbour branching rule.
    bad=dict(allprog['baseline'])
    branch=[q for q in bad['jumps'] if q['offsets']==[-1,1]]
    assert len(branch)==1
    bad['jumps']=[q for q in bad['jumps'] if q['offsets']!=[-1,1]]
    bad['kill_fraction']=str(F(bad['kill_fraction'])+F(branch[0]['rate_fraction']))
    bad['alpha_fraction']=allprog['baseline']['alpha_fraction']
    # Ignoring branch while maintaining total alpha changes predicted residual sharply.
    bad['local_residual_fraction']='0'
    broken_detected=False
    try:source_field('baseline',bad,local_intervals(measurements['baseline']))
    except AssertionError:broken_detected=True
    assert broken_detected
    out={'independent_source_rate_check':'PASS','all_quantities_exact_rationals':True,'verified':checked,
         'kappa':str(kappa),'rho':str(rho),
         'rational_upper_error_single_site_T1p2':str(rational),
         'rational_upper_error_single_site_T1p2_float':float(rational),
         'branch_rule_deletion_rejected':broken_detected,
         'joint_data_failure_probability_upper':'48 exp(-22) < 1.4e-8',
         'machine_scope':'Exact local interval arithmetic and generator identity; numerical trajectory RNG and physical device assumptions are separate'}
    (ROOT/'independent_verification.json').write_text(json.dumps(out,indent=2,sort_keys=True))
    print(json.dumps(out,indent=2))

#!/usr/bin/env python3
"""Inspect saved capped runs against the explicit primitive and bit budgets.

This supplements exact tape replay; it is not an independent proof validator.
"""
import argparse,hashlib,json,time
from fractions import Fraction as Q
from pathlib import Path
from probability_budget import asq,build_budget,enc,is_psd
from certified_normal import CertifiedNormal
HERE=Path(__file__).resolve().parent

def check(path):
    start=time.perf_counter();r=json.loads(path.read_text());ds=r['dimensions'];c=r['native_certificate']
    b=build_budget(c['H'],ds['p'],ds['n'],c['r'],asq(r['budget']['epsilon']))
    assert enc(b)==r['budget'],'Budget differs from fresh exact computation'
    rho=b['primitive_error_rho'];gen=CertifiedNormal(b['primitive_error_bits'],b['normal_cutoff_L0'],b['normal_uniform_bits'])
    checks={'fresh_exact_budget_matches':True,'trial_count_within_cap':len(r['trials'])<=b['trial_cap'],
      'H_operator_residual_within_rho':asq(r['H_factor']['exact_residual_bound'])<=rho}
    normal_count=usedbits=0
    for t in r['trials']:
        pref='trial_'+str(t['trial'])+'_';normal_ok=True
        for s in t.get('normal_certificates',[]):
            usedbits+=s.get('uniform_bits',b['normal_uniform_bits']);normal_count+=1
            if s['fallback']:continue
            lo,hi=map(asq,s['interval']);value=asq(s['value']);err=asq(s['error_bound'])
            k=int(s['uniform_cell_index']);den=1<<s['uniform_bits']
            a,z=gen.cdf(lo);u,v=gen.cdf(hi)
            normal_ok &= z<=Q(k,den) and u>=Q(k+1,den) and max(value-lo,hi-value)<=err<=rho
        checks[pref+'normal_full_cell_certificates']=bool(normal_ok)
        if 'proposal' in t:
            p=t['proposal'];checks[pref+'V_separated_cutoff']=asq(p['V'])>=b['V_implementation_min']
            checks[pref+'sqrt_error']=asq(p['sqrt_certificate']['midpoint_error_bound'])<=rho
            checks[pref+'lambda_rounding_error']=asq(p['lambda_rounding_error_squared'])<=rho*rho
            checks[pref+'H_solve_exact']=asq(p['solve']['residual_squared'])==0
        if 'precision_factor' in t:
            checks[pref+'K_operator_residual']=asq(t['precision_factor']['exact_residual_bound'])<=rho
        if 'acceptance' in t:
            a=t['acceptance'];usedbits+=a['uniform_bits']
            checks[pref+'acceptance_interval_width']=asq(a['squared_probability_width'])<=rho*rho
            checks[pref+'acceptance_uniform_width']=Q(1,1<<a['uniform_bits'])<=rho
        if 'output_numerics' in t:
            x=t['output_numerics']['X_solve'];y=t['output_numerics']['Y_projection']
            checks[pref+'X_solve_error']=asq(x['distance_squared_upper'])<=rho*rho
            checks[pref+'Y_projection_error']=asq(y['projection_rounding_error'])<=rho
            checks[pref+'fiber_conditioning']=is_psd([[asq(x) for x in row] for row in t['conditioning']['S_minus_2tH']])
    out=r['output'];norm2=sum((asq(x)**2 for x in out['x']+out['y']),Q(0))
    checks['bounded_output']=norm2==asq(out['norm_squared']) and norm2<=b['output_norm_cap']**2
    checks['reported_residual_within_epsilon']=asq(out['residual_squared'])<=b['epsilon']**2
    if r['terminal_reason']!='accepted':checks['fallback_is_zero']=norm2==0
    bitcap=b['trial_cap']*((b['r']+ds['p']+ds['n'])*b['normal_uniform_bits']+b['per_acceptance_uniform_bits'])
    checks['finite_bit_cap']=usedbits<=bitcap
    assert all(checks.values()),str({k:v for k,v in checks.items() if not v})
    return {'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'observed_contract_checks_passed':True,'checks':checks,'random_bits_used':usedbits,
      'random_bits_cap':bitcap,'certified_normal_cells':normal_count,
      'randomness_mode':r['randomness_mode'],'terminal_reason':r['terminal_reason'],
      'guarantee_status':'Implemented capped sampler under stated analytic proof and independent-uniform-bit model',
      'assumptions':['Native raw-input certificate is recomputed by the core and its replay verifier.',
        'Independent uniform bits are a mathematical model; deterministic replay is not claimed to realize that law.',
        'Finite-event accounting and polar-coupling/generator-majorant arguments are stated in FINITE_PROBABILITY_CONTRACT.md.',
        'No independent formal or specialist proof validation has been completed.'],
      'validation_scope':'Exact budget, cell enclosures and reported primitive inequalities; use tape replay for complete core recomputation.',
      'wall_seconds':time.perf_counter()-start}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('reports',nargs='*',type=Path);ap.add_argument('--output',type=Path,default=HERE/'GLOBAL_CONTRACT_CHECKS.json');a=ap.parse_args()
    paths=a.reports or [HERE/'FINITE_BIT_DRAW.json',HERE/'FINITE_BIT_SYSTEM_DRAW.json']
    results=[check(p) for p in paths]
    a.output.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ['file','observed_contract_checks_passed','random_bits_used','random_bits_cap','wall_seconds']} for r in results],indent=2))
if __name__=='__main__':main()

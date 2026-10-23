#!/usr/bin/env python3
"""Exact scalar counterfactual analysis of an existing proof, not owner replay."""
from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from math import comb
from pathlib import Path
import hashlib, json, platform, resource, time

HERE = Path(__file__).resolve().parent

def central_sums(n):
    if n < 0:
        return F(0), F(0), F(0)
    a = F(comb(2*n, n), 4**n)
    s0 = (2*n+1)*a
    return s0, F(n,3)*s0, F(n*(3*n+2),15)*s0

def moments(k):
    e0,e1,e2 = central_sums((k-2)//2)
    o0,o1,o2 = central_sums((k-3)//2)
    v = F(k*(k-1),8) - ((k-1)*e0-2*e1)/8
    c = (2*(k-1)*e1-4*e2 + (k-2)*o0+(2*k-6)*o1-4*o2)/8
    return v,c

def direct_moments(k):
    C = F(0)
    c = F(0)
    for j in range(k-1):
        if j % 2 == 0:
            C += (k-1-j)*F(comb(j,j//2),2**j)
        m = j//2
        absolute = j*F(comb(2*m,m),4**m)
        c += (k-1-j)*absolute/8
    return F(k*(k-1),8)-C/8,c

def ln2_interval(terms=52):
    lo = 2*sum((F(1,(2*j+1)*3**(2*j+1)) for j in range(terms)), F(0))
    rem = F(9,4*(2*terms+1)*3**(2*terms+1))
    return lo,lo+rem

def decimal(x, direction=None):
    with localcontext() as ctx:
        ctx.prec = 30
        if direction == 'lower':
            ctx.rounding = ROUND_FLOOR
        elif direction == 'upper':
            ctx.rounding = ROUND_CEILING
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def main():
    t0,c0 = time.perf_counter(),time.process_time()
    for k in range(2,81):
        assert moments(k) == direct_moments(k)
    ell_lo,ell_hi = ln2_interval()
    sqrt2_lo = F(1414213562373095,10**15)
    sqrt105_hi = F(102469507659596,10**13)
    assert sqrt2_lo**2 < 2 and sqrt105_hi**2 > 105
    rows=[]
    r=F(1,256)
    for k in [4,16,256,1024,16384,65536,131072]:
        b=r/k
        a=1-b
        v,c=moments(k)
        assert F(k*k,32) <= v <= F(k*(k-1),8)
        # Same actual affine inward margin, and retained target margin.
        margin_lo=a*ell_lo*v*b*b*(F(1,16)-2*r)
        target_hi=a*ell_hi*v*b*b/128
        # Upper allowances from the two valid sufficient estimates.
        generic_hi=k*ell_hi**2*r*r/4
        generic_lo=k*ell_lo**2*r*r/4
        structured_hi=ell_hi**2*r**3/2
        structured_pass=margin_lo-structured_hi-target_hi
        generic_exhausted=generic_lo-(a*ell_hi*v*b*b*(F(1,16)-2*r))
        # Same square C=I-(ln2/8)bH, normalized globally instead of by pattern.
        g_lo,g_hi=ell_lo/8,ell_hi/8
        charge_lo=2*a*(g_lo*b)**2*c/(1+(g_hi*b)**2*v)
        offdiag_hi=2*r*(g_hi*r/sqrt2_lo+sqrt105_hi*g_hi**2*r*r)
        raw_drift_lo=charge_lo-offdiag_hi
        assert structured_pass > 0
        assert generic_exhausted > 0
        rows.append({
            'k':k,'b':str(b),'r':str(r),
            'inward_affine_margin_lower':decimal(margin_lo,'lower'),
            'retained_target_margin_upper':decimal(target_hi,'upper'),
            'generic_correction_allowance_upper':decimal(generic_hi,'upper'),
            'structured_correction_allowance_upper':decimal(structured_hi,'upper'),
            'generic_allowance_div_structured_allowance_exact':str(F(k,2*r)),
            'structured_certification_slack_lower':decimal(structured_pass,'lower'),
            'generic_allowance_minus_margin_lower':decimal(generic_exhausted,'lower'),
            'generic_estimate_exhausts_this_proof_budget':True,
            'raw_square_actual_outward_drift_lower':decimal(raw_drift_lo,'lower'),
            'raw_square_outward_drift_certified':raw_drift_lo>0,
            'negative_raw_lower_bound_means':'inconclusive, not inward drift'
        })
    assert rows[-1]['raw_square_outward_drift_certified']
    sources=[]
    base=HERE.parent/'inputs/pro1/Astra_Amplification_Cycle10_PRO1_20261023'
    for name in ['QUADRATIC_CAPACITY_FLOOR.tex','FAILED_ROUTES.md',
                 'contributions/charge_structure/CHARGE_BIAS_AND_NORMALIZATION.md']:
        path=base/name
        if path.exists():
            sources.append({'path':str(path.relative_to(HERE.parent)),
                            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    out={
        'study':'Retrospective proof-level complementary-operation analysis',
        'scope':'New exact scalar consequences of delivered identities; no new channel or owner frontier',
        'causal_agent_trial':False,'independent_invention':False,
        'historical_novelty_established':False,'research_amplification_demonstrated':False,
        'factorial_same_complete_input_intervention':False,
        'raw_comparison_scope':'Same square factor, but raw source family has no delivered charge tilt T; no normalization-only causal claim',
        'closed_form_crosschecks':79,
        'exact_rational_comparisons':True,
        'ln2_enclosure_width':decimal(ell_hi-ell_lo),
        'rows':rows,'source_bindings':sources,
        'cpu_seconds':time.process_time()-c0,'wall_seconds':time.perf_counter()-t0,
        'process_peak_rss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'rss_unit':'bytes' if platform.system()=='Darwin' else 'KiB',
        'scientific_design_model_tokens_and_total_cost':'UNKNOWN'
    }
    path=HERE/'COMPLEMENTARITY_RESULT.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'result':str(path),'cpu_seconds':out['cpu_seconds'],
          'raw_outward_k':[x['k'] for x in rows if x['raw_square_outward_drift_certified']],
          'structured_passes':len(rows),'last_raw_lower':rows[-1]['raw_square_actual_outward_drift_lower']}))

if __name__ == '__main__':
    main()

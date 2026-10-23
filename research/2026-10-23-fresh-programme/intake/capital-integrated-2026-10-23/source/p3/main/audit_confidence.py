#!/usr/bin/env python3
"""Outward, high-precision audit of the advertised 5% / 95% targets.

Original displayed epsilon values were binary64 diagnostics. This audit uses
the preserved Decimal upper certificates, including the sampled dyadic q.
It does not claim to formally verify the PRNG or the hardware floating kernel.
"""
from decimal import Decimal,localcontext,ROUND_CEILING
from pathlib import Path
import hashlib,json,time
import research as base

ROOT=Path(__file__).resolve().parent


def audit(logK,n,tau,logpoint):
    with localcontext() as c:
        c.prec=100; c.rounding=ROUND_CEILING
        K=base.exp_interval(Decimal(logK)).hi
        variance=max(Decimal(0),K-1)
        eps2=variance/(Decimal(n)*Decimal('0.05'))
        eps=eps2.sqrt()+Decimal('1e-80')
        # Extra 1e-12 covers representation of the displayed final log point.
        tauD=Decimal.from_float(tau)+Decimal('1e-12')
        eps_total=base.exp_interval(tauD).hi*(1+eps)-1
        result={'K_upper_decimal':str(K),'epsilon_sampling_upper_decimal':str(eps),
                'epsilon_computed_mean_upper_decimal':str(eps_total),
                'target_5percent_pass':eps_total<Decimal('0.05'),'paths':n,
                'failure_probability':'0.05','numerical_contract':'standard binary64 local-error model and Decimal correct rounding; independent draws model'}
        if result['target_5percent_pass']:
            # Because total point error is <.05 on the Chebyshev event, the
            # conservative 5% confidence interval inverts y/(1+eps),y/(1-eps).
            point=base.exp_interval(Decimal.from_float(logpoint))
            iv=base.Interval(point.lo,point.hi)
            lower=(iv/base.Interval(Decimal('1.05'))).lo
            upper=(iv/base.Interval(Decimal('0.95'))).hi
            result['conservative_95percent_probability_interval']=[str(lower),str(upper)]
        return result


def main():
    start=time.perf_counter(); rows={}
    for name in ['small_confirmation','main_confirmation','scale_confirmation']:
        d=json.loads((ROOT/'results'/name/'results.json').read_text()); st=d['methods']['probability_midpoint_minimax']
        rows[name]=audit(d['logK_decimal']['probability_midpoint_minimax'],st['paths'],st['uniform_log_weight_error_allowance'],st['log_probability_estimate'])
    d=json.loads((ROOT/'results'/'secant_extension'/'main_confirmation'/'results.json').read_text())
    for name in ['probability_midpoint_minimax','log_midpoint_tilt']:
        st=d['methods'][name]
        rows['secant_main_'+name]=audit(d['new_logK_decimal'][name],st['paths'],st['uniform_log_weight_error_allowance'],st['log_probability_estimate'])
    d=json.loads((ROOT/'results'/'critical_confirmation'/'critical_spatial_confirmation'/'results.json').read_text())
    for name in ['probability_midpoint_minimax','log_midpoint_tilt']:
        st=d['methods'][name]
        rows['critical_'+name]=audit(d['secant_logK_decimal'][name],st['paths'],st['uniform_log_weight_error_allowance'],st['log_probability_estimate'])
    full=json.loads((ROOT/'results'/'complete_baselines'/'results.json').read_text())
    orig=json.loads((ROOT/'results'/'main_confirmation'/'results.json').read_text())
    sec=json.loads((ROOT/'results'/'secant_extension'/'main_confirmation'/'results.json').read_text())
    for tag,l in [('derivative_certificate',orig['logK_decimal']['linear_tilt']),('secant_certificate',sec['original_linear_tilt_new_certificate_logK'])]:
        st=full['main_confirmation']['methods'][tag]
        rows['full_linear_main_'+tag]=audit(l,st['paths'],full['main_confirmation']['receipt']['uniform_log_weight_error_allowance'],st['log_probability_estimate'])
    st=full['critical_spatial_confirmation']['methods']['secant_certificate']
    rows['full_linear_critical']=audit(d['linear_tilt_secant_certificate_logK'],st['paths'],st['uniform_log_weight_error_allowance'],st['log_probability_estimate'])
    assert all(v['target_5percent_pass'] for v in rows.values())
    out={'rows':rows,'all_advertised_targets_pass':True,'elapsed_seconds':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'results'/'confidence_audit.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:{'paths':v['paths'],'epsilon_total':float(v['epsilon_computed_mean_upper_decimal'])} for k,v in rows.items()},indent=2))


if __name__=='__main__': main()

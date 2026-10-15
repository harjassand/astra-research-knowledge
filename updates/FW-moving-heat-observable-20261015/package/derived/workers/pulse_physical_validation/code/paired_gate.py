"""Current-amplitude-free paired-pulse gate, with explicit conditional premises.

For a 10s charge pulse followed by an equal 10s discharge pulse and zero initial
relaxation, the second pulse's signed voltage drop at age t contains Q(t) plus
the additional positive decay of memory left by the first pulse. Q(t) is
nonnegative, increasing, and concave on t>0 in the positive-RC+capacitor class.
Thus charge_rise <= max(1,t_charge/t_discharge)*discharge_fall, even when the
same unknown I multiplies both. Duration/sample brackets bound the time ratio.

This excludes the stated common-state linear model with millivolt precision;
it does not exclude arbitrary unknown initial relaxation or unequal currents.
"""
from pathlib import Path
from fractions import Fraction
import json
import numpy as np
from audit_data import load, pulse_info

BASE=Path(__file__).resolve().parents[1]

def bounds(info):
    t=info['t']; v=info['v']; ion=info['on_index']; ioff=info['off_index']
    # Intersect voltage-derived brackets with the published exact 10s command.
    onlo=max(t[ion-1],t[ioff-1]-10.)
    onhi=min(t[ion],t[ioff]-10.)
    assert onlo<=onhi
    end=info['end_index']; age=[float(t[end]-onhi),float(t[end]-onlo)]
    base=[float(v[:ion].min()),float(v[:ion].max())]
    if info['direction']==1: amp=[float(v[end]-base[1]),float(v[end]-base[0])]
    else: amp=[float(base[0]-v[end]),float(base[1]-v[end])]
    return {'age_bracket_s':age,'on_bracket_with_10s_command_s':[float(onlo),float(onhi)],
            'baseline_range_V':base,'endpoint_increment_bracket_V':amp}

def main():
    _,p,_=load(); rows=[]
    for cell in range(92):
        pi=pulse_info(p,'pos',cell); ni=pulse_info(p,'neg',cell)
        pb=bounds(pi); nb=bounds(ni)
        # Exact arithmetic over the acquired IEEE floats gives a reproducible
        # rational number. This is not an instrument accuracy certificate.
        r=max(Fraction(1),Fraction(pb['age_bracket_s'][1])/Fraction(nb['age_bracket_s'][0]))
        rise=Fraction(pb['endpoint_increment_bracket_V'][0])
        fall=Fraction(nb['endpoint_increment_bracket_V'][1])
        gap=rise-r*fall
        e=max(Fraction(0),gap/(1+r))
        rows.append({'cell_one_based':cell+1,'charge':pb,'discharge':nb,
            'time_ratio_allowance':float(r),'observed_directional_gap_mV':pi['endpoint_delta_mV']-ni['endpoint_delta_mV'],
            'conservative_inequality_violation_mV':1000*float(gap),
            'minimum_per_endpoint_uniform_error_mV':1000*float(e),
            'error_lower_bound_V_exact_rational':str(e),
            'gate_failed':gap>0,
            'samples_removed_as_padding':pi['padding_samples_removed']+ni['padding_samples_removed']})
    es=np.array([r['minimum_per_endpoint_uniform_error_mV'] for r in rows])
    out={'status':'CONDITIONAL_CONTINUUM_MODEL_MISMATCH',
         'premises':['positive-RC+nonnegative capacitor, series R, switching impulses excluded',
                     'same constant amplitude magnitude in charge and discharge',
                     'each commanded pulse exactly 10s',
                     'zero initial relaxation before first pulse; only known first pulse contributes memory to second',
                     'same stationary linear response and thermal/material state',
                     'corresponding cell columns are aligned across the published MATs'],
         'uncertainty_accounted':['voltage-derived switching brackets','entire observed pre-pulse baseline range',
                                  'unknown common absolute current amplitude','positive memory of previous pulse'],
         'uncertainty_not_acquired':['actual current trace','per-cell current/capacity calibration',
                                     'initial relaxation state','independent equilibrium OCV',
                                     'instrument voltage error bound'],
         'proof':'Q(t)=R+k*t+integral(1-exp(-t/tau))dmu is nonnegative, increasing and concave. For t1,t2>0, Q(t1)<=max(1,t1/t2)Q(t2). The decay of the previous positive pulse during the later negative pulse adds integral(1-exp(-10/tau))*exp(-d/tau)*(1-exp(-t2/tau))dmu>=0 to the discharge fall. Combine these facts and the timestamp brackets. If two endpoint residuals have absolute value <=e, rise-r*fall <= (1+r)e.',
         'all_92':{'failed_count':sum(r['gate_failed'] for r in rows),
                   'error_floor_mV_min':float(es.min()),'error_floor_mV_median':float(np.median(es)),
                   'error_floor_mV_max':float(es.max())},
         'cell_001':rows[0], 'rows':rows,
         'physical_validation':False,
         'meaning':'Rejects transferring the narrow EIS-only certificate as a common-state finite-amplitude voltage guarantee. Does not identify whether mismatch comes from actual waveform/amplitude, unknown initial state, nonlinearity, hysteresis, or thermal/material drift. No novelty claim.'}
    (BASE/'results/paired_gate.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))

if __name__=='__main__': main()

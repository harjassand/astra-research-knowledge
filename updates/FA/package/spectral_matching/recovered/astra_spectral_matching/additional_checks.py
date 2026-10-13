#!/usr/bin/env python3
"""Finite pulse cutoff checks and the nonuniform product-dimer obstruction."""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import k0, k1
from checks import A, BETA, matched_gamma, rate
ROOT=Path(__file__).resolve().parent

def cutoff_check(eta=1., W=10., tolerance=.01):
    if eta<=0 or W<eta or not 0<tolerance<.5:
        raise ValueError('Require eta>0, W>=eta, and 0<tolerance<.5')
    c=3/4
    lo=math.pi*tolerance*c/(2*A*W)
    hi=8*A/(math.pi*tolerance*eta)
    m=BETA*eta
    lam_envelope=2*A/math.pi*(1/lo-1/hi)
    phase_action_bound=2*A/math.pi*math.log(hi/lo)
    phase_action_exact=2*A/math.pi*(k0(m*lo)-k0(m*hi))
    rows=[]
    for w in np.r_[0.,np.geomspace(.001,W,41)]:
        val,quaderr=quad(lambda u:4*A*m/math.pi * k1(m*math.exp(u))*math.sin(w*math.exp(u)/2)**2,
                        math.log(lo),math.log(hi),epsabs=1e-10,limit=400)
        gm=float(matched_gamma(w,eta));gt=eta+val
        assert gm-gt >= -1e-8 and gm-gt<=tolerance*gm+1e-8
        r=float(rate(np.array(w),np.array(gt))/rate(np.array(w),np.array(max(eta,w))))
        assert r>=.97*(1-tolerance)-1e-8
        rows.append({'gap':float(w),'ideal_width':gm,'truncated_width':gt,'ratio_to_edge_oracle':r})
    return dict(eta=eta,local_gap_bound=W,tolerance=tolerance,minimum_pulse_phase=lo,
                maximum_pulse_phase=hi,proposal_rate=lam_envelope,
                expected_absolute_phase_per_unit_target_time=phase_action_exact,
                absolute_phase_upper_bound=phase_action_bound,values=rows)

def dimer_check(J=.05,eta=1.):
    if not 0<J<eta/4:raise ValueError('Overdamped regime required')
    om=math.sqrt(eta*eta-16*J*J)
    a=(1+eta/om)/2;b=(1-eta/om)/2
    lslow=(eta-om)/2;lfast=(eta+om)/2
    def corr(t):
        return a*math.exp(-lslow*t)+b*math.exp(-lfast*t)
    rows=[]
    for n in [1,10,100,1000,10000,1000000]:
        scale=1/(J*math.sqrt(n))
        def val(s):
            c=corr(s*scale)
            return math.exp(n*math.log(c)) if c>0 else 0.
        integral=quad(val,0,np.inf,epsabs=1e-9,limit=300)[0]*scale
        kinetic=eta/(4*n*J*J)
        asymptotic=math.sqrt(math.pi)/(2*math.sqrt(2)*J*math.sqrt(n))
        rows.append(dict(dimers=n,quantum_integral=integral,kinetic_integral=kinetic,
                         quantum_over_kinetic=integral/kinetic,
                         quantum_over_large_n_asymptotic=integral/asymptotic))
    return dict(J=J,eta=eta,status='exact formula integrated numerically; asymptotic proved in note',values=rows)

if __name__=='__main__':
    out={'finite_pulse_cutoff':cutoff_check(),'nonuniform_dimer_obstruction':dimer_check()}
    (ROOT/'additional_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

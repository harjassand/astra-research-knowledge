"""Executed conditional whole-turnover bounds for the reported pulse.

This is an optimistic irreversible-cycle bound, not an empirical fit.
The actual hot barrier's operating potential, pulse waveform, gate free
energy, source gross activity and donor coupling have not been acquired.
"""
from pathlib import Path
import json
import numpy as np
from scipy.special import expi, gammaln
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent
KB=8.617333262e-5
GAMMA=.5772156649015328606
T=298.
TAU=41e-9
DE=.192
C=DE/(KB*T)

def shape(c):
    return expi(c)-GAMMA-np.log(c)

Iexp=TAU*shape(C)
Irect=TAU*np.expm1(C)
rows=[]
for G in [3.3,3.3*.04175/.079]:
    for J0 in [.2,1.,4.]:
        for m in [1.,10.,100.,1000.]:
            row=dict(target_gain=G,J0_per_second=J0,donor_budget_m=m)
            for name,I in [('continuous_exponential',Iexp),('rectangle_or_mean_lifetime_cap',Irect)]:
                x=m*J0*I
                required_I=(1-1/G)/(m*J0)
                c_required=(brentq(lambda c: shape(c)-required_I/TAU,.001,40)
                    if name=='continuous_exponential' else np.log1p(required_I/TAU))
                row[name]=dict(exposure_s=I,feedback_bound=x,
                    gain_upper=1/(1-x) if x<1 else None,
                    donor_budget_required=(1-1/G)/(J0*I),
                    received_pulse_rate_required=(G-1)/I,
                    lifetime_required_s=TAU*required_I/I,
                    barrier_reduction_required_eV=float(KB*T*c_required))
            rows.append(row)

# Own-cycle pulse created just after adsorption: three chemical steps
# must complete before the OH* step. This is the exact expected residual
# excess hazard, using the exponential pulse series and Laplace transforms
# of independent exponential chemical wait times. Conditional benchmark.
own=[]
for J0 in [.2,1.,4.]:
    for f in [.5,.75,.9]:
        kpre=5*J0/(1-f)
        kb=J0/f
        n=np.arange(1,151,dtype=float)
        log_terms=n*np.log(C)-np.log(n)-gammaln(n+1)+3*np.log(kpre/(kpre+n/TAU))
        A=kb*TAU*np.exp(log_terms).sum()
        A0=kb*Iexp
        loose=A0*(kpre*TAU/(1+kpre*TAU))**3
        assert A<=loose*(1+1e-12)
        own.append(dict(J0=J0,target_cold_wait_fraction=f,
            preceding_rates_per_second=kpre,target_rate_per_second=kb,
            expected_extra_hazard_on_target_arrival=float(A),
            coincident_extra_hazard=A0,
            independent_three_step_delay_bound=loose,
            bound_ratio_to_coincident=float(A/A0)))

out=dict(parameters=dict(T_K=T,tau_s=TAU,delta_barrier_eV=DE,c=C,
    max_hot_ratio=float(np.exp(C)),I_exponential_s=float(Iexp),
    I_rectangle_s=float(Irect),
    source_site_ratio=.04175/.079,
    site_normalized_gain=3.3,per_mass_current_gain_if_same_basis=3.3*.04175/.079),
    scope='Conditional bounds for identical cold cycles, same site basis, nonnegative pulse envelope, and at most m productive donor pulses per target turnover. Actual gross reversible activity is not bounded by net current. Rectangle needs a global amplitude cap and mean pulse duration or energy-area bound.',
    cases=rows,own_cycle_arrival=own)
(ROOT/'pulse_resource_bounds.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['parameters'],indent=2))
for r in rows:
    if r['target_gain']==3.3 and r['donor_budget_m']==100:
        print(json.dumps(r,indent=2))
print('Own-cycle cases',json.dumps(own,indent=2))

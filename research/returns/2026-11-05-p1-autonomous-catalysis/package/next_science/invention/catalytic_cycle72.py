#!/usr/bin/env python3
"""SYNTHETIC, fully reversible two-site ORR/shared-mode closure.

This is not a fit or a reconstruction of Liang et al.'s catalyst.  Rates not
identified in that paper are explicit illustrative inputs.  All channels obey
local detailed balance, including adsorption that charges the mode and the
reverse of that process.  Source numerical stress tests are conditional on
identifying 0.126 eV as a mode FREE energy and 41 ns as its thermal lifetime.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import mpmath as mp

mp.mp.dps = 55
M = mp.mpf
KB = M('8.617333262145e-5')


def solve_case(mode='consume', capture='1', eta='0.3', fast='100',
               gap='0.126', tau='4.1e-8', temp='298', internal=False):
    beta = 1/(KB*M(temp))
    p = M(capture)
    gap, tau, eta, fast = map(M, (gap, tau, eta, fast))
    # The six chemical stages are E, O2*, OOH*, O*, OH*, H2O*.
    # Energies below are explicitly SYNTHETIC illustrative state free energies.
    F = list(map(M, ['0', '-0.95', '-0.70', '-0.40', '-0.20', '-0.10']))
    cold = M('2.3e9')*mp.exp(-beta*M('0.375'))
    hot = M('2.3e9')*mp.exp(-beta*M('0.183'))
    k = [fast, fast, fast, fast, cold, fast]
    work = [M(0), eta, eta, eta, eta, M(0)]
    states = list(itertools.product(range(6), range(6), range(2)))
    ids = {s:i for i,s in enumerate(states)}
    n = len(states)
    Q = mp.matrix(n,n)
    edges = []

    def energy(s):
        return F[s[0]] + F[s[1]] + gap*s[2]

    def channel(s, t, kp, w, label, site=-1, step=-1):
        if kp == 0:
            return
        i,j = ids[s],ids[t]
        dF = energy(t)-energy(s)
        km = kp*mp.exp(-beta*(w-dF))
        Q[i,j] += kp
        Q[j,i] += km
        Q[i,i] -= kp
        Q[j,j] -= km
        edges.append((i,j,kp,km,w,dF,label,site,step))

    for s in states:
        g = s[2]
        if g == 0:
            t = s[:2]+(1,)
            channel(s,t,mp.exp(-beta*gap)/tau,M(0),'thermal')
        for site in (0,1):
            step=s[site]
            t=list(s)
            t[site]=(step+1)%6
            base=k[step]
            if step==0 and g==0:
                channel(s,tuple(t),base*(1-p),work[step],
                        'ordinary',site,step)
                t[2]=1
                channel(s,tuple(t),base*p,work[step],
                        'capture',site,step)
            else:
                if step==4 and g==1 and mode=='modulate':
                    base=hot
                channel(s,tuple(t),base,work[step],
                        'ordinary',site,step)
            if step==4 and g==1 and mode=='consume':
                t=list(s)
                t[site]=5
                t[2]=0
                channel(s,tuple(t),hot-cold,work[step],
                        'consume',site,step)

    # Arbitrary-precision solve, followed by independent current/entropy checks.
    A=Q.T.copy()
    rhs=mp.matrix(n,1)
    for j in range(n):
        A[n-1,j]=1
    rhs[n-1]=1
    pi=mp.lu_solve(A,rhs)
    assert min(pi)>0
    residual=max(abs(sum(pi[i]*Q[i,j] for i in range(n))) for j in range(n))
    assert residual < M('1e-35')
    current=[[M(0) for _ in range(6)] for _ in range(2)]
    gross_ads=M(0)
    capture_current=consume_current=thermal_current=M(0)
    entropy=chem_power=internal_balance=M(0)
    max_local_db_error=M(0)
    for i,j,kp,km,w,dF,label,site,step in edges:
        fp,fr=pi[i]*kp,pi[j]*km
        J=fp-fr
        entropy += J*mp.log(fp/fr)
        chem_power += J*w
        internal_balance += J*dF
        max_local_db_error=max(max_local_db_error,
                              abs(mp.log(kp/km)-beta*(w-dF)))
        if site>=0:
            current[site][step]+=J
            if step==0:
                gross_ads+=fp
        if label=='capture': capture_current+=J
        if label=='consume': consume_current+=J
        if label=='thermal': thermal_current+=J
    total_current=current[0][0]+current[1][0]
    max_step_mismatch=max(abs(v-current[s][0])
                          for s in (0,1) for v in current[s])
    gate_balance=capture_current+thermal_current-consume_current
    assert max_step_mismatch < M('1e-35')
    assert abs(gate_balance)<M('1e-35')
    assert abs(internal_balance)<M('1e-35')
    assert abs(entropy-beta*chem_power)<M('1e-35')
    assert abs(chem_power-4*eta*total_current)<M('1e-35')
    hot_prob=sum(pi[i] for i,s in enumerate(states) if s[2])
    oh_prob=sum(pi[i] for i,s in enumerate(states) if s[0]==4)
    hot_given_oh=sum(pi[i] for i,s in enumerate(states) if s[0]==4 and s[2])/oh_prob
    eq_hot=1/(1+mp.exp(beta*gap))
    out={
        'synthetic':True,'mode':mode,'capture_fraction':float(p),
        'eta_V':float(eta),'temperature_K':float(temp),
        'mode_free_energy_eV':float(gap),'thermal_lifetime_s':float(tau),
        'unspecified_other_forward_rates_s-1':float(fast),
        'illustrative_chemical_state_free_energies_eV':[float(v) for v in F],
        'source_conditional_cold_rate_s-1':float(cold),
        'source_conditional_hot_rate_s-1':float(hot),
        'thermal_up_rate_s-1':float(mp.exp(-beta*gap)/tau),
        'net_cycles_per_site_per_s':float(total_current/2),
        'gross_adsorptions_pair_per_s':float(gross_ads),
        'net_adsorptions_pair_per_s':float(total_current),
        'net_mode_capture_pair_per_s':float(capture_current),
        'net_mode_consumption_pair_per_s':float(consume_current),
        'net_mode_thermal_up_pair_per_s':float(thermal_current),
        'mode_hot_probability':float(hot_prob),
        'equilibrium_mode_hot_probability':float(eq_hot),
        'OH_probability_per_site':float(oh_prob),
        'mode_hot_probability_conditional_on_OH':float(hot_given_oh),
        'entropy_production_kB_per_s':float(entropy),
        'chemical_power_eV_per_s':float(chem_power),
        'current_conservation_error':str(max_step_mismatch),
        'gate_balance_error':str(gate_balance),
        'internal_energy_balance_error':str(internal_balance),
        'entropy_identity_error':str(entropy-beta*chem_power),
        'local_detailed_balance_max_error':str(max_local_db_error),
        'stationarity_max_error':str(residual),
    }
    if eta==0:
        eq=mp.matrix([mp.exp(-beta*energy(s)) for s in states])
        eq/=sum(eq)
        out['equilibrium_Gibbs_probability_error']=str(max(abs(pi[i]-eq[i]) for i in range(n)))
        assert max(abs(pi[i]-eq[i]) for i in range(n))<M('1e-35')
    if internal:
        return {'output':out,'Q':Q,'pi':pi,'edges':edges,
                'states':states,'beta':beta}
    return out


def static_witness():
    T=M(298)
    r=mp.exp(M('0.192')/(KB*T))
    F=M('3.3')
    x=(1-1/F)/(1-1/r)
    xp=F*x/r
    # Fully reversible two-channel cycle: forward a,b; reverse qa,qb.
    # Net J=(1-q)ab/(a+b), q=exp[-(4 eta)/(2 kBT)]. Scaling b and
    # qb together changes the barrier while retaining all cycle affinities.
    # The cycle-gain formula is therefore exact, not an irreversible limit.
    eta=M('0.3')
    q=mp.exp(-2*eta/(KB*T))
    common_tafel_term=(2*q/(1000*KB*T*(1-q)))/mp.log(10)
    # Tafel derivative: 1/b=common+(1-x)/b_other+x/b_changed.
    A=mp.matrix([[1-x,x],[1-xp,xp]])
    y=mp.matrix([1/M('66.1')-common_tafel_term,
                 1/M('60.2')-common_tafel_term])
    v=mp.lu_solve(A,y)
    return {
        'identifiability_witness_not_fitted_mechanism':True,
        'fully_reversible_two_channel_cycle':True,
        'eta_for_tafel_witness_V':float(eta),
        'reverse_to_forward_rate_ratio_each_channel':float(q),
        'instantaneous_changed_step_factor':float(r),
        'whole_cycle_factor':float(F),
        'initial_changed_step_waiting_fraction':float(x),
        'modified_changed_step_waiting_fraction':float(xp),
        'other_step_tafel_mV_dec':float(1/v[0]),
        'changed_step_tafel_mV_dec':float(1/v[1]),
        'effective_whole_cycle_barrier_reduction_eV':float(KB*T*mp.log(F)),
        'measured_titration_modified_over_original':float(M('0.04175')/M('0.079')),
        'mass_current_factor_if_tof3point3_and_titration_correct':float(F*M('0.04175')/M('0.079')),
    }


def main():
    cases=[]
    for mode in ('modulate','consume'):
        for fast in ('100','1e6'):
            baseline=None
            for capture in ('0','1'):
                c=solve_case(mode=mode,capture=capture,fast=fast)
                if baseline is None: baseline=c['net_cycles_per_site_per_s']
                c['gain_relative_to_same_thermal_model_without_capture']=c['net_cycles_per_site_per_s']/baseline
                cases.append(c)
                print(json.dumps({k:c[k] for k in (
                    'mode','capture_fraction','unspecified_other_forward_rates_s-1',
                    'net_cycles_per_site_per_s','gain_relative_to_same_thermal_model_without_capture',
                    'mode_hot_probability','net_mode_capture_pair_per_s')}),flush=True)
    equilibrium=solve_case(mode='consume',capture='1',eta='0',fast='100')
    output={'description':'Synthetic fully reversible 72-state catalytic closure; not a fit to the paper',
            'cases':cases,'equilibrium_check':equilibrium,'static_alternative_witness':static_witness()}
    out=Path(__file__).with_name('catalytic_cycle72_results.json')
    out.write_text(json.dumps(output,indent=2)+'\n')
    print(str(out),flush=True)


if __name__=='__main__': main()

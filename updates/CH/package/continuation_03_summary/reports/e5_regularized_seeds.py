#!/usr/bin/env python3
"""Bounded rank-two full-support-seed approximations; no infinite-rank claims.

Imports the previously frozen e5_realization.py physical cutoff-erasure map.
All evaluated inputs are exact finite-support states. Missing mass of the
intended infinite seeds is separately charged by closed-form rational tails.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import resource
import time

import numpy as np

import e5_realization as base


Q = Fraction(13,20)
PROFILES = {
    'geometric_positive': (0.,0.),
    'irrational_quadratic': (math.pi*math.sqrt(2)/8,0.),
    'irrational_cubic': (0.,math.pi*math.sqrt(3)/128),
}
PARTNERS = ['phase_shift_pi_over_3','number_weight_n_plus_1']
WEIGHTS = [Fraction(1,100),Fraction(1,1000),Fraction(1,100000),Fraction(1,10000000)]


def upper_float(value: Fraction) -> float:
    answer = float(value)
    if Fraction.from_float(answer) < value:
        answer = math.nextafter(answer,math.inf)
    return answer


def exact_tail(cutoff,partner):
    """Exact rational mass above cutoff for a normalized infinite seed."""
    L = cutoff+1
    if partner == 'phase_shift_pi_over_3' or partner == 'seed':
        return Q**L
    if partner != 'number_weight_n_plus_1':
        raise ValueError(partner)
    return Q**L*((L+1)**2*(1-Q)**2+2*(L+1)*Q*(1-Q)+Q*(1+Q))/(1+Q)


def phase_values(n,profile):
    theta,phi = PROFILES[profile]
    return theta*n*n+phi*n*n*n


def seeds(cutoff,profile,partner):
    n = np.arange(cutoff+1,dtype=float)
    seed = float(Q)**(n/2)*np.exp(1j*phase_values(n,profile))
    seed /= np.linalg.norm(seed)
    if partner == 'phase_shift_pi_over_3':
        other = seed*np.exp(1j*math.pi*n/3)
    elif partner == 'number_weight_n_plus_1':
        other = (n+1)*seed
    else:
        raise ValueError(partner)
    other /= np.linalg.norm(other)
    return seed,other


def conditional_continuity(delta):
    if delta <= 0:
        return 0.
    if delta >= 1:
        return 2.
    z = delta/(1+delta)
    return 2*delta+(1+delta)*float(base.hbits(z)+base.hbits(1-z))


def prepare(eta,cutoff,output_cutoff,profile,partner):
    started = time.monotonic()
    seed,other = seeds(cutoff,profile,partner)
    channel = base.ThermalCutoff(eta,1,cutoff,output_cutoff)
    C = np.stack([seed,other])/math.sqrt(2)
    midpoint = channel.apply_purification(C)
    overlap = np.vdot(seed,other)
    energy = np.arange(cutoff+1,dtype=float)
    return {'eta':eta,'input_cutoff':cutoff,'output_cutoff':output_cutoff,
            'profile':profile,'partner':partner,'seed':seed,'other':other,
            'overlap':overlap,'seed_energy':float(np.dot(energy,abs(seed)**2)),
            'partner_energy':float(np.dot(energy,abs(other)**2)),
            'midpoint':midpoint,'prepare_seconds':time.monotonic()-started}


def evaluate(prepared,weight:Fraction):
    started = time.monotonic()
    z = prepared
    p = float(weight)
    mid = z['midpoint']
    m = z['output_cutoff']+1
    scale = np.repeat(np.sqrt([2*(1-p),2*p]),m)
    joint = mid['retained_rb']*scale[:,None]*scale[None,:]
    flag_scale = np.sqrt([2*(1-p),2*p])
    flag = mid['erased_r']*flag_scale[:,None]*flag_scale[None,:]
    output = 2*(1-p)*mid['retained_rb'][:m,:m]+2*p*mid['retained_rb'][m:,m:]
    sf,ef = base.entropy(flag)
    srb0,er = base.entropy(joint)
    sb0,eb = base.entropy(output)
    prob_flag = float(np.trace(flag).real)
    sb = sb0+float(base.hbits(prob_flag))
    srb = srb0+sf
    overlap = z['overlap']
    reference = np.array([[1-p,math.sqrt(p*(1-p))*overlap.conjugate()],
                          [math.sqrt(p*(1-p))*overlap,p]],dtype=complex)
    sinput,_ = base.entropy(reference)
    seed_tail = exact_tail(z['input_cutoff'],'seed')
    partner_tail = exact_tail(z['input_cutoff'],z['partner'])
    missing_mass = (1-weight)*seed_tail+weight*partner_tail
    # Pure-state distance from branch-normalized infinite approximation:
    # delta^2 <= 2*((1-p)*seed_tail+p*partner_tail). Closed-form rational RHS.
    delta_upper_diagnostic = math.sqrt(2*upper_float(missing_mass))
    seed_mean = Q/(1-Q)
    partner_mean = (seed_mean if z['partner']=='phase_shift_pi_over_3' else
                    2*Q*(2+Q)/((1-Q)*(1+Q)))
    channel_flag_infinite_upper = min(1.,prob_flag+upper_float(missing_mass))
    result = {
        'eta':z['eta'],'nu':1.,'profile':z['profile'],'partner':z['partner'],
        'q_numerator':Q.numerator,'q_denominator':Q.denominator,'weight_partner':p,
        'input_cutoff':z['input_cutoff'],'output_cutoff':z['output_cutoff'],
        'ic_bits_per_use':sb-srb,'S_B':sb,'S_RB':srb,'input_entropy_bits':sinput,
        'ic_over_p_log2_inverse_p':(sb-srb)/(p*math.log2(1/p)),
        'overlap_magnitude':float(abs(overlap)),'overlap_squared':float(abs(overlap)**2),
        'finite_energy_photons':(1-p)*z['seed_energy']+p*z['partner_energy'],
        'intended_infinite_energy_photons':float((1-weight)*seed_mean+weight*partner_mean),
        'p_output_erasure_finite':prob_flag,
        'p_output_erasure_intended_infinite_upper_diagnostic':channel_flag_infinite_upper,
        'seed_input_tail_upper':upper_float(seed_tail),
        'partner_input_tail_upper':upper_float(partner_tail),
        'weighted_input_tail_upper':upper_float(missing_mass),
        'input_trace_distance_upper_diagnostic':delta_upper_diagnostic,
        'input_ic_continuity_charge_bits_diagnostic':conditional_continuity(delta_upper_diagnostic),
        'source_seed_projection_success_lower':math.nextafter(1-upper_float(seed_tail),-math.inf),
        'source_partner_projection_success_lower':math.nextafter(1-upper_float(partner_tail),-math.inf),
        'direct_finite_preparation_success_probability':1.,
        'reference_dimension':2,'input_fock_dimension':z['input_cutoff']+1,
        'output_dimension_with_flag':m+1,'joint_dimension_with_flag':2*(m+1),
        'trace_RB':float(np.trace(joint).real+np.trace(flag).real),
        'trace_B':float(np.trace(output).real+prob_flag),
        'minimum_eigenvalue':float(min(ef.min(),er.min(),eb.min())),
        'tp_residual':mid['tp_residual'],'preparation_kernel_seconds':z['prepare_seconds'],
        'reweight_entropy_seconds':time.monotonic()-started,
        'kernel_workspace_vector_bytes':mid['workspace_vector_bytes'],
        'reweight_arrays_bytes':joint.nbytes+flag.nbytes+output.nbytes,
        'process_peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'interval_certified':False,
    }
    return result


def controls():
    z = prepare(.76,16,24,'irrational_quadratic','number_weight_n_plus_1')
    by_reweight = evaluate(z,Fraction(1,1000))['ic_bits_per_use']
    C = np.stack([math.sqrt(.999)*z['seed'],math.sqrt(.001)*z['other']])
    direct = base.ThermalCutoff(.76,1,16,24).apply_purification(C)['ic_bits_per_use']
    pure = base.ThermalCutoff(.76,1,16,24).apply_purification(z['seed'][None,:])['ic_bits_per_use']
    result = {'reweight_vs_direct_error':abs(by_reweight-direct),'pure_input_ic':pure,
              'weighted_partner_infinite_energy':float(2*Q*(2+Q)/((1-Q)*(1+Q))),
              'infinite_phase_partner_overlap_squared':float((1-Q)**2/(1+Q*Q-Q)),
              'infinite_number_partner_overlap_squared':float(1/(1+Q))}
    assert result['reweight_vs_direct_error'] < 2e-11
    assert abs(pure)<2e-11
    return result


def scan(destination):
    results=[]
    start=time.monotonic()
    for cutoff in [32,64,96]:
        for eta in [.75,.7501,.76,.78,.8]:
            for profile in PROFILES:
                for partner in PARTNERS:
                    z=prepare(eta,cutoff,cutoff+16,profile,partner)
                    rows=[evaluate(z,p) for p in WEIGHTS]
                    results.extend(rows)
                    print(json.dumps({'input_cutoff':cutoff,'eta':eta,'profile':profile,
                                      'partner':partner,'results':[
                                          [r['weight_partner'],r['ic_bits_per_use'],r['input_ic_continuity_charge_bits_diagnostic']]
                                          for r in rows]}),flush=True)
    data={'controls':controls(),'results':results,'elapsed_seconds':time.monotonic()-start,
          'faithfulness_inferred':False,'positive_capacity_claim':False}
    Path(destination).write_text(json.dumps(data,indent=2)+'\n')
    return data


def refine(destination):
    started=time.monotonic()
    results=[]
    for eta in [.7501,.8]:
        z=prepare(eta,128,144,'irrational_cubic','number_weight_n_plus_1')
        for p in WEIGHTS:
            row=evaluate(z,p)
            results.append(row)
            print(json.dumps(row),flush=True)
    data={'controls':controls(),'results':results,'elapsed_seconds':time.monotonic()-started,
          'faithfulness_inferred':False,'positive_capacity_claim':False}
    Path(destination).write_text(json.dumps(data,indent=2)+'\n')
    return data


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['controls','scan','refine'])
    parser.add_argument('--output')
    args=parser.parse_args()
    if args.mode=='controls':
        print(json.dumps(controls()))
    else:
        default=Path(__file__).with_suffix('.json')
        if args.mode=='refine':
            default=default.with_name(default.stem+'_refinement.json')
        destination=args.output or str(default)
        if args.mode=='scan':
            scan(destination)
        else:
            refine(destination)


if __name__=='__main__':
    main()

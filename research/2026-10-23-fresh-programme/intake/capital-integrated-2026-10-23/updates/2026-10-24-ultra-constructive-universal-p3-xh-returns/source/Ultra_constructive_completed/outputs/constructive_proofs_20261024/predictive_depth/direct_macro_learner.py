#!/usr/bin/env python3
"""Direct selected-operation tomography from integer counts; no plant import."""
import itertools
import math
import numpy as np
from finite_predictive_learner import CountOracle


def learn_macro(data,alpha=0.01):
    ps,fs = data['preparations'],data['tests']
    r = len(ps)
    if data['architecture_rank_upper_bound'] != r:
        raise ValueError('Full quotient exhaustion needs the architecture bound')
    # Basis is fixed from independent pilot data. This new confidence pool is
    # conditional on that choice and covers all subsequently used raw events.
    pool = 2*r*r
    def width(n):
        return math.sqrt(math.log(2*pool/alpha)/(2*n))
    # Reuse the ORIGINAL uniformly covered pilot core. More macro shots alone
    # would not remove this core's calibration uncertainty. No new high-shot
    # calibration is manufactured to force an all-input certificate.
    pilot = CountOracle(data['pilot_calibration'],alpha)
    macros = {(tuple(s['preparation']),s['future_action']):s for s in data['macro']}
    h,dh = np.ones((r,r)),np.zeros((r,r))
    hz = {b:np.zeros((r,r)) for b in ['success','abort']}
    dz = {b:np.zeros((r,r)) for b in ['success','abort']}
    gamma = 1-data['abort_probability']
    tail = gamma**data['maximum_calls']
    for j,p in enumerate(ps):
        for i,f in enumerate(fs):
            if f:
                a,o = f[0]
                value,error,_,_ = pilot.cell(tuple(p),tuple(tuple(z) for z in f))
                h[i,j],dh[i,j] = value,error
                cellm = macros[tuple(p),a]
                for b in hz:
                    hz[b][i,j] = cellm['counts'][f'{b},{o}']/cellm['shots']
                    dz[b][i,j] = width(cellm['shots'])+tail
            else:
                # Use one of the already acquired future-action experiments;
                # summing over its test outcomes leaves the macro's mass.
                a = fs[1][0][0]
                cellm = macros[tuple(p),a]
                for b in hz:
                    hz[b][i,j] = sum(cellm['counts'][f'{b},{o}'] for o in range(2))/cellm['shots']
                    dz[b][i,j] = width(cellm['shots'])+tail
    inv = np.linalg.inv(h)
    jhat = float(np.linalg.norm(inv,np.inf))
    deltah = float(np.linalg.norm(dh,np.inf))
    nu = jhat*deltah
    if nu >= 1:
        raise ValueError('Data do not certify invertibility of the full core')
    jbar = jhat/(1-nu)
    # Exact small-r infinity->1 norm, then a rigorous inverse-perturbation
    # margin: ||H^-1-Hhat^-1||infinity <= Jbar*dH*Jhat.
    kap_hat = max(float(np.linalg.norm(inv@np.array(signs),1))
                  for signs in itertools.product([-1,1],repeat=r))
    kap_bar = kap_hat+r*jbar*deltah*jhat
    ops = {b:hz[b]@inv for b in hz}
    trace = np.eye(r)[0]
    repair = trace-ops['success'][0]-ops['abort'][0]
    ops['abort'][0] += repair
    errors = {}
    for b in hz:
        raw = hz[b]@inv
        errors[b] = float((np.linalg.norm(dz[b],np.inf)+np.linalg.norm(raw,np.inf)*deltah)*jbar
                          +np.linalg.norm(ops[b]-raw,np.inf))
    e = kap_bar*sum(errors.values())
    initial_column = ps.index([])
    x0 = h[:,initial_column]
    # Known initial column makes repeated macro prediction evaluable without
    # another initial-state oracle. The width of that column is explicit.
    initial_error = kap_bar*float(max(dh[:,initial_column]))
    certificate = {'confidence_failure_probability':2*alpha,
                   'pilot_confidence_failure_probability':alpha,
                   'macro_confidence_failure_probability':alpha,
                   'simultaneous_macro_event_pool':pool,
                   'basis_fixed_using_independent_pilot_data':True,
                   'maximum_entry_statistical_width':max(width(s['shots']) for s in data['macro']),
                   'cap_systematic_entry_error_upper_bound':tail,
                   'H_error_infinity_bound':deltah,'inverse_neumann_product':nu,
                   'inverse_H_infinity_norm':jhat,'true_inverse_H_upper_bound':jbar,
                   'rank_exhaustion_certified_given_architecture':True,
                   'observed_infinity_to_1_inverse_norm':kap_hat,
                   'physical_quotient_kappa_upper_bound':kap_bar,
                   'branch_coordinate_error_bounds':errors,
                   'joint_terminal_instrument_quotient_error_upper_bound':e,
                   'initial_quotient_error_upper_bound':initial_error,
                   'single_invocation_error_including_initial':e+(1+e)*initial_error,
                   'two_invocation_error_including_initial':2*e+e*e+(1+e)**2*initial_error,
                   'causal_row_repair_infinity_norm':float(np.linalg.norm(repair,1))}
    return {'H':h,'H_inverse':inv,'ops':ops,'x0':x0,'certificate':certificate}

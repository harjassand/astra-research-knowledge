#!/usr/bin/env python3
"""Post-release cross-review checks; reads frozen peer code without changing it."""
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


warm = module('warm_replay', HERE/'replay_multiport.py')
compact = module('compact_replay', HERE.parent/'compact/native_multiport_check.py')


def scalar_instrument():
    # Direct Gauss-Hermite integration of compact's outcome density, not its
    # evaluate() covariance path. Fourier-transform convention is exp(+iky).
    nodes, weights = np.polynomial.hermite.hermgauss(80)
    q, c, p, f, eta, vb, vd, gain = .2, .11, -.17, .4, .7, 3., 5., .31
    W = f*vb+(1-f)*vd+(1-eta)/(2*eta)
    spins = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    error = 0.
    for a, b in spins:
        for ap, bp in spins:
            qs, ps, qsp, psp = q*a+c*b, p*b, q*ap+c*bp, p*bp
            dq, dp = qs-qsp, ps-psp
            C = np.exp(-vb*(dq*dq+dp*dp)/2 + .5j*(qsp*ps-psp*qs))
            L = math.sqrt(f)*vb*dq + .5j*math.sqrt(f)*(ps+psp)
            k = gain*(a-ap)
            y = L.imag+math.sqrt(2*W)*nodes
            integrand = np.exp(L.real*L.real/(2*W)
                              -1j*L.real*(y-L.imag)/W+1j*k*y)
            direct = C*np.dot(weights, integrand)/math.sqrt(math.pi)
            closed = C*np.exp(-W*k*k/2+k*L)
            error = max(error, float(abs(direct-closed)))
    assert error < 1e-12
    return error


def constrained_subspace_diagnostic(model):
    # The public function permits temporal_basis with wiener_fixed_phase, but
    # its adjustment leaves that basis. Current frozen data never call this
    # combination, so this is a latent API defect, not a failed recorded claim.
    n, f, eta, v = model['bins'], .25, .9, 10.5
    y = model['aligned_p'][:n]
    vb = v*(model['outputs']@model['outputs'].T)
    M = f*y@vb@y.T+((1-f)*v+(1-eta)/(2*eta))*np.eye(n)
    c = math.sqrt(f)*y@vb@model['generator'][0]
    basis = model['q'].reshape(n, 1)/np.linalg.norm(model['q'])
    h = math.sqrt(f)*model['p']
    target = float(model['q']@model['p'])
    g0 = basis@np.linalg.solve(basis.T@M@basis, basis.T@c)
    adjust = np.linalg.solve(M, h)
    implemented = g0+adjust*(target-h@g0)/(h@adjust)
    # Correct constrained solve within the allowed basis.
    Mr, cr, hr = basis.T@M@basis, basis.T@c, basis.T@h
    ar = np.linalg.solve(Mr, cr)
    zr = np.linalg.solve(Mr, hr)
    ar += zr*(target-hr@ar)/(hr@zr)
    repaired = basis@ar
    outside = np.linalg.norm(implemented-basis@(basis.T@implemented))
    assert outside > 1e-4
    assert abs(h@implemented-target) < 1e-12
    assert abs(h@repaired-target) < 1e-12
    return {'gain_outside_allowed_subspace_norm': float(outside),
            'implemented_norm2': float(implemented@implemented),
            'repaired_subspace_norm2': float(repaired@repaired),
            'recorded_frozen_cases_affected': False}


def matched_models():
    gamma, kappa, v = .08, .01, 10.5
    grid = np.linspace(0, 2*math.pi, 8193)
    p = warm.pulse(grid, gamma, kappa)
    gammas = gamma*np.array([.6, .4])
    bright = np.sqrt(gammas/gamma)
    k = warm.residual_kernel(p['rd'], p['re'], gammas, bright)
    G = warm.actual_output_G(grid, k, gamma, kappa, gammas, np.full(2,v-.5), v)
    comparisons, last = [], None
    for bins in [80, 160, 320]:
        model = compact.make_dilation(bins, gamma, kappa)
        item = compact.evaluate(model, 1., 1., v, v, v, 'bright_cancel')
        comparisons.append({'bins': bins,
            'covariance_max_abs_error': float(np.max(np.abs(np.array(item['residual_phase_covariance'])-G))),
            'theta_abs_error': abs(item['theta']-p['logical']),
            'closure_error': model['closure_error'],
            'CCR_max_error': model['commutator_error']})
        last = model
    assert comparisons[-1]['covariance_max_abs_error'] < 2e-8
    assert comparisons[-1]['theta_abs_error'] < 2e-6
    return {'same_declared_model': {'gamma': gamma, 'kappa': kappa, 'v': v,
            'f': 1., 'eta': 1., 'omega_m_hbar': 1.},
            'warm_continuum_theta': p['logical'], 'warm_continuum_G': G.tolist(),
            'comparisons': comparisons}, last


def paid_reference():
    rows = []
    for v in [10.5, 1000.5, 1000000.5]:
        for r in [.01, .1, 1.]:
            # Two-mode covariance created by the actual D/vacuum BS.
            varD = (1-r)*v+r/2
            varR = r*v+(1-r)/2
            cov = math.sqrt(r*(1-r))*(v-.5)
            posterior = varD-cov*cov/varR
            formula = v/(2*varR)
            assert abs(posterior-formula) < 1e-7
            assert posterior >= .5-1e-7
            rows.append({'v': v, 'r': r, 'posterior': posterior,
                         'cold_replacement_floor': .5})
    return rows


def main():
    same, last = matched_models()
    result = {'post_peer_release_only': True,
              'scalar_outcome_instrument_max_integration_error': scalar_instrument(),
              'matched_model_replay': same,
              'latent_constrained_temporal_basis_defect': constrained_subspace_diagnostic(last),
              'paid_reference_BS_covariance_checks': paid_reference()}
    out = HERE/'CROSS_REVIEW_CHECKS.json'
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

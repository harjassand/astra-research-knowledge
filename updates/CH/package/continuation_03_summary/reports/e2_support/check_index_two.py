#!/usr/bin/env python3
"""Floating diagnostics for the exact index-two GKP defect gate.

The entropy inequalities are analytic. These unvalidated quadratures are not
certified capacity witnesses and do not establish global optimality.
"""
import json
import math
from pathlib import Path
import numpy as np


def one_dimensional_parts(period, variance, points=16384):
    x = period * ((np.arange(points) + .5) / points - .5)
    even, odd, shifted = (np.zeros(points) for _ in range(3))
    images = math.ceil(10 * math.sqrt(variance) / period) + 2
    for image in range(-images, images + 1):
        z = x + image * period
        term = np.exp(-z*z/(2*variance)) / math.sqrt(2*math.pi*variance)
        if image % 2:
            odd += term
        else:
            even += term
        z_shifted = z + period/2
        shifted += np.exp(-z_shifted*z_shifted/(2*variance)) / math.sqrt(2*math.pi*variance)
    density = even + odd
    rho_deficit = float(np.mean(4*even*odd/density)) * period
    beta_deficit = float(np.mean((np.sqrt(density)-np.sqrt(shifted))**2)) * period/2
    return rho_deficit, beta_deficit, float(np.mean(density))*period


def rectangular(variance, aspect, points=16384):
    h = math.sqrt(2*math.pi)
    rho_deficit, _, nq = one_dimensional_parts(h*aspect, variance, points)
    _, beta_deficit, np_ = one_dimensional_parts(h/aspect, variance, points)
    rho, beta = 1-rho_deficit, 1-beta_deficit
    record = dict(variance=variance, aspect=aspect, rho=rho, beta=beta,
                  rho_deficit=rho_deficit, beta_deficit=beta_deficit,
                  stable_deficit_log_ratio=math.log(rho_deficit/beta_deficit),
                  normalization_error=max(abs(nq-1), abs(np_-1)))
    if rho > beta:
        n = math.floor(math.log(2*math.log(2))/math.log(rho/beta)) + 1
        margin = rho**n/(2*math.log(2))-beta**n
        record.update(sufficient_repeat_block=n, ideal_lower_bound=margin,
                      ideal_lower_bound_per_mode=margin/n)
    return record


def threshold(aspect):
    lo, hi = .3, .4
    for _ in range(32):
        mid = (lo+hi)/2
        if rectangular(mid, aspect, points=8192)['stable_deficit_log_ratio'] < 0:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def two_dimensional_parts(basis, parity, variance, points=128):
    x = (np.arange(points)+.5)/points-.5
    u = np.stack(np.meshgrid(x, x, indexing='ij'), axis=-1).reshape(-1, 2)
    even, odd, shifted = (np.zeros(len(u)) for _ in range(3))
    scale = 1/(2*math.pi*variance)
    for i in range(-4, 5):
        for j in range(-4, 5):
            lattice_image = np.array([i,j])
            z = (u+lattice_image) @ basis.T
            term = np.exp(-np.sum(z*z, axis=1)/(2*variance))*scale
            if int(lattice_image @ parity) % 2:
                odd += term
            else:
                even += term
            z = (u+lattice_image+parity/2) @ basis.T
            shifted += np.exp(-np.sum(z*z, axis=1)/(2*variance))*scale
    density = even+odd
    volume = abs(float(np.linalg.det(basis)))
    return (float(np.mean(4*even*odd/density))*volume,
            float(np.mean((np.sqrt(density)-np.sqrt(shifted))**2))*volume/2,
            float(np.mean(density))*volume)


def hexagonal(variance, parity=(1,0)):
    a = math.sqrt(2/math.sqrt(3))
    matrix = np.array([[a,a/2],[0,a*math.sqrt(3)/2]])
    h = math.sqrt(2*math.pi)
    c = np.array(parity)
    rho_deficit, _, nq = two_dimensional_parts(h*matrix, c, variance)
    _, beta_deficit, np_ = two_dimensional_parts(h*np.linalg.inv(matrix).T, c, variance)
    return dict(variance=variance, parity=parity, rho=1-rho_deficit,
                beta=1-beta_deficit,
                stable_deficit_log_ratio=math.log(rho_deficit/beta_deficit),
                normalization_error=max(abs(nq-1), abs(np_-1)))


def theta(t):
    return 1+2*sum(math.exp(-math.pi*t*j*j) for j in range(1,30))


def main():
    aspects = [.5,.7,1,1.2,1.4,1.6,1.68,1.8,2,2.2,2.5,3,4]
    roots = [dict(aspect=a, floating_threshold=threshold(a)) for a in aspects]
    records = [rectangular(v,a) for v in [.34,.36,1/math.e,.4,.49,.5]
               for a in [1,1.68,2,3]]
    hex_records = [hexagonal(v,c) for v in [.34,1/math.e,.49]
                   for c in [(1,0),(1,1)]]
    lo, hi = .3,.45
    for _ in range(24):
        mid = (lo+hi)/2
        if hexagonal(mid)['stable_deficit_log_ratio'] < 0:
            lo=mid
        else:
            hi=mid
    result = dict(status='floating_point_diagnostics_not_capacity_certificate',
                  rectangular_points_per_period=16384,
                  rectangular_thresholds=roots, rectangular_records=records,
                  hexagonal_points_per_coordinate=128, hexagonal_records=hex_records,
                  hexagonal_floating_threshold=(lo+hi)/2,
                  rational_transducer_center_l1_bound=(theta(1.5)**2-1)/(2-theta(6)**2))
    path = Path(__file__).with_name('index_two_diagnostics.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(rectangular_thresholds=roots,
                         hexagonal_threshold=result['hexagonal_floating_threshold'],
                         rational_center_bound=result['rational_transducer_center_l1_bound']), indent=2))
    print('maximum normalization error', max(r['normalization_error'] for r in records+hex_records))
    print('saved',path)


if __name__ == '__main__':
    main()

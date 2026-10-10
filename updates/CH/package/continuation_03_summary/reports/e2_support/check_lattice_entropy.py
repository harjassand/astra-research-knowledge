#!/usr/bin/env python3
"""Deterministic quadrature check of the rectangular GKP quotient identities.

This script is a floating-point diagnostic, not an interval capacity certificate.
It preserves the analog syndrome and accounts for stabilizer degeneracy.
"""
import json
import math
from pathlib import Path
import numpy as np


def wrapped_entropy_fisher(period, variance, points=16384):
    step = period / points
    x = -period / 2 + (np.arange(points) + .5) * step
    images = math.ceil(9 * math.sqrt(variance) / period) + 2
    density = np.zeros(points)
    derivative = np.zeros(points)
    for k in range(-images, images + 1):
        z = x + k * period
        term = np.exp(-z*z/(2*variance)) / math.sqrt(2*math.pi*variance)
        density += term
        derivative -= z/variance * term
    h = -float(np.sum(density * np.log2(density))) * step
    j = float(np.sum(derivative*derivative/density)) * step
    return h, j, float(np.sum(density) * step)


def quotient(variance, ratio):
    dq, dp = math.sqrt(math.pi)*ratio, math.sqrt(math.pi)/ratio
    hq, jq, nq = wrapped_entropy_fisher(dq, variance)
    hp, jp, np_ = wrapped_entropy_fisher(dp, variance)
    h2q, j2q, n2q = wrapped_entropy_fisher(2*dq, variance)
    h2p, j2p, n2p = wrapped_entropy_fisher(2*dp, variance)
    hsyndrome = hq + hp
    hwrapped_stabilizer = h2q + h2p
    hnoise = math.log2(2*math.pi*math.e*variance)
    conditional_logical_entropy = hwrapped_stabilizer - hsyndrome
    degeneracy = hnoise - hwrapped_stabilizer
    deficit = math.log2(math.pi) - hsyndrome
    hashing = math.log2(1/(math.e*variance))
    ic = 1-conditional_logical_entropy
    from_degeneracy = hashing - deficit + degeneracy
    return dict(variance=variance, rectangular_ratio=ratio,
        inner_coherent_information=ic, logical_entropy=conditional_logical_entropy,
        stabilizer_degeneracy=degeneracy, syndrome_uniformity_deficit=deficit,
        gaussian_hashing_term=hashing, entropy_identity_error=ic-from_degeneracy,
        derivative_from_fisher=(jq+jp-j2q-j2p)/(2*math.log(2)),
        normalization_error=max(abs(nq-1), abs(np_-1), abs(n2q-1), abs(n2p-1)))


def main():
    records = [quotient(v,r) for v in [.3, .34, 1/math.e, .4, .49, .5]
               for r in [1, 2, 3]]
    for record in records:
        v, r = record['variance'], record['rectangular_ratio']
        dv = 1e-5
        numerical = (quotient(v+dv,r)['inner_coherent_information']
                     - quotient(v-dv,r)['inner_coherent_information'])/(2*dv)
        record['derivative_finite_difference']=numerical
        record['derivative_difference']=numerical-record['derivative_from_fisher']
    result=dict(status='floating_point_diagnostic_not_capacity_certificate',
                points_per_period=16384, records=records)
    path=Path(__file__).with_name('lattice_entropy_diagnostics.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    for record in records:
        if record['variance'] in [.49,.5]:
            print(json.dumps(record))
    print('max identity error', max(abs(r['entropy_identity_error']) for r in records))
    print('max de Bruijn difference', max(abs(r['derivative_difference']) for r in records))
    print('max normalization error', max(r['normalization_error'] for r in records))
    print('saved',path)


if __name__=='__main__':
    main()

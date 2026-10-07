"""Full-density quadrature probe of the parameter-independent product decoder.

This integrates the specified classical quartic law and compares the ENTIRE
Schur-Weyl block density, including exact multiplicities, with the Gibbs state.
It is a floating-point quadrature diagnostic, not an interval-certified bound.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from spin_sep_checks import A, b, irrep_spins, exp_hermitian


def decoded_blocks(N, radial_points=64, polar_points=16, azimuth_points=32):
    roots, weights = np.polynomial.legendre.leggauss(radial_points)
    radius = 2*(roots+1)  # [0,4]; tail is un-certified, exponentially tiny here.
    rweights = 2*weights*radius**2*np.exp(-4*radius**4/3)
    cosines, pweights = np.polynomial.legendre.leggauss(polar_points)
    j2s = list(range(N % 2, N+1, 2))
    Js = [irrep_spins(j2) for j2 in j2s]
    blocks = [np.zeros((j2+1, j2+1), complex) for j2 in j2s]
    theta = 4*N**(-.25)*radius
    logden = N*np.logaddexp(theta/2, -theta/2)
    normalization = 0.
    for cosine, pweight in zip(cosines, pweights):
        sinangle = math.sqrt(1-cosine*cosine)
        for index in range(azimuth_points):
            phi = 2*math.pi*index/azimuth_points
            u = np.array([sinangle*math.cos(phi), sinangle*math.sin(phi), cosine])
            sphere_weight = pweight/(2*azimuth_points)
            radial_weight = rweights*np.exp(radius**2*(u@A@u)+radius*(b@u))
            normalization += sphere_weight*np.sum(radial_weight)
            for Js_j, block in zip(Js, blocks):
                values, vectors = np.linalg.eigh(sum(u[k]*Js_j[k] for k in range(3)))
                coeff = radial_weight@np.exp(theta[:, None]*values[None, :]-logden[:, None])
                block += sphere_weight*(vectors*coeff[None, :])@vectors.conj().T
    return j2s, [block/normalization for block in blocks]


def target_blocks(N, j2s):
    blocks = []
    multiplicities = []
    for j2 in j2s:
        j = j2/2
        Js = irrep_spins(j2)
        H = sum(A[k,k]*Js[k]@Js[k]/N**1.5+b[k]*Js[k]/N**.75
                for k in range(3))
        blocks.append(math.exp(2*j*(j+1)/N)*exp_hermitian(H))
        multiplicities.append((j2+1)*math.comb(N+1,(N-j2)//2)/(N+1))
    normalization = sum(m*np.trace(block).real for m,block in zip(multiplicities, blocks))
    return [block/normalization for block in blocks], multiplicities


def check(N, **quadrature):
    j2s, decoded = decoded_blocks(N, **quadrature)
    target, multiplicities = target_blocks(N, j2s)
    trace = sum(m*np.trace(block).real for m,block in zip(multiplicities, decoded))
    error = sum(m*np.sum(abs(np.linalg.eigvalsh((left-right+left.conj().T-right.conj().T)/2)))/2
                for m,left,right in zip(multiplicities, decoded, target))
    return dict(N=N, decoded_trace=float(trace), trace_distance=float(error),
                N_one_quarter_times_error=float(N**.25*error),
                N_one_half_times_error=float(N**.5*error), quadrature=quadrature)


def main():
    data = dict(scope='Floating-point radial/spherical full-density quadrature, not certified; no hardware.',
                parameters=dict(A_diagonal=np.diag(A).tolist(), b=b.tolist()),
                coarse=[check(N) for N in [4,8,16,32]],
                refinement=check(16, radial_points=96, polar_points=24, azimuth_points=48))
    path = Path(__file__).with_name('spin_universal_decoder_checks.json')
    path.write_text(json.dumps(data, indent=2))
    print(json.dumps(data, indent=2))
    print('Saved', path)


if __name__ == '__main__':
    main()

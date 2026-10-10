#!/usr/bin/env python3
"""Independent scoped checks. All q/H3 calls use auditor-known matrices.

No data are acquired from a physical system. mpmath checks do not prove
novelty, a sample bound, or global stability of the inverse problem.
"""
from math import comb, factorial, sqrt
from pathlib import Path
import json
import numpy as np
import mpmath as mp

OUT = Path(__file__).resolve().parent


def helmert(n):
    u = np.zeros((n, n))
    u[0] = 1 / np.sqrt(n)
    for r in range(2, n + 1):
        u[r - 1, :r - 1] = 1 / np.sqrt(r * (r - 1))
        u[r - 1, r - 1] = -(r - 1) / np.sqrt(r * (r - 1))
    return u


def cauchy_witness(n):
    eps = 1 / (n * sqrt(n * comb(2*n-2, n-1)))
    u = helmert(n)
    k = (u * np.arange(1, n+1)) @ u.T
    hidden = k[1:, 0]**2
    expected = np.arange(2, n+1)*np.arange(1, n)/(4*n)
    return dict(n=n, uniform_frequency_projection_bound=eps,
                samples_n_sigma_min_upper_bound=sqrt(n)*eps,
                relative_inverse_noise_gain_lower_bound=1/(sqrt(n)*eps),
                helmert_orthogonality_error=float(np.linalg.norm(u@u.T-np.eye(n))),
                hidden_beta_identity_error=float(np.max(np.abs(hidden-expected))),
                min_hidden_beta=float(hidden.min()),
                min_hidden_beta_gap=float(np.diff(hidden).min()))


def finite_pair_check(n=5):
    mp.mp.dps = 85
    u = mp.matrix(n,n)
    for j in range(n): u[0,j] = 1/mp.sqrt(n)
    for r in range(2,n+1):
        for j in range(r-1): u[r-1,j] = 1/mp.sqrt(r*(r-1))
        u[r-1,r-1] = -(r-1)/mp.sqrt(r*(r-1))
    lam = list(range(1,n+1))
    k = u*mp.diag(lam)*u.T
    alpha = [mp.mpf(1)]*n
    s,t = mp.j*mp.mpf('0.6'), mp.j*mp.mpf('1.1')
    c=(s-t)/2
    def q(z): return u*mp.matrix([1/(mp.sqrt(n)*(z+l)) for l in lam])
    qs,qt=q(s),q(t)
    b=sum(alpha[r]*k[r,0]**2*qs[r]*qt[r] for r in range(1,n))
    def hidden(R):
        a,d=q(c+R),q(c-R)
        return sum(alpha[r]*qs[r]*qt[r]*a[r]*d[r] for r in range(1,n))
    convergence=[]
    for omega in [10,30,100,300]:
        approx=(mp.j*omega)**4*hidden(mp.j*omega)
        convergence.append(dict(omega=omega, relative_error=float(abs((approx-b)/b))))
    zz=[-(mp.mpf(j)**2) for j in range(1,n)]
    weights=[]
    for j,z in enumerate(zz):
        D=mp.fprod((l+c)**2-z for l in lam)
        denominator=mp.fprod(z-zz[h] for h in range(n-1) if h!=j)
        weights.append((-1)**n*D/denominator)
    recovered=sum(w*hidden(mp.j*(j+1)) for j,w in enumerate(weights))
    return dict(n=n, high_pair_convergence=convergence,
                finite_known_pole_samples=n-1,
                finite_interpolation_relative_error=float(abs((recovered-b)/b)),
                exact_H3_error_l1_gain=float(sum(abs(w) for w in weights)),
                port_transfer_assumed_exact=True)


def oscillator_cluster_check(n=8):
    lam=np.arange(1,n+1,dtype=float)
    omega=np.sqrt(lam)
    delta=min(np.diff(omega).min(),2*omega.min())
    gamma=delta/(1000*n)
    poles=np.concatenate([-gamma/2+1j*omega,-gamma/2-1j*omega,
                          gamma/2+1j*omega,gamma/2-1j*omega])
    centers=np.concatenate([omega,-omega])
    samples=np.concatenate([1j*(centers+gamma/2),1j*(centers-gamma/2)])
    scaled=gamma/(samples[:,None]-poles[None,:])
    sv=np.linalg.svd(scaled,compute_uv=False)
    min_block=10.0
    for ratio in np.linspace(-1,1,1001):
        z=np.array([-.5+1j*ratio/2,.5-1j*ratio/2])
        sample=np.array([.5j,-.5j])
        C=1/(sample[:,None]-z[None,:])
        min_block=min(min_block,float(np.linalg.svd(C,compute_uv=False)[-1]))
    return dict(n=n,gamma=gamma,same_side_min_imaginary_gap=delta,
                scaled_residue_matrix_min_singular=float(sv[-1]),
                scaled_residue_matrix_condition=float(sv[0]/sv[-1]),
                close_pair_grid_min_singular=min_block,
                proved_close_pair_lower_bound=.16)


def main():
    result=dict(disclosure=__doc__,
                cauchy_witnesses=[cauchy_witness(n) for n in [4,8,16,32,64]],
                paired_first_order=finite_pair_check(),
                oscillator_pole_clusters=[oscillator_cluster_check(n) for n in [4,8,16,32]])
    (OUT/'independent_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()

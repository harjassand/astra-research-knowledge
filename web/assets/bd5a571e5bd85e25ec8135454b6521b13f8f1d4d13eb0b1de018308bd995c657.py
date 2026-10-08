#!/usr/bin/env python3
"""Finite diagnostics for the local-access theorem; numpy only.

This does not certify the all-size theorem. Small-N density matrices are built
from exact Schur projectors, diagonalized in double precision. Large-N z-readout
laws use conserved sector weights and hypergeometric sampling; this is a
classical measurement lower bound on quantum trace distance.
"""
from pathlib import Path
from math import lgamma, log, exp, sqrt, pi
import json
import numpy as np

OUT = Path(__file__).resolve().parent


def sector_law(n):
    ms = np.arange(n % 2, n + 1, 2, dtype=int)
    logw = np.array([
        2*log(int(m)+1)-log((n+int(m))/2+1)
        +lgamma(n+1)-lgamma((n-int(m))/2+1)
        -lgamma((n+int(m))/2+1)-n*log(2)
        for m in ms
    ])
    w = np.exp(logw)
    rawmass = float(w.sum())
    w /= rawmass
    return ms, w, rawmass


def bottom_density(n):
    """rho_inf at nu=0, with initially white Schur-sector weights."""
    dim = 1 << n
    rho = np.zeros((dim, dim))
    for down in range((n+1)//2, n+1):
        m = n/2-down
        j = -m
        ids = [i for i in range(dim) if i.bit_count() == down]
        index = {i:k for k,i in enumerate(ids)}
        j2 = np.eye(len(ids))*(m*m+n/2)
        for col,i in enumerate(ids):
            for a in range(n):
                if not (i >> a) & 1:
                    for b in range(n):
                        if (i >> b) & 1:
                            row = index[i ^ (1 << a) ^ (1 << b)]
                            j2[row,col] += 1.0
        vals, vecs = np.linalg.eigh(j2)
        keep = np.abs(vals-j*(j+1)) < 1e-8
        projector = vecs[:,keep] @ vecs[:,keep].T
        rho[np.ix_(ids,ids)] = (2*j+1)/(2**n)*projector
    return rho


def small_density_checks():
    rows = []
    for n in range(2,11):
        rho = bottom_density(n)
        assert abs(np.trace(rho)-1) < 1e-12
        assert np.linalg.eigvalsh(rho)[0] > -1e-12
        ms,w,_ = sector_law(n)
        casimir = float(np.dot(w,ms*(ms+2)/4))
        assert abs(casimir-3*n/4) < 1e-10
        for r in range(1,min(n,5)+1):
            d = 1 << r
            reduced = np.trace(rho.reshape(d,1 << (n-r),d,1 << (n-r)),
                               axis1=1,axis2=3)
            eig = np.linalg.eigvalsh(reduced)
            tv = float(np.abs(eig-1/d).sum()/2)
            positive = eig[eig > 1e-13]
            rel = float(np.sum(positive*np.log(positive*d)))
            chi = float(d*np.dot(eig,eig)-1)
            entropy_bound = r*log(3*n+1)/(2*n)
            universal_bound = min(1,6*r/(n+1)+6*sqrt(log(2)*r/(n+1)))
            assert tv <= universal_bound+1e-12
            assert rel <= entropy_bound+1e-11
            assert rel <= log(1+chi)+1e-11
            rows.append(dict(N=n,r=r,quantum_half_trace=tv,
                             relative_entropy_nats=rel,chi_square=chi,
                             entropy_bound=entropy_bound,
                             common_measure_bound=universal_bound))
    return rows


def z_law(n,r):
    """Selected stationary z-readout count at nu=0; exchangeability suffices."""
    ms,w,rawmass = sector_law(n)
    logfact = np.array([lgamma(k+1) for k in range(n+1)])
    def logchoose(a,k):
        return logfact[a]-logfact[k]-logfact[a-k]
    h = np.arange(r+1)
    prob = np.zeros(r+1)
    logden = float(logchoose(n,r))
    dropped = 0.0
    for m,weight in zip(ms,w):
        if weight < 1e-18:
            dropped += float(weight)
            continue
        up = (n-int(m))//2
        ok = (h <= up) & (r-h <= n-up)
        z = h[ok]
        prob[ok] += weight*np.exp(logchoose(up,z)
                       +logchoose(n-up,r-z)-logden)
    white = np.exp(logchoose(r,h)-r*log(2))
    tv = float(np.abs(prob-white).sum()/2)
    mu = float(np.dot(w,ms/2))
    mean = float(np.dot(prob,h-r/2))
    mean_expected = -r*mu/n
    assert abs(mean-mean_expected) < 2e-6*max(1,abs(mean_expected))
    pscale = mu/sqrt(n)
    result = dict(N=n,r=r,r_over_N=r/n,classical_half_trace=tv,
                  target_probability_mass=float(prob.sum()),
                  raw_sector_mass=rawmass,dropped_sector_mass=dropped,
                  polarization_over_sqrtN=pscale,
                  magnetization_mean=mean,
                  mean_identity=mean_expected,
                  macro_bound_alpha_P2_over6=(r/n)*pscale**2/6,
                  chebyshev_preparations_for_error_sum_0p2=
                      int(np.ceil(20*n/(r*pscale**2))))
    return result


def main():
    small = small_density_checks()
    large = []
    for n in [64,256,1024,4096]:
        rs = sorted(set([1,int(sqrt(n)),int(n**.75),n//4,n//2]))
        for r in rs:
            large.append(z_law(n,r))
    result = dict(status='finite_double_precision_diagnostics_not_proof',
                  model='selected nu=0 stationary state, white initial Schur weights',
                  log_base='natural',half_trace_convention=True,
                  small_density=small,z_measurement=large,
                  resource='NumPy CPU, largest density 1024 by 1024; no cloud',
                  limitations=['Large-N z laws lower-bound quantum trace distance only.',
                               'No floating output is an all-size certificate.',
                               'Uniform common-measure constant is loose and trivial at small N.'])
    (OUT/'diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(small_fixtures=len(small),z_fixtures=len(large),
                         status=result['status'],
                         largest_N=large[-1]['N'],
                         last_examples=large[-5:]),indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Actual conservative residual family; finite spectral diagnostics only."""
import csv
import math
from pathlib import Path
import numpy as np


def lse(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x-m) for x in xs))


def logcoscoef(n, omega):
    if omega == 0:
        return 0. if n == 0 else -math.inf
    return -.5*omega*omega + n*math.log(abs(omega)) - .5*math.lgamma(n+1)


def loginvnorm(n, kappa, derivative=False):
    a = math.sqrt(1-kappa*kappa)
    lr = math.log(kappa/a)
    terms = []
    for j in range(n+1):
        x = -2*math.log(a) + 2*j*lr + math.lgamma(n+1)-math.lgamma(j+1)-math.lgamma(n-j+1)
        x -= 2*math.log(j+2)
        if not derivative:
            x -= 2*math.log(j+1)
        terms.append(x)
    return .5*lse(terms)


def compute(k, kappa=.5, delta=.2, quadrature=100, maximum_degree=2048):
    a = math.sqrt(1-kappa*kappa)
    xx, ww = np.polynomial.legendre.leggauss(quadrature)
    us, ws = (xx+1)/2, ww/2
    J, D, JS, DS, residual = [], [], [], [], []
    for n in range(0, maximum_degree+1, 2):
        lc = [math.log(kappa*delta)+logcoscoef(n,k)]
        for u, w in zip(us, ws):
            base = math.log(float(w))-.5*k*k*(1-u*u)
            lc.append(math.log(kappa*delta)+base+logcoscoef(n,k*u))
            lc.append(math.log(delta*delta/2)+base+logcoscoef(n,k*(1+u)))
            lc.append(math.log(delta*delta/2)+base+logcoscoef(n,k*(1-u)))
        coef = lse(lc)
        lj, ld = loginvnorm(n,kappa), loginvnorm(n,kappa,True)
        residual.append(2*coef)
        J.append(2*(coef+lj))
        D.append(2*(coef+ld))
        JS.append(2*(coef+lj+n*math.log(a)))
        DS.append(2*(coef+ld+n*math.log(a)))
    lam = k*k/(a*a)
    lower = kappa*delta/a * math.exp((lam-k*k)/2)/(2*(2*lam+2)**2) if lam >=16 else 0.
    return {
        'k':k, 'kappa':kappa, 'delta':delta, 'Lip_bound':kappa+delta,
        'max_degree':maximum_degree, 'quad_nodes':quadrature,
        'residual_L2_partial': math.exp(.5*lse(residual)),
        'J_unsmoothed_L2_partial':math.exp(.5*lse(J)),
        'DZ_u_unsmoothed_L2_partial':math.exp(.5*lse(D)),
        'J_critical_smoothed_L2_partial':math.exp(.5*lse(JS)),
        'DZ_u_critical_smoothed_L2_partial':math.exp(.5*lse(DS)),
        'proved_J_lower_bound':lower,
    }


if __name__ == '__main__':
    rows = [compute(k) for k in [1,2,4,8,12,16]]
    path = Path(__file__).resolve().parent/'genuine_family.csv'
    with path.open('w',newline='') as f:
        wr=csv.DictWriter(f, fieldnames=list(rows[0]))
        wr.writeheader(); wr.writerows(rows)
    for r in rows:
        print('k={k:2d} R={residual_L2_partial:.6g} J={J_unsmoothed_L2_partial:.6g} J_sm={J_critical_smoothed_L2_partial:.6g} proved_lower={proved_J_lower_bound:.6g}'.format(**r))

"""Owned exact checks of the newly derived ball and Lie-chart identities.

Finite transcription evidence only. No diffusion is simulated, no all-N
asymptotic claim follows from fixtures, and no peer code is imported.
"""
from itertools import product
from pathlib import Path
import json
import time
import sympy as s
import mpmath as mp


def tensor(xs):
    out = s.ones(1)
    for x in xs:
        out = s.kronecker_product(out, x)
    return out


def same(a, b):
    assert all(s.simplify(t) == 0 for t in a - b)


def local_axes(d):
    x = s.zeros(d)
    y = s.zeros(d)
    x[0, 1] = x[1, 0] = 1 / s.sqrt(2)
    y[0, 1] = -s.I / s.sqrt(2)
    y[1, 0] = s.I / s.sqrt(2)
    z = s.diag(1 / s.sqrt(2), -1 / s.sqrt(2), *([0] * (d - 2)))
    return [x, y, z]


def ball_checks():
    rows = []
    for d in (2, 3):
        axes = local_axes(d)
        for t in axes:
            assert s.trace(t) == 0 and s.trace(t*t) == 1
            for sign in (-1, 1):
                local = (s.eye(d) + sign*t) / d
                assert local.is_hermitian and s.trace(local) == 1
                assert all(v.is_nonnegative for v in local.eigenvals())
        for n in (1, 2, 3):
            for r in range(1, n + 1):
                active = [axes[j % len(axes)] for j in range(r)]
                p = tensor(active + [s.eye(d)] * (n - r))
                for parity in (-1, 1):
                    signs = [v for v in product((-1, 1), repeat=r)
                             if s.prod(v) == parity]
                    mixture = sum((tensor([(s.eye(d) + z*t) / d
                                           for z, t in zip(v, active)] +
                                          [s.eye(d) / d] * (n - r))
                                   for v in signs), s.zeros(d**n)) / len(signs)
                    same(mixture, (s.eye(d**n) + parity*p) / d**n)
                rows.append({'d': d, 'N': n, 'support': r,
                             'parity_vertices_exact': True})
            eta = s.Rational(1, 3*d)
            rho = s.diag(*[s.Rational(2**j, 2**d - 1) for j in range(d)])
            # Use a stronger cutoff only when this specific rho permits it.
            eta = min(eta, min(rho.diagonal()) / 2)
            prime = (rho - eta*s.eye(d)) / (1-d*eta)
            white = (d*eta)**n * s.eye(d**n) / d**n
            other = s.zeros(d**n)
            for bits in product((0, 1), repeat=n):
                if not any(bits):
                    continue
                weight = s.prod((1-d*eta) if b else d*eta for b in bits)
                other += weight * tensor([prime if b else s.eye(d)/d for b in bits])
            same(tensor([rho]*n), white+other)
            assert s.trace(other) == 1-(d*eta)**n
            rows.append({'d':d, 'N':n, 'white_weight_exact':str((d*eta)**n)})
    return rows


def chart_checks():
    ell = s.log(2)
    h = [ell, 0, -ell]
    p = [s.Rational(4, 7), s.Rational(2, 7), s.Rational(1, 7)]
    rho = s.diag(*p)
    jx = s.Matrix([[0,1,0], [1,0,1], [0,1,0]])
    jy = s.Matrix([[0,-s.I,0], [s.I,0,-s.I], [0,s.I,0]])
    jz = s.diag(1,0,-1)
    rows=[]
    for label, t in zip(('Jx','Jy','Jz'), (jx,jy,jz)):
        y=s.zeros(3)
        kt=s.zeros(3)
        for i in range(3):
            for j in range(3):
                z=h[i]-h[j]
                g0=1 if z==0 else z*(p[i]+p[j])/(2*(p[i]-p[j]))
                y[i,j]=g0*t[i,j]
                kt[i,j]=s.I*(p[i]-p[j])/(p[i]+p[j])*t[i,j]
        # Explicit divided-difference Df, with the normalizer differentiated.
        out=s.zeros(3)
        mean=s.trace(rho*y)
        for i in range(3):
            for j in range(3):
                if i==j:
                    out[i,j]=p[i]*(y[i,i]-mean)
                else:
                    out[i,j]=(p[i]-p[j])/(h[i]-h[j])*y[i,j]
        v=(t*rho+rho*t)/2-s.trace(rho*t)*rho
        same(out,v)
        same(-s.I*(t*rho-rho*t)/2,
             (kt*rho+rho*kt)/2-s.trace(rho*kt)*rho)
        if label in ('Jx','Jy'):
            same(y, 3*ell*t/2)
        else:
            same(y,t)
        rows.append({'proper_Lie_space':'spin1_SU2','axis':label,
                     'Df_g0_equals_V':True,'R_over2_equals_V_K':True})
    return rows


def threshold_checks():
    k,r=s.symbols('k r',positive=True)
    l=k/2+s.sqrt(k*k/4+k*r)
    assert s.simplify(s.expand(l*l/k-l-r))==0
    mp.mp.dps=60
    rows=[]
    for d,alpha,bound in ((2,mp.mpf('0.01'),0),(2,1,2),(3,1,0),(5,5,3)):
        beta=2*alpha*(d-1)*(d+3)+d*bound
        hbar=2*alpha*(d-1)*(d+1)/d+bound
        kappa=8*alpha*d*(d-1)
        q=max(hbar,1)
        r=hbar+(d+1)*mp.log(d)+beta+3+mp.log(2*q)
        l=kappa/2+mp.sqrt(kappa*kappa/4+kappa*r)
        x=d*mp.log(d)+beta+l
        exit_rate=l*l/kappa
        for n in (1,2,7,100):
            log_error=mp.log(2*hbar*n)-n*(exit_rate-hbar)
            log_ball=-n*(x+mp.log(d))
            assert log_error <= log_ball-2*n+mp.mpf('1e-40')
        rows.append({'d':d,'alpha':str(alpha),'field_bound':bound,
                     'log_eta':str(-x),'log_delta_star':str(mp.log(alpha/40)-2*x),
                     'all_N_quadratic_identity_exact':True,
                     'finite_N_absorption_fixtures':True})
    return rows


if __name__=='__main__':
    start=time.perf_counter()
    result={'status':'PASS_EXACT_AND_SCALAR_TRANSCRIPTION',
            'ball_fixtures':ball_checks(),'chart_fixtures':chart_checks(),
            'threshold_fixtures':threshold_checks(),
            'scope':'Finite algebra and scalar checks only; no SDE/compiler/external validation.'}
    result['runtime_seconds']=time.perf_counter()-start
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'runtime_seconds':result['runtime_seconds']}))

"""Actual compatible periodic-gradient search for negative heat dissipation.

This objective is distinct from Jensen/quasiconvexity. A negative witness,
if acquired, is subsequently rationalized and integrated in exact Fourier
arithmetic before being accepted.
"""
from pathlib import Path
from itertools import product
from math import factorial
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import json
import time
import numpy as np
import sympy as s
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent


def tensor():
    target = json.loads((ROOT.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json').read_text())
    p = list(map(s.Rational, target['coefficients']))
    a, b, c, d = z = s.symbols('a b c d')
    u, v, w, q = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
    f = s.Poly(sum(v*t for v, t in zip(p, [u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w])), *z)
    out = np.zeros((4,)*4)
    for indices in product(range(4), repeat=4):
        counts = tuple(indices.count(i) for i in range(4))
        coeff = f.coeff_monomial(counts)
        out[indices] = float(coeff*s.prod(factorial(c) for c in counts)/24)
    return out, float(p[0])


class CompatibleHeat:
    def __init__(self, cutoff=2, grid=20, frequencies=None):
        self.freq = frequencies if frequencies is not None else [
            (i,j) for i in range(cutoff+1) for j in range(-cutoff,cutoff+1)
            if i>0 or (i==0 and j>0)]
        largest = max(abs(v) for pair in self.freq for v in pair)
        assert grid > 4*largest
        theta = np.arange(grid)*2*np.pi/grid
        tx, ty = np.meshgrid(theta, theta, indexing='ij')
        points = np.stack([tx.ravel(),ty.ravel()], axis=1)
        n, m = len(points), len(self.freq)
        self.shape = (m, 2, 2)  # mode, cosine/sine potential, output component.
        self.M = np.zeros((n,4,m*4))
        self.N = np.zeros((n,2,4,m*4))
        for fi, k in enumerate(self.freq):
            kk = np.array(k,float)
            phase = points@kk
            norm = np.linalg.norm(kk)
            for trig in range(2):
                first = -np.sin(phase) if trig==0 else np.cos(phase)
                second = -np.cos(phase) if trig==0 else -np.sin(phase)
                for output in range(2):
                    col = fi*4+trig*2+output
                    for i in range(2):
                        entry = 2*output+i
                        self.M[:,entry,col] = first*kk[i]/norm
                        for j in range(2):
                            self.N[:,j,entry,col] = second*kk[i]*kk[j]/norm
        self.t, self.scale = tensor()
        self.n = n
        self.mflat = self.M.reshape(n*4,-1)
        self.nflat = self.N.reshape(n*8,-1)

    def evaluate(self, raw, gradient=True):
        length = np.linalg.norm(raw)
        if length == 0:
            raise ValueError('zero direction')
        coeff = raw/length
        a = (self.mflat@coeff).reshape(self.n,4)
        b = (self.nflat@coeff).reshape(self.n,2,4)
        bb = np.einsum('nsi,nsj->nij', b,b)
        ha = 12*(bb.reshape(self.n,16)@self.t.reshape(16,16)).reshape(self.n,4,4)
        h = ha.mean(axis=0)
        lin = np.einsum('nij,nj->ni',ha,a).mean(axis=0)
        background = -np.linalg.solve(h, lin)
        fulla = a+background
        grad_a = 2*np.einsum('nij,nj->ni',ha,fulla)
        value = .5*np.sum(fulla*grad_a)/self.n
        bnorm = np.sum(b*b)/self.n
        objective = value/(self.scale*bnorm)
        if not gradient:
            return {'objective':float(objective),'dissipation':float(value),
                    'background':background.tolist(),
                    'normalized_gradient_amplitudes':coeff.reshape(self.shape).tolist(),
                    'frequencies':self.freq,
                    'background_quadratic_eigenvalues':np.linalg.eigvalsh(h).tolist(),
                    'gradient_second_moment':float(np.sum(a*a)/self.n),
                    'Hessian_second_moment':float(bnorm)}
        aa = np.einsum('ni,nj->nij',fulla,fulla)
        hb = 12*(aa.reshape(self.n,16)@self.t.reshape(16,16)).reshape(self.n,4,4)
        grad_b = 2*np.einsum('nij,nsj->nsi',hb,b)
        dv = (self.mflat.T@grad_a.ravel()+self.nflat.T@grad_b.ravel())/self.n
        dn = 2*self.nflat.T@b.ravel()/self.n
        grad = dv/(self.scale*bnorm)-value*dn/(self.scale*bnorm**2)
        grad = (grad-coeff*np.dot(coeff,grad))/length
        return objective, grad


def main():
    start = time.monotonic()
    op = CompatibleHeat()
    rng = np.random.default_rng(278381)
    dim = np.prod(op.shape)
    x = rng.normal(size=dim)
    value, grad = op.evaluate(x)
    h = 1e-5
    numeric = np.array([(op.evaluate(x+np.eye(1,dim,i).ravel()*h)[0]
                         - op.evaluate(x-np.eye(1,dim,i).ravel()*h)[0])/(2*h)
                        for i in range(dim)])
    error = float(np.max(np.abs(numeric-grad)))
    assert error < 1e-7, error
    starts = [rng.normal(size=dim) for _ in range(24)]
    other = ROOT.parent/'compatible_quartic_attack/data/fourier_cutoff2.json'
    if other.exists():
        for run in json.loads(other.read_text())['runs']:
            amps = np.array(run['normalized_gradient_amplitudes'])
            if amps.shape == op.shape:
                # Peer records cosine/sine GRADIENT amplitudes; this code's
                # coefficients are cosine/sine POTENTIAL amplitudes.
                converted = np.stack([-amps[:,1,:], amps[:,0,:]],axis=1)
                starts.append(converted.ravel())
    best = None
    summaries = []
    for i, initial in enumerate(starts):
        result = minimize(op.evaluate, initial, method='L-BFGS-B', jac=True,
                          options={'maxiter':350,'ftol':1e-13,'gtol':1e-8,'maxls':35})
        record = op.evaluate(result.x, gradient=False)
        summaries.append({'start':i,'objective':record['objective'],
                          'iterations':result.nit,'evaluations':result.nfev,
                          'status':str(result.message)})
        if best is None or record['objective'] < best['objective']:
            best = record
            print(json.dumps({'start':i,'best_objective':best['objective'],
                              'dissipation':best['dissipation']}), flush=True)
            (ROOT/'HEAT_FOURIER_BEST.json').write_text(json.dumps(best,indent=2)+'\n')
        if best['dissipation'] < -1e-8:
            break
    out = {'status':'BOUNDED_COMPATIBLE_HEAT_SEARCH_NUMERICAL_ONLY',
           'finite_difference_gradient_error':error,
           'cutoff':2,'grid':20,'degree4_aliasing':'grid>4*maximum_frequency',
           'best':best,'starts':summaries,'seconds':time.monotonic()-start,
           'scope':'A negative acquisition requires exact rational Fourier replay; a positive bounded search does not establish heat monotonicity or QC.'}
    (ROOT/'HEAT_FOURIER_SEARCH.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['best','starts']},indent=2))


if __name__ == '__main__':
    main()

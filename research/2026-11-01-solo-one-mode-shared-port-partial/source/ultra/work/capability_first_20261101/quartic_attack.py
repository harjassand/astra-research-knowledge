"""HISTORICAL REPLAY: actual periodic gradients for the planar ADM quartic.

SOURCE CORRECTION: Bruno--Pasqualotto arXiv:2608.06367v1 Theorem 1 covers
this entire rank-one-convex parameter range. No further negative searches here
are warranted; the implementation is retained for reproducibility and transfer.

Only floating-point search. Quadrature is exact in exact arithmetic for the
bandlimited quartic: n > 4*k. Negative output would require exact verification.
No non-gradient relaxation or sampled rank-one-convexity test is used.
"""
import argparse
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import minimize


J = np.array([[0., 0., 0., 1.], [0., 0., -1., 0.],
              [0., -1., 0., 0.], [1., 0., 0., 0.]])


def value_gradient(a, gamma):
    s = np.sum(a*a, axis=-1)
    co = a @ J
    det = np.sum(a*co, axis=-1)/2
    f = s*s-2*gamma*s*det
    df = 4*(s-gamma*det)[..., None]*a-2*gamma*s[..., None]*co
    return f, df


def optimal_mean(g, gamma):
    v = g.reshape(-1, 4)
    s = np.sum(v*v, axis=1)
    co = v @ J
    det = np.sum(v*co, axis=1)/2
    cov = v.T @ v / len(v)
    sbar = np.trace(cov)
    b = np.mean(4*s[:, None]*v - 2*gamma*(s[:, None]*co+2*det[:, None]*v), axis=0)
    B = 2*sbar*np.eye(4)+4*cov-2*gamma*(cov@J+J@cov)-gamma*sbar*J
    ev, evec = np.linalg.eigh(B)
    cutoff = max(1e-13, np.max(ev)*1e-12)
    ib = evec.T @ b
    m = -evec @ np.where(ev>cutoff, ib/np.maximum(ev, cutoff), 0.)/2
    f0 = np.mean(s*s-2*gamma*s*det)
    return m, f0+np.dot(b, m)+m@B@m, ev, b, B


class Field:
    def __init__(self, k, gamma):
        self.k = k
        self.n = 4*k+1
        self.gamma = gamma
        freq = np.fft.fftfreq(self.n)*self.n
        fx, fy = np.meshgrid(freq, freq, indexing='ij')
        mask = (np.abs(fx)<=k)&(np.abs(fy)<=k)
        self.dx = 1j*fx*mask
        self.dy = 1j*fy*mask

    def gradient(self, u):
        uf = np.fft.fft2(u.reshape(2, self.n, self.n), axes=(-2, -1))
        gx = np.fft.ifft2(uf*self.dx, axes=(-2, -1)).real
        gy = np.fft.ifft2(uf*self.dy, axes=(-2, -1)).real
        return np.stack([gx[0], gy[0], gx[1], gy[1]], axis=-1)

    def adjoint(self, dg):
        fx = np.fft.fft2(np.stack([dg[..., 0], dg[..., 2]]), axes=(-2, -1))
        fy = np.fft.fft2(np.stack([dg[..., 1], dg[..., 3]]), axes=(-2, -1))
        return np.fft.ifft2(-self.dx*fx-self.dy*fy, axes=(-2, -1)).real.ravel()

    def objective(self, u):
        g = self.gradient(u)
        s = np.mean(np.sum(g*g, axis=-1))
        m, energy, *_ = optimal_mean(g, self.gamma)
        _, df = value_gradient(g+m, self.gamma)
        # Envelope theorem; mean(g)=0 for every admissible variation.
        dg = df/s**2-4*energy*g/s**3
        return energy/s**2, self.adjoint(dg)/(self.n*self.n)


def checks():
    rng = np.random.default_rng(916)
    field = Field(2, 2/np.sqrt(3))
    u = rng.normal(size=2*field.n*field.n)
    g = field.gradient(u)
    m, energy, ev, _, _ = optimal_mean(g, field.gamma)
    f, _ = value_gradient(g+m, field.gamma)
    fm, _ = value_gradient(m, field.gamma)
    direct = np.mean(f)-float(fm)
    err = abs(direct-energy)
    direction = rng.normal(size=u.size)
    direction /= np.linalg.norm(direction)
    val, grad = field.objective(u)
    eps = 1e-5
    fd = (field.objective(u+eps*direction)[0]-field.objective(u-eps*direction)[0])/(2*eps)
    gradient_error = abs(fd-grad@direction)
    assert err < 1e-8
    assert gradient_error < 1e-7
    # A rank-one compatible single wave cannot give negative Jensen gap.
    x = np.arange(field.n)*2*np.pi/field.n
    uu = np.zeros((2, field.n, field.n))
    uu[0] = np.sin(x[:, None])
    single = field.objective(uu.ravel())[0]
    assert single > 0
    # Deliberately NON-rank-one-convex control. An actual single gradient
    # wave at this mean has the exact negative Jensen gap -117/3200.
    gg = field.gradient(uu.ravel())/2
    mm = np.array([1., 0., 0., 9/5])
    ff, _ = value_gradient(gg+mm, 6/5)
    fm, _ = value_gradient(mm, 6/5)
    negative_control = float(np.mean(ff)-fm)
    assert abs(negative_control+117/3200) < 1e-12
    return dict(expansion_error=err, gradient_error=gradient_error,
                covariance_min_eigenvalue=float(ev[0]), single_wave_gap=float(single),
                non_roc_negative_control=negative_control)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--k', type=int, default=3)
    ap.add_argument('--starts', type=int, default=8)
    ap.add_argument('--iterations', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=92011)
    ap.add_argument('--gamma', type=float, default=2/np.sqrt(3))
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    if not 0 <= args.gamma <= 2/np.sqrt(3):
        ap.error('This mean-minimization search requires 0 <= gamma <= 2/sqrt(3).')
    check = checks()
    rng = np.random.default_rng(args.seed)
    field = Field(args.k, args.gamma)
    rows = []
    best = float('inf')
    args.out.mkdir(parents=True, exist_ok=True)
    start_time = time.monotonic()
    for i in range(args.starts):
        u = rng.normal(size=2*field.n*field.n)
        # Initial gradients are normalized; the objective is scale invariant.
        u /= np.sqrt(np.mean(np.sum(field.gradient(u)**2, axis=-1)))
        result = minimize(field.objective, u, jac=True, method='L-BFGS-B',
                          options={'maxiter': args.iterations, 'ftol': 1e-13,
                                   'gtol': 1e-8, 'maxls': 40, 'maxcor': 20})
        g = field.gradient(result.x)
        norm = np.sqrt(np.mean(np.sum(g*g, axis=-1)))
        g /= norm
        m, energy, ev, _, _ = optimal_mean(g, args.gamma)
        row = dict(start=i, gap=float(energy), iterations=int(result.nit),
                   evaluations=int(result.nfev), converged=bool(result.success),
                   status=str(result.message), mean=m.tolist(),
                   covariance_background_eigenvalues=ev.tolist(),
                   gradient_norm=float(np.linalg.norm(result.jac)),
                   seconds=time.monotonic()-start_time)
        rows.append(row)
        print(json.dumps(row), flush=True)
        if energy < best:
            best = float(energy)
            np.savez(args.out/'best_field.npz', u=result.x.reshape(2, field.n, field.n)/norm,
                     mean=m, k=args.k, gamma=args.gamma, gap=energy)
        (args.out/'search.json').write_text(json.dumps(dict(
            k=args.k, grid=field.n, gamma=args.gamma, seed=args.seed,
            quadrature='uniform torus; n=4k+1; exact for quartic in exact arithmetic',
            checks=check, rows=rows, best_gap=best), indent=2)+'\n')


if __name__ == '__main__':
    main()

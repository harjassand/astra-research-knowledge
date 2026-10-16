"""Bounded, reproducible asynchronous parity-product diagnostics.

No numerical result from this script is a proof. Seed-factorized and broad
cross-parity families are kept separate. Uses only already installed NumPy/SciPy.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

BASE = Path(__file__).resolve().parent
I2 = np.eye(2)
X = np.array([[0, 1], [1, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
P = [np.diag([1, 0]), np.diag([0, 1])]


def herm(v, d):
    out = np.zeros((d, d), complex)
    out[np.diag_indices(d)] = v[:d]
    k = d
    for i in range(d):
        for j in range(i + 1, d):
            out[i, j] = v[k] + 1j * v[k + 1]
            out[j, i] = out[i, j].conjugate()
            k += 2
    return out


def normalize(h):
    n = np.max(np.abs(np.linalg.eigvalsh(h)))
    return h / max(1., n)


def matrices(v, d, kind):
    """Return H0 and legal V1,V2 with each V norm at most one."""
    if kind == "seed":
        h0, a1, a2 = [herm(a, d) for a in v.reshape(3, d*d)]
        return (np.kron(np.eye(4), h0),
                np.kron(np.kron(X, I2), normalize(a1)),
                np.kron(np.kron(I2, X), normalize(a2)))
    # Sector basis is 00,01,10,11, followed by bath index.
    # Each edge block is an arbitrary rectangular complex bath operator.
    n0 = 4*d*d
    h0 = np.zeros((4*d, 4*d), complex)
    for s in range(4):
        h0[s*d:(s+1)*d, s*d:(s+1)*d] = herm(v[s*d*d:(s+1)*d*d], d)
    edges = v[n0:].reshape(4, 2, d, d)
    couplings = [edges[k, 0] + 1j*edges[k, 1] for k in range(4)]
    vs = []
    for pairs, bs in [([(0, 2), (1, 3)], couplings[:2]),
                      ([(0, 1), (2, 3)], couplings[2:])]:
        vv = np.zeros_like(h0)
        for (s, t), b in zip(pairs, bs):
            bb = b/max(1., np.linalg.norm(b, 2))
            vv[s*d:(s+1)*d, t*d:(t+1)*d] = bb
            vv[t*d:(t+1)*d, s*d:(s+1)*d] = bb.conj().T
        vs.append(vv)
    return h0, *vs


def evaluate(v, d, kind, actions, return_detail=False, split_free=False):
    # A three-segment schedule: pinch 1 after segment 0, pinch 2 after segment 1.
    npseg = 3*d*d if kind == "seed" else 12*d*d
    nseg=len(actions)
    slices=nseg//3
    rows = v.reshape(nseg, npseg)
    z1 = np.kron(np.kron(Z, I2), np.eye(d))
    z2 = np.kron(np.kron(I2, Z), np.eye(d))
    # Backpropagate terminal 11 effect, applying exact own complete pinches.
    effect = np.kron(np.kron(P[1], P[1]), np.eye(d)).astype(complex)
    residual = 0.
    for k in reversed(range(nseg)):
        h0, a1, a2 = matrices(rows[k], d, kind)
        h = (0 if split_free else h0) + actions[k][0]*a1 + actions[k][1]*a2
        eig, basis = np.linalg.eigh(h)
        u = (basis*np.exp(-1j*eig))@basis.conj().T
        if split_free:
            eig0,basis0=np.linalg.eigh(h0)
            u0=(basis0*np.exp(-1j*eig0))@basis0.conj().T
            u=u0@u
        effect = u.conj().T @ effect @ u
        if k == 2*slices:
            effect = (effect + z2 @ effect @ z2)/2
        elif k == slices:
            effect = (effect + z1 @ effect @ z1)/2
        if return_detail:
            residual = max(residual, np.linalg.norm(h0@z1-z1@h0),
                           np.linalg.norm(h0@z2-z2@h0),
                           np.linalg.norm(a1@z1+z1@a1),
                           np.linalg.norm(a2@z2+z2@a2),
                           np.linalg.norm(a1@z2-z2@a1),
                           np.linalg.norm(a2@z1-z1@a2),
                           max(0.,np.linalg.norm(a1,2)-1),
                           max(0.,np.linalg.norm(a2,2)-1))
    ev, vec = np.linalg.eigh(effect[:d,:d])
    acts = np.asarray(actions)
    own = [[acts[:slices,0].sum(), acts[slices:,0].sum()],
           [acts[:2*slices,1].sum(), acts[2*slices:,1].sum()]]
    qs = [1-np.prod(np.cos(np.minimum(a, np.pi/2))**2) for a in own]
    ratio = float(ev[-1]/np.prod(qs))
    if return_detail:
        return dict(probability=float(ev[-1]), product_Q=float(np.prod(qs)),
                    Q=qs, ratio=ratio, own_gap_actions=own,
                    hypothesis_residual=float(residual),
                    initial_bath_real=vec[:,-1].real.tolist(),
                    initial_bath_imag=vec[:,-1].imag.tolist())
    return ratio


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--kind', choices=['seed','broad'], default='broad')
    ap.add_argument('--d', type=int, default=1)
    ap.add_argument('--starts', type=int, default=8)
    ap.add_argument('--maxiter', type=int, default=120)
    ap.add_argument('--action', type=float, default=.4)
    ap.add_argument('--rng', type=int, default=20261016)
    ap.add_argument('--slices', type=int, default=1)
    ap.add_argument('--split-free', action='store_true')
    args=ap.parse_args()
    rng=np.random.default_rng(args.rng)
    actions=np.full((3*args.slices,2),args.action/args.slices).tolist()
    n=(3 if args.kind=='seed' else 12)*args.d*args.d*3*args.slices
    outcomes=[]
    best=-np.inf
    start=time.time()
    for k in range(args.starts):
        v=rng.normal(0,.55,size=n)
        opt=minimize(lambda p:-evaluate(p,args.d,args.kind,actions,split_free=args.split_free),v,
                     method='L-BFGS-B', bounds=[(-4,4)]*n,
                     options=dict(maxiter=args.maxiter,ftol=1e-12,gtol=2e-7,maxls=15))
        result=evaluate(opt.x,args.d,args.kind,actions,True,split_free=args.split_free)
        result.update(start=k,nit=int(opt.nit),nfev=int(opt.nfev),
                      success=bool(opt.success),message=str(opt.message))
        outcomes.append(result)
        if result['ratio']>best:
            best=result['ratio']
            np.save(BASE/f'candidate_{args.kind}_d{args.d}_a{args.action}_s{args.slices}_f{int(args.split_free)}.npy',opt.x)
        print(json.dumps(result),flush=True)
    report=dict(args=vars(args),family='independent arbitrary piecewise constant legal parity Hamiltonians',
                actions=actions,elapsed_seconds=time.time()-start,results=outcomes,
                epistemic_status='finite floating-point diagnostics only; no proof or exact counterexample')
    (BASE/f'search_{args.kind}_d{args.d}_a{args.action}_s{args.slices}_f{int(args.split_free)}.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    main()

"""Matrix-free diagnostic of the exact bath-channel singular gap.

This is a finite-dimensional spectral calculation, not a proof of a gap
profile or a simulation of a receiver.  Pauli coefficients use normalized
Hilbert--Schmidt inner product.  The JSON path is an explicit CLI argument.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

P = [np.eye(2, dtype=complex), np.array([[0, 1], [1, 0]], complex),
     np.array([[0, -1j], [1j, 0]], complex), np.diag([1, -1]).astype(complex)]
W = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])


def local_transfer(theta):
    u = np.cos(theta)*np.eye(4)+1j*np.sin(theta)*W
    pp = [np.kron(a,b) for a in P for b in P]
    return np.array([[np.trace(a@u@b@u.conj().T).real/4
                      for b in pp] for a in pp])


def channel(n, theta):
    g = local_transfer(theta)
    shape = (4,)*(n+1)
    def step(x, j, inverse=False):
        order = [0, j]+[k for k in range(1, n+1) if k != j]
        inv = np.argsort(order)
        z = x.transpose(order).reshape(16,-1)
        z = (g.T if inverse else g)@z
        return z.reshape(shape).transpose(inv)
    def apply(v, inverse=False):
        x = np.zeros((4,4**n), dtype=float)
        x[0] = v
        x = x.reshape(shape)
        for j in (range(n,0,-1) if inverse else range(1,n+1)):
            x = step(x,j,inverse)
        return x.reshape(4,-1)[0].copy()
    return apply


def probe(n, theta, tol, maxiter):
    t = channel(n,theta)
    dim = 4**n
    count = [0]
    def mv(v):
        count[0] += 1
        z = t(t(v),True)
        # Remove the exact identity eigenvector without numerical ambiguity.
        z[0] = 0
        return z
    a = LinearOperator((dim,dim),matvec=mv,dtype=float)
    rng = np.random.default_rng(142+n)
    v0 = rng.normal(size=dim); v0[0]=0
    vals,vecs = eigsh(a,k=1,which='LA',tol=tol,maxiter=maxiter,v0=v0)
    v = vecs[:,0]
    # Compute loss from the final source-traceless block only indirectly here;
    # use the Rayleigh residual to report achieved numerical convergence.
    av = mv(v)
    lam = float(v@av)
    return {'n':n,'theta':theta,'singular_squared':lam,
            'commutator_gap':(8/3)*(1-lam),
            'eigen_residual':float(np.linalg.norm(av-lam*v)),
            'matvecs':count[0], 'r_to_n':float((1-np.sin(theta)**4)**n)}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--theta',type=float,required=True)
    ap.add_argument('--lengths',type=int,nargs='+',required=True)
    ap.add_argument('--tol',type=float,default=1e-11)
    ap.add_argument('--maxiter',type=int,default=10000)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    rows=[]
    for n in args.lengths:
        row=probe(n,args.theta,args.tol,args.maxiter)
        rows.append(row); print(json.dumps(row),flush=True)
        args.output.write_text(json.dumps(rows,indent=2)+'\n')

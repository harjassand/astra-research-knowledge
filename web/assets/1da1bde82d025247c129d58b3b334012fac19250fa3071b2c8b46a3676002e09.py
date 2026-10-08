"""Exploratory rank-constrained Werner forms. No numerical result is a proof."""
from __future__ import annotations
import itertools
import numpy as np
from numpy.typing import NDArray


def partial_trace(c: NDArray, dims: tuple[int, ...], sites: tuple[int, ...]) -> NDArray:
    if c.shape != (np.prod(dims), np.prod(dims)):
        raise ValueError('Matrix shape disagrees with subsystem dimensions')
    a = c.reshape(dims + dims)
    remaining = list(dims)
    for i in sorted(sites, reverse=True):
        a = np.trace(a, axis1=i, axis2=i + len(remaining))
        del remaining[i]
    size = int(np.prod(remaining))
    return a.reshape(size, size)


def werner_form(c: NDArray, dims: tuple[int, ...], alpha: float = -0.5) -> float:
    out = 0.0
    for mask in range(1 << len(dims)):
        sites = tuple(i for i in range(len(dims)) if (mask >> i) & 1)
        t = partial_trace(c, dims, sites)
        out += alpha ** len(sites) * np.vdot(t, t).real
    return float(out)


def form_operator(c: NDArray, dims: tuple[int, ...], alpha: float = -0.5) -> NDArray:
    """Apply the HS-self-adjoint superoperator tensor_i (id + alpha D_i)."""
    n = len(dims)
    a = c.reshape(dims + dims).copy()
    # Each D_i takes a partial trace and inserts the identity in that subsystem.
    for i, d in enumerate(dims):
        t = np.trace(a, axis1=i, axis2=n+i)
        t = np.expand_dims(t, axis=(i, n+i))
        shape = [1] * (2*n)
        shape[i] = shape[n+i] = d
        a = a + alpha * t * np.eye(d).reshape(shape)
    return a.reshape(c.shape)


def restricted_matrix(u: NDArray, dims: tuple[int, ...]) -> NDArray:
    """Quadratic form for C=U W, where U has orthonormal columns."""
    N, r = u.shape
    h = np.empty((r*N, r*N), dtype=complex)
    for k in range(r*N):
        w = np.zeros((r,N),dtype=complex)
        w.flat[k]=1
        h[:,k] = (u.conj().T @ form_operator(u@w, dims)).ravel()
    if np.linalg.norm(h-h.conj().T)>1e-8:
        raise ArithmeticError('Restricted form failed Hermiticity check')
    return (h+h.conj().T)/2


def seesaw(dims: tuple[int, ...], seed: int, rounds: int = 30) -> tuple[float, NDArray]:
    rng = np.random.default_rng(seed)
    N = int(np.prod(dims))
    u, _ = np.linalg.qr(rng.normal(size=(N,2)) + 1j*rng.normal(size=(N,2)))
    c = np.zeros((N,N),dtype=complex)
    previous = float('inf')
    for step in range(rounds):
        h=restricted_matrix(u,dims)
        vals,vecs=np.linalg.eigh(h)
        w=vecs[:,0].reshape(2,N)
        c=u@w
        value=werner_form(c,dims)
        if value>previous+1e-8:
            raise ArithmeticError('Seesaw monotonicity check failed')
        if abs(value-previous)<1e-12:
            break
        previous=value
        # Adjoints leave the form invariant; replace the row space by the range.
        u,_=np.linalg.qr(w.conj().T)
    return value,c

if __name__=='__main__':
    rng=np.random.default_rng(904)
    for dims in [(2,), (3,3), (3,3,3)]:
        N=int(np.prod(dims))
        c=rng.normal(size=(N,N))+1j*rng.normal(size=(N,N))
        assert np.allclose(werner_form(c,dims),np.vdot(c,form_operator(c,dims)).real)
    for seed in range(8):
        v,c=seesaw((3,3,3),seed,rounds=35)
        print('seed',seed,'q3',v,'rank',np.linalg.matrix_rank(c,tol=1e-8),flush=True)
    # Save beside this script so the exploratory replay is portable.
    from pathlib import Path
    np.save(Path(__file__).with_name('last_probe_matrix.npy'), c)

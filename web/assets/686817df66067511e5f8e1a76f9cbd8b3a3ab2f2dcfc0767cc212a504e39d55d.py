"""Floating-point prototype of Lim's centered Gaussian reset sampler.

The new research result concerns its IDEAL real-arithmetic distribution.
This implementation has no certified total-variation rounding-error bound.
It does not evaluate hafnians, postselect records, or impose a photon cutoff.
A resource guard raises an exception instead of returning a truncated record.
"""
from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatMatrix = NDArray[np.float64]

def covariance_from_network(transfer: ArrayLike, squeezings: ArrayLike) -> FloatMatrix:
    """Return K = covariance - I/2 for a supplied passive vacuum-loss map.

    transfer has shape (output_modes, squeezed_input_modes). Entries may be
    complex; singular values must not exceed one. Squeezings are nonnegative
    real magnitudes, one per input. Their phases can be absorbed into transfer.
    """
    t = np.asarray(transfer, dtype=np.complex128)
    r = np.asarray(squeezings, dtype=np.float64)
    if t.ndim != 2 or min(t.shape) < 1 or r.shape != (t.shape[1],):
        raise ValueError('Expected an M-by-N transfer and N squeezing magnitudes.')
    if not np.all(np.isfinite(t)) or not np.all(np.isfinite(r)) or np.any(r < 0):
        raise ValueError('Inputs must be finite and squeezing magnitudes nonnegative.')
    if np.linalg.svd(t, compute_uv=False)[0] > 1 + 1e-12:
        raise ValueError('Transfer is not a contraction.')
    with np.errstate(over='raise', invalid='raise'):
        ns = np.sinh(r)**2
        ms = np.sinh(r)*np.cosh(r)
    l = np.block([[t.real,-t.imag],[t.imag,t.real]])
    k = (l*np.concatenate([ns+ms,ns-ms]))@l.T
    return np.asarray((k+k.T)/2, dtype=np.float64)

def spectral_cubic(transfer: ArrayLike) -> float:
    """Sum of cubed power transmissions, equivalently sum of singular values^6."""
    t = np.asarray(transfer, dtype=np.complex128)
    if t.ndim != 2 or not np.all(np.isfinite(t)):
        raise ValueError('Expected a finite two-dimensional matrix.')
    return float(np.sum(np.linalg.svd(t,compute_uv=False)**6))

def sample_centered_covariance(
    k0: ArrayLike,
    rng: np.random.Generator,
    *,
    inversion_steps: int = 64,
    max_events: int = 100000,
    check_physical: bool = True,
) -> NDArray[np.int64]:
    """Sample one approximate photon-count vector using dense covariance updates.

    Quadratures are ordered q_1,...,q_M,p_1,...,p_M. A tiny negative rate
    (at most 1e-11 times matrix norm) is clipped as a numerical expedient.
    No claim of a certified numerical TV error is made for this expedient,
    the eigendecomposition, finite bisection, or floating-point randomness.
    """
    k = np.asarray(k0,dtype=np.float64).copy()
    if k.ndim != 2 or k.shape[0] != k.shape[1] or k.shape[0]%2 or not k.size:
        raise ValueError('K must be a nonempty real 2M-by-2M matrix.')
    if not np.all(np.isfinite(k)) or not np.allclose(k,k.T,rtol=0,atol=1e-11):
        raise ValueError('K must be finite and symmetric.')
    if inversion_steps < 16 or max_events < 1:
        raise ValueError('Use at least 16 inversion steps and a positive resource guard.')
    modes=k.shape[0]//2
    if check_physical:
        j=np.block([[np.zeros((modes,modes)),-np.eye(modes)],
                    [np.eye(modes),np.zeros((modes,modes))]])
        h=k+np.eye(2*modes)/2+0.5j*j
        if np.linalg.eigvalsh(h)[0] < -1e-10:
            raise ValueError('Covariance fails the uncertainty relation numerically.')
    counts=np.zeros(modes,dtype=np.int64)
    for _ in range(max_events):
        ev,vec=np.linalg.eigh((k+k.T)/2)
        if ev[0] <= -1:
            raise FloatingPointError('No-click determinant has left its domain.')
        log_p0=-0.5*float(np.log1p(ev).sum())
        if log_p0 > 1e-10:
            raise FloatingPointError('Unphysical vacuum probability.')
        p0=float(np.exp(min(log_p0,0.)))
        uniform=float(rng.random())
        if uniform <= p0:
            return counts
        target_log=float(np.log(uniform))
        low,high=0.,1.
        for _ in range(inversion_steps):
            v=(low+high)/2
            log_survival=-0.5*float(np.log1p((1-v)*ev).sum())
            if log_survival < target_log:
                low=v
            else:
                high=v
        v=(low+high)/2
        flowed=v*ev/(1+(1-v)*ev)
        k=(vec*flowed)@vec.T
        rates=0.5*(np.diag(k)[:modes]+np.diag(k)[modes:])
        tolerance=1e-11*max(1.,float(np.max(np.abs(flowed))))
        if float(np.min(rates)) < -tolerance:
            raise FloatingPointError('Negative detection rate beyond rounding tolerance.')
        rates=np.maximum(rates,0)
        total=float(rates.sum())
        if not total>0:
            raise FloatingPointError('A nonterminal event has numerically zero rate.')
        chosen=int(rng.choice(modes,p=rates/total))
        cols=k[:,[chosen,chosen+modes]]
        k=k+(cols@cols.T)/rates[chosen]
        k=(k+k.T)/2
        counts[chosen]+=1
    raise RuntimeError('Resource guard reached; no truncated sample was returned.')

if __name__ == '__main__':
    random=np.random.default_rng(20261007)
    transfer=np.diag(np.sqrt([.04,.01])).astype(complex)
    covariance=covariance_from_network(transfer,[np.log(2),np.log(3)])
    print({'S3':spectral_cubic(transfer),
           'sample':sample_centered_covariance(covariance,random).tolist()})

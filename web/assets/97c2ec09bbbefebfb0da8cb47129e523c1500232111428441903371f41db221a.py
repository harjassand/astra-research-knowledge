"""Floating-point diagnostics, not proof or formal certification.

Checks the reference-correction channel, canonical-likelihood estimate,
and exact finite averaging over shifted logarithmic pinching partitions.
Run: python check_lemmas.py
Requires NumPy only. Random seed is fixed for reproducibility.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

RNG = np.random.default_rng(20261009)


def herm(a: np.ndarray) -> np.ndarray:
    return (a + a.conj().T) / 2


def power(a: np.ndarray, p: float) -> np.ndarray:
    w, v = np.linalg.eigh(herm(a))
    if p < 0 and w.min() <= 0:
        raise ValueError('An inverse requires a positive definite matrix.')
    w = np.maximum(w, 0)
    return (v * (w**p)) @ v.conj().T


def pos(a: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eigh(herm(a))
    return (v * np.maximum(w, 0)) @ v.conj().T


def norm1(a: np.ndarray) -> float:
    return float(np.linalg.svd(a, compute_uv=False).sum())


def norm2sq(a: np.ndarray) -> float:
    return float(np.vdot(a, a).real)


def state(d: int, rank: int | None = None) -> np.ndarray:
    rank = d if rank is None else rank
    z = RNG.standard_normal((d, rank)) + 1j*RNG.standard_normal((d, rank))
    a = z @ z.conj().T
    return a / np.trace(a).real


def unitary(d: int) -> np.ndarray:
    z = RNG.standard_normal((d, d)) + 1j*RNG.standard_normal((d, d))
    q, _ = np.linalg.qr(z)
    return q


def correction(nu: np.ndarray, omega: np.ndarray):
    d = len(nu)
    delta = norm1(nu-omega)/2
    if delta < 1e-13:
        return lambda z: z.copy(), delta
    c = nu + pos(omega - nu)
    a = power(omega, .5) @ power(c, -.5)
    defect = herm(np.eye(d) - a.conj().T @ a)
    residual = herm(omega - a @ nu @ a.conj().T)
    p = np.trace(residual).real
    if p < -1e-9:
        raise AssertionError('Negative replacement mass.')
    replacement = residual/p if p > 1e-12 else omega
    def r(z: np.ndarray) -> np.ndarray:
        return a @ z @ a.conj().T + np.trace(defect @ z)*replacement
    return r, delta


def choi(fn, d: int) -> np.ndarray:
    out = np.zeros((d*d, d*d), dtype=complex)
    for i in range(d):
        for j in range(d):
            e = np.zeros((d,d), dtype=complex); e[i,j]=1
            out[i*d:(i+1)*d, j*d:(j+1)*d] = fn(e)
    return herm(out)


def shifted_pinchings(sigma: np.ndarray, width: float):
    s, u = np.linalg.eigh(herm(sigma))
    logs = np.log(s)
    breaks = sorted(set([0., width] + list(np.mod(logs, width))))
    for left, right in zip(breaks[:-1], breaks[1:]):
        if right-left < 1e-13:
            continue
        r = (left + right)/2
        bins = np.floor((logs-r)/width).astype(int)
        mask = bins[:,None] == bins[None,:]
        def pinch(z, mask=mask):
            return u @ ((u.conj().T @ z @ u)*mask) @ u.conj().T
        yield (right-left)/width, pinch


stats = {
    'seed': 20261009,
    'scope': 'Floating-point diagnostics only; not universal proof or formal certification.',
    'reference_cases': 0, 'likelihood_cases': 0, 'pinching_cases': 0,
    'reference_error_max': 0., 'choi_min_eigenvalue': 1.,
    'trace_preservation_error_max': 0., 'reference_bound_ratio_max': 0.,
    'likelihood_bound_ratio_max': 0., 'pinching_second_moment_ratio_max': 0.,
}
for d in (2, 3, 5):
    for k in range(30):
        nu = state(d, max(1, d-1) if k % 4 == 0 else d)
        omega = .08*np.eye(d)/d + .92*state(d)
        if k % 5 == 0:
            nu = (1-10**(-2-k%3))*omega + 10**(-2-k%3)*nu
        r, delta = correction(nu, omega)
        j = choi(r, d)
        stats['reference_error_max'] = max(stats['reference_error_max'], norm1(r(nu)-omega))
        stats['choi_min_eigenvalue'] = min(stats['choi_min_eigenvalue'], float(np.linalg.eigvalsh(j).min()))
        tr_out = np.einsum('iaja->ij', j.reshape(d,d,d,d))
        stats['trace_preservation_error_max'] = max(stats['trace_preservation_error_max'], norm1(tr_out-np.eye(d)))
        # theta <= K nu on nu's support, with K calculated directly.
        vals, vecs = np.linalg.eigh(herm(nu))
        support = vals > 1e-10
        v = vecs[:,support]
        theta = v @ state(int(support.sum())) @ v.conj().T
        inv = (v / np.sqrt(vals[support])) @ v.conj().T
        K = float(np.linalg.eigvalsh(herm(inv @ theta @ inv)).max())
        lhs = norm1(r(theta)-theta)/2
        rhs = np.sqrt(K*delta)+K*delta/2
        if rhs > 1e-12:
            stats['reference_bound_ratio_max'] = max(stats['reference_bound_ratio_max'], lhs/rhs)
        assert lhs <= rhs + 2e-8
        assert np.linalg.eigvalsh(j).min() > -2e-8
        stats['reference_cases'] += 1

for d in (2,3,5,8):
    for k in range(35):
        u = unitary(d)
        eig = np.exp(np.linspace(-7 if k % 2 else -2, 0, d)); eig /= eig.sum()
        sigma = (u * eig) @ u.conj().T
        rho = state(d, 1) if k % 7 == 0 else .1*sigma + .9*state(d, d-1 if k % 3 == 0 else d)
        ss = power(sigma,.5); si = power(sigma,-.5); sr = power(rho,.5)
        x = si @ power(ss @ rho @ ss, .5) @ si
        K = float(np.linalg.eigvalsh(herm(si @ rho @ si)).max())
        gap = norm1(sr @ ss) - np.trace(sr @ ss).real
        lhs = norm2sq(x @ ss - sr)
        rhs = 2*np.sqrt(K)*max(gap,0)
        if rhs > 1e-12:
            stats['likelihood_bound_ratio_max'] = max(stats['likelihood_bound_ratio_max'], lhs/rhs)
        assert norm1(x @ sigma @ x-rho) < 3e-7
        assert lhs <= rhs + 3e-7
        c = norm2sq(x @ ss - ss @ x)
        for width in (.1, .4, 1.):
            expectation = 0.
            mass = 0.
            for weight, pinch in shifted_pinchings(sigma, width):
                expectation += weight*norm2sq((x-pinch(x)) @ ss)
                mass += weight
            bound = 5*np.sqrt(c)/width
            assert abs(mass-1)<1e-9
            assert expectation <= bound + 2e-7
            if bound>1e-12:
                stats['pinching_second_moment_ratio_max'] = max(stats['pinching_second_moment_ratio_max'], expectation/bound)
            stats['pinching_cases'] += 1
        stats['likelihood_cases'] += 1

# Scalar constants used in the explicit proof.
assert 2*np.sqrt(5)+1+np.sqrt(5*np.e)+5*np.e/2 < 16
assert 2*np.sqrt(5)+8*np.sqrt(np.e) < 18
assert 16*np.sqrt(6)+1 < 41
assert 18*41**(1/16) < 24
# At L >= 65536 these scalar differences are increasing (checked analytically
# in the manuscript); these evaluations are diagnostics at the endpoint.
L = 65536.
assert np.log(.5*np.sqrt(L)) <= (127/1024-1/9)*L
# Log of [32*4^(33/32)*(1+L/9)^(1/32)*exp(-L/512)] <= log(128/sqrt(L)).
assert np.log(32)+(33/32)*np.log(4)+np.log1p(L/9)/32-L/512 <= np.log(128)-np.log(L)/2

path = Path(__file__).with_name('diagnostic_results.json')
path.write_text(json.dumps(stats, indent=2)+'\n')
print(json.dumps(stats, indent=2))

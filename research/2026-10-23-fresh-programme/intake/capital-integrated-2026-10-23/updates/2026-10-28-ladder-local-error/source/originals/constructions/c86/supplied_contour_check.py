#!/usr/local/bin/python3
"""Momentum-contour quadrature diagnostic. No finite-chain resonance claim.

Discretizes the explicit analytically deformed continuum integrals using
Gauss-Legendre quadrature. Writes only beside this script. The mathematical
existence argument is in PROOF.md and does not depend on this computation.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eig
from scipy.optimize import root
from numpy.polynomial.legendre import leggauss

OUT = Path(__file__).resolve().parent


def channel(n, c, coupling2, theta):
    x, w = leggauss(n)
    k = np.pi * (x + 1) / 2
    w = w * np.pi / 2
    phi = k - 1j * theta * np.sin(k)
    deriv = 1 - 1j * theta * np.cos(k)
    lam = c - np.cos(phi)
    v = np.sqrt(coupling2 * 2 / np.pi * w) * np.sin(phi) * np.sqrt(deriv)
    h = np.diag(np.r_[3.0, lam]).astype(complex)
    h[0, 1:] = v
    h[1:, 0] = v
    return h


def spectral(h):
    vals, vecs = eig(h)
    vecs = vecs / np.sqrt(np.sum(vecs * vecs, axis=0))[None, :]
    return vals, vecs


def sums(vals, weights, z, derivative=False):
    den = vals[:, None] + vals[None, :] - z
    return np.sum(weights[:, None] * weights[None, :] / den ** (2 if derivative else 1))


def scalar_response(n, theta, energy):
    data = []
    for c, kappa in [(5, 2 / 25), (1, 1 / 25)]:
        vals, vecs = spectral(channel(n, c, kappa, theta))
        weights = vecs[0] ** 2
        data.append((vals, weights))
    (xp, wp), (ym, wm) = data
    D = sums(xp, wp, energy, True) + sums(ym, wm, energy, True)
    up = np.sum(wp[None, :] / (xp[:, None] + xp[None, :] - energy), axis=1)
    um = np.sum(wm[None, :] / (ym[:, None] + ym[None, :] - energy), axis=1)
    den = xp[:, None] + ym[None, :] - energy
    measure = wp[:, None] * wm[None, :]
    source = up[:, None] + um[None, :]
    M = np.sum(measure / den)
    J = np.sum(measure * source / den)
    F = np.sum(measure * source ** 2 / den)
    S = (2 / D) * (F - J ** 2 / M)
    pair_residual = sums(xp, wp, energy) + sums(ym, wm, energy)
    return D, M, J, S, pair_residual


def actual_eta_pole(n, theta, eta, energy):
    hp = channel(n, 5, 2 / 25, theta)
    hm = channel(n, 1, 1 / 25, theta)
    N = 2 * (n + 1)
    h = np.zeros((N, N), complex)
    h[:n + 1, :n + 1] = hp
    h[n + 1:, n + 1:] = hm
    h[0, n + 1] = h[n + 1, 0] = eta
    vals, vecs = spectral(h)
    a, b = vecs[0], vecs[n + 1]
    qe = (a[:, None] * a[None, :] + b[:, None] * b[None, :]) / np.sqrt(2)
    qo = (a[:, None] * b[None, :] + b[:, None] * a[None, :]) / np.sqrt(2)
    pair_sums = vals[:, None] + vals[None, :]
    def schur(z):
        inv = 1 / (pair_sums - z)
        kee = np.sum(qe ** 2 * inv)
        keo = np.sum(qe * qo * inv)
        koo = np.sum(qo ** 2 * inv)
        return kee - keo ** 2 / koo
    def fun(z):
        f = schur(z[0] + 1j * z[1])
        return [f.real, f.imag]
    ans = root(fun, [energy, -np.pi * 2.1275067206e-8 * eta ** 2], tol=1e-10)
    z = complex(*ans.x)
    return dict(eta=eta, pole_real=z.real, pole_imag=z.imag,
                eta2_shift_real=((z-energy)/eta**2).real,
                eta2_shift_imag=((z-energy)/eta**2).imag,
                residual=abs(schur(z)), solver_success=bool(ans.success))


def ascomplex(z):
    return dict(real=float(np.real(z)), imag=float(np.imag(z)))

def small_fock_identity_check():
    """Direct bosonic Fock compression versus its two-forbidden-state inverse."""
    n, theta, eta = 5, .25, .07
    hp, hm = channel(n, 5, 2/25, theta), channel(n, 1, 1/25, theta)
    N = 2 * (n + 1)
    h = np.zeros((N, N), complex)
    h[:n+1, :n+1], h[n+1:, n+1:] = hp, hm
    h[0, n+1] = h[n+1, 0] = eta
    basis = [(i, j) for i in range(N) for j in range(i, N)]
    index = {state: a for a, state in enumerate(basis)}
    A = np.zeros((len(basis), len(basis)), complex)
    V = np.zeros_like(A)
    for col, state in enumerate(basis):
        occ = np.bincount(state, minlength=N)
        for j in np.flatnonzero(occ):
            for i in np.flatnonzero(h[:, j]):
                moved = occ.copy()
                amplitude = np.sqrt(moved[j])
                moved[j] -= 1
                amplitude *= np.sqrt(moved[i] + 1)
                moved[i] += 1
                out = tuple(np.repeat(np.arange(N), moved))
                row = index[out]
                A[row, col] += h[i, j] * amplitude
                if {i, j} == {0, n+1}:
                    V[row, col] += amplitude
    pp, mm, pm = index[(0, 0)], index[(n+1, n+1)], index[(0, n+1)]
    W = np.zeros((len(basis), 2))
    W[pp, 0] = W[mm, 0] = 1 / np.sqrt(2)
    W[pm, 1] = 1
    p = np.zeros(len(basis))
    p[pp], p[mm] = 1/np.sqrt(2), -1/np.sqrt(2)
    kept = [a for a in range(len(basis)) if a not in [pp, mm, pm]]
    T = np.column_stack([p, np.eye(len(basis))[:, kept]])
    # Explicit contractions avoid a local BLAS matmul floating-point-status
    # warning observed even for these bounded, entirely finite inputs.
    mmul = lambda a, b: np.einsum('ik,kj->ij', a, b, optimize=False)
    assert np.all(np.isfinite(A)) and np.max(np.abs(A)) < 13
    H = mmul(mmul(T.T, A), T)
    z = 5.97857931516658 + .017j
    R = np.linalg.inv(A - z * np.eye(len(basis)))
    K = mmul(mmul(W.T, R), W)
    subtracted = R - mmul(mmul(R, W), np.linalg.solve(K, mmul(W.T, R)))
    compressed = mmul(mmul(T.T, subtracted), T)
    direct = np.linalg.inv(H - z * np.eye(H.shape[0]))
    assert np.all(np.isfinite(direct)) and np.all(np.isfinite(compressed))
    return dict(nodes_per_band=n, eta=eta,
                forbidden_overlap_norm=float(np.linalg.norm(mmul(W.T, T))),
                full_inverse_max_error=float(np.max(np.abs(direct-compressed))),
                physical_V_norm=float(np.linalg.norm(mmul(mmul(T.T, V), T), 2)),
                symmetry_error=float(np.max(np.abs(H-H.T))))


energy = 5.97857931516658
checks = []
for n, theta in [(48, .25), (96, .25), (160, .25), (160, .4)]:
    D, M, J, S, residual = scalar_response(n, theta, energy)
    checks.append(dict(nodes_per_band=n, theta=theta, D=ascomplex(D),
                       M=ascomplex(M), J=ascomplex(J), S=ascomplex(S),
                       rho_from_continuation=float(S.imag/np.pi),
                       pair_root_residual=ascomplex(residual)))
poles = [actual_eta_pole(128, .25, eta, energy) for eta in [.04, .02, .01]]
result = dict(scope='Uncertified contour quadrature; not an existence proof.',
              fixed_energy=energy, continuation_checks=checks, actual_eta_poles=poles,
              direct_fock_identity=small_fock_identity_check())
(OUT / 'contour_check_results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))

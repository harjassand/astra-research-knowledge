#!/usr/bin/env python3
"""Independent small quadrature Fock check; diagnostic only, not a proof.

Construct directly in L/R memory coordinates with a Kronecker symmetrizer,
then remove LL and RR. Check parity, compression, and the bilinear pole
coefficient without using the supplied scripts.
"""
import json
import os
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eig, eigh, solve

# Some local BLAS matmul builds retain floating exception flags across calls.
# Suppress warnings only; independently reject any nonfinite calculation below.
np.seterr(all='ignore')
NODES = int(os.environ.get('REVIEW_NODES', '10'))
THETA = float(os.environ.get('REVIEW_THETA', '0.25'))
zstar = 5.978579315166578 + 0.17j
q, w = leggauss(NODES)
k = np.pi * (q + 1) / 2
w = np.pi * w / 2
phi = k - 1j * THETA * np.sin(k)
jac = 1 - 1j * THETA * np.cos(k)
d = 2 + 2 * NODES
h0 = np.zeros((d, d), dtype=complex)
h0[0, 0] = h0[1, 1] = 3
for center, strength, begin, parity in [(5, 2/25, 2, 1),
                                        (1, 1/25, 2 + NODES, -1)]:
    ix = np.arange(begin, begin + NODES)
    h0[ix, ix] = center - np.cos(phi)
    vec = np.sqrt(strength / np.pi * w) * np.sin(phi) * np.sqrt(jac)
    h0[0, ix] = h0[ix, 0] = vec
    h0[1, ix] = h0[ix, 1] = parity * vec
v1 = np.zeros_like(h0)
v1[0, 0], v1[1, 1] = 1, -1

labels = [(i, j) for i in range(d) for j in range(i, d)]
sym = np.zeros((d*d, len(labels)))
for col, (i, j) in enumerate(labels):
    if i == j:
        sym[i*d+j, col] = 1
    else:
        sym[i*d+j, col] = sym[j*d+i, col] = 1 / np.sqrt(2)
ident = np.eye(d)
def second(a):
    return sym.T @ (np.kron(a, ident) + np.kron(ident, a)) @ sym

A0, Vfull = second(h0), second(v1)
forbidden = [labels.index((0, 0)), labels.index((1, 1))]
allowed = [i for i in range(len(labels)) if i not in forbidden]
W = np.eye(len(labels))[:, forbidden]
T = np.eye(len(labels))[:, allowed]
H0, V = T.T @ A0 @ T, T.T @ Vfull @ T
assert all(np.isfinite(x).all() for x in (h0, A0, Vfull, H0, V))

s1 = np.eye(d)
s1[:2, :2] = [[0, 1], [1, 0]]
s1[2+NODES:, 2+NODES:] *= -1
S = T.T @ sym.T @ np.kron(s1, s1) @ sym @ T
parity, U = eigh(S)
Pe, Po = U[:, parity > 0], U[:, parity < 0]
He, Ho = Pe.T @ H0 @ Pe, Po.T @ H0 @ Po
ev, Evec = eig(He)
idx = np.argmin(abs(ev - 5.978579315166578))
E0 = ev[idx]
psi = Evec[:, idx]
psi /= np.sqrt(psi.T @ psi)
f = Po.T @ V @ Pe @ psi
response = solve(Ho - E0*np.eye(Ho.shape[0]), f)
coefficient = -f.T @ response
wrong_coefficient = -np.vdot(f, response) / np.vdot(psi, psi)
def near_eigenvalue(eta):
    vals = eig(H0 + eta * V, left=False, right=False)
    return vals[np.argmin(abs(vals-E0))]

eta = 0.02
ep, em = near_eigenvalue(eta), near_eigenvalue(-eta)
RA = np.linalg.inv(A0 + eta * Vfull - zstar*np.eye(A0.shape[0]))
K = W.T @ RA @ W
schur = T.T @ (RA - RA @ W @ solve(K, W.T @ RA)) @ T
direct = np.linalg.inv(H0 + eta*V - zstar*np.eye(H0.shape[0]))
assert all(np.isfinite(x).all() for x in (ev, psi, f, response, RA, K, schur, direct))
assert np.max(np.abs(A0)) < 20 and np.max(np.abs(H0)) < 20
fmt = lambda z: {'real': float(np.real(z)), 'imag': float(np.imag(z))}
out = {
  'scope': 'finite quadrature diagnostic, not an infinite-volume pole proof',
  'nodes_per_bath': NODES, 'theta': THETA, 'eta': eta,
  'deformed_complex_symmetry_error': float(np.linalg.norm(H0-H0.T)),
  'physical_v_norm': float(np.linalg.norm(V, 2)),
  'parity_conjugation_error': float(np.linalg.norm(S@(H0+eta*V)@S-(H0-eta*V))),
  'schur_full_inverse_max_error': float(np.max(np.abs(schur-direct))),
  'reference_even_eigenvalue': fmt(E0),
  'eta_plus_eigenvalue': fmt(ep), 'eta_minus_eigenvalue': fmt(em),
  'evenness_error': float(abs(ep-em)),
  'bilinear_quadratic_coefficient': fmt(coefficient),
  'hermitian_pairing_coefficient_for_comparison': fmt(wrong_coefficient),
  'actual_finite_difference_coefficient': fmt((ep-E0)/eta**2),
}
print(json.dumps(out, indent=2))

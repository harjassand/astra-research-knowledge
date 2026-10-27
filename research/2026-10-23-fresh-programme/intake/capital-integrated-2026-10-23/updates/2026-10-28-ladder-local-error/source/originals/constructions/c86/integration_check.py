#!/usr/local/bin/python3
"""Independent finite quadrature/Fock check of the full-detuning reduction.

This constructs the memories in the physical L,R basis, deletes LL and RR,
and uses a rank-one Feshbach reduction at the unperturbed pair.  The
quadrature is not a proof or an interval calculation. All output is local.
"""
import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eig, eigh
from scipy.linalg.blas import zgemm, zgemv

OUT = Path(__file__).resolve().parent


def mm(a, b):
    # Direct BLAS calls avoid a local NumPy matmul floating-point-status
    # warning for bounded finite inputs. Check the result explicitly.
    ans = zgemv(1., a, b) if b.ndim == 1 else zgemm(1., a, b)
    assert np.all(np.isfinite(ans))
    return ans


def bilinear(a, b):
    return np.sum(a * b)


def fock(n, theta):
    x, w = leggauss(n)
    k, w = (x + 1) * np.pi / 2, w * np.pi / 2
    phi = k - 1j * theta * np.sin(k)
    endpoint = np.sqrt(2 * w / np.pi) * np.sin(phi) * np.sqrt(
        1 - 1j * theta * np.cos(k))
    N = 2 + 2 * n
    h = np.diag(np.r_[3., 3., 5 - np.cos(phi), 1 - np.cos(phi)]).astype(complex)
    for memory, sign in [(0, 1), (1, -1)]:
        for offset, coupling in [(2, np.sqrt(2 / 25) / np.sqrt(2)),
                                 (2 + n, sign * np.sqrt(1 / 25) / np.sqrt(2))]:
            h[memory, offset:offset + n] = coupling * endpoint
            h[offset:offset + n, memory] = coupling * endpoint
    basis = [(i, j) for i in range(N) for j in range(i, N)]
    lookup = {b: j for j, b in enumerate(basis)}
    A = np.zeros((len(basis), len(basis)), complex)
    V = np.zeros_like(A)
    S = np.zeros_like(A).real
    for column, state in enumerate(basis):
        occ = np.bincount(state, minlength=N)
        V[column, column] = occ[0] - occ[1]
        reflected = tuple(sorted(1 - i if i < 2 else i for i in state))
        parity = (-1) ** sum(i >= 2 + n for i in state)
        S[lookup[reflected], column] = parity
        for j in np.flatnonzero(occ):
            for i in np.flatnonzero(h[:, j]):
                moved = occ.copy()
                amp = np.sqrt(moved[j])
                moved[j] -= 1
                amp *= np.sqrt(moved[i] + 1)
                moved[i] += 1
                final = tuple(np.repeat(np.arange(N), moved))
                A[lookup[final], column] += h[i, j] * amp
    forbidden = [lookup[(0, 0)], lookup[(1, 1)]]
    allowed = [j for j in range(len(basis)) if j not in forbidden]
    H, Vh, Sh = [a[np.ix_(allowed, allowed)] for a in (A, V, S)]
    pair = np.zeros(len(allowed))
    pair[allowed.index(lookup[(0, 1)])] = 1
    return A, V, H, Vh, Sh, pair, allowed, forbidden


def run(n, theta):
    A, V, H, Vh, Sh, pair, allowed, forbidden = fock(n, theta)
    parities, U = eigh(Sh)
    Ue, Uo = U[:, parities > 0], U[:, parities < 0]
    He, Ho = mm(mm(Ue.T, H), Ue), mm(mm(Uo.T, H), Uo)
    energies, vecs = eig(He)
    selected = np.argmin(abs(energies - 5.97857931516658))
    E = energies[selected]
    psi = mm(Ue, vecs[:, selected])
    psi /= np.sqrt(bilinear(psi, psi))
    f = mm(Uo.T, mm(Vh, psi))
    s = bilinear(f, np.linalg.solve(Ho - E * np.eye(len(Ho)), f))

    # Complex orthogonal coordinates split span(psi) and its transpose
    # complement. A Householder reflection gives O.T @ O = I exactly
    # in algebra, without replacing the transpose by a conjugate transpose.
    sign = 1 if abs(psi[0] + 1) >= abs(psi[0] - 1) else -1
    direction = psi.copy()
    direction[0] += sign
    O = np.eye(len(psi)) - 2 * np.outer(direction, direction) / bilinear(direction, direction)
    Q = O[:, 1:]
    fq = mm(Q.T, mm(Vh, psi))
    hq, vq = mm(mm(Q.T, H), Q), mm(mm(Q.T, Vh), Q)
    poles = []
    for eta in [.04, .02]:
        detuned = H + eta * Vh
        ev, vv = eig(detuned)
        j = np.argmin(abs(ev - E))
        lam = ev[j]
        chi = vv[:, j] / np.sqrt(bilinear(vv[:, j], vv[:, j]))
        schur = E - lam - eta ** 2 * bilinear(fq, np.linalg.solve(
            hq + eta * vq - lam * np.eye(len(hq)), fq))
        poles.append(dict(eta=eta, pole=complex_dict(lam),
                          eta2_shift=complex_dict((lam - E) / eta ** 2),
                          exact_Feshbach_residual=float(abs(schur)),
                          bare_pair_coefficient=complex_dict(bilinear(pair, chi) ** 2),
                          dressed_pair_coefficient=complex_dict(bilinear(psi, chi) ** 2)))

    # Full harmonic two-constraint inverse in the physical memory basis.
    eta, z = .07, E + .017j
    RA = np.linalg.inv(A + eta * V - z * np.eye(len(A)))
    K = RA[np.ix_(forbidden, forbidden)]
    constrained = RA - mm(RA[:, forbidden], np.linalg.solve(K, RA[forbidden, :]))
    direct = np.linalg.inv(H + eta * Vh - z * np.eye(len(H)))
    error = np.max(abs(direct - constrained[np.ix_(allowed, allowed)]))
    D = hq + eta * vq - z * np.eye(len(hq))
    Df = np.linalg.solve(D, fq)
    F = E - z - eta ** 2 * bilinear(fq, Df)
    pq = mm(Q.T, pair)
    Dp = np.linalg.solve(D, pq)
    numerator = bilinear(psi, pair) - eta * bilinear(fq, Dp)
    Gp_formula = bilinear(pq, Dp) + numerator ** 2 / F
    Gpsi_direct = bilinear(psi, mm(direct, psi))
    Gp_direct = bilinear(pair, mm(direct, pair))
    Fminus = E - z - eta ** 2 * bilinear(fq, np.linalg.solve(
        hq - eta * vq - z * np.eye(len(hq)), fq))
    return dict(nodes_per_bath=n, theta=theta, allowed_dimension=len(H),
                E=complex_dict(E), s=complex_dict(s),
                rho_from_s=float(s.imag / np.pi),
                full_two_constraint_inverse_error=float(error),
                exact_dressed_response_error=float(abs(Gpsi_direct - 1 / F)),
                exact_bare_response_error=float(abs(Gp_direct - Gp_formula)),
                exact_Feshbach_evenness_error=float(abs(F - Fminus)),
                parity_commutator=float(np.max(abs(mm(H, Sh) - mm(Sh, H)))),
                perturbation_parity_error=float(np.max(abs(mm(Vh, Sh) + mm(Sh, Vh)))),
                perturbation_norm=float(np.max(abs(np.diag(Vh)))),
                complex_orthogonal_error=float(np.max(abs(mm(O.T, O) - np.eye(len(O))))),
                pair_equation_residual=float(np.linalg.norm(mm(H, psi) - E * psi)),
                actual_detuning_poles=poles)


def complex_dict(z):
    return {"real": float(np.real(z)), "imag": float(np.imag(z))}


if __name__ == "__main__":
    results = dict(scope="Floating-point finite quadrature/Fock diagnostics only; no interval or existence claim.",
                   checks=[run(8, .25), run(12, .25), run(20, .25)])
    (OUT / "integration_check_results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))

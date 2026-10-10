"""Algebraic third-order acquisition check; no H3-oracle experiment claim.

The H3 calls here are evaluated from auditor-known K/alpha. Physical
phase-cycling acquisition is a separate obligation, explicitly not simulated
by this file. Python + numpy only.
"""
import json
import numpy as np
from pathlib import Path

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(314159)


def world(n):
    a = np.ones(n) / np.sqrt(n)
    z = np.eye(n)[0] - a
    H = np.eye(n) - 2 * np.outer(z, z) / (z @ z)
    Q, _ = np.linalg.qr(RNG.normal(size=(n - 1, n - 1)))
    P = np.eye(n)
    P[1:, 1:] = Q
    U = P @ H
    lam = np.linspace(1.0, 4.0, n)
    K = (U * lam) @ U.T
    alpha = RNG.uniform(0.5, 1.5, n)
    k = K[:, 0]
    beta = alpha * k * k
    beta[0] = 0
    A = U.T @ np.diag(beta) @ U
    gamma = (lam[1] - lam[0]) / (20 * n * np.sqrt(lam[-1]))
    return dict(U=U, a=a, lam=lam, K=K, alpha=alpha, beta=beta,
                A=A, gamma=gamma, n=n)


def v(w, s, oscillator):
    z = s * s + w['gamma'] * s if oscillator else s
    return w['a'] / (w['lam'] + z)


def q(w, s, oscillator):
    return w['U'] @ v(w, s, oscillator)


def F(w, s, t, R, oscillator, sigma=0):
    c = (s - t) / 2
    qs, qt = q(w, s, oscillator), q(w, t, oscillator)
    qp, qm = q(w, R + c, oscillator), q(w, -R + c, oscillator)
    raw = np.sum(w['alpha'] * qs * qt * qp * qm)
    raw += sigma * (RNG.normal() + 1j * RNG.normal()) / np.sqrt(2)
    return raw, qp[0] * qm[0]


def Bfinite(w, s, t, Omega, oscillator, sigma=0):
    R = 1j * Omega
    f1, p1 = F(w, s, t, R, oscillator, sigma)
    f2, p2 = F(w, s, t, 2 * R, oscillator, sigma)
    if oscillator:
        return (16 / 15) * R**4 * (f1 / p1 - f2 / p2)
    return -(4 / 3) * R**2 * (f1 / p1 - f2 / p2)


def AfromB(V, B):
    return np.linalg.solve(V.T, np.linalg.solve(V.T, B.T).T)


def quotient_error(w, A):
    A = np.real((A + A.T) / 2)
    eig, rows = np.linalg.eigh(A)
    Uhat = rows.T
    # beta ordering and row signs are auditor-only error alignment, not learner input.
    order = np.argsort(w['beta'])
    Utrue = w['U'][order]
    signs = np.sign(np.sum(Uhat * Utrue, axis=1))
    Uhat *= signs[:, None]
    Khat = (Uhat * w['lam']) @ Uhat.T
    Ktrue = w['K'][np.ix_(order, order)]
    return float(np.linalg.norm(Khat - Ktrue, 2)), float(np.min(np.diff(np.sort(w['beta']))))


def run():
    result = {'disclosure': __doc__.strip(), 'conditioning': [], 'oscillator_finite': [],
              'first_order_finite': [], 'noise': []}
    worlds = {}
    for n in [4, 8, 16, 32]:
        w = worlds[n] = world(n)
        ss = 1j * np.sqrt(w['lam'])
        for osc in [False, True]:
            V = np.array([v(w, s, osc) for s in ss]).T
            B = V.T @ w['A'] @ V
            Ah = AfromB(V, B)
            err, gap = quotient_error(w, Ah)
            result['conditioning'].append(dict(n=n, oscillator=osc,
                gamma=w['gamma'] if osc else None, condV=float(np.linalg.cond(V)),
                exact_B_A_error=float(np.linalg.norm(Ah - w['A'], 2)),
                exact_B_K_error=err, beta_gap=gap))
        for Omega in [10, 20, 40, 80, 160]:
            for osc in [False, True]:
                if not osc and n > 8:
                    continue
                V = np.array([v(w, s, osc) for s in ss]).T
                B = np.array([[Bfinite(w, s, t, Omega, osc) for t in ss] for s in ss])
                Ah = AfromB(V, B)
                err, gap = quotient_error(w, Ah)
                key = 'oscillator_finite' if osc else 'first_order_finite'
                result[key].append(dict(n=n, Omega=Omega,
                    A_error=float(np.linalg.norm(Ah-w['A'], 2)), K_error=err,
                    beta_gap=gap))
    w = worlds[8]
    ss = 1j * np.sqrt(w['lam'])
    V = np.array([v(w, s, True) for s in ss]).T
    for Omega in [10, 20, 40, 80]:
        for sigma in [0, 1e-16, 1e-14, 1e-12, 1e-10]:
            B = np.array([[Bfinite(w, s, t, Omega, True, sigma) for t in ss] for s in ss])
            Ah = AfromB(V, B)
            err, gap = quotient_error(w, Ah)
            result['noise'].append(dict(n=8, Omega=Omega, raw_H3_complex_noise=sigma,
                A_error=float(np.linalg.norm(Ah-w['A'], 2)), K_error=err))
    (OUT / 'recovery_results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()

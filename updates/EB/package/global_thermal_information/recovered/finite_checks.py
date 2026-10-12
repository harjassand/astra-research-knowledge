"""Finite falsification checks for the global thermal-conditioning proof.

These computations check exact algebraic identities up to floating-point and
quadrature error. They are not a proof of any uniform-in-system-size bound.
Run: python finite_checks.py --output finite_checks.json
Requires Python >=3.10, NumPy, SciPy.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from scipy.integrate import quad_vec

CArray = NDArray[np.complex128]
PAULI = [np.eye(2, dtype=complex), np.array([[0, 1], [1, 0]], complex),
         np.array([[0, -1j], [1j, 0]], complex), np.diag([1, -1]).astype(complex)]

def pauli(word: tuple[int, ...]) -> CArray:
    out = np.ones((1, 1), complex)
    for a in word:
        out = np.kron(out, PAULI[a])
    return out

def word(n: int, assignments: dict[int, int]) -> tuple[int, ...]:
    return tuple(assignments.get(i, 0) for i in range(n))

def thermal_data(H: CArray, beta: float):
    e, U = np.linalg.eigh(H)
    logs = -beta * (e - e.min())
    p = np.exp(logs)
    p /= p.sum()
    return e, U, p

def covariance_matrices(H: CArray, basis: list[CArray], beta: float):
    e, U, p = thermal_data(H, beta)
    mats = np.array([U.conj().T @ P @ U for P in basis])
    means = np.real(np.einsum('i,aii->a', p, mats))
    for a, m in enumerate(means):
        mats[a] -= m * np.eye(H.shape[0])
    kms = np.sqrt(p[:, None] * p[None, :])
    # Stable logarithmic mean via sinh(x)/x near zero.
    halfdiff = 0.5 * (np.log(p)[:, None] - np.log(p)[None, :])
    ratio = np.ones_like(halfdiff)
    mask = np.abs(halfdiff) > 1e-8
    ratio[mask] = np.sinh(halfdiff[mask]) / halfdiff[mask]
    bkm = kms * ratio
    flat = mats.reshape(len(basis), -1)
    K = np.real((flat.conj() * kms.ravel()) @ flat.T)
    C = np.real((flat.conj() * bkm.ravel()) @ flat.T)
    return K, C

def identity_check(rng: np.random.Generator, n: int, beta: float):
    words = [word(n, {i: a}) for i in range(n) for a in (1, 2, 3)]
    words += [word(n, {i: 1, i + 1: 3}) for i in range(n - 1)]
    basis = [pauli(w) for w in words]
    h = rng.uniform(-0.7, 0.7, len(words))
    strength = max(sum(abs(h[a]) for a, w in enumerate(words) if w[i]) for i in range(n))
    h /= strength
    H = sum(c * P for c, P in zip(h, basis))
    e, U, p = thermal_data(H, beta)
    de = e[:, None] - e[None, :]
    Q = U.conj().T @ pauli(word(n, {0: 2})) @ U
    X = rng.normal(size=H.shape) + 1j * rng.normal(size=H.shape)
    Y = rng.normal(size=H.shape) + 1j * rng.normal(size=H.shape)
    W = np.sqrt(p[:, None] * p[None, :])
    inner = lambda A, B: np.sum(A.conj() * B * W)
    filt = lambda w: Q * np.exp(-0.5 * (w - de) ** 2)
    max_adjoint = 0.0
    max_modular = 0.0
    for w in (-2.1, -0.3, 0.0, 0.8, 2.0):
        B = filt(w)
        dX = B @ X - X @ B
        C = np.exp(-beta * w / 2 + beta ** 2 / 8) * filt(-w + beta / 2)
        D = np.exp(beta * w / 2 + beta ** 2 / 8) * filt(-w - beta / 2)
        dsharpY = C @ Y - Y @ D
        lhs, rhs = inner(dX, Y), inner(X, dsharpY)
        max_adjoint = max(max_adjoint, float(abs(lhs - rhs) / max(1.0, abs(lhs), abs(rhs))))
        z = beta / 2
        left = np.exp(z * de) * B
        right = np.exp(z * w + z * z / 2) * filt(w + z)
        max_modular = max(max_modular, float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left))))
    # Integration tests on one local G_j; split at |omega|'s cusp.
    def applyG(A: CArray):
        def integrand(w: float):
            B = filt(w)
            dA = B @ A - A @ B
            C = np.exp(-beta * w / 2 + beta ** 2 / 8) * filt(-w + beta / 2)
            D = np.exp(beta * w / 2 + beta ** 2 / 8) * filt(-w - beta / 2)
            return np.exp(-(1 + beta) * abs(w)) * (C @ dA - dA @ D)
        R = float(np.ptp(e) + beta / 2 + 10)
        a, ea = quad_vec(integrand, -R, 0, epsabs=2e-11, epsrel=2e-11)
        b, eb = quad_vec(integrand, 0, R, epsabs=2e-11, epsrel=2e-11)
        return a + b, float(ea + eb)
    GX, errx = applyG(X)
    GY, erry = applyG(Y)
    GI, _ = applyG(np.eye(H.shape[0], dtype=complex))
    lhs, rhs = inner(X, GY), inner(GX, Y)
    pos = inner(X, GX)
    return {"n": n, "beta": beta,
            "max_pointwise_adjoint_relative_error": max_adjoint,
            "max_gaussian_modular_relative_error": max_modular,
            "integrated_self_adjoint_relative_error": float(abs(lhs-rhs)/max(1.0,abs(lhs),abs(rhs))),
            "integrated_identity_image_norm": float(np.linalg.norm(GI)),
            "positive_quadratic_form_real": float(pos.real),
            "positive_quadratic_form_imaginary": float(abs(pos.imag)),
            "quadrature_reported_error": max(errx, erry)}

def covariance_checks(rng: np.random.Generator):
    output = []
    for n in (3, 4, 5):
        for model in ("random_noncommuting_chain", "antiferromagnetic_heisenberg_cycle"):
            words = [word(n, {i: a}) for i in range(n) for a in (1, 2, 3)]
            edges = [(i, i+1) for i in range(n-1)]
            if model.startswith("antiferromagnetic"):
                edges.append((n-1, 0))
            words += [word(n, {i: a, j: a}) for i,j in edges for a in (1,2,3)]
            words = list(dict.fromkeys(words))
            basis = [pauli(w) for w in words]
            if model.startswith("random"):
                h = rng.uniform(-1, 1, len(words))
            else:
                h = np.array([0.12 * rng.uniform(-1, 1) if sum(a != 0 for a in w) == 1 else 1.0 for w in words])
            g = max(sum(abs(h[a]) for a,w in enumerate(words) if w[i]) for i in range(n))
            h /= g
            H = sum(c*P for c,P in zip(h,basis))
            for beta in (0.2, 1.0, 4.0, 10.0):
                K, C = covariance_matrices(H,basis,beta)
                output.append({"n": n, "model": model, "beta_g": beta,
                    "terms": len(words), "kms_min_eigenvalue": float(np.linalg.eigvalsh(K)[0]),
                    "bkm_min_eigenvalue": float(np.linalg.eigvalsh(C)[0]),
                    "bkm_minus_kms_min_eigenvalue": float(np.linalg.eigvalsh(C-K)[0])})
    return output

def star_checks():
    beta,h,lam = 1.3,0.7,0.4
    t = math.tanh(beta*h)
    out=[]
    for N in (2,4,8,32,128,1024,100000):
        ts=np.tanh(beta*(h+lam*np.array([-1.,1.])/N))
        logs=beta*h*np.array([-1.,1.])+N*np.log(2*np.cosh(beta*(h+lam*np.array([-1.,1.])/N)))
        ps=np.exp(logs-logs.max()); ps/=ps.sum()
        mean=float(np.dot(ps,np.array([-1.,1.])*(ts-t)))
        second=float(np.dot(ps,(1-ts*ts)/N+(ts-t)**2))
        var=second-mean*mean
        out.append({"N":N,"variance":var,"coefficient_norm_squared":t*t+1/N,
            "variance_ratio":var/(t*t+1/N),"proven_variance_upper_bound":1/N+(beta*lam)**2/N**2})
    return {"beta":beta,"h":h,"lambda":lam,"values":out}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('finite_checks.json'))
    args=parser.parse_args()
    rng=np.random.default_rng(261012)
    ids=[identity_check(rng,n,b) for n in (2,3) for b in (0.2,1.0,3.0)]
    cov=covariance_checks(rng)
    out={"status":"finite floating-point falsification checks, not proof or independent validation",
         "seed":261012,"identity_checks":ids,"covariance_checks":cov,"star_counterexample":star_checks()}
    # Loose numerical tolerances, explicitly reported rather than treated as certification.
    out['all_declared_checks_passed']=bool(
        all(x['max_pointwise_adjoint_relative_error']<1e-9 and x['max_gaussian_modular_relative_error']<1e-9
            and x['integrated_self_adjoint_relative_error']<1e-9 and x['integrated_identity_image_norm']<1e-10
            and x['positive_quadratic_form_real']>-1e-9 for x in ids)
        and all(x['kms_min_eigenvalue']>-1e-9 and x['bkm_minus_kms_min_eigenvalue']>-1e-9 for x in cov)
        and all(x['variance']<=x['proven_variance_upper_bound']+1e-12 for x in out['star_counterexample']['values']))
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'passed':out['all_declared_checks_passed'],'identity_instances':len(ids),
        'covariance_instances':len(cov),'max_adjoint_error':max(x['max_pointwise_adjoint_relative_error'] for x in ids),
        'min_kms_eigenvalue':min(x['kms_min_eigenvalue'] for x in cov)},indent=2))

if __name__=='__main__':
    main()

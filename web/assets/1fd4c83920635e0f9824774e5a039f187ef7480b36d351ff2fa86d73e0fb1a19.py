"""Finite diagnostics for the independent concentration theorem; not proof validation."""
from fractions import Fraction as F
from math import comb, sqrt
from pathlib import Path
import itertools
import json
import numpy as np


exact_checks = 0
for n in range(2, 65):
    for r in range(1, min(n-1, 16)+1):
        for k in range(1, r+1):
            assert F(comb(r, k), comb(n, k)) <= F(r, n)**k
            falling = 1
            for ell in range(k):
                falling *= n-ell
            assert falling >= (n-r)**k
            exact_checks += 2

for d in range(2, 9):
    m = d*d-1
    for k in range(2, 65):
        alpha = 1
        for ell in range(k):
            alpha *= m+2*ell
        assert F(alpha) <= (F(k)*(F(m, 2)+1))**k
        exact_checks += 1

example_checks = []
for d in range(2, 6):
    for n in [4, 8, 16, 32, 64]:
        for r in [2, 3, 4]:
            if r > n:
                continue
            eps = F(2, d*n)
            direct = ((1+eps)**r+(1-eps)**r)/2-1
            expansion = sum(F(comb(r, k))*eps**k for k in range(2, r+1, 2))
            lower = F(2*r*(r-1), d*d*n*n)
            assert direct == expansion
            assert direct >= lower
            exact_checks += 2
            if n == 64 and r == 4:
                example_checks.append({"d": d, "N": n, "r": r,
                                       "chi2": float(direct),
                                       "quadratic_term": float(lower)})


def basis(d):
    answer = []
    for a in range(d):
        for b in range(a+1, d):
            symmetric = np.zeros((d, d), complex)
            symmetric[a, b] = symmetric[b, a] = 1/sqrt(2)
            answer.append(symmetric)
            imaginary = np.zeros((d, d), complex)
            imaginary[a, b] = -1j/sqrt(2)
            imaginary[b, a] = 1j/sqrt(2)
            answer.append(imaginary)
    for k in range(1, d):
        diagonal = np.zeros(d)
        diagonal[:k] = 1/sqrt(k*(k+1))
        diagonal[k] = -k/sqrt(k*(k+1))
        answer.append(np.diag(diagonal).astype(complex))
    return answer


def kron_all(items):
    answer = np.array([[1]], complex)
    for item in items:
        answer = np.kron(answer, item)
    return answer


rng = np.random.default_rng(2026100811)
scalar_checks = 0
for _ in range(10000):
    a = rng.uniform(-2, 2)
    z = rng.uniform(-2, 2)+1j*rng.uniform(-2, 2)
    lhs = abs(1+z*a)
    rhs = np.exp(a*z.real+abs(z)**2*a*a/2)
    assert lhs <= rhs+1e-12
    scalar_checks += 1

matrix_checks = []
for d in [2, 3, 4]:
    fs = basis(d)
    hs_gram = np.array([[np.trace(left@right) for right in fs] for left in fs])
    assert np.max(abs(hs_gram-np.eye(d*d-1))) < 1e-12
    for trial in range(3):
        w = rng.normal(size=(d, d))+1j*rng.normal(size=(d, d))
        tau = 0.5*np.eye(d)/d+0.5*(w@w.conj().T)/np.trace(w@w.conj().T).real
        coefficients = rng.normal(size=d*d-1)
        k_operator = sum(coefficient*fa for coefficient, fa in zip(coefficients, fs))
        k_operator /= np.linalg.norm(k_operator, 2)
        kapp = 0.5/d
        centered = [fa-np.trace(tau@fa).real*np.eye(d) for fa in fs]
        gram = np.array([[np.trace(tau@left@right) for right in centered]
                         for left in centered])
        assert np.linalg.eigvalsh(gram)[0] >= kapp-1e-12
        moments = np.array([np.trace(k_operator@fa).real for fa in fs])
        parsed_k_norm = (moments.conj()@np.linalg.solve(gram, moments)).real
        direct_k_norm = np.trace(k_operator@k_operator@np.linalg.inv(tau)).real
        assert abs(parsed_k_norm-direct_k_norm) < 1e-11
        n = 8
        epsilon = 0.2/d/sqrt(n)
        plus = tau+epsilon*k_operator
        minus = tau-epsilon*k_operator
        assert np.linalg.eigvalsh(plus)[0] > 0
        assert np.linalg.eigvalsh(minus)[0] > 0
        for r in [2, 3]:
            rho = (kron_all([plus]*r)+kron_all([minus]*r))/2
            sigma = kron_all([tau]*r)
            direct = np.trace(rho@rho@np.linalg.inv(sigma)).real-1
            s = epsilon**2*direct_k_norm
            exact_branch = ((1+s)**r+(1-s)**r)/2-1
            parsed = sum(comb(r, k)*(epsilon**2*parsed_k_norm)**k
                         for k in range(2, r+1, 2))
            assert abs(direct-exact_branch) < 1e-10
            assert abs(direct-parsed) < 1e-10
            eigenvalues = np.linalg.eigvalsh(rho)
            ref_values, ref_vectors = np.linalg.eigh(sigma)
            log_sigma = (ref_vectors*np.log(ref_values))@ref_vectors.conj().T
            entropy = np.sum(eigenvalues*np.log(eigenvalues))-np.trace(rho@log_sigma).real
            assert entropy <= np.log1p(direct)+1e-10
            commutator = np.linalg.norm(rho@sigma-sigma@rho)
            assert commutator > 1e-12
            matrix_checks.append({"d": d, "trial": trial, "N": n, "r": r,
                                  "chi2": float(direct),
                                  "gram_error": float(abs(direct-parsed)),
                                  "relative_entropy": float(entropy),
                                  "commutator_norm": float(commutator),
                                  "gram_minimum_eigenvalue": float(np.linalg.eigvalsh(gram)[0]),
                                  "kappa": kapp})

results = {"exact_checks": exact_checks,
           "scalar_generating_product_checks": scalar_checks,
           "noncommuting_matrix_cases": len(matrix_checks),
           "max_gram_error": max(case["gram_error"] for case in matrix_checks),
           "quadratic_rate_example_diagnostics": example_checks,
           "matrix_diagnostics": matrix_checks,
           "scope": "Finite diagnostics, not a substitute for the written proof or external validation."}
Path(__file__).with_name("verification_results.json").write_text(json.dumps(results, indent=2)+"\n")
print(json.dumps({k: v for k, v in results.items() if k != "matrix_diagnostics"}, indent=2))

#!/usr/bin/env python3
"""Exact finite checks for response-completed closure.

General proofs are in proof_note.md. These checks are falsification tests,
not an independent proof, novelty check, or statistical experiment.
Requires sympy, numpy, scipy. Outputs verification_results.json.
"""
from __future__ import annotations
import json
import random
from pathlib import Path
import sympy as sp
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent
COUNT = 0


def check(condition: bool, message: str) -> None:
    global COUNT
    if not condition:
        raise AssertionError(message)
    COUNT += 1


def zeq(a: sp.Matrix, b: sp.Matrix, message: str) -> None:
    check(a == b, message)


def stationary(Q: sp.Matrix) -> sp.Matrix:
    n = Q.rows
    A = Q.T.copy()
    rhs = sp.zeros(n, 1)
    A[n - 1, :] = sp.ones(1, n)
    rhs[n - 1] = 1
    return A.inv() * rhs


def indicator(labels: list[int]) -> sp.Matrix:
    k = max(labels) + 1
    return sp.Matrix([[int(a == b) for b in range(k)] for a in labels])


def generator(raw: sp.Matrix) -> sp.Matrix:
    Q = raw.copy()
    for i in range(Q.rows):
        Q[i, i] = -sum(Q[i, j] for j in range(Q.rows) if j != i)
    return Q


def rate_derivative(Q: sp.Matrix, f: sp.Matrix) -> sp.Matrix:
    V = sp.zeros(Q.rows)
    for i in range(Q.rows):
        for j in range(Q.rows):
            if i != j:
                V[i, j] = Q[i, j] * (f[j] - f[i]) / 2
    return generator(V)


def closure_data(Q: sp.Matrix, labels: list[int]) -> dict:
    n = Q.rows
    E = indicator(labels)
    k = E.cols
    pi = stationary(Q)
    R = sp.diag(*pi)
    mu = E.T * pi
    M = sp.diag(*mu)
    P = E * M.inv() * E.T * R
    A = E.T * R * Q * E
    L = M.inv() * A
    C2 = E.T * R * Q**2 * E
    X2 = sp.zeros(k)
    X2clock = sp.zeros(k)
    for a in range(k):
        V = rate_derivative(Q, E[:, a])
        X2[a, :] = pi.T * V * Q * E
        Vclock = -sp.diag(*E[:, a]) * Q
        X2clock[a, :] = pi.T * Vclock * Q * E
    weights = [(sp.Rational(2), -sp.Rational(1,6)),
               (sp.Rational(1,2), sp.Rational(1,6)),
               (sp.Rational(3,2), sp.Rational(9,10)),
               (sp.Rational(2,3), -sp.Rational(9,10))]
    X2finite = sp.zeros(k)
    for a in range(k):
        fa=E[:,a]
        for z,weight in weights:
            raw=sp.zeros(n)
            for i in range(n):
                for j in range(n):
                    if i != j: raw[i,j]=Q[i,j]*z**(fa[j]-fa[i])
            Qz=generator(raw)
            X2finite[a,:] += weight*pi.T*Qz**2*E
    zeq(X2finite,X2,'four finite fields recover exact response curvature')
    H = -2 * X2 - C2
    Gamma = H - L.T * M * L
    residual = Q * E - E * L
    zeq(Q * sp.ones(n, 1), sp.zeros(n, 1), 'row sums')
    zeq(pi.T * Q, sp.zeros(1, n), 'stationarity')
    check(all(p > 0 for p in pi), 'positive pi')
    zeq(H, E.T * Q.T * R * Q * E, 'response Gram identity')
    zeq(Gamma, residual.T * R * residual, 'residual factorization')
    zeq(Gamma, Gamma.T, 'symmetry')
    zeq(Gamma * sp.ones(k, 1), sp.zeros(k, 1), 'constant nullspace')
    zeq(X2clock, -C2, 'source-clock FDT curvature')
    zeq(P**2, P, 'projection')
    zeq(P.T * R, R * P, 'weighted orthogonality')
    rng = random.Random(n * 101 + k)
    for _ in range(5):
        v = sp.Matrix([rng.randrange(-3, 4) for _ in range(k)])
        check((v.T * Gamma * v)[0] >= 0, 'nonnegative tested direction')
    return dict(Q=Q, E=E, pi=pi, R=R, mu=mu, M=M, P=P,
                A=A, L=L, C2=C2, X2=X2, Gamma=Gamma, residual=residual)


def random_general(seed: int, n: int, k: int) -> dict:
    rng = random.Random(seed)
    raw = sp.Matrix(n, n, lambda i, j: 0 if i == j else rng.randrange(1, 13))
    Q = generator(raw)
    scale = max(-Q[i, i] for i in range(n))
    Q /= scale
    labels = [i % k for i in range(n)]
    return closure_data(Q, labels)


def random_passive_fiber(seed: int, n: int, k: int) -> dict:
    rng = random.Random(seed)
    labels = [i % k for i in range(n)]
    E = indicator(labels)
    pi = sp.ones(n, 1) / n
    M = sp.diag(*(E.T * pi))
    P = E * M.inv() * E.T / n
    J = sp.ones(n) / n
    Z = sp.Matrix(n, n, lambda i, j: rng.randrange(-3, 4))
    A = (sp.eye(n) - P) * Z * (sp.eye(n) - J)
    largest = max(abs(a) for a in A)
    epsilon = sp.Rational(1, 4*n) / max(sp.Rational(1), largest)
    Q = J - sp.eye(n) + epsilon * A
    data = closure_data(Q, labels)
    zeq(P * Q * (sp.eye(n) - P), sp.zeros(n), 'reverse lumpability')
    zeq(data['L'], sp.ones(k, 1) * data['mu'].T - sp.eye(k), 'fixed macro generator')
    for j in range(1, 6):
        zeq(E.T * data['R'] * Q**j * E,
            M * data['L']**j, 'passive semigroup jets')
    check(all(Q[i,j] >= sp.Rational(3,4*n)
              for i in range(n) for j in range(n) if i != j), 'positive fiber rates')
    return data


def lift_lumpable(seed: int) -> dict:
    rng = random.Random(seed)
    n, k = 6, 3
    labels = [0,0,1,1,2,2]
    macro = generator(sp.Matrix(k,k,lambda a,b: 0 if a==b else sp.Rational(rng.randrange(1,6),20)))
    raw = sp.zeros(n)
    for i in range(n):
        a = labels[i]
        for b in range(k):
            targets = [j for j in range(n) if labels[j] == b and j != i]
            if b == a:
                for j in targets:
                    raw[i,j] = sp.Rational(rng.randrange(1,5),30)
            else:
                first = sp.Rational(rng.randrange(1,9),10)
                raw[i,targets[0]] = macro[a,b] * first
                raw[i,targets[1]] = macro[a,b] * (1-first)
    data = closure_data(generator(raw), labels)
    zeq(data['Gamma'], sp.zeros(k), 'strong lumpability implies zero certificate')
    zeq(data['L'], macro, 'lift has intended macro generator')
    return data


def lumpable_comparator(data: dict) -> sp.Matrix:
    Q, E, L = data['Q'], data['E'], data['L']
    n, k = Q.rows, E.cols
    labels = [next(b for b in range(k) if E[i,b]) for i in range(n)]
    raw = sp.zeros(n)
    for i in range(n):
        a = labels[i]
        for b in range(k):
            targets = [j for j in range(n) if labels[j] == b and j != i]
            if a == b:
                for j in targets: raw[i,j] = Q[i,j]
            else:
                r = sum(Q[i,j] for j in targets)
                if r > 0:
                    for j in targets: raw[i,j] = Q[i,j] * L[a,b] / r
                else:
                    for j in targets: raw[i,j] = L[a,b] / len(targets)
    Qbar = generator(raw)
    zeq(Qbar * E, E * L, 'comparison chain exactly lumpable')
    return Qbar


def numeric_kl_rate(data: dict) -> dict:
    Q, Qbar = data['Q'], lumpable_comparator(data)
    pi, L, E = data['pi'], data['L'], data['E']
    n,k = Q.rows,E.cols
    rate = 0.0
    variance_bound = 0.0
    for i in range(n):
        a = next(b for b in range(k) if E[i,b])
        for b in range(k):
            if b == a: continue
            r = sum(Q[i,j] for j in range(n) if E[j,b])
            l = L[a,b]
            if l > 0:
                rr, ll = float(r), float(l)
                rate += float(pi[i]) * (rr*np.log(rr/ll)-rr+ll if rr else ll)
                variance_bound += float(pi[i] * (r-l)**2/l)
    ell = min(L[a,b] for a in range(k) for b in range(k) if a != b and L[a,b]>0)
    trace_bound = float(sp.trace(data['Gamma'])/ell)
    check(rate <= variance_bound + 1e-13, 'numeric Poisson entropy upper bound')
    check(variance_bound <= trace_bound + 1e-13, 'numeric trace bound')
    return dict(kl_rate=rate, variance_bound=variance_bound, trace_bound=trace_bound)


def finite_mean(Q: np.ndarray, pi: np.ndarray, f: np.ndarray,
                g: np.ndarray, h: float, t: float, clock=False) -> float:
    if clock:
        Qh = np.diag(np.exp(-h*f)) @ Q
    else:
        Qh = Q * np.exp(h*(f[None,:]-f[:,None])/2)
        np.fill_diagonal(Qh, 0.0)
        np.fill_diagonal(Qh, -Qh.sum(axis=1))
    return float(pi @ expm(t*Qh) @ g)


def four_state() -> dict:
    n=4
    f=sp.Matrix([1,-1,1,-1])
    g=sp.Matrix([1,1,-1,-1])
    d=sp.matrix_multiply_elementwise(f,g)
    epsilon=sp.Rational(1,4)
    A=d*f.T/n
    Q=sp.ones(n)/n-sp.eye(n)+epsilon*A
    data=closure_data(Q,[0,1,0,1])
    R=data['R']
    P=data['P']
    zeq(P*Q*(sp.eye(n)-P),sp.zeros(n),'four-state exact passive Markov')
    zeq(A**2,sp.zeros(n),'rank-one nilpotence')
    zeq(data['Gamma'], epsilon**2/4*sp.Matrix([[1,-1],[-1,1]]), 'four-state Gamma')
    check(((Q*f+f).T*R*(Q*f+f))[0] == epsilon**2,'leakage magnitude')
    Qn=np.array(Q,float); pin=np.ones(n)/n; fn=np.array(f,float).ravel()
    h=1e-3; t=1.0
    central=(finite_mean(Qn,pin,fn,fn,h,t)-finite_mean(Qn,pin,fn,fn,-h,t))/(2*h)
    expected=1-np.exp(-t)-float(epsilon**2)/2*(1-(1+t)*np.exp(-t))
    source=(finite_mean(Qn,pin,fn,fn,h,t,True)-finite_mean(Qn,pin,fn,fn,-h,t,True))/(2*h)
    check(abs(central-expected)<1e-6,'numeric geometric response')
    check(abs(source-(1-np.exp(-t)))<1e-6,'numeric source-clock response')
    return dict(generator=[[str(v) for v in Q.row(i)] for i in range(n)],
                gamma=[[str(v) for v in data['Gamma'].row(i)] for i in range(2)],
                numeric_response=central, exact_formula_response=expected,
                numeric_source_clock_response=source)


def ladder_robustness(r: int) -> dict:
    # Only algebra on a 4r-dimensional orthonormal ladder basis is needed.
    n=4*r; ell=2*r-1
    one, f = 0, 1
    c=list(range(2,2+ell)); d=list(range(2+ell,n))
    A=sp.zeros(n)
    A[d[0],f]=1
    for j in range(ell-1): A[d[j+1],c[j]]=1
    A[f,c[-1]]=1
    E=sp.zeros(n)
    E[f,d[0]]=1
    E[c[-1],f]=1
    R=sp.zeros(n); R[one,one]=R[f,f]=1
    for j in range(ell): R[d[ell-1-j],c[j]]=1; R[c[ell-1-j],d[j]]=1
    zeq(R*E*R,E.T,'shortcut retains observation reflection')
    epsilon=sp.Rational(1,16*r); rho=sp.Rational(1,1000)
    Q=-sp.eye(n)+epsilon*A+rho*E; Q[one,one]=0
    basisf=sp.eye(n)[:,f]
    T=Q+sp.eye(n)
    zeq(T**2*basisf,2*epsilon*rho*basisf,'two-step passive shortcut')
    for j in range(1,5):
        check((basisf.T*T**(2*j)*basisf)[0] == (2*epsilon*rho)**j,'cosh even coefficients')
        check((basisf.T*T**(2*j-1)*basisf)[0] == 0,'cosh odd coefficients')
    return dict(r=r,epsilon=str(epsilon),shortcut=str(rho),
                curvature_increment=str(2*epsilon*rho))


def main() -> None:
    cases=[]
    for seed in range(24):
        n=3+seed%6; k=2+seed%min(3,n-1)
        d=random_general(seed,n,k)
        if seed<6: cases.append(numeric_kl_rate(d))
    for seed in range(10): random_passive_fiber(100+seed,6+seed%3,2+seed%2)
    for seed in range(6): lift_lumpable(seed)
    example=four_state()
    shortcuts=[ladder_robustness(r) for r in range(1,9)]
    result=dict(status='Executed exact rational identities plus separately identified floating diagnostics; not a general proof or priority validation.',
                total_checks=COUNT, exact_rational_checks=COUNT-14, floating_diagnostic_checks=14, general_rational_models=24,
                passive_equivalent_fiber_models=10, exactly_lumpable_models=6,
                four_state=example, entropy_rate_diagnostics=cases,
                shortcut_algebra=shortcuts)
    (ROOT/'verification_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ['entropy_rate_diagnostics','shortcut_algebra']},indent=2))

if __name__=='__main__':
    main()

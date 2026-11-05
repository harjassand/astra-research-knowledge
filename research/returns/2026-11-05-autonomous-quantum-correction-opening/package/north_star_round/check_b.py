"""Finite quantum/clock audits; not an asymptotic memory certificate."""
from fractions import Fraction
from math import comb, exp, cosh, ceil, log2
from pathlib import Path
import json
import numpy as np


def expm(matrix):
    """Small-matrix scaling/squaring Taylor exponential; only NumPy needed."""
    norm = float(np.linalg.norm(matrix, ord=np.inf))
    scale = max(0, ceil(log2(norm))) if norm else 0
    small = matrix/(2**scale)
    answer = np.eye(len(matrix), dtype=complex)
    term = answer.copy()
    for k in range(1, 100):
        term = term @ small/k
        answer += term
        if np.linalg.norm(term, ord=np.inf) < 1e-16:
            break
    else:
        raise AssertionError('matrix exponential series failed to converge')
    for _ in range(scale):
        answer = answer @ answer
    return answer


def generator(H, jumps):
    d = len(H)
    eye = np.eye(d)
    out = -1j*(np.kron(eye, H) - np.kron(H.T, eye))
    for jump in jumps:
        square = jump.conj().T @ jump
        out += (np.kron(jump.conj(), jump)
                - .5*np.kron(eye, square) - .5*np.kron(square.T, eye))
    return out


I = np.eye(2)
Z = np.diag([1., -1.])
ground = np.diag([1., 0.])
excited = np.diag([0., 1.])
down = np.array([[0., 1.], [0., 0.]])
up = down.T
bell = np.array([1., 0., 0., 1.])/np.sqrt(2)
initial = np.kron(np.outer(bell, bell), ground)
quantum_cases = 0
max_fidelity_error = 0.
max_negativity_error = 0.
max_stationary_residual = 0.
Delta, rate = 1.5, 1.
for beta in [.5, 2.]:
    for epsilon in [0., .01, .2]:
        H = np.kron(Delta*I + epsilon*Z, excited)
        if epsilon == 0:
            jumps = [np.sqrt(rate)*np.kron(I, down),
                     np.sqrt(rate*exp(-beta*Delta))*np.kron(I, up)]
        else:
            jumps = []
            for P, sign in [(ground, 1), (excited, -1)]:
                jumps += [np.sqrt(rate)*np.kron(P, down),
                          np.sqrt(rate*exp(-beta*(Delta+sign*epsilon)))
                          * np.kron(P, up)]
        gibbs = expm(-beta*H)
        gibbs /= np.trace(gibbs)
        residual = np.linalg.norm(generator(H, jumps) @ gibbs.reshape(-1, order='F'))
        assert residual < 1e-12
        max_stationary_residual = max(max_stationary_residual, float(residual))
        whole_generator = generator(np.kron(I, H), [np.kron(I, j) for j in jumps])
        for time in [.1, 1., 3.]:
            whole = (expm(time*whole_generator) @ initial.reshape(-1, order='F'))
            whole = whole.reshape((8, 8), order='F')
            reduced = np.trace(whole.reshape(2, 2, 2, 2, 2, 2), axis1=2, axis2=5)
            fidelity = float(np.real(bell @ reduced.reshape(4, 4) @ bell))
            partial = whole.reshape(2, 4, 2, 4).transpose(2, 1, 0, 3).reshape(8, 8)
            negativity = float(sum(-x for x in np.linalg.eigvalsh(partial) if x < 0))
            coherence = (1. if epsilon == 0
                         else exp(-rate*exp(-beta*Delta)*cosh(beta*epsilon)*time))
            ferror = abs(fidelity - (1+coherence)/2)
            nerror = abs(negativity - coherence/2)
            assert ferror < 1e-11 and nerror < 1e-11
            max_fidelity_error = max(max_fidelity_error, ferror)
            max_negativity_error = max(max_negativity_error, nerror)
            quantum_cases += 1

rng = np.random.default_rng(729)
port_cases = 0
for m in [1, 2]:
    d = 2**m
    slot_dim = 3**(2*m)
    random = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
    U, _ = np.linalg.qr(random)
    def basis_index(digits):
        value = 0
        for digit in digits:
            value = 3*value + digit
        return value
    def bits(value):
        return [1 + ((value >> k) & 1) for k in reversed(range(m))]
    V = np.zeros((slot_dim, slot_dim), dtype=complex)
    for x in range(d):
        for y in range(d):
            V[basis_index([0]*m+bits(y)), basis_index(bits(x)+[0]*m)] = U[y, x]
    P = V.conj().T @ V
    assert np.linalg.norm(P@P-P) < 1e-11
    assert np.linalg.norm(V@V) < 1e-11
    assert np.linalg.norm(P@V) < 1e-11
    R = np.eye(slot_dim)-P
    random = rng.normal(size=(slot_dim, slot_dim)) + 1j*rng.normal(size=(slot_dim, slot_dim))
    rho = random @ random.conj().T
    rho /= np.trace(rho)
    def attempt(state):
        return V@state@V.conj().T + R@state@R
    assert np.linalg.norm(attempt(attempt(rho))-attempt(rho)) < 1e-11
    assert abs(np.trace(attempt(rho))-1) < 1e-11
    port_cases += 1

clock_cases = 0
for m in range(1, 6):
    for H in [1, 2, 4, 8, 16]:
        dp = {}
        for i in reversed(range(m+1)):
            for j in reversed(range(H+1)):
                dp[i,j] = (Fraction(0) if i == m else Fraction(1) if j == H
                           else (dp[i+1,j]+dp[i,j+1])/2)
        exact = sum(Fraction(comb(H+j-1, j), 2**(H+j)) for j in range(m))
        assert dp[0,0] == exact
        clock_cases += 1

out = {"toy_quantum_cases": quantum_cases,
       "max_fidelity_error": max_fidelity_error,
       "max_negativity_error": max_negativity_error,
       "max_Gibbs_stationarity_residual": max_stationary_residual,
       "one_and_two_qubit_random_unitary_port_cases": port_cases,
       "exact_watchdog_race_cases": clock_cases,
       "status": "all assertions passed",
       "limitation": "finite audits; no autonomous threshold established"}
Path(__file__).with_name('checks_b.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))

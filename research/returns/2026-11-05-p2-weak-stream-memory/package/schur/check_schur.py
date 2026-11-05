#!/usr/bin/env python3
"""Small finite algebra checks and exact analytic Schur-bound evaluation.

This is not a simulation of a streaming decoder or of 43,462 qubits.
"""
import json
import math
from pathlib import Path
import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
P = [I, X, Y, Z]

def swap(n, a, b):
    out = np.zeros((2**n, 2**n), dtype=complex)
    for x in range(2**n):
        bits = [(x >> (n-1-j)) & 1 for j in range(n)]
        bits[a], bits[b] = bits[b], bits[a]
        y = sum(t << (n-1-j) for j, t in enumerate(bits))
        out[y, x] = 1
    return out

def schur_bound(n):
    js = np.arange(n % 2, n+1, 2, dtype=float)/2
    k = n/2-js
    # mu_J = binom(n,k) * (2J+1)/(n/2+J+1).
    lw = np.array([
        2*math.log(2*j+1) - math.log(n/2+j+1)
        + math.lgamma(n+1)-math.lgamma(q+1)-math.lgamma(n-q+1)
        - n*math.log(2)
        for j,q in zip(js,k)
    ])
    w = np.exp(lw)
    active = js > 0
    t = float(np.sum(w[active]*(js[active]+1)/(3*js[active])))
    return {"N": n, "weight_sum": float(w.sum()), "t_upper": t,
            "half_diamond_error_lower": .75*(1-t),
            "asymptotic_lower_leading": .5-1/math.sqrt(2*math.pi*n)}

checks=[]
for theta in (.1, .37, .9):
    c,s = math.cos(theta),math.sin(theta)
    U1=c*np.eye(8)+1j*s*swap(3,0,1)
    U2=c*np.eye(8)+1j*s*swap(3,0,2)
    full=U2@U1@np.kron(Z,np.eye(4))@U1.conj().T@U2.conj().T
    B=np.trace(full.reshape(2,4,2,4),axis1=0,axis2=2)/2
    formula=s*s*(np.kron(Z,I)+c*c*np.kron(I,Z)
                 +c*s*(np.kron(X,Y)-np.kron(Y,X)))
    target=np.sort([-s*s*(1+c*c),s*s*(1+c*c),
                    -s**3*math.sqrt(4-3*s*s),s**3*math.sqrt(4-3*s*s)])
    bell=np.array([1,0,0,1],dtype=complex)/math.sqrt(2)
    phi=np.outer(bell,bell.conj())
    crossed=c*np.eye(4)-2j*s*phi
    Ks=[]
    for pauli in P:
        Q=np.kron(pauli,I)
        phi_p=Q@phi@Q.conj().T
        Ks.append(c*np.eye(4)/2-1j*s*phi_p)
    checks.append({"theta":theta,
                   "N2_formula_error":float(np.linalg.norm(B-formula)),
                   "N2_spectrum_error":float(np.linalg.norm(np.linalg.eigvalsh(B)-target)),
                   "crossed_filter_max_singular_sq":float(np.linalg.norm(crossed,2)**2),
                   "crossed_filter_expected_max_singular_sq":1+3*s*s,
                   "weak_bell_instrument_TP_error":float(np.linalg.norm(sum(k.conj().T@k for k in Ks)-np.eye(4)))})
receipt={"scope":"Finite N=2 matrix checks plus analytic combinatorial sums; no device or large-state simulation.",
         "checks":checks,"schur_bounds":[schur_bound(n) for n in (2,3,10,100,1000,43462)]}
assert max(q["N2_formula_error"] for q in checks)<1e-12
assert max(q["N2_spectrum_error"] for q in checks)<1e-12
assert max(q["weak_bell_instrument_TP_error"] for q in checks)<1e-12
out=Path(__file__).with_name("schur_receipt.json")
out.write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))

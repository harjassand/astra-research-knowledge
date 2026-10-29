"""Finite-matrix checks of polynomial-strength theorem, including high color counts."""
import csv
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.special import logsumexp

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(2026102918)
n, k, order = 4, 2, 8
dim = 2**n


def embed(a, support):
    out = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        b = [(col >> (n-1-j)) & 1 for j in range(n)]
        lc = sum(b[s] << (len(support)-1-j) for j, s in enumerate(support))
        for lr in range(2**len(support)):
            bb = b.copy()
            for j, s in enumerate(support):
                bb[s] = (lr >> (len(support)-1-j)) & 1
            row = sum(bb[j] << (n-1-j) for j in range(n))
            out[row, col] += a[lr, lc]
    return out


def random_term(support):
    d = 2**len(support)
    a = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    a = (a+a.conj().T)/2
    a /= np.linalg.norm(a,2)
    return embed(a,support)


def herm(a):
    return (a+a.conj().T)/2


def norm(a):
    return float(np.linalg.norm(a,2))


def conjugation_coefficients(layers, h):
    coeff = [h] + [np.zeros_like(h) for _ in range(order)]
    for H in layers:
        new = [np.zeros_like(h) for _ in range(order+1)]
        for p in range(order+1):
            term = coeff[p].copy()
            new[p] += term
            for ell in range(1,order-p+1):
                term = -(H@term-term@H)/(2*ell)
                new[p+ell] += term
        coeff = new
    return coeff


matchings = [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]
coefficient_rows, step_rows = [], []
for c in [1,4,16,64]:
    for weight_mode in ["equal", "nonuniform"]:
        Hs, Js, local = [], [], []
        for j in range(c):
            weights = [1/c,1/c] if weight_mode == "equal" else rng.uniform(.05,1,size=2)/c
            terms = [w*random_term(s) for w,s in zip(weights,matchings[j%3])]
            Hs.append(sum(terms))
            Js.append(max(weights))
            local.extend(terms)
        L = sum(norm(h) for h in local)
        K = k*sum(Js)
        assert K <= 2+1e-12
        H = sum(Hs)
        probe = random_term((0,2))
        for suffix in [0, c//2]:
            coeff = conjugation_coefficients(Hs[suffix:],probe)
            for p in range(1,order+1):
                actual = norm(coeff[p])
                bound = K**p
                parity_error = norm(coeff[p].conj().T-(-1)**p*coeff[p])
                assert actual <= bound+1e-10
                assert parity_error <= 1e-9*max(1,actual)
                coefficient_rows.append(dict(c=c,weights=weight_mode,suffix=suffix,p=p,
                                             coefficient_norm=actual,bound=bound,parity_error=parity_error))
        for beta in [.7,4.]:
            logZ = logsumexp(-beta*np.linalg.eigvalsh(H))
            base_r = max(1,math.ceil(2*K*beta))
            for multiple in [1,2,4]:
                r = base_r*multiple
                delta = beta/r
                Q = np.eye(dim,dtype=complex)
                for Hj in Hs:
                    Q = expm(-delta*Hj/2)@Q
                P = herm(Q.conj().T@Q)
                ev,vec = np.linalg.eigh(P)
                assert min(ev)>0
                logP = herm((vec*np.log(ev))@vec.conj().T)
                step_error = norm(logP+delta*H)
                x = K*delta
                step_bound = 2*L*(np.arctanh(x)/K-delta)
                relaxed_bound = 2*L*K*K*delta**3/(3*(1-x*x))
                R = Q@expm(delta*H/2)
                relative_error = max(abs(np.log(np.linalg.eigvalsh(herm(R.conj().T@R)))))
                density_error = abs(logsumexp(r*np.log(ev))-logZ)/n
                density_bound = r*step_bound/n
                assert step_error<=step_bound+1e-10
                assert relative_error<=step_bound+1e-10
                assert step_bound<=relaxed_bound+1e-10
                assert density_error<=density_bound+1e-10
                step_rows.append(dict(c=c,weights=weight_mode,L=L,K=K,beta=beta,r=r,x=x,
                                      step_error=step_error,step_bound=step_bound,
                                      relaxed_bound=relaxed_bound,relative_error=float(relative_error),
                                      log_density_error=float(density_error),log_density_bound=float(density_bound)))

for name,rows in [("local_strength_coefficients.csv",coefficient_rows),("local_strength_steps.csv",step_rows)]:
    with (OUT/name).open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(status="PASS",seed=2026102918,coefficient_checks=len(coefficient_rows),
             step_checks=len(step_rows),largest_color_count=64,
             max_coefficient_ratio=max(x["coefficient_norm"]/x["bound"] for x in coefficient_rows),
             max_step_ratio=max(x["step_error"]/x["step_bound"] for x in step_rows),
             scope="Complex Hermitian high-color and arbitrary-weight small-matrix sanity checks; analytic proof remains governing.")
(OUT/"local_strength_checks_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))

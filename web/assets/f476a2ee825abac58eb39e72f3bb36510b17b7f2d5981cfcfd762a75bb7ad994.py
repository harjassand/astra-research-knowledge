#!/usr/bin/env python3
"""Finite matrix/convention checks. These do not certify the quantified theorem."""
from fractions import Fraction
from math import acos, exp, pi, sqrt
from pathlib import Path
import json
import numpy as np


def spin(j):
    d = int(2*j+1)
    z = np.diag(j-np.arange(d))
    plus = np.zeros((d,d), dtype=complex)
    for k in range(1,d):
        plus[k-1,k] = sqrt(k*(2*j-k+1))
    return (plus+plus.conj().T)/2, (plus-plus.conj().T)/(2j), z


def rotations(j, nangles=None, nnodes=None):
    _, y, z = spin(j)
    d = len(z)
    n = nangles or int(4*j+1)
    q = nnodes or d
    nodes, weights = np.polynomial.legendre.leggauss(q)
    evals, evecs = np.linalg.eigh(y)
    ans = []
    for x,w in zip(nodes,weights):
        theta = acos(float(x))
        uy = (evecs*np.exp(-1j*theta*evals)) @ evecs.conj().T
        for a in range(n):
            alpha = 2*pi*a/n
            u = np.exp(-1j*alpha*np.diag(z))[:,None]*uy
            v = np.array([sqrt(1-x*x)*np.cos(alpha),
                          sqrt(1-x*x)*np.sin(alpha), x])
            ans.append((u,float(w)/(2*n),v))
    return ans


def channel(j,q):
    d = int(2*j+1)
    f = np.maximum(1-np.arange(d)/q,0)
    s = float(f@f)
    kraus = []
    for u,w,_ in rotations(j):
        fu = (u*f)@u.conj().T
        kraus.append(sqrt(d*w/s)*fu)
    def phi(x):
        return sum((k@x@k.conj().T for k in kraus), np.zeros((d,d),complex))
    return f,s,kraus,phi


def energy(js,f):
    a = np.diag(f)
    return sum(np.linalg.norm(x@a-a@x,"fro")**2 for x in js)


def radius_exact(q,l):
    if l == 0:
        return Fraction(0)
    j = Fraction(l,2)
    z = sum(q**k for k in range(l+1))
    return sum((j-k)*q**k for k in range(l+1))/z/(j+1)


def run():
    rng = np.random.default_rng(20261008)
    max_tp = max_dipole = max_score = max_poly_slack = 0.
    matrix_count = scalar_count = score_count = rank_count = 0
    rows = []
    for j in (.5,1,1.5,2,3,4):
        js = spin(j)
        d = int(2*j+1)
        for q in range(1,min(4,d)):
            f,s,kraus,phi = channel(j,q)
            en = energy(js,f)
            formula = 3*d/(2*q+1)-1
            assert abs(en/s-formula) < 3e-12
            tp = np.linalg.norm(phi(np.eye(d))-np.eye(d),"fro")
            max_tp = max(max_tp,float(tp))
            assert tp < 4e-12
            lam = 1-en/(2*s*j*(j+1))
            dipole = np.linalg.norm(phi(js[2])-lam*js[2],"fro")
            max_dipole = max(max_dipole,float(dipole))
            assert dipole < 5e-12
            ss = js[2]/j
            for m in range(1,9):
                sm = np.linalg.matrix_power(ss,m)
                actual = np.sum(np.linalg.svd(phi(sm)-sm,compute_uv=False))
                bound = d*en/(2*s)*(m/(j*(j+1))+m*(m-1)/(3*j*j))
                assert actual <= bound+4e-12
                max_poly_slack = max(max_poly_slack,float(actual-bound))
            for beta in (.05,.25,.7,1.3):
                p = np.exp(beta*np.diag(js[2]))
                p /= p.sum()
                tau = np.diag(p)
                actual = .5*np.sum(np.linalg.svd(phi(tau)-tau,compute_uv=False))
                h = beta*j
                bound = en/(4*s*j*j)*(h+h*h/3)*exp(h)
                assert actual <= bound+4e-12
                rows.append(dict(j=j,Q=q,beta=beta,error=float(actual),bound=bound,
                                 labels=len(kraus),energy_over_s=float(en/s)))
                matrix_count += 1

    # Exact scalar monotonicity and complete-sector score dominance.
    for q in (Fraction(1,3),Fraction(1,2),Fraction(3,4),Fraction(7,8)):
        aa = [radius_exact(q,l) for l in range(42)]
        for l in range(1,41):
            assert aa[l] < aa[l+1]
            assert aa[l]/l > aa[l+1]/(l+1)
            scalar_count += 1
        for l in range(1,31):
            j = Fraction(l,2)
            for klen in range(1,31):
                k = Fraction(klen,2)
                transport = aa[l]**2/j-aa[l]*aa[klen]/max(j,k)
                assert transport >= 0
                scalar_count += 1

    # Direct prior quadrature checks the sign and d,j,k factors in (5.4).
    for j,k in ((1,.5),(1,2),(1.5,1.5),(2,1)):
        jij, kik = spin(j), spin(k)
        dj,dk = int(2*j+1),int(2*k+1)
        for rank in range(1,min(3,dj,dk)+1):
            a = ((rng.normal(size=(dk,rank))+1j*rng.normal(size=(dk,rank)))
                 @ (rng.normal(size=(rank,dj))+1j*rng.normal(size=(rank,dj))))
            a *= sqrt(dj)/np.linalg.norm(a,"fro")
            beta = .6
            pj = np.exp(beta*np.diag(jij[2])); pj /= pj.sum()
            pk = np.exp(beta*np.diag(kik[2])); pk /= pk.sum()
            aj = float(pj@np.diag(jij[2]))/(j+1)
            ak = float(pk@np.diag(kik[2]))/(k+1)
            h = sum(np.trace(a@x@a.conj().T@y).real for x,y in zip(jij,kik))/dj
            prediction = aj*ak*h/(j*k)-ak*ak/2
            actual = 0.
            for u,w,v in rotations(j,int(4*j+5),int(2*j+3)):
                tau = (u*pj)@u.conj().T
                fk = ak*sum(vv*x for vv,x in zip(v,kik))/k-ak*ak*np.eye(dk)/2
                actual += w*np.trace(a@tau@a.conj().T@fk).real
            residual = abs(actual-prediction)
            max_score = max(max_score,float(residual))
            assert residual < 6e-12
            score_count += 1

    # General unequal-spin rank-Q low-total-spin projection bound.
    for j,k in ((1,1),(1,2),(1.5,2.5),(3,3)):
        jj,kk = spin(j),spin(k)
        dj,dk = int(2*j+1),int(2*k+1)
        h = -sum(np.kron(x,y) for x,y in zip(jj,kk))
        evals,evecs = np.linalg.eigh(h)
        m,M = min(j,k),max(j,k)
        for cutoff in range(int(2*m)):
            delta = M-m
            ecut = cutoff*(2*delta+cutoff+1)/2
            mask = evals >= j*k+m-ecut-1e-9
            proj = evecs[:,mask]@evecs[:,mask].conj().T
            dim = (cutoff+1)*(2*delta+cutoff+1)
            assert abs(np.trace(proj).real-dim)<1e-10
            tensor = proj.reshape(dj,dk,dj,dk)
            margj = np.einsum('abcb->ac',tensor)
            margk = np.einsum('abad->bd',tensor)
            assert np.linalg.norm(margj-dim/dj*np.eye(dj))<1e-10
            assert np.linalg.norm(margk-dim/dk*np.eye(dk))<1e-10
            for rank in range(1,min(4,dj,dk)):
                for _ in range(10):
                    a = ((rng.normal(size=(dj,rank))+1j*rng.normal(size=(dj,rank)))
                         @ (rng.normal(size=(rank,dk))+1j*rng.normal(size=(rank,dk))))
                    v = a.reshape(-1); v /= np.linalg.norm(v)
                    mass = np.vdot(v,proj@v).real
                    bound = min(1.,rank*dim/(2*M+1))
                    assert mass <= bound+1e-11
                    rank_count += 1

    out = dict(status="FINITE-EVIDENCE",matrix_thermal_fixtures=matrix_count,
               exact_scalar_fixtures=scalar_count,choi_score_fixtures=score_count,
               random_rank_projector_fixtures=rank_count,
               max_unital_residual=max_tp,max_dipole_residual=max_dipole,
               max_choi_score_residual=max_score,
               maximum_polynomial_bound_violation=max_poly_slack,
               numpy_version=np.__version__,rows=rows,
               limitations="Small finite matrices and exact scalar fixtures; not formal proof, global rank optimization, gate synthesis, or novelty evidence.")
    path = Path(__file__).with_name("quantum_branch_checks.json")
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k != "rows"},indent=2))


if __name__ == "__main__":
    run()

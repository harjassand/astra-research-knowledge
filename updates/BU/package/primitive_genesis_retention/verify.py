#!/usr/bin/env python3
"""Finite checks for the retention note; not a proof assistant.

Requirements: Python >=3.10, numpy, sympy.
Run: python verify.py --output verification_receipt.json
No network access is used. All comparisons raise on failure, including under -O.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import platform
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any
import numpy as np
import sympy as sp

CHECKS: list[dict[str, Any]] = []

def require(ok: bool, name: str, **details: Any) -> None:
    if not ok:
        raise RuntimeError(f"Failed check: {name}; {details}")
    CHECKS.append({"name": name, "status": "PASS", **details})

def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def phase_partition_checks() -> None:
    # Exhaust all deterministic encoders of the q equally spaced circle points.
    # Permutation symmetry permits assigning the first point label 0.
    for q in range(2, 9):
        z = np.exp(2j * np.pi * np.arange(q) / q)
        for m in range(1, min(q, 4) + 1):
            best = 0.0
            count = 0
            for tail in itertools.product(range(m), repeat=q-1):
                sums = np.zeros(m, dtype=complex)
                for root, label in zip(z, (0,) + tail):
                    sums[label] += root
                best = max(best, float(np.abs(sums).sum() / q))
                count += 1
            a, r = divmod(q, m)
            predicted = ((m-r)*math.sin(a*math.pi/q)
                         + r*math.sin((a+1)*math.pi/q)) / (q*math.sin(math.pi/q))
            require(abs(best-predicted) < 3e-13,
                    f"finite circle partition q={q},m={m}",
                    kind="exhaustive finite enumeration with floating complex arithmetic",
                    encoders_enumerated=count, observed=best, predicted=predicted)

    # Midpoint quadrature on each exact nearest-neighbour sector, then powers.
    for m in (2, 3, 4, 7, 13):
        phases = 2*np.pi*np.arange(m)/m
        z = np.exp(1j*phases)
        eta = math.sin(math.pi/m)/(math.pi/m)
        A = eta*np.outer(z, z.conj())/m
        n = 4000
        offset = (np.arange(n)+0.5)/n*(2*np.pi/m)-np.pi/m
        B = np.empty((m, m), dtype=complex)
        for i in range(m):
            for j in range(m):
                theta = phases[j]-phases[i]+offset
                B[i, j] = np.exp(-1j*theta).mean()/m
        require(float(np.max(np.abs(B-A))) < 3e-8,
                f"circle transfer quadrature m={m}", kind="numerical diagnostic",
                maximum_entry_error=float(np.max(np.abs(B-A))))
        for t in (1, 2, 5, 20):
            actual = np.max(np.sum(np.abs(np.linalg.matrix_power(A,t)),axis=1))
            require(abs(actual-eta**t)<2e-13,
                    f"circle operator power m={m},t={t}",
                    kind="numerical diagnostic", actual=float(actual), predicted=eta**t)

def exact_signed_triangle() -> None:
    rt = sp.sqrt(3)
    E = sp.Matrix([[1, 0], [-sp.Rational(1,2), rt/2],
                   [-sp.Rational(1,2), -rt/2]])
    R = sp.Matrix([[sp.Rational(3,5),-sp.Rational(4,5)],
                   [sp.Rational(4,5),sp.Rational(3,5)]])
    def lift(g):
        return (sp.ones(3,3)+2*E*g.T*E.T)/3
    P = lift(R)
    require(P*sp.ones(3,1)==sp.ones(3,1), "signed triangle row sums",
            kind="exact symbolic algebra")
    require(sp.simplify(P*P-lift(R*R))==sp.zeros(3),
            "signed triangle composition", kind="exact symbolic algebra")
    N = lift(-sp.eye(2))
    require(N[0,0]==-sp.Rational(1,3) and N[0,1]==sp.Rational(2,3),
            "signed triangle negative entry", kind="exact symbolic algebra",
            first_row=[str(N[0,j]) for j in range(3)])
    x = sp.Matrix([sp.Rational(1,3), sp.Rational(1,5)])
    px=(sp.ones(3,1)+E*x)/3
    target=(sp.ones(3,1)+E*R*x)/3
    require(sp.simplify(P.T*px-target)==sp.zeros(3,1),
            "signed triangle reachable distribution", kind="exact symbolic algebra")

def exact_positive_square() -> None:
    vertices = [[F(s),F(t)] for s,t in itertools.product((-1,1), repeat=2)]
    alpha=F(1,2)
    rotations=[[[F(3,5),-F(4,5)],[F(4,5),F(3,5)]],
               [[F(5,13),F(12,13)],[-F(12,13),F(5,13)]],
               [[F(0),F(-1)],[F(1),F(0)]]]
    def lift(R):
        P=[]
        for v in vertices:
            y=[alpha*sum(R[k][l]*v[l] for l in range(2)) for k in range(2)]
            P.append([(1+w[0]*y[0])*(1+w[1]*y[1])/4 for w in vertices])
        return P
    for k,R in enumerate(rotations):
        P=lift(R)
        require(all(sum(row)==1 and min(row)>=0 for row in P),
                f"square lift positivity and row sums {k}",kind="exact rational arithmetic")
        actual=matmul(P,vertices)
        expected=[[alpha*sum(R[k][l]*v[l] for l in range(2)) for k in range(2)]
                  for v in vertices]
        require(actual==expected, f"square lift barycentres {k}", kind="exact rational arithmetic")
    x=[F(1,3),F(-1,4)]
    p=[[(1+v[0]*x[0])*(1+v[1]*x[1])/4 for v in vertices]]
    for t in range(1,31):
        R=rotations[(t-1)%len(rotations)]
        p=matmul(p,lift(R))
        x=[alpha*sum(R[k][l]*x[l] for l in range(2)) for k in range(2)]
        require(matmul(p,vertices)[0]==x, f"positive square sequential mean t={t}",
                kind="exact rational arithmetic")
        if t in (1,7,30):
            u=[F(2,3),F(1,5)]; delta=F(1,3)
            h=[[ (1+delta*sum(u[k]*v[k] for k in range(2)))/2] for v in vertices]
            predicted=(1+delta*sum(u[k]*x[k] for k in range(2)))/2
            require(matmul(p,h)[0][0]==predicted,
                    f"positive square output t={t}", kind="exact rational arithmetic")

def simplex_and_qubit() -> None:
    # A rational tetrahedron of radius sqrt(3), with inner ball radius 1/sqrt(3).
    # Symbolic rescaling gives the regular simplex directions and vertices 3e_i.
    E=sp.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/sp.sqrt(3)
    x=sp.Matrix(sp.symbols('x1:4', real=True))
    u=sp.Matrix(sp.symbols('u1:4', real=True))
    delta=sp.symbols('delta', real=True)
    p=(sp.ones(4,1)+E*x)/4
    h=(sp.ones(4,1)+3*delta*E*u)/2
    require(sp.simplify((p.T*h)[0]-(1+delta*x.dot(u))/2)==0,
            "static four-state tetrahedron", kind="exact symbolic algebra")
    sx=sp.Matrix([[0,1],[1,0]]); sy=sp.Matrix([[0,-sp.I],[sp.I,0]])
    sz=sp.diag(1,-1); sig=[sx,sy,sz]
    rho=(sp.eye(2)+sum((x[k]*sig[k] for k in range(3)),sp.zeros(2)))/2
    effect=(sp.eye(2)+delta*sum((u[k]*sig[k] for k in range(3)),sp.zeros(2)))/2
    require(sp.simplify(sp.trace(rho*effect)-(1+delta*x.dot(u))/2)==0,
            "qubit Born identity", kind="exact symbolic algebra")
    for d in range(2,8):
        K=sp.ones(d+1,d+1)/2
        for k in range(1,d+1): K[k,k]+=delta/2
        require(sp.factor(K.det()-delta**d/2**(d+1))==0,
                f"static rank minor d={d}",kind="exact symbolic algebra")

def random_primal_checks() -> None:
    # The 2D finite group is a finite analogue, not a proof about Haar measure.
    rng=np.random.default_rng(731902)
    for m,q in [(2,11),(3,17),(4,23),(7,29)]:
        theta=2*np.pi*np.arange(q)/q
        R=np.stack([np.stack([np.cos(theta),-np.sin(theta)],axis=-1),
                    np.stack([np.sin(theta),np.cos(theta)],axis=-1)],axis=1)
        a,r=divmod(q,m)
        kappa=((m-r)*np.sin(a*np.pi/q)+r*np.sin((a+1)*np.pi/q))/(q*np.sin(np.pi/q))
        for run in range(20):
            b=rng.normal(size=(m,2)); b/=np.linalg.norm(b,axis=1).sum()
            raw=rng.uniform(size=(q,m,m)); P=raw/raw.sum(axis=2,keepdims=True)
            next_b=np.einsum('qkl,il,qij->jk',R,b,P)/q
            ratio=np.linalg.norm(next_b,axis=1).sum()
            require(ratio<=kappa+1e-12,
                    f"finite-group primal contraction m={m},q={q},run={run}",
                    kind="seeded numerical diagnostic", ratio=float(ratio), upper=float(kappa))

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('verification_receipt.json'))
    args=parser.parse_args()
    phase_partition_checks(); exact_signed_triangle(); exact_positive_square()
    simplex_and_qubit(); random_primal_checks()
    receipt={"status":"PASS", "check_count":len(CHECKS),
      "scope":"Finite exact algebra, finite enumeration and floating diagnostics. Not a formal proof, external audit or priority certification.",
      "python":platform.python_version(), "numpy":np.__version__, "sympy":sp.__version__,
      "optimization_flag":sys.flags.optimize, "checks":CHECKS}
    args.output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:receipt[k] for k in ('status','check_count','optimization_flag','scope')},indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())

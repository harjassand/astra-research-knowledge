#!/usr/bin/env python3
"""Exact finite SAT-to-word checks; no solver-hardness benchmark or novelty claim."""
from itertools import product
from pathlib import Path
import json
import sympy as sp


def automaton(clauses,h):
    m=len(clauses);N=2*m*(h+1)
    index=lambda j,k,s:2*(j*(h+1)+k)+s
    mats=[sp.zeros(N),sp.zeros(N)]
    b=sp.zeros(N,1);c=sp.zeros(N,1)
    for j,clause in enumerate(clauses):
        b[index(j,0,0)]=sp.Rational(1,m);c[index(j,h,1)]=1
        for k in range(h+1):
            for s in range(2):
                for a in range(2):
                    sat=s or ((k+1 if a else -(k+1)) in clause)
                    target=index(j,min(h,k+1),s if k==h else int(sat))
                    mats[a][target,index(j,k,s)]=1
    return mats,b,c


def run():
    cases=[([[1,1,1],[-1,-1,-1]],2),
           ([[1,2,2],[-1,2,2]],2),
           ([[1,-2,3],[-1,2,-3],[1,2,-3]],3)]
    rows=[]
    for clauses,h in cases:
        P,b,c=automaton(clauses,h);m=len(clauses);N=len(b)
        q=1-sp.Rational(1,2*h);tau=q**h*(1-sp.Rational(1,2*m));gamma=q**h/(2*m)
        D=sp.diag(*[sp.Rational(i+1,2*(N+1)) for i in range(N)])
        X=sp.ones(N)/(2*N)
        rho=q**h/(32*m*h)
        A=[(1-rho)*q*P[0]+rho*D,(1-rho)*q*P[1]+rho*X]
        sat=False;minimum_margin=None
        for word in product(range(2),repeat=h):
            score=sum(any(bool(word[abs(l)-1])==(l>0) for l in clause) for clause in clauses)
            xp=b;xa=b
            for a in word:xp=q*P[a]*xp;xa=A[a]*xa
            truth=(c.T*xp)[0];pert=(c.T*xa)[0]
            assert truth==q**h*sp.Rational(score,m)
            assert abs(pert-truth)<=2*h*rho
            assert bool(pert>tau)==(score==m)
            minimum_margin=abs(pert-tau) if minimum_margin is None else min(minimum_margin,abs(pert-tau))
            sat=sat or score==m
        assert minimum_margin>=3*gamma/4
        rows.append({'clauses':clauses,'variables':h,'states':N,'satisfiable':sat,
                     'words_checked':2**h,'threshold':str(tau),'unperturbed_gap':str(gamma),
                     'perturbation_parameter':str(rho),'minimum_perturbed_margin':str(minimum_margin)})
    return {'scope':'Exact reduction/gap checks. Full-algebra generic perturbation is proved separately; this script does not claim to verify its determinant for every example.','cases':rows}


if __name__=='__main__':
    out=run();Path('barrier_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

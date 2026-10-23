"""Exact matrix identities for sharp normal-CTMC flat-mode witnesses.

Exponentials and transcendental bounds are proved symbolically in the audit.
Floating values here are diagnostics only, not acceptance decisions.
"""
from fractions import Fraction as F
from math import exp, pi
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent


def require(value,message):
    if not value:
        raise ValueError(message)


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a,b):
    return [[sum(x*y for x,y in zip(row,column)) for column in zip(*b)] for row in a]


def matvec(a,z):
    return [sum(x*y for x,y in zip(row,z)) for row in a]


def check_cycle(kplus,kminus):
    n=4
    cycle=[[F(i==(j+1)%n) for j in range(n)] for i in range(n)]
    reverse=transpose(cycle)
    identity=[[F(i==j) for j in range(n)] for i in range(n)]
    s,d=kplus+kminus,kplus-kminus
    require(s>0 and d!=0,'nonzero circulation')
    q=[[kplus*cycle[i][j]+kminus*reverse[i][j]-s*identity[i][j]
        for j in range(n)] for i in range(n)]
    qt=transpose(q)
    require(all(q[i][j]>=0 for i in range(n) for j in range(n) if i!=j),
            'Markov off diagonals')
    require(all(sum(row)==0 for row in q),'zero row sums')
    require(all(sum(row)==0 for row in qt),'zero column sums')
    require(multiply(q,qt)==multiply(qt,q),'normality')
    lap=[[-(q[i][j]+qt[i][j])/2 for j in range(n)] for i in range(n)]
    skew=[[(q[i][j]-qt[i][j])/2 for j in range(n)] for i in range(n)]
    z=[F(1),F(1),F(-1),F(-1)]
    cz=matvec(cycle,z)
    require(matvec(cycle,cz)==[-x for x in z],'quarter-turn mode')
    require(matvec(reverse,z)==[-x for x in cz],'opposite quarter turn')
    require(matvec(lap,z)==[s*x for x in z],'scalar symmetric damping')
    require(matvec(skew,z)==[d*x for x in cz],'scalar skew rotation')
    rho=abs(d)/s
    for i in range(n):
        cross=[j for j in range(n) if z[i]!=z[j]]
        require(sum(-lap[i][j] for j in cross)==s/2,'cross conductance per vertex')
        require(abs(matvec(skew,z)[i])==rho*s,'flat maximum-principle saturation')
        for j in range(n):
            if i!=j:
                require(abs(skew[i][j])<=rho*(-lap[i][j]),'affinity envelope')
    return dict(kplus=str(kplus),kminus=str(kminus),rho=str(rho),
                z=[str(x) for x in z],Cz=[str(x) for x in cz],
                exact_return_time='pi/'+str(abs(d)),
                exact_alpha='exp(-pi*'+str(s/abs(d))+')',
                alpha_float=exp(-pi*float(s/abs(d))),
                flip_probability_float=(1+exp(-pi*float(s/abs(d))))/2,
                all_matrix_checks_exact=True)


if __name__=='__main__':
    cases=[check_cycle(F(1),F(0)),check_cycle(F(3),F(1)),
           check_cycle(F(2),F(1)),check_cycle(F(1),F(3))]
    out=dict(cases=cases,arithmetic='Exact Fraction matrix identities; exponentials only diagnostic floats',
             scope='Four-state saturation witnesses and separate written universal proof; no novelty or hardware claim.')
    (ROOT/'normal_autonomous_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

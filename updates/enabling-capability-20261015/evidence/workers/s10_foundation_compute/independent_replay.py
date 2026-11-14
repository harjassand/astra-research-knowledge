"""Independent exact implementation checks; finite checks are not the proof.

The universal proof is rank2_blocks.py plus the phase-template argument.
This script uses partial traces rather than that script's entry formula.
"""
from itertools import product
from pathlib import Path
import json
import sympy as sp
from rank2_blocks import blocks,t


def phi(X,p,q):
    ta=sp.zeros(q);tb=sp.zeros(p)
    for a,b,c,d in product(range(p),range(q),range(p),range(q)):
        if a==c:ta[b,d]+=X[a*q+b,c*q+d]
        if b==d:tb[a,c]+=X[a*q+b,c*q+d]
    return sp.trace(X)*sp.eye(p*q)-(sp.kronecker_product(tb,sp.eye(q))+sp.kronecker_product(sp.eye(p),ta))/2+X/4


def direct(u,p,q):
    n=p*q;e=sp.eye(n);A=phi(u*u.H,p,q);Ai=A.inv()
    L=[phi(e[:,j]*u.H,p,q) for j in range(n)]
    C=sp.zeros(n*n);S=sp.zeros(n*n)
    for a,b in product(range(n),repeat=2):
        C[b*n:(b+1)*n,a*n:(a+1)*n]=phi(e[:,a]*e[:,b].H,p,q)
        S[b*n:(b+1)*n,a*n:(a+1)*n]=L[a]*Ai*L[b].H
    return C,S


def main():
    out={'status':'FINITE_EXACT_IMPLEMENTATION_REPLAY_NOT_UNIVERSAL_PROOF','checks':[]}
    p=q=3;n=p*q
    bb,total,A=blocks(p,q)
    for tau in [sp.Rational(0),sp.Rational(1,3),sp.Integer(1),sp.Integer(2)]:
        u=sp.zeros(n,1);u[0]=1;u[q+1]=tau
        C,S=direct(u,p,q)
        # Rebuild all phase blocks with their stored multiplicity ignored:
        # representative entries are cross-checked, and cross-phase zeros are
        # independently checked for the full exact matrices below.
        representative_ok=True
        for b in bb:
            indices=[(q*i[0]+i[1])*n+(q*r[0]+r[1]) for i,r in b['labels']]
            representative_ok &= C.extract(indices,indices)==b['C']
            representative_ok &= S.extract(indices,indices)==b['S'].subs(t,tau)
        from rank2_blocks import phase_weight
        weights=[phase_weight(a,b,c,d,p,q) for a,b,c,d in product(range(p),range(q),range(p),range(q))]
        cross_zero=all(C[i,j]==0 and S[i,j]==0 for i,j in product(range(n*n),repeat=2) if weights[i]!=weights[j])
        out['checks'].append({'dims':[p,q],'t':str(tau),'independent_phi_entries_agree':bool(representative_ok),
                              'cross_phase_entries_exactly_zero':cross_zero})
    # Rational complex local unitaries; every check is exact Gaussian rational.
    p=2;q=3;n=p*q;tau=sp.Rational(2,3)
    UA=sp.Matrix([[sp.Rational(3,5),sp.Rational(4,5)*sp.I],[sp.Rational(4,5)*sp.I,sp.Rational(3,5)]])
    UB=sp.Matrix([[sp.Rational(3,5),sp.Rational(4,5),0],[-sp.Rational(4,5),sp.Rational(3,5),0],[0,0,sp.I]])
    U=sp.kronecker_product(UA,UB);assert U.H*U==sp.eye(n)
    u=sp.zeros(n,1);u[0]=1;u[q+1]=tau
    C,S=direct(u,p,q);Cu,Su=direct(U*u,p,q);UU=sp.kronecker_product(U,U)
    out['checks'].append({'dims':[p,q],'t':str(tau),
                          'exact_complex_covariance_C':(Cu-UU*C*UU.H).applyfunc(sp.simplify)==sp.zeros(n*n),
                          'exact_complex_covariance_S':(Su-UU*S*UU.H).applyfunc(sp.simplify)==sp.zeros(n*n)})
    assert all(all(v is True for k,v in r.items() if k not in ['dims','t']) for r in out['checks'])
    Path(__file__).with_name('independent_replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()

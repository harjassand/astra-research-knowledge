#!/usr/bin/env python3
"""Exact single-case physical nonreversible entropy/root Hessian obstruction.

No scan, floating arithmetic, numerical logarithm, or spectral approximation.
All logarithmic coefficients are rational multiples of log 2. The proved
inequality log 2<7/10 certifies the strict coefficient-2 Hessian gap.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys


def zero(n=4):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def diag(xs):
    out=zero(len(xs))
    for i,x in enumerate(xs): out[i][i]=F(x)
    return out


def add(a,b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def scale(a,r):
    return [[F(r)*x for x in ar] for ar in a]


def mul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F())
             for j in range(len(b[0]))] for i in range(len(a))]


def adj(a): return [list(x) for x in zip(*a)]
def tr(a): return sum((a[i][i] for i in range(len(a))),F())


def run():
    # This is one fixed case chosen from the exact rank-one phase mechanism.
    kvals=[0,18,20,22]
    sv=[F(2)**k for k in kvals]
    sqrt_sv=[F(2)**(k//2) for k in kvals]
    S=diag(sv)
    Z=sum((s*s for s in sv),F())
    sigma=diag([s*s/Z for s in sv])
    phase=[1,-1,1]
    B=zero()
    for i in range(1,4):
        for j in range(1,4): B[i][j]=F(phase[i-1])
    assert B!=adj(B)
    Y=mul(mul(adj(B),S),B)
    ZZ=mul(mul(B,S),adj(B))
    D=zero()
    for i in range(4):
        for j in range(4):
            if i==j:
                assert Y[i][i]==ZZ[i][i]
                D[i][i]=Y[i][i]/sv[i]
            else:
                D[i][j]=2*(sv[i]*Y[i][j]-sv[j]*ZZ[i][j])/(sv[i]**2-sv[j]**2)
    V=scale(add(D,adj(D)),F(1,2))

    def H(X):
        return add(scale(add(mul(adj(D),X),mul(X,D)),F(1,2)),
                   scale(mul(mul(adj(B),X),B),-1))

    def Hstar(X):
        return add(scale(add(mul(D,X),mul(X,adj(D))),F(1,2)),
                   scale(mul(mul(B,X),adj(B)),-1))

    assert H(S)==zero() and Hstar(S)==zero()
    assert any(D[i][j]!=D[j][i] for i in range(4) for j in range(4))
    rootS=diag(sqrt_sv)
    invrootS=diag([1/x for x in sqrt_sv])
    K=mul(mul(rootS,B),invrootS)
    C=mul(mul(rootS,D),invrootS)
    assert add(C,adj(C))==scale(mul(adj(K),K),2)

    def Lstar(X):
        return add(scale(add(mul(C,X),mul(X,adj(C))),F(1,2)),
                   scale(mul(mul(K,X),adj(K)),-1))

    assert Lstar(sigma)==zero()
    Q=zero()
    hv=[1,2,1]
    for i in range(1,4): Q[0][i]=Q[i][0]=F(hv[i-1])*sqrt_sv[i]
    delta_rho=scale(add(mul(S,Q),mul(Q,S)),1/Z)
    # Dlog_sigma(delta_rho), with log2 factored out, only has center-leaf entries.
    logderivative=zero()
    for i in range(1,4):
        logderivative[0][i]=logderivative[i][0]=2*kvals[i]*Q[0][i]/(sv[i]-1)
    Jcoeff=tr(mul(Lstar(delta_rho),logderivative))
    Ecoeff=tr(mul(Q,scale(add(H(Q),Hstar(Q)),F(1,2))))/Z
    A0=sum(sv[1:],F())
    expected_J=F(316301432858573464,16131331232096465)
    assert Jcoeff*Z/A0==expected_J
    assert Ecoeff*Z/A0==F(118,17)
    assert Jcoeff>0 and Ecoeff>0

    # log2=2*atanh(1/3); four terms plus an exact geometric tail.
    log2_lower=2*sum((F(1,3)**(2*n+1)/F(2*n+1) for n in range(4)),F())
    log2_upper=log2_lower+2*F(1,3)**9/(9*(1-F(1,3)**2))
    assert log2_upper<F(7,10)
    gap_upper=Jcoeff*F(7,10)-2*Ecoeff
    assert gap_upper<0
    return {
        'status':'PASS',
        'dimension':4,
        'raw_s':[str(x) for x in sv],
        'normalization_Z':str(Z),
        'noise_B':[[str(x) for x in row] for row in B],
        'transported_D':[[str(x) for x in row] for row in D],
        'physical_K':[[str(x) for x in row] for row in K],
        'physical_C':[[str(x) for x in row] for row in C],
        'Q_root_coherence':[[str(x) for x in row] for row in Q],
        'physical_CPTP_stationary_legality':True,
        'both_Hs_Hstars_zero':True,
        'non_HS_selfadjoint':True,
        'physical_J2_over_A0_log2_per_Z':str(Jcoeff*Z/A0),
        'root_E2_over_A0_per_Z':str(Ecoeff*Z/A0),
        'log2_upper_bound':str(log2_upper),
        'J2_minus_2E2_upper_bound':str(gap_upper),
        'ratio_upper_bound':str(Jcoeff*F(7,10)/Ecoeff),
        'scope':'Exact legal finite generator and negative physical coefficient-2 Hessian; nonlinear counterexamples exist for sufficiently small positive rational perturbation. A particular nonlinear epsilon is not certified here.',
        'scan_count':0,
        'arithmetic':'Python stdlib Fraction only'
    }


def main():
    path=Path(__file__).resolve().parent/'FIXED_DIM4_REPLAY.json'
    result=run()
    if sys.argv[1:]==['--verify']:
        assert json.loads(path.read_text())==result
        print('PASS: frozen fixed dimension4 replay exactly reproduced.')
    elif not sys.argv[1:]:
        with path.open('x') as f:
            json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
        print('PASS: wrote exact fixed dimension4 replay.')
    else:raise SystemExit('Usage: verify_fixed_dim4.py [--verify]')
    print('sha256',hashlib.sha256(path.read_bytes()).hexdigest())


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Exact rational generator tests and numerical asymptotic convergence.
Python 3.11+ standard library. These finite checks are not a mathematical proof.
"""
from fractions import Fraction
from math import exp, lgamma, log, prod

def falling(n, ell):
    return prod(range(n-ell+1,n+1))

def path_data(ell,K,eps):
    eps=Fraction(eps)
    P=Fraction(1); KL=Fraction(0)
    for n in range(ell,K):
        lam=falling(n,ell)
        mu=eps*falling(n,ell+1)
        P*=Fraction(lam,1)/(lam+mu)
        KL+=mu/lam
    return 1-P,KL,P

def firstpass_recurrence(ell,K,eps):
    eps=Fraction(eps)
    S=Fraction(1); total=Fraction(0)
    for n in range(ell,K):
        if n>ell:S=1+eps*n*S
        total+=S/falling(n,ell)
    return total

def solve_backward_generator(ell,K,eps):
    """Independent Gaussian elimination on killed generator, rational arithmetic."""
    eps=Fraction(eps); size=K-ell
    A=[[Fraction(0) for _ in range(size+1)] for _ in range(size)]
    for i,n in enumerate(range(ell,K)):
        lam=Fraction(falling(n,ell))
        mu=eps*falling(n,ell+1)
        A[i][i]=lam+mu
        if i>0:A[i][i-1]=-mu
        if i+1<size:A[i][i+1]=-lam
        A[i][size]=1
    for i in range(size):
        piv=next(k for k in range(i,size) if A[k][i])
        A[i],A[piv]=A[piv],A[i]
        z=A[i][i]
        A[i]=[v/z for v in A[i]]
        for j in range(size):
            if j==i:continue
            z=A[j][i]
            A[j]=[a-z*b for a,b in zip(A[j],A[i])]
    return A[0][-1]

def mean_float(ell,K,eps):
    S=1.; total=0.; last=0.
    for n in range(ell,K):
        if n>ell:S=1+eps*n*S
        last=S/falling(n,ell);total+=last
    return total

def run():
    checks=0
    for ell in [2,3,4]:
        for K in range(ell+2,ell+7):
            for eps in [Fraction(1,10),Fraction(3,7)]:
                assert firstpass_recurrence(ell,K,eps)==solve_backward_generator(ell,K,eps)
                checks+=1
                tv,kl,Q=path_data(ell,K,eps)
                L=K-ell
                assert kl==eps*L*(L-1)/2
                assert Q==prod(Fraction(1,1)/(1+eps*j) for j in range(L))
                checks+=1
                z=1/eps
                for n in range(ell,K):
                    mu=eps*falling(n+1,ell+1)
                    assert Fraction(falling(n,ell),mu)==z/Fraction(n+1)
                    checks+=1
    print("EXACT rational generator, first passage, TV/KL, detailed balance:",checks,"PASS")
    print("ell=2,K=6,eps=1/10:",path_data(2,6,Fraction(1,10)))
    gamma=0.5772156649015328606
    print("ell=2 alpha=1/2 second-order constant should converge to",gamma-3)
    for eps in [0.02,0.01,0.005,0.002,0.001,0.0002]:
        K=round(0.5/eps)
        m=mean_float(2,K,eps)
        print(eps,m,(m-1)/eps-log(1/eps))
    print("ell>=3 first-order coefficients:")
    for ell in [3,4,5]:
        pure=1/((ell-1)*falling(ell-1,ell-1))
        goal=1/((ell-2)*falling(ell-1,ell-1))
        for eps in [0.01,0.002,0.0005]:
            print(ell,eps,(mean_float(ell,round(.5/eps),eps)-pure)/eps,goal)
    alpha=1.5
    print("alpha>1 last-term ratio should approach",alpha/(alpha-1))
    for eps in [0.02,0.005,0.002,0.001]:
        K=round(alpha/eps); z=1/eps;n=K-1
        last_asympt_log=z-n*log(z)+lgamma(n-2+1)
        val=mean_float(2,K,eps)
        print(eps,eps*log(val),val/exp(last_asympt_log))
    print("Rate I(alpha)",alpha*log(alpha)-alpha+1)
    print("ALL CHECKS PASSED")

if __name__=="__main__":
    run()

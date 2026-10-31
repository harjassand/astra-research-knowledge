#!/usr/bin/env python3
"""Exact quadratic leakage statistics and elementary confidence inversion."""
from pathlib import Path
import hashlib
import itertools
import json
import math
import sys
import sympy as s

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'robust_operator_reuse_20261031'/'finite_observation'))
from robust_replay import sqrt_up
R=s.Rational


def median_repetitions(delta,q=R(1,16)):
    delta=R(delta);q=R(q)
    if not 0<delta<1 or not 0<q<R(1,2):raise ValueError('confidence')
    k=1
    while sum(math.comb(k,j)*q**j*(1-q)**(k-j) for j in range((k+1)//2,k+1))>delta:k+=2
    return k


def upper_squared(stat,a,b,q=R(1,16)):
    stat=R(stat);a=R(a);b=R(b);q=R(q)
    if a<0 or b<0 or not 0<q<1:raise ValueError('variance envelope')
    x=max(R(0),stat);aa=a/q
    return x+aa/2+sqrt_up(aa*x+aa*aa/4+b/q,bits=40)


def partition_check(parts,n):
    if any(not p for p in parts) or sorted(i for p in parts for i in p)!=list(range(n)):
        raise ValueError('partition')


def outgoing_stat(counts,parts):
    n=len(counts);partition_check(parts,n)
    if any(type(x) is not int or x<0 for x in counts):raise ValueError('counts')
    N=sum(counts)
    if N<2:raise ValueError('at least two samples')
    val=R(sum(x*x for x in counts)-N)
    for part in parts:
        c=sum(counts[i] for i in part)
        val-=R(c*c-c,len(part))
    return R(n,N*(N-1))*val


def incoming_stat(left,right,parts):
    n=len(left);r=len(parts);partition_check(parts,n)
    if len(right)!=n or any(len(x)!=r for x in left+right):raise ValueError('shape')
    if any(type(x) is not int or x<0 for row in left+right for x in row):raise ValueError('counts')
    N=sum(left[0])
    if N<1 or any(sum(row)!=N for row in left+right):raise ValueError('equal fixed row sample counts')
    val=R(0)
    for g,dest in enumerate(parts):
        v=R(sum(left[i][g]*right[i][g] for i in range(n)))
        for src in parts:
            v-=R(sum(left[i][g] for i in src)*sum(right[i][g] for i in src),len(src))
        val+=v/len(dest)
    return val/(N*N)


def run_checks():
    checks=0
    def check(ok):
        nonlocal checks
        assert ok;checks+=1
    outgoing=[]
    for probs,parts in (([R(1,3)]*3,[[0],[1,2]]),
                        ([R(1,2),R(1,3),R(1,6)],[[0,1],[2]]),
                        ([R(1,10),R(2,10),R(3,10),R(4,10)],[[0,1],[2,3]])):
        n=len(probs);p=s.Matrix(probs);P=s.zeros(n)
        for part in parts:
            for i in part:
                for j in part:P[i,j]=R(1,len(part))
        Q=s.eye(n)-P;mu=Q*p;cov=Q*s.diag(*probs)*Q-mu*mu.T
        v=n*(mu.T*mu)[0];kap=n*max(probs)
        for N in (2,3):
            mean=R(0);second=R(0)
            for seq in itertools.product(range(n),repeat=N):
                prob=s.prod(probs[j] for j in seq);counts=[seq.count(i) for i in range(n)]
                value=outgoing_stat(counts,parts);mean+=prob*value;second+=prob*value*value
            variance=second-mean*mean
            exact=R(4*n*n,N)*(mu.T*cov*mu)[0]+R(2*n*n,N*(N-1))*(cov*cov).trace()
            bound=4*kap*v/N+R(2)*kap*n/(N*(N-1))
            check(mean==v);check(variance==exact);check(variance<=bound)
            outgoing.append({'n':n,'N':N,'v':str(v),'variance':str(variance),'variance_upper':str(bound)})
    # Incoming split statistic, exhaustive two independent one-sample halves.
    n=4;parts=[[0,1],[2,3]];r=2;N=1
    probs=[[R(1,3),R(2,3)],[R(2,5),R(3,5)],[R(3,4),R(1,4)],[R(1,4),R(3,4)]]
    P=s.zeros(n)
    for part in parts:
        for i in part:
            for j in part:P[i,j]=R(1,len(part))
    Q=s.eye(n)-P;M=s.Matrix(probs);v=R(2,n)*(M.T*Q*M).trace()
    mean=R(0);second=R(0)
    for seq in itertools.product(range(r),repeat=2*n):
        prob=s.prod(probs[i][seq[i]]*probs[i][seq[n+i]] for i in range(n))
        left=[[int(seq[i]==g) for g in range(r)] for i in range(n)]
        right=[[int(seq[n+i]==g) for g in range(r)] for i in range(n)]
        value=incoming_stat(left,right,parts);mean+=prob*value;second+=prob*value*value
    variance=second-mean*mean;sigma=R(2);T=R(2*n)
    bound=2*sigma*v/(n*N)+sigma*T/(n*n*N*N)
    check(mean==v);check(variance<=bound)
    # Exact linear/bilinear variance decomposition without irrational features.
    covs=[2*(s.diag(*p)-s.Matrix(p)*s.Matrix(p).T) for p in probs]
    cov=s.diag(*covs);Qbig=s.kronecker_product(Q,s.eye(r));QM=Q*M
    linear=R(4,n*n)*sum((QM.row(i)*covs[i]*QM.row(i).T)[0] for i in range(n))
    bilinear=(Qbig*cov*Qbig*cov).trace()/(n*n)
    check(variance==linear+bilinear)
    check(outgoing_stat([1,1,1,1],parts)<0)
    check(upper_squared(R(-2),R(1),R(1))>=0)
    # Test the inversion wherever its defining one-sided deviation event holds.
    for iv in range(21):
        vv=R(iv,10)
        for iss in range(-10,31):
            ss=R(iss,10);a=R(1,7);b=R(1,13);q=R(1,16)
            if vv<=ss or (vv-ss)**2<=(a*vv+b)/q:
                check(vv<=upper_squared(ss,a,b,q))
    k=median_repetitions(R(1,100000));q=R(1,16)
    tail=sum(math.comb(k,j)*q**j*(1-q)**(k-j) for j in range((k+1)//2,k+1))
    check(tail<=R(1,100000))
    return {'checks':checks,'status':'PASS','outgoing_cases':outgoing,
            'incoming_case':{'v':str(v),'variance':str(variance),'variance_upper':str(bound)},
            'median_example':{'delta':'1/100000','base_failure':'1/16','repetitions':k,'tail':str(tail)},
            'scope':'Exact finite variance/statistic checks, not independent review or empirical proof of coverage.',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    out=run_checks();(ROOT/'quadratic_leakage_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

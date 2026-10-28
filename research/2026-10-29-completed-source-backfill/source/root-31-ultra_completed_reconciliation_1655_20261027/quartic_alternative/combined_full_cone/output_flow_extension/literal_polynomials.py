# Prefix snapshot of the frozen core verifier; no executable main.
"""Independent literal common separator and strict ROC replay; stdlib only."""
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr,combinations
from pathlib import Path
import json,hashlib,time,argparse
N=10
def clean(p):return {e:c for e,c in p.items() if c}
def add(*ps):
    z={}
    for p in ps:
        for e,c in p.items():z[e]=z.get(e,F(0))+c
    return clean(z)
def scale(p,c):return clean({e:c*v for e,v in p.items()})
def mul(p,q):
    z={}
    for e,c in p.items():
        for f,d in q.items():
            g=tuple(i+j for i,j in zip(e,f));z[g]=z.get(g,F(0))+c*d
    return clean(z)
def product(ps):
    p={(0,)*N:F(1)}
    for q in ps:p=mul(p,q)
    return p
def var(j):
    e=[0]*N;e[j]=1;return {tuple(e):F(1)}
def diff(p,j):
    z={}
    for e,c in p.items():
        if e[j]:
            f=list(e);f[j]-=1;z[tuple(f)]=c*e[j]
    return z
def invariants(a):
    aa,b,c,d=a
    return add(mul(aa,aa),mul(c,c)),add(mul(b,b),mul(d,d)),add(mul(aa,b),mul(c,d)),add(mul(aa,d),scale(mul(b,c),-1))
def bases(a):
    u,v,w,q=invariants(a)
    return [mul(u,u),mul(v,v),mul(u,v),mul(w,w),mul(u,w),mul(v,w),mul(q,u),mul(q,v),mul(q,w)]
def shifted(p,values):
    z={}
    for e,c in p.items():z=add(z,scale(product(values[i] for i in range(4) for j in range(e[i])),c))
    return z
def positive_matrix(A,pivots):
    """Schur complement elimination, then independent full reconstruction."""
    n=len(A);W=[row.copy() for row in A];L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
    assert all(A[i][j]==A[j][i] for i in range(n) for j in range(n))
    for k in range(n):
        d=W[k][k];assert d>0,(k,d);D.append(d)
        for i in range(k+1,n):L[i][k]=W[i][k]/d
        for i in range(k+1,n):
            for j in range(i,n):W[i][j]=W[j][i]=W[i][j]-W[i][k]*W[j][k]/d
    assert D==list(map(F,pivots))
    assert all(A[i][j]==sum(L[i][k]*D[k]*L[j][k] for k in range(n)) for i in range(n) for j in range(n))
    return D
def coefficient(p,exponent):return p.get(tuple(exponent),F(0))
def quadratic_matrix(p):
    out=[]
    for i in range(4):
        row=[]
        for j in range(4):
            e=[0]*N;e[i]+=1;e[j]+=1;row.append(coefficient(p,e)/(1 if i==j else 2))
        out.append(row)
    return out
def acoustic_matrix(f):
    aa=quadratic_matrix(diff(diff(f,0),0));ab=quadratic_matrix(diff(diff(f,0),1));bb=quadratic_matrix(diff(diff(f,1),1))
    return [[(aa if i<4 and j<4 else bb if i>=4 and j>=4 else ab)[i%4][j%4] for j in range(8)] for i in range(8)]



"""Exact rational certificate: N=3 thermal reentrant PPT->NPT->PPT.
Rational uniformization, integer witness, rational Poisson tail bound.
"""
from fractions import Fraction as F
from math import factorial
import sympy as sp

N=3; nu=F(3,20); t=F(5,2); Lambda=F(6); mu=Lambda*t; K=90
ids={k:[i for i in range(1<<N) if i.bit_count()==k] for k in range(N+1)}

def profile_rational(M, stationary=False):
    if stationary:
        q=nu/(nu+1)
        z=sum(q**i for i in range(M+1))
        return [q**i/z for i in range(M+1)]
    Q=[[F(0) for _ in range(M+1)] for _ in range(M+1)]
    for i in range(M+1):
        down=(nu+1)*i*(M-i+1)
        up=nu*(M-i)*(i+1)
        Q[i][i]-=down+up
        if i>0:Q[i-1][i]+=down
        if i<M:Q[i+1][i]+=up
    P=[[(F(1) if i==j else F(0))+Q[i][j]/Lambda for j in range(M+1)] for i in range(M+1)]
    assert all(x>=0 for row in P for x in row)
    assert all(sum(P[i][j] for i in range(M+1))==1 for j in range(M+1))
    v=[F(1,M+1)]*(M+1)
    accum=[F(0)]*(M+1)
    coef=F(1)
    for k in range(K+1):
        for i in range(M+1):accum[i]+=coef*v[i]
        v=[sum(P[i][j]*v[j] for j in range(M+1)) for i in range(M+1)]
        coef=coef*mu/(k+1)
    return accum


def rho_mat(stationary=False):
    pj3=profile_rational(3,stationary=stationary)
    pj1=profile_rational(1,stationary=stationary)
    A=[[F(0) for _ in range(8)] for _ in range(8)]
    for k in range(4):
        block=ids[k]; d=len(block)
        for u,i in enumerate(block):
            for v,j in enumerate(block):
                high=F(4,8)*pj3[k]/d
                low=F(0) if d==1 else F(2,8)*pj1[k-1]*((F(1) if u==v else F(0))-F(1,d))
                A[i][j]=high+low
    return A

def pt(A):
    d=1<<(N-1)
    # reorder first qubit as high bit
    return [[A[(j//d)*d+(i%d)][(i//d)*d+(j%d)] for j in range(8)] for i in range(8)]

def qform(A,v):
    return sum(v[i]*v[j]*A[i][j] for i in range(8) for j in range(8))

v=[0,1,1,0,0,0,0,14]
A=pt(rho_mat(False)); B=pt(rho_mat(True))
q=qform(A,v); qs=qform(B,v)
assert q<0, f'no NPT {float(q)}'
assert qs>0
# All eigenvalues of stationary singleton partial transpose positive via Sylvester principal minors
BM=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in r] for r in B])
minor=[BM[:i,:i].det(method='domain-ge') for i in range(1,9)]
assert all(a>0 for a in minor)
# unnormalized omitted uniformization mass =sum_{k>K} 15^k/k!, bounded by geometric majorant
first=mu**(K+1)/F(factorial(K+1))
R=first/(1-mu/F(K+2))
# every partial-transpose quadratic form along v is <= ||v||^2 ||PT(state)||op <= 2||v||² for normalized density matrix
# Actually for 2 x d, ||PT(rho)||op <= ||PT(rho)||2 = ||rho||2 <=1. Thus <=||v||². 
err=R*sum(x*x for x in v)
assert -q>err
print('N=3 nu=3/20 tGamma=5/2, uniformization lambda=6, mean=15, degree',K)
print('integer witness nonzero components (binary order, first qubit highest):',[(i,c) for i,c in enumerate(v) if c])
print('RATIONAL truncated unnormalized PT quadratic form sign:',q<0)
print('q truncated unnormalized approx',float(q))
print('tail bound approx',float(R),'quadratic error',float(err))
print('certification margin -q/err >',float(-q/err))
print('stationary witness approx',float(qs),'all 8 stationary PT Sylvester leading minors positive', all(x>0 for x in minor))
print('smallest stationary leading minor approx',min(float(x) for x in minor))
print('max exit check: P valid for both Ms')

# Compute symbolic witness polynomial for clean readable proof
p30,p31,p32,p33,p10,p11=sp.symbols('a0 a1 a2 a3 b0 b1')
coords={3:[p30,p31,p32,p33],1:[p10,p11]}
Am=[[sp.Integer(0) for _ in range(8)] for _ in range(8)]
for k in range(4):
  block=ids[k];d=len(block)
  for u,i in enumerate(block):
    for z,j in enumerate(block):
      high=sp.Rational(1,2)*coords[3][k]/d
      low=0 if d==1 else sp.Rational(1,4)*coords[1][k-1]*((1 if u==z else 0)-sp.Rational(1,d))
      Am[i][j]=high+low
PT=[[Am[(j//4)*4+(i%4)][(i//4)*4+(j%4)] for j in range(8)] for i in range(8)]
print('symbolic qform=',sp.factor(sum(v[i]*v[j]*PT[i][j] for i in range(8) for j in range(8))))

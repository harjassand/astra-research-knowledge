#!/usr/bin/env python3
"""Bounded exploratory SOS test of N740's isotropic closed heat gate for F*.

Uses all homogeneous-quadratic closed two-forms and a Gram matrix on A_i jet_j.
Numerical feasibility/failure is not a mathematical certificate or refutation.
Never touches frozen source files. NumPy and SymPy only; no grid sampling.
"""
from pathlib import Path
import json
import time
import numpy as np
import sympy as S

OUT=Path(__file__).parent
x=S.symbols('x0:4'); z=S.symbols('z0:6')
a,b,c,d=x; u=a*a+c*c; v=b*b+d*d; w=a*b+c*d; q=a*d-b*c
F=u*u+v*v+4*w*w+S.Rational(7,2)*q*q-S.Rational(29,10)*q*(u+v)
J1=S.Matrix([z[0],z[1],z[3],z[4]])
J2=S.Matrix([z[1],z[2],z[4],z[5]])
J=(J1,J2)
xpairs=[(i,j) for i in range(4) for j in range(i,4)]
zpairs=[(i,j) for i in range(6) for j in range(i,6)]
formpairs=[(i,j) for i in range(4) for j in range(i+1,4)]
xmon=[x[i]*x[j] for i,j in xpairs]
zmon=[z[i]*z[j] for i,j in zpairs]
mon=[a*b for a in xmon for b in zmon]
monexp=[S.Poly(m,*(x+z)).monoms()[0] for m in mon]
lookup={e:i for i,e in enumerate(monexp)}
def coeff(poly):
    ans=S.zeros(len(mon),1)
    for ex,val in S.Poly(S.expand(poly),*(x+z)).terms(): ans[lookup[ex]]=val
    return ans
def diss(poly):
    H=S.hessian(poly,x)
    return S.expand(sum((j.T*H*j)[0] for j in J))

# Build the 16 homogeneous-linear closedness equations; their rank is 15.
ws=S.symbols('w0:60')
forms={ij:sum(ws[10*n+k]*m for k,m in enumerate(xmon)) for n,ij in enumerate(formpairs)}
def form(i,j): return forms[(i,j)] if i<j else -forms[(j,i)]
closed=[]
for i in range(4):
    for j in range(i+1,4):
        for k in range(j+1,4):
            dd=S.diff(form(j,k),x[i])-S.diff(form(i,k),x[j])+S.diff(form(i,j),x[k])
            closed.extend([S.expand(dd).coeff(xx) for xx in x])
C,_=S.linear_eq_to_matrix(closed,ws)
assert C.rank()==15
N=S.Matrix.hstack(*C.nullspace())
assert N.shape==(60,45)
O=S.Matrix.hstack(*[coeff(m*(J1[i]*J2[j]-J1[j]*J2[i])) for i,j in formpairs for m in xmon])
ON=np.array(O*N,dtype=float)
U,sig,_=np.linalg.svd(ON,full_matrices=True)
assert np.sum(sig>1e-9)==45
D=U[:,45:].T

# Orthonormal vectorization of a symmetric 24-by-24 bilinear Gram matrix.
n=24
ij=np.triu_indices(n); wt=np.where(ij[0]==ij[1],1.,np.sqrt(2.))
bmon=[xx*zz for xx in x for zz in z]
P=np.column_stack([np.array(coeff(bmon[i]*bmon[j]),dtype=float).ravel()*(1. if i==j else np.sqrt(2.)) for i,j in zip(*ij)])
Ef=np.array(coeff(diss(F)),float).ravel()
Ed=np.array(coeff(diss(q*q)),float).ravel()

# Unknowns are Gram vech and a nonnegative minor-removal coefficient gamma.
T=np.column_stack([D@P,D@Ed])
rhs=D@Ef
tp=np.linalg.pinv(T,rcond=1e-11)
anchor=tp@rhs
projector=np.eye(T.shape[1])-tp@T
assert np.linalg.norm(T@anchor-rhs)<1e-8
def mat(vec):
    out=np.zeros((n,n));out[ij]=vec/wt;out[(ij[1],ij[0])]=vec/wt
    return out
def vech(mm): return mm[ij]*wt


# Extension: expose dissipation map for every invariant coefficient.
basis=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
E=np.column_stack([np.array(coeff(diss(f)),float).ravel() for f in basis])
s,t=S.symbols('s t')
QL=[]
for f in basis:
    ac=S.expand(s*s*S.diff(f,a,a)+2*s*t*S.diff(f,a,b)+t*t*S.diff(f,b,b))
    M11=S.hessian(ac.coeff(s,2).coeff(t,0),x)/2
    M12=S.hessian(ac.coeff(s,1).coeff(t,1),x)/4
    M22=S.hessian(ac.coeff(s,0).coeff(t,2),x)/2
    QL.append(np.array(M11.row_join(M12).col_join(M12.row_join(M22)),float))
for i,j in formpairs:
    K=np.zeros((4,4));K[i,j]=1;K[j,i]=-1
    QL.append(np.block([[np.zeros((4,4)),K],[-K,np.zeros((4,4))]]))
np.savez(OUT/'interfaces.npz',E=E,D=D,P=P,T=T,Ti=tp,Proj=projector,ON=ON,N=np.array(N,float),O=np.array(O,float),C=np.array(C,float),Q=np.array(QL),Ed=Ed)
Ea=np.array([np.column_stack([np.array(coeff((J[0].T*S.hessian(f,x)*J[0])[0]),float).ravel(),np.array(coeff(2*(J[0].T*S.hessian(f,x)*J[1])[0]),float).ravel(),np.array(coeff((J[1].T*S.hessian(f,x)*J[1])[0]),float).ravel()]) for f in basis]); np.savez(OUT/'anisotropic_maps.npz',Ea=Ea); print('interfaces built',flush=True)

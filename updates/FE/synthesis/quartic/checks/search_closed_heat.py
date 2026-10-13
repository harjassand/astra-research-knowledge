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

records=[]
for margin in [0.,1e-4]:
    y=anchor.copy(); dual=np.zeros_like(y)
    tick=time.monotonic()
    for step in range(10001):
        xx=anchor+projector@(y-dual)
        lam,V=np.linalg.eigh(mat(xx[:-1]+dual[:-1]))
        yp=np.r_[vech((V*np.maximum(lam,margin))@V.T),max(0.,xx[-1]+dual[-1])]
        dual+=xx-yp
        primal=np.linalg.norm(xx-yp); diff=np.linalg.norm(yp-y);y=yp
        if step%2000==0: print('margin',margin,'step',step,'residual',primal,'gamma',xx[-1],flush=True)
        if primal<1e-10 and diff<1e-10:break
    ev=np.linalg.eigvalsh(mat(xx[:-1]))
    rec={'margin':margin,'iterations':step,'primal_residual':float(primal),'dual_residual':float(diff),'min_eigenvalue':float(ev[0]),'gamma':float(xx[-1]),'seconds':time.monotonic()-tick,'status':'NUMERICAL_ONLY'}
    records.append(rec)
    np.savez(OUT/f'heat_candidate_{margin:g}.npz',gram=mat(xx[:-1]),gamma=xx[-1],projection_residual=T@xx-rhs,omega_basis=np.array(N,float),omega_map=ON,P=P,Ef=Ef,Ed=Ed)
    print(json.dumps(rec),flush=True)
(OUT/'heat_search_results.json').write_text(json.dumps({'method':'full closed quadratic 2-form, bilinear SOS Gram, identity diffusion, nonnegative gamma; bounded ADMM, numerical only','records':records},indent=2)+'\n')

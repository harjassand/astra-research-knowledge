#!/usr/bin/env python3
"""Bounded many-mode compatible Hessian attack on G, with all-B optimization.

phi=((2/3)v_y,v_x), periodic scalar Fourier v. Continuous compatibility is
exact at representation level. Floating spectral quadrature resolves quartic
products but is not a rational sign certificate. Any negative candidate must
be independently reconstructed before promotion.
"""
import json,time
from pathlib import Path
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parent

a,b,c,d=s.symbols("a b c d")
u=a*a+c*c;vv=b*b+d*d;q=a*d-b*c
G=3*(u+vv-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u
gf=s.lambdify((a,b,c,d),G,"numpy")
dg=s.lambdify((a,b,c,d),[s.diff(G,z) for z in (a,b,c,d)],"numpy")
hh=s.lambdify((a,b,c,d),list(s.hessian(G,(a,b,c,d))),"numpy")

M=3;N=32
modes=[(i,j) for i in range(M+1) for j in range(-M,M+1) if i>0 or j>0]
grid=np.arange(N)*2*np.pi/N
x,y=np.meshgrid(grid,grid,indexing="ij");x=x.ravel();y=y.ravel()
P=[];Q=[];R=[]
for i,j in modes:
 arg=i*x+j*y
 weight=max(1,i*i+j*j)
 for f in [np.cos(arg),np.sin(arg)]:
  P.append(-i*i*f/weight);Q.append(-i*j*f/weight);R.append(-j*j*f/weight)
P,Q,R=[np.array(z).T for z in (P,Q,R)]
size=len(modes)*2

def fields(coef):
 p=P@coef;qq=Q@coef;r=R@coef
 return p,qq,r,np.array([(2/3)*qq,(2/3)*r,p,qq])

def objective(coef,need_grad=True):
 p,qq,r,X=fields(coef)
 H=np.array([np.mean(z) if np.ndim(z)>0 else z for z in hh(*X)]).reshape(4,4)
 H=(H+H.T)/2
 eig=np.linalg.eigvalsh(H)
 stress=np.array(dg(*X));bb=stress.mean(axis=1)
 if eig[0]<=1e-10*max(1,eig[-1]):
  return 1e6,np.zeros(size),{"status":"near_singular_H","eigenvalues":eig.tolist()}
 B=-np.linalg.solve(H,bb)
 Y=X+B[:,None]
 energy=float(np.mean(gf(*Y))-gf(*B))
 norm2=(X*X).sum(axis=0);norm4=float(np.mean(norm2*norm2))
 value=energy/norm4
 info={"status":"regular","Jensen_gap":energy,"norm_fourth":norm4,
       "ratio":value,"B":B.reshape(2,2).tolist(),"H_eigenvalues":eig.tolist()}
 if not need_grad:return value,None,info
 S=np.array(dg(*Y))
 gradE=((2/3)*Q.T@S[0]+(2/3)*R.T@S[1]+P.T@S[2]+Q.T@S[3])/(N*N)
 SN=4*norm2[None,:]*X
 gradN=((2/3)*Q.T@SN[0]+(2/3)*R.T@SN[1]+P.T@SN[2]+Q.T@SN[3])/(N*N)
 grad=(gradE-value*gradN)/norm4
 return value,grad,info

def solve(seed,iterations=800):
 rng=np.random.default_rng(seed)
 c=rng.normal(size=size);c/=np.linalg.norm(c)
 f,g,info=objective(c)
 # An independent directional derivative check is useful for this moment
 # gradient; it does not certify the continuum sign of a numerical result.
 probe=rng.normal(size=size);probe-=np.dot(probe,c)*c;probe/=np.linalg.norm(probe)
 delta=2e-6
 fp=objective((c+delta*probe)/np.linalg.norm(c+delta*probe),False)[0]
 fm=objective((c-delta*probe)/np.linalg.norm(c-delta*probe),False)[0]
 assert abs((fp-fm)/(2*delta)-np.dot(g,probe))<1e-4
 alpha=.1;ledger=[];start=time.time()
 for it in range(iterations):
  tangent=g-np.dot(c,g)*c
  gn=float(np.linalg.norm(tangent))
  if it%100==0:ledger.append({"iteration":it,"ratio":f,"gradient_norm":gn})
  if gn<1e-8:break
  step=alpha
  for backtrack in range(40):
   trial=c-step*tangent;trial/=np.linalg.norm(trial)
   ft,gt,infot=objective(trial)
   if ft<=f-1e-4*step*gn*gn:break
   step*=.5
  else:break
  dc=trial-c;dg0=gt-g;denom=np.dot(dc,dg0)
  alpha=float(np.clip(np.dot(dc,dc)/denom,1e-7,10.)) if denom>0 else .1
  c,f,g,info=trial,ft,gt,infot
  if info["Jensen_gap"]< -1e-10:break
 p,qq,r,X=fields(c)
 Q2=(5/12)*np.mean(p*p)
 C3=-(5/162)*np.mean(qq*(9*p*p+4*qq*qq))
 D4=float(np.mean(gf(*X)))
 discr=C3*C3/(4*Q2*D4) if Q2>0 and D4>0 else None
 return {"seed":seed,"modes":modes,"basis_normalization":"1/max(1,i^2+j^2)",
  "coefficients":c.tolist(),"iterations":it+1,"ledger":ledger,
  "seconds":time.time()-start,"result":info,
  "soft_I_quadratic":float(Q2),"soft_I_cubic":float(C3),
  "soft_I_quartic":D4,"soft_I_discriminant_ratio":None if discr is None else float(discr),
  "scope":"48 Fourier coefficients, continuous compatible Hessian map, floating all-B moment optimum."}

results=[]
for seed in [1501,1502,1503]:
 rec=solve(seed);results.append(rec)
 (ROOT/"soft_hessian_search.json").write_text(json.dumps({
  "scope":"Bounded many-mode negative attack; no positive result is a continuum lower bound.",
  "N":N,"M":M,"results":results},indent=2)+"\n")
 print({k:v for k,v in rec.items() if k not in ("coefficients","modes")},flush=True)

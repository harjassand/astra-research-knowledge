#!/usr/bin/env python3
"""Independent rational Gram inverse-root compiler and finite raw-sign guards.
Source-disabled fixtures, no sampled learning or generic Jacobi/compiler execution.
"""
from pathlib import Path
import sympy as s
import numpy as np
import hashlib,json
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z]
axis=s.Matrix([s.Rational(3,5),0,s.Rational(4,5)]);T=s.Rational(4,5)*s.eye(3)-s.Rational(4,25)*axis*axis.T
D=[sum((T[k,j]*P[k]/2 for k in range(3)),s.zeros(2)) for j in range(3)]
G=s.Matrix(3,3,lambda j,k:s.trace(D[j]*D[k]));assert G==T*T/2

def posdef(A):return all(A[:k,:k].det()>0 for k in range(1,A.rows+1))
def invroot_rational(A,u):
 assert posdef(A)
 q=max(s.Rational(1),s.trace(A));h=q;halves=0
 while not posdef(A-h*s.eye(3)):h/=2;halves+=1
 r=1-h/q;Z0=s.eye(3)-A/q;coef=s.Rational(1);power=s.eye(3);series=power.copy();m=0
 while r**(m+1)/(1-r)>u/2:
  m+=1;coef*=s.Rational(2*m-1,2*m);power=power*Z0;series+=coef*power
 lo=s.Rational(0);hi=s.Rational(1);steps=0
 while hi-lo>u*(1-r)/2:
  mid=(lo+hi)/2
  if q*mid*mid<=1:lo=mid
  else:hi=mid
  steps+=1
 W=lo*series
 assert r**(m+1)/(1-r)+(hi-lo)/(1-r)<=u
 return W,h,{'degree':m,'h_halvings':halves,'scalar_bisections':steps,'q':str(q),'h':str(h),'r':str(r),'certified_error':str(u)}

def rotation(t,kind):
 c=(1-t*t)/(1+t*t);v=2*t/(1+t*t)
 return s.Matrix([[c,-v],[v,c]]) if kind=='X' else c*I-s.I*v*X
# rational angle approximates tan(pi/8), with exact rational-unitary columns.
t=s.Rational(414213562373095,10**15);Qs=[rotation(t,'X'),rotation(t,'Y'),I]
# Enumerate the actual three-input-axis/three-readout-axis ordinary law.
gamma=s.Rational(9,25);translation=gamma*sum((axis[k]*P[k] for k in range(3)),s.zeros(2));rho0=(I+translation)/2
means=[s.zeros(2) for _ in range(3)];seconds=[s.zeros(2) for _ in range(3)];events=0
for j in range(3):
 for sign in [1,-1]:
  rho=rho0+sign*D[j]
  for M in P:
   for b in [1,-1]:
    proj=(I+b*M)/2;prob=s.trace(proj*rho)/18;shadow=3*proj-I;record=3*sign*shadow
    means[j]+=prob*record;seconds[j]+=prob*record**2;events+=1
for j in range(3):
 assert (means[j]-D[j]).applyfunc(s.simplify)==s.zeros(2)
 assert (seconds[j]-3*(2*I+rho0)).applyfunc(s.simplify)==s.zeros(2)
 assert all(v<=9 for v in seconds[j].eigenvals())
rows=[]
for a in [s.Rational(1,10**6),s.Rational(1,10**7)]:
 H=[Z,I/2,X];Dh=[D[j]+a*H[j] for j in range(3)];Gh=s.Matrix(3,3,lambda j,k:s.trace(Dh[j]*Dh[k]))
 g=6*(2*a+a*a);u=s.Rational(1,10**7)
 W,h,meta=invroot_rational(Gh,u);assert h>g
 # Entirely rational outward bound for the displayed guard, deliberately loose.
 E=2*a/h+g/(h-g)**2+2*(1+a)*u
 assert h<1 and h-g<1
 C=[sum((Dh[k]*W[k,j] for k in range(3)),s.zeros(2)) for j in range(3)]
 Gn=np.array(Gh,dtype=float);ev,Q=np.linalg.eigh(Gn);Wn=Q@np.diag(ev**-.5)@Q.T
 actual_inverse_error=float(np.linalg.norm(np.array(W,dtype=float)-Wn,2));assert actual_inverse_error<float(u)
 guards=[]
 for j,Qj in enumerate(Qs):
  assert Qj.H*Qj==I
  rotated=Qj.H*C[j]*Qj;diag=s.diag(rotated[0,0],rotated[1,1]);res=C[j]-Qj*diag*Qj.H
  # L1 absolute real/imag entry sum upper bounds Frobenius, exactly rational.
  v=sum(abs(s.re(z))+abs(s.im(z)) for z in res)
  e=E+v;ell=min(abs(diag[0,0]),abs(diag[1,1]));delta=s.Rational(1,20)
  assert ell>e and 2*e<=delta*(2*ell-e)
  signs=s.diag(s.sign(diag[0,0]),s.sign(diag[1,1]));S=Qj*signs*Qj.H;assert S*S==I
  actual=float(np.linalg.norm(np.array(S-P[j],dtype=complex),2));assert actual<=float(delta)
  whitening_error=float(np.linalg.norm(np.array(C[j],dtype=complex)-np.array(P[j],dtype=complex)/np.sqrt(2),2));assert whitening_error<=float(E)
  guards.append({'axis':j,'reflection_error':actual,'certified_target':float(delta),'whitening_error':whitening_error,'rational_E':str(E),'raw_guard_pass':True})
 rows.append({'a':str(a),'inverse_root':meta,'actual_inverse_root_error':actual_inverse_error,'guards':guards})
result={'status':'PASS','scope':'Exact rational finite inverse-root and raw sign guard fixtures plus floating diagnostics; no sampled acquisition or generic Jacobi run','source_outcomes':0,'rng_draws':0,'exact_ordinary_born_events':events,'cases':rows,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__)]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

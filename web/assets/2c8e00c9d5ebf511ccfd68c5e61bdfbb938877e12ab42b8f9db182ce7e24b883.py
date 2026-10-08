"""Finite floating checks of the analytic exact Euler/Legendre cubature.
These checks verify transcription, not the unrestricted broadcasting theorem.
"""
from pathlib import Path
import json, platform
import numpy as np
from sympy import S
from sympy.physics.wigner import clebsch_gordan

def spin(j2):
 j=j2/2;d=j2+1;m=np.arange(j,-j-1,-1);z=np.diag(m);p=np.zeros((d,d),complex)
 for k in range(1,d):p[k-1,k]=np.sqrt((j-m[k])*(j+m[k]+1))
 return [(p+p.T)/2,(p-p.T)/2j,z]
def multipoles(j2,l):
 j=S(j2)/2;d=j2+1;ms=[j-S(k) for k in range(d)];cs=[]
 for q in range(-l,l+1):
  T=np.array([[complex((-1)**int(j-m2)*clebsch_gordan(j,j,S(l),m1,-m2,S(q))) for m2 in ms] for m1 in ms])*np.sqrt(d)
  for A in [(T+T.conj().T)/2,(T-T.conj().T)/2j]:
   for B in cs:A-=np.trace(B@A).real/d*B
   n=np.sqrt(np.trace(A@A).real/d)
   if n>1e-8:cs.append(A/n)
 return cs
rows=[]
for j2 in [2,3]:
 d=j2+1;j=j2/2;Jx,Jy,Jz=spin(j2);m=np.diag(Jz);e,V=np.linalg.eigh(Jy);z,w=np.polynomial.legendre.leggauss(d);N=2*d-1
 for t in [0,.35,.75,(1.5 if j2==2 else 1.8)]:
  sp=np.sqrt(2*t/3) if j2==2 else np.sqrt(5*t/9)
  psi=np.zeros(d,complex);psi[0]=np.sqrt((1+sp)/2);psi[-1]=np.sqrt((1-sp)/2)
  sm=np.zeros((d*d,d*d),complex);choi=np.zeros_like(sm);povm=np.zeros((d,d),complex);count=0
  for a in range(N):
   Ua=np.diag(np.exp(-1j*(2*np.pi*a/N)*m))
   for c in range(N):
    Uc=np.diag(np.exp(-1j*(2*np.pi*c/N)*m))
    for zz,ww in zip(z,w):
     Ub=(V*np.exp(-1j*np.arccos(zz)*e))@V.conj().T;v=Ua@Ub@Uc@psi;P=np.outer(v,v.conj());wt=ww/(2*N*N)
     pvec=P.reshape(-1);sm+=d*wt*np.outer(pvec,pvec.conj());choi+=d*wt*np.kron(P.T,P);povm+=d*wt*P;count+=1
  expected=[t/3,(2-t)/5] if j2==2 else [t/3,.2,(2-t)/7]
  residuals=[];observed=[]
  for l,mu in enumerate(expected,1):
   Bs=multipoles(j2,l);obs=[]
   for B in Bs:
    out=(sm@B.reshape(-1)).reshape(d,d);residuals.append(float(np.linalg.norm(out-mu*B)));obs.append(float(np.trace(B@out).real/d))
   observed.append(sum(obs)/len(obs))
  row={'j':j,'t':t,'outcomes':count,'povm_sum_error':float(np.linalg.norm(povm-np.eye(d))),'choi_min_eig':float(np.linalg.eigvalsh(choi)[0]),'super_min_eig':float(np.linalg.eigvalsh(sm)[0]),'mu_expected':expected,'mu_observed':observed,'max_multipole_error':max(residuals)}
  assert count==d*(2*d-1)**2 and row['povm_sum_error']<1e-11 and row['max_multipole_error']<1e-11 and row['choi_min_eig']>-1e-11
  rows.append(row)
result={'status':'FINITE-EVIDENCE','purpose':'Transcription check of analytically exact cubature','python':platform.python_version(),'numpy':np.__version__,'rows':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

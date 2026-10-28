#!/usr/bin/env python3
"""Author matrix/algebra/ledger checks; not a production quantum or SDP execution."""
from pathlib import Path
import hashlib,json,math
from fractions import Fraction as F
import numpy as np
from scipy.linalg import solve_sylvester
rng=np.random.default_rng(281228)
def basis(d):
 out=[]
 for i in range(d):
  Q=np.zeros((d,d),complex);Q[i,i]=1;out.append(Q)
 for i in range(d):
  for j in range(i+1,d):
   Q=np.zeros((d,d),complex);Q[i,j]=Q[j,i]=1/math.sqrt(2);out.append(Q)
   Q=np.zeros((d,d),complex);Q[i,j]=1j/math.sqrt(2);Q[j,i]=-1j/math.sqrt(2);out.append(Q)
 return np.array(out)
def dilation(Z):
 d=Z.shape[0];return np.block([[np.zeros((d,d)),Z],[Z.conj().T,np.zeros((d,d))]])
def clip(X,t):
 e,U=np.linalg.eigh(X);return (U*np.clip(e,-t,t))@U.conj().T
covcases=0;maxmoment=0.;maxrecon=0.;maxbias=0.;maxBslack=0.
for d in [2,3,4,6,8]:
 Bs=basis(d);p=d*d
 for rep in range(8):
  Z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));T=Z@Z.conj().T;T/=np.trace(T).real
  eta=2.**(-2-rep);U=T+2*eta*np.eye(d)
  lc=np.linalg.cholesky(U)
  # Explicit finite dyadic entries, increasing only known arithmetic precision.
  bits=math.ceil(math.log2(1000*d/eta))
  lc=np.round(lc.real*2**bits)/2**bits+1j*np.round(lc.imag*2**bits)/2**bits
  assert np.linalg.norm(lc@lc.conj().T-U,2)<=eta/10
  B=1.1*lc;W=B@B.conj().T
  assert np.linalg.eigvalsh(W-U)[0]>0 and np.linalg.eigvalsh(2*U-W)[0]>0
  KUb=np.array([[np.trace(A@(U@C+C@U)/2).real for C in Bs] for A in Bs])
  e,V=np.linalg.eigh(KUb);Ks=(V*np.sqrt(e))@V.T
  Qm,_=np.linalg.qr(rng.normal(size=(p,p)));C=Ks@Qm@np.diag(rng.uniform(.05,1,size=p))@Qm.T@Ks
  e,V=np.linalg.eigh(C);Fac=(V*np.sqrt(np.maximum(e,0)))@V.T
  mats=[np.einsum('a,aij->ij',Fac[:,i],Bs) for i in range(p)]
  zerr=[B.conj().T@solve_sylvester(W,W,E) for E in mats]
  R=sum(z@z.conj().T for z in zerr);C2=sum(z.conj().T@z for z in zerr)
  ratio=max(np.linalg.eigvalsh(R)[-1],np.linalg.eigvalsh(C2)[-1])/(d/2);maxmoment=max(maxmoment,float(ratio));assert ratio<=1+1e-10
  # Imbalanced +/- finite laws retain the same second moment but have nonzero bias.
  sk=rng.uniform(-.8,.8,size=p);mean=sum(s*z for s,z in zip(sk,zerr))/math.sqrt(p)
  assert np.linalg.norm(mean,2)<=math.sqrt(d/2)+1e-10;maxbias=max(maxbias,float(np.linalg.norm(mean,2)/math.sqrt(d/2)))
  zs=B.conj().T@solve_sylvester(W,W,T)
  maxrecon=max(maxrecon,float(np.linalg.norm(B@zs+zs.conj().T@B.conj().T-T)))
  assert np.linalg.norm(zs,2)<4;covcases+=1
clipcases=0;max_clip_bias=0.;max_varratio=0.;max_offdiag=0.;active=0
for d in [1,2,3,5]:
 for pp in [1e-1,1e-4,1e-8,1e-12]:
  for delta in [0.,.01,1.,4.]:
   Z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));Z/=np.linalg.norm(Z,2)
   C=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));C/=np.linalg.norm(C,2)
   sigma=.003;v=2*(sigma*sigma+delta*delta);t=256*math.sqrt(v)*1.9
   X0=-delta*dilation(C);X1=X0+sigma/math.sqrt(pp)*dilation(Z)
   probs=[1-pp,pp];xs=[X0,X1];ys=[clip(X,t) for X in xs]
   if np.linalg.norm(X1,2)>t:active+=1
   EX=sum(p*X for p,X in zip(probs,xs));EX2=sum(p*X@X for p,X in zip(probs,xs));EY=sum(p*Y for p,Y in zip(probs,ys));EY2=sum(p*Y@Y for p,Y in zip(probs,ys))
   assert np.linalg.eigvalsh(v*np.eye(2*d)-EX2)[0]>-1e-8
   bias=np.linalg.norm(EY-EX,2)/(v/t);max_clip_bias=max(max_clip_bias,float(bias));assert bias<=1+1e-8
   vr=np.linalg.eigvalsh(EY2-EY@EY)[-1]/v;max_varratio=max(max_varratio,float(vr));assert vr<=1+1e-8
   for Y in ys:
    off=max(np.linalg.norm(Y[:d,:d]),np.linalg.norm(Y[d:,d:]));max_offdiag=max(max_offdiag,float(off));assert off<=1e-8*(1+t)
   clipcases+=1
# Exact recurrence and precision/decision caps.
rec=0;max_radius=F(0)
for j in range(1,101):
 eta=F(1,2**j);sb=F(1,2**(11+j//2));tj=(13+j//2+1)//2
 assert F(101)*eta/F(2**29)<=sb*sb
 assert 128*sb*sb<=eta/F(128**2)
 dd=F(4)
 for _ in range(tj):dd=dd/4+2*sb
 assert dd<=4*sb;max_radius=max(max_radius,dd/sb);rec+=1
for rr in np.linspace(1,2,101):assert 1/rr+math.sqrt(2)+4*rr/3<8
# Fixed raw-cap check uses conservative exact integer upper bounds on logarithms.
def ceilq(q):return -(-q.numerator//q.denominator)
def clog2(q):
 n,den=q.numerator,q.denominator;k=n.bit_length()-den.bit_length()
 if (n>den*2**k if k>=0 else n*2**(-k)>den):k+=1
 return k
capcases=0
for k,Rrank in [(1,1),(2,1),(3,3),(6,2),(9,4)]:
 d=2*k;r=min(d,3*Rrank);D=10*d*d;L=8*D;Dp=d*r;Dplus=2**clog2(F(Dp))
 for j in [1,8,23,50]:
  eta=F(1,2**j);n=ceilq(F(2**28*d*L)/eta);fl=ceilq(2+F(r)/eta);mb=n+fl+1
  z=min(eta/(10**6*D*n),F(1,mb*mb));Sz=10+D*clog2(F(4)/eta/F(1,2**20))+1
  Lz=2+clog2(1/z);lb=mb+Lz;beta=z/(1000*lb*lb*Dp*Dp*mb*mb);n0bar=320*Dplus*clog2(12*Dplus/beta)+1
  for ss in [1,7,31]:
   S=min(ss,Sz);ww=[int(i) for i in rng.integers(1,100,size=S)];tot=sum(ww);mi=[ceilq(n*F(w,tot))+fl for w in ww]
   assert max(mi)<=mb and sum(mi)<=n+Sz*(fl+1)
   raw=0
   for m in mi:
    assert z<=F(1,m*m)
    l=max(m,(clog2(4/z)+1)//2);bi=z/(1000*l*l*Dp*Dp*m*m);assert bi>=beta
    n0=320*Dplus*clog2(12*Dplus/bi)
    raw+=n0+m+l
   assert raw<=2*n+Sz*(2*(fl+1)+n0bar+Lz);capcases+=1
p=Path(__file__).resolve().parent/'ordinary_generic_matrix_gls_sylvester_clipping_20261028.md'
out={'status':'PASS_AUTHOR_SYLVESTER_CLIPPING_GLS','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dominated_real_covariance_cases':covcases,'max_two_sided_transformed_moment_over_bound':maxmoment,'max_exact_reconstruction_numerical_residual':maxrecon,'max_finite_law_bias_over_sigma_bound':maxbias,'finite_heavy_tail_clipping_cases':clipcases,'active_clipping_cases':active,'max_clipping_bias_over_bound':max_clip_bias,'max_centered_clipped_variance_over_bound':max_varratio,'max_dilation_diagonal_block_residual':max_offdiag,'exact_dyadic_recurrence_cases':rec,'max_final_radius_over_sigmabar':float(max_radius),'exact_raw_source_cap_cases':capcases,'scope':'Finite matrix/covariance, biased heavy-tail clipping, exact recurrence and raw ledger checks. No full conservative pilot, production SDP, local quantum query or hardware execution.'}
p.with_name(p.stem+'_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

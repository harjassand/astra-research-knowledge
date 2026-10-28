"""Finite binomial identities and exact-moment covariance checks.
Numerical evaluation of closed finite sums, not a hardware experiment or receiver proof.
"""
import json, math, hashlib
from pathlib import Path
import numpy as np
from scipy.stats import binom
root=Path(__file__).resolve().parent
rng=np.random.default_rng(28100709)
maxmom=[0.,0.,0.]
for l in [2,3,4,5,8,13,25,50,100,300,1000]:
 for q in [0.75,0.76,0.8,0.9,0.97,0.999,1.]:
  k=np.arange(l+1); p=binom.pmf(k,l,q); h=(l+1)/(k+1); t=k/l
  eh=np.dot(p,h); eh2=np.dot(p,h*h)
  eerr=np.dot(p,(h-1/q)**2)
  er=np.dot(p,(h-1/q+(t-q)/q**2)**2)
  assert abs(eh-(1-(1-q)**(l+1))/q)<3e-13
  assert eh2<=4+1e-12 and eerr<=4/l+1e-12 and er<=9/l**2+1e-12
  maxmom=np.maximum(maxmom,[eh2,eerr*l,er*l*l]).tolist()
count=0; maxratio=0.; minvar=1e9; zero_count=0
for D in [2,3,4,7,12]:
 d=D-1
 for q in [.75,.8,.95,1.]:
  b=rng.normal(size=d)+1j*rng.normal(size=d); b*=math.sqrt((1-q)/np.vdot(b,b).real)
  psi=np.r_[math.sqrt(q),b]; P=np.outer(psi,psi.conj()); z=math.sqrt(q)*b
  Sigma=q*np.eye(d)+d/(d+1)*((1-q)*np.eye(d)+np.outer(b,b.conj()))-np.outer(z,z.conj())
  pseudo=-np.outer(z,z)
  assert np.linalg.eigvalsh(Sigma).min()>-1e-12 and np.linalg.eigvalsh(Sigma).max()<=2+1e-12
  for null in [False,True]:
   A=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D)); O=(A+A.conj().T)/2
   if null:
    Q=np.eye(D)-P; O=Q@O@Q; zero_count+=1
   alpha=O[0,0].real; c=O[1:,0]; B=O[1:,1:]; b0=np.vdot(z,B@z).real
   ro=np.vdot(psi,O@O@psi).real; fro=np.trace(O@O).real
   for m in [2,3,5,12,50]:
    for l in [m,2*m,4*m]:
     k=np.arange(l+1); probs=binom.pmf(k,l,q); hs=(l+1)/(k+1); ts=k/l
     mu=alpha*ts+b0*hs
     varq=np.dot(probs,mu**2)-np.dot(probs,mu)**2
     linear=[]
     for h in hs:
      v=c+h*(B@z)
      val=2*(np.vdot(v,Sigma@v).real+np.vdot(v,pseudo@v.conj()).real)/m
      linear.append(val)
     deg=(np.trace(B@Sigma@B@Sigma).real+b0*b0)/(m*(m-1))
     var=varq+np.dot(probs,linear)+np.dot(probs,hs*hs)*deg
     bound=24*ro/m+80*fro/(m*m)
     assert var>=-1e-10 and var<=bound+1e-9,(D,q,null,m,l,var,bound)
     maxratio=max(maxratio,var/max(bound,1e-100)); minvar=min(minvar,var);count+=1
# The known-center null-task special case is exact and detects an n^-1 error.
for D in [2,5,20]:
 B=np.eye(D-1)
 for m in [2,10,100]:
  exact=(D-1)/(m*(m-1))
  assert exact>0
# Actual randomized basis normalization and finite-sample moment diagnostics.
# Monte Carlo is a diagnostic only; the theorem uses exact sphere moments.
mc=[]
for D in [2,3,5]:
 d=D-1;q=.8;b=np.ones(d,dtype=complex)*math.sqrt((1-q)/d);psi=np.r_[math.sqrt(q),b]
 F=np.exp(2j*np.pi*np.outer(np.arange(D),np.arange(D))/D)/math.sqrt(D)
 out=[]; completeness=0.
 for _ in range(10000):
  G=(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))/math.sqrt(2)
  U,R=np.linalg.qr(G); phases=np.diag(R); phases=np.where(abs(phases)>0,phases/abs(phases),1)
  U=U@np.diag(phases)
  V=np.zeros((D,D),complex);V[0,0]=1;V[1:,1:]=U;V=V@F
  completeness=max(completeness,float(np.max(abs(V.conj().T@V-np.eye(D)))))
  ps=abs(V.conj().T@psi)**2; j=rng.choice(D,p=ps/ps.sum())
  out.append(math.sqrt(D)*V[1:,j])
 W=np.array(out); expected=math.sqrt(q)*b
 meanerror=float(np.linalg.norm(W.mean(axis=0)-expected))
 assert meanerror<.08
 mc.append({'D':D,'mean_error':meanerror,'basis_residual':completeness})
r={'status':'PASS_AUTHOR_FINITE_MOMENT_CHECKS_NOT_INDEPENDENT_RECEIVING','binomial_cases':77,'known_center_covariance_cases':count,'null_observable_fixtures':zero_count,'maximum_variance_bound_ratio':maxratio,'minimum_computed_variance':minvar,'max_Eh2_lMSE_l2R2':maxmom,'random_basis_diagnostics':mc,'scope':'Exact finite moment formula evaluation plus non-proof sampling diagnostics. Does not implement random purification or certify all finite QR gates.','source_sha256':hashlib.sha256((root/'ordinary_adaptive_pure_matrix_query_20261028.md').read_bytes()).hexdigest()}
(root/'ordinary_adaptive_pure_matrix_query_20261028_check.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))

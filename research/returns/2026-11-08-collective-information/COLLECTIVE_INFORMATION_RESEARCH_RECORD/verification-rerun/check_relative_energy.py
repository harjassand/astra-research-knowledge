"""Synthetic finite diagnostics; not physical experiments or theorem proofs."""
from pathlib import Path
import numpy as np, math, json

def build(m=6,J=2.2,kappa=20000.,mult=None):
 n=2**m;x=(np.arange(n)[:,None]>>np.arange(m))&1;k=x.sum(1)
 E=-J*(2*k-m)**2/(2*m);p=np.exp(-E-max(-E));p/=p.sum();s=np.sqrt(p)
 F=np.zeros((n,n));B=np.zeros((n,n))
 for a in range(n):
  for i in range(m-1):
   if x[a,i]!=x[a,i+1]:
    b=a^(1<<i)^(1<<(i+1));F[a,a]+=kappa;F[a,b]-=kappa
  for i in range(m):
   b=a^(1<<i);pat=(int(x[a,(i-1)%m]),int(x[a,(i+1)%m]))
   mob=1+.4*pat[0]+.3*pat[1]
   if mult is not None:mob*=mult[pat]
   r=mob*np.exp(-(E[b]-E[a])/2);B[a,a]+=r;B[a,b]-=r
 F=s[:,None]*F/s[None,:];B=s[:,None]*B/s[None,:]
 P=(k[:,None]==k[None,:]).astype(float);P/=P.sum(1)[:,None];Q=np.eye(n)-P
 return x,k,p,F,B,P,Q

def invroot(a):
 w,v=np.linalg.eigh((a+a.T)/2);z=np.zeros_like(w);mask=w>1e-8;z[mask]=1/np.sqrt(w[mask]);return (v*z)@v.T

def ex(a,t):
 w,v=np.linalg.eigh((a+a.T)/2);w=np.maximum(w,0)
 if w[0]<1e-7:w[0]=0
 return (v*np.exp(-t*w))@v.T
D=lambda d:d/(2*np.sqrt(1-d))
x,k,p,F,B,P,Q=build();A=F+B;C=P@B@P+Q@A@Q;Z=invroot(C)
d=float(np.linalg.norm(Z@(A-C)@Z,2));gamma=40000*(1-math.cos(math.pi/6))
Cc=2*math.exp(2.2)*(2*3*1.7)**2;db=math.sqrt(Cc/gamma)
errs=[float(np.linalg.norm(ex(A,t)-ex(C,t),2)) for t in np.logspace(-9,7,51)]
r={'physical_experiments':0,'relative_form':{'d_actual':d,'d_bound':db,'max_error':max(errs),'certificate':float(D(d)),'constructive_certificate':float(D(db))}}
assert max(errs)<=D(d)+1e-6 and d<=db+1e-7
U=np.eye(len(p));V=U.copy();ds=[]
for j,mu in enumerate([{(0,0):1.,(0,1):1.8,(1,0):.6,(1,1):1.3},{(0,0):2.,(0,1):.7,(1,0):1.2,(1,1):.8}]):
 _,_,_,_,Bj,Pj,Qj=build(mult=mu);Aj=F+Bj;Cj=Pj@Bj@Pj+Qj@Aj@Qj;Z=invroot(Cj)
 ds.append(float(np.linalg.norm(Z@(Aj-Cj)@Z,2)));U=ex(Aj,10**(2*j))@U;V=ex(Cj,10**(2*j))@V
 e=float(np.linalg.norm(U-V,2))
r['noncommuting_kinetic_drives']={'error':e,'certificate':float(D(max(ds)))}
assert e<=D(max(ds))+1e-7
idx=np.flatnonzero(k<=3);pc=p[idx];Ac=A[np.ix_(idx,idx)];Bc=B[np.ix_(idx,idx)];Pc=P[np.ix_(idx,idx)];Qc=np.eye(len(idx))-Pc
Dc=Pc@Bc@Pc+Qc@Ac@Qc;Z=invroot(Dc);dk=float(np.linalg.norm(Z@(Ac-Dc)@Z,2));one=np.sqrt(pc)
tm=float(one@np.linalg.solve(Ac,one)/sum(pc));tc=float(one@np.linalg.solve(Dc,one)/sum(pc))
r['killed_mean_lifetime']={'microscopic':tm,'coarse':tc,'ratio':tm/tc,'upper':1/(1-dk**2)}
assert tm/tc>=1-1e-7 and tm/tc<=1/(1-dk**2)+1e-6
qp=np.zeros(len(p));qm=qp.copy()
for a in range(len(p)):
 for i in range(6):
  b=a^(1<<i);rate=-B[a,b]*np.sqrt(p[b]/p[a]);(qp if x[a,i]==0 else qm)[a]+=rate
ratios=[]
for kk in range(7):
 for q in [qp,qm]:
  av=float(q[k==kk].mean());va=float(q[k==kk].var())
  if av:ratios.append(va/av)
r['conditional_variance']={'maximum_var_over_mean':max(ratios),'bound':Cc/4}
assert max(ratios)<=Cc/4+1e-8

def falling(a,z):
 if a<z:return 0
 v=1
 for j in range(z):v*=a-j
 return v
err=0
for kk in range(7):
 for sign in [1,-1]:
  ans=0;pr=(6-kk)/6 if sign==1 else kk/6;up=kk if sign==1 else kk-1;dn=5-kk if sign==1 else 6-kk
  for aa in [0,1]:
   for bb in [0,1]:
    prob=falling(up,aa+bb)*falling(dn,2-aa-bb)/falling(5,2);ans+=6*pr*(1+.4*aa+.3*bb)*prob
  if 0<=kk+sign<=6:ans*=math.exp((2.2*(2*(kk+sign)-6)**2-2.2*(2*kk-6)**2)/24)
  else:ans=0
  err=max(err,abs(ans-float((qp if sign==1 else qm)[k==kk].mean())))
r['hypergeometric']={'max_error':err};assert err<1e-10
_,_,_,_,B0,_,_=build(kappa=0.);gg=ex(B0,.12)@(k/6*np.sqrt(p))/np.sqrt(p);spread=max(float(np.ptp(gg[k==j])) for j in range(7))
r['unfavorable_no_stirring']={'same_count_preparation_gap':spread,'certificate_valid':False};assert spread>1e-6
Path(__file__).with_name('relative_energy_result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

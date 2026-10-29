#!/usr/bin/env python3
import numpy as np, math, json
from pathlib import Path
rng=np.random.default_rng(202610282309)
def iso(d,k):
 q,r=np.linalg.qr(rng.normal(size=(d,k))+1j*rng.normal(size=(d,k)))
 return q[:,:k]
def filt(x,m):
 c=1.; term=np.ones_like(x); total=term.copy()
 for j in range(1,m+1):
  c*= (2*j-1)/(2*j);term*=1-x*x;total+=c*term
 return x*total
rows=[]
for trial in range(120):
 k=2; n=3; d=6
 F=[iso(d,k) for _ in range(n)]
 if trial<80 and trial%4==0:F[1]=F[0].copy() # exact rank defects allowed
 if trial>=80:
  basis=iso(d,d);amp=(1e-4,.01,.05,.1)[trial%4]
  F=[np.linalg.qr(basis[:,i*k:(i+1)*k]+amp*(rng.normal(size=(d,k))+1j*rng.normal(size=(d,k))))[0] for i in range(n)]
 p=rng.dirichlet(np.ones(n));U=iso(n,n)
 S=U.conj().T@np.diag(p)@U
 F=[sum(F[i]*U[i,j] for i in range(n)) for j in range(n)]
 M=np.concatenate(F,axis=1);G=M.conj().T@M;R=np.kron(S,np.eye(k)/k)
 alpha=max(1.,np.linalg.norm(M,2));eps=1e-6
 m=math.ceil(4*alpha*alpha*math.log(2*alpha/eps))
 u,s,vh=np.linalg.svd(M,full_matrices=False)
 f=filt(s/alpha,m);A=(vh.conj().T*f)@u.conj().T
 Q=np.eye(d)-A.conj().T@A;ev,V=np.linalg.eigh((Q+Q.conj().T)/2)
 assert min(ev)>-2e-12
 sq=(V*np.sqrt(np.maximum(ev,0)))@V.conj().T
 D=[A[i*k:(i+1)*k] for i in range(n)]
 for j in range(d):
  B=np.zeros((k,d),complex);B[0]=sq[j];D.append(B)
 val,W=np.linalg.eigh(S)
 Ks=[sum(F[i]*W[i,a] for i in range(n))*np.sqrt(max(val[a],0)) for a in range(n)]
 tp=np.linalg.norm(sum(x.conj().T@x for x in Ks)-np.eye(k))
 fe=sum(abs(np.trace(a@b))**2 for a in D for b in Ks)/(k*k)
 AM=A@M
 penalty=np.trace(R@(np.eye(n*k)+G-AM-AM.conj().T)).real
 defect=np.trace(R@(G-np.eye(n*k))@(G-np.eye(n*k))).real
 bound=20*defect/9+2*alpha*eps
 assert 1-fe<=penalty+3e-12 and penalty<=bound+3e-12
 rows.append({'trial':trial,'alpha':alpha,'min_sigma':float(min(s)),'degree':2*m+1,'TP_error':tp,'Fe':float(fe),'penalty':penalty,'defect':defect,'bound':bound,'commutator_norm':float(np.linalg.norm(R@G-G@R))})
# Scalar uniform checks including zero and transition, conservative noninterval diagnostics.
for alpha in (1.,2.,7.):
 eps=1e-5;m=math.ceil(4*alpha*alpha*math.log(2*alpha/eps));sig=np.linspace(0,alpha,10001);f=filt(sig/alpha,m)
 assert min(f)>=-1e-12 and max(f)<=1+1e-12
 assert np.max(1+sig*sig-2*sig*f-(20/9)*(sig*sig-1)**2-2*alpha*eps)<1e-10
out={'status':'FLOATING_DIAGNOSTIC_CHECKS_PASS_NOT_AN_INDEPENDENT_REVIEW','cases':rows,'scalar_grids':3,'seed':202610282309}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'cases':len(rows),'max_TP':max(r['TP_error'] for r in rows),'max_violation':max(1-r['Fe']-r['bound'] for r in rows),'exact_rank_defect_cases':20}))

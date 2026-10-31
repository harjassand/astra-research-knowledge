#!/usr/bin/env python3
"""Exploratory complete-record check of reset-free private sign epochs.
Actual source states are retained through all stages. Weak measurements retain
all four outcome records, with outcome-dependent system control. No bath reset.
Float Choi norm comparisons, not certified arithmetic or a theorem.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(48391)
def diss(L):
 A=L.conj().T@L;d=len(L);return np.kron(L.conj(),L)-.5*(np.kron(np.eye(d),A)+np.kron(A.T,np.eye(d)))
def ham(H):return -1j*(np.kron(np.eye(len(H)),H)-np.kron(H.T,np.eye(len(H))))
def cn(S,di,do):
 J=np.block([[S[:,a+di*b].reshape((do,do),order='F') for b in range(di)] for a in range(di)])
 return float(np.linalg.norm(J,ord='nuc'))
D=3;d=2;dim=D*d;Ls=[]
for i in [1,2]:
 L=np.zeros((D,D),complex);L[0,i]=np.sqrt(2);Ls.append(L)
for j in range(2):
 L=(rng.normal(size=(D,D))+1j*rng.normal(size=(D,D)))/2;L[:,0]=0;Ls.append(L)
H=sum(L.conj().T@L for L in Ls)/2;v,U=np.linalg.eigh(H);Hi=(U*np.array([0]+list(1/np.sqrt(v[1:]))))@U.conj().T
K=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim));K=(K+K.conj().T)/2;K[:d,:d]=0;K/=np.linalg.norm(K,2)
H0=np.array([[.2,.3],[.3,-.2]],complex);prep=np.kron(np.eye(D)[:,0,None],np.eye(d));E=np.sqrt(2)*np.kron(Hi,np.eye(d))@K@prep
Le=ham(H0)+sum(diss(E[i*d:(i+1)*d]) for i in range(D));eff=expm(Le/3)
trace=np.zeros((d*d,dim*dim),complex)
for j in range(dim*dim):
 a=np.zeros((dim,dim));a[j%dim,j//dim]=1;trace[:,j]=np.einsum('aiaj->ij',a.reshape(D,d,D,d)).reshape(d*d,order='F')
G=sum(diss(np.kron(L,np.eye(d))) for L in Ls);L0=ham(np.kron(np.eye(D),H0));VK=ham(K)
X=np.array([[0,1],[1,0]],complex);m=.6
Ks=[np.diag(np.sqrt([(1+m)/2,(1-m)/2])),X@np.diag(np.sqrt([(1-m)/2,(1+m)/2]))]
Cs=[np.kron(k.conj(),k) for k in Ks]
CFs=[np.kron(np.kron(np.eye(D),k).conj(),np.kron(np.eye(D),k)) for k in Ks]
rows=[]
for lam in [100,1000,10000,100000]:
 plus=expm((lam*G+L0+math.sqrt(lam)*VK)/3);minus=expm((lam*G+L0-math.sqrt(lam)*VK)/3);mix=(plus+minus)/2
 norms={key:0. for key in ['fixed_plus','private_global_sign','private_fresh_epochs','exposed_global_sign']}
 traceerr=0;sumout=np.zeros((4,dim*dim),complex)
 for a in range(2):
  for b in range(2):
   target=eff@Cs[b]@eff@Cs[a]@eff@trace
   pp=trace@plus@CFs[b]@plus@CFs[a]@plus
   mm=trace@minus@CFs[b]@minus@CFs[a]@minus
   fresh=trace@mix@CFs[b]@mix@CFs[a]@mix
   norms['fixed_plus']+=cn(pp-target,dim,d)
   norms['private_global_sign']+=cn((pp+mm)/2-target,dim,d)
   norms['private_fresh_epochs']+=cn(fresh-target,dim,d)
   norms['exposed_global_sign']+=(cn(pp-target,dim,d)+cn(mm-target,dim,d))/2
   sumout+=fresh
 trsys=np.eye(d).reshape(-1,order='F');trinput=np.eye(dim).reshape(-1,order='F')
 traceerr=float(np.linalg.norm(trsys@sumout-trinput))
 rows.append(dict(rate=lam,record_branches=4,epochs=3,all_input_complete_record_choi_norms=norms,trace_defect=traceerr))
out=dict(scope=__doc__,rows=rows);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

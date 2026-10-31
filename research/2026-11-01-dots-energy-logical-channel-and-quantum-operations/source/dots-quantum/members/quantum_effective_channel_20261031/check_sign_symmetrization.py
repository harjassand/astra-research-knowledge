#!/usr/bin/env python3
"""Exploratory fixed interaction-sign mixture, not a theorem.
The sign is sampled once, kept private, and applied for the whole trajectory.
Same arbitrary input state for both signs; classical mixture is CPTP.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(48391)
def diss(L):
 A=L.conj().T@L;d=len(L)
 return np.kron(L.conj(),L)-.5*(np.kron(np.eye(d),A)+np.kron(A.T,np.eye(d)))
def ham(H):return -1j*(np.kron(np.eye(len(H)),H)-np.kron(H.T,np.eye(len(H))))
def choi(S,di,do):return np.block([[S[:,a+di*b].reshape((do,do),order='F') for b in range(di)] for a in range(di)])
def cn(S,di,do):
 J=choi(S,di,do);return float(np.linalg.norm(J,ord='nuc'))
D=3;d=2;dim=D*d;P=np.diag([1,0,0]);Ls=[]
for i in [1,2]:
 L=np.zeros((D,D),complex);L[0,i]=np.sqrt(2);Ls.append(L)
for j in range(2):
 L=(rng.normal(size=(D,D))+1j*rng.normal(size=(D,D)))/2;L[:,0]=0;Ls.append(L)
H=sum(L.conj().T@L for L in Ls)/2;v,U=np.linalg.eigh(H);Hi=(U*np.array([0]+list(1/np.sqrt(v[1:]))))@U.conj().T
K=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim));K=(K+K.conj().T)/2;K[:d,:d]=0;K/=np.linalg.norm(K,2)
H0=np.array([[.2,.3],[.3,-.2]],complex);psi=np.eye(D)[:,0];prep=np.kron(psi[:,None],np.eye(d));E=np.sqrt(2)*np.kron(Hi,np.eye(d))@K@prep
Le=ham(H0)+sum(diss(E[i*d:(i+1)*d]) for i in range(D));eff=expm(Le)
trace=np.zeros((d*d,dim*dim),complex)
for j in range(dim*dim):
 a=np.zeros((dim,dim));a[j%dim,j//dim]=1
 trace[:,j]=np.einsum('aiaj->ij',a.reshape(D,d,D,d)).reshape(d*d,order='F')
prepmap=np.kron(prep.conj(),prep)
G=sum(diss(np.kron(L,np.eye(d))) for L in Ls);L0=ham(np.kron(np.eye(D),H0));VK=ham(K)
rows=[]
for lam in [100,1000,10000,100000,1000000]:
 plus=trace@expm(lam*G+L0+math.sqrt(lam)*VK)
 minus=trace@expm(lam*G+L0-math.sqrt(lam)*VK)
 target=eff@trace;average=(plus+minus)/2
 rows.append(dict(rate=lam,cold_single_choi_norm=cn((plus-target)@prepmap,d,d),cold_mixture_choi_norm=cn((average-target)@prepmap,d,d),all_input_single_choi_norm=cn(plus-target,dim,d),all_input_mixture_choi_norm=cn(average-target,dim,d)))
out=dict(scope=__doc__,source='qutrit dark source with genuinely mixed P/Q jump outputs; random centered K includes QQ coupling',rows=rows);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

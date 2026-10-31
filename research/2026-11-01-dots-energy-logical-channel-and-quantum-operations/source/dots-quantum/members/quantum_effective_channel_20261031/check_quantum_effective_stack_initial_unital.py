#!/usr/bin/env python3
"""Nonclassical dark-source reduction diagnostic; not rigorous floating bounds.
Compares complete channels from arbitrary quantum source+system inputs, not only
CQ or prepared bath inputs. Uses exact dark-source formula for the effective
stack, whose reservoir need not preserve a classical observable algebra.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
def diss(L):
 d=L.shape[1];A=L.conj().T@L
 return np.kron(L.conj(),L)-.5*(np.kron(np.eye(d),A)+np.kron(A.T,np.eye(d)))
def comm(H):return -1j*(np.kron(np.eye(len(H)),H)-np.kron(H.T,np.eye(len(H))))
def ptr(r,D):return np.einsum('aiaj->ij',r.reshape(D,2,D,2))
def mapchoi(S,din,dout):
 return np.block([[S[:,a+din*b].reshape((dout,dout),order='F') for b in range(din)] for a in range(din)])
rows=[]
for n in [1,2,3]:
 D=2**n;q=21/20
 w=np.array([q**sum(((x>>i)&1)==((x>>(i+1))&1) for i in range(n-1)) for x in range(D)])
 psi=np.sqrt(w/w.sum()).astype(complex);P=np.outer(psi,psi.conj());Ls=[]
 for i in range(n):
  l0=np.zeros((D,D));l1=l0.copy()
  for x in range(D):
   if (x>>i)&1:continue
   y=x^(1<<i);r=w[y]/(w[x]+w[y]);l0[y,x]=np.sqrt(r);l0[y,y]=-np.sqrt(1-r);l1[x,x]=-np.sqrt(r);l1[x,y]=np.sqrt(1-r)
  Ls.extend([l0,l1])
 H=sum(l.conj().T@l for l in Ls)/2;vals,vecs=np.linalg.eigh(H)
 invsqrt=(vecs*np.array([1/np.sqrt(v) if v>1e-10 else 0 for v in vals]))@vecs.conj().T
 # Source X/Y at first spin: X is centered exactly using the supplied psi.
 Bx=np.zeros((D,D),complex);By=Bx.copy()
 for x in range(D):Bx[x^1,x]=1;By[x^1,x]=1j*(1-2*(x&1))
 Bx-=np.vdot(psi,Bx@psi)*np.eye(D)
 K=(np.kron(Bx,X)+np.kron(By,Y))/2
 K/=np.linalg.norm(K,2);H0=Z/3
 Vpsi=np.kron(psi[:,None],np.eye(2));E=np.sqrt(2)*np.kron(invsqrt,np.eye(2))@K@Vpsi
 jumps=[E[2*j:2*j+2,:] for j in range(D)]
 Le=comm(H0)+sum(diss(l) for l in jumps)
 eff=expm(Le)
 din=2*D;trace_map=np.zeros((4,din*din),complex)
 for j in range(din*din):
  e=np.zeros((din,din),complex);e[j%din,j//din]=1;trace_map[:,j]=ptr(e,D).reshape(4,order='F')
 fullG=sum(diss(np.kron(l,np.eye(2))) for l in Ls)
 for lam in [100,10000,1000000]:
  full=expm(lam*fullG+comm(np.kron(np.eye(D),H0)+np.sqrt(lam)*K))
  delta=trace_map@full-eff@trace_map;J=mapchoi(delta,din,2);J=(J+J.conj().T)/2
  norm=float(np.abs(np.linalg.eigvalsh(J)).sum())
  rows.append(dict(n=n,rate=lam,source_centering_residual=float(np.linalg.norm(Vpsi.conj().T@K@Vpsi)),dark_residual=float(np.linalg.norm(H@psi)),complete_channel_diamond_lower=norm/din,complete_channel_diamond_upper=min(2,norm),effective_unitality_defect=float(np.linalg.norm((eff@np.eye(2).reshape(4,order='F')).reshape(2,2,order='F')-np.eye(2))),effective_jump_stack_norm=float(np.linalg.norm(E,2))))
out=dict(scope=__doc__,rows=rows);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

#!/usr/bin/env python3
"""Finite-matrix diagnostic of first-corrector identities with QLQ recycling.
Random system Hermitian observables test relative energy bounds. This
is not a proof of complete bounds or certified floating arithmetic.
"""
import numpy as np,json,math
from pathlib import Path
rng=np.random.default_rng(7289)
rows=[]
for D in [2,3,5]:
 psi=np.eye(D)[:,0];P=np.outer(psi,psi);Q=np.eye(D)-P
 Ls=[]
 # Both direct return and genuinely excited-to-excited recycling, same dark psi.
 for a in range(1,D):
  L=np.zeros((D,D),complex);L[0,a]=np.sqrt(2);Ls.append(L)
 for j in range(3):
  L=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));L[:,0]=0;Ls.append(L/np.sqrt(3*D))
 H=sum(L.conj().T@L for L in Ls)/2
 v,U=np.linalg.eigh(H);g=min(v[1:]);inv=(U*np.array([0]+list(1/v[1:])))@U.conj().T
 half=(U*np.array([0]+list(1/np.sqrt(v[1:]))))@U.conj().T
 for ds in [2,3]:
  dim=D*ds;Is=np.eye(ds);PP=np.kron(P,Is);QQ=np.kron(Q,Is);HH=np.kron(H,Is);II=np.eye(dim)
  K=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim));K=(K+K.conj().T)/2;K-=PP@K@PP;K/=np.linalg.norm(K,2)
  S=np.kron(inv,Is)@K@PP+PP@K@np.kron(inv,Is);s=np.linalg.norm(S,2);beta=2/g+4*s
  jumps=[np.kron(L,Is) for L in Ls]
  def gd(A):return sum(L.conj().T@A@L for L in jumps)-HH@A-A@HH
  def V(A):return 1j*(K@A-A@K)
  worst=0;rel=0;pblock=0;efferr=0
  Vpsi=np.kron(psi[:,None],Is);Estack=np.sqrt(2)*np.kron(half,Is)@K@Vpsi
  ej=[Estack[a*ds:(a+1)*ds] for a in range(D)];eprod=Estack.conj().T@Estack
  for trial in range(12):
   O=rng.normal(size=(ds,ds))+1j*rng.normal(size=(ds,ds));O=(O+O.conj().T)/2;O/=np.linalg.norm(O,2);emb=np.kron(np.eye(D),O)
   F=1j*(S@emb-emb@S);B=QQ@V(emb)@QQ+sum(L.conj().T@F@L for L in jumps)
   worst=max(worst,np.linalg.norm(gd(F)+V(emb)-B,2))
   pblock=max(pblock,np.linalg.norm(PP@B,2))
   rel=max(rel,np.linalg.norm(np.kron(half,Is)@B@np.kron(half,Is),2)/beta)
   Deff=Vpsi.conj().T@V(F)@Vpsi
   expected=sum(e.conj().T@O@e for e in ej)-.5*(eprod@O+O@eprod)
   efferr=max(efferr,np.linalg.norm(Deff-expected,2))
  assert worst<1e-11 and pblock<1e-11 and efferr<1e-11 and rel<1+1e-12
  rows.append(dict(source_dimension=D,system_dimension=ds,identity_residual=float(worst),QQ_support_residual=float(pblock),effective_stack_identity_residual=float(efferr),relative_bound_ratio=float(rel),excited_recycling_norm=float(max(np.linalg.norm(Q@L@Q,2) for L in Ls))))
out=dict(scope=__doc__,rows=rows);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

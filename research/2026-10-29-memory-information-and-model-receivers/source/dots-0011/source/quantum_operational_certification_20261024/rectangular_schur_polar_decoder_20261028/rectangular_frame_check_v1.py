#!/usr/bin/env python3
"""Finite Young-orthogonal frame and polar fixture. Dense simulation only."""
import numpy as np,itertools,json,math,hashlib,os
from pathlib import Path
D=Path(__file__).resolve().parent

def tableaux(m):
 out=[]
 def go(a,b,cs):
  if a==b==m:out.append(tuple(cs));return
  if a<m:go(a+1,b,cs+[a])
  if b<a:go(a,b+1,cs+[b-1])
 go(0,0,[]);return out

def adjacent(tabs):
 ix={t:i for i,t in enumerate(tabs)};d=len(tabs);k=len(tabs[0]);ops=[]
 for j in range(k-1):
  diag=[];other=[];amp=[]
  for a,t in enumerate(tabs):
   r=t[j+1]-t[j];diag.append(1/r)
   tt=list(t);tt[j],tt[j+1]=tt[j+1],tt[j];b=ix.get(tuple(tt),a)
   other.append(b);amp.append(math.sqrt(max(0,1-1/r**2)))
  ops.append((np.array(diag),np.array(other),np.array(amp)))
 return ops

def apply(op,C):
 d,idx,a=op;return d[:,None]*C+a[:,None]*C[idx]

def trans(ops,i,j,C):
 for x in list(range(i,j-1))+[j-1]+list(range(j-2,i-1,-1)):C=apply(ops[x],C)
 return C

rows=[]
for k in [4,6,8,10,12,14,16]:
 m=k//2;tabs=tableaux(m);d=len(tabs);ops=adjacent(tabs);edges=list(itertools.combinations(range(k),2));q=len(edges);n2=k*(k-3)//2;N=n2+1
 B=np.zeros((q,k))
 for e,(i,j) in enumerate(edges):B[e,i]=B[e,j]=1
 PP=np.eye(q)-B@np.linalg.inv(B.T@B)@B.T
 ev,V=np.linalg.eigh(PP);V=V[:,ev>.5]
 assert V.shape==(q,n2)
 c=(k-4)/(2*(k-1));h=3*(k*k-4)/(4*(k-1)*(k-3))
 rng=np.random.default_rng(261028+k);K=2
 C=rng.normal(size=(d,K))+1j*rng.normal(size=(d,K));C=np.linalg.qr(C)[0]
 UC=np.array([trans(ops,i,j,C) for i,j in edges])
 FC=np.tensordot(V.T,UC,axes=(1,0))/math.sqrt(h)
 WC=np.concatenate([C]+[a for a in FC],axis=1);G=WC.conj().T@WC
 eig=np.linalg.eigvalsh(G);beta=(d*(d*K-1)*N/d+d*(d-K))/(d*d-1)-1 # D=d
 # weighted reference T=I/N, actual output trace=1 for all C
 defect=float(np.trace((G-np.eye(K*N))@(G-np.eye(K*N))).real/(K*N))
 gramerr=None
 if k<=8:
  U=np.array([trans(ops,i,j,np.eye(d)) for i,j in edges]);H=np.einsum('aij,bij->ab',U,U)/d
  gramerr=float(np.max(abs(H-(c*c*np.ones((q,q))+h*PP))))
 # hard-cutoff diagnostic only; implementation uses smooth bounded polynomial.
 x=np.maximum(eig,0);g=(x>=.25).astype(float)
 penalty=float(np.mean(1+x-2*np.sqrt(x)*g))
 assert penalty<=(20/9)*defect+1e-9
 rows.append({'k':k,'d':d,'N':N,'K':K,'frame_gram_entry_error_small_fixture':gramerr,'mean_gram_defect_fixture':defect,'paper_haar_mean_beta':float(beta),'singular_min':float(math.sqrt(max(0,eig[0]))),'hard_cut_penalty_diagnostic':penalty,'alpha':2*k*math.sqrt(N)})
 print(rows[-1],flush=True)
# Scalar bounded soft-sign filter tested without expanding unstable coefficients.
sc=[]
for a in [2,4,8]:
 eps=.01;M=math.ceil(4*a*a*math.log(2*a/eps));xx=np.linspace(0,1,2001);term=np.ones_like(xx);ss=term.copy()
 for j in range(1,M+1):term*=((2*j-1)/(2*j))*(1-xx*xx);ss+=term
 ff=xx*ss
 assert ff.min()>-1e-10 and ff.max()<1+1e-10
 mask=xx>=1/(2*a);err=float(np.max(1-ff[mask]));assert err<=eps
 sc.append({'alpha':a,'M':M,'maximum_high_filter_error_grid':err})
out={'status':'finite floating checks, not circuit execution or proof of all k','rows':rows,'soft_filter_checks':sc,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(D/'rectangular_frame_check_v1.json').write_text(json.dumps(out,indent=2)+'\n')

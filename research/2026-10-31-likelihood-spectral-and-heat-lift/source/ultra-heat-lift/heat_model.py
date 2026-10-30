"""Proposal: graded heat completion for the actual near-boundary ROC fixture.

A positive result is only numerical until a universal exact certificate is
reconstructed. A failure is a limitation of this primitive/Gram ansatz.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,product
import sys,json,time
import numpy as np,scipy.linalg as la,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/acoustic_capacity'))
from receive import r,b,ca,dot,quadratic
start=time.perf_counter();F,C,T=r.m.acquired();base=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());P=[b.literal(rows,4) for rows in base['primitive']]
HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)];HC=[[b.diff(b.diff(C,i),j) for j in range(4)] for i in range(4)];Avars=[b.var(4,i) for i in range(4)]
Omega={}
for i,j in combinations(range(4),2):Omega[i,j]=b.add(b.mul(T,b.add(b.diff(P[j],i),b.scale(b.diff(P[i],j),-1))),b.scale(b.add(b.mul(Avars[i],P[j]),b.scale(b.mul(Avars[j],P[i]),-1)),-2))
L1=np.zeros((4,6));L2=np.zeros((4,6))
for i,j in enumerate((0,1,3,4)):L1[i,j]=1
for i,j in enumerate((1,2,4,5)):L2[i,j]=1
pairs4=list(combinations(range(4),2));pairs6=list(combinations(range(6),2));Wedges=[]
for i,j in pairs4:
 O=np.zeros((4,4));O[i,j]=1;O[j,i]=-1;W=L1.T@O@L2;Wedges.append((W+W.T)/2)
Wedges=np.array(Wedges)
def poly_arrays(poly):return np.array(list(poly),int),np.array([float(v) for v in poly.values()])
def value(poly,v):
 pw,co=poly_arrays(poly);return float(np.prod(np.asarray(v)[None,:]**pw,axis=1)@co) if len(co) else 0.
FHA=[[poly_arrays(p) for p in row] for row in HF];ON=[poly_arrays(Omega[pair]) for pair in pairs4]
def eval_array(data,v):
 pw,co=data;return float(np.prod(v[None,:]**pw,axis=1)@co) if len(co) else 0.
def SF(v):
 v=np.asarray(v,float);tt=v@v;H=np.array([[eval_array(d,v) for d in row] for row in FHA]);omega=np.array([eval_array(d,v)/tt**2 for d in ON]);return L1.T@H@L1+L2.T@H@L2+np.einsum('p,pij->ij',omega,Wedges)
def SF_exact(v,deriv=None):
 tt=sum(z*z for z in v);H=[[b.evaluate(b.diff(p,deriv) if deriv is not None else p,v) for p in row] for row in HF];out=[[R(0) for _ in range(6)] for _ in range(6)]
 for aa,LL in enumerate((L1,L2)):
  inds=(0,1,3,4) if aa==0 else (1,2,4,5)
  for i in range(4):
   for j in range(4):out[inds[i]][inds[j]]+=H[i][j]
 for pair,W in zip(pairs4,Wedges):
  N=Omega[pair]
  co=b.evaluate(N,v)/tt**2 if deriv is None else b.evaluate(b.add(b.scale(b.mul(T,b.diff(N,deriv)),1),b.scale(b.mul(Avars[deriv],N),-4)),v)/tt**3
  for i in range(6):
   for j in range(6):out[i][j]+=co*R(float(W[i,j]))
 return out
# Closed linear two-forms have 24 coefficients and four closure equations.
dependent=[pairs4.index((i,j))*4+k for i,j,k in combinations(range(4),3)];free=[i for i in range(24) if i not in dependent];V=np.zeros((24,20))
for k,j in enumerate(free):V[j,k]=1
for i,j,k in combinations(range(4),3):V[pairs4.index((i,j))*4+k]=V[pairs4.index((i,k))*4+j]-V[pairs4.index((j,k))*4+i]
X0=np.zeros((4,6,6));XB=np.zeros((4,6,6,80))
for a in range(4):
 ea=[R(int(i==a)) for i in range(4)];H=np.array([[float(b.evaluate(p,ea)) for p in row] for row in HC]);X0[a]=(L1.T@H@L1+L2.T@H@L2)/2
 for l in range(20):XB[a,:,:,l]=sum(V[p*4+a,l]*Wedges[p]/2 for p in range(6))
 for k,(i,j) in enumerate(pairs6):XB[a,i,j,20+15*a+k]=1;XB[a,j,i,20+15*a+k]=-1

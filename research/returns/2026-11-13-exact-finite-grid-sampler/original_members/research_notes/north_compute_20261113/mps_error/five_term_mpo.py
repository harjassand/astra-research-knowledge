"""Exact-operator (floating arithmetic) sum-product MPS application utilities.
No claim of low final Schmidt rank. Compression error charged by caller's MPS.adj.
"""
import numpy as np
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex)
PHI=np.arctan2(4,3)

def dressed_terms(u,v,counts,known=None):
 # Site labels remain physical; caller maps keys into MPS ordering if necessary.
 terms=[(12/13,{})]
 for zu in [1,-1]:
  for zv in [1,-1]:
   zs={u:zu,v:zv}
   if known is not None and any(known[s] is not None and known[s]!=(1-z)//2 for s,z in zs.items()):continue
   factors={};coefficient=-5j/13
   for s,z in zs.items():
    a=np.zeros((2,2),complex);b=(1-z)//2;a[1-b,b]=1;factors[s]=a
   angles={}
   for (a,b),m in counts.items():
    if not m or ((a in zs)==(b in zs)):continue
    target=a if a in zs else b;control=b if a in zs else a
    angles[control]=angles.get(control,0)+2*m*PHI*zs[target]
   for s,angle in angles.items():
    if known is not None and known[s] is not None:coefficient*=np.exp(1j*angle*(1-2*known[s]))
    else:factors[s]=np.diag(np.exp(1j*angle*np.array([1,-1])))
   terms.append((coefficient,factors))
 return terms

def direct_qd_terms(u,v):
 return [(36/65,{}),(48j/65,{u:Z,v:Z}),(-3j/13,{u:X,v:X}),(-4/13,{u:Y,v:Y})]

def apply_sum_products(m,terms):
 """m is the underlying MPS, with factors indexed in its tensor order.
 Performs exactly span SVD compressions; all losses charged by m.adj.
 """
 support=sorted({s for _,factors in terms for s in factors})
 if not support:
  m.ts[m.center]*=sum(c for c,_ in terms);return 0
 i,j=support[0],support[-1];R=len(terms)
 if i==j:
  gate=sum((c*f.get(i,I) for c,f in terms),np.zeros((2,2),complex));m.one(i,gate);return 0
 m.move(i)
 for k in range(i,j+1):
  original=m.ts[k];l,d,r=original.shape
  mapped=[np.einsum('st,atb->asb',f.get(k,I),original) for _,f in terms]
  if k==i:m.ts[k]=np.concatenate([c*a for (c,_),a in zip(terms,mapped)],axis=2)
  elif k==j:m.ts[k]=np.concatenate(mapped,axis=0)
  else:
   tensor=np.zeros((R*l,2,R*r),complex)
   for h,a in enumerate(mapped):tensor[h*l:(h+1)*l,:,h*r:(h+1)*r]=a
   m.ts[k]=tensor
 # Outside interval canonical because m.move(i) preceded exact application.
 m.center=j;m.move(i)
 for k in range(i,j):m.adj(k,np.eye(4))
 return j-i

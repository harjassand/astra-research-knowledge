"""Exact rational Dobrushin coefficients for all routed loop types to length12.
Numerical spectrum is a screen, never an all-loop convergence certificate.
"""
from fractions import Fraction as F
from pathlib import Path
import json,numpy as np
from collections import Counter
OUT=Path(__file__).resolve().parent
CAT=OUT.parent/'square_aklt_loop_audit_20261105/loop_catalog_through12.json'
def norm(vs):
 x=min(q[0] for q in vs);y=min(q[1] for q in vs)
 return tuple((a-x,b-y) for a,b in vs)
def routekey(vs):
 vs=norm(vs);n=len(vs)
 return min(vs[k:]+vs[:k] for k in range(n)) if False else min([vs[k:]+vs[:k] for k in range(n)]+[vs[::-1][k:]+vs[::-1][:k] for k in range(n)])
def variants(vs):
 out=set()
 for f in [-1,1]:
  for k in range(4):
   q=[]
   for x,y in vs:
    x*=f
    for _ in range(k):x,y=-y,x
    q.append((x,y))
   out.add(routekey(q))
 return out

def edgelist(vs):
 return {tuple(sorted((vs[k],vs[(k+1)%len(vs)]))) for k in range(len(vs))}

def pairrow(root,target,w):
 root=tuple(map(tuple,root));rv=set(root);re=edgelist(root)
 mayer=F(0);influence=F(0)
 for q in variants(target):
  vs=set(q);es=edgelist(q)
  shifts={(x-u,y-v) for x,y in rv for u,v in vs}
  for dx,dy in shifts:
   shifted={(x+dx,y+dy) for x,y in vs}
   shiftedE={tuple(sorted(((x+dx,y+dy),(u+dx,v+dy)))) for (x,y),(u,v) in es}
   delta=F(0) if re&shiftedE else F(3,5)**len(rv&shifted)
   mayer+=1-delta
   influence+=w*(1-delta)/((1+w)*(1+delta*w))
 return mayer,influence
if __name__=='__main__':
 cat=json.loads(CAT.read_text());n=len(cat)
 rows=[];B=np.zeros((n,n));C=np.zeros_like(B)
 for i,r in enumerate(cat):
  row=[]
  for j,s in enumerate(cat):
   w=F(s['activity']);m,b=pairrow(r['cyclic_vertices'],s['cyclic_vertices'],w)
   if i==j:b-=w/(1+w) # A heat-bath update does not depend on its own old bit.
   row.append(str(b));B[i,j]=float(b);C[i,j]=float(m*w)
  rows.append(row)
  if i%10==0:print('row',i,n,flush=True)
 eig,U=np.linalg.eig(B);idx=np.argmax(eig.real);v=U[:,idx].real;v*=np.sign(v.sum());v/=min(v)
 result={'number_types':n,'max_length':12,'perron_root_sharp':float(eig[idx].real),'perron_root_crude_with_self':float(max(np.linalg.eigvals(C).real)),
  'matrix_exact':rows,'perron_vector':v.tolist(),'catalog':str(CAT.name),
  'scope':'Truncated loop-type influence suboperator. Omitted longer loops forbid any full contraction conclusion.'}
 np.savez_compressed(OUT/'crossed_loop_influence_l12.npz',B=B,C=C)
 (OUT/'crossed_loop_influence_l12.json').write_text(json.dumps(result,indent=2)+'\n')
 print({k:result[k] for k in ['number_types','perron_root_sharp','perron_root_crude_with_self']},flush=True)

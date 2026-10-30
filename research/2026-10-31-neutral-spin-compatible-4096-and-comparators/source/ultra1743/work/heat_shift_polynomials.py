"""Exact acoustic-centered coordinates, avoiding numerical root cancellation."""
from pathlib import Path
from fractions import Fraction as R
from math import comb
from decimal import Decimal,getcontext
import json,pickle,numpy as np,time
root=Path(__file__).resolve().parents[1];start=time.perf_counter();d=pickle.load((root/'work/heat_exact_schur.pkl').open('rb'));s=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());e0,f0=map(R,s['ray']['canonical_zero']);getcontext().prec=35
def shift(p):
 q={}
 for (a,b,c),v in p.items():
  for i in range(a+1):
   for j in range(b+1):
    ee=(i,j,c);q[ee]=q.get(ee,R(0))+v*comb(a,i)*comb(b,j)*e0**(a-i)*f0**(b-j)
 return {ee:v for ee,v in q.items() if v}
arrays={}
for name in ('charts','physical_charts'):
 ds=[];n=len(d[name][0]);arr=np.zeros((4,n,n,9,9,5))
 for ch,M in enumerate(d[name]):
  MM=[[shift(p) for p in row] for row in M];ds.append(MM)
  if name=='physical_charts':
   assert all(a+b>=2 for a,b,c in MM[0][0])
   assert all(a+b>=1 for p in MM[0][1:] for a,b,c in p)
  for i in range(n):
   for j in range(n):
    for ee,v in MM[i][j].items():arr[(ch,i,j)+ee]=float(v)
 d[name+'_centered']=ds;arrays[name]=arr
 print('shifted',name,flush=True)
with (root/'work/heat_exact_schur.pkl').open('wb') as fp:pickle.dump(d,fp)
np.savez(root/'work/heat_centered_float.npz',**arrays)
print('centering seconds',time.perf_counter()-start,flush=True)

#!/usr/bin/env python3
from collections import defaultdict
from itertools import product,combinations
from fractions import Fraction as F
from pathlib import Path
import sys,json,time,resource
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'representation'))
from four_call_representation import history,charge

def probe(n):
 t0=time.perf_counter();words=list(product((0,1,2),repeat=n));baths=list(product((1,2),repeat=n))
 masks=[0]+[1<<j for j in range(n)]+[(1<<j)|(1<<k) for j,k in combinations(range(n),2)]
 groups=defaultdict(list)
 for i,x in enumerate(words):
  for u,bath in enumerate(baths):
   for mask in masks:
    y,seed,w,r=history(x,0,bath,mask)
    groups[(charge(x),y,seed,w)].append((i,u,r))
 D=defaultdict(int)
 for (q,y,seed,w),ps in groups.items():
  delta=len(w)-n
  if not delta:continue
  for i,u,r in ps:
   for j,v,s in ps:
    if r+s==2:D[i,u,j,v]+=delta*(1 if r==s else -1)
 D={key:v for key,v in D.items() if v}
 H=defaultdict(int)
 for (i,u,j,v),val in D.items():
  if u==v and i!=j:H[i,j]+=val
 H={ij:v for ij,v in H.items() if v}
 T=defaultdict(int)
 for (i,u,j,v),val in D.items():
  if (j,i) in H:T[u,v]-=val*H[j,i]*(1<<(n-charge(words[i])))
 T={ij:v for ij,v in T.items() if v}
 denom=1<<(3*n);mat=np.zeros((1<<n,1<<n))
 for (u,v),val in T.items():mat[u,v]=val/denom
 eig=np.linalg.eigvalsh(mat)
 var=F(sum(v*v*(1<<(n-charge(words[i]))) for (i,j),v in H.items()),1<<(4*n))
 d=[F(T.get((i,i),0),denom) for i in range(1<<n)]
 off=[(i,j,F(v,denom)) for (i,j),v in T.items() if i!=j]
 return {'n':n,'F_variance':str(var),'T_diagonal_values':sorted(set(map(str,d))),'offdiag_count':len(off),'max_offdiag':max([abs(float(v)) for _,_,v in off] or [0]),'T_eigen_range':[float(eig[0]),float(eig[-1])],'negative_margin':float(-eig[-1]),'candidate_A_per_call':float((eig[-1]**2)*np.log(2)/(8*float(var)*n)) if eig[-1]<0 else 0,'wall_seconds':time.perf_counter()-t0,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},words,H,T,D
if __name__=='__main__':
 out=[]
 for n in range(2,6):
  r,*_=probe(n);out.append(r);print(json.dumps(r),flush=True)
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')

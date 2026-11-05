"""Certified finite-memory upper bounds for square-lattice trails with factor3/5
per four-leg self-contact. Unremembered edge reuse and contacts are relaxed,
so the automaton upper-bounds true weighted trails. Perron vector numerical
selection is followed by exact integer Collatz inequalities.
"""
import numpy as np
from fractions import Fraction
import math,json,time,sys
D=((1,0),(0,1),(-1,0),(0,-1))
def edge(a,b):return tuple(sorted((a,b)))
def enumerate_states(m):
 states=[]
 def dfs(ds,ps,used):
  if len(ds)==m:states.append(tuple(ds));return
  x,y=ps[-1]
  for k,(dx,dy) in enumerate(D):
   p=(x+dx,y+dy);e=edge(ps[-1],p)
   if e not in used:dfs(ds+[k],ps+[p],used|{e})
 dfs([0],[(0,0),(1,0)],{((0,0),(1,0))})
 return states

def build(m):
 states=enumerate_states(m);ix={d:i for i,d in enumerate(states)}
 targets=np.zeros((len(states),3),dtype=np.int64)
 weights=np.zeros_like(targets)
 for i,ds in enumerate(states):
  ps=[(0,0)]
  for d in ds:ps.append((ps[-1][0]+D[d][0],ps[-1][1]+D[d][1]))
  used={edge(ps[k],ps[k+1]) for k in range(m)}
  internal=set(ps[1:-1]);x,y=ps[-1];j=0
  for k,(dx,dy) in enumerate(D):
   p=(x+dx,y+dy)
   if edge(ps[-1],p) in used:continue
   new=ds[1:]+(k,);rot=new[0];new=tuple((d-rot)%4 for d in new)
   targets[i,j]=ix[new]
   weights[i,j]=3 if p in internal else 5
   j+=1
 return states,targets,weights

def run(m):
 start=time.perf_counter();states,to,w=build(m);v=np.ones(len(states))
 for it in range(3000):
  av=(w*v[to]).sum(1)/5
  av/=max(av)
  if max(abs(av-v))<1e-13:v=av;break
  v=av
 # Strictly positive rational super-eigenvector and rational upper bound.
 vi=np.maximum(1,np.rint(v*10**9)).astype(np.int64)
 num=(w*vi[to]).sum(1);den=5*vi
 alpha_num=math.ceil(float(max(num/den))*10**6)+1
 assert np.all(num*10**6<=den*alpha_num)
 alpha=Fraction(alpha_num,10**6)
 # Sum over any lengthn>=m prefix weights is bounded by
 # [4 sum(v_i)/min(v_i)] alpha^(n-m); contact omissions only increase weights.
 prefactor=Fraction(4*sum(map(int,vi)),int(min(vi)))
 record=dict(memory_edges=m,states=len(states),iterations=it+1,growth_upper=str(alpha),growth_upper_decimal=float(alpha),log_tilt_available=math.log(3/float(alpha)),prefactor=str(prefactor),elapsed_sec=time.perf_counter()-start,min_v=int(min(vi)),max_v=int(max(vi)))
 np.savez_compressed(f'trail_certificate_m{m}.npz',targets=to,weights=w,v=vi,alpha_num=alpha_num,alpha_den=10**6)
 print(json.dumps(record),flush=True)
 return record
if __name__=='__main__':
 ms=list(map(int,sys.argv[1:])) or [6,8,10,12]
 results=[run(m) for m in ms]
 with open('weighted_trail_results.json','w') as f:json.dump(results,f,indent=2)

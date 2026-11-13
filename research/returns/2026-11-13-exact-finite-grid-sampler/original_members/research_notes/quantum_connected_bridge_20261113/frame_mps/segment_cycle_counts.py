import numpy as np,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'frame_sampler'))
from sampler import plan,UF

def grid(w,d):
 p=[]
 for a in[0,1]:p.append([(y*w+x,y*w+x+1) for y in range(w) for x in range(a,w-1,2)])
 for a in[0,1]:p.append([(y*w+x,(y+1)*w+x) for y in range(a,w-1,2) for x in range(w)])
 return[p[t%4] for t in range(d)]
def count(n,records):
 uf=UF(n);cur=list(range(n));K=0;Q=0;resets=0
 for ev,_,_,_ in records:
  for(u,v),reset,rare,cand in ev:
   if rare:
    Q+=1
    if uf.root(cur[u])==uf.root(cur[v]):K+=1
    else:uf.union(cur[u],cur[v])
  for(u,v),reset,rare,cand in ev:
   if reset:
    resets+=1;cur[u]=uf.add();cur[v]=uf.add()
 return dict(cycle_rank=K,rare=Q,resets=resets,segments=len(uf.p))
if __name__=='__main__':
 rows=[]
 for w in[4,16,32]:
  for e in[.02,.05]:
   for seed in range(10):
    rec,*_=plan(w*w,grid(w,100),.03,e,np.random.default_rng(50000+seed));rows.append(dict(width=w,eps=e,seed=50000+seed,**count(w*w,rec)))
 Path(__file__).with_name('segment_cycle_counts.json').write_text(json.dumps(rows,indent=2))
 for w in[4,16,32]:
  for e in[.02,.05]:
   a=[x['cycle_rank'] for x in rows if x['width']==w and x['eps']==e];print(w,e,a)

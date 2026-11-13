"""Future-aware Z cuts from reset-segment cycle-space signatures."""
from segment_cycle_sampler import graph

def gf2rank(rows):
 piv={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)

def schedule(n,records,metrics=False):
 Q,cycles=graph(n,records);rows=[0]*Q
 for k,c in enumerate(cycles):
  while c:
   lb=c&-c;rows[lb.bit_length()-1]|=1<<k;c^=lb
 sig=[0]*n;qi=0;cuts=[];trace=[];active=[False]*n
 for t,(ev,_,_,_) in enumerate(records):
  touched=set()
  for(u,v),reset,rare,cand in ev:
   if rare:
    sig[u]^=rows[qi];sig[v]^=rows[qi];qi+=1;touched|={u,v};active[u]=active[v]=True
  now={s for s in touched if sig[s]==0};cuts.append(now)
  for s in now:active[s]=False
  if metrics:trace.append(dict(layer=t,quantum_sites=sum(active),signature_rank=gf2rank(sig)))
  for(u,v),reset,rare,cand in ev:
   if reset:
    assert sig[u]==sig[v]==0
    sig[u]=sig[v]=0;active[u]=active[v]=False
 assert not any(sig)
 return cuts,dict(K=len(cycles),Q=Q,trace=trace)
if __name__=='__main__':
 import numpy as np,json
 from pathlib import Path
 from segment_cycle_counts import grid
 from sampler import plan
 from ordering import last_q_sites
 rows=[]
 for w in[16,32]:
  for eps in[.02,.05]:
   for seed in range(5):
    rec,*_=plan(w*w,grid(w,100),.03,eps,np.random.default_rng(80000+seed));cuts,meta=schedule(w*w,rec,True);last=last_q_sites(w*w,rec)
    rows.append(dict(width=w,eps=eps,seed=seed,K=meta['K'],max_quantum=max(t['quantum_sites'] for t in meta['trace']),max_rank=max(t['signature_rank'] for t in meta['trace']),additional_cuts=sum(len(a-b) for a,b in zip(cuts,last))))
 Path(__file__).with_name('cycle_cut_counts.json').write_text(json.dumps(rows,indent=2));print(rows)

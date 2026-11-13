"""Exact flag-based upper-bound graph for Z-affine-support simulation.
Does NOT execute quantum amplitudes. No independent factorization after measurements.
"""
import sys,json,time
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path('research_notes/quantum_connected_bridge_20261113/frame_mps').resolve()))
from mps_sampler import plan
from ordering import last_q_sites

def layers(w,T):
 L=[]
 for axis,p in [(0,0),(0,1),(1,0),(1,1)]:
  E=[]
  for y in range(w):
   for x in range(w):
    if axis==0 and x%2==p and x+1<w:E.append((y*w+x,y*w+x+1))
    if axis==1 and y%2==p and y+1<w:E.append((y*w+x,(y+1)*w+x))
  L.append(E)
 return [L[i%4] for i in range(T)]

def probe(n,records,early=True):
 pc=[{i} for i in range(n)];qc=[None]*n;last=last_q_sites(n,records);peakm=peakw=peakglobalm=0;infers=0
 def qmerge(u,v):
  a=qc[u] or {u};b=qc[v] or {v};merged=a|b
  for w in merged:qc[w]=merged
 def remove(w):
  if qc[w] is None:return
  old=qc[w];new=old-{w};qc[w]=None
  for s in new:qc[s]=new
 def measure(v):
  nonlocal infers
  a=pc[v]
  if len(a)==1:return
  rest=a-{v};pc[v]={v}
  for w in rest:pc[w]=rest
  remove(v)
  if len(rest)==1:
   w=next(iter(rest));remove(w);infers+=1
 def ledger():
  nonlocal peakm,peakw,peakglobalm
  groups={id(x):x for x in qc if x is not None};mvals=[]
  for group in groups.values():
   # Each active parity component is wholly contained in its quantum group.
   pcomps={id(pc[v]) for v in group};m=len(group)-len(pcomps)
   assert all(pc[v]<=group for v in group)
   mvals.append(m);peakm=max(peakm,m);peakw=max(peakw,len(group))
  peakglobalm=max(peakglobalm,sum(mvals))
 for t,(events,_,_,_) in enumerate(records):
  for (u,v),reset,rare,cand in events:
   if not reset and len(pc[u])>1 and len(pc[v])>1:qmerge(u,v)
  for (u,v),reset,rare,cand in events:
   if not rare:continue
   qmerge(u,v)
   if pc[u] is not pc[v]:
    merged=pc[u]|pc[v]
    for w in merged:pc[w]=merged
   ledger()
  if early:
   for v in sorted(last[t]):measure(v)
  for (u,v),reset,rare,cand in events:
   if reset:measure(u);measure(v)
  ledger()
 return dict(max_group_logical_qubits=peakm,max_group_physical_qubits=peakw,max_total_logical_qubits=peakglobalm,inferred_basis_retirements=infers)

if __name__=='__main__':
 start=time.time();rows=[]
 for width in [16,32]:
  for eps in [.02,.05]:
   vals=[]
   for seed in range(100):
    records,*_=plan(width*width,layers(width,100),.03,eps,np.random.default_rng(29100+seed));vals.append(probe(width*width,records))
   rows.append(dict(n=width*width,T=100,r=.03,epsilon=eps,trials=100,mean_group_logical=float(np.mean([v['max_group_logical_qubits'] for v in vals])),max_group_logical=max(v['max_group_logical_qubits'] for v in vals),mean_group_physical=float(np.mean([v['max_group_physical_qubits'] for v in vals])),max_group_physical=max(v['max_group_physical_qubits'] for v in vals),raw=vals))
 out={'rows':rows,'seconds':time.time()-start,'scope':'Flag-graph resource upperbounds only. Affine support dimension not exact magic or actual nonzero-amplitude count; no quantum samples generated; no tail/scaling claim.'}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps([{k:v for k,v in a.items() if k!='raw'} for a in rows],indent=2))

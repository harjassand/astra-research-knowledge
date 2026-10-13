"""Error-jet driven finite-basis discovery. Selection is heuristic, certification is separate."""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
from collections import defaultdict
import numpy as np
from jet_solver import JetSolver
from fast_algebra import build,basis

def key(w):return ((w[0]|w[1]).bit_length(),w)
def enrich(s:JetSolver,fs,gs,cap=2500,maxspan=18,weights=(1.,1.,.3)):
    scoreF=defaultdict(float);scoreG=defaultdict(float)
    # Use the full objective gradients, including diagonal pressure rows.
    for k,weight in enumerate(weights):
      if k>=len(fs):break
      po=s.AG@gs[k];qe=s.AF@fs[k]
      po[s.fidx]+=s.qf*fs[k];qe[s.gidx]+=s.qg*gs[k]
      if k==0:po-=s.j
      else:po+=k*(s.BG@gs[k-1]);qe+=k*(s.BF@fs[k-1])
      def action(rows,coeff,inv):
        keep=np.flatnonzero(np.abs(coeff)>1e-11)
        rw=[rows[i] for i in keep];co=coeff[keep]*inv[keep]
        rr,AA=build(rw,**{q:s.params[q] for q in ['t','U','V']})
        return rr,AA@co
      ar1,ac1=action(s.orr,po,s.io);ar2,ac2=action(s.er,qe,s.ie)
      gf=defaultdict(float,zip(s.orr,po));gg=defaultdict(float,zip(s.er,qe))
      for w,c in zip(ar2,ac2):gf[w]-=c
      for w,c in zip(ar1,ac1):gg[w]-=c
      for w,c in gf.items():
        if w[0] and (w[0]|w[1]).bit_length()<=maxspan:
          scoreF[w]+=weight*c*c/max(1,w[0].bit_count())
      for w,c in gg.items():
        if (w[0]|w[1]).bit_length()<=maxspan:
          scoreG[w]+=weight*c*c/max(1,w[0].bit_count())
    out=[]
    for score,old in [(scoreF,s.fw),(scoreG,s.gw)]:
      existing=set(old);cand=sorted(((v,w) for w,v in score.items() if w not in existing and v>1e-24),reverse=True)[:cap]
      out.append(sorted(existing|{w for v,w in cand},key=key))
    return out

def run(V,out,steps=5,cap=2500,start=None,L=8,order=2,maxspan=18):
 root=Path(out);root.mkdir(parents=True,exist_ok=True)
 if start:
  q=np.load(start);fw=[tuple(map(int,w)) for w in q['fw']];gw=[tuple(map(int,w)) for w in q['gw']]
 else:fw=basis(L,1);gw=basis(L,0)
 begin=time.perf_counter();summary=[]
 for step in range(steps+1):
  s=JetSolver(fw,gw,V=V)
  name=root/f'step{step}'
  rec=s.solve(order=order,output=name)
  summary.append(rec)
  (root/'summary.json').write_text(json.dumps(dict(V=V,seconds=time.perf_counter()-begin,steps=summary),indent=2))
  if step<steps:
   data=np.load(str(name)+'.npz');fw,gw=enrich(s,data['fs'],data['gs'],cap,maxspan)
 return summary
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--V',type=float,default=2.21875);p.add_argument('--out',required=True);p.add_argument('--steps',type=int,default=5);p.add_argument('--cap',type=int,default=2500);p.add_argument('--start');p.add_argument('--L',type=int,default=8);p.add_argument('--order',type=int,default=2);p.add_argument('--maxspan',type=int,default=18);a=p.parse_args();run(a.V,a.out,a.steps,a.cap,a.start,a.L,a.order,a.maxspan)

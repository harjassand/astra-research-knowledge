"""Classical record bookkeeping regression, NOT a quantum probability simulation.
Tests combined-LAST birth, all-T depth-two endpoints, bounded descendants,
and per-owner disjointness when selecting one path per distinct root.
"""
from random import Random
from collections import defaultdict
from pathlib import Path
import json
rng=Random(20261030);bA=bB=cAB=2;B=bA+bB+bA*cAB
maxoffs=0;intervalchecks=0;via_dirty_abort=0
for run in range(500):
    ma=[None]*3; mb=[False]*3; sb=[False]*3; cause=[None]*3
    roots={};desc=defaultdict(list);emissions=[]
    for t in range(1,501):
        op=rng.randrange(7)
        if op<3:
            rid=len(roots);roots[rid]=t;e=rng.randrange(3)
            for a in [e,(e+1)%3]:ma[a]=(rid,t)
            for b in [e,(e+2)%3]:mb[b]=True;cause[b]=(rid,[(('B',b),t,None)])
        elif op<5:
            a=rng.randrange(3)
            if ma[a] is not None:
                rid,tau=ma[a];path=[(('A',a),tau,t)]
                desc[rid].append((t,path));emissions.append((rid,t,path,'A'))
                for b in [a,(a+1)%3]:
                    sb[b]=True;cause[b]=(rid,path+[(('B',b),t,None)])
            ma[a]=None
        else:
            b=rng.randrange(3);success=bool(rng.randrange(2));charged=mb[b] or (sb[b] and success)
            if charged:
                rid,pending=cause[b];path=[(owner,start,t if end is None else end) for owner,start,end in pending]
                desc[rid].append((t,path));emissions.append((rid,t,path,'B'))
                if len(path)==2 and mb[b] and not success:via_dirty_abort+=1
            mb[b]=sb[b]=False;cause[b]=None
    for rid,entries in desc.items():
        maxoffs=max(maxoffs,len(entries));assert len(entries)<=B
    for trial in range(20):
        lo=rng.randrange(1,450);hi=lo+rng.randrange(1,51)
        chosen=[]
        for rid,tau in roots.items():
            if lo<=tau<hi:chosen.append((rid,[]));continue
            eligible=[p for t,p in desc[rid] if lo<=t<hi]
            if eligible:chosen.append((rid,rng.choice(eligible)))
        byowner=defaultdict(list)
        for rid,path in chosen:
            for owner,start,end in path:byowner[owner].append((start,end,rid))
        for owner,segments in byowner.items():
            segments.sort()
            for left,right in zip(segments,segments[1:]):
                assert left[1]<=right[0],(run,owner,left,right)
                intervalchecks+=1
assert via_dirty_abort>0
out={'histories':500,'events_per_history':500,'selected_window_trials':10000,'offspring_bound':B,'maximum_observed_reset_descendants':maxoffs,'selected_interval_disjointness_checks':intervalchecks,'depth_two_mechanical_dirty_abort_endpoints':via_dirty_abort,'all_checks_pass':True,'scope':'record invariants only; no quantum-survival or Poisson-intensity probability claim'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

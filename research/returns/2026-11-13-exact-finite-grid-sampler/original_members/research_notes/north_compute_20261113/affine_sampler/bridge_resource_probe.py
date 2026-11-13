import sys,time,json,statistics
from pathlib import Path
import numpy as np
from resource_probe import layers,probe,plan
sys.path.insert(0,str(Path('research_notes/north_compute_20261113/bridge_dephasing').resolve()))
from check import bridge_indices
rows=[]
for width in [16,32]:
 for eps in [.02,.05]:
  data=[];start=time.time()
  for seed in range(30):
   records,*_=plan(width*width,layers(width,100),.03,eps,np.random.default_rng(49300+seed));events=[(u,v,'R' if reset else 'Q' if rare else 'D') for ev,*_ in records for (u,v),reset,rare,cand in ev];bridges=bridge_indices(width*width,events)
   modified=[];index=0
   for ev,cuts,before,after in records:
    changed=[]
    for e,reset,rare,cand in ev:changed.append((e,reset,rare and index not in bridges,cand));index+=1
    modified.append((changed,cuts,before,after))
   # Sampled productXX bridge flips alter signs, not parity-partition/rank resources.
   a=probe(width*width,modified);a['seed']=49300+seed;a['removed_bridge_Q']=len(bridges);data.append(a)
  summary={key+'_mean':statistics.mean(x[key] for x in data) for key in data[0] if key!='seed'};summary['max_group_logical_qubits_max']=max(x['max_group_logical_qubits'] for x in data)
  rows.append(dict(n=width*width,T=100,r=.03,epsilon=eps,trials=30,seconds=time.time()-start,summary=summary,raw=data));print(width,eps,summary,flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps({'rows':rows,'scope':'Flag-only exact-resource-envelope probe after bridge dephasing. No amplitudes computed, no tail guarantee; ordinaryD still merges uncertain entanglement groups.'},indent=2))

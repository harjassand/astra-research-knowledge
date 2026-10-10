import sys,math,json,numpy as np
sys.path.insert(0,'work/continuation_03/reports/e4_zero_support')
from gaussian_reference_full_mean_probe import gap
rng=np.random.default_rng(8923161)
out={'status':'floating-point search, no rigorous certificate','rows':[]}
for eta in [.750001,.7501,.751,.752,.755,.76,.762,.765,.77]:
    best=(float('inf'),None);valid=0
    for i in range(16000):
        u=.5+10**rng.uniform(-8,-.5)
        w=.5+10**rng.uniform(-.2,3.5)
        rr=10**rng.uniform(-5,-.1)
        sa=10**rng.uniform(-2,2)
        v=gap(eta,u,w,rr,sa)
        if v is None:continue
        valid+=1
        if v<best[0]:best=(v,[u,w,rr,sa])
    row={'eta':eta,'valid':valid,'gap':best[0],'parameters':best[1]};out['rows'].append(row);print(json.dumps(row),flush=True)
with open('work/continuation_03/reports/e4_zero_support/gaussian_reference_target_probe.json','w') as f:json.dump(out,f,indent=2)

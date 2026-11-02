#!/usr/bin/env python3
"""Run independent synthetic end-to-end campaigns; preserve stochastic variation."""
import json
from pathlib import Path
import numpy as np
from pooled_photonic_selection_v2 import run
from heritable_photonic_matter_v3 import OPT, STRESS

def stats(a):
    a=np.array(a,dtype=float)
    return dict(mean=float(a.mean()),p05=float(np.quantile(a,.05)),p95=float(np.quantile(a,.95)))
records=[]
for sc in (OPT,STRESS):
    group=[]
    for i in range(7):
        r=run(20261103+i*31,sc,0.05,1000,2)
        group.append(r)
    records+=group
    print(sc.name,flush=True)
    for k in ('fresh_reexpressed_AE_weighted_pool','fresh_reexpressed_AE_uniform_pool','fresh_reexpressed_AE_incumbent_direct_geometric'):
        print(' ',k,stats([r[k] for r in group]),flush=True)
    print(' near3 after two rounds',stats([r['rounds'][-1]['high_three_near_after'] for r in group]),flush=True)
Path('/mnt/data/pooled_photonic_selection_v2_replicate_results.json').write_text(json.dumps(records,indent=2))

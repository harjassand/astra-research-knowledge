#!/usr/bin/env python3
"""Post-primary common-60 sensitivity. Labels absent from records remain unknown."""
from pathlib import Path
from collections import defaultdict
import csv, json
BASE=Path(__file__).resolve().parent
rows=list(csv.DictReader((BASE/'ROOT_ATTEMPT_ROWS.csv').open()))
result={}
for name in sorted({r['run'] for r in rows}):
    rs=[r for r in rows if r['run']==name]
    detail=[]
    for r in rs:
        py,cy,pu,cu=[int(r[k]) for k in ('parent_successes_60','child_successes_60','parent_unknown_60','child_unknown_60')]
        detail.append({'child':r['child'],'parent':r['parent'],'admitted':r['native_admitted']=='True',
                       'parent_interval':[py,py+pu], 'child_interval':[cy,cy+cu],
                       'delta_interval':[cy-py-pu,cy+cu-py],
                       'almost_complete':pu<=3 and cu<=3})
    selected=[r for r in detail if r['almost_complete']]
    admitted=[r for r in detail if r['admitted']]
    result[name]={
        'all_attempts':len(rs),
        'pairs_at_least_57_of_60_each':len(selected),
        'definite_gain_among_almost_complete':sum(r['delta_interval'][0]>0 for r in selected),
        'definite_loss_among_almost_complete':sum(r['delta_interval'][1]<0 for r in selected),
        'ambiguous_or_tie_among_almost_complete':sum(r['delta_interval'][0]<=0<=r['delta_interval'][1] for r in selected),
        'sum_delta_lower_among_almost_complete':sum(r['delta_interval'][0] for r in selected),
        'sum_delta_upper_among_almost_complete':sum(r['delta_interval'][1] for r in selected),
        'admitted_common60_top_lower':max([r['child_interval'][0] for r in admitted]+[12]),
        'admitted_common60_top_upper':max([r['child_interval'][1] for r in admitted]+[14]),
        'admitted_common60_top_lower_agent':max(admitted,key=lambda r:r['child_interval'][0]),
        'individual_pairs':detail}
out={'scope':'Post-primary sensitivity, selected after metadata inspection. Missing evaluation tiers prevent an unconditional common-60 ranking.',
     'selection':'At least57 known labels in BOTH parent and child. This is outcome-dependent survivor selection; no causal rate.',
     'runs':result}
(BASE/'ROOT_SENSITIVITY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({n:{k:v for k,v in d.items() if k!='individual_pairs'} for n,d in result.items()},indent=2))

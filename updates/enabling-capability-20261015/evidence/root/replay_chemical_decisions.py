"""Independent root arithmetic on source-derived extracted observations.
This checks descriptive counts, not chemical accuracy or independence.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,math,time
P=Path(__file__).resolve().parents[1]
p=P/'workers/chemistry_search/MEASURED_YIELDS.json'
b=p.read_bytes(); data=json.loads(b); cols=data['columns']; rows=[dict(zip(cols,x)) for x in data['rows']]
t=time.perf_counter()
assert len(rows)==50688 and len({r['reaction_id'] for r in rows})==50688
out={'scope':'Root reconstruction of descriptive decisions using producer-derived labels; NOT assay validation','derived_input_sha256':hashlib.sha256(b).hexdigest(),'source_parquet_sha256':hashlib.sha256((P/'workers/chemistry_search/ord_dataset-805ad863feef48579d95d86a728035f4.parquet').read_bytes()).hexdigest(),'rows':len(rows),'groups':{}}
for name,rr in [('all',rows),('no_metal',[r for r in rows if r['no_metal']]),('metal',[r for r in rows if not r['no_metal']])]:
 valid=[r for r in rr if math.isfinite(r['target_yield_pct']) and math.isfinite(r['side_yield_pct']) and r['target_yield_pct']>=0 and r['side_yield_pct']>=0 and r['target_yield_pct']+r['side_yield_pct']<=100]
 apparent=[r for r in valid if r['target_yield_pct']+r['side_yield_pct']>=50]
 good=[r for r in valid if r['target_yield_pct']>=50 and r['target_yield_pct']/(r['target_yield_pct']+r['side_yield_pct'])>=.95]
 out['groups'][name]={'count':len(rr),'admissible_nonnegative_sum_le_100':len(valid),'negative':sum(min(r['target_yield_pct'],r['side_yield_pct'])<0 for r in rr),'sum_over_100':sum(r['target_yield_pct']+r['side_yield_pct']>100 for r in rr),'combined_ge_50':len(apparent),'combined_ge_50_but_desired_below_50':sum(r['target_yield_pct']<50 for r in apparent),'target_ge_50_and_reported_fraction_ge_95':len(good),'combined_ge_50_failing_joint_target':len(apparent)-len(good)}
assert out['groups']['all']['admissible_nonnegative_sum_le_100']==50518
assert out['groups']['all']['combined_ge_50']==276
assert out['groups']['all']['combined_ge_50_but_desired_below_50']==199
assert out['groups']['all']['combined_ge_50_failing_joint_target']==211
assert out['groups']['no_metal']['count']==6336
assert out['groups']['no_metal']['target_ge_50_and_reported_fraction_ge_95']==0
assert out['groups']['metal']['target_ge_50_and_reported_fraction_ge_95']==65
out['wall_seconds']=time.perf_counter()-t
out['passed']=True
out['qualifiers']=['Exploratory descriptive thresholds, not preregistration or error-rate inference','Unphysical reported pairs retained in source and separately counted; never clipped','Selectivity among two reported components is not total purity or isolated recovery','Zero labels do not establish absence below detection','Prior source already reports separate desired/side yields and their treatment effects']
(P/'root/CHEMISTRY_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

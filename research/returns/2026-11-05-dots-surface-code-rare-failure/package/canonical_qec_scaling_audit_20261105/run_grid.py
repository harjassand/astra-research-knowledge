from pathlib import Path
import sys,random,json,time,gc
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'canonical_qec_witness_20261105'))
from sampler import Model,Proposal
rows=[]
for j,p in enumerate([F(1,10000),F(1,1000),F(1,200)]):
 for i,d in enumerate([13,25,41,61]):
  t=time.perf_counter();m=Model(d);q=Proposal(m,p,max(55,3*d));setup=time.perf_counter()-t
  rng=random.Random(2026110500+100*j+i);counts={k:0 for k in ['accepted','nonsimple','not_failure','other_witness']}; t=time.perf_counter()
  for k in range(2000):
   _,why=q.trial(rng);counts[why]+=1
  row={'d':d,'p':str(p),'shots':2000,'Lmax':q.Lmax,'counts':counts,'acceptance':counts['accepted']/2000,'Z':float(q.Z),'tail':float(q.tail),'tail_over_Z':float(q.tail/q.Z),'setup_seconds':setup,'sampling_seconds':time.perf_counter()-t}
  rows.append(row);print(json.dumps(row),flush=True)
  Path(__file__).with_name('square_grid_results.json').write_text(json.dumps({'scope':'exploratory fixed-grid diagnostics, not confidence claims','rows':rows},indent=2)+'\n')
  del q,m;gc.collect()

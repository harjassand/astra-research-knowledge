from sampler import Model,Proposal
from fractions import Fraction as F
from pathlib import Path
import random,time,json,sys
# Predeclared diagnostic only: observed acceptance and time, no new confidence claim.
rows=[]
for d in [5,9,17,25,41]:
 start=time.perf_counter();m=Model(d);q=Proposal(m,F(1,1000),max(55,3*d));setup=time.perf_counter()-start
 rng=random.Random(2026110500+d);counts={k:0 for k in ['accepted','nonsimple','not_failure','other_witness']}
 for i in range(1000):v,why=q.trial(rng);counts[why]+=1
 row={'d':d,'qubits':len(m.edges),'p':str(q.p),'Lmax':q.Lmax,'shots':1000,'counts':counts,'Z':float(q.Z),'tail_bound':float(q.tail),'point_estimate_diagnostic':float(q.Z)*counts['accepted']/1000,'setup_seconds':setup,'sampling_seconds':time.perf_counter()-start-setup,'total_seconds':time.perf_counter()-start}
 rows.append(row);print(json.dumps(row),flush=True)
 Path(__file__).with_name('scaling_screen.json').write_text(json.dumps({'scope':'predeclared exploratory scaling screen, no confidence claim','rows':rows},indent=2)+'\n')

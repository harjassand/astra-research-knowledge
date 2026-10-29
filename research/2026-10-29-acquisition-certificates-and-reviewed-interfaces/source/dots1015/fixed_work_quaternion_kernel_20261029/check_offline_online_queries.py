"""OFFLINE query-quality replay, not a new source/action trajectory."""
import json,time,hashlib
from pathlib import Path
from fractions import Fraction as F
from fixed_work_oracle import solve,verify,exps
r=Path(__file__).parent;src=Path('producer-workspace/online_ftpl_result.json');j=json.load(open(src));rows=[];st=time.time();sums=[F(0)]*3
for tt,rr in enumerate(j['oracle_calls']):
 for e,record in enumerate(rr):
  query={a:F(v) for a,v in zip(exps,record['query'])};t=time.time();c=solve(query);assert verify(query,c);elapsed=time.time()-t;sums[e]+=F(c['gap']);old=record['certificate'];rows.append(dict(round=tt+1,edge=e,seconds=elapsed,certificate=c,old_gap=old['gap'],candidate_excess_vs_old_upper=str(F(c['upper'])-F(old['upper'])),lower_shortfall_vs_old_lower=str(F(old['lower'])-F(c['lower']))))
 if (tt+1)%10==0:print('round',tt+1,'elapsed',time.time()-st,flush=True)
T=j['T'];R=F(j['perturbation_radius']);out=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),source=str(src),rows=rows,per_edge_realized_gap_sums=list(map(str,sums)),per_edge_realized_gap_over_TR=[float(v/(T*R)) for v in sums],public_gap_bound=str(F(T*720,1)/F(1,3)+35*R),total_seconds=time.time()-st,scope='OFFLINE360 fixed query replay on previous controller trajectory. No fresh quantum source experiment, no actual-history/readiness inference for new actions, no expected-gap budget inferred from realized sums.')
(r/'offline_query_results.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='rows'},flush=True)

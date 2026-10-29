"""Independent memory-channel renewal audit of finite guard DP, not scalar iid model."""
import numpy as np,json
from pathlib import Path
src=Path('producer-workspace/sos_frame_guard_bridge_20261029');z=np.load(src/'maps_and_fixture.npz');sigma=z['sigma'].reshape(4);rows=[]
def tr(v):return (v[...,0]+v[...,3]).sum().real
for row in json.loads((src/'results.json').read_text())['rows']:
 name=row['candidate_policy']
 for r in row['guard_results']:
  six=r['test']=='six_state';s=r['s'];P=z[name+('_six_pass' if six else '_matching_pass')];S=z[name+'_service'];G=z[name+('_completed_good' if six else '_raw_good')];B=S-G
  # Sum every possible run of passes before next service, keeping bath channel order.
  V=np.linalg.inv(np.eye(4)-(1-s)*P);Ag=s*G@V;Ab=s*B@V;A=Ag+Ab
  bath=sigma.copy();cost=0.;buckets=np.zeros((8,4),complex);buckets[0]=sigma
  for j in range(155):
   cost+=tr(V@bath);bath=A@bath
   nxt=buckets@Ag.T;nxt[1:]+=buckets[:-1]@Ab.T;nxt[-1]+=buckets[-1]@Ab.T;buckets=nxt
  accept=tr(bath);over=tr(buckets[-1]);cap=r['cap_abort']
  # Infinite continuation acceptance exceeds capped acceptance by <= live cap mass.
  assert abs(accept-r['acceptance'])<max(1e-11,2*cap)
  assert abs(cost-r['expected_native_calls'])<max(1e-9,2*cap*155/s)
  assert abs(over-r['accepted_bad_weight_above6'])<max(1e-12,2*cap)
  assert abs(tr(buckets)-accept)<1e-11
  rows.append({'policy':name,'test':r['test'],'uncapped_acceptance':float(accept),'finite_acceptance':r['acceptance'],'absolute_acceptance_difference':float(abs(accept-r['acceptance'])),'uncapped_expected_calls':float(cost),'expected_call_difference':float(abs(cost-r['expected_native_calls'])),'accepted_over6_difference':float(abs(over-r['accepted_bad_weight_above6'])),'cap_live_mass':cap})
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'Independent matrix-resolvent geometric-run sum retaining bath channel, all 8 candidate/test combinations','checks':rows},indent=2)+'\n');print(json.dumps(rows,indent=2))

"""Independent native-record calculation on actual three-role simulation; not acceptance."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from exact_threshold import upper_root

def rotation(q):
 w,x,y,z=map(F,q);assert w*w+x*x+y*y+z*z==1
 return [[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]]
p=Path('producer-workspace/bounded_live_probe_replay.json');j=json.loads(p.read_text());prob=F(j['p']);units=0;bits=40;count=0;checks=0
for call,certs in zip(j['calls'],j['oracle_calls']):
 if call['role']!='learn':continue
 raw=call['probe_raw'];a=raw['output_axes'];c=raw['input_axes'];y=raw['output_signs'];u=raw['input_signs'];W=F(0)
 for edge in range(3):
  i=edge+1;C=rotation(certs[edge]['certificate']['quaternion'])
  hat=F(3,4)-F(9,4)*y[i]*y[0]*C[a[i]][a[0]]-F(81,4)*y[i]*y[0]*u[i]*u[0]*C[a[i]][a[0]]*C[c[i]][c[0]]
  assert hat==F(call['selected_probe_estimates'][edge]);W+=hat/prob;checks+=1
 scaled=W*(1<<bits);rounded=-((-scaled.numerator)//scaled.denominator);assert F(rounded,1<<bits)>=W
 units+=rounded;count+=1
score=F(units,1<<bits);radius=F(45*3,prob)*upper_root(F(j['T']*20,2));bound=max(F(0),score+radius)
out=dict(source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),native_record_matches=checks,probe_count=count,reported_prequential_upper=str(score),reported_prequential_float=float(score),maximum_rounding_excess=str(F(count,1<<bits)),radius_exact=str(radius),radius_float=float(radius),selected_loss_upper=str(bound),selected_loss_upper_float=float(bound),simulator_actual_selected_loss_sum=sum(c['current_star_loss'] for c in j['calls']),trivial_loss_bound=3*j['T'],readiness_pass=False,scope='Three-role live simulation diagnostic only. Prequential loss bound holds for arbitrary other roles with inherited bank privacy, but no two-role quantum instrument was executed, no outer code or unknown payload. No acceptance/yield claim.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

import math, json
from pathlib import Path
def g(e):
 return ((1+e)*math.log1p(e)+(1-e)*math.log1p(-e))/2
out=[]
for e in [0.5,0.2,0.1,0.01,0.001,0.0001]:
 d=g(e)/2;err=e/4
 out.append({'e':e,'holevo_loss_nats':d,'optimal_EB_average_trace_distance':err,'ratio':err/math.sqrt(d)})
assert abs(out[-1]['ratio']-0.5)<1e-7
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)

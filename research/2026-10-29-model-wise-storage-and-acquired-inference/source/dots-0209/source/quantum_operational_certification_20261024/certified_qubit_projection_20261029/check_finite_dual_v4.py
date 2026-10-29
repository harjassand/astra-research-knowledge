from certified_projection_v4 import *
from pathlib import Path
import json,time
rng=np.random.default_rng(10629);results=[];start=time.time()
# Rational complex Hermitian inputs, including indefinite centers and both
# overloaded and underloaded active faces. Not an exhaustive theorem.
for power in [0,10,20,30,39]:
 for trial in range(12):
  Y=[[F(int(x),20) for x in row] for row in rng.integers(-8,15,size=(3,4))]
  mult=[1,1,1<<power]
  try:
   E,c=project_certified(Y,mult,F(1,10**9));c.update(K_power=power,trial=trial);results.append(c)
  except Exception as exc:
   results.append({'K_power':power,'trial':trial,'failure':repr(exc),'input_Y':[[str(x) for x in y] for y in Y],'multiplicities':[str(k) for k in mult]})
 out={'tested':len(results),'passed':sum(c.get('certified',False) for c in results),'elapsed':time.time()-start,'cases':results}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
 print(power,out['passed'],'/',out['tested'],flush=True)

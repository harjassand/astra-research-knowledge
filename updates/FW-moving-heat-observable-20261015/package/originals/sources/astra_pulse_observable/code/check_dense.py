import json,numpy as np
from compact_model import BASE,features,target
rs=json.loads((BASE/'results/compact_lp.json').read_text())[-2:]
x=np.geomspace(1e-14,1e14,200000); s=np.r_[0,x/(1+x),1.]
for r in rs:
 for key in ['lower','upper']:
  v=np.array(r[key]['weights']); f=np.array(r['frequencies']); sign=1 if key=='lower' else -1
  # Batched to keep memory bounded.
  out=[]
  for ss in np.array_split(s,20):
   F=features(ss,f); resid=sign*(target(ss,r['time_s'])-(v[:len(f)]@F.real+v[len(f):]@F.imag)); out.extend(resid)
  out=np.array(out); j=np.argmin(out); print(r['time_s'],key,'minresidual',out[j],'s',s[j],'tau',s[j]/(1-s[j])/(2*np.pi*.01))

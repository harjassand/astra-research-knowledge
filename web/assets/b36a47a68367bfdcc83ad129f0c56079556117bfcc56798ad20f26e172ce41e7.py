"""Single structured alignment U=I10 direct-sum (K direct-sum I4) direct-sum 1."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent))
from diagnostics import K,superop,choi,diagnostic
from sep_sdp import whiten
import numpy as np

a=superop(K);b=a.T
out={}
for name,m,d,e in [('S*S',b@a,10,10),('SS*',a@b,6,6),('SS*S',a@b@a,10,6)]:
    out[name]=diagnostic(m,d,e)
    j=choi(m,d,e);j/=np.trace(j);w,x,y=whiten(j,d,e)
    out[name]['whitened_hs_distance']=float(np.linalg.norm(w-np.eye(d*e)/(d*e)))
    out[name]['whitened_realignment_norm']=float(np.linalg.svd(w.reshape(d,e,d,e).transpose(0,2,1,3).reshape(d*d,e*e),compute_uv=False).sum())
print(json.dumps(out,indent=2))

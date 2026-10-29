"""Independent convention stress test; not a proof or solver performance result."""
import numpy as np
import json
from pathlib import Path
rng=np.random.default_rng(8274)
worst=0.0
for d,k in [(3,2),(2,3),(4,2)]:
 for trial in range(20):
  raw=rng.normal(size=(d*3,k))+1j*rng.normal(size=(d*3,k)); q,_=np.linalg.qr(raw)
  E=[q[i*d:(i+1)*d] for i in range(3)]
  raw=rng.normal(size=(k*3,d))+1j*rng.normal(size=(k*3,d)); q,_=np.linalg.qr(raw)
  R=[q[i*k:(i+1)*k] for i in range(3)]
  v=lambda a:a.reshape(-1)
  H=sum(np.outer(v(e.conj().T),v(e.conj().T).conj()) for e in E)
  K=sum(np.outer(v(r),v(r).conj()) for r in R)
  fe=sum(abs(np.trace(r@e))**2 for r in R for e in E)/k**2
  err=float(abs(np.trace(H@K)/k**2-fe)); worst=max(worst,err)
  J=sum(np.outer(v(e),v(e).conj()) for e in E)
  H2=J.reshape(d,k,d,k).transpose(1,0,3,2).reshape(k*d,k*d).T
  assert np.max(abs(H-H2))<1e-13
  assert err<1e-13
out={'seed':8274,'complex_random_channel_pairs':60,'worst_objective_error':worst,'status':'passed, numerical convention stress test only'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

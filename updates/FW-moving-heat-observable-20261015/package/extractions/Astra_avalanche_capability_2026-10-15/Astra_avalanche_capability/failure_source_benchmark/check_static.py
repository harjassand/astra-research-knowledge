import json
import numpy as np
from verify_avalanche_clock import clock
from pathlib import Path
rng=np.random.default_rng(676251)
worst=0.;cases=0
for n in [1,2,3,5,10,30,100]:
 for f in [0.,.125,.15,.175,.5,1.]:
  for T in [.05,.1,.15]:
   for rep in range(50):
    h=rng.uniform(size=n);E=rng.exponential(size=n)*np.exp(h/T);F=n*f
    C=[]
    for k in range(1,n+1):
     z=E[h>F/k]
     C.append(0. if len(z)<k else np.partition(z,len(z)-k)[len(z)-k])
    Ts=np.maximum.accumulate(C[::-1])[::-1]
    psi=np.r_[0.,np.exp(-F/(np.arange(1,n+1)*T))]
    static=np.diff(psi)@Ts
    timed,events=clock(h,f,T,E=E)
    err=abs(static-timed)/max(1,abs(timed));worst=max(worst,err);cases+=1
    assert err<1e-12,(n,f,T,static,timed)
    # Monotonicity and sup-norm Lipschitz test, diagnostics not proof.
    delta=rng.uniform(size=n);E2=E+delta
    t2,_=clock(h,f,T,E=E2)
    assert t2>=timed-1e-10
    assert t2-timed<=psi[-1]*max(delta)+64*np.finfo(float).eps*max(1,abs(timed)),(n,f,T,timed,t2-timed,psi[-1]*max(delta))
out={'cases':cases,'max_relative_error':worst,'status':'all static-vs-event identities, monotonicity and Lipschitz diagnostics passed'}
Path(__file__).with_name('static_results.json').write_text(json.dumps(out,indent=2));print(out)

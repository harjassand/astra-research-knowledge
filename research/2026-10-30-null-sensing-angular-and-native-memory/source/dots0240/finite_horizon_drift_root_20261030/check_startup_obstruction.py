"""Exact finite sums with quadrature; asymptotic proof is in the accompanying note."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
th=.3; a=.4; T=.5
rows=[]
for m in [16,64,256,1024,4096,16384]:
    ell=np.arange(1,m+1,dtype=float)
    # Normalize each initial term by exp(am); no overflow from exponential V.
    coef=(m-ell+1)*np.exp(a*(ell-m)); v0=coef.sum()
    def g(t): return th+(1-th)*np.exp(-t)*(1+t)
    def w_scaled(t): return np.sum(ell*coef*np.exp(ell*np.log(g(t))))/v0
    vt=np.sum(coef*np.exp(ell*np.log(g(T))))/v0
    integ=quad(w_scaled,0,T,epsabs=1e-8,epsrel=1e-9,limit=200)[0]
    loss=1-vt
    rows.append(dict(m=m,initial_W_over_V=float((ell*coef).sum()/v0),loss_over_V=float(loss),integrated_W_over_V=float(integ),integrated_W_over_sqrt_m_V=float(integ/np.sqrt(m)),service_ratio=float(loss/integ)))
assert all(rows[i+1]['service_ratio']<rows[i]['service_ratio'] for i in range(len(rows)-1))
report={'theta':th,'a':a,'T':T,'rows':rows,'scope':'Finite regression of exact independent two-stage model; not an FGL-code counterexample.'}
Path(__file__).with_name('startup_obstruction_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

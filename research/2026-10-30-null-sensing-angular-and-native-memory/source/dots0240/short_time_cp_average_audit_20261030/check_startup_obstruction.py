"""Independent normalized full-interval calculation, avoiding exp(a*m) overflow."""
import numpy as np,json
from scipy.integrate import quad
from scipy.special import logsumexp
a=.3;theta=.1;T=1.
rows=[]
for m in [16,64,256,1024,4096]:
 ell=np.arange(1,m+1,dtype=float)
 logweights=np.log(m-ell+1)+a*ell
 logV0=logsumexp(logweights)
 p=np.exp(logweights-logV0)
 def g(t):return theta+(1-theta)*np.exp(-t)*(1+t)
 def wratio(t):return float(np.sum(p*ell*np.exp(ell*np.log(g(t)))))
 VTratio=float(np.sum(p*np.exp(ell*np.log(g(T)))))
 integ=quad(wratio,0,T,epsabs=1e-9,epsrel=1e-10,limit=200)[0]
 rows.append({'m':m,'W0_over_V0':float(np.dot(p,ell)),
              'decrement_over_V0':1-VTratio,
              'integrated_W_over_V0':integ,
              'integrated_W_over_sqrt_m_V0':integ/np.sqrt(m),
              'largest_possible_alpha_without_linear_allowance':(1-VTratio)/integ})
print(json.dumps({'a':a,'theta':theta,'T':T,'rows':rows,
 'proof_status':'Regression only; the written proof gives divergence and handles b*m exactly.'},indent=2))
assert rows[-1]['integrated_W_over_V0']>rows[0]['integrated_W_over_V0']
assert rows[-1]['largest_possible_alpha_without_linear_allowance']<.02

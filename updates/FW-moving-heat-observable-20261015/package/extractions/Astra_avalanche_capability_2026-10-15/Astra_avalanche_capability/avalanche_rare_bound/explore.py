from pathlib import Path
import sys,json,numpy as np
from scipy.stats import poisson,binom
sys.path.insert(0,str(Path(__file__).resolve().parent.parent / 'avalanche_boundary_dp'))
from boundary_dp import pmf
out=[]
for n in [100,400]:
 s=np.sort(np.random.RandomState(0).uniform(size=n))[::-1];F=.175*n;T=.15
 js=np.array([sum(s>F/k) for k in range(1,n+1)]);feas=np.where(js>=np.arange(1,n+1))[0]+1
 kmin,n0=feas[0],feas[-1];r=int(max(js-np.arange(1,n+1)+1))
 rates=[np.exp(F/(k*T))*sum(np.exp(-s[js[k-1]-k:js[k-1]]/T)) for k in feas];R=max(rates)
 for t in [.001,.01,.03,.1,.3,1]:
  low=pmf(s,F,np.exp(-np.exp(-s/T)*t/np.exp(-F/(n0*T))))[0]
  hi=pmf(s,F,np.exp(-np.exp(-s/T)*t/np.exp(-F/(kmin*T))))[0]
  out.append(dict(n=n,kmin=int(kmin),n0=int(n0),r=r,R=R,t=t,lower=low,upper=hi,poisson=poisson.sf(r-1,R*t),binomial=binom.sf(r-1,n0,-np.expm1(-t))))
print(json.dumps(out,indent=2))
for n in [100,400]:
 s=np.sort(np.random.RandomState(0).uniform(size=n))[::-1];F=.175*n;T=.15
 for t in [.01,.1,.3,1]:
  vals=[sum(pmf(s,F,np.exp(-np.exp(-s/T)*t/np.exp(-F/(k*T))))[:k]) for k in range(1,n+1)]
  k=np.argmin(vals)+1
  print('optimized',n,t,k,vals[k-1])

from pathlib import Path
from certify import *
from scipy.linalg import expm

def trigger_rates(n,f0=Fraction(7,40),T=Fraction(3,20)):
 s,F,T,feas,r,R=setup(n,f0,T);n0=max(feas)
 js={k:sum(x*k>F for x in s) for k in feas}
 hazard={k:mp.iv.exp(I(F)/(k*I(T)))*sum((mp.iv.exp(-I(x)/I(T)) for x in s[js[k]-k:js[k]]),mp.iv.mpf(0)) for k in feas}
 rates=[];counts=[]
 for ell in range(r):
  klow=max(k for k in feas if js[k]-ell>=k)
  allowed=[k for k in feas if klow<=k<=n0-ell and js[k]-k<=ell]
  if ell==0:allowed=[n0]
  rates.append(mp.iv.mpf([max(hazard[k].a for k in allowed),max(hazard[k].b for k in allowed)]));counts.append(allowed)
 return rates,counts

def cdf_upper(rates,t):
 # Positive uniformization; finite series plus rigorously bounded Poisson tail.
 R=mp.iv.mpf(max(x.b for x in rates));x=R*I(t);r=len(rates)
 a=[z/R for z in rates];v=[mp.iv.mpf(0) for _ in range(r+1)];v[0]=mp.iv.mpf(1)
 w=mp.iv.exp(-x);total=mp.iv.mpf(0)
 for k in range(1,r+600):
  v=[v[0]*(1-a[0])]+[v[j]*(1-a[j])+v[j-1]*a[j-1] for j in range(1,r)]+[v[r]+v[r-1]*a[r-1]]
  w=w*x/k;total+=w*v[r]
 rho=x/(k+1);return total+w*rho/(1-rho)
if __name__=='__main__':
 out=[]
 for n in [100,400]:
  rates,counts=trigger_rates(n)
  for ts in ['.01','.1','.3','1']:
   start=time.perf_counter();p=cdf_upper(rates,Fraction(ts));elapsed=time.perf_counter()-start
   row=dict(n=n,t=ts,rates=[bounds(z) for z in rates],allowed_counts=counts,upper_interval=bounds(p),seconds=elapsed);out.append(row)
   print(n,ts,bounds(p),elapsed,flush=True)
 with open(str(Path(__file__).resolve().parent.parent / 'avalanche_rare_bound/trigger_results.json'),'w') as f:json.dump(out,f,indent=2)

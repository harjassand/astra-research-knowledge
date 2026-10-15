from pathlib import Path
from trigger_baseline import *
out=[]
for n,m in [(100,37),(400,142)]:
 s,F,T,feas,r,R=setup(n,Fraction(3,20),Fraction(1,10));rates,counts=trigger_rates(n,Fraction(3,20),Fraction(1,10))
 for ts in ['.01','.1','.3','1']:
  t=Fraction(ts);start=time.perf_counter();p=below(s,F,T,t,m);dt=time.perf_counter()-start
  start=time.perf_counter();b=cdf_upper(rates,t);bt=time.perf_counter()-start
  row=dict(n=n,m=m,f0='.15',T='.1',t=ts,r=r,kmin=min(feas),n0=max(feas),boundary_interval=bounds(p),birth_interval=bounds(b),dp_seconds=dt,birth_seconds=bt);out.append(row)
  print(n,ts,float(p.b),float(b.b),flush=True)
with open(str(Path(__file__).resolve().parent.parent / 'avalanche_rare_bound/midpoint_results.json'),'w') as f:json.dump(out,f,indent=2)

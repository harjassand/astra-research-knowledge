from pathlib import Path
"""Illustrative input uncertainty, not a measured confidence region."""
from certify import *
out=[]
for f0,T in [(Fraction(3,20),Fraction(1,10)),(Fraction(7,40),Fraction(3,20))]:
 s0,F,T,feas,r,R=setup(400,f0,T)
 for eta in [Fraction(0),Fraction(1,200),Fraction(1,100)]:
  s=[max(Fraction(0),x-eta) for x in s0]
  deficits=[sum(x*k>F for x in s)-k+1 for k in range(1,401)]
  m=int(np.argmax(deficits))+1;r=max(deficits)
  start=time.perf_counter();p=below(s,F,T,Fraction(1,10),m);elapsed=time.perf_counter()-start
  row=dict(n=400,f0=str(f0),T=str(T),eta=str(eta),deadline='1/10',m=m,min_thermal_triggers=r,worst_corner_bound_interval=bounds(p),seconds=elapsed);out.append(row)
  print(row,flush=True)
with open(str(Path(__file__).resolve().parent.parent / 'avalanche_rare_bound/strength_uncertainty_results.json'),'w') as f:json.dump(out,f,indent=2)

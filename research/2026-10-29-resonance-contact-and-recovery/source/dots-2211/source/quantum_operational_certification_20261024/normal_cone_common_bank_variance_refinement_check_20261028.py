import math,json,hashlib
from pathlib import Path
checks=0
for ell in range(1,9):
 assert sum(math.comb(ell,k)*3**k*3**(k+1) for k in range(1,ell+1))==3*(10**ell-1)
 assert sum(math.comb(ell,k)*3**k*(3**(k+1)+1)**2 for k in range(1,ell+1))==9*(28**ell-1)+6*(10**ell-1)+(4**ell-1)
 for N in [1,100,10000,10000000]:
  t=7.;etas=[math.sqrt(2*3**(k+1)*t/N)+2*(3**(k+1)+1)*t/(3*N) for k in range(1,ell+1)]
  h2=9/16*sum(math.comb(ell,k)*3**k*etas[k-1]**2 for k in range(1,ell+1))
  upper=27/4*(10**ell-1)*t/N+(9*(28**ell-1)+6*(10**ell-1)+(4**ell-1))*t*t/(2*N*N)
  assert h2<=upper*(1+1e-12);checks+=1
M=18;beta=.05;t=math.log(2*M/beta)
def h(N):return .75*math.sqrt(3)*(math.sqrt(18*t/N)+20*t/(3*N))
lo,hi=1,1000000
while lo<hi:
 mid=(lo+hi)//2
 if h(mid)<=.05:hi=mid
 else:lo=mid+1
assert lo==82202 and h(lo-1)>.05
out={'status':'PASS_EXACT_WEIGHT_SUMS_AND_FINITE_BOUND_CALCULATIONS','finite_bound_checks':checks,'variance_bound_source_calls':lo,'score_halfwidth':h(lo),'parent_Hoeffding_calls':959255,'budget_ratio':959255/lo,'scope':'No acquisition or physical advantage measured; exact integer identities and finite scalar budget calculation.'};p=Path(__file__);out['source_sha256']=hashlib.sha256(p.with_name('normal_cone_common_bank_variance_refinement_20261028.md').read_bytes()).hexdigest();p.with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

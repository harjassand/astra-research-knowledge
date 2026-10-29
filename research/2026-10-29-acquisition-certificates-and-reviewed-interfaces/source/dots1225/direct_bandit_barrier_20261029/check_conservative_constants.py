from fractions import Fraction as F
from pathlib import Path
import json
rows=[]
for T in [120,10**6,10**9,10**12,10**15,10**18]:
 ell=(T-1).bit_length() # >=ln(T), for T>1
 best=None
 for r in range(1,5001):
  M=(2*r+1)**3;per=F(216,r*r)+F(6+144*(M-1)*ell,T)
  if best is None or per<best[0]:best=(per,r,M)
 per,r,M=best;rows.append(dict(T=T,r=r,M=M,ceil_log2_T=ell,per_edge_average_bound=str(per),per_edge_average_bound_float=float(per),sum_three_bound=float(3*per),raw_service_bound_alpha8=float(24*per)))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(scope='Conservative exact arithmetic theorem bounds, not simulation or practical rate; m3,p_w1/3,rho1/9. Search r1..5000 is a chosen feasible bound, not proved global optimizer.',rows=rows),indent=2)+'\n')
for row in rows:print(row['T'],row['r'],row['per_edge_average_bound_float'],row['raw_service_bound_alpha8'])

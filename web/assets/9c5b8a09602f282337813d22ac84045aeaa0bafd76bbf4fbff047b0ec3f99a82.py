from fractions import Fraction as Q
from itertools import combinations, permutations
from math import prod
import json
from pathlib import Path

u=Q(1,4096)
eps=Q(1,64)
den=1+u*u
common_den=2**24+1
c=(1-u*u)/den
s=2*u/den
P=[[int(j==(i+1)%3) for j in range(3)] for i in range(3)]
F=[[Q(0) for _ in range(6)] for _ in range(6)]
for i in range(3):
 for j in range(3):
  F[i][j]=c*P[i][j]; F[i][j+3]=-s*P[i][j]
  F[i+3][j]=s*P[i][j]; F[i+3][j+3]=c*P[i][j]
assert all(sum(F[k][i]*F[k][j] for k in range(6))==int(i==j) for i in range(6) for j in range(6))
# A common denominator on all 12 columns multiplies every size-six determinant equally.
V=[]
for i in range(6): V.append([int(i==j)*common_den for j in range(6)]+[int(F[j][i]*common_den) for j in range(6)])
perms=list(permutations(range(6)))
def det_cols(sel):
 total=0
 for p in perms:
  inv=sum(p[i]>p[j] for i in range(6) for j in range(i+1,6))
  val=(-1 if inv&1 else 1)
  for i,j in enumerate(p): val*=V[i][sel[j]]
  total+=val
 return total
Z=Q(0); H=Q(0); col=[Q(0) for _ in range(12)]; bysplit={}
for S in combinations(range(12),6):
 det=det_cols(S); ifzero=(det==0)
 occ=[sum(int(j==i or j==i+6) for j in S) for i in range(6)]
 split=sum(x==1 for x in occ)
 wt=Q(det*det,1)*eps**split
 Z+=wt; bysplit[split]=bysplit.get(split,Q(0))+wt
 if split==0: H+=wt
 for j in S: col[j]+=wt
# Remove common denominator scaling of each selected column (d^6 in determinant).
scale=common_den**12
Z0=Z/scale; H0=H/scale; cols=[x/scale for x in col]
a=c**6+3*c**2*s**4
b=3*c**4*s**2+s**6
formula= a*(6*eps+2*eps**3)**2 + b*((1+eps)**6+(eps-1)**6)
prob=H/Z
out={"result":"PASS" if Z0==formula and all(x==Z0/2 for x in cols) else "FAIL",
     "parameters":{"u":str(u),"epsilon":str(eps),"c":str(c),"s":str(s)},
     "enumerated_selections":924,"hard_probability_exact":str(prob),
     "hard_probability_float":float(prob),"formula_hard_probability_asymptotic_scale":float(s*s/(6*eps*eps)),
     "soft_partition_formula_matches_exact":Z0==formula,
     "all_12_column_marginals_one_half":all(x==Z/2 for x in col),
     "split_weight_by_count":{str(k):str(v/scale) for k,v in sorted(bysplit.items())},
     "claim_limit":"one exact finite instance of the soft-overlap obstruction; asymptotic hardness is the algebraic u->0 expansion, not inferred from this check"}
Path('work/cycle6/c01_l09/revisions/soft_overlap_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

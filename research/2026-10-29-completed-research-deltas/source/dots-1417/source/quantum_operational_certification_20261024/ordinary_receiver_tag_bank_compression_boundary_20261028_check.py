from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
Z=[(tuple(F(int(i==j)) for i in range(4)),F(1,12)) for j in range(4)]
Z += [(tuple(F(s,2) for s in ss),F(1,24)) for ss in product([-1,1],repeat=4)]
assert sum(w for z,w in Z)==1
moments=0
for i,j,k,l in product(range(4),repeat=4):
 v=sum(w*z[i]*z[j]*z[k]*z[l] for z,w in Z)
 e=F(int(i==j and k==l)+int(i==k and j==l)+int(i==l and j==k),24)
 assert v==e; moments+=1
cases=0
for den in range(2,42):
 delta=F(1,den)
 B=[(2+3*delta)/24,(2+delta)/24,(4+delta)/24,(4+delta)/24]
 C=[(4-3*delta)/24,(4-delta)/24,(2-delta)/24,(2-delta)/24]
 q0=B+C;q1=[B[1],B[0],B[2],B[3],C[1],C[0],C[2],C[3]]
 assert sum(q0)==sum(q1)==1 and min(q0)>0
 chi=sum((p-q)**2/q for p,q in zip(q0,q1))
 formula=delta**2/F(6)*(1/(2+delta)+1/(2+3*delta)+1/(4-delta)+1/(4-3*delta))
 assert chi==formula and chi<=delta**2/3
 assert 4*sum(B)+96*B[1]==10+5*delta
 for i in range(4):
  a=[delta,0,1,1]
  direct=sum(w*sum(a[j]*z[j]**2 for j in range(4))*z[i]**2 for z,w in Z)
  assert direct==B[i]
 cases+=1
p=Path(str(Path(__file__)).replace('_check.py','.md'))
out={'status':'PASS_EXACT_FINITE_TAG_MOMENTS_AND_BOUNDARY_CONSTANTS','fourth_moments':moments,'rational_parameter_cases':cases,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'Exact rational moments, diagonal compressed states, chi-squared formula and zero-risk second moment. General CPTP/Le Cam proof is in manuscript; no physical query, SDP or circuit execution.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

import sympy as S
from itertools import permutations,product
from pathlib import Path
import json
rot=[]
for p in permutations(range(3)):
 for signs in product((-1,1),repeat=3):
  r=S.zeros(3)
  for i in range(3):r[i,p[i]]=signs[i]
  if r.det()==1:rot.append(r)
assert len(rot)==24
T=sum((S.kronecker_product(r,r) for r in rot),S.zeros(9))/24
v=S.Matrix([1,0,0,0,1,0,0,0,1]);Pi=v*v.T/3
assert T==Pi and T*T==T and T.rank()==1
D=T-S.eye(9)
assert D*D==-D and D.rank()==8 and D*v==S.zeros(9,1)
out={'exact':True,'proper_rotations':24,'twirl_rank':1,'defect_rank':8,'nonzero_singular_values':[1]*8,'gap':1,'scope':'Fresh uniform source octahedral second moment, in fixed unknown frames; arbitrary preceding full-joint collective-algebra operation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

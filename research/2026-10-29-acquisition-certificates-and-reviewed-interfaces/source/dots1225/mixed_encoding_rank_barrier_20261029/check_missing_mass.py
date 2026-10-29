from fractions import Fraction as F
import itertools,json,numpy as np
from pathlib import Path
rows=[]
for p in [[F(1,2)]*2,[F(1,3)]*3,[F(1,2),F(1,3),F(1,6)]]:
 r=len(p)
 for n in range(6):
  unseen=F(0)
  for flags in itertools.product(range(r),repeat=n):
   prob=F(1)
   for i in flags:prob*=p[i]
   unseen+=prob*sum(p[j] for j in range(r) if j not in flags)
  formula=sum(pj*(1-pj)**n for pj in p);assert unseen==formula
  rows.append(dict(p=[str(x) for x in p],n=n,missing_mass=str(formula),qubit_Fe=str(1-F(3,4)*formula),qubit_halfdiamond=str(F(3,4)*formula)))
errs=[]
for k in [2,3,4]:
 omega=np.exp(2j*np.pi/k);W=[]
 for a in range(k):
  for b in range(k):
   U=np.zeros((k,k),complex)
   for j in range(k):U[(j+a)%k,j]=omega**(b*j)
   W.append(U)
 C=np.column_stack([U.reshape(-1)/np.sqrt(k) for U in W]);orth=np.linalg.norm(C.conj().T@C-np.eye(k*k))
 E=np.zeros((k,k),complex);E[0,1]=1;out=sum(U@E@U.conj().T for U in W)/(k*k)
 err=np.linalg.norm(out);assert orth<1e-12 and err<1e-12
 errs.append(dict(k=k,Bell_orthogonality_residual=float(orth),offdiagonal_Weyl_twirl_residual=float(err)))
res=dict(exact_coupon_cases=rows,physical_Weyl_checks=errs,scope='Exact finite flag enumeration plus dense known Bell/Weyl diagnostics; universal lower bound governed by decoupling proof')
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print('passed',len(rows),'exact coupon cases and',len(errs),'Weyl checks')

"""Build physical six-dimensional Schur polynomials from the exact lift."""
from pathlib import Path
from fractions import Fraction as R
from decimal import Decimal,getcontext
import pickle,json,sys
import numpy as np
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/hopf_structure'));import receive as b
data=pickle.load((root/'work/heat_exact_schur.pkl').open('rb'));src=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());e0,f0=map(R,src['ray']['canonical_zero']);w=b.add(b.var(3,0),{(0,0,0):-e0});g=b.add(b.var(3,1),{(0,0,0):-f0});one={(0,0,0):R(1)};D=[[{} for _ in range(6)] for _ in range(7)];D[0][0]=w;D[1][0]=g
for j in range(1,6):D[j+1][j]=one
def mm(A,B):return [[b.add(*(b.mul(a,c) for a,c in zip(row,col))) for col in zip(*B)] for row in A]
Q=[mm(list(map(list,zip(*D))),mm(G,D)) for G in data['charts']];data['physical_charts']=Q
with (root/'work/heat_exact_schur.pkl').open('wb') as fp:pickle.dump(data,fp)
getcontext().prec=40;arr=np.zeros((4,6,6,9,9,5),dtype=np.longdouble)
for ch,M in enumerate(Q):
 for i in range(6):
  for j in range(6):
   for e,co in M[i][j].items():arr[(ch,i,j)+e]=np.longdouble(str(Decimal(co.numerator)/Decimal(co.denominator)))
np.savez(root/'work/heat_physical_float.npz',charts=arr)
print('four exact physical Schur polynomials built',flush=True)

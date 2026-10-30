"""Exact algebra for QC stabilization by Q0=b^2+c^2 (rank two).

Tests all acoustic-row annihilation identities and the two bottom
kernel columns. Existence of this linear lift is separate from the
global heat bound; no solver status is used as a QC claim.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations
import json,sys,time
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import heat_model as h
b,r,ca=h.b,h.r,h.ca;start=time.perf_counter();ss=(root/'work/graded_heat_lift.py').read_text();ns={'__file__':str(root/'work/graded_heat_lift.py'),'__name__':'root_rows'};exec(ss[:ss.index('c0=[R(q)')],ns);E,RHS=ns['E'],ns['RHS'];powers=ns['powers'];CB=ns['CB'];rank0=ns['rankE'];targetpolys=[{tuple(pw):R(1)} for pw in powers]
for a in range(4):
 A=[R(int(i==a)) for i in range(4)]
 for col in (0,5):
  for i in range(6):
   E.append([R(float(h.XB[a,i,col,l])) for l in range(80)]);rr=[]
   for P in targetpolys:
    HC=[[b.evaluate(b.diff(b.diff(P,j),k),A) for k in range(4)] for j in range(4)];V=[[R(0)]*6 for _ in range(6)]
    for ids in ((0,1,3,4),(1,2,4,5)):
     for j in range(4):
      for k in range(4):V[ids[j]][ids[k]]+=HC[j][k]/2
    rr.append(-V[i][col])
   RHS.append(rr)
rk=b.rank(E);ra=b.rank([row+rr for row,rr in zip(E,RHS)]);dim=20-(ra-rk)
print('rank-two quadratic heat lift: variable rank',rk,'augmentation',ra,'cubic dimension',dim,flush=True)
# The natural candidate is exactly the completed capacity kernel of E11,E22.
sys.path.insert(0,str(root/'outputs/acoustic_capacity'));ks=__import__('kernel');factors=[ks.feature_factor(R0,'closed')[1] for R0 in ([1,0,0,0],[0,0,0,1])];J=factors[0]+factors[1];rankJ=b.rank(J)
def nullbasis(A):
 A=[list(row) for row in A];p=0;piv=[]
 for j in range(len(A[0])):
  k=next((i for i in range(p,len(A)) if A[i][j]),None)
  if k is None:continue
  A[p],A[k]=A[k],A[p];v=A[p][j];A[p]=[x/v for x in A[p]]
  for i in range(len(A)):
   if i!=p:v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[p])]
  piv.append(j);p+=1
  if p==len(A):break
 out=[]
 for free in range(len(A[0])):
  if free in piv:continue
  v=[R(0)]*len(A[0]);v[free]=1
  for i,j in enumerate(piv):v[j]=-A[i][free]
  out.append(v)
 return out
zz=nullbasis(J);CC=[[sum(v*row[j] for v,row in zip(z,CB)) for j in range(20)] for z in zz];assert len(CC)==12-rankJ
admitted=False;solution=None
try:
 sol,rrank=ca.solve_range(E,[[sum(a*c for a,c in zip(row,cv)) for cv in CC] for row in RHS]);admitted=True;solution=sol
except Exception as err:print('candidate lift range obstruction',type(err).__name__,str(err)[:150],flush=True)
out={'linear_variable_rank':rk,'augmented_rank':ra,'admitted_cubic_dimension':dim,'completed_two_root_kernel_dimension':len(CC),'completed_two_root_kernel_cubics':[[str(v) for v in row] for row in CC],'all_completed_kernel_cubics_have_degenerate_heat_lift':admitted,'linear_heat_lift_coefficients':None if solution is None else [[str(v) for v in row] for row in solution],'scope':'Exact algebra only. A QC claim additionally requires a global bounded heat-Schur cost relative to the fixed positive leading certificate.','seconds':time.perf_counter()-start};(root/'work/degenerate_quadratic_lift.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if not isinstance(v,list)},indent=2),flush=True)

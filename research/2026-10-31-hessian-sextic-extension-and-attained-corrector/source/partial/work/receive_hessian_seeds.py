"""Acquire exact strict conic-ROC quartics from the broader cone search.

Only the reconstructed rational 9x9 PSD Gram is used for admission.
Heat/SOS failure remains a numerical diagnostic, not a QC obstruction.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations_with_replacement
import sys,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import hessian_quartic_cone as m
sys.path.insert(0,str(root/'outputs/shared_mode_gluing'));import capacity as ca
start=time.perf_counter();b=m.b;raw=json.loads((root/'work/hessian_heat_sos.json').read_text());qq=[b.var(3,i) for i in range(3)];norm=b.add(b.mul(qq[0],qq[0]),b.scale(b.mul(qq[1],qq[1]),2),b.mul(qq[2],qq[2]));norm4=b.mul(norm,norm);nc=np.array([float(norm4.get(pw,0)) for pw in m.powers]);pairs=list(combinations_with_replacement(range(9),2));E=[]
for k in range(5):
 for i,j in combinations_with_replacement(range(3),2):
  row=[]
  for a,c in pairs:
   value=0
   for u in range(3):
    for v in range(3):
     if u+v==k:
      ai,cj=3*u+i,3*v+j
      if (min(ai,cj),max(ai,cj))==(a,c):value+=1
   row.append(R(value))
  E.append(row)
records=[]
for idx in (4,7,15):
 rec=next(row for row in raw['records'] if row['name']==f'ROC_sample_{idx}');h0=np.array(rec['quartic_coefficients'])+1e-4*nc;coef=[R(round(float(v)*2**36),2**36) for v in h0];target=[]
 for k in range(5):
  for i,j in combinations_with_replacement(range(3),2):target.append(sum(R(int(round(m.Hcoef[k,l,i,j])))*coef[l] for l in range(15)))
 G=cp.Variable((9,9),symmetric=True);margin=cp.Variable();constraints=[G-margin*np.eye(9)>>0]
 for k in range(5):constraints.append(sum(G[3*i:3*i+3,3*j:3*j+3] for i in range(3) for j in range(3) if i+j==k)==np.einsum('lij,l->ij',m.Hcoef[k],np.array(coef,float)))
 prob=cp.Problem(cp.Maximize(margin),constraints);prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-11,max_iter=400);assert G.value is not None and margin.value>1e-7
 vv=[R(round(float(G.value[i,j])*2**44),2**44) for i,j in pairs];delta,_=ca.solve_range(E,[[t-sum(a*c for a,c in zip(row,vv))] for row,t in zip(E,target)]);vv=[a+q[0] for a,q in zip(vv,delta)];GM=[[R(0)]*9 for _ in range(9)]
 for (i,j),v in zip(pairs,vv):GM[i][j]=GM[j][i]=v
 assert all(sum(a*c for a,c in zip(row,vv))==t for row,t in zip(E,target));eta=R(1,2**24);b.pd([[v-(eta if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(GM)])
 record={'name':f'H{idx}','quartic_coefficients':list(map(str,coef)),'Gram':[[str(v) for v in row] for row in GM],'strict_Gram_margin':str(eta),'strict_conic_ROC_modulus_Frobenius':str(eta/4),'QC_status':'UNKNOWN','source_numerical_polynomial_heat_margin':rec['maximum_Gram_margin']};records.append(record);print('received exact strict conic ROC seed',record['name'],flush=True)
out={'powers':m.powers,'records':records,'seconds':time.perf_counter()-start,'scope':'Exact globally conic rank-one-convex quartic polynomials on Sym(2), not globally ROC polynomials on all nonsymmetric 2x2 matrices. QC is unresolved until an actual-field or variational proof is received.'};(root/'outputs/hessian_frontier/seeds.json').write_text(json.dumps(out,indent=2)+'\n')

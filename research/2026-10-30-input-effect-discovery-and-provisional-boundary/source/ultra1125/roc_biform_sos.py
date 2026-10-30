"""Exact global ROC admission for a proposed quadratic, no QC inference."""
from pathlib import Path
from fractions import Fraction as R
import importlib.util,json,time,sys
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];start=time.perf_counter()
spec=importlib.util.spec_from_file_location('core',root/'outputs/hopf_structure/receive.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
raw=json.loads((root/'work/actual_boundary.json').read_text());nu=R(sys.argv[1]) if len(sys.argv)>1 else R(2000)
delta={tuple(row[:1]):R(row[1],row[2]) for row in raw['delta']};numerator={tuple(row[:3]):R(row[3],row[4]) for row in raw['regularized_numerator']}
poly={}
def put(e,c):poly[e]=poly.get(e,R(0))+c
for (ti,),co in delta.items():
    for tpower in (ti,ti+2):
        for ypower,bc in ((0,1),(2,3),(4,3),(6,1)):put((tpower,6-ypower,ypower),2*nu*co*bc)
for e,co in numerator.items():put(e,-co)
poly={e:c for e,c in poly.items() if c};scale=max(map(abs,poly.values()));target={e:c/scale for e,c in poly.items()}
mons=[(i,j,3-j) for i in range(4) for j in range(4)];groups={}
for i in range(16):
    for j in range(i,16):
        ex=tuple(a+c for a,c in zip(mons[i],mons[j]));groups.setdefault(ex,[]).append((i,j,1 if i==j else 2))
assert set(poly).issubset(groups)
G=cp.Variable((16,16),symmetric=True);margin=cp.Variable();cons=[G-margin*np.eye(16)>>0]
for e,entries in groups.items():cons.append(sum(w*G[i,j] for i,j,w in entries)==float(target.get(e,0)))
prob=cp.Problem(cp.Maximize(margin),cons)
prob.solve(solver='CLARABEL',tol_feas=1e-10,tol_gap_abs=1e-10,tol_gap_rel=1e-10,max_iter=250)
print('proposal',prob.status,'margin',margin.value,flush=True)
if G.value is None or margin.value<=0:raise ValueError('No positive Gram acquired; no non-ROC or QC conclusion follows')
GG=[[R(round(float(G.value[i,j])*10**12),10**12) for j in range(16)] for i in range(16)]
for e,entries in groups.items():
    i,j,w=entries[0];value=target.get(e,R(0))-sum(ww*GG[ii][jj] for ii,jj,ww in entries[1:]);GG[i][j]=GG[j][i]=value/w
b.pd(GG)
for e,entries in groups.items():assert sum(w*GG[i][j] for i,j,w in entries)==target.get(e,R(0))
out={'nu':str(nu),'Gram_monomials':mons,'Gram':[[str(v) for v in row] for row in GG],
     'scale':str(scale),'polynomial':[[*e,c.numerator,c.denominator] for e,c in poly.items()],
     'seconds':time.perf_counter()-start,'scope':'Exact positive Gram for the regularized biform, hence global ROC. Quasiconvexity is not inferred.'}
(root/f'work/roc_biform_{nu.numerator}_{nu.denominator}.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('Gram','polynomial','Gram_monomials')},indent=2))

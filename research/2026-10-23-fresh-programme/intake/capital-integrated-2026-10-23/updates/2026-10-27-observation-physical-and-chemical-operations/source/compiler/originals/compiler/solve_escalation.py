import sys,json,time
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'continuation_magic_decomposition'/'deps'))
import numpy as np
import sympy as sp
from scipy.optimize import linprog
root=Path(__file__).resolve().parent
src=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-redesign-20261026/experiments/channel_case/teams/T31/stage2/worker1/H03_INPUT.json')
data=json.loads(src.read_text()); (root/'sources'/f'{data["id"]}_INPUT.json').write_text(json.dumps(data,indent=2)+'\n')
K=sp.Matrix(data['K']); L=sp.Matrix(data['L']); ny,nx=K.shape; nz=L.rows
A=[];b=[];names=[]
def add(row,rhs,name): A.append(row);b.append(sp.Rational(rhs));names.append(name)
for z in range(nz):
 row=[sp.S.Zero]*(ny*nz+1)
 for y in range(ny):row[y*nz+z]=sp.S.One
 add(row,1,f'column_{z}')
for y in range(ny):
 for x in range(nx):
  row=[sp.S.Zero]*(ny*nz+1)
  for z in range(nz):row[y*nz+z]=L[z,x]
  add(row,K[y,x],f'output_{y}_{x}')
for x in range(nx):
 row=[-L[z,x] for y in range(ny) for z in range(nz)]+[-sp.S.One]
 add(row,-1,f'query_{x}')
Am=sp.Matrix(A);bm=sp.Matrix(b);cost=sp.Matrix([0]*(ny*nz)+[1]); start=time.perf_counter();cpu=time.process_time()
res=linprog(np.array(cost,dtype=float).ravel(),A_ub=np.array(Am,dtype=float),b_ub=np.array(bm,dtype=float).ravel(),bounds=(0,None),method='highs')
assert res.success,res.message
active=[i for i,s in enumerate(res.ineqlin.residual) if abs(s)<1e-8]
zeros=[i for i,v in enumerate(res.x) if abs(v)<1e-8]
E=sp.Matrix([A[i] for i in active]+[[int(j==i) for j in range(ny*nz+1)] for i in zeros]);f=sp.Matrix([b[i] for i in active]+[0]*len(zeros))
v=next(iter(sp.linsolve((E,f))))
assert not set().union(*(x.free_symbols for x in v))
v=sp.Matrix(v); assert all(x>=0 for x in v) and all(x>=0 for x in bm-Am*v)
# Reconstruct dual by fixing its numerical zero coordinates and equality on positive primal coordinates.
dual_support=[i for i,x in enumerate(-res.ineqlin.marginals) if x>1e-8]
F=Am[dual_support,:].T; eqrows=[i for i,x in enumerate(v) if x>0]
Fpos=F[eqrows,:];g=-cost[eqrows,:]
lam_support=next(iter(sp.linsolve((Fpos,g))));assert not set().union(*(x.free_symbols for x in lam_support))
lam=sp.zeros(len(b),1)
for i,x in zip(dual_support,lam_support):lam[i]=x
assert all(x>=0 for x in lam) and all(x>=0 for x in cost+Am.T*lam)
assert (cost.T*v)[0]==(-bm.T*lam)[0]
U=sp.Matrix(ny,nz,list(v)[:-1]);q=v[-1];s=sp.ones(1,ny)*U;qx=sp.ones(1,nx)-s*L;D=K-U*L
R=K*L.inv()
report={
 'input_id':data['id'],'input_source':str(src), 'column_stochastic':True,
 'q':str(q),'q_decimal':float(q),'U':[[str(U[y,z]) for z in range(nz)] for y in range(ny)],
 'query_by_z':[str(1-s[z]) for z in range(nz)],'query_by_x':[str(x) for x in qx],
 'residual':[[str(D[y,x]) for x in range(nx)] for y in range(ny)],
 'dual':[{ 'constraint':n,'weight':str(w)} for n,w in zip(names,lam) if w],
 'least_favorable_input':[str(x) for x in lam[-nx:]],
 'direct_garbling':[[str(R[y,z]) for z in range(nz)] for y in range(ny)],
 'active_constraints':[names[i] for i in active], 'lp_iterations':int(res.nit),
 'solve_and_reconstruct_wall_s':time.perf_counter()-start,'solve_and_reconstruct_cpu_s':time.process_time()-cpu,
 'exact_checks':['primal_nonnegative','primal_feasible','dual_nonnegative','dual_feasible','strong_duality'],
 'scope':'One-step minimax charged raw-read probability; exact rational certificate, not historical novelty or global simulation advantage.'}
(root/f'{data["id"]}_CERTIFICATE.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json
from scipy.optimize import minimize
from pathlib import Path
p=Path(__file__).parent
# Load only definitions; do not execute a new source trajectory.
s=(p/'quantum_memory_fixture_v1.py').read_text().split('max_grad=0;')[0]
exec(s,globals())
records=np.load(Path(__file__).parent/'quantum_memory_records_v1.npy');out=[]
for seed in [7301,7302,7303]:
 mem=np.array([[.5,.5],[.5,.5]],complex);S=np.zeros((16,2,2),complex);mins=[]
 for row in records[records[:,0]==seed]:
  _,t,x,wi,b=row;rho,rdg,blocks,sig=emit(mem);S+=sig/64
  mins.append(min(float(np.min(np.linalg.eigvalsh(sig[0]-q))) for q in sig))
  new=memory_after(blocks[x],pa[wi],b);mem=new/np.trace(new)
 def Y(y):return sum(a*b for a,b in zip(y,pa))
 def con(y):return np.linalg.eigvalsh(Y(y)[None,:,:]-S).reshape(-1)
 z=minimize(lambda y:2*y[0],np.array([1.,0,0,0]),constraints=[{'type':'ineq','fun':con}],method='SLSQP',options={'ftol':1e-13,'maxiter':1000})
 dual=Y(z.x);shift=max(0.,-min(con(z.x)))+1e-12;dual+=shift*I
 M=np.repeat((I/16)[None,:,:],16,axis=0)
 for k in range(3000):
  nxt,it=project(M+2*S,np.ones(16))
  if np.max(abs(nxt-M))<1e-12:M=nxt;break
  M=nxt
 primal=float(np.einsum('xij,xji->',M,S).real);upper=float(np.trace(dual).real)
 out.append({'seed':seed,'identity_score':float(np.trace(S[0]).real),'per_history_min_identity_dominance_eigenvalue':min(mins),'path_average_identity_dominance_min_eigenvalue':min(float(np.min(np.linalg.eigvalsh(S[0]-q))) for q in S),'numerical_fixed_path_occupation_primal':primal,'numerical_dual_upper':upper,'numerical_gap':upper-primal,'solver_success':bool(z.success),'nonzero_primal_effects_over_1e_minus7':int(sum(np.trace(q).real>1e-7 for q in M)),'scope':'oracle for realized-path average conditional coefficients, NOT best fixed expected-occupation oracle; numerical not rigorous certificate'})
result={'records_replayed':192,'new_distinct_records':0,'runs':out,'scope':'source-informed offline diagnostic; coefficients not available to learner; no independent source experiment or confidence claim'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

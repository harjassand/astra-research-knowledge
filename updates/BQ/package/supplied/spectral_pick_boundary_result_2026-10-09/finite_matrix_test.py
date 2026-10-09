"""Finite-N GOE smoke tests; not yet a comparative benchmark."""
import numpy as np,json,time
from pick_inverse import inverse,free_stieltjes
rng=np.random.default_rng(9102601)
rows=[]; raw={}
for N in [256,1024]:
 for k in [3,5]:
  atoms=np.array([-1.,.2,1.]) if k==3 else np.linspace(-1,1,5)
  weights=np.array([.25,.5,.25]) if k==3 else np.ones(k)/k
  n=np.floor(weights*N).astype(int);n[-1]+=N-n.sum()
  actual_weights=n/N
  a=np.repeat(atoms,n)
  z=np.linspace(-1.4,1.4,k)+.6j
  for variance in [.0625,.5625]:
   for rep in range(4):
    start=time.perf_counter();Z=rng.normal(size=(N,N));W=(Z+Z.T)/np.sqrt(2*N)
    c=np.linalg.eigvalsh(np.diag(a)+np.sqrt(variance)*W)
    matrix_seconds=time.perf_counter()-start
    start=time.perf_counter();g=np.mean(1/(z[:,None]-c),axis=1);transform_seconds=time.perf_counter()-start
    start=time.perf_counter();r=inverse(z,g);inverse_seconds=time.perf_counter()-start
    glimit=free_stieltjes(z,atoms,actual_weights,variance)
    err={'variance':abs(r['variance']-variance),'atoms_max':float(np.max(abs(r['atoms']-atoms))),'weights_max':float(np.max(abs(r['weights']-actual_weights)))}
    key=f'N{N}_k{k}_v{variance}_r{rep}'
    raw[key+'_eigenvalues']=c;raw[key+'_z']=z;raw[key+'_g']=g
    rows.append({'key':key,'N':N,'k':k,'true_variance':variance,'true_atoms':atoms.tolist(),'true_weights':actual_weights.tolist(),'inferred_variance':r['variance'],'inferred_atoms':r['atoms'].tolist(),'inferred_weights':r['weights'].tolist(),'errors':err,'g_limit_max_error':float(max(abs(g-glimit))),'K_condition':float(r['K_eigenvalues'][-1]/r['K_eigenvalues'][0]),'mass':r['mass'],'interpolation_residual':r['interpolation_residual'],'matrix_seconds':matrix_seconds,'transform_seconds':transform_seconds,'inverse_seconds':inverse_seconds})
np.savez_compressed('finite_matrix_raw.npz',**raw)
with open('finite_matrix_results.json','w') as f:json.dump(rows,f,indent=2)
for N in [256,1024]:
 for k in [3,5]:
  for v in [.0625,.5625]:
   rr=[r for r in rows if r['N']==N and r['k']==k and r['true_variance']==v]
   print(N,k,v,'mean errors',[np.mean([r['errors'][key] for r in rr]) for key in ['variance','atoms_max','weights_max']],'median inverse sec',np.median([r['inverse_seconds'] for r in rr]))

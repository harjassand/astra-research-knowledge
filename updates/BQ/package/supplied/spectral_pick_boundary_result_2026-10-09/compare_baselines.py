import numpy as np,json,time
from eigenmatrix_baseline import inverse as eigen_inverse
from pick_inverse import inverse as pick_inverse
rows=json.load(open('finite_matrix_results.json'));raw=np.load('finite_matrix_raw.npz');out=[]
for row in rows:
 if row['N']!=1024:continue
 key=row['key'];c=raw[key+'_eigenvalues'];k=row['k']
 support=(float(min(c)),float(max(c)));mid=sum(support)/2;half=(support[1]-support[0])/2
 theta=np.pi*(np.arange(32)+.5)/32
 z=mid+1.15*half*np.cos(theta)+.6j*half*np.sin(theta);z=np.r_[z,z.conj()]
 start=time.perf_counter();g=np.mean(1/(z[:,None]-c),axis=1);transform_seconds=time.perf_counter()-start
 start=time.perf_counter()
 try:
  r=eigen_inverse(z,g,k,support,float(np.var(c)))
  seconds=time.perf_counter()-start
  a=np.asarray(row['true_atoms']);p=np.asarray(row['true_weights'])
  r.update(errors={'variance':abs(r['variance']-row['true_variance']),'atoms_max':float(max(abs(r['atoms']-a))),'weights_max':float(max(abs(r['weights']-p)))},seconds=seconds,transform_seconds=transform_seconds)
  rr={key:value.tolist() if isinstance(value,np.ndarray) else (bool(value) if isinstance(value,np.bool_) else value) for key,value in r.items()}
 except Exception as exc:rr={'error':str(exc),'seconds':time.perf_counter()-start}
 out.append({'key':key,'pick':row,'eigenmatrix':rr})
with open('baseline_comparison.json','w') as f:json.dump(out,f,indent=2)
for k in [3,5]:
 for v in [.0625,.5625]:
  rr=[r for r in out if r['pick']['k']==k and r['pick']['true_variance']==v]
  for method in ['pick','eigenmatrix']:
   valid=[r[method] for r in rr if 'errors' in r[method]]
   print(k,v,method,len(valid),'mean errs',[float(np.mean([r['errors'][key] for r in valid])) for key in ['variance','atoms_max','weights_max']],'median sec',float(np.median([r.get('seconds',r.get('inverse_seconds')) for r in valid])))

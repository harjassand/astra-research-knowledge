import numpy as np,json,time
from scipy.stats import wasserstein_distance
from eigenmatrix_baseline import inverse as eigen_inverse
from pick_inverse import inverse as pick_inverse
from direct_fit_baseline import fit
rows=json.load(open('finite_matrix_results.json'));raw=np.load('finite_matrix_raw.npz');out=[];arrays={}
def serial(r):
 return {k:v.tolist() if isinstance(v,np.ndarray) else bool(v) if isinstance(v,np.bool_) else v for k,v in r.items()}
def errors(r,row):
 a=np.asarray(row['true_atoms']);p=np.asarray(row['true_weights'])
 pp=np.maximum(r['weights'],0);pp=pp/pp.sum()
 return {'variance':abs(r['variance']-row['true_variance']),'atoms_max':float(max(abs(r['atoms']-a))),'weights_max':float(max(abs(r['weights']-p))),'wasserstein1':float(wasserstein_distance(a,r['atoms'],p,pp))}
for row in rows:
 if row['N']!=1024:continue
 key=row['key'];c=raw[key+'_eigenvalues'];k=row['k'];support=(float(min(c)),float(max(c)));mid=sum(support)/2;half=(support[1]-support[0])/2;upper=float(np.var(c))
 z=mid+.8*half*np.linspace(-1,1,k)+.3j*half
 tic=time.perf_counter();g=np.mean(1/(z[:,None]-c),axis=1);r=pick_inverse(z,g);r['total_seconds']=time.perf_counter()-tic;r['errors']=errors(r,row)
 theta=np.pi*(np.arange(32)+.5)/32
 ze=mid+1.15*half*np.cos(theta)+.6j*half*np.sin(theta);ze=np.r_[ze,ze.conj()]
 tic=time.perf_counter();ge=np.mean(1/(ze[:,None]-c),axis=1);e=eigen_inverse(ze,ge,k,support,upper);e['total_seconds']=time.perf_counter()-tic;e['errors']=errors(e,row)
 zf=mid+.8*half*np.linspace(-1,1,32)+.3j*half
 tic=time.perf_counter();gf=np.mean(1/(zf[:,None]-c),axis=1);prep=time.perf_counter()-tic
 candidates=[];total_fit=prep
 cheap_atoms=np.quantile(c,(np.arange(k)+.5)/k)
 for frac in [.1,.35,.65,.9]:
  ai=np.mean(c)+np.sqrt(1-frac)*(cheap_atoms-np.mean(c))
  tic=time.perf_counter();ff=fit(zf,gf,k,ai,np.ones(k)/k,frac*upper,support,upper);ff['seconds']=time.perf_counter()-tic;ff['init']=str(frac);ff['errors']=errors(ff,row);total_fit+=ff['seconds'];candidates.append(ff)
 tic=time.perf_counter();ff=fit(zf,gf,k,r['atoms'],r['weights'],r['variance'],support,upper);ff['seconds']=time.perf_counter()-tic;ff['init']='pick';ff['errors']=errors(ff,row);candidates.append(ff)
 best=min(candidates,key=lambda d:d['cost']).copy();best['total_multistart_seconds']=total_fit+candidates[-1]['seconds']+r['total_seconds'];best['best_independent_cost']=min(d['cost'] for d in candidates[:-1]);best['best_independent_seconds']=total_fit
 # Same data as the Pick estimator, with four starts, checks exact-interpolation equality.
 same=[]
 for frac in [.1,.35,.65,.9]:
  ai=np.mean(c)+np.sqrt(1-frac)*(cheap_atoms-np.mean(c))
  tic=time.perf_counter();ss=fit(z,g,k,ai,np.ones(k)/k,frac*upper,support,upper);ss['seconds']=time.perf_counter()-tic;ss['errors']=errors(ss,row);same.append(ss)
 sb=min(same,key=lambda d:d['cost']).copy();sb['total_seconds']=sum(d['seconds'] for d in same)
 out.append({'key':key,'N':row['N'],'k':k,'true_variance':row['true_variance'],'node_rule':'observed spectral midpoint/halfspan; Pick m=k x=.8half linspace, eta=.3half; fit m=32 same rule; Ying32 conjugate pairs ellipse1.15half,.6half','pick':serial(r),'eigenmatrix':serial(e),'full_forward_fit':serial(best),'fit_candidates':[serial(x) for x in candidates],'same_nodes_fit':serial(sb)})
 for name,val in [('pick_z',z),('pick_g',g),('eigen_z',ze),('eigen_g',ge),('fit_z',zf),('fit_g',gf)]:arrays[key+'_'+name]=val
 print(key,'W1',r['errors']['wasserstein1'],e['errors']['wasserstein1'],best['errors']['wasserstein1'],flush=True)
json.dump(out,open('matched_comparison_results.json','w'),indent=2)
np.savez_compressed('matched_comparison_raw.npz',**arrays)
print('\nSUMMARY')
for k in [3,5]:
 for v in [.0625,.5625]:
  rr=[r for r in out if r['k']==k and r['true_variance']==v]
  for method in ['pick','eigenmatrix','full_forward_fit','same_nodes_fit']:
   ms=[r[method] for r in rr]
   print(k,v,method,'mean t/W1 errors',[float(np.mean([r['errors'][key] for r in ms])) for key in ['variance','wasserstein1']],'median sec',float(np.median([r.get('total_multistart_seconds',r.get('total_seconds')) for r in ms])))

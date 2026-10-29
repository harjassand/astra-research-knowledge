"""Exact-form CP transition matrices in the diagonal exterior basis; floating trajectory sampling."""
import numpy as np,itertools,json,time
from pathlib import Path
p=np.array([1,1,1,2,2,3,3,3],float)/16;r=8;S={};F={};basis={k:list(itertools.combinations(range(r),k)) for k in range(1,r+1)}
for k in range(1,r):
 old=basis[k];new=basis[k+1];oi={a:i for i,a in enumerate(old)};ni={a:i for i,a in enumerate(new)};s=np.zeros((len(new),len(old)))
 for J,jj in ni.items():
  for a in J:s[jj,oi[tuple(x for x in J if x!=a)]]+=p[a]/(k+1)
 f=np.zeros((len(old),len(old)))
 for I,ii in oi.items():
  f[ii,ii]=1-2*(1-sum(p[a] for a in I))/(k+1)
  for j in range(r):
   if j not in I:f[ii,:]+=s[ni[tuple(sorted(I+(j,)))],:]/(k+1)
 assert np.min(f)>-1e-14 and np.max(np.abs(np.sum(s,axis=0)+np.sum(f,axis=0)-1))<1e-14
 S[k]=s;F[k]=f
rng=np.random.default_rng(202610291109);trials=2000;cap=2048;rows=[];st=time.time();minimum_ratio=10;max_norm_error=0.
for trial in range(trials):
 k=0;programs=0;omega=None;calls=0;minus=0;measurements=0
 while calls<cap and programs<2:
  calls+=1
  if rng.random()>=4/9:continue
  minus+=1
  if k==0:k=1;omega=p.copy();continue
  measurements+=1;v=S[k]@omega;ps=float(v.sum());lo=(r-k)/(16*(k+1));minimum_ratio=min(minimum_ratio,ps/lo);assert ps>=lo-1e-12
  if rng.random()<ps:
   omega=v/ps;k+=1
   if k==8:programs+=1;k=0;omega=None
  else:omega=F[k]@omega/(1-ps)
  if omega is not None:
   err=abs(omega.sum()-1);max_norm_error=max(max_norm_error,float(err));assert err<1e-10 and np.min(omega)>-1e-12;omega/=omega.sum()
 rows.append(dict(programs=programs,calls=calls,minus=minus,growth_measurements=measurements))
res=dict(scope='Two-axis iid quantum growth instrument simulated in its exact diagonal exterior-basis reduction; no native9-level circuit or arbitrary-memory yield claim',trials=trials,cap=cap,ready=sum(x['programs']==2 for x in rows),ready_fraction=sum(x['programs']==2 for x in rows)/trials,mean_calls=float(np.mean([x['calls'] for x in rows])),mean_growth_measurements=float(np.mean([x['growth_measurements'] for x in rows])),minimum_ratio_to_uniform_lower=minimum_ratio,max_step_normalization_residual=max_norm_error,seconds=time.time()-st,rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print({k:v for k,v in res.items() if k!='rows'})

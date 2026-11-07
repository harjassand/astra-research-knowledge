from pathlib import Path
import numpy as np,json
rng=np.random.default_rng(70117);rows=[]
for n in [4,8,14]:
 for j in range(6):
  v,_=np.linalg.qr(rng.normal(size=(n,n)));lam=np.r_[0.,np.geomspace(1e-8,30,n-1)];rt=(v*np.sqrt(lam))@v.T
  vv,_=np.linalg.qr(rng.normal(size=(n,n)));ee=rng.uniform(-.01,.01,n);E=(vv*ee)@vv.T;C=rt@(np.eye(n)+E)@rt
  mm=1+rng.uniform(-.01,.01,n);ri=np.diag(1/np.sqrt(mm));rs=np.diag(np.sqrt(mm));w,u=np.linalg.eigh(ri@C@ri);w=np.maximum(w,0);w[0]=0;d=max(float(np.linalg.norm(E,2)),float(max(abs(mm-1))));err=0.
  for t in np.logspace(-5,11,57):
   aa=(v*np.exp(-t*lam))@v.T;bb=ri@((u*np.exp(-t*w))@u.T)@rs;err=max(err,float(np.linalg.norm(aa-bb,2)))
  assert err<=8*d/(1-d)+1e-5
  rows.append({'n':n,'trial':j,'d':d,'maximum_error':err,'certificate':8*d/(1-d)})
ct=[]
for n in [100,1000,10000]:
 d=n**-.5;i=np.arange(n+1);lp=2*d*i;p=np.exp(lp-max(lp));p/=sum(p);ct.append({'n':n,'local_log_rate_error':d,'unbiased_mean':.5,'biased_mean':float(p@i/n)})
r={'physical_experiments':0,'cases':rows,'changing_stationary_law_counterexample':ct};Path(__file__).with_name('mass_metric_result.json').write_text(json.dumps(r,indent=2));print(json.dumps({'cases':len(rows),'largest_error':max(z['maximum_error'] for z in rows),'smallest_bound':min(z['certificate'] for z in rows),'counterexample':ct},indent=2))

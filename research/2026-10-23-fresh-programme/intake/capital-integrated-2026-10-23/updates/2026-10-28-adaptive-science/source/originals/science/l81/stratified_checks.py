"""Compare iid/stratified legal covariance actions. Diagnostics only."""
from pathlib import Path
import csv, json, math
import numpy as np
from covariance_sampler import QueryOracle, corrected_sampler

HERE=Path(__file__).resolve().parent
rng=np.random.default_rng(8102719)
v=(1-math.exp(-2))/2
varq=math.exp(-2)-1/8-3*math.exp(-4)/8
rows=[]
for k in [1,2,4,8,16,32,64]:
    a=np.arange(k)/k;b=np.arange(1,k+1)/k
    means=math.exp(-1)*k*(np.sinh(b)-np.sinh(a))
    moments=math.exp(-2)*k*((b-a)/2+(np.sinh(2*b)-np.sinh(2*a))/4)
    stratvar=float(np.sum(moments-means*means)/k**2)
    rows.append(dict(k=k,iid_qbar_variance=varq/k,stratified_qbar_variance=stratvar,
                     variance_ratio=(varq/k)/stratvar,proved_stratified_upper_bound=v*v/(12*k**3)))
with (HERE/'stratified_time_variance.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(rows,indent=2),flush=True)

# Both legal samplers use n+4k values. Target samples are an independent reference.
results=[]
for dim,n,k,reps in [(4096,8,8,512),(65536,8,8,384)]:
    result=dict(dim=dim,n=n,k=k,queries=n+4*k,trials=reps)
    for name,flag in [('iid',False),('stratified',True)]:
        shells=[]
        for start in range(0,reps,4):
            batch=min(4,reps-start);q=QueryOracle(np.sin)
            y=corrected_sampler(q,n,k,batch,dim,1.0,rng,stratified_time=flag)
            assert q.queries_per_execution==n+4*k
            shells.extend((np.sum(y*y,axis=1)-dim)/np.sqrt(2*dim))
        shells=np.array(shells)
        result[name]=dict(radial_mean=float(shells.mean()),radial_sd=float(shells.std(ddof=1)),
                          outside_two_sd=float(np.mean(np.abs(shells)>2)))
    target=[]
    for start in range(0,reps,4):
        z=rng.standard_normal((min(4,reps-start),dim))
        target.extend((np.sum(z*z,axis=1)-dim)/np.sqrt(2*dim))
    target=np.array(target)
    result['target']=dict(radial_mean=float(target.mean()),radial_sd=float(target.std(ddof=1)),
                          outside_two_sd=float(np.mean(np.abs(target)>2)))
    results.append(result);print(json.dumps(result),flush=True)
(HERE/'stratified_checks.json').write_text(json.dumps(dict(seed=8102719,time_variance=rows,law_diagnostics=results),indent=2)+'\n')

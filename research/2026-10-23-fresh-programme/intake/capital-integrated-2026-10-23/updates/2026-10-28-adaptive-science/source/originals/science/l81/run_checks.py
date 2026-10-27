from pathlib import Path
import csv, json, math
import numpy as np
from covariance_sampler import QueryOracle, covariance_action, corrected_sampler, ordinary_sampler, safe_bound, ordinary_bound

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(2026102781)
records = {}
A = np.array([[0.4, 0.13, 0.0], [0.13, -0.3, 0.08], [0.0, 0.08, 0.2]])
b = np.array([0.6, -0.4, 0.2])
v = rng.standard_normal((10000, 3))
q = QueryOracle(lambda x: x @ A.T + b)
j = covariance_action(q, v, rng)
records['affine_action'] = dict(queries=q.queries_per_execution,
    max_abs_error=float(np.max(np.abs(j-v @ (A@A).T))),
    rms_error=float(np.mean((j-v @ (A@A).T)**2)**0.5))
A = np.diag([0.2, 0.4, 0.6]); w = np.ones(3)/np.sqrt(3.0); beta = 0.3
cov = A@A + beta*np.exp(-0.5)*(np.outer(A@w,w)+np.outer(w,A@w)) + beta**2*(1-np.exp(-2))/2*np.outer(w,w)
q = QueryOracle(lambda x: x@A.T + beta*np.sin(x@w)[:,None]*w)
N = 120000
est = np.zeros((3,3)); se = np.zeros((3,3)); maxratio=0.0
for col in range(3):
    inp = np.zeros((N,3)); inp[:,col]=1.0
    jj = covariance_action(q, inp, rng)
    est[:,col]=jj.mean(axis=0)
    se[:,col]=jj.std(axis=0, ddof=1)/np.sqrt(N)
    maxratio=max(maxratio,float(np.linalg.norm(jj,axis=1).max()))
records['noncommuting_action'] = dict(samples_per_column=N, exact_covariance=cov.tolist(),
    estimated_covariance=est.tolist(), standard_errors=se.tolist(),
    max_standardized_error=float(np.max(np.abs(est-cov)/se)),
    max_action_norm=maxratio, guaranteed_norm_bound=0.9**2)
A = np.diag([0.4, -0.7, 0.9]); b=np.array([1.2,-0.8,0.6]); sigma=1.0
n,k,batch=7,3,100000
q=QueryOracle(lambda x:x@A.T+b)
y=corrected_sampler(q,n,k,batch,3,sigma,rng)
theory=np.eye(3)+np.linalg.matrix_power(A,4)/(2*n*n)
records['affine_law'] = dict(n=n,k=k,queries=q.queries_per_execution,
    expected_queries=n+4*k, mean=y.mean(axis=0).tolist(), target_mean=b.tolist(),
    sample_covariance=np.cov(y,rowvar=False).tolist(), exact_output_covariance=theory.tolist(),
    max_mean_standard_error=float(np.max(np.abs(y.mean(axis=0)-b)/np.sqrt(np.diag(theory)/batch))))
rows=[]
for dim in [16,64,256,1024,4096]:
    eps=0.1;best=None
    upper=math.ceil(12*dim**(1/3)*eps**(-2/3))
    for n in range(1,upper+1):
        det=safe_bound(dim,n,10**18)
        if det<eps:
            k=max(1,math.ceil(dim/(2*n*n*(eps-det))))
            if safe_bound(dim,n,k)<=eps and (best is None or n+4*k<best[0]):best=(n+4*k,n,k)
    total,n,k=best
    trials=2400 if dim<=256 else 1200
    target=rng.standard_normal((trials,dim));corr=[];base=[]
    max_batch=64 if dim<=1024 else 24
    for start in range(0,trials,max_batch):
        batch=min(max_batch,trials-start)
        qc=QueryOracle(np.sin);corr.append(corrected_sampler(qc,n,k,batch,dim,1.0,rng))
        qb=QueryOracle(np.sin);base.append(ordinary_sampler(qb,total,batch,dim,1.0,rng))
        assert qc.queries_per_execution==qb.queries_per_execution==total
    corr=np.vstack(corr);base=np.vstack(base)
    def diagnostics(arr):
        shell=(np.sum(arr*arr,axis=1)-dim)/np.sqrt(2*dim)
        return dict(radial_mean=float(shell.mean()), radial_sd=float(shell.std(ddof=1)),
                    shell_outside=float(np.mean(np.abs(shell)>1.5)),
                    first_coordinate_positive=float(np.mean(arr[:,0]>0)),
                    first_coordinate_abs_gt_1=float(np.mean(np.abs(arr[:,0])>1)))
    rec=dict(dim=dim,n=n,k=k,total_queries=total,trials=trials,
       corrected_TV_upper_bound=safe_bound(dim,n,k),ordinary_TV_upper_bound=ordinary_bound(dim,total),
       corrected=diagnostics(corr),ordinary_equal_queries=diagnostics(base),target=diagnostics(target))
    rows.append(rec);print(json.dumps(rec),flush=True)
records['nonlinear_diagnostics']=rows
(HERE/'checks.json').write_text(json.dumps(records,indent=2)+'\n')
with (HERE/'diagnostics.csv').open('w',newline='') as f:
    keys=['dim','n','k','total_queries','trials','corrected_TV_upper_bound','ordinary_TV_upper_bound']
    w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
    for r in rows:w.writerow({key:r[key] for key in keys})
print('Wrote checks.json and diagnostics.csv',flush=True)

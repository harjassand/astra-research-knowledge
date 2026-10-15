"""Joint raw-mean f0/a/B fit, equal-variance noise, same data and starts."""
import time,json
import numpy as np
from scipy.optimize import least_squares
from benchmark import OUT,setup,response,metric
D=OUT/'joint_raw_fit';D.mkdir(exist_ok=True)
results=[];start=time.perf_counter()
for m in range(5,11):
 masks,ii,jj=setup(m)
 for seed in range(2):
  for design in ['two_anchor','random']:
   tag=f'm{m}_seed{seed}_noise0.001_{design}';data=np.load(OUT/(tag+'.npz'));train=data['train'];held=data['heldout'];target=data['raw'][train].mean(1);truth=data['truth'];mtrain=masks[train]
   f0=data['raw'][0].mean();a=data['raw'][1<<np.arange(m)].mean(1)-f0
   def calc(p):
    f=p[0];a=p[1:1+m];b=p[1+m:];B=np.zeros((m,m));B[ii,jj]=b
    M=np.eye(m)[None,:,:]+mtrain[:,:,None]*B[None,:,:]*mtrain[:,None,:]
    x=np.linalg.solve(M,mtrain[:,:,None])[:,:,0]
    y=np.linalg.solve(M.transpose(0,2,1),(mtrain*a)[:,:,None])[:,:,0]
    return f+x@a,np.column_stack((np.ones(len(train)),x,-y[:,ii]*x[:,jj]))
   class Cache:
    def __init__(self):self.p=None
    def calculate(self,p):
     if self.p is None or not np.array_equal(self.p,p):self.p=p.copy();self.g,self.j=calc(p)
    def fun(self,p):self.calculate(p);return self.g-target
    def jac(self,p):self.calculate(p);return self.j
   fits=[]
   for restart in range(12):
    rr=np.random.default_rng(44000+1000*m+100*seed+restart)
    b=np.zeros(len(ii)) if restart==0 else rr.normal(0,.04,len(ii));p0=np.r_[f0,a,b]
    c=Cache();t=time.perf_counter()
    opt=least_squares(c.fun,p0,jac=c.jac,method='trf',bounds=(np.r_[np.full(m+1,-np.inf),np.full(len(ii),-.6)],np.r_[np.full(m+1,np.inf),np.full(len(ii),.6)]),max_nfev=1000,ftol=1e-11,xtol=1e-11,gtol=1e-11)
    elapsed=time.perf_counter()-t;pred=opt.x[0]+response(opt.x[1+m:],opt.x[1:m+1],masks,ii,jj);err=pred-truth
    B=np.zeros((m,m));B[ii,jj]=opt.x[1+m:]
    record=dict(m=m,seed=seed,design=design,restart=restart,noise_raw_sd=.001,repeats=4,calibration_settings=len(train),calibration_readings=4*len(train),nfev=opt.nfev,njev=opt.njev,optimizer_success=bool(opt.success),status=int(opt.status),runtime_seconds=elapsed,train_raw_mean_rmse=float(np.sqrt(np.mean(opt.fun**2))),heldout=metric(err,held),all_table=metric(err,np.arange(2**m)),fitted_euclidean_shifted_margin=float(np.linalg.eigvalsh(np.eye(m)+(B+B.T)/2).min()))
    fits.append((opt.x,pred,record));results.append(record)
   best=min(range(12),key=lambda j:fits[j][2]['train_raw_mean_rmse'])
   for j in range(12):fits[j][2]['selected_by_training_loss']=(j==best)
   np.savez_compressed(D/(tag+'.npz'),fit_parameters=np.array([x[0] for x in fits]),predictions=np.array([x[1] for x in fits]),errors=np.array([x[1]-truth for x in fits]),train=train,heldout=held,truth=truth)
   print(tag,'best',best,'train',fits[best][2]['train_raw_mean_rmse'],'held',fits[best][2]['heldout']['rmse'],flush=True)
   (D/'results.json').write_text(json.dumps(results,indent=2))
# Check ALL parameter derivatives against finite differences, at last calibration initializer.
g,J=calc(p0);eps=1e-6;fd=np.column_stack([(calc(p0+eps*np.eye(len(p0))[k])[0]-calc(p0-eps*np.eye(len(p0))[k])[0])/(2*eps) for k in range(len(p0))])
(D/'metadata.json').write_text(json.dumps(dict(elapsed_seconds=time.perf_counter()-start,jacobian_finite_difference_max_abs=float(np.max(abs(J-fd)))),indent=2))
print('DONE',time.perf_counter()-start,flush=True)

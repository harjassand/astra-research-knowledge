"""Synthetic binary scalar-resolvent fitting. No measured/hardware data.
Run: OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python benchmark.py
"""
import os,time,json,itertools,platform
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import least_squares
OUT=Path(__file__).resolve().parent

def setup(m):
    masks=((np.arange(2**m)[:,None]>>np.arange(m))&1).astype(float)
    ii,jj=np.where(~np.eye(m,dtype=bool))
    return masks,ii,jj

def response(theta,a,masks,ii,jj,jac=False):
    m=len(a); B=np.zeros((m,m));B[ii,jj]=theta
    M=np.eye(m)[None,:,:]+masks[:,:,None]*B[None,:,:]*masks[:,None,:]
    x=np.linalg.solve(M,masks[:,:,None])[:,:,0]
    g=x@a
    if not jac:return g
    y=np.linalg.solve(M.transpose(0,2,1),(masks*a)[:,:,None])[:,:,0]
    return g,-y[:,ii]*x[:,jj]

def truth(m,seed):
    rng=np.random.default_rng(10000+m*100+seed)
    R=rng.normal(size=(m,m)); S=(R+R.T)/2; S*=.65/np.linalg.norm(S,2)
    R=rng.normal(size=(m,m)); K=(R-R.T)/2; K*=.55/np.linalg.norm(K,2)
    H0=np.eye(m)+S+K
    L=1+np.diag(H0);B=H0/L[None,:];np.fill_diagonal(B,0)
    a=rng.uniform(.5,1.5,m)
    # H0 is accretive and realizable by A=H0^-1, P=I. t=1, W=I.
    weighted=(np.eye(m)+B)*np.sqrt(L[None,:]/L[:,None])
    return B,a,H0,L,{'H0_accretivity':float(np.linalg.eigvalsh((H0+H0.T)/2).min()),'true_weighted_shifted_margin':float(np.linalg.eigvalsh((weighted+weighted.T)/2).min()),'true_full_condition':float(np.linalg.cond(np.eye(m)+B))}

def metric(e,sel):
    z=e[sel]
    return {'rmse':float(np.sqrt(np.mean(z*z))),'max_abs':float(np.max(abs(z)))} if len(z) else {'rmse':None,'max_abs':None}

def main():
    start=time.perf_counter(); records=[]; audits=[]
    for m in range(5,11):
      masks,ii,jj=setup(m);common=np.where(masks.sum(1)<=1)[0];pool=np.where(masks.sum(1)>=2)[0]
      anchor=np.where(masks[:,2:].sum(1)<=2)[0];n=len(anchor)
      for seed in range(2):
        B,a,H0,L,phys=truth(m,seed);gt=response(B[ii,jj],a,masks,ii,jj);f0=.3
        rng=np.random.default_rng(22000+100*m+seed)
        random=np.sort(np.r_[common,rng.choice(pool,n-len(common),replace=False)])
        for noise in (0.,1.e-3):
          repeats=1 if noise==0 else 4
          nrng=np.random.default_rng(33000+100*m+seed)
          # Same virtual raw noise table used for overlapping settings in either design.
          raw=f0+gt[:,None]+nrng.normal(0,noise,(2**m,repeats))
          means=raw.mean(1);fhat=means[0];ahat=means[1<<np.arange(m)]-fhat
          for design,train in [('two_anchor',anchor),('random',random)]:
            fitids=np.setdiff1d(train,common);held=np.setdiff1d(np.arange(2**m),train)
            target=means[fitids]-fhat
            def funjac(p):return response(p,ahat,masks[fitids],ii,jj,True)
            class Cache:
              def __init__(self):self.p=None
              def calc(self,p):
                if self.p is None or not np.array_equal(self.p,p):self.p=p.copy();self.g,self.j=funjac(p)
              def fun(self,p):self.calc(p);return self.g-target
              def jac(self,p):self.calc(p);return self.j
            fits=[]
            for restart in range(12):
              rr=np.random.default_rng(44000+1000*m+100*seed+restart)
              p0=np.zeros(len(ii)) if restart==0 else rr.normal(0,.04,len(ii))
              c=Cache();t=time.perf_counter()
              opt=least_squares(c.fun,p0,jac=c.jac,method='trf',bounds=(-.6,.6),max_nfev=1000,ftol=1e-11,xtol=1e-11,gtol=1e-11)
              runtime=time.perf_counter()-t
              pred=fhat+response(opt.x,ahat,masks,ii,jj);err=pred-(f0+gt)
              BF=np.zeros((m,m));BF[ii,jj]=opt.x
              singular=np.linalg.svd(opt.jac,compute_uv=False)
              rec=dict(m=m,seed=seed,noise_raw_sd=noise,repeats=repeats,design=design,restart=restart,calibration_settings=n,calibration_readings=n*repeats,baseline_singleton_settings=m+1,joint_fit_settings=len(fitids),heldout_settings=len(held),all_table_settings=2**m,additional_truth_diagnostic_settings=len(held),runtime_seconds=runtime,nfev=opt.nfev,njev=opt.njev,status=int(opt.status),optimizer_success=bool(opt.success),train_measured_rmse=float(np.sqrt(np.mean(opt.fun**2))),all_table=metric(err,np.arange(2**m)),heldout=metric(err,held),training_truth=metric(err,train),parameter_frobenius_error=float(np.linalg.norm(BF-B)),fitted_euclidean_shifted_margin=float(np.linalg.eigvalsh(np.eye(m)+(BF+BF.T)/2).min()),jacobian_min_singular=float(singular[-1]),jacobian_rank_1e8=int(sum(singular>singular[0]*1e-8)),**phys)
              rec['exact_predictive_success']=bool(rec['all_table']['max_abs']<1e-7) if noise==0 else None
              fits.append((opt.x,pred,rec));records.append(rec)
            best=min(range(12),key=lambda j:fits[j][2]['train_measured_rmse'])
            for j in range(12):fits[j][2]['selected_by_training_loss']=(j==best)
            tag=f'm{m}_seed{seed}_noise{noise:g}_{design}'
            np.savez_compressed(OUT/(tag+'.npz'),B=B,a=a,H0=H0,L=L,masks=masks,truth=f0+gt,raw=raw,train=train,heldout=held,fit_parameters=np.array([f[0] for f in fits]),predictions=np.array([f[1] for f in fits]),errors=np.array([f[1]-(f0+gt) for f in fits]))
            pairdiff=max(np.linalg.norm(fits[i][0]-fits[j][0]) for i in range(12) for j in range(i))
            rec=fits[best][2]
            audits.append(dict(tag=tag,best_restart=best,max_parameter_difference_between_starts=float(pairdiff),max_prediction_difference_between_starts=float(max(np.max(abs(fits[i][1]-fits[j][1])) for i in range(12) for j in range(i)))))
            print(tag,'best',best,'train',f'{rec["train_measured_rmse"]:.2g}','held',f'{rec["heldout"]["rmse"]:.2g}','time',f'{sum(f[2]["runtime_seconds"] for f in fits):.1f}',flush=True)
            (OUT/'results.json').write_text(json.dumps(records,indent=2));(OUT/'audits.json').write_text(json.dumps(audits,indent=2))
    # Central-difference adjoint check independent of fit outcomes.
    m=6; masks,ii,jj=setup(m);B,a,*_=truth(m,99);p=B[ii,jj];g,J=response(p,a,masks,ii,jj,True);eps=1e-6
    fd=np.column_stack([(response(p+eps*np.eye(len(p))[k],a,masks,ii,jj)-response(p-eps*np.eye(len(p))[k],a,masks,ii,jj))/(2*eps) for k in range(len(p))])
    metadata=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,elapsed_seconds=time.perf_counter()-start,analytic_jacobian_max_absolute_error=float(abs(J-fd).max()),blas_threads=os.getenv('OPENBLAS_NUM_THREADS'))
    (OUT/'metadata.json').write_text(json.dumps(metadata,indent=2));print(metadata,flush=True)
if __name__=='__main__':main()

"""Matched cap-constrained full-likelihood baseline, fixed seeds, CPU only.

One positive forward sweep plus analytic adjoint per objective/gradient call.
Cheap first-generation initialization and inverse warm start both included.
No claim of global likelihood optimality or statistical domination.
"""
import json,time,platform,sys
import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.linalg import expm
from positive_causal_inverse import positive_inverse,choose_order
from causal_clipped_inverse import numerical_defect,repair_prefix_mass,clipped_inverse
from fragment_inverse import generator
from no_sc_noise_test import true_cell_masses


def likelihood_gradient(k,y,rates,a,tolerance=1e-13):
    """Poisson endpoint likelihood and exact truncated-series adjoint."""
    n=len(k);J,_=choose_order(a,max(1.,float(sum(k))),tolerance)
    z=1-rates;u=np.zeros((J+1,n));u[0,0]=np.exp(-a)
    for r in range(1,J+1):
        u[r]=(a/r)*(z*u[r-1]+np.convolve(k,rates*u[r-1])[:n])
    pred=np.sum(u,axis=0);safe=np.maximum(pred,1e-300)
    d=1-y/safe;d[0]=0
    loss=float(sum(safe[1:]-y[1:]*np.log(safe[1:])))
    g=np.zeros(n);adj=d.copy()
    for r in range(J,0,-1):
        g+=(a/r)*np.correlate(adj,rates*u[r-1],mode='full')[n-1:]
        adj=d+(a/r)*(z*adj+rates*np.correlate(adj,k,mode='full')[n-1:])
    return loss,g,pred,J


def measure(k,truth,y,rates,a):
    loss,grad,pred,J=likelihood_gradient(k,y,rates,a)
    repaired=repair_prefix_mass(k)
    rloss,_,rpred,_=likelihood_gradient(repaired,y,rates,a)
    return {'kernel_l1_pre':float(sum(abs(k-truth))),
       'kernel_l1_repaired':float(sum(abs(repaired-truth))),
       'prefix_mass':float(sum(k)),'poisson_objective_pre':loss,
       'poisson_objective_repaired':rloss,
       'endpoint_l1_pre':float(sum(abs(pred-y))),
       'endpoint_l1_repaired':float(sum(abs(rpred-y))),
       'evaluation_order':J}


def fit(y,rates,a,cap,x0,truth,maxiter=500):
    calls=0;trace=[];st=time.perf_counter()
    def fun(x):
        nonlocal calls
        calls+=1
        f,g,_,_=likelihood_gradient(np.r_[0.,x],y,rates,a)
        return f,g[1:]
    def callback(x):
        k=np.r_[0.,x]
        trace.append({'iteration':len(trace)+1,'seconds':time.perf_counter()-st,
            'kernel_l1_repaired':float(sum(abs(repair_prefix_mass(k)-truth)))})
    res=minimize(fun,x0[1:],jac=True,bounds=[(0.,cap)]*(len(y)-1),
        method='L-BFGS-B',callback=callback,
        options={'maxiter':maxiter,'ftol':1e-13,'gtol':1e-9,'maxls':30,'maxcor':20})
    secs=time.perf_counter()-st;k=np.r_[0.,res.x]
    pg=res.jac.copy()
    pg[(res.x<=0)&(pg>0)]=0;pg[(res.x>=cap)&(pg<0)]=0
    return k,{'optimization_seconds':secs,'objective_gradient_calls':calls,
       'iterations':int(res.nit),'success':bool(res.success),'message':str(res.message),
       'projected_gradient_sup':float(max(abs(pg))),
       'trace':trace}


def main():
    seed=941038;rng=np.random.default_rng(seed)
    out={'seed':seed,'settings':{'a':2.,'L':4.,'M':2.,'poisson_exposure':100000,
       'cap':'M*h','tail_tolerance_inverse':1e-12,'tail_tolerance_fit':1e-13,
       'mass_constraint':'same post-hoc prefix mass repair for both; no hidden simplex constraint',
       'fit':'L-BFGS-B analytic adjoint, cap bounds, maxiter 500, ftol 1e-13, gtol 1e-9',
       'timing':'single-process wall clock; no package import/truth generation; rate setup, initialization, optimization and repair separately recorded',
       'error_target':'same realization direct repaired L1 error; oracle diagnostic only'},
       'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,
                      'platform':platform.platform()},'gradient_check':{},'cases':[]}
    n=19;a=1.4;q=.97;rates=q**np.arange(n)
    k=np.r_[0.,rng.uniform(.005,.035,n-1)];y=rng.uniform(.005,.025,n);y[0]=np.exp(-a)
    loss,g,p,J=likelihood_gradient(k,y,rates,a)
    exact=expm(a*generator(k,q))[:,0]
    err=[]
    for j in [1,3,7,18]:
        kp=k.copy();km=k.copy();kp[j]+=1e-6;km[j]-=1e-6
        fd=(likelihood_gradient(kp,y,rates,a)[0]-likelihood_gradient(km,y,rates,a)[0])/2e-6
        err.append(abs(fd-g[j]))
    out['gradient_check']={'max_forward_error':float(max(abs(exact-p))),
                           'max_central_difference_error':float(max(err)),'order':J}
    raw={}
    for n in [101,501]:
      for gamma in [1.3,.02]:
        h=4/(n-1);a=2.;cap=2*h;logq=-gamma*h
        st=time.perf_counter();rates=np.exp(logq*np.arange(n));q=np.exp(logq);setup=time.perf_counter()-st
        truth=true_cell_masses(h,n)
        _,_,f,_=likelihood_gradient(truth,np.zeros(n),rates,a)
        y=rng.poisson(f*100000)/100000;y[0]=f[0]
        st=time.perf_counter();direct,diag=positive_inverse(y,a,cap,rates=rates);direct_s=time.perf_counter()-st
        st=time.perf_counter();repaired=repair_prefix_mass(direct);repair_s=time.perf_counter()-st
        md=measure(direct,truth,y,rates,a)
        st=time.perf_counter();defect,_,_=numerical_defect(direct,y,q,a,cap);check_s=time.perf_counter()-st
        case={'n':n,'gamma':gamma,'rate_setup_seconds':setup,
            'direct':dict(md,seconds=direct_s,repair_seconds=repair_s,
             optional_forward_check_seconds=check_s,defect=defect,
             uniformization_order=diag['order'],tail_bound=diag['tail_l1_bound']), 'fits':[]}
        if n==101:
            st=time.perf_counter();mp,_,wmax=clipped_inverse(y,q,a,cap,dps=100);mp_s=time.perf_counter()-st
            case['high_precision_causal']={'decimal_digits':100,'seconds':mp_s,
                'difference_to_positive_l1':float(sum(abs(mp-direct))),'W_max':wmax}
        for start in ['first_generation','direct_warm_start']:
            st=time.perf_counter()
            if start=='first_generation':
                z=-np.expm1(logq*np.arange(1,n));A=np.exp(-a)*np.expm1(a*z)/z
                x0=np.r_[0.,np.clip(y[1:]/A,0,cap)]
                init_s=time.perf_counter()-st
            else:x0=direct.copy();init_s=direct_s
            fitted,info=fit(y,rates,a,cap,x0,truth)
            st=time.perf_counter();repair_prefix_mass(fitted);fitrepair_s=time.perf_counter()-st
            info.update(measure(fitted,truth,y,rates,a))
            info.update(initializer=start,initialization_seconds=init_s,
                repair_seconds=fitrepair_s,total_including_initializer_seconds=init_s+info['optimization_seconds']+fitrepair_s)
            target=md['kernel_l1_repaired'];initialerr=float(sum(abs(repair_prefix_mass(x0)-truth)))
            hit=next((v for v in info['trace'] if v['kernel_l1_repaired']<=target),None)
            info['first_oracle_equal_error_seconds']=(init_s if initialerr<=target else
                (None if hit is None else init_s+hit['seconds']))
            case['fits'].append(info)
            raw[f'n{n}_g{gamma}_{start}']=fitted
        out['cases'].append(case)
        raw[f'n{n}_g{gamma}_truth']=truth;raw[f'n{n}_g{gamma}_observed']=y;raw[f'n{n}_g{gamma}_direct']=direct
        print(json.dumps({key:val for key,val in case.items() if key!='fits'}),flush=True)
        for info in case['fits']:print(json.dumps({key:val for key,val in info.items() if key!='trace'}),flush=True)
    np.savez_compressed('positive_fit_raw_arrays.npz',**raw)
    json.dump(out,open('positive_fit_results.json','w'),indent=2)
    print('Gradient check:',out['gradient_check'],flush=True)

if __name__=='__main__':main()

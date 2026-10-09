"""Static recovery of irreversible entropy production in a known quartic-potential family.

FULL model acquisition: samples from 4 perturbed stationary densities; logistic
ratios for B; baseline score matching of all unknown H and quartic coefficient;
plug-in reconstruction of the stationary current and physical entropy production.

The quartic parametrization is SUPPLIED, not discovered from data.
This is a synthetic demonstration under restrictive, testable structure.
"""
from __future__ import annotations
import argparse,json,time
import numpy as np
from stationary_tilt_experiment import (H,QUARTIC,D,K,B,A_TRUE,U,DIM,
        sample_exact,estimate_ratio)


def fit_potential(x):
    n,d=x.shape
    # Symmetric H_ij (diagonal d, then i<j), plus isotropic quartic parameter.
    hs=[];ds=[]
    for i in range(d):
        h=np.zeros((d,d));h[i,i]=1
        hs.append(h);ds.append(-1.)
    for i in range(d):
        for j in range(i+1,d):
            h=np.zeros((d,d));h[i,j]=h[j,i]=1
            hs.append(h);ds.append(0.)
    feature=np.stack([-x@h for h in hs]+[-x**3],axis=-1)
    G=np.einsum('ndp,ndq->pq',feature,feature)/n
    div=np.array(ds +[-3.*np.sum(x*x)/n])
    params=np.linalg.solve(G,-div)
    Hhat=np.einsum('p,pij->ij',params[:-1],np.array(hs))
    lam=params[-1]
    return Hhat,lam


def ep_from_samples(x, Bhat,Hhat,lam):
    Dhat=(Bhat+Bhat.T)*0.5
    Khat=(Bhat-Bhat.T)*0.5
    if np.linalg.eigvalsh(Dhat).min()<=0:return float('nan')
    s=-x@Hhat-lam*x**3
    current=s@Khat.T
    return float(np.einsum('ni,ij,nj->',current,np.linalg.inv(Dhat),current)/len(x))


def replicate(n, rng, ref):
    start=time.perf_counter()
    x0,queries=sample_exact(n,np.zeros(DIM),rng)
    a_log=np.zeros((DIM,DIM));a_moment=np.zeros_like(a_log)
    mean=x0.mean(axis=0);cov=np.cov(x0.T)
    for i in range(DIM):
        xi,q=sample_exact(n,A_TRUE[:,i],rng);queries+=q
        a_log[:,i]=estimate_ratio(x0,xi)
        a_moment[:,i]=np.linalg.solve(cov,xi.mean(axis=0)-mean)
    Bhat=U@np.linalg.inv(a_log)
    Bmom=U@np.linalg.inv(a_moment)
    Hhat,lam=fit_potential(x0)
    ep_hat=ep_from_samples(x0,Bhat,Hhat,lam)
    ep_moment=ep_from_samples(x0,Bmom,Hhat,lam)
    return {'n_per_regime':n,'total_samples':4*n,'generator_proposals':queries,
            'generation_and_analysis_seconds':time.perf_counter()-start,
            'estimated_potential_lambda':float(lam),
            'potential_H_rel_error':float(np.linalg.norm(H-Hhat)/np.linalg.norm(H)),
            'entropy_production_estimate':ep_hat,
            'entropy_production_rel_error':abs(ep_hat-ref)/ref,
            'moment_based_entropy_prod':ep_moment,
            'moment_based_entropy_prod_rel_error':abs(ep_moment-ref)/ref,
            'true_entropy_production':ref}


def main():
    p=argparse.ArgumentParser();p.add_argument('--n',nargs='+',type=int,default=[2000,8000,32000]);p.add_argument('--reps',type=int,default=12);p.add_argument('--output',default='entropy_production_results.json');args=p.parse_args()
    rng=np.random.default_rng(726212)
    # Independently acquired reference with accounted proposals
    ref_samples,ref_queries=sample_exact(750000,np.zeros(DIM),rng)
    ref=ep_from_samples(ref_samples,B,H,QUARTIC)
    out={'known_potential_family':'symmetric-quadratic + shared quartic',
          'reference_entropy_production':ref,'reference_samples':len(ref_samples),
          'reference_proposals':ref_queries,'rows':[],'aggregate':[]}
    del ref_samples
    print('Reference entropy-production:',ref,'reference proposals:',ref_queries)
    for n in args.n:
        rows=[]
        for i in range(args.reps):
            v=replicate(n,rng,ref);rows.append(v);out['rows'].append(v)
        summary={'n_per_regime':n,'replications':len(rows)}
        for key in ['entropy_production_rel_error','moment_based_entropy_prod_rel_error','potential_H_rel_error',
                    'generation_and_analysis_seconds','generator_proposals','estimated_potential_lambda']:
            data=np.array([r[key] for r in rows]);summary[key+'_mean']=float(data.mean());summary[key+'_median']=float(np.median(data))
        out['aggregate'].append(summary);print(json.dumps(summary,indent=2))
    with open(args.output,'w') as f:json.dump(out,f,indent=2)

if __name__=='__main__':main()

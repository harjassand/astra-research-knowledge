"""Matched-labelled-snapshot comparison of exact density-ratio and score-moment estimators.

Model is an affine-tilted nonlinear quartic stationary family. Both algorithms
observe exactly the same baseline + three perturbed sample populations.
The score-moment estimator is additionally allowed to exploit the GIVEN form
of the quartic potential (its coefficients must be fitted from baseline data).
No hidden true coefficients are passed to either estimator. Count every draw.
"""
from __future__ import annotations
import argparse,json,time
import numpy as np
from stationary_tilt_experiment import sample_exact, estimate_ratio, H,D,K,B,U,A_TRUE,DIM
from entropy_production_experiment import fit_potential


def estimate_once(n,rng):
    start=time.perf_counter()
    x0,work=sample_exact(n,np.zeros(DIM),rng)
    Hhat, lam=fit_potential(x0)
    C0=np.cov(x0.T)
    mu0=np.mean(x0,axis=0)
    A_log=np.empty((DIM,DIM)); A_stein=np.empty_like(A_log);A_gauss=np.empty_like(A_log)
    for j in range(DIM):
        xi,wi=sample_exact(n,A_TRUE[:,j],rng);work+=wi
        A_log[:,j]=estimate_ratio(x0,xi)
        A_stein[:,j]=np.mean(xi@Hhat+lam*xi**3,axis=0)
        A_gauss[:,j]=np.linalg.solve(C0,np.mean(xi,axis=0)-mu0)
    truth_norm=np.linalg.norm(B)
    errs={}
    for label,a in [('ratio_logistic',A_log),('potential_score_mean',A_stein),('Gaussian_moment',A_gauss)]:
        try:
            Bhat=U@np.linalg.inv(a)
            errs[label+'_matrix_err']=float(np.linalg.norm(Bhat-B)/truth_norm)
            errs[label+'_D_err']=float(np.linalg.norm((Bhat+Bhat.T)/2-D)/np.linalg.norm(D))
            errs[label+'_K_err']=float(np.linalg.norm((Bhat-Bhat.T)/2-K)/np.linalg.norm(K))
        except np.linalg.LinAlgError:
            errs[label+'_matrix_err']=float('nan')
    errs.update({'n_per_regime':n,'total_samples':4*n,'proposals':work,
                 'acquire_sample_fit_seconds':time.perf_counter()-start,
                 'quartic_estimated':float(lam),'potential_H_rel_error':float(np.linalg.norm(Hhat-H)/np.linalg.norm(H))})
    return errs


def main():
    p=argparse.ArgumentParser();p.add_argument('--sizes',type=int,nargs='+',default=[500,2000,8000,32000]);p.add_argument('--reps',type=int,default=25);p.add_argument('--output',default='matched_comparator_results.json');a=p.parse_args()
    rng=np.random.default_rng(12026)
    data={'model':'3D stationary quartic affine ratio','potential_basis_known_and_parameters_estimated':True,
          'model_parameter_advantage':'score-moment estimator uses supplied quartic form; ratio logistic is correct without it',
          'rows':[],'aggregate':[]}
    for n in a.sizes:
        rows=[estimate_once(n,rng) for _ in range(a.reps)]
        data['rows'].extend(rows)
        summary={'n_per_regime':n,'replications':len(rows)}
        for k in ['ratio_logistic_matrix_err','potential_score_mean_matrix_err','Gaussian_moment_matrix_err',
                  'potential_H_rel_error','proposals','acquire_sample_fit_seconds']:
            vals=np.array([r[k] for r in rows]);summary[k+'_mean']=float(np.nanmean(vals));summary[k+'_median']=float(np.nanmedian(vals))
        data['aggregate'].append(summary)
        print(json.dumps(summary,indent=2))
    with open(a.output,'w') as f:json.dump(data,f,indent=2)

if __name__=='__main__':main()

"""Local Schur response bounds; no extensive slow-generator norm.

Uses the root-derived bounded-overlap fast-monomial coupling estimate, with the
PSD Schur refinement proved in LOCAL_SCHUR_PROOF.txt. This is a complete finite
algorithm for a separated hierarchy; bounds can be wide without that hierarchy.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json, math, time
from pathlib import Path
import numpy as np
from scipy.special import expit
from conditional_decimation import (SP,initial_model,one_decimation,
    edge_marginals,prefactors,source_variance,decimal_dense)
from audit_local_schur import local_theta

def fast_trial_slow_energy(J,rates,weights):
    n=len(weights);a=prefactors(rates)
    bn=np.arctanh(np.tanh(J[0::2])*np.tanh(J[1::2]))
    pairs=edge_marginals(bn)
    total=0.
    for k,i in enumerate(range(1,n,2)):
        pmid=pairs[k].sum(axis=0)
        triple=pairs[k][:,:,None]*pairs[k+1][None,:,:]/pmid[None,:,None]
        for l,L in enumerate(SP):
            for s,S in enumerate(SP):
                for r,R in enumerate(SP):
                    if triple[l,s,r]==0:continue
                    ml=math.tanh(J[i-1]*L+J[i]*S)
                    mr=math.tanh(J[i+1]*S+J[i+2]*R)
                    mlflip=math.tanh(J[i-1]*L-J[i]*S)
                    mrflip=math.tanh(-J[i+1]*S+J[i+2]*R)
                    pl=np.array([expit(2*x*(J[i-1]*L+J[i]*S)) for x in SP])
                    pr=np.array([expit(2*x*(J[i+1]*S+J[i+2]*R)) for x in SP])
                    dhleft=weights[i-1]*((SP-ml)/a[i-1,l,s]-(SP-mlflip)/a[i-1,l,1-s])
                    dhright=weights[i+1]*((SP-mr)/a[i+1,s,r]-(SP-mrflip)/a[i+1,1-s,r])
                    delta=dhleft[:,None]+dhright[None,:]
                    total+=.5*triple[l,s,r]*np.sum(pl[:,None]*pr[None,:]*rates[i,:,s,:]*delta**2)
    return float(total)

def local_response(J,rates,weights):
    begin=time.perf_counter();variance=source_variance(J,weights)[1];levels=[]
    while len(weights)>1:
        theta=local_theta(J,rates,True)
        theta_sup=local_theta(J,rates,False)
        c=fast_trial_slow_energy(J,rates,weights)
        J,rates,weights,rec=one_decimation(J,rates,weights)
        rec['global_theta']=rec.pop('theta')
        rec['local_theta']=theta;rec['local_sup_theta']=theta_sup
        rec['fast_trial_slow_energy']=c
        levels.append(rec)
    var=1-math.tanh(float(J.sum()))**2
    pref=float(prefactors(rates)[0,1,1])
    exactbase=float(weights[0]**2*var/pref)
    lower=upper=estimate=exactbase
    for rec in reversed(levels):
        b=rec['fast_response'];c=rec['fast_trial_slow_energy'];theta=rec['local_theta']
        crossing=math.sqrt(max(theta*upper*b,0))
        correction=max(b-crossing,0)**2/(b+c) if b+c else 0.
        lower=lower+correction
        upper=(1+theta)*upper+b+2*crossing
        estimate+=b
    return dict(estimate=estimate,lower=lower,upper=upper,
        relative_width=(upper-lower)/lower,levels=levels,seconds=time.perf_counter()-begin,
        source_variance=variance,final_projection_variance=float(weights[0]**2*var),
        final_projection_fraction=float(weights[0]**2*var/variance),
        final_slow_prefactor=pref)

def main():
    checks=[]
    for n,J,alpha in [(3,.8,1e-2),(7,1.2,1e-3),(7,1.2,1e-6)]:
        b,r,w,_=initial_model(n,J,alpha)
        out=local_response(b,r,w)
        exact=float(decimal_dense(n,J,alpha))
        checks.append(dict(n=n,J=J,alpha=alpha,exact_decimal=exact,response=out,
            contains=out['lower']<=exact<=out['upper']))
    collective=[]
    # Separation is independent of total n. Static correlation length scales with n.
    for n in [31,127,511,2047]:
        J=.5*math.log(n+1);alpha=1e-5
        b,r,w,nu=initial_model(n,J,alpha)
        out=local_response(b,r,w)
        collective.append(dict(n=n,J=J,alpha=alpha,clock_log10_span=-float(np.log10(nu.min())),response=out))
    out={'scope':'Local conditional-Schur bounds evaluated in floating point; no interval arithmetic, no historical-novelty or general algorithm superiority claim.',
        'small_decimal_checks':checks,'collective':collective}
    Path(__file__).with_name('local_response_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'checks_pass':all(x['contains'] for x in checks),
        'collective':[{k:x[k] for k in ['n','J','alpha','clock_log10_span']}|{k:x['response'][k] for k in ['estimate','lower','upper','relative_width','final_projection_fraction','seconds']} for x in collective]},indent=2))

if __name__=='__main__':main()

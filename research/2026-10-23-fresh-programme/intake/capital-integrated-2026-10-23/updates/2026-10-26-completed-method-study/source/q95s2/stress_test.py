#!/usr/local/bin/python3
"""Q95 stage 2. All observations are synthetic; no network or stage1 writes."""
from pathlib import Path
import csv, hashlib, json, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import log_ndtr, ndtri
from scipy.stats import beta as beta_distribution

P=Path(__file__).resolve().parent
ALPHA=.05
SIGMA=.02
RHO=1.
TIMES=np.geomspace(1e-3,1e6,64)
REPS=2000

def boundary(t,alpha):
    def f(s):
        v=t+RHO
        return math.log(2)+.5*math.log(RHO/v)+s*s/(2*v)+float(log_ndtr(s/math.sqrt(v)))+math.log(alpha)
    hi=math.sqrt(t+RHO)
    while f(hi)<0: hi*=2
    return brentq(f,0.,hi,xtol=1e-11,rtol=1e-12)

def csvwrite(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def make_cases():
    rng=np.random.default_rng(2951026)
    cases=[]
    for i in range(24):
        g=[0.,.1,.3,.8][i%4]
        n=int(rng.integers(1,33))
        cases.append(dict(name=f'withheld_{i:02}',g=g,kind='discrete',
                          rates=(10**rng.uniform(-6,2,n)).tolist(),
                          weights=rng.dirichlet(np.full(n,.3)).tolist()))
    for i,(beta,scale) in enumerate([(.2,1e-4),(.7,.02),(1.,1.),(2.5,1e-5)]):
        cases.append(dict(name=f'continuous_gamma_{i}',g=[0.,.1,.3,.8][i],
                          kind='gamma',beta=beta,scale=scale))
    for rate in [1e-10,1e-8,1e-6]:
        cases.append(dict(name=f'adversarial_slow_{rate:g}',g=0.,kind='discrete',rates=[rate],weights=[1.]))
    cases.append(dict(name='permanent_spring',g=1.,kind='discrete',rates=[1.],weights=[1.]))
    (P/'WITHHELD_CASES.json').write_text(json.dumps(cases,indent=2)+'\n')
    return cases

def integrated_response(case,t):
    g=case['g']
    if case['kind']=='discrete':
        rates=np.array(case['rates']); weights=np.array(case['weights'])
        relax=np.sum(weights[:,None]*(-np.expm1(-rates[:,None]*t[None,:]))/rates[:,None],axis=0)
    else:
        beta,scale=case['beta'],case['scale']
        if beta==1.: relax=np.log1p(scale*t)/scale
        else: relax=np.expm1((1-beta)*np.log1p(scale*t))/(scale*(1-beta))
    return g*t+(1-g)*relax

def first_time(upper,threshold):
    hit=upper<threshold
    first=np.argmax(hit,axis=1)
    return np.where(np.any(hit,axis=1),TIMES[first],np.inf)

def main():
    # Freeze generated truth before any outcome or detector noise is inspected.
    cases=make_cases()
    rng=np.random.default_rng(2951027)
    h=np.diff(np.r_[0.,TIMES]); n=len(TIMES)
    b=np.array([boundary(t,ALPHA) for t in TIMES])
    restart_b=np.full((n,n),np.nan)
    starts=np.r_[0.,TIMES[:-1]]
    for i,t in enumerate(TIMES):
        for j in range(i+1): restart_b[i,j]=boundary(t-starts[j],ALPHA/n)
    # Exact fixed-grid simultaneous Gaussian correction, every possible tail window.
    q=float(ndtri(1-ALPHA/(n*(n+1)/2)))
    rows=[]; plotdata={}; worst_failure={k:0. for k in ['cumulative_CS','restart_CS','ordinary_all_windows']}
    for case in cases:
        integral=integrated_response(case,TIMES)
        dy=np.diff(np.r_[0.,integral])[None,:]+SIGMA*np.sqrt(h)[None,:]*rng.standard_normal((REPS,n))
        y=np.cumsum(dy,axis=1)
        cum=(y+SIGMA*b[None,:])/TIMES[None,:]
        restart=np.full_like(cum,np.inf); ordinary=np.full_like(cum,np.inf)
        prior=np.c_[np.zeros(REPS),y[:,:-1]]
        for i,t in enumerate(TIMES):
            dt=t-starts[:i+1]
            increments=y[:,i,None]-prior[:,:i+1]
            restart[:,i]=np.min((increments+SIGMA*restart_b[i,:i+1])/dt,axis=1)
            ordinary[:,i]=np.min(increments/dt+SIGMA*q/np.sqrt(dt),axis=1)
        methods={}
        for name,raw in [('cumulative_CS',cum),('restart_CS',restart),('ordinary_all_windows',ordinary)]:
            upper=np.minimum.accumulate(np.clip(raw,0.,1.),axis=1)
            methods[name]=upper
            failure_count=int(np.sum(np.any(upper<case['g']-1e-12,axis=1)))
            failure=failure_count/REPS
            ci_lower=float(beta_distribution.ppf(.025,failure_count,REPS-failure_count+1)) if failure_count else 0.
            ci_upper=float(beta_distribution.ppf(.975,failure_count+1,REPS-failure_count)) if failure_count<REPS else 1.
            worst_failure[name]=max(worst_failure[name],failure)
            stop=first_time(upper,.2); finite=stop[np.isfinite(stop)]
            rows.append(dict(case=case['name'],kind=case['kind'],equilibrium_modulus=case['g'],method=name,
                paths=REPS,simultaneous_miscoverage=failure,
                miscoverage_count=failure_count,miscoverage_MC_95_lower=ci_lower,miscoverage_MC_95_upper=ci_upper,
                miscoverage_MC_standard_error=math.sqrt(failure*(1-failure)/REPS),
                median_final_upper=float(np.median(upper[:,-1])),
                median_final_excess=float(np.median(upper[:,-1]-case['g'])),
                fraction_certified_below_0_2=float(len(finite)/REPS),
                median_time_among_completed=float(np.median(finite)) if len(finite) else None,
                median_time_including_noncompletion=float(np.median(stop)) if np.sum(np.isfinite(stop))>REPS/2 else None))
        plotdata[case['name']]=dict(y=y[0].tolist(),mean_integral=integral.tolist(),
                                   curves={k:v[0].tolist() for k,v in methods.items()},g=case['g'])
    csvwrite('WITHHELD_COMPARISON.csv',rows)
    # Quantitative sequential lower-bound witnesses: the rate changes with the horizon.
    witnesses=[]
    for t in [1.,10.,100.,1e3,1e4,1e5,1e6]:
        rate=.01*SIGMA*math.sqrt(3)/t**1.5
        info=t*quad(lambda s:(-math.expm1(-rate*t*s))**2,0.,1.,epsabs=1e-30)[0]/SIGMA**2
        from scipy.special import ndtr
        tv=2*float(ndtr(math.sqrt(info)/2))-1
        assert tv<.0041
        witnesses.append(dict(horizon=t,rate=rate,equilibrium_gap=1.,whitened_distance_squared=info,TV_upper_bound=tv))
    csvwrite('SEQUENTIAL_WITNESSES.csv',witnesses)
    # Verify that stage1 was not modified, without importing any stage1 code.
    preserved=True
    for line in (P/'STAGE1_SHA256.txt').read_text().splitlines():
        digest,name=line.split('  ',1)
        preserved &= hashlib.sha256((P.parent/'stage1'/name).read_bytes()).hexdigest()==digest
    assert preserved
    summary=dict(cases=len(cases),paths_per_case=REPS,total_paths=len(cases)*REPS,
        alpha=ALPHA,noise_density=SIGMA,observation_times=TIMES.tolist(),rho=RHO,
        scope='All observations synthetic; full-domain validity is proved, not inferred from coverage.',
        worst_case_empirical_miscoverage=worst_failure,stage1_unchanged=preserved,
        ordinary_window_quantile=q,design_seed=2951026,noise_seed=2951027)
    (P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    (P/'EXAMPLE_PATHS.json').write_text(json.dumps(plotdata,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(13,4),constrained_layout=True)
    for ax,name in zip(axes,['withheld_01','continuous_gamma_0','adversarial_slow_1e-10']):
        obj=plotdata[name]
        for method,curve in obj['curves'].items(): ax.semilogx(TIMES,curve,label=method.replace('_',' '))
        ax.axhline(obj['g'],color='black',ls=':',label='True equilibrium modulus')
        ax.axhline(.2,color='gray',ls='--',label='Engineering threshold')
        ax.set(title=name,xlabel='Time',ylabel='Upper bound on equilibrium modulus',ylim=(-.02,1.05))
    axes[0].legend(fontsize=7)
    fig.suptitle('Q95 stage 2: valid upper certificates, unknown slow modes — simulations only')
    fig.savefig(P/'STAGE2_FIGURE.png',dpi=180); fig.savefig(P/'STAGE2_FIGURE.pdf')
    print(json.dumps(summary,indent=2))
    for name in ['withheld_01','continuous_gamma_0','adversarial_slow_1e-10','permanent_spring']:
        print(name)
        for r in rows:
            if r['case']==name: print(r)

if __name__=='__main__': main()

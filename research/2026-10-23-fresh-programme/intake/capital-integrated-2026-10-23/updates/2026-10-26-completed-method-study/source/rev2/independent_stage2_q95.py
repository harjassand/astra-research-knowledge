"""Reconstruct Q95's confidence bounds from Howard et al. Proposition 6.

No candidate routines are imported. Formula checks use direct mixing-density
integration and saved path increments; coverage simulation is a diagnostic.
"""
from pathlib import Path
import csv
import json
import math

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ndtri

HERE=Path(__file__).resolve().parent
FROZEN=HERE.parents[1]/'review_material/Q95/stage2'


def boundary(t,alpha):
    v=1+t
    def log_level(x):
        phi=.5*(1+math.erf(x/math.sqrt(2)))
        return math.log(2)-.5*math.log(v)+.5*x*x+math.log(phi)+math.log(alpha)
    return math.sqrt(v)*brentq(log_level,0,10,xtol=1e-13)


def mixture_checks():
    tests=[]
    for t in (.001,1.,1e3,1e6):
        for alpha in (.05,.05/64):
            v=1+t;s=boundary(t,alpha);x=s/math.sqrt(v)
            # q is transformed to r=q*sqrt(t+rho) for stable integration.
            integral=math.sqrt(2/math.pi/v)*quad(lambda r:math.exp(r*x-r*r/2),
                                                 0,np.inf,epsabs=1e-9,epsrel=1e-12)[0]
            rel=abs(integral*alpha-1)
            assert rel<1e-10
            tests.append({'time':t,'alpha':alpha,'relative_mixture_equation_error':rel})
    return tests


def reconstruct_paths():
    summary=json.loads((FROZEN/'SUMMARY.json').read_text())
    times=np.array(summary['observation_times']);n=len(times)
    b=np.array([boundary(t,.05) for t in times])
    starts=np.r_[0,times[:-1]]
    restart=np.zeros((n,n))
    for i,t in enumerate(times):
        for j in range(i+1):restart[i,j]=boundary(t-starts[j],.05/n)
    q=float(ndtri(1-.05/(n*(n+1)/2)))
    def methods(y):
        cum=(y+.02*b)/times
        prior=np.r_[0,y[:-1]]
        r=np.empty(n);w=np.empty(n)
        for i,t in enumerate(times):
            dt=t-starts[:i+1];dy=y[i]-prior[:i+1]
            r[i]=np.min((dy+.02*restart[i,:i+1])/dt)
            w[i]=np.min(dy/dt+.02*q/np.sqrt(dt))
        return {key:np.minimum.accumulate(np.clip(vals,0,1))
                for key,vals in [('cumulative_CS',cum),('restart_CS',r),('ordinary_all_windows',w)]}
    saved=json.loads((FROZEN/'EXAMPLE_PATHS.json').read_text())
    largest=0
    for obj in saved.values():
        calc=methods(np.array(obj['y']))
        for key,val in calc.items():
            err=float(np.max(np.abs(val-np.array(obj['curves'][key]))))
            assert err<1e-10
            largest=max(largest,err)
    # Fresh Brownian paths under the least-favourable constant stress null G=g=1.
    rng=np.random.default_rng(95261026);trials=12000
    dt=np.diff(np.r_[0,times])
    y=times[None,:]+.02*np.cumsum(rng.standard_normal((trials,n))*np.sqrt(dt)[None,:],axis=1)
    cumulative=np.minimum.accumulate(np.clip((y+.02*b[None,:])/times[None,:],0,1),axis=1)
    miscoverage=float(np.mean(np.any(cumulative<1,axis=1)))
    assert miscoverage<.05
    return {'saved_paths_checked':len(saved),'methods_per_path':3,
            'maximum_bound_discrepancy':largest,'fresh_null_paths':trials,
            'fresh_cumulative_grid_miscoverage':miscoverage}


def comparisons_and_witnesses():
    with (FROZEN/'WITHHELD_COMPARISON.csv').open() as inp:rows=list(csv.DictReader(inp))
    grouped={}
    for row in rows:grouped.setdefault(row['case'],{})[row['method']]=row
    ordinary_wins=0;ties=0
    for obj in grouped.values():
        candidate=float(obj['cumulative_CS']['median_final_upper'])
        conventional=float(obj['ordinary_all_windows']['median_final_upper'])
        ordinary_wins+=int(conventional<candidate-1e-12)
        ties+=int(abs(conventional-candidate)<=1e-12)
    averages={method:float(np.mean([float(r['median_final_excess']) for r in rows if r['method']==method]))
              for method in ('cumulative_CS','restart_CS','ordinary_all_windows')}
    with (FROZEN/'SEQUENTIAL_WITNESSES.csv').open() as inp:witnesses=list(csv.DictReader(inp))
    tvs=[]
    for row in witnesses:
        t,rate=float(row['horizon']),float(row['rate'])
        d2=t*quad(lambda x:(-math.expm1(-rate*t*x))**2,0,1,epsabs=1e-30)[0]/.02**2
        tv=math.erf(math.sqrt(d2)/(2*math.sqrt(2)))
        assert abs(tv-float(row['TV_upper_bound']))<1e-12
        tvs.append(tv)
    slow=grouped['adversarial_slow_1e-10']
    assert all(float(r['fraction_certified_below_0_2'])==0 for r in slow.values())
    return {'comparison_cases':len(grouped),'ordinary_final_bound_wins':ordinary_wins,
            'ordinary_final_bound_ties':ties,'average_case_median_excess':averages,
            'sequential_witnesses_checked':len(tvs),'maximum_finite_record_TV':max(tvs),
            'rate_1e_minus10_certificates':0}


if __name__=='__main__':
    result={'half_normal_integration':mixture_checks(),'path_reconstruction':reconstruct_paths(),
            'comparison_and_sequential_witnesses':comparisons_and_witnesses()}
    (HERE/'independent_stage2_q95_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

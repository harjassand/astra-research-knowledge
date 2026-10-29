"""Execute the proposed full-law algorithm and equally informed controls.

All continuous distributions / ODEs here use floating arithmetic. Every
reported discrepancy is retained. This is not a universal numerical audit.
"""
import json
from pathlib import Path
from time import perf_counter
import numpy as np
from angular_dual import (Counts,declared_model,moment_sample,ratio_sample,
                          sample_velocity,wild_velocity,linear_factory)
from moment_reference import construct,moments


def estimate(values, reference):
    x = np.asarray(values,float)
    stderr = float(x.std(ddof=1)/np.sqrt(len(x)))
    return dict(mean=float(x.mean()),reference=float(reference),stderr=stderr,
                zscore=float((x.mean()-reference)/stderr) if stderr else None)


def sample_summary(samples,t,reference):
    covref = reference.covariance(t)
    values = {}
    for i in range(3):
        direction = np.eye(3)[i]
        _,fourth = moments(t,direction)
        values['v'+str(i)] = estimate(samples[:,i],0)
        values['v'+str(i)+'_squared'] = estimate(samples[:,i]**2,covref[i,i])
        values['v'+str(i)+'_fourth'] = estimate(samples[:,i]**4,fourth)
    values['v0v1'] = estimate(samples[:,0]*samples[:,1],covref[0,1])
    return values


def main():
    started=perf_counter()
    rng=np.random.default_rng(2026102905)
    model=declared_model()
    out=dict(scope='Floating implementation diagnostics, ideal theorem separate',
             seed=2026102905,model=dict(matrices=model.matrices.tolist(),
                    probabilities=model.probabilities.tolist(),bounds=model.bounds()),
             factory_controls=[],moment_controls=[],ratio_controls=[],
             full_law_runs=[],ordinary_wild_runs=[])
    # Imported factory independently checked with literal iid coins.
    for p in [.05,.2,.4]:
        count=Counts(); tick=perf_counter()
        values=[linear_factory(lambda: rng.random()<p,1-2*p,rng,count)
                for _ in range(20000)]
        out['factory_controls'].append(dict(p=p,estimate=estimate(values,2*p),
                                counts=count.json(),seconds=perf_counter()-tick))
    tick=perf_counter(); ref=construct()
    out['ordinary_moment_build_seconds']=perf_counter()-tick
    out['ordinary_moment_declared_dimension']=18
    for t in [0.,1.,3.,30.,1e6]:
        for k in [1,2,4]:
            # q4's reference is available at t0 and equilibrium only.
            if k==4 and t not in [0.,1e6]: continue
            count=Counts(); tick=perf_counter()
            values=[moment_sample(k,np.array([1.,0,0]),t,model.draw_e,rng,count)
                    for _ in range(16000)]
            if t==0:
                target=sum(p*e[0,0]**k for p,e in zip(model.probabilities,model.es))
            elif t==1e6:
                target=((model.mu-model.c)/model.h)**k
            else:
                m2,m4=moments(t,[1,0,0])
                target=((m2-model.c)/model.h if k==1 else
                        (m4/3-2*model.c*m2+model.c**2)/model.h**2)
            out['moment_controls'].append(dict(t=t,k=k,estimate=estimate(values,target),
                            counts=count.json(),seconds=perf_counter()-tick))
    # The invalid radial transfer has an exact, macroscopically wrong mean.
    vals=[moment_sample(1,np.array([1.,0,0]),3.,model.draw_e,rng,
                        discard_rotations=True) for _ in range(16000)]
    target=(model.covariance(3)[0,0]-model.c)/model.h
    out['negative_discard_rotations']=dict(estimate=estimate(vals,target),
                                  invalid_mean=-.6,scope='intentionally wrong algorithm')
    for v in [np.array([0.,0,0]),np.array([1.,.5,-.25])]:
        count=Counts(); tick=perf_counter()
        vals=[ratio_sample(v,0,model,rng,count) for _ in range(60000)]
        f=sum(p*np.exp(-v@np.linalg.solve(s,v)/2)/np.sqrt(np.linalg.det(s))
              for p,s in zip(model.probabilities,model.matrices))/(2*np.pi)**1.5
        q=np.exp(-v@v/(2*model.g))/(2*np.pi*model.g)**1.5
        out['ratio_controls'].append(dict(v=v.tolist(),estimate=estimate(vals,f/q),
                              counts=count.json(),seconds=perf_counter()-tick))
    for t in [0.,1.,3.,30.,1e6]:
        count=Counts(); tick=perf_counter()
        samples=np.array([sample_velocity(t,model,rng,count) for _ in range(6000)])
        seconds=perf_counter()-tick
        out['full_law_runs'].append(dict(t=t,n=len(samples),seconds=seconds,
                          estimates=sample_summary(samples,t,model),counts=count.json()))
    for t in [0.,1.,3.]:
        tick=perf_counter(); draws=[wild_velocity(t,model,rng) for _ in range(6000)]
        seconds=perf_counter()-tick
        samples=np.array([x[0] for x in draws]); leaves=sum(x[1] for x in draws)
        out['ordinary_wild_runs'].append(dict(t=t,n=len(draws),seconds=seconds,
                         estimates=sample_summary(samples,t,model),leaves=leaves,
                         expected_leaves=len(draws)*float(np.exp(t))))
    # Warm marginal moment work is measured separately; same information,
    # weaker output (moments), and therefore not a full-sampler speed claim.
    tick=perf_counter()
    for t in np.linspace(0,30,200): moments(float(t),[1.,0,0])
    out['ordinary_200_moment_queries_seconds']=perf_counter()-tick
    out['total_seconds']=perf_counter()-started
    path=Path(__file__).parent/'outputs'/'ACQUISITION.json'
    path.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(output=str(path),seconds=out['total_seconds'],
                   sampler_seconds=[(x['t'],x['seconds']) for x in out['full_law_runs']],
                   wild_seconds=[(x['t'],x['seconds']) for x in out['ordinary_wild_runs']]),indent=2))


if __name__=='__main__': main()

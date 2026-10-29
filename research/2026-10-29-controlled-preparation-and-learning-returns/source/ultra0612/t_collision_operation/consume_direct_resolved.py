"""Fixed controls and same-law ordinary comparator, no rerun-until-pass."""
import json
from pathlib import Path
from time import perf_counter
import sympy as sp
import numpy as np
from direct_resolved import (BoundedSymmetricSource,Model,Work,
                              complex_moment,ratio,sample_velocity)
from angular_dual import wild_velocity
from moment_reference import resolved_moments,construct_resolved
from run_acquisition import estimate


def main():
    start=perf_counter();rng=np.random.default_rng(2026102907)
    source=BoundedSymmetricSource(np.eye(3),np.full(3,1/3),1.)
    model=Model(source,2.)
    z=np.array([.6,.48+.64j,0],complex)
    exact_z=sp.Matrix([sp.Rational(3,5),sp.Rational(12,25)+sp.I*sp.Rational(16,25),0])
    assert sp.expand((sp.conjugate(exact_z).T*exact_z)[0])==1
    dq=lambda q:sp.factorial(2*q)/(2**q*sp.factorial(q))
    for q in range(1,17):
        for j in range(q+1):
            assert sp.binomial(2*q,2*j)*dq(j)*dq(q-j)/dq(q)==sp.binomial(q,j)
    exact_terminal=[]
    for q in range(1,9):
        f=sp.expand(sum(a**(2*q) for a in exact_z)/(3*dq(q)))
        assert sp.simplify(f*sp.conjugate(f))<=1
        exact_terminal.append(dict(q=q,real=str(sp.re(f)),imag=str(sp.im(f))))
    assert sp.Rational(145,9)-3*sp.Rational(7,3)**2==-sp.Rational(2,9)
    out=dict(scope='Direct INITIAL VELOCITY operation; floating runs, exact theorem separate',
      seed=2026102907,bounds=model.bounds(),exact_raw_gain_identities=152,
      exact_terminal_values=exact_terminal,declared_Gaussian_variance=2,
      initial_directional_variance='7/3',initial_directional_fourth='145/9',
      initial_fourth_cumulant='-2/9',complex_moment_controls=[],
      density_controls=[],full_law_runs=[],ordinary_wild_runs=[])
    for t in [0.,3.]:
        for q in [1,2]:
            count=Work();tick=perf_counter()
            values=np.array([complex_moment(q,z,t,source,rng,count) for _ in range(20000)])
            second,fourth=resolved_moments(t,z,variance=0)
            target=second if q==1 else fourth/3
            out['complex_moment_controls'].append(dict(t=t,q=q,
                    real=estimate(values.real,target.real),imag=estimate(values.imag,target.imag),
                    seconds=perf_counter()-tick,counts=count.json()))
    v=np.array([1.,.5,-.25]);count=Work();tick=perf_counter()
    values=[ratio(v,0.,model,rng,count) for _ in range(40000)]
    target_density=sum((np.exp(-np.sum((v-u)**2)/(2*model.s))
                        +np.exp(-np.sum((v+u)**2)/(2*model.s)))
                       for u in np.eye(3))/(6*(2*np.pi*model.s)**1.5)
    proposal=np.exp(-v@v/(2*model.g))/(2*np.pi*model.g)**1.5
    out['density_controls'].append(dict(t=0,v=v.tolist(),
          estimate=estimate(values,target_density/proposal),seconds=perf_counter()-tick,
          counts=count.json()))
    direction=np.ones(3)/np.sqrt(3)
    def summary(values,t):
        projection=values@direction;m2,m4=resolved_moments(t,direction,variance=2)
        return dict(second=estimate(projection**2,m2),fourth=estimate(projection**4,m4),
                    covariance_diagonal=[estimate(values[:,i]**2,model.covariance(t)[i,i])
                                         for i in range(3)])
    for t in [0.,3.,1e6]:
        count=Work();tick=perf_counter()
        values=np.array([sample_velocity(t,model,rng,count) for _ in range(1000)])
        out['full_law_runs'].append(dict(t=t,n=len(values),seconds=perf_counter()-tick,
                         estimates=summary(values,t),counts=count.json()))
    for t in [0.,3.]:
        tick=perf_counter();draws=[wild_velocity(t,model,rng) for _ in range(1000)]
        values=np.array([x[0] for x in draws])
        out['ordinary_wild_runs'].append(dict(t=t,n=len(draws),seconds=perf_counter()-tick,
                         estimates=summary(values,t),leaves=sum(x[1] for x in draws)))
    tick=perf_counter()
    for t in np.linspace(0,30,200):resolved_moments(float(t),direction,variance=2)
    out['ordinary_200_moment_queries_seconds']=perf_counter()-tick
    out['seconds']=perf_counter()-start
    path=Path(__file__).parent/'outputs'/'DIRECT_RESOLVED.json'
    path.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(output=str(path),seconds=out['seconds'],
          moments=[(r['t'],r['q'],r['real']['zscore'],r['imag']['zscore'])
                   for r in out['complex_moment_controls']],
          density_z=out['density_controls'][0]['estimate']['zscore'],
          full=[(r['t'],r['seconds']) for r in out['full_law_runs']],
          ordinary=[(r['t'],r['seconds']) for r in out['ordinary_wild_runs']]),indent=2))


if __name__=='__main__':main()

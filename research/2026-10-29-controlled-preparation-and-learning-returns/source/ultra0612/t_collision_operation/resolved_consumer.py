"""Exact changed-input discriminator plus actual non-mixture full-law run."""
import json
from pathlib import Path
from time import perf_counter
import math
import sympy as s
import numpy as np
from angular_dual import ResolvedVelocityModel,Counts,sample_velocity,wild_velocity
from moment_reference import resolved_moments
from run_acquisition import estimate


def main():
    started=perf_counter();u=s.Symbol('u');checks=[]
    d=lambda q:s.factorial(2*q)/(2**q*s.factorial(q))
    for q in range(1,17):
        for j in range(q+1):
            coefficient=(s.binomial(2*q,2*j)*s.integrate(u**j*(1-u)**(q-j),(u,0,1))
                         *d(j)*d(q-j)/d(q))
            assert coefficient==s.Rational(1,q+1)
            checks.append((q,j,str(coefficient)))
    variance=s.Rational(25,3);fourth=s.Rational(1873,9)
    assert fourth-3*variance**2==-s.Rational(2,9)
    rng=np.random.default_rng(2026102906)
    model=ResolvedVelocityModel(np.eye(3),np.full(3,1/3),1.,8.)
    n=np.ones(3)/math.sqrt(3)
    out=dict(scope='Exact finite identities plus FLOATING full-law implementation diagnostics',
      exact_beta_checks=len(checks),initial_diagonal_variance=str(variance),
      initial_diagonal_fourth=str(fourth),initial_fourth_cumulant='-2/9',
      outside_centered_gaussian_covariance_mixtures=True,bounds=model.bounds(),
      full_law_runs=[],ordinary_wild_runs=[])
    for t in [0.,3.,1e6]:
        count=Counts();tick=perf_counter()
        samples=np.array([sample_velocity(t,model,rng,count) for _ in range(4000)])
        seconds=perf_counter()-tick
        projected=samples@n;m2,m4=resolved_moments(t,n)
        out['full_law_runs'].append(dict(t=t,n=len(samples),seconds=seconds,
                projected_second=estimate(projected**2,m2),
                projected_fourth=estimate(projected**4,m4),counts=count.json()))
    for t in [0.,3.]:
        tick=perf_counter();draws=[wild_velocity(t,model,rng) for _ in range(4000)]
        seconds=perf_counter()-tick
        projected=np.array([x[0]@n for x in draws]);m2,m4=resolved_moments(t,n)
        out['ordinary_wild_runs'].append(dict(t=t,n=len(draws),seconds=seconds,
                projected_second=estimate(projected**2,m2),
                projected_fourth=estimate(projected**4,m4),
                leaves=sum(x[1] for x in draws)))
    out['seconds']=perf_counter()-started
    path=Path(__file__).parent/'outputs'/'RESOLVED_ACQUISITION.json'
    path.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()

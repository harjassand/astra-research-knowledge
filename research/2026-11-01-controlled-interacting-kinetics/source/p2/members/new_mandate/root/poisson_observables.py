"""Earn a second service: integrated equilibrium energy autocovariance.
This is zero-frequency energy noise for a bath-coupled model, not conductivity.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json,time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from gaussian_kinetics import model,dense_generator


def energy_reference(m):
    weights=2*m['J']
    B=m['U'].T@(weights[:,None]*m['V'])
    F=B-B.T
    i,j=np.triu_indices(m['n'],1)
    square=F[i,j]**2
    return {'variance':float(square.sum()),
            'integrated_covariance':float(np.sum(square/(m['eps'][i]+m['eps'][j])))}


def run():
    rng=np.random.default_rng(55261101);checks=[]
    for n in [4,6,8]:
        m=model(rng.uniform(-.4,1.0,n),rng.uniform(.2,1.4,n))
        ref=energy_reference(m)
        states,Q,K,p=dense_generator(m)
        obs=np.array([sum(2*m['J'][i]*((s>>i)&1) for i in range(n)) for s in states])
        f=(obs-p@obs)*np.sqrt(p)
        ev,O=eigh(K);G=(O[:,1:]/ev[1:])@O[:,1:].T
        exact=float(f@G@f)
        _,Qe,Ke,pe=dense_generator(m,.7)
        eve,Oe=eigh(Ke);Ge=(Oe[:,1:]/eve[1:])@Oe[:,1:].T
        actual=float(f@Ge@f);c=1.35;rho=.7/2.7
        R=G/c;E=Ke-c*K;series=0.;records=[]
        for order in range(5):
            series+=(-1)**order*(f@R@np.linalg.matrix_power(E@R,order)@f)
            records.append({'order':order,'relative_error':abs(series/actual-1),'bound':rho**(order+1)})
        checks.append({'n':n,'variance_absolute_error':abs(ref['variance']-float(f@f)),
                       'reference_relative_error':abs(ref['integrated_covariance']/exact-1),
                       'reference':ref,'nonintegrable_integrated_covariance':actual,
                       'nonintegrable_series':records})
    large=[]
    for n in [64,128,256]:
        t=time.perf_counter()
        J=.4+.25*np.cos(np.arange(n)*np.sqrt(2))
        nu=.3+.7*(np.sin(np.arange(n)*np.sqrt(3))**2)
        m=model(J,nu);r=energy_reference(m)
        large.append({'n':n,'reference':r,'seconds':time.perf_counter()-t})
    out={'scope':'Second observable verifies source generalization; exact Gaussian reference, nonintegrable small-state checks, no transport-coefficient claim.',
         'dense_checks':checks,'large_disordered_reference':large}
    Path(__file__).with_name('poisson_observables_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()

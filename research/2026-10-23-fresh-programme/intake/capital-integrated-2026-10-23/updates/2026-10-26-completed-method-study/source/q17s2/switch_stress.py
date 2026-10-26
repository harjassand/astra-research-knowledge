"""Contrast frontier and ordinary self-cooling thermal-switch comparison.

All output is local idealized-model computation, not physical measurement.
Smooth curves are model curves, not fits to a cited switch's measurements.
"""
from pathlib import Path
import json
import time
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad, solve_ivp
from scipy.special import expit

OUT=Path(__file__).resolve().parent


def twice_atanh_minus(v):
    if v<.1:
        return 2*sum(v**j/j for j in range(3,51,2))
    return 2*(np.arctanh(v)-v)


def minuslog_minus(x):
    if x<.1:
        return sum(x**j/j for j in range(2,51))
    return -np.log1p(-x)-x


def frontier(k):
    rhs=minuslog_minus(1/k)
    v=brentq(lambda u:twice_atanh_minus(u)-rhs,1e-14,1-1e-13,xtol=1e-15)
    d=2*v-1/k
    eta=np.exp(-d)
    return v,d,eta


def step_moments(k,d):
    eta=np.exp(-d)
    m=-np.expm1(-d)+eta/k
    m2=2*(-np.expm1(-d)-eta*d+eta*(d/k+1/k**2))
    return float(m),float(m2-m*m),float(m2/(m*m)-1)


def direct_density_quadrature(k,d):
    # Conditional tail is d+Exp(k), with tail weight exp(-d).
    eta=np.exp(-d)
    m=quad(lambda t:t*np.exp(-t),0,d,epsabs=1e-13)[0]
    m+=eta*quad(lambda s:(d+s/k)*np.exp(-s),0,np.inf,epsabs=1e-13)[0]
    m2=quad(lambda t:t*t*np.exp(-t),0,d,epsabs=1e-13)[0]
    m2+=eta*quad(lambda s:(d+s/k)**2*np.exp(-s),0,np.inf,epsabs=1e-13)[0]
    return float(m),float(m2/(m*m)-1)


def smooth_moments(k,width,theta):
    def ode(z,y):
        temp=np.exp(-z)
        g=1+(k-1)*expit((theta-temp)/width)
        a=1/g
        weight=np.exp(-z)
        return [a,a*weight,2*y[0]*a*weight]
    sol=solve_ivp(ode,(0,40),[0.,0.,0.],method='DOP853',
                  rtol=2e-10,atol=2e-13,max_step=.3)
    assert sol.success
    m=sol.y[1,-1];m2=sol.y[2,-1]
    return float(m),float(m2/(m*m)-1)


def optimize_smooth(k,width):
    grid=np.linspace(.001,.999,31)
    values=[smooth_moments(k,width,x)[1] for x in grid]
    candidates=[]
    for j in np.argsort(values)[:4]:
        lo=grid[max(0,j-1)];hi=grid[min(len(grid)-1,j+1)]
        res=minimize_scalar(lambda theta:smooth_moments(k,width,theta)[1],
                            bounds=(lo,hi),method='bounded',
                            options={'xatol':2e-9,'maxiter':100})
        candidates.append((float(res.fun),float(res.x),bool(res.success)))
    value,theta,success=min(candidates)
    m,cv=smooth_moments(k,width,theta)
    return dict(k=k,width_fraction=width,theta_fraction=theta,
                mean=m,cv2=cv,cv=float(np.sqrt(cv)),converged=success,
                grid_points=len(grid),local_refinements=len(candidates),
                ideal_lower_cv2=frontier(k)[0])


if __name__=='__main__':
    start=time.perf_counter()
    exact=[]
    for k in [3.,7.,25.,111.,1000.,10000.]:
        v,d,eta=frontier(k)
        ordinary=minimize_scalar(lambda delay:step_moments(k,delay)[2],
                                 bounds=(1e-7,5.),method='bounded',
                                 options={'xatol':1e-12,'maxiter':200})
        qm,qcv=direct_density_quadrature(k,d)
        exact.append(dict(k=k,analytic_cv2=float(v),cv=float(np.sqrt(v)),
                          delay=d,retained_fraction_at_switch=eta,
                          analytic_moments=step_moments(k,d),
                          independent_quadrature_cv2=qcv,
                          ordinary_best_cv2=float(ordinary.fun),
                          ordinary_delay=float(ordinary.x),
                          ordinary_success=bool(ordinary.success),
                          relative_threshold_sensitivity=1/(eta*d)))
    smooth=[optimize_smooth(k,w) for k in [100.,1000.] for w in [.0001,.001,.01,.05]]
    result=dict(scope='Ideal memoryless bounded G(T), illustrative parameters only; no experimentally validated integrated device.',
                threshold_frontier=exact,smooth_retuned_comparators=smooth,
                wall_seconds=time.perf_counter()-start)
    (OUT/'switch_stress_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))

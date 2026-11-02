"""Numerical diagnostics only; PROOF.md carries the analytic proof.
Run with Python + NumPy + SciPy. No target samples are claimed as a new solver.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import expit

R=1/8

def eta(z):
    return math.exp(-z*z/(1-z*z)) if abs(z)<1 else 0.

I,Ierr=quad(eta,-1,1,epsabs=1e-13,epsrel=1e-13)

def oracle(x,b):
    x=np.asarray(x,dtype=float); b=np.asarray(b,dtype=int)
    d=len(x); z=(x-(.25+.5*b))/R
    if np.any(np.abs(z)>=1):
        return 0.,np.zeros(d),np.zeros((d,d))
    t=1-z*z
    a=np.sum(z*z/t); ell=d*math.log(1/(R*I))
    p=expit(ell-a)
    g=2*z/t**2/R
    h=(2/t**2+8*z*z/t**3)/R**2
    return -np.logaddexp(0.,ell-a),p*g,p*np.diag(h)-p*(1-p)*np.outer(g,g)

rng=np.random.default_rng(20261102)
results={'diagnostic_only':True,'I':I,'quadrature_error_reported':Ierr,
         'depth_per_dimension':math.log(1/(R*I)),'dimensions':[]}
# One-dimensional product integration gives exactly Z=2 analytically.
assert abs(quad(lambda x: 1+eta((x-.25)/R)/(R*I),0,1,epsabs=1e-11)[0]-2)<1e-9
# Every possible candidate center has at most one non-flat response.
for d in range(1,9):
    N=2**d; labels=np.array([[(k>>i)&1 for i in range(d)] for k in range(N)])
    b=labels[N//3]
    active=sum(oracle(.25+.5*c,b)[0]<0 for c in labels)
    assert active==1
    ell=d*math.log(1/(R*I))
    gb=8*math.sqrt(d)/R*(1+ell)**2
    hb=216/R**2*(1+ell)**3+1024*d/R**2*(1+ell)**4
    gmax=hmax=0.
    for _ in range(200):
        x=.25+.5*b+R*rng.uniform(-.999,.999,d)
        u,g,h=oracle(x,b)
        gmax=max(gmax,float(np.linalg.norm(g)))
        hmax=max(hmax,float(np.linalg.norm(h,2)))
        assert -math.log(2)-ell-1e-12 <=u<=0
        assert np.linalg.norm(g)<=gb and np.linalg.norm(h,2)<=hb
    # Finite differences at a nonsingular interior point.
    x=.25+.5*b+R*np.full(d,.32)
    _,g,h=oracle(x,b); step=1e-6
    gd=np.array([(oracle(x+step*np.eye(d)[i],b)[0]-oracle(x-step*np.eye(d)[i],b)[0])/(2*step) for i in range(d)])
    hd=np.column_stack([(oracle(x+step*np.eye(d)[i],b)[1]-oracle(x-step*np.eye(d)[i],b)[1])/(2*step) for i in range(d)])
    assert np.max(np.abs(g-gd))<1e-5
    assert np.max(np.abs(h-hd))<1e-3
    q=N//4; hit_fraction=sum(k<q for k in range(N))/N
    assert hit_fraction==q/N
    results['dimensions'].append({'d':d,'N':N,'unique_active_center':int(active),
      'query_budget':q,'exact_discovery_fraction':hit_fraction,
      'gradient_max_sampled':gmax,'hessian_max_sampled':hmax,
      'gradient_fd_error':float(np.max(np.abs(g-gd))),
      'hessian_fd_error':float(np.max(np.abs(h-hd))),
      'sampling_query_lower_bound_epsilon_0_1':N*((1+4**(-d))/2-.1)-1})
# Bernoulli coarse graining, equality when regionwise likelihood is constant.
for a,p in [(.5,.01),(.7,.2),(.2,.8),(.5,2**(-20))]:
    lhs=a*a/p+(1-a)**2/(1-p)-1
    rhs=(a-p)**2/(p*(1-p))
    assert math.isclose(lhs,rhs,rel_tol=1e-12,abs_tol=1e-12)
results['all_checks_passed']=True
out=Path(__file__).with_name('checks.json');out.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'dimensions':len(results['dimensions']),'I':I,'file':str(out)}))

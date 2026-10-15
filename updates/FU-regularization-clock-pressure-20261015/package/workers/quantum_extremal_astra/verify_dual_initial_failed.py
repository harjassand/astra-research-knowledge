"""Finite diagnostics for GLOBAL_OPTIMALITY_PROOF.md; not a proof certificate."""
import functools, hashlib, json, math, pathlib
from datetime import datetime, timezone
import numpy as np
from scipy.integrate import quad
from scipy.special import exp1

GAMMA=0.5772156649015328606

def invd(t):
    if t<1e-5:
        return math.exp(t-t*t/2+2*t**3/9-t**4/12)
    return math.exp((GAMMA+math.log(2*t)+exp1(2*t))/2)

def quadinf(fn):
    return quad(fn,0,np.inf,epsabs=3e-11,epsrel=3e-11,limit=250)[0]

K=.5*quadinf(lambda t:((-math.expm1(-t))/t)**2*invd(t) if t else 1.)
c=1/(4*K+2)
kappa=23/3-2*c/3

@functools.lru_cache(maxsize=None)
def ell(r):
    return .5*quadinf(lambda t:math.exp(-r*t)*invd(t))

@functools.lru_cache(maxsize=None)
def J(r):
    if r==0:return 0.
    return .5*quadinf(lambda t:math.exp(-(2-r)*t)*(-math.expm1(-2*r*t))*invd(t)/t if t else 2*r)

@functools.lru_cache(maxsize=None)
def C(r):
    # C=F+4cr²ell. Only smooth kernel arguments >=2 are used.
    return (1+c/2)*r*r-r**3+r**4/4+c*quad(lambda u:J(u)+2*u*ell(2+u),0,r,epsabs=2e-11,epsrel=2e-11)[0]

@functools.lru_cache(maxsize=None)
def G(r):
    # G=F-2r f(1-r). Only smooth kernel arguments >=1 are used.
    return -(3+1.5*c)*r*r+5*r**3-7*r**4/4-c*quad(lambda u:u*J(u)+2*u*u*ell(2-u),0,r,epsabs=2e-11,epsrel=2e-11)[0]

def P(r):return .5*r*r+2*r+2/3+c/3+4*c*ell(r)/3

def U(r):
    if r==0:return 1+c/2+2*c*ell(2)/3
    if r>=1:return P(r)
    return .5*r*r+2*r+2/3+c/3+C(r)/(3*r*r)

def V(r):
    if r==0:return U(0)
    if r==1:return 0.
    return -G(r)/(3*r*r)

def qfinite(fn,a,b):
    if b<=a:return 0.
    points=[x for x in [1.] if a<x<b]
    return quad(fn,a,b,points=points,epsabs=1e-9,epsrel=1e-9,limit=120)[0]

checks=[]
for s in [.01,.1,.25,.5,.9,.99,1.01,1.3,1.7,1.99,2.01,3.,5.,10.]:
    coeff=(2*(s-1)*U(s-1) if s>1 else 0)-qfinite(U,abs(s-1),s+1)
    if s<2: coeff+=qfinite(V,abs(s-1),1.)
    if s<1: coeff-=2*(1-s)*V(1-s)
    target=s**3-kappa*s
    checks.append({'s':s,'dual_coefficient':coeff,'target':target,'residual':coeff-target})

rgrid=np.r_[0.,np.linspace(.001,.999,101),1.]
mult=[{'r':float(r),'U':U(float(r)),'V':V(float(r))} for r in rgrid]
M=-.5*quadinf(lambda t:-t*math.exp(-t)*invd(t))
ldcheck=[]
for r in [.1,.5,1.,2.,5.,10.]:
    val=2*r*ell(r)-qfinite(ell,r,r+2)
    deriv=-.5*quadinf(lambda t:t*math.exp(-r*t)*invd(t))
    ldcheck.append({'r':r,'integral_residual':val-1,'differential_residual':2*r*deriv+3*ell(r)-ell(r+2)})

out={'status':'finite floating point diagnostics only','timestamp_utc':datetime.now(timezone.utc).isoformat(),'K':K,'c':c,'variance':kappa/3,'c_bound':{'value':c,'upper':1/8},'minus_ell_prime_one':M,'ell_prime_bound':16/5,'strict_monotonicity_margin_lower_bound':1-2.5*c*M,'F1_residual':C(1.)-4*c*ell(1.),'G1_residual':G(1.),'min_U_grid':min(m['U'] for m in mult),'min_V_interior_grid':min(m['V'] for m in mult if 0<m['r']<1),'max_adjoint_residual':max(abs(x['residual']) for x in checks),'adjoint_checks':checks,'kernel_checks':ldcheck,'multipliers':mult}
pathlib.Path('dual_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['multipliers','adjoint_checks','kernel_checks']},indent=2))
for fn in ['GLOBAL_OPTIMALITY_PROOF.md','extremal_numerics.py','extremal_numerics.json','verify_dual.py','dual_checks.json']:
    p=pathlib.Path(fn)
    print(fn,hashlib.sha256(p.read_bytes()).hexdigest())

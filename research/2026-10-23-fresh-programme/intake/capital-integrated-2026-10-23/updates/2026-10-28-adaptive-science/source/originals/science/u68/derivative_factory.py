"""Monte Carlo diagnostics for the exact value-only DK action.

Analytical identities and bounds live in RESOLVENT_DERIVATIVE_FACTORY.md.
These finite diagnostics test implementation; they do not certify TV.
"""
import json
import math
from pathlib import Path
import numpy as np


def factory(g, y, v, w, count, rng, b=1.0, antithetic=False):
    d = len(y)
    u = w/np.linalg.norm(w)
    mass = 1-math.sqrt(1-b*b)
    s = 1-mass*rng.random(count)
    rho = np.sqrt(1-s*s)
    z = rng.normal(size=(count,d))
    zp = z-(z@u)[:,None]*u
    r = np.linalg.norm(rng.normal(size=(count,3)),axis=1)
    t = rng.uniform(-1,1,size=count)
    def at(zperp, pair_t):
        c = rho[:,None]*y+s[:,None]*zperp
        plus = g(c+(s*r)[:,None]*u)
        minus = g(c-(s*r)[:,None]*u)
        mid = g(c+(s*r*t)[:,None]*u)
        D = (plus-minus)/(2*s*r)[:,None]
        if pair_t:
            mid2 = g(c-(s*r*t)[:,None]*u)
            Q = (plus+minus-mid-mid2)/(2*s)[:,None]
        else:
            Q = (plus+minus-2*mid)/(2*s)[:,None]
        return mass*np.linalg.norm(w)*(
            (zperp@v)[:,None]*D+float(v@u)*Q)
    raw = at(zp,False)
    if antithetic:
        even = .5*(at(zp,True)+at(-zp,True))
        return raw,even
    return raw


def reference(y,v,w,direction,k,b,alpha):
    # Integrate after S=sqrt(1-rho²), avoiding a high-frequency endpoint layer.
    pts, weights = np.polynomial.legendre.leggauss(300)
    low = math.sqrt(1-b*b)
    s = low+(1-low)*(pts+1)/2
    rho = np.sqrt(1-s*s)
    integral = (1-low)/2*np.sum(weights*s*
        np.sin(k*rho*float(direction@y))*np.exp(-.5*k*k*s*s))
    return (-alpha*k*float(direction@v)*float(direction@w)*integral)*direction


def experiment(d,k,b,kind,n=240000):
    rng = np.random.default_rng(10000+d*100+k+int(b*10))
    direction = rng.normal(size=d)
    direction /= np.linalg.norm(direction)
    y = .7*direction
    if d==1:
        v=w=direction.copy()
    else:
        q = rng.normal(size=d)
        q -= float(q@direction)*direction
        q /= np.linalg.norm(q)
        v=(direction+q)/math.sqrt(2)
        w=(direction-q)/math.sqrt(2)
    alpha=.7
    if kind=='affine':
        # Symmetric operator, globally 0.7-Lipschitz; a C1,1 potential exists.
        def g(x): return .7*x+np.arange(d)*.01
        truth=np.zeros(d)
        L=.7
    else:
        def g(x):
            return alpha*np.sin(k*(x@direction))[:,None]*direction/k
        truth=reference(y,v,w,direction,k,b,alpha)
        L=alpha
    sums=np.zeros((2,d)); sumsq=np.zeros((2,d)); normsq=np.zeros(2)
    max_affine_even=0.0
    for start in range(0,n,8000):
        raw,even=factory(g,y,v,w,min(8000,n-start),rng,b,True)
        for j,x in enumerate((raw,even)):
            sums[j]+=np.sum(x,axis=0)
            sumsq[j]+=np.sum(x*x,axis=0)
            normsq[j]+=np.sum(x*x)
        max_affine_even=max(max_affine_even,float(np.max(np.abs(even))))
    means=sums/n
    var=np.maximum(0,sumsq/n-means*means)
    # The scalar projection onto truth direction is the nonzero signal here.
    # All outputs for a rank-one source remain in that direction.
    records=[]
    for j,name in enumerate(('three_query','eight_query_antithetic')):
        se_norm=math.sqrt(float(np.sum(var[j]))/n)
        records.append(dict(estimator=name,mean_norm=float(np.linalg.norm(means[j])),
            mean_error_norm=float(np.linalg.norm(means[j]-truth)),
            monte_carlo_se_norm=se_norm,
            l2_output=math.sqrt(float(normsq[j]/n)),
            proved_l2_upper=2*(1-math.sqrt(1-b*b))*L*
                float(np.linalg.norm(v))*float(np.linalg.norm(w))))
    return dict(d=d,k=k,b=b,kind=kind,draws=n,
                truth=truth.tolist(),records=records,
                antithetic_max_abs=max_affine_even)


def main():
    cases=[(1,k,1.,'nonlinear') for k in (1,4,16,64)]
    cases += [(8,3,1.,'nonlinear'),(64,3,1.,'nonlinear'),
              (8,3,.8,'nonlinear'),(1,1,1.,'affine'),
              (8,1,1.,'affine'),(64,1,1.,'affine')]
    results=[]
    for case in cases:
        r=experiment(*case)
        results.append(r)
        print(json.dumps(r),flush=True)
    path=Path(__file__).with_name('derivative_factory_results.json')
    path.write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__': main()

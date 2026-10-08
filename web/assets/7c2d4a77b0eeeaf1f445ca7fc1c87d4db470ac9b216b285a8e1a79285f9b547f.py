"""Independent numerical check of an extension of the heat witness."""
import numpy as np
import json
from numpy.polynomial.legendre import leggauss
xr,wr=leggauss(160); r=4*(xr+1); wr=4*wr
u,wu=leggauss(100)
z=r[:,None]*u[None,:]
perp=r[:,None]**2-z*z
p=8*np.sqrt(2/np.pi)*r*r*np.exp(-2*r*r)
rng=np.random.default_rng(48394)

def setup(c):
    qr=r[:,None]/c
    ang=qr*np.exp(-qr*(u[None,:]+1))/(-np.expm1(-2*qr))
    return wr[:,None]*p[:,None]*wu[None,:]*ang

def gap(tp,tz,mu,P):
    F=np.sum(P*np.exp(-tp*perp-tz*(z-mu)**2))
    if tz>=tp:B=1/(1+tp/2)
    else:B=1/np.sqrt((1+tp/2)*(1+tz/2))
    return float(F-B)

def opt(c):
    P=setup(c)
    best=(-1,0,0,0)
    starts=[(10**rng.uniform(-3,.6),10**rng.uniform(-3,.6),rng.uniform(-1,0)) for _ in range(400)]
    starts+=[(.04,.04,-.5),(.3,.3,-.52),(1,1,-.6),(.1,.02,-.5),(.02,.1,-.5)]
    vals=sorted([(gap(tp,tz,mu,P),tp,tz,mu) for tp,tz,mu in starts],reverse=True)[:7]
    for v,tp,tz,mu in vals:
        ds=np.array([.3*tp,.3*tz,.06])
        params=np.array([tp,tz,mu])
        for _ in range(85):
            improved=False
            for k in range(3):
                choices=[]
                for sign in [-1,1]:
                    trial=params.copy();trial[k]+=sign*ds[k]
                    trial[:2]=np.maximum(trial[:2],1e-8)
                    choices.append((gap(*trial,P),trial))
                vv,trial=max(choices,key=lambda x:x[0])
                if vv>v+1e-13:
                    v=vv;params=trial;improved=True
            if not improved:ds*=.73
        if v>best[0]:best=(v,*params)
    return {'c':c,'gap':best[0],'t_perp':best[1],'t_z':best[2],'mu':best[3],'normalization':float(P.sum())}
out=[opt(c) for c in [.3,.32,.3281137,.33,.35,.4,.5,1.0]]
print(json.dumps(out,indent=2))
with open('work/agents/thermal_blind/results/anisotropic_diagnostics.json','w') as f:json.dump(out,f,indent=2)

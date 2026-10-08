"""Independent Gauss-Legendre diagnostics; these are not certified bounds."""
import numpy as np
import json
from numpy.polynomial.legendre import leggauss
n=600
x,w=leggauss(n)
r=4*(x+1)
wr=4*w
p=8*np.sqrt(2/np.pi)*r*r*np.exp(-2*r*r)

def m(c):
    return np.sum(wr*p*(r/np.tanh(r/c)-c))
def logsinh(z):
    return z+np.log(-np.expm1(-2*z))-np.log(2)
def F(c,t,mu):
    q=1/c
    k=q-2*t*mu
    if abs(k)<1e-12:
        ratio=q*r/np.sinh(q*r)
    else:
        ratio=np.exp(logsinh(abs(k)*r)-logsinh(q*r))*q/abs(k)
    return np.sum(wr*p*np.exp(-t*(r*r+mu*mu))*ratio)
def gap(c,t,mu):
    return F(c,t,mu)-1/(1+t/2)
def optimize(c):
    ts=np.geomspace(0.001,15,90)
    mus=np.linspace(-1.15,0,120)
    best=(-100,None,None)
    for t in ts:
        for mu in mus:
            v=gap(c,t,mu)
            if v>best[0]: best=(float(v),float(t),float(mu))
    v,t,mu=best
    dt=0.12*t; dm=.02
    for _ in range(45):
        choices=[(gap(c,tt,mm),tt,mm) for tt in [max(1e-8,t-dt),t,t+dt] for mm in [mu-dm,mu,mu+dm]]
        v2,t2,mu2=max(choices)
        if v2<=v+1e-14:
            dt*=.6;dm*=.6
        else: v,t,mu=v2,t2,mu2
    return {'c':c,'polarization':float(m(c)),'gap':float(v),'t':float(t),'mu':float(mu)}
lo,hi=.01,2.
for _ in range(60):
    mid=(lo+hi)/2
    if m(mid)>.5:lo=mid
    else:hi=mid
out={'normalization':float(np.sum(wr*p)),'moment_threshold':(lo+hi)/2,'optimizations':[optimize(c) for c in [.05,.1,.2,.25,.3,.32,.33,.35,.4,.5,1.0]]}
print(json.dumps(out,indent=2))
with open('work/agents/thermal_blind/results/heat_witness_diagnostics.json','w') as f:json.dump(out,f,indent=2)

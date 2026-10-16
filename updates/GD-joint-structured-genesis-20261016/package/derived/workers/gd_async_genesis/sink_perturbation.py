"""Bounded independent search around an exactly saturating asynchronous sink.

Hilbert space C^3 x C^3, with parities diag(1,-1,-1) on each
factor. Each own odd gate rotates |0> toward a conditioned bright
vector in span(|1>,|2>), leaving its orthogonal vector dark.
"""
import json,time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
CAPS=np.array([.4,.2,.2,.2,.2,.4]); COORDS=[0,1,0,1,0,1]
ZA=np.diag(np.repeat([1,-1,-1],3)); ZB=np.diag(np.tile([1,-1,-1],3))
PARITY_BAD=np.array([4,5,7,8])

def gate(i,p):
    u=np.eye(9,dtype=complex)
    for other in range(3):
        theta,eta,phi0,phi1=p[other]
        v=np.array([np.cos(eta)*np.exp(1j*phi0),np.sin(eta)*np.exp(1j*phi1)])
        c,s=np.cos(theta),np.sin(theta)
        block=np.eye(3,dtype=complex);block[0,0]=c
        block[1:,1:]+=(c-1)*np.outer(v,v.conj())
        block[1:,0]=-1j*s*v;block[0,1:]=-1j*s*v.conj()
        inds=np.array([other,3+other,6+other]) if i==0 else np.array([3*other,3*other+1,3*other+2])
        u[np.ix_(inds,inds)]=block
    return u

def evaluate(x):
    rho=np.zeros((9,9),complex);rho[0,0]=1
    for k in range(6):
        u=gate(COORDS[k],x[k]);rho=u@rho@u.conj().T
        if k==1:rho=(rho+ZA@rho@ZA)/2
        if k==3:rho=(rho+ZB@rho@ZB)/2
    return float(np.real(np.diag(rho)[PARITY_BAD].sum()))

def project(x):
    x=x.copy();x[:,:,0]=np.clip(x[:,:,0],-CAPS[:,None],CAPS[:,None]);return x

def baseline():
    x=np.zeros((6,3,4));x[:,:,0]=CAPS[:,None]
    x[[2,4,5],:,1]=np.pi/2
    return x

def optimize(x,steps):
    x=project(x);m=np.zeros_like(x);v=m.copy();best=(evaluate(x),x.copy());h=2e-5
    for t in range(1,steps+1):
        grad=np.zeros_like(x)
        for n in np.ndindex(x.shape):
            xp=x.copy();xm=x.copy();xp[n]+=h;xm[n]-=h
            grad[n]=(evaluate(xp)-evaluate(xm))/(2*h)
        m=.9*m+.1*grad;v=.999*v+.001*grad*grad
        x=project(x+.025*(m/(1-.9**t))/(np.sqrt(v/(1-.999**t))+1e-8))
        val=evaluate(x)
        if val>best[0]:best=(val,x.copy())
    return best

def main():
    start=time.monotonic();rng=np.random.default_rng(74829)
    x0=baseline();q=1-np.cos(.4)**4;target=q*q;best=(evaluate(x0),x0)
    # Probe the local tangent with 256 random small directions, then run
    # exactly 8 fixed-seed starts of 180 steps each.
    probes=[]
    for _ in range(256):
        x=x0.copy();x[:,:,1:]+=rng.normal(0,.04,(6,3,3))
        probes.append(evaluate(x))
    vals=[]
    for r in range(8):
        x=x0.copy();x[:,:,1:]+=rng.normal(0,.15 if r<4 else .8,(6,3,3))
        val,xx=optimize(x,180);vals.append(val)
        if val>best[0]:best=(val,xx)
    out={"scope":"256 tangent probes; eight starts, 180 own optimizer steps, conditional rank-one qutrit gates",
         "dimension":9,"own_gap_actions":{"A":[.4,.4],"B":[.4,.4]},
         "target_product_Q":target,"exact_product_sink_numerical":evaluate(x0),
         "best_probability":best[0],"best_parameters":best[1].tolist(),
         "max_tangent_probe":max(probes),"per_start":vals,"elapsed_seconds":time.monotonic()-start,
         "interpretation":"Diagnostic only; no universal inference from failure to violate."}
    (ROOT/'sink_perturbation_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['best_parameters','per_start']},indent=2))

if __name__=='__main__':main()

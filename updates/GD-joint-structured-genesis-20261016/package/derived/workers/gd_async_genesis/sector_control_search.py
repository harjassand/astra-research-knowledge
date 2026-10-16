"""Bounded qutrit search with arbitrary real sector-preserving rotations.

Each of five baseline-control slots uses Givens rotations within the
two singly-wrong sectors and the four-dimensional jointly-wrong sector.
The baseline has no resource cap in the mathematical source contract.
"""
import json,time
from pathlib import Path
import numpy as np
from sink_perturbation import CAPS,COORDS,gate,baseline,ZA,ZB,PARITY_BAD

ROOT=Path(__file__).resolve().parent
PAIRS=[(3,6),(1,2),(4,5),(4,7),(4,8),(5,7),(5,8),(7,8)]

def control(angles):
    u=np.eye(9)
    for theta,(i,j) in zip(angles,PAIRS):
        c,s=np.cos(theta),np.sin(theta)
        ri=u[i].copy();rj=u[j].copy();u[i]=c*ri-s*rj;u[j]=s*ri+c*rj
    return u

def unpack(x):
    gates=baseline();gates[:,:,1]=x[:18].reshape(6,3)
    return gates,x[18:].reshape(5,8)

def evaluate(x):
    gates,controls=unpack(x)
    rho=np.zeros((9,9),complex);rho[0,0]=1
    for k in range(6):
        u=gate(COORDS[k],gates[k]);rho=u@rho@u.conj().T
        if k<5:
            h=control(controls[k]);rho=h@rho@h.T
        if k==1:rho=(rho+ZA@rho@ZA)/2
        if k==3:rho=(rho+ZB@rho@ZB)/2
    return float(np.real(np.diag(rho)[PARITY_BAD].sum()))

def optimize(x,steps):
    m=np.zeros_like(x);v=m.copy();best=(evaluate(x),x.copy());h=2e-5
    for t in range(1,steps+1):
        grad=np.zeros_like(x)
        for n in range(x.size):
            xp=x.copy();xm=x.copy();xp[n]+=h;xm[n]-=h
            grad[n]=(evaluate(xp)-evaluate(xm))/(2*h)
        m=.9*m+.1*grad;v=.999*v+.001*grad*grad
        x=x+.03*(m/(1-.9**t))/(np.sqrt(v/(1-.999**t))+1e-8)
        val=evaluate(x)
        if val>best[0]:best=(val,x.copy())
    return best

def main():
    start=time.monotonic();rng=np.random.default_rng(348012)
    x0=np.zeros(58);x0[:18]=baseline()[:,:,1].ravel()
    q=1-np.cos(.4)**4;target=q*q;best=(evaluate(x0),x0.copy());vals=[]
    for r in range(12):
        x=x0+rng.normal(0,.1 if r<6 else .9,58)
        val,xx=optimize(x,180);vals.append(val)
        if val>best[0]:best=(val,xx)
    out={"scope":"12 starts, 180 own optimizer steps; 58 real parameters; five sector-preserving control slots",
         "dimension":9,"own_gap_actions":{"A":[.4,.4],"B":[.4,.4]},
         "target_product_Q":target,"exact_product_sink_numerical":evaluate(x0),
         "best_probability":best[0],"best_parameters":best[1].tolist(),"per_start":vals,
         "elapsed_seconds":time.monotonic()-start,
         "interpretation":"Diagnostic only; no universal inference from failure to violate. Baseline control action is unconstrained in the mathematical model."}
    (ROOT/'sector_control_search_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['best_parameters','per_start']},indent=2))

if __name__=='__main__':main()

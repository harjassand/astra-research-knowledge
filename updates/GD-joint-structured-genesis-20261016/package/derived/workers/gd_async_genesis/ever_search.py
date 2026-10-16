"""Bounded no-bath search for the all-ever-mismatch record event."""
import json,time
from pathlib import Path
import numpy as np
from circuit_search import gate,CAPS,COORDS,project

ROOT=Path(__file__).resolve().parent
IND_A=np.array([0,0,1,1]);IND_B=np.array([0,1,0,1])

def evaluate(x):
    branches=[(np.array([1,0,0,0],complex),0,0)]
    for k in range(6):
        u=gate(COORDS[k],x[k]); branches=[(u@psi,a,b) for psi,a,b in branches]
        if k in [1,3]:
            idx=IND_A if k==1 else IND_B; bb=[]
            for psi,a,b in branches:
                for label in [0,1]:
                    ps=psi*(idx==label)
                    bb.append((ps,label if k==1 else a,label if k==3 else b))
            branches=bb
    p=0.
    for psi,a,b in branches:
        event=((a==1)|(IND_A==1)) & ((b==1)|(IND_B==1))
        p+=float(np.vdot(psi*event,psi*event).real)
    return p

def optimize(x,steps):
    x=project(x);m=np.zeros_like(x);v=m.copy();best=(evaluate(x),x.copy());h=1e-5
    for t in range(1,steps+1):
        grad=np.zeros_like(x)
        for n in np.ndindex(x.shape):
            xp=x.copy();xm=x.copy();xp[n]+=h;xm[n]-=h
            grad[n]=(evaluate(xp)-evaluate(xm))/(2*h)
        m=.9*m+.1*grad;v=.999*v+.001*grad*grad
        x=project(x+.035*(m/(1-.9**t))/(np.sqrt(v/(1-.999**t))+1e-8))
        val=evaluate(x)
        if val>best[0]:best=(val,x.copy())
    return best

def main():
    start=time.monotonic();rng=np.random.default_rng(18284)
    x0=np.zeros((6,4));x0[:,0]=x0[:,2]=CAPS
    q=1-np.cos(.4)**4;target=q*q;best=(evaluate(x0),x0.copy());vals=[]
    for r in range(32):
        x=x0.copy()
        if r:x[:,1::2]=rng.uniform(-np.pi,np.pi,(6,2))
        val,xx=optimize(x,180);vals.append(val)
        if val>best[0]:best=(val,xx)
    out={"scope":"32 starts, 180 own optimizer steps; no-bath controlled rotations; all-ever record objective",
         "own_gap_actions":{"A":[.4,.4],"B":[.4,.4]},"target_product_Q":target,
         "independent_qubits_numerical":evaluate(x0),"best_probability":best[0],
         "best_parameters":best[1].tolist(),"per_start":vals,"elapsed_seconds":time.monotonic()-start,
         "interpretation":"Diagnostic only; no universal inference from failure to violate."}
    (ROOT/'ever_search_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['best_parameters','per_start']},indent=2))

if __name__=='__main__':main()

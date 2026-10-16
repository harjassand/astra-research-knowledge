"""Own bounded diagnostics for the asynchronous two-parity question.

No package installation. Uses NumPy only. These finite controls are not proofs.
"""
import json, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
Z_A=np.diag([1,1,-1,-1]); Z_B=np.diag([1,-1,1,-1])
CAPS=np.array([.4,.2,.2,.2,.2,.4])
COORDS=[0,1,0,1,0,1]

def gate(coordinate, p):
    u=np.eye(4,dtype=complex)
    pairs=[(0,2),(1,3)] if coordinate==0 else [(0,1),(2,3)]
    for n,(i,j) in enumerate(pairs):
        angle,phase=p[2*n:2*n+2]
        c,s=np.cos(angle),np.sin(angle)
        u[i,i]=u[j,j]=c
        u[i,j]=-1j*s*np.exp(-1j*phase)
        u[j,i]=-1j*s*np.exp(1j*phase)
    return u

def evaluate(x):
    rho=np.diag([1,0,0,0]).astype(complex)
    for k in range(6):
        u=gate(COORDS[k],x[k]); rho=u@rho@u.conj().T
        if k==1: rho=(rho+Z_A@rho@Z_A)/2
        if k==3: rho=(rho+Z_B@rho@Z_B)/2
    return float(rho[3,3].real)

def project(x):
    x=x.copy()
    x[:,0]=np.clip(x[:,0],-CAPS,CAPS)
    x[:,2]=np.clip(x[:,2],-CAPS,CAPS)
    return x

def optimize(x,steps):
    # Deterministic central-difference Adam followed by coordinate polishing.
    x=project(x); m=np.zeros_like(x);v=m.copy(); best=(evaluate(x),x.copy())
    h=1e-5
    for t in range(1,steps+1):
        grad=np.zeros_like(x)
        for n in np.ndindex(x.shape):
            xp=x.copy();xm=x.copy();xp[n]+=h;xm[n]-=h
            grad[n]=(evaluate(xp)-evaluate(xm))/(2*h)
        m=.9*m+.1*grad;v=.999*v+.001*grad*grad
        x=project(x+.04*(m/(1-.9**t))/(np.sqrt(v/(1-.999**t))+1e-8))
        val=evaluate(x)
        if val>best[0]:best=(val,x.copy())
    return best

def main():
    start=time.monotonic();rng=np.random.default_rng(581237)
    q=1-np.cos(.4)**4; target=q*q; results=[]; best=(-1,None)
    for r in range(24):
        x=np.zeros((6,4)); x[:,0]=CAPS; x[:,2]=CAPS
        if r:
            x[:,0]*=rng.uniform(-1,1,6);x[:,2]*=rng.uniform(-1,1,6)
            x[:,1]=rng.uniform(-np.pi,np.pi,6);x[:,3]=rng.uniform(-np.pi,np.pi,6)
        val,xx=optimize(x,180)
        results.append(val)
        if val>best[0]:best=(val,xx)
    out={"scope":"24 fixed-seed starts, 180 own optimizer steps each, six no-bath controlled rotations",
         "caps":CAPS.tolist(),"own_gap_actions":{"A":[.4,.4],"B":[.4,.4]},
         "target_product_Q":target,"best_probability":best[0],"best_parameters":best[1].tolist(),
         "per_start":results,"elapsed_seconds":time.monotonic()-start,
         "interpretation":"Diagnostic only; no universal inference from failure to violate."}
    (ROOT/'circuit_search_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['best_parameters','per_start']},indent=2))

if __name__=='__main__':main()

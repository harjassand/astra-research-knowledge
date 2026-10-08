#!/usr/bin/env python3
"""Fixed-step RK4 invasion-rate reproduction for Hofbauer–Schreiber's periodic chemostat."""
from __future__ import annotations
import itertools, json, math
from pathlib import Path

D0, omega, R0 = 0.4675, 0.2, 11.0
alpha = (1.0, 0.7, 0.64)
beta = (1.0, 0.3, 0.2)
period = 2*math.pi/omega

def monod(R, i):
    return alpha[i]*R/(beta[i]+R)

def rhs(y, t, amp, residents):
    R=y[0]
    X=y[1:1+len(residents)]
    D=D0+amp*math.cos(omega*t)
    f=[monod(R,i) for i in range(3)]
    dR=(R0-R)*D-sum(f[i]*x for i,x in zip(residents,X))
    dx=[x*(f[i]-D) for i,x in zip(residents,X)]
    dq=[f[i]-D for i in range(3)]
    return [dR,*dx,*dq]

def rk4_step(y,t,h,amp,residents):
    k1=rhs(y,t,amp,residents)
    k2=rhs([a+h*b/2 for a,b in zip(y,k1)],t+h/2,amp,residents)
    k3=rhs([a+h*b/2 for a,b in zip(y,k2)],t+h/2,amp,residents)
    k4=rhs([a+h*b for a,b in zip(y,k3)],t+h,amp,residents)
    return [a+h*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(y,k1,k2,k3,k4)]

def cycle(y, amp, residents, nstep):
    h=period/nstep
    z=list(y)
    for k in range(nstep):
        z=rk4_step(z,k*h,h,amp,residents)
    return z

def face_orbit(amp,residents,nstep=240,max_cycles=500):
    requested=tuple(residents)
    residents=requested
    y=[R0]+[0.25 for _ in residents]
    hist=[]
    # Find the attracting periodic state on this face.
    for n in range(max_cycles):
        z=cycle(y,amp,residents,nstep)
        dist=max(abs(z[i]-y[i]) for i in range(1+len(residents)))
        y=z[:1+len(residents)]
        hist.append(dist)
        if dist<2e-10 and n>10:
            break
    # Assess resident support after convergence.
    support=tuple(i for i,x in zip(residents,y[1:]) if x>1e-7)
    if support != residents:
        # Refit the reduced support from the reached state.
        idx=[residents.index(i) for i in support]
        y=[y[0]]+[y[1+j] for j in idx]
        residents=support
        for n2 in range(max_cycles):
            z=cycle(y,amp,residents,nstep)
            dist=max(abs(z[i]-y[i]) for i in range(1+len(residents)))
            y=z[:1+len(residents)]
            if dist<2e-10 and n2>10: break
    # One period from the converged resident state gives the average per-capita rates.
    z=cycle(y+[0.0,0.0,0.0],amp,residents,nstep)
    lam=[v/period for v in z[1+len(residents):]]
    return {"requested_face":list(requested),"support":list(support),"state0":y,"periodic_residual":hist[-1] if hist else None,"cycles":len(hist),"lambda":lam}

def all_faces(amp,nstep):
    out=[]
    for k in range(4):
        for S in itertools.combinations(range(3),k):
            row=face_orbit(amp,S,nstep=nstep)
            row["amp"]=amp;row["nstep_per_period"]=nstep
            out.append(row)
    return out

if __name__=='__main__':
    allout=[]
    for a in (0.2,0.275,0.3,0.325):
        allout.extend(all_faces(a,240))
    p=Path(__file__).with_name('invasion_rates_rk4.json')
    p.write_text(json.dumps(allout,indent=2))
    for r in allout:
        ss=''.join(str(i+1) for i in r['support']) or '∅'
        print(f"a={r['amp']:.3f} requested={r['requested_face']} support={ss} cycles={r['cycles']} resid={r['periodic_residual']:.2e} lambda="+','.join(f'{x:+.7e}' for x in r['lambda']))
    print('wrote',p)

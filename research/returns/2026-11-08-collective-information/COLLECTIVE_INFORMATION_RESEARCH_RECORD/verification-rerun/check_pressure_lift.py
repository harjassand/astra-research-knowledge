"""Finite independent spectral/overlap check, not an infinite-volume proof."""
from pathlib import Path
from itertools import product
import json
import numpy as np

N,L=8,3
states=list(product((0,1),repeat=N));lookup={s:i for i,s in enumerate(states)}
size=len(states)
full=np.zeros((size,size));blocks=[];W=[]
for start in range(N):
    inside=[(start+j)%N for j in range(L)]
    z=np.zeros((size,size))
    for i,s in enumerate(states):
        for left in inside[:-1]:
            right=(left+1)%N
            if s[left]==s[right]:continue
            t=list(s);t[left],t[right]=t[right],t[left]
            j=lookup[tuple(t)];rate=1+s[(left-1)%N]*s[(left+2)%N]
            z[i,i]+=rate;z[i,j]-=rate
    blocks.append(z)
    W.append(np.array([s[inside[-1]]-s[inside[0]] for s in states],float))
for i,s in enumerate(states):
    for left in range(N):
        right=(left+1)%N
        if s[left]==s[right]:continue
        t=list(s);t[left],t[right]=t[right],t[left]
        j=lookup[tuple(t)];rate=1+s[(left-1)%N]*s[(left+2)%N]
        full[i,i]+=rate;full[i,j]-=rate
assert np.max(np.abs(sum(blocks)-(L-1)*full))<1e-13

g0=L**-2;vmax=0.;localrows=[]
groups={}
for i,s in enumerate(states):
    key=(sum(s[:L]),s[L:]);groups.setdefault(key,[]).append(i)
for ids in groups.values():
    g=blocks[0][np.ix_(ids,ids)];w=W[0][ids]
    assert abs(w.mean())<1e-13
    if len(ids)==1:continue
    ev,vec=np.linalg.eigh(g);positive=ev>1e-10
    assert ev[positive].min()>=g0-1e-12
    gp=(vec[:,positive]/ev[positive])@vec[:,positive].T
    v=float(w@gp@w/len(ids));vmax=max(vmax,v)
    for s in (-.04,.04):
        theta=abs(s)*max(abs(w))/g0
        actual=float(np.linalg.eigvalsh(-g+s*np.diag(w))[-1])
        bound=s*s*v/(1-theta)
        assert actual<=bound+1e-12
        localrows.append({'tilt':s,'actual':actual,'bound':bound})
a=np.array([(-1)**x*(1+.2*np.cos(x)) for x in range(N)])
A=max(abs(a));rows=[]
potential=sum(ax*w for ax,w in zip(a,W))
for beta in (.01,.03,.05,.1):
    assert beta*A/(N*g0)<=.5
    actual=float(np.linalg.eigvalsh(-N*N*full+(beta*N/L)*np.diag(potential))[-1]/N)
    bound=2*beta*beta*A*A*vmax/L
    assert actual<=bound+1e-11
    rows.append({'tilt':beta,'pressure_over_N':actual,'certified_upper':bound})

# A state-dependent multiplier destroys the first-order centering.
g=np.array([[1.,-1.],[-1.,1.]])
w=np.array([1.,-1.]);beta=.1
feedback_pressure=float(np.linalg.eigvalsh(-g+beta*np.diag(w*w))[-1])
misapplied_centered_bound=beta*beta*.5/(1-beta/2)
assert feedback_pressure>misapplied_centered_bound
out={'physical_experiments':0,'N':N,'L':L,'max_conditional_resolvent_variance':vmax,
     'block_sum_error':float(np.max(np.abs(sum(blocks)-(L-1)*full))),
     'local_spectral_cases':len(localrows),'ring_pressure':rows,
     'feedback_obstruction':{'actual_pressure':feedback_pressure,'invalid_centered_bound':misapplied_centered_bound}}
Path(__file__).with_name('pressure_lift_result.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))

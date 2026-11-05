"""Finite checks of the reusable interface and Ramsey calibration identity.
The five-qubit code is an algebraic example, not a BDL lifetime simulation.
"""
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

N = 5
def pauli(s):
    x = z = 0
    for j, c in enumerate(s):
        if c in 'XY': x |= 1 << j
        if c in 'ZY': z |= 1 << j
    return x, z
def mul(a,b): return a[0]^b[0],a[1]^b[1]
def symp(a,b):
    return ((a[0]&b[1]).bit_count()+(a[1]&b[0]).bit_count())%2
checks=list(map(pauli,['XZZXI','IXZZX','XIXZZ','ZXIXZ']))
lx,lz=pauli('XXXXX'),pauli('ZZZZZ')
singles=[(1<<j,0) for j in range(N)]+[(0,1<<j) for j in range(N)]+[(1<<j,1<<j) for j in range(N)]
def syndrome(p): return sum(symp(p,c)<<a for a,c in enumerate(checks))
frames={0:(0,0)}
for p in singles:
    assert syndrome(p) not in frames
    frames[syndrome(p)]=p
assert len(frames)==16
weights=np.array([.73,1.07,.91,1.23]);beta=2.4
energy=np.array([sum(weights[a] for a in range(4) if (s>>a)&1) for s in range(16)])
pi=np.exp(-beta*energy);pi/=pi.sum()
Q=np.zeros((16,16));K=np.zeros_like(Q);bad_rate=np.zeros(16)
for s in range(16):
    for p in singles:
        t=s^syndrome(p)
        residual=mul(frames[t],mul(p,frames[s]))
        assert syndrome(residual)==0
        logical=(symp(residual,lz),symp(residual,lx))
        r=1/(1+np.exp(beta*(energy[t]-energy[s])))
        Q[s,t]+=r;Q[s,s]-=r;K[s,s]-=r
        if logical==(0,0):K[s,t]+=r
        else:bad_rate[s]+=r
assert np.max(np.abs(pi@Q))<1e-12
assert np.max(np.abs(pi[:,None]*Q-(pi[:,None]*Q).T))<1e-12
assert bad_rate[0]==0
lam=float(pi@bad_rate);first_bad=[]
for T in [.001,.01,.1,.5]:
    p_bad=float(1-(pi@expm(T*K)).sum())
    assert p_bad<=T*lam+1e-12
    campaign=pi.copy()
    for t in [T/7,2*T/7,4*T/7]:campaign=campaign@expm(t*K)
    assert np.max(np.abs(campaign-pi@expm(T*K)))<1e-12
    first_bad.append(dict(passive_time=T,failure_probability=p_bad,stationary_flux_bound=T*lam))
ramsey_errors=[]
all_R=list(itertools.product(range(1<<N),repeat=2))
for a,S in enumerate(checks):
    probe=next(p for p in singles if symp(p,S))
    B=[b for b,C in enumerate(checks) if symp(probe,C)]
    recovered=0.
    for R in all_R:
        chi=np.array([(-1)**symp(R,C) for C in checks])
        gap=sum(weights[b]*chi[b] for b in B)
        recovered+=chi[a]*gap/len(all_R)
    ramsey_errors.append(abs(recovered-weights[a]))
assert max(ramsey_errors)<1e-12
phi=np.array([1,0,0,1])/np.sqrt(2);rho=np.outer(phi,phi)
p=pi.copy();p[0]-=.01;p[1]+=.01
trace_norm=sum(abs(p[s]-pi[s])*np.linalg.svd(rho,compute_uv=False).sum() for s in range(16))
tv=np.abs(p-pi).sum()/2
assert abs(trace_norm/2-tv)<1e-14
result=dict(example='five-qubit perfect code; interface check only',stationarity_residual=float(np.max(np.abs(pi@Q))),stationary_logical_jump_flux=lam,first_bad_jump_checks=first_bad,maximum_ramsey_coefficient_error=max(ramsey_errors),orthogonal_block_loading_TV=float(tv),all_checks_passed=True)
Path(__file__).with_name('register_verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

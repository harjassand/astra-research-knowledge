"""Finite diagnostics for a theorem proved separately in initial/machinery.md."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent
beta, angle, s = 2.3, np.pi/2, .17
u = np.diag([0.,0.,1.,1.]); a = np.zeros((4,4),complex); a[0,2]=1
up = np.array([[0,0],[1,0]],complex)
k = np.kron(a,up)+np.kron(a.conj().T,up.conj().T)
et = np.kron(u,np.eye(2))+np.kron(np.eye(4),np.diag([0.,1.]))
w = expm(-1j*angle*k); p1=1/(1+np.exp(beta)); p=[1-p1,p1]
ks=[np.sqrt(p[i])*w[o::2,i::2] for o in range(2) for i in range(2)]
v=np.diag(np.exp(s*np.diag(u)))
actual=sum(q.conj().T@v@q for q in ks)
expected=v@(np.eye(4)+p[0]*(np.exp(-s)-1)*a.conj().T@a+p[1]*(np.exp(s)-1)*a@a.conj().T)
gb=np.diag(np.exp(-beta*np.diag(u))); gb/=np.trace(gb)
res={"collision":{"energy_commutator":float(np.linalg.norm(k@et-et@k)),"dual_formula_error":float(np.linalg.norm(actual-expected)),"stationarity_error":float(np.linalg.norm(sum(q@gb@q.conj().T for q in ks)-gb)),"trace_error":float(np.linalg.norm(sum(q.conj().T@q for q in ks)-np.eye(4)))}}
n=6; xs=np.array([[(x>>i)&1 for i in range(n)] for x in range(2**n)])
energies=xs.sum(axis=1)+(xs*np.roll(xs,-1,axis=1)).sum(axis=1)
catalog=[(i,d) for i in range(n) for d in (1,2,3)]
beta,s=4.,.002; trans=np.eye(2**n)
for i,d in catalog:
    step=np.eye(2**n)
    for x in range(2**n):
        y=x^(1<<i); de=energies[y]-energies[x]
        if abs(de)!=d: continue
        p=1/(1+np.exp(-beta*d)) if de<0 else 1/(1+np.exp(beta*d))
        step[x,x]-=p; step[x,y]+=p
    trans=trans@step
C,kappa,M,D=9,1/3,len(catalog)/n,3
c=min(kappa/(C+2),.5); b=(D+C/(C+2))*M*np.exp(-beta)
mean_bound=(1-c)*energies+b*n
L=2*n  # loose finite range; asymptotic proof uses a constant causal cone
f=s*b+s*s*M*L*L/8
gb=np.exp(-beta*energies); gb/=gb.sum()
res["overlapping_sweep"]={"n":n,"states":2**n,"catalog":len(catalog),"mean_max_violation":float(np.max(trans@energies-mean_bound)),"mgf_max_ratio":float(np.max((trans@np.exp(s*energies))/np.exp(f*n+s*(1-c)*energies))),"stationarity_error":float(np.max(np.abs(gb@trans-gb))),"row_sum_error":float(np.max(np.abs(trans.sum(axis=1)-1))),"scope":"finite diagnostic only"}
assert res["collision"]["dual_formula_error"]<1e-12
assert res["overlapping_sweep"]["mean_max_violation"]<=1e-12
assert res["overlapping_sweep"]["mgf_max_ratio"]<=1+1e-12
(ROOT/'collision_checks.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))

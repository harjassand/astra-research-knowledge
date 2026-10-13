"""Check the optional measured-kinetic-energy and local-coherence budgets."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm,block_diag
from certificates import coherence_budget,histogram_interval,thermal_statistics
rng=np.random.default_rng(915811); rows=[]
for case in range(150):
    da,db=int(rng.integers(1,7)),int(rng.integers(1,7)); n=da+db
    a=rng.normal(size=(da,da))+1j*rng.normal(size=(da,da)); a=(a+a.conj().T)/2
    b=rng.normal(size=(db,db))+1j*rng.normal(size=(db,db)); b=(b+b.conj().T)/2
    if case%3==0: b+=30*np.eye(db)
    t=(rng.normal(size=(da,db))+1j*rng.normal(size=(da,db)))*rng.uniform(.03,.4)
    D=block_diag(a,b); T=np.zeros((n,n),complex); T[:da,da:]=t; T[da:,:da]=t.conj().T
    H=D+T; beta=float(rng.uniform(.3,3)); eh=expm(-beta*H); zd=np.trace(expm(-beta*D)).real
    z=np.trace(eh).real; rho=eh/z; tau=np.trace(rho@T).real
    k=np.linalg.norm(t,2); Cnorm=np.cosh(beta*k); Ckin=np.exp(max(0,-beta*tau))
    assert 1-1e-9<=z/zd<=min(Cnorm,Ckin)+1e-8
    labels=np.r_[np.zeros(da,dtype=int),np.ones(db,dtype=int)]
    p=np.array([np.trace(rho[:da,:da]).real,np.trace(rho[da:,da:]).real])
    v=rng.uniform(-5,5,size=2); f,p2=thermal_statistics(H,beta,labels,2)
    fv,_=thermal_statistics(H+np.diag(v[labels]),beta,labels,2)
    lo,hi=histogram_interval(p,v,beta,min(Cnorm,Ckin))
    assert lo-1e-9<=fv-f<=hi+1e-9
    rows.append({'C_norm':float(Cnorm),'C_kinetic':float(Ckin),'true_ratio':z/zd})
# Predefined off-resonant illustration: large operator norm, small energetic activity.
H=np.array([[0.,1.],[1.,100.]])
beta=1.;D=np.diag(np.diag(H));T=H-D;eh=expm(-H);z=np.trace(eh);tau=np.trace(eh@T)/z
example={'dimension':2,'level_offset':100.,'hopping':1.,'beta':1.,
         'C_norm':float(np.cosh(1.)),'C_kinetic':float(np.exp(-tau)),
         'true_Z_over_Zpinched':float(z/np.trace(expm(-D)))}
out={'passed_interacting_block_tests':len(rows),'measured_budget_better_count':sum(x['C_kinetic']<x['C_norm'] for x in rows),
     'illustration_not_scientific_benchmark':example,'warning':'double precision only'}
Path(__file__).with_name('kinetic_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

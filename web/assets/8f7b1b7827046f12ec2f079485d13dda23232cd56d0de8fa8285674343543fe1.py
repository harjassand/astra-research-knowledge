"""Seeded diagnostics for unequal squeezing, rectangular and rank-deficient maps.
Floating-point checks are not a proof or a certified numerical sampler.
"""
import json
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parent
rng=np.random.default_rng(20261008)

def realify(t):
    return np.block([[t.real,-t.imag],[t.imag,t.real]])

def ortho(m,k):
    return np.linalg.qr(rng.normal(size=(m,k))+1j*rng.normal(size=(m,k)))[0]

def sym(a): return (a+a.T)/2
max_flow=0.; max_dom=-float('inf'); max_jump=-float('inf')
max_passive=-float('inf'); max_budget=-float('inf'); smallest_y=float('inf')
counts={'fixtures':0,'trajectory_states':0,'rectangular_fixtures':0,'rank_deficient_fixtures':0}
for trial in range(250):
    m=int(rng.integers(2,10)); n=int(rng.integers(1,9))
    k=int(rng.integers(1,min(m,n)+1))
    U=ortho(m,k); V=ortho(n,k)
    nus=rng.uniform(.0005,.09,size=k)
    L=realify(np.diag(np.sqrt(nus))@V.conj().T)
    O=realify(U); C=L@L.T; dim=2*k; I=np.eye(dim)
    J=np.block([[np.zeros((k,k)),-np.eye(k)],[np.eye(k),np.zeros((k,k))]])
    project=lambda A:sym((A+J@A@J.T)/2)
    rs=rng.uniform(.02,1.8,size=n)
    ns=np.sinh(rs)**2; ms=np.sinh(rs)*np.cosh(rs)
    R=(L*np.tile(ns,2))@L.T
    X=(L*np.concatenate([ms,-ms]))@L.T
    K0=sym(R+X)
    D=sym(X@np.linalg.solve(R,X)-R)
    max_dom=max(max_dom,np.linalg.eigvalsh(sym(D-C))[-1])
    B0=sym(C@np.linalg.inv(I-C))
    pmax=float(np.max(ns+ms)); S3=float(np.sum(nus**3))
    phi0=float(np.trace((K0+B0)@K0@K0))
    budget=2*pmax*pmax*(pmax+1/(1-max(nus)))*S3
    max_budget=max(max_budget,(phi0-budget)/(1+budget))
    Ps=[]
    for i in range(m):
        Ri=O[[i,i+m],:]; Ps.append(Ri.T@Ri)
    for u in (.0,.4,.8,1.):
        H=sym(K0@np.linalg.inv(I+u*K0))
        Rh=project(H); Xh=H-Rh
        Dh=sym(Xh@np.linalg.solve(Rh,Xh)-Rh)
        expected=D@np.linalg.inv(I-u*D)
        max_flow=max(max_flow,np.linalg.norm(Dh-expected,ord=2)/(1+np.linalg.norm(Dh,ord=2)))
        Gamma=-B0+B0@np.linalg.solve(H+B0,B0)
        max_passive=max(max_passive,np.linalg.eigvalsh(project(Gamma))[-1])
    K=K0.copy(); B=B0.copy()
    for step in range(5):
        v=float(rng.uniform(.3,1.)); K=sym(v*K@np.linalg.inv(I+(1-v)*K)); B*=v
        Y=K+B
        smallest_y=min(smallest_y,float(np.linalg.eigvalsh(Y)[0]))
        rates=np.array([np.trace(P@K)/2 for P in Ps])
        assert min(rates)>-1e-10
        ds=[sym(K@P@K/lam) for P,lam in zip(Ps,rates) if lam>1e-13]
        max_jump=max(max_jump,max(float(np.linalg.eigvalsh(d-2*Y)[-1]) for d in ds))
        chosen=int(rng.choice(m,p=np.maximum(rates,0)/sum(np.maximum(rates,0))))
        K=sym(K+K@Ps[chosen]@K/rates[chosen]); counts['trajectory_states']+=1
    counts['fixtures']+=1
    counts['rectangular_fixtures']+=int(m!=n)
    counts['rank_deficient_fixtures']+=int(k<min(m,n))
assert max_flow<1e-9 and max_dom<1e-9 and max_jump<1e-9 and max_passive<1e-9 and smallest_y>-1e-9 and max_budget<1e-9
out={'status':'PASS','seed':20261008,**counts,'max_relative_schur_flow_residual':max_flow,
     'max_D_minus_C_eigenvalue':max_dom,'max_jump_minus_2Y_eigenvalue':max_jump,
     'max_passive_resolvent_eigenvalue':max_passive,'min_Y_eigenvalue':smallest_y,
     'max_normalized_budget_excess':max_budget,'scope':'Seeded finite floating-point diagnostics only'}
(root/'general_random_results.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))

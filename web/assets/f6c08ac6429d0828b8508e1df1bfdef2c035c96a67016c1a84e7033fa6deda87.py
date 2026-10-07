"""Seeded floating-point adversarial diagnostics for the matrix certificate."""
import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(20261007)
root=Path(__file__).resolve().parent

def unitary(n):
    Z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    Q,R=np.linalg.qr(Z)
    d=np.diag(R); return Q*(d/np.abs(d))
def realify(T): return np.block([[T.real,-T.imag],[T.imag,T.real]])
def sym(A):return (A+A.T)/2
worst={'passive_upper_eigenvalue':-1e10,'relative_jump_upper_eigenvalue':-1e10,
       'normalized_drift_excess':-1e10,'normalized_initial_budget_excess':-1e10,
       'smallest_Y_eigenvalue':1e10}
states=0
for fixture in range(200):
    N=int(rng.integers(2,9)); r=float(rng.uniform(.15,1.8))
    n=np.sinh(r)**2; m=np.sinh(r)*np.cosh(r); p=n+m
    eta=np.exp(rng.uniform(np.log(.0004),np.log(.09),N))
    T=unitary(N)@np.diag(np.sqrt(eta))@unitary(N)
    L=realify(T); C=sym(L@L.T)
    K0=sym(n*C+m*L@np.diag([1.]*N+[-1.]*N)@L.T)
    B0=C/(1-eta.max()); I=np.eye(2*N)
    J=np.block([[np.zeros((N,N)),-np.eye(N)],[np.eye(N),np.zeros((N,N))]])
    u=float(rng.uniform(0,.95)); v=1-u
    H=sym(K0@np.linalg.inv(I+u*K0))
    G=sym(-B0+B0@np.linalg.inv(H+B0)@B0)
    passive=sym((G+J@G@J.T)/2)
    worst['passive_upper_eigenvalue']=max(worst['passive_upper_eigenvalue'],float(np.linalg.eigvalsh(passive)[-1]))
    phi0=np.trace((K0+B0)@K0@K0)
    bound=2*p*p*(p+1/(1-eta.max()))*sum(eta**3)
    worst['normalized_initial_budget_excess']=max(worst['normalized_initial_budget_excess'],float((phi0-bound)/(1+bound)))
    K=v*H; B=v*B0
    for step in range(6):
        Y=sym(K+B); ev=np.linalg.eigvalsh(Y)
        worst['smallest_Y_eigenvalue']=min(worst['smallest_Y_eigenvalue'],float(ev[0]))
        rates=[]; ds=[]
        for i in range(N):
            inds=[i,i+N]; la=(K[i,i]+K[i+N,i+N])/2
            assert la>0
            D=sym(K[:,inds]@K[inds,:]/la)
            ex=np.linalg.eigvalsh(sym(D-2*Y))[-1]
            worst['relative_jump_upper_eigenvalue']=max(worst['relative_jump_upper_eigenvalue'],float(ex))
            rates.append(la); ds.append(D)
        weighted=sum((la*D for la,D in zip(rates,ds)),np.zeros_like(K))
        assert np.linalg.norm(weighted-K@K)<1e-8*(1+np.linalg.norm(K@K))
        rem=sum(la*np.trace((Y+2*K)@D@D+D@D@D) for la,D in zip(rates,ds))
        upper=10*np.trace(Y@Y@K@K)
        worst['normalized_drift_excess']=max(worst['normalized_drift_excess'],float((rem-upper)/(1+abs(upper))))
        states+=1
        K=sym(K+ds[int(rng.integers(N))])
        # Allow a flow interval before the next click.
        vv=float(rng.uniform(.6,1.)); K=sym(vv*K@np.linalg.inv(I+(1-vv)*K)); B*=vv
assert worst['passive_upper_eigenvalue']<1e-9
assert worst['relative_jump_upper_eigenvalue']<1e-9
assert worst['normalized_drift_excess']<1e-9
assert worst['normalized_initial_budget_excess']<1e-9
assert worst['smallest_Y_eigenvalue']>-1e-9
out={'status':'PASS','seed':20261007,'fixtures':200,'trajectory_states':states,'worst_diagnostics':worst,
     'scope':'Floating-point diagnostics, not a proof; square full-rank contractions, random noncommuting mixing, 2-8 modes.'}
(root/'random_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

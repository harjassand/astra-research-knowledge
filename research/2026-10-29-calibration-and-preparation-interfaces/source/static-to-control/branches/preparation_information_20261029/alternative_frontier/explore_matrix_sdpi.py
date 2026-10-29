"""Exploratory search only: neither numerical optima nor no-separation are proofs."""
import json, numpy as np
from pathlib import Path
from scipy.optimize import differential_evolution, minimize
from scipy.special import softmax, xlogy
BASE=Path(__file__).resolve().parent
rng=np.random.default_rng(20261029)
def ent_mat(A):
    ev=np.maximum(np.linalg.eigvalsh(A),0)
    return np.sum(xlogy(ev,ev))
def scalar_eta(T,pi):
    q=T@pi
    def ratio(u):
        p=softmax(np.r_[u,0.])
        D=np.sum(xlogy(p,p/pi))
        if D<1e-11:return 0.
        z=T@p
        return np.sum(xlogy(z,z/q))/D
    r=differential_evolution(lambda u:-ratio(u),[(-25,25)]*(len(pi)-1),tol=1e-9,popsize=12,maxiter=120,seed=73)
    vals=[(-r.fun,softmax(np.r_[r.x,0.]))]
    for i in range(len(pi)):
        p=np.eye(len(pi))[i];z=T@p
        vals.append((np.sum(xlogy(z,z/q))/np.log(1/pi[i]),p))
    return max(vals,key=lambda x:x[0])
def quantum_ratio(v,T,pi,d):
    n=len(pi)
    L=v.reshape(n,d,d)
    A=np.einsum('nik,njk->nij',L,L)
    norm=np.trace(A,axis1=1,axis2=2).sum()
    if norm<1e-20:return 0.
    A=A/norm;K=A.sum(0);Y=np.einsum('yn,nij->yij',T,A)
    ek=ent_mat(K)
    din=sum(ent_mat(a) for a in A)-ek-np.dot(np.trace(A,axis1=1,axis2=2),np.log(pi))
    dout=sum(ent_mat(y) for y in Y)-ek-np.dot(np.trace(Y,axis1=1,axis2=2),np.log(T@pi))
    return dout/din if din>1e-11 else 0.
rows=[]
for k in range(16):
    n=3;d=2 if k<8 else 3
    alpha=0.3 if k%2 else 1.
    T=np.column_stack([rng.dirichlet(np.full(3,alpha)) for _ in range(n)])
    pi=rng.dirichlet(np.full(n,alpha))
    eta,pstar=scalar_eta(T,pi)
    best=(-1,None)
    for j in range(6):
        init=rng.normal(size=n*d*d)
        if j==0:
            init=np.zeros((n,d,d));init[:,0,0]=np.sqrt(pstar+1e-8);init=init.ravel()
        res=minimize(lambda v:-quantum_ratio(v,T,pi,d),init,method='BFGS',options={'maxiter':160,'gtol':3e-7})
        val=-res.fun
        if val>best[0]:best=(val,res.x.tolist())
    rows.append({'k':k,'d':d,'T':T.tolist(),'pi':pi.tolist(),'scalar_lower_bound':float(eta),'scalar_candidate':pstar.tolist(),'matrix_lower_bound':float(best[0]),'matrix_candidate':best[1],'candidate_gap':float(best[0]-eta)})
    print(k,d,eta,best[0],best[0]-eta,flush=True)
(BASE/'MATRIX_SDPI_EXPLORATION.json').write_text(json.dumps({'status':'exploration; all optima are lower bounds; no certification','seed':20261029,'rows':rows},indent=2))


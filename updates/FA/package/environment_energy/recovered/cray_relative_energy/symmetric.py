"""SU(2)-covariant reduction for the relative-energy channel prototype."""
from __future__ import annotations
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,time,json
from pathlib import Path
from scipy.linalg import eigh,null_space
from scipy.sparse.linalg import eigsh
from scipy.optimize import linprog, minimize
from experiment import kagome,heisenberg,local_pair


def su2_basis(d=4):
    if d!=4:raise ValueError('This diagnostic uses an active spin pair.')
    m=d*d;iu,ju=np.triu_indices(m);p=len(iu)
    B=np.zeros((p,m,m))
    for k,(i,j) in enumerate(zip(iu,ju)):B[k,i,j]=B[k,j,i]=1
    # Enforce the unital trace constraints and covariance of the Choi matrix.
    tr=np.stack([sum(T.reshape(d,d,d,d)[i,:,i,:] for i in range(d)) for T in B])
    eq=[tr.reshape(p,-1).T]
    sig=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
    for s in sig:
        S=(np.kron(s,np.eye(2))+np.kron(np.eye(2),s))/2
        G=-np.kron(S.T,np.eye(d))+np.kron(np.eye(d),S)
        com=G@B-B@G
        eq.extend([com.real.reshape(p,-1).T,com.imag.reshape(p,-1).T])
    N=null_space(np.concatenate(eq),rcond=1e-10)
    return np.eye(m)/d,np.einsum('pk,pij->kij',N,B),N


def lower_symmetric(ha,hb,d=4,maxiter=180,tol=1e-6,verbose=True):
    D=len(ha);r=D//d;m=d*d
    t0=time.perf_counter();C0,BC,N=su2_basis(d);k=len(BC)
    def image(C):return np.einsum('iajb,irjs->arbs',C.reshape(d,d,d,d),ha.reshape(d,r,d,r),optimize=True).reshape(D,D)
    R0=hb-image(C0);BR=-np.stack([image(B) for B in BC])
    ident=np.outer(np.eye(d).ravel(),np.eye(d).ravel())
    iu,ju=np.triu_indices(m);xid=N.T@(ident-C0)[iu,ju]
    assert np.linalg.norm(C0+np.einsum('k,kij->ij',xid,BC)-ident)<1e-9
    if verbose:print('reduced real channel dimension',k,'matrix dimensions',m,D,flush=True)
    raw=eigh(hb-ha,eigvals_only=True);best=float(raw[0]);bestC=ident;A=[];b=[];hist=[]
    def ccut(v):return np.r_[-np.einsum('i,kij,j->k',v,BC,v),0],float(v@C0@v)
    def rcut(v):return np.r_[-np.einsum('i,kij,j->k',v,BR,v),1],float(v@R0@v)
    for v in np.eye(m):row,y=ccut(v);A.append(row);b.append(y)
    for v in eigh(R0)[1].T:row,y=rcut(v);A.append(row);b.append(y)
    upper=raw[-1]
    for it in range(maxiter):
        sol=linprog(np.r_[np.zeros(k),-1.],A_ub=np.array(A),b_ub=np.array(b),bounds=[(-d-1,d+1)]*k+[(raw[0]-1e-8,raw[-1]+1e-8)],method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
        if not sol.success:raise RuntimeError(sol.message)
        u=sol.x[:-1];upper=float(sol.x[-1]);C=C0+np.einsum('k,kij->ij',u,BC);R=R0+np.einsum('k,kij->ij',u,BR)
        ce,cv=eigh(C);re,rv=eigh(R)
        t=max(0.,-d*ce[0])+1e-13;Cp=(C+t*C0)/(1+t)
        actual=float(eigh(hb-image(Cp),eigvals_only=True)[0])
        if actual>best:best=actual;bestC=Cp
        hist.append([it,upper,best,ce[0],re[0],len(A),time.perf_counter()-t0])
        if verbose and (it%10==0 or upper-best<tol):print('it',it,'outer',upper,'feasible',best,'gap',upper-best,'cuts',len(A),flush=True)
        if upper-best<tol:break
        for v in cv[:,ce<-tol*.05].T:row,y=ccut(v);A.append(row);b.append(y)
        for v in rv[:,re<upper-tol*.05].T:row,y=rcut(v);A.append(row);b.append(y)
    return {'lower':best,'optimization_upper':upper,'seconds':time.perf_counter()-t0,'iterations':it+1,'choi':bestC,'history':hist,'raw_lower':float(raw[0]),'raw_upper':float(raw[-1]),'reduced_dim':k}

if __name__=='__main__':
    import argparse
    pa=argparse.ArgumentParser();pa.add_argument('--system',default='kagome');pa.add_argument('--delta',type=float,default=1.);pa.add_argument('--reverse',action='store_true');pa.add_argument('--iter',type=int,default=200);a=pa.parse_args()
    if a.system=='kagome':coords,edges=kagome();n=len(coords)
    elif a.system=='chain':n=12;edges=[(i,(i+1)%n,1.) for i in range(n)]
    elif a.system=='dimer':n=4;edges=[(0,1,1.),(1,2,.2),(2,3,1.)]
    else:raise ValueError('Unknown system')
    change=(0,1,a.delta);ha,hb,sites=local_pair(edges,[0,1],change)
    if a.reverse:ha,hb=hb,ha
    out=lower_symmetric(ha,hb,maxiter=a.iter)
    C=out.pop('choi');suffix=f'sym_{a.system}_{a.delta}_{"rev" if a.reverse else "fwd"}'
    np.savez(Path(__file__).parent/f'{suffix}.npz',ha=ha,hb=hb,choi=C)
    ea=float(eigsh(heisenberg(n,edges),k=1,which='SA',return_eigenvectors=False,tol=1e-12)[0]);eb=float(eigsh(heisenberg(n,edges)+heisenberg(n,[change]),k=1,which='SA',return_eigenvectors=False,tol=1e-12)[0])
    out.update({'system':a.system,'n':n,'sites':sites,'delta':a.delta,'reverse':a.reverse,'EA':ea,'EB':eb,'exact_difference_numeric':eb-ea,'edges':edges})
    (Path(__file__).parent/f'{suffix}.json').write_text(json.dumps(out,indent=2))
    print({k:v for k,v in out.items() if k not in ['history','edges']},flush=True)

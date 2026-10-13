"""Direct relative-ground-energy bounds via local unital CP maps.
Research prototype; spectral checks use floating point, not interval arithmetic.
No quantum-state or full-environment input is used by the certificate solver.
"""
from __future__ import annotations
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import json,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import eigh
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh


def kagome(lx:int=2,ly:int=2):
    a=np.array([1.,0.]); b=np.array([.5,np.sqrt(3)/2])
    basis=[np.array([0.,0.]),a/2,b/2]
    coords=np.array([x*a+y*b+r for x in range(lx) for y in range(ly) for r in basis])
    edges=[]
    for i in range(len(coords)):
        for j in range(i+1,len(coords)):
            dist=min(np.linalg.norm(coords[i]-coords[j]+p*lx*a+q*ly*b) for p in [-1,0,1] for q in [-1,0,1])
            if abs(dist-.5)<1e-8: edges.append((i,j,1.))
    return coords,edges


def heisenberg(n:int,edges:list,field:dict|None=None):
    """S_i.S_j with spin-1/2 and computational basis site 0 most significant."""
    D=2**n; rr=[];cc=[];vv=[]
    for z in range(D):
        diag=0.
        for i,j,J in edges:
            pi=1<<(n-1-i);pj=1<<(n-1-j)
            same=bool(z&pi)==bool(z&pj)
            diag+=J*(.25 if same else -.25)
            if not same: rr.append(z);cc.append(z^pi^pj);vv.append(J*.5)
        if field:
            for i,h in field.items(): diag+=h*(.5 if not(z&(1<<(n-1-i))) else -.5)
        rr.append(z);cc.append(z);vv.append(diag)
    return coo_matrix((vv,(rr,cc)),shape=(D,D)).tocsr()


def local_pair(edges,active,change):
    """Only terms meeting active set survive the channel subtraction."""
    touch=[e for e in edges if e[0] in active or e[1] in active]
    sites=list(active)+sorted(set(sum(([i,j] for i,j,_ in touch),[]))-set(active))
    ix={a:i for i,a in enumerate(sites)}
    loc=[(ix[i],ix[j],J) for i,j,J in touch]
    ha=heisenberg(len(sites),loc).toarray()
    hb=ha.copy()
    i,j,delta=change
    hb+=heisenberg(len(sites),[(ix[i],ix[j],delta)]).toarray()
    return ha,hb,sites


def lower_channel(ha,hb,d,maxiter=220,tol=1e-6,verbose=True):
    D=len(ha); r=D//d; m=d*d
    assert ha.shape==hb.shape and D==d*r
    iu,ju=np.triu_indices(m);p=len(iu)
    pairindex={(a,b):k for k,(a,b) in enumerate(zip(iu,ju))}
    def unpack(x):
        C=np.zeros((m,m));C[iu,ju]=x[:p];C[ju,iu]=x[:p];return C
    def pack(G): return G[iu,ju]*np.where(iu==ju,1.,2.)
    ha4=ha.reshape(d,r,d,r)
    def image(C):
        return np.einsum('iajb,irjs->arbs',C.reshape(d,d,d,d),ha4,optimize=True).reshape(D,D)
    def energycut(v):
        vv=v.reshape(d,r)
        G=np.einsum('irjs,ar,bs->iajb',ha4,vv,vv,optimize=True).reshape(m,m)
        return np.r_[pack(G),1.],float(v@hb@v)
    Aeq=[];beq=[]
    for a in range(d):
        for b in range(a,d):
            row=np.zeros(p+1)
            for i in range(d): row[pairindex[(i*d+a,i*d+b)]]+=1
            Aeq.append(row);beq.append(float(a==b))
    A=[];rhs=[]
    # Finite outer approximations; eigenvector separation adds missing PSD tests.
    for a in range(m):
        for b in range(a+1,m):
            for sign in [-1,1]:
                v=np.zeros(m);v[a]=1/np.sqrt(2);v[b]=sign/np.sqrt(2)
                A.append(np.r_[-pack(np.outer(v,v)),0.]);rhs.append(0.)
    for v in eigh(hb)[1].T:
        row,val=energycut(v);A.append(row);rhs.append(val)
    va=eigh(hb-ha,eigvals_only=True);lo=float(va[0]);hi=float(va[-1])
    bounds=[(0.,float(d)) if a==b else (-float(d),float(d)) for a,b in zip(iu,ju)]+[(lo-1e-9,hi+1e-9)]
    obj=np.r_[np.zeros(p),-1.]
    eyeC=np.eye(m)/d
    omega=np.eye(d).ravel();identC=np.outer(omega,omega)
    assert np.linalg.norm(image(identC)-ha)<1e-10
    best=lo;bestC=identC;hist=[];start=time.perf_counter()
    for it in range(maxiter):
        sol=linprog(obj,A_ub=np.asarray(A),b_ub=np.asarray(rhs),A_eq=np.asarray(Aeq),b_eq=np.asarray(beq),bounds=bounds,method='highs',options={'dual_feasibility_tolerance':1e-8,'primal_feasibility_tolerance':1e-8})
        if not sol.success: raise RuntimeError(sol.message)
        C=unpack(sol.x);c=float(sol.x[-1]);ce,cv=eigh(C)
        Re,Rv=eigh(hb-image(C))
        t=max(0.,-d*ce[0])+1e-12
        Cp=(C+t*eyeC)/(1+t)
        actual=float(eigh(hb-image(Cp),eigvals_only=True,subset_by_index=[0,0])[0])
        if actual>best: best=actual;bestC=Cp
        hist.append([it,c,best,float(ce[0]),float(Re[0]),len(A),time.perf_counter()-start])
        if verbose and (it%10==0 or c-best<tol): print('iter',it,'upper',c,'feasible',best,'gap',c-best,'cuts',len(A),flush=True)
        if c-best<tol: break
        for k in np.where(ce<-tol*.05)[0]:
            A.append(np.r_[-pack(np.outer(cv[:,k],cv[:,k])),0.]);rhs.append(0.)
        for k in np.where(Re<c-tol*.05)[0]:
            row,val=energycut(Rv[:,k]);A.append(row);rhs.append(val)
    return {'lower':best,'optimization_upper':c,'seconds':time.perf_counter()-start,'iterations':it+1,'choi':bestC,'history':hist,'raw_lower':lo,'raw_upper':hi}

if __name__=='__main__':
    import argparse
    pa=argparse.ArgumentParser();pa.add_argument('--delta',type=float,default=1.);pa.add_argument('--reverse',action='store_true');pa.add_argument('--iter',type=int,default=180);pa.add_argument('--system',default='kagome');a=pa.parse_args()
    if a.system=='kagome':
        coords,edges=kagome();n=len(coords)
    elif a.system=='chain':
        n=12;edges=[(i,(i+1)%n,1.) for i in range(n)]
    elif a.system=='dimer':
        n=4;edges=[(0,1,1.),(1,2,.2),(2,3,1.)]
    else: raise ValueError('Unknown system')
    bond=(0,1,a.delta);ha,hb,sites=local_pair(edges,[0,1],bond)
    print('sites',sites,'localdim',len(ha),'edges',edges,flush=True)
    if a.reverse:ha,hb=hb,ha
    out=lower_channel(ha,hb,4,maxiter=a.iter)
    C=out.pop('choi');suffix=f'{a.system}_{a.delta}_{"rev" if a.reverse else "fwd"}'
    np.savez(Path(__file__).parent/f'{suffix}.npz',ha=ha,hb=hb,choi=C)
    fullA=heisenberg(n,edges);fullB=fullA+heisenberg(n,[bond])
    EA=float(eigsh(fullA,k=1,which='SA',return_eigenvectors=False,tol=1e-11)[0]);EB=float(eigsh(fullB,k=1,which='SA',return_eigenvectors=False,tol=1e-11)[0])
    out.update({'system':a.system,'n':n,'sites':sites,'delta':a.delta,'reverse':a.reverse,'EA':EA,'EB':EB,'exact_difference_numeric':EB-EA,'edges':edges})
    (Path(__file__).parent/f'{suffix}.json').write_text(json.dumps(out,indent=2))
    print({k:v for k,v in out.items() if k not in ['history','edges']},flush=True)

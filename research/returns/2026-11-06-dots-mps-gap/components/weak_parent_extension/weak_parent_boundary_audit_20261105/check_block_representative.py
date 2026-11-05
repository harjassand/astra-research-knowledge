"""Independent finite operator checks of b=B_k/(k-1), including boundaries."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
from pathlib import Path
import json, time
import numpy as np
import scipy.linalg as la

OUT=Path(__file__).resolve().parent


def embed(A, axes, d, N):
    axes=list(axes)
    T=np.eye(d**N,dtype=complex).reshape(*([d]*N),d**N)
    perm=axes+[j for j in range(N+1) if j not in axes]
    Z=T.transpose(perm);shape=Z.shape
    return (A@Z.reshape(d**len(axes),-1)).reshape(shape).transpose(np.argsort(perm)).reshape(d**N,d**N)


def native(lambdas):
    d=len(lambdas)+1;lam=np.r_[1,lambdas]
    h=np.zeros((d*d,d*d),complex)
    for i in range(d):
        for j in range(i+1,d):
            v=np.zeros(d*d,complex);v[i*d+j]=1
            v[j*d+i]=-np.exp(1j*(.17+i*.11+j*.07))*lam[j]/lam[i]
            v/=la.norm(v);h+=np.outer(v,v.conj())
    for i in range(1,d):h[i*d+i,i*d+i]=1
    X=np.diag(np.r_[0,.5-np.array(lambdas)**2/(1+np.array(lambdas)**2)])
    return h,X,d


def models():
    d=3;h=np.zeros((9,9),complex)
    for s,lam in ((1,.5),(2,2.)):
        v=np.zeros(9);v[s]=1;v[3*s]=-lam;v/=la.norm(v);h+=np.outer(v,v)
    for i in (1,2):
        for j in (1,2):h[3*i+j,3*i+j]=1
    yield 'closing-open-gap qutrit',h,np.diag([0,.3,-.3]),3,2
    h,X,d=native([.5,.5])
    yield 'native two equal species with complex phases',h,X,d,3
    diag=np.ones(9);diag[0]=0;diag[5]=diag[7]=.1
    yield 'positive B3 with indefinite shifted two-site term',np.diag(diag),np.diag([0,.5,-.5]),3,3


def check(label,h,X,d,k):
    B=sum(embed(h,(j,j+1),d,k) for j in range(k-1))+embed(X,(0,),d,k)-embed(X,(k-1,),d,k)
    b=B/(k-1);ev=la.eigvalsh(B)
    assert abs(ev[0])<1e-12 and ev[1]>1e-10
    assert la.norm(B[:,0])<1e-12
    shifted=h+np.kron(X,np.eye(d))-np.kron(np.eye(d),X)
    periodic=[]
    for N in (k,k+1,k+2):
        # N=k=2 has the standard two oriented bonds; both conventions compared identically.
        Hh=sum(embed(h,(j,(j+1)%N),d,N) for j in range(N))
        Hb=sum(embed(b,[(j+a)%N for a in range(k)],d,N) for j in range(N))
        err=float(la.norm(Hb-Hh,2));assert err<1e-11
        periodic.append(dict(N=N,operator_equality_error=err))
    L=2*k-1;J=L-k+1
    Hh=sum(embed(h,(j,j+1),d,L) for j in range(L-1))
    Hb=sum(embed(b,range(j,j+k),d,L) for j in range(J))
    weighted=np.zeros_like(Hh)
    weights=[]
    for j1 in range(1,L):
        w=max(0,min(j1,J)-max(1,j1-k+2)+1);weights.append(w)
        weighted+=w*embed(h,(j1-1,j1),d,L)/(k-1)
    for x in range(J):weighted+=(embed(X,(x,),d,L)-embed(X,(x+k-1,),d,L))/(k-1)
    boundary_error=float(la.norm(Hb-weighted,2));assert boundary_error<1e-11
    # The centered site is disjoint from the two endpoint correction supports.
    A=np.arange(d*d).reshape(d,d)+1j*np.eye(d)
    A=embed(A,(k-1,),d,L)
    diff=Hb-Hh
    comm=float(la.norm(diff@A-A@diff,2));assert comm<1e-11
    eopen=la.eigvalsh(Hb)
    assert abs(eopen[0])<1e-11 and eopen[1]>=ev[1]/(k-1)-1e-11
    return dict(model=label,d=d,k=k,B_kernel_dimension=1,B_coercive_c=float(ev[1]),
                shifted_two_site_minimum=float(la.eigvalsh(shifted)[0]),
                periodic=periodic,open_length=L,open_bond_counts=weights,
                open_weight_formula_error=boundary_error,
                original_representative_open_difference_norm=float(la.norm(diff,2)),
                interior_derivation_error=comm,
                representative_open_gap=float(eopen[1]),
                guaranteed_open_gap=float(ev[1]/(k-1)))


def main():
    start=time.perf_counter()
    cases=[check(*m) for m in models()]
    assert cases[-1]['shifted_two_site_minimum']<-.8
    result=dict(scope='Finite full-operator verification of exact algebra; no infinite-gap numerical inference',
                cases=cases,elapsed_seconds=time.perf_counter()-start)
    (OUT/'block_representative_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

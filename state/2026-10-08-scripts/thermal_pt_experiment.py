import numpy as np
from scipy.linalg import eigh, expm
from math import comb, sqrt

def make_projectors(N):
    groups={}
    for mask in range(1<<N): groups.setdefault(mask.bit_count(),[]).append(mask)
    blocks=[]
    for k, ids in sorted(groups.items()):
        m=k-N/2;dim=len(ids);pos={x:i for i,x in enumerate(ids)}
        A=np.eye(dim)*(m*m+N/2)
        for i,x in enumerate(ids):
            for u in range(N):
                for v in range(u+1,N):
                    if ((x>>u)^(x>>v))&1:
                        y=x^(1<<u)^(1<<v)
                        A[i,pos[y]]=1
        w,V=eigh(A,check_finite=False)
        proj={}
        for j2 in range(0 if N%2==0 else 1,N+1,2):
            j=j2/2
            indices=np.where(np.abs(w-j*(j+1))<1e-7)[0]
            if len(indices):proj[j]=V[:,indices]@V[:,indices].T
        assert np.max(np.abs(sum(proj.values())-np.eye(dim)))<1e-10
        blocks.append((ids,m,proj))
    return blocks

def p_j(j,nu,t):
    ms=np.arange(-j,j+1,1);d=len(ms);Q=np.zeros((d,d))
    for i,m in enumerate(ms):
        down=(nu+1)*(j+m)*(j-m+1)
        up=nu*(j-m)*(j+m+1)
        Q[i,i]=-(down+up)
        if i>0: Q[i-1,i]=down
        if i<d-1: Q[i+1,i]=up
    return expm(Q*t)@np.ones(d)/d

def build_rho(N,nu,t,blocks):
    n=1<<N;rho=np.zeros((n,n));curves={}
    for ids,m,projs in blocks:
        ind=np.ix_(ids,ids);block=np.zeros((len(ids),len(ids)))
        for j,P in projs.items():
            if j not in curves: curves[j]=p_j(j,nu,t)
            v=curves[j][round(m+j)]*(2*j+1)/(2**N)
            block+=v*P
        rho[ind]=block
    return rho

def ppt_min(rho,N):
    d=1<<(N-1)
    # reorder first qubit high order; reshaping to block and swapping row/col first-qubit
    PT=rho.reshape(2,d,2,d).transpose(2,1,0,3).reshape(rho.shape)
    return np.linalg.eigvalsh(PT)[0]

def witness_margin(rho,N):
    m=np.array([i.bit_count()-N/2 for i in range(1<<N)])
    M=-(m@np.diag(rho))
    return float(M*M-N/4)

if __name__=='__main__':
    for N in [2,3,4,5,6,7,8]:
        blocks=make_projectors(N)
        nu=.20
        vals=[]
        for t in [0,.01,.03,.1,.3,1,2,5,10,20]:
            rho=build_rho(N,nu,t,blocks)
            ev=ppt_min(rho,N)
            w=witness_margin(rho,N)
            vals.append((t,round(ev,10),round(w,5)))
        print('N=',N,'nu=',nu,vals,flush=True)

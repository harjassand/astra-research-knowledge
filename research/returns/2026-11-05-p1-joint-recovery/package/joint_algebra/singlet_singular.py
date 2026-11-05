import numpy as np, itertools, math, json, sys, os
from scipy.linalg import svdvals

def schur(n):
    # Twice-spin and twice-magnetic quantum numbers.
    states={(0,()): {0: np.ones(1)}}
    for k in range(n):
        nxt={}
        for (jj,path),ms in states.items():
            j=jj/2
            for JJ in (jj+1,jj-1):
                if JJ<0:continue
                J=JJ/2; nd={}
                for MM in range(-JJ,JJ+1,2):
                    M=MM/2; v=np.zeros(2**(k+1))
                    for spin in (1,-1):
                        mm=MM-spin
                        if mm not in ms:continue
                        if JJ==jj+1:co=math.sqrt((j+spin*M+.5)/(2*j+1))
                        else:co=(-1 if spin==1 else 1)*math.sqrt((j-spin*M+.5)/(2*j+1))
                        v[(0 if spin==1 else 1)::2]+=co*ms[mm]
                    nd[MM]=v
                nxt[(JJ,path+(JJ,))]=nd
        states=nxt
    groups={}
    for (jj,path),ms in states.items():groups.setdefault(jj,[]).append(np.stack([ms[m] for m in sorted(ms)],axis=1))
    return groups

def basis(n):
    groups=schur(n); arr=[]
    for jj,ws in groups.items():
        for a in ws:
            for b in ws:arr.append((a@b.T)/math.sqrt(jj+1))
    return np.array(arr)

def gateU(n,theta):
    dim=2**(n+1);U=np.eye(dim,dtype=complex);c=np.cos(theta);s=np.sin(theta)
    nums=np.arange(dim)
    for j in range(1,n+1):
        a=n;b=n-j
        flips=((nums>>a)^(nums>>b))&1
        perm=nums^(flips<<a)^(flips<<b)
        U=c*U+1j*s*U[perm]
    return U

def singlet_T(n,theta,B=None):
    if B is None:B=basis(n)
    d=2**n;U=gateU(n,theta).reshape(2,d,2,d)
    out=np.zeros_like(B,dtype=complex)
    for a in range(2):
        for b in range(2):
            K=U[a,:,b,:]
            out+=(K@B@K.conj().T)/2
    T=np.einsum('ijk,ljk->il',B.conj(),out,optimize=True)
    return T
if __name__=='__main__':
    ns=range(2,8) if len(sys.argv)==1 else [int(sys.argv[1])]
    for n in ns:
        B=basis(n)
        for th in (.03,.1,.3,.7,1.2):
            T=singlet_T(n,th,B); ss=svdvals(T);gap=1-ss[1]**2
            rec=dict(n=n,theta=th,invariant_dim=len(B),gap=float(gap),ratio_theta4=float(gap/th**4),normal_defect=float(np.linalg.norm(T@T.conj().T-T.conj().T@T)))
            print(json.dumps(rec),flush=True)

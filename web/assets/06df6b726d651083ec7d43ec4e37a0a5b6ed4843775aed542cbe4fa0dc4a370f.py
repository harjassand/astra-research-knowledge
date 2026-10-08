import numpy as np
from scipy.linalg import eigh
rng=np.random.default_rng(2219)
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex); I=np.eye(2)
v=np.array([0,1,-1,0])/np.sqrt(2); S=np.outer(v,v)
def invroot(x):
    val,vec=np.linalg.eigh((x+x.conj().T)/2)
    return (vec/np.sqrt(val))@vec.conj().T

def pt(x): return x.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
def channel(ks,x):return sum(k@x@k.conj().T for k in ks)
def sinkhorn(ks):
    A=I.copy(); B=I.copy(); ls=ks.copy()
    for j in range(2000):
        a=invroot(channel(ls,I)); ls=np.array([a@x for x in ls]); A=a@A
        b=invroot(sum(x.conj().T@x for x in ls)); ls=np.array([x@b for x in ls]); B=B@b
        err=np.linalg.norm(channel(ls,I)-I)
        if err<1e-12: return A,B,ls,err,j
    raise RuntimeError(err)
worst=0; pairMismatch=0
for n in range(50):
    z=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2)); q=np.linalg.qr(z)[0]; ks=q.reshape(4,2,2)
    A,B,ls,err,j=sinkhorn(ks)
    T=np.array([[np.trace(p@channel(ls,q)).real/2 for q in P] for p in P]); s=np.sum(T*T)
    pairout=channel([np.kron(a,b) for a in ks for b in ks],S)
    inv_id=np.kron(B,B)@S@np.kron(B,B).conj().T-abs(np.linalg.det(B))**2*S
    out2=channel([np.kron(a,b) for a in ls for b in ls],S)
    congr=abs(np.linalg.det(B))**2*np.kron(A,A)@pairout@np.kron(A,A).conj().T
    worst=max(worst,np.linalg.norm(inv_id),np.linalg.norm(out2-congr))
    e=np.linalg.eigvalsh(pt(pairout)).min()
    pairMismatch+= (e<-1e-8)!=(s>1+1e-8)
print({'identity_error':worst,'pair_mismatches':pairMismatch})

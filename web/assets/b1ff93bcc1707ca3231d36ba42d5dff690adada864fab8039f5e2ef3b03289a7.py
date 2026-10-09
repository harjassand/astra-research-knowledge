"""Diagnostic dual/witness check for the general-channel conjecture. No certification."""
import numpy as np
from support_witness_probe import fisher

def phi(y,lam):
    d=y.shape[0]
    return lam*y+(1-lam)*np.trace(y)*np.eye(d)/d

def apply_blocks(a,n,d,lam):
    # a consists of n-by-n blocks of size d; the same code allows rectangular arrays.
    nr=a.shape[0]//d; nc=a.shape[1]//d
    return np.block([[phi(a[i*d:(i+1)*d,j*d:(j+1)*d],lam) for j in range(nc)] for i in range(nr)])

def ptrace_blocks(a,d):
    nr=a.shape[0]//d;nc=a.shape[1]//d
    return np.array([[np.trace(a[i*d:(i+1)*d,j*d:(j+1)*d]) for j in range(nc)] for i in range(nr)])

def rld(a,b):return np.trace(b.conj().T@np.linalg.pinv(a,rcond=1e-12)@b).real

def witness(lam=.5,d=2):
    fs=[]
    for i in range(d):
        for j in range(d):
            f=np.zeros((d,d));f[i,j]=1;fs.append(f)
    n=d*d
    et=1-d**3/(1/((1+(d*d-1)*lam)/d)+(d*d-1)/((1-lam)/d))
    # Simplified qubit formula: 3 lambda^2/(1+2 lambda).
    alpha=(1-et)*np.array([np.trace(f)/d for f in fs])
    aa=np.vstack([phi(f,lam) for f in fs])
    gg=np.block([[phi(f@g.conj().T,lam) for g in fs] for f in fs])
    ac=aa-np.kron(alpha[:,None],np.eye(d))
    dd=et*gg-ac@ac.conj().T
    ev,vec=np.linalg.eigh(dd)
    ker=vec[:,np.abs(ev)<1e-9]
    c=ker@ker.conj().T/ker.shape[1]
    b=c@ac
    trb=ptrace_blocks(b,d)
    print('eta',et,'defect eigenvalues',ev,'kernel dim',ker.shape[1],flush=True)
    print('partial trace b norm',np.linalg.norm(trb),'Cr eigenvalues',np.linalg.eigvalsh(ptrace_blocks(c,d)),flush=True)
    nc=apply_blocks(c,n,d,lam);nb=apply_blocks(b,n,d,lam)
    print('RLD ratio',rld(nc,nb)/rld(c,b),'input metric',rld(c,b),flush=True)
    # Normalize b so Tr b^*c^+b=1; the block positive matrix then has trace 2.
    b=b/np.sqrt(rld(c,b));small=b.conj().T@np.linalg.pinv(c,rcond=1e-12)@b
    tau=np.eye(d)/d
    for p,s in [(1e-2,1e-5),(1e-3,1e-7),(1e-4,1e-9)]:
        base=np.block([[(1-s)*c,np.sqrt(s*(1-s))*b],[np.sqrt(s*(1-s))*b.conj().T,s*small]])
        rare=np.zeros_like(base);rare[-d:,-d:]=tau
        rho=(1-p)*base+p*rare;dx=rare-base
        out=apply_blocks(rho,n+1,d,lam);do=apply_blocks(dx,n+1,d,lam)
        ref=ptrace_blocks(rho,d);dr=ptrace_blocks(dx,d)
        gi=fisher(rho,dx)-fisher(ref,dr)
        go=fisher(out,do)-fisher(ref,dr)
        print('p,s',p,s,'conditional BKM ratio',go/gi,flush=True)
    return c,b,small,et

if __name__=='__main__':
    c,b,dd,eta=witness()
    np.savez(__file__.replace('.py','.npz'),c=c,b=b,d=dd,eta=eta)

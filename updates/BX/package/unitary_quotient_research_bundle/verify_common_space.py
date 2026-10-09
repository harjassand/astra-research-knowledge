import numpy as np, json
rng=np.random.default_rng(82345)
def unitary(n):
    Q,R=np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))
    return Q@np.diag(np.diag(R)/abs(np.diag(R))).conj()
results=[]
for n,D,r in [(5,6,4),(8,7,6),(10,10,9),(20,23,19),(4,4,4),(10,6,5)]:
    a,b=n-r,D-r; ell=n+b; worst=-1e9; uniterr=0
    for trial in range(20):
        Bn,BD=unitary(n),unitary(D)
        w=BD[:,:r]@Bn[:,:r].conj().T
        E=np.zeros((ell,D),complex);E[:n,:r]=Bn[:,:r];E[n:,r:]=np.eye(b)
        J=E@BD.conj().T
        rho=unitary(D)
        sigma=J@rho@J.conj().T+np.eye(ell)-J@J.conj().T
        P=np.eye(n)[:,rng.permutation(n)]
        Pext=np.eye(ell);Pext[:n,:n]=P
        A=w.conj().T@rho@w
        lhs=np.linalg.norm(sigma-Pext)**2
        rhs=np.linalg.norm(A-P)**2+3*a+6*b
        worst=max(worst,lhs-rhs)
        uniterr=max(uniterr,np.linalg.norm(sigma@sigma.conj().T-np.eye(ell)))
    assert worst<1e-9 and uniterr<1e-9
    results.append({'n':n,'D':D,'r':r,'trials':20,'worst_bound_residual':worst,'max_unitarity_error':uniterr})
print(json.dumps(results,indent=2))

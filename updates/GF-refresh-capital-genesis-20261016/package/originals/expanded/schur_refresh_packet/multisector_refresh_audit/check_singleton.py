import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(72026)
err=0.0
for K in [1,2,3,7]:
    for _ in range(100):
        p,q,eta=rng.random(3)
        lam=eta+(1-eta)/K
        c=min(1,eta*np.sqrt((1-p)*(1-q)/(p*q))/lam)
        n=K+2
        u=np.eye(n)[:,0]
        v=np.r_[0,np.ones(K)/np.sqrt(K),0]
        sink=np.eye(n)[:,-1]
        w=c*v+np.sqrt(1-c*c)*sink
        A=np.outer(u,v)+np.outer(v,u)
        B=np.outer(u,w)+np.outer(w,u)
        psi=expm(-1j*np.arcsin(np.sqrt(p))*A)@u
        rho=np.outer(psi,psi.conj())
        pinch=np.zeros_like(rho)
        blocks=[[0],[1,K+1]]+[[j] for j in range(2,K+1)]
        for block in blocks:
            pinch[np.ix_(block,block)]=rho[np.ix_(block,block)]
        rho=eta*rho+(1-eta)*pinch
        U=expm(-1j*np.arcsin(np.sqrt(q))*B)
        actual=1-(U@rho@U.conj().T)[0,0].real
        formula=p+q-p*q-p*lam*q*c*c+2*eta*np.sqrt(p*q*(1-p)*(1-q))*c
        err=max(err,abs(actual-formula))
assert err<1e-12
print('400 direct channel witnesses; maximum absolute formula error:',err)

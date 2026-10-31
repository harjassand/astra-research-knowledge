"""Exact Gaussian cross-density evolution for quadratic branch Hamiltonians.

Each block sigma_ij obeys -i(H_i sigma-sigma H_j)+common linear Lindblad.
The complex Gaussian Wigner covariance closes under a Riccati equation.
An optional commuting coordinate records an integrated homodyne output.
"""
import numpy as np
from scipy.integrate import solve_ivp


def symplectic(modes):
    return np.kron(np.eye(modes),np.array([[0.,1.],[-1.,0.]]))


def cross_rhs(V,m,logw,Gleft,Gright,dleft,dright,hleft,hright,
              Omega,Aextra,Dextra,Q=None,qconstant=0.0):
    """Inputs may have a leading batch axis. Q is no-click sum L†L Hessian."""
    DG=Gleft-Gright
    Dh=hleft-hright
    if Q is not None:
        DG=DG-1j*Q
        Dh=Dh-1j*qconstant
    dd=dleft-dright
    A=Omega@((Gleft+Gright)/2)+Aextra
    v=(Omega@((dleft+dright)/2)[...,None])[...,0]
    D=Dextra+0.25j*(Omega.T@DG@Omega)
    VDG=V@DG
    dV=A@V+V@np.swapaxes(A,-1,-2)+D-1j*VDG@V
    dm=(A@m[...,None])[...,0]+v-1j*(V@(DG@m[...,None]+dd[...,None]))[...,0]
    dl=-1j*(0.5*np.einsum('...i,...ij,...j->...',m,DG,m)
             +0.5*np.einsum('...ij,...ji->...',DG,V)
             +np.einsum('...i,...i->...',dd,m)+Dh)
    return dV,dm,dl


def integrate_small(G1,G2,d1,d2,h1,h2,gamma,heat,T,nojump=False):
    n=len(d1); O=symplectic(n//2)
    Aextra=np.eye(n)*((-gamma+heat)/2 if not nojump else heat/2)
    Dextra=np.eye(n)*(gamma+heat)/2 if not nojump else np.eye(n)*heat/2
    Q=np.eye(n)*gamma if nojump else None
    qc=-gamma*n/4 if nojump else 0.
    initial=np.r_[np.eye(n).ravel()/2,np.zeros(n),0.].astype(complex)
    def fun(t,y):
        V=y[:n*n].reshape(n,n); m=y[n*n:n*n+n]
        a,b,c=cross_rhs(V,m,y[-1],G1,G2,d1,d2,h1,h2,O,Aextra,Dextra,Q,qc)
        return np.r_[a.ravel(),b,c]
    sol=solve_ivp(fun,[0,T],initial,rtol=2e-11,atol=2e-12)
    y=sol.y[:,-1]
    return y[:n*n].reshape(n,n),y[n*n:n*n+n],np.exp(y[-1])


def validation():
    from scipy import sparse as sp
    from scipy.sparse.linalg import expm_multiply
    N=24; gamma=.7; heat=.002; T=2.1
    b=sp.diags(np.sqrt(np.arange(1,N)),1,shape=(N,N),format='csr')
    q=(b+b.conj().T)/np.sqrt(2);p=(b-b.conj().T)/(1j*np.sqrt(2))
    rs=[q,p];eye=sp.eye(N,format='csr')
    G1=np.array([[.21,.07],[.07,.09]])
    G2=np.array([[-.08,.03],[.03,.13]])
    d1=np.array([.31,-.22]); d2=np.array([-.17,.08])
    h1,h2=.13,-.09
    def H(G,d,h):
        out=h*eye
        for i in range(2):
            out=out+d[i]*rs[i]
            for j in range(2):out=out+.25*G[i,j]*(rs[i]@rs[j]+rs[j]@rs[i])
        return out
    H1,H2=H(G1,d1,h1),H(G2,d2,h2)
    result=[]
    for nojump in (False,True):
        L=-1j*(sp.kron(eye,H1)-sp.kron(H2.T,eye))
        for J,retain in [(np.sqrt(gamma)*b,not nojump),(np.sqrt(heat)*b.conj().T,True)]:
            Q=J.conj().T@J
            L+=(-.5*sp.kron(eye,Q)-.5*sp.kron(Q.T,eye))
            if retain:L+=sp.kron(J.conj(),J)
        rho=np.zeros((N,N),complex);rho[0,0]=1
        rho=expm_multiply(L*T,rho.reshape(-1,order='F')).reshape((N,N),order='F')
        tr=np.trace(rho)
        mf=np.array([np.trace(r@rho)/tr for r in rs])
        Vf=np.array([[np.trace((r@s+s@r)@rho)/(2*tr)-mf[i]*mf[j]
                      for j,s in enumerate(rs)] for i,r in enumerate(rs)])
        V,m,w=integrate_small(G1,G2,d1,d2,h1,h2,gamma,heat,T,nojump)
        result.append({'no_click':nojump,'trace_error':float(abs(w-tr)),
                       'mean_error':float(np.max(abs(m-mf))),
                       'covariance_error':float(np.max(abs(V-Vf)))})
    return result


if __name__=='__main__':
    import json
    print(json.dumps(validation(),indent=2))

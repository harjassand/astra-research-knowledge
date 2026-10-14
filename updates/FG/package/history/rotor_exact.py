"""Nonperturbative TWO-MANIFOLD rotor reference. Not a complete CaOH+ forecast."""
import numpy as np
from scipy.linalg import eigh
from rotor_probe import rotor_blocks,theta_from_fluence,free,NU,B,sigma_t
from scipy import constants as c

def pulse_parts(e,plus,theta,steps=160):
    # Remove finite-bandwidth factor from rotor_probe; build genuine angular dipole.
    dp=plus.toarray()
    delta=e[:,None]-e[None,:]
    mask=abs(dp)>0
    dp[mask]/=np.exp(-(2*np.pi*c.c*100*delta[mask]*sigma_t)**2)
    D=dp+dp.conj().T
    lam,V=eigh(D)
    h0=2*np.pi*c.c*100*e
    tmax=8*sigma_t; dt=2*tmax/steps
    half=np.exp(-.5j*h0*dt)
    U=np.eye(len(e),dtype=complex)
    for t in np.linspace(-tmax+dt/2,tmax-dt/2,steps):
        a=theta/(2*np.sqrt(np.pi)*sigma_t)*np.exp(-t*t/(4*sigma_t*sigma_t))
        U=half[:,None]*(V @ (np.exp(-.5j*a*dt*lam)[:,None]*(V.conj().T @ (half[:,None]*U))))
    # Scattering operator relative to free propagation at pulse centre.
    end=np.exp(1j*h0*tmax)
    U=end[:,None]*U*end[None,:]
    n=len(e)//2
    parts={i:np.zeros_like(U) for i in [-1,0,1]}
    parts[0][:n,:n]=U[:n,:n];parts[0][n:,n:]=U[n:,n:]
    parts[1][n:,:n]=U[n:,:n]; parts[-1][:n,n:]=U[:n,n:]
    return parts,U

def fourier_map(K,parts,ell,q,s):
    out=np.zeros_like(K)
    for m in [-1,0,1]:
        n=m-ell
        if n in parts:
            out+=np.exp(1j*(m+n)*q*s/2)*(parts[m]@K@parts[n].conj().T)
    return out

def build_model(jmax=60,center=NU,B1=B,theta=None,steps=160):
    if theta is None:theta=theta_from_fluence(275)
    model=[]; p=0.
    for e,dp,dm,rho,n in rotor_blocks(jmax,center,B1):
        parts,U=pulse_parts(e,dp,theta,steps)
        rho1=U@rho@U.conj().T;p+=np.trace(rho1[n:,n:]).real
        model.append((e,parts,rho))
    return model,p

def signal(model,T=1.,t1=1.,t3=1.,q=(1,1,1,1),s=.702):
    groups=np.zeros(2,dtype=complex)
    for e,parts,rho in model:
        K=free(fourier_map(rho,parts,-1,q[0],s),e,t1)
        Ks=[parts[1]@K@parts[0].conj().T,parts[0]@K@parts[-1].conj().T]
        for a,K2 in enumerate(Ks):
            K2=free(K2,e,T)
            K3=free(fourier_map(K2,parts,1,q[2],s),e,t3)
            K4=fourier_map(K3,parts,-1,q[3],s)
            groups[a]+=np.trace(K4)
    return np.sum(groups*np.exp(1j*q[1]*s/2*np.array([1,-1]))),groups

if __name__=='__main__':
    import time
    start=time.time();model,p=build_model(jmax=60)
    print('build secs',time.time()-start,'single pulse p',p)
    for T in [0.8,1.,2.,5.,10.]:
        print(T,signal(model,T=T))
    print('total secs',time.time()-start)

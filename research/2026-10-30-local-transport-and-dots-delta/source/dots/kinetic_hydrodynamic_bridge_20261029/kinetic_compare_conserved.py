"""Positive local collision + spectral advection Strang comparator.
Finite grid/time approximation, not a certified PDE result.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator
from scipy.special import logsumexp
from math import sqrt,log
import json,time
nu=1/12;gamma=sqrt(2)/4;c=sqrt(2/3)

def collide(f,dt):
    rho=f.sum(axis=0);j=f[2]-f[0];g=f[0]+f[2]
    disc=np.sqrt(4*rho*rho-3*j*j)
    low=(4*rho-disc)/3;R=2*disc/3;y=g-low;e=np.exp(-disc*dt)
    gn=low+y*e/(1-y/R*(1-e))
    return np.array([(gn-j)/2,rho-gn,(gn+j)/2])
def speed(rho,j):
    d=np.sqrt(4*rho*rho-3*j*j);gp=(4-4*rho/d)/3;gj=j/d
    return (gj+np.sqrt(gj*gj+4*gp))/2

def run(k,delta,N,dt):
    phase=2*np.pi*np.arange(N)/N;rho=1+sqrt(3)*delta*np.cos(phase)
    # Exact right simple-wave initial curve for the nonlinear equilibrium Euler flux.
    rrlo=1-sqrt(3)*delta;rrhi=1+sqrt(3)*delta
    solp=solve_ivp(lambda r,j:[speed(r,j[0])],(1,rrhi),[0.],rtol=1e-11,atol=1e-12,dense_output=True)
    solm=solve_ivp(lambda r,j:[speed(r,j[0])],(1,rrlo),[0.],rtol=1e-11,atol=1e-12,dense_output=True)
    j=np.where(rho>=1,solp.sol(rho)[0],solm.sol(rho)[0]);g=(4*rho-np.sqrt(4*rho*rho-3*j*j))/3
    f=np.array([(g-j)/2,rho-g,(g+j)/2]);initial_mean=f.mean(axis=1)
    t=6*log(2)/k**2;steps=int(np.ceil(t/dt));dt=t/steps
    modes=np.fft.fftfreq(N,d=1/N)*k
    adv=np.exp(-1j*np.outer([-1,0,1],modes)*dt)
    f=collide(f,dt/2)
    minimum=1.;start=time.perf_counter()
    for z in range(steps):
        f=np.fft.ifft(np.fft.fft(f,axis=1)*adv,axis=1).real
        f=collide(f,dt if z<steps-1 else dt/2)
        minimum=min(minimum,float(f.min()))
    # periodic Burgers Fourier heat solution with uniform phase quadrature
    A=gamma*delta/(2*nu*k);T=nu*k*k*t
    M=max(4096,int(64*sqrt(max(A,1))));th=2*np.pi*np.arange(M)/M
    w=np.exp(-A*(1+np.sin(th)));wcoeff=np.fft.fft(w)
    mm=np.fft.fftfreq(M,d=1/M);heat=wcoeff*np.exp(-T*mm*mm)
    jbar=initial_mean[2]-initial_mean[0]
    cbar=speed(1,jbar)
    ys=(phase-cbar*k*t)%(2*np.pi)
    psi=np.array([np.sum(heat*np.exp(1j*mm*y)).real/M for y in ys])
    deriv=np.array([np.sum(1j*mm*heat*np.exp(1j*mm*y)).real/M for y in ys])
    ub=-2*nu*k/gamma*deriv/psi
    u=(f.sum(axis=0)-1)/sqrt(3)
    # unknown mean shift of simple-wave momentum retained; not fitted away.
    return {'k':k,'delta':delta,'cells':N,'dt':dt,'steps':steps,'time':t,'runtime_seconds':time.perf_counter()-start,'min_density_component':minimum,'known_mean_momentum':float(jbar),'conserved_background_speed':float(cbar),'kinetic_max_u_over_k':float(np.max(abs(u))/k),'burgers_max_u_over_k':float(np.max(abs(ub))/k),'max_difference_over_k':float(np.max(abs(u-ub))/k),'relative_L2_error':float(np.linalg.norm(u-ub)/np.linalg.norm(u)),'mass_error':float(abs(f.sum(axis=0).mean()-1)),'momentum_error':float(abs((f[2]-f[0]).mean()-(initial_mean[2]-initial_mean[0])))}
if __name__=="__main__":
 print(json.dumps([run(.1,.05,256,.2),run(.03,.05,512,.2),run(.03,.05,512,.1),run(.01,.05,512,.2)],indent=2))

#!/usr/bin/env python3
"""Exact mirror-symmetric four-internal-mode temporal echo and its sparse inverse control.

Independent radiation ODE + forward Schrödinger propagation. Numerical results
are diagnostics; the algebraic synthesis and terminal radiation cancellation
are proved in companion markdown file.
"""
import os,json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre, betainc, beta

T=12.0; tau=0.5; alpha=0.16; eta=float(os.environ.get("ASTRA_ECHO_ETA","0.01")); cutoff=12.0; mu=2*np.pi
N=40
wx, wt0=roots_legendre(N); w=.5*cutoff*(wx+1); wt=.5*cutoff*wt0
v=eta*np.sqrt(w)*(1-w/cutoff)**2
x=np.array([-tau,0,tau]); freq=np.tile(w,2)
Wfull=np.vstack([np.sqrt(wt)[:,None]*v[:,None]*np.exp(1j*sgn*w[:,None]*x[None,:]) for sgn in (+1,-1)])
W=np.column_stack(((Wfull[:,0]+Wfull[:,2])/np.sqrt(2), Wfull[:,1]))
start=tau; end=T-tau; L=end-start

def bump(t):
    if t <=start or t>=end: return 0.,0.
    u=(t-start)/L; p=4*u*(1-u)
    return p**3,(12./L)*p*p*(1-2*u)

def h_hprime(t):
    a,ap=bump(t); b,bp=bump(t-tau); c,cp=bump(t+tau)
    return alpha*np.array([np.sqrt(2)*a,b+c]), alpha*np.array([np.sqrt(2)*ap,bp+cp])

def q(t):
    h,_=h_hprime(t)
    return 1j*np.exp(-1j*mu*t)*h

def rrhs(t,xi): return -1j*(freq*xi+W@q(t))
rad_sol=solve_ivp(rrhs,(0,T),np.zeros(len(freq),complex),method='DOP853',rtol=5e-12,atol=1e-14,max_step=.04,dense_output=True)
assert rad_sol.success
I=L*4**6*beta(7,7)

def theta(t):
    if t<=start:return 0.,0.
    if t>=end:return np.pi/2,0.
    u=(t-start)/L; f,_=bump(t)
    return np.pi/2*betainc(7,7,u), np.pi/2*f*f/I

# H=mu I_4 + [[0,C],[C.T,Q]]. The outer parity emitter couples
# to both stores by C[:,0]; the center couples by C[:,1].
def state_controls(t):
    xi=rad_sol.sol(t)
    xid=rrhs(t,xi)
    h,hp=h_hprime(t)
    rho2=1.-np.vdot(xi,xi).real-np.dot(h,h)
    assert rho2>.7, (t,rho2)
    rho=np.sqrt(rho2)
    rhop=-(np.vdot(xi,xid).real+np.dot(h,hp))/rho
    th,thp=theta(t)
    direction=np.array([np.cos(th),np.sin(th)])
    tangent=np.array([-np.sin(th),np.cos(th)])
    r=rho*direction; rp=rhop*direction+rho*thp*tangent
    g=np.exp(1j*mu*t)*(W.conj().T@xi)
    y=-hp-g.real; z=-g.imag
    C=np.zeros((2,2)); Q=np.zeros((2,2))
    if h[1] > 1.e-15:
        # 'outer' column is parallel to r; second solves storage transport.
        C[:,0]=y[0]*r/np.dot(r,r)
        C[:,1]=(rp-C[:,0]*h[0])/h[1]
        # One off-diagonal emitter link plus one center onsite control.
        Q[0,1]=Q[1,0]=z[0]/h[1]
        Q[1,1]=(z[1]-Q[0,1]*h[0])/h[1]
    Hcorr=np.zeros((4,4));Hcorr[:2,2:]=C;Hcorr[2:,:2]=C.T;Hcorr[2:,2:]=Q
    H=mu*np.eye(4)+Hcorr
    u=np.r_[np.exp(-1j*mu*t)*r,1j*np.exp(-1j*mu*t)*h]
    udot=np.r_[np.exp(-1j*mu*t)*(rp-1j*mu*r),np.exp(-1j*mu*t)*(mu*h+1j*hp)]
    src=np.r_[np.zeros(2,complex),W.conj().T@xi]
    residual=np.linalg.norm(1j*udot-H@u-src)
    compat=np.dot(r,rp)-np.dot(h,y)
    return u,xi,H,C,Q,residual,compat

schur=W.conj().T@(W/freq[:,None]);posadd=np.zeros((4,4),complex);posadd[2:,2:]=schur
records=[]
for t in np.linspace(0,T,901):
    u,xi,H,C,Q,res,compat=state_controls(t)
    records.append([t,np.linalg.eigvalsh(H-posadd)[0],res,compat,np.max(abs(C)),np.max(abs(Q)),np.linalg.norm(H-mu*np.eye(4),2),np.linalg.norm(xi),np.linalg.norm(u[2:])])
records=np.array(records)

def full_rhs(t,psi):
    _,_,H,*_=state_controls(t)
    u=psi[:4];xi=psi[4:]
    return np.r_[-1j*(H@u+np.r_[np.zeros(2,complex),W.conj().T@xi]),-1j*(freq*xi+W@u[2:])]
psi0=np.zeros(4+len(freq),complex);psi0[0]=1
sol=solve_ivp(full_rhs,(0,T),psi0,method='DOP853',rtol=5e-11,atol=5e-13,max_step=.034)
assert sol.success
want=np.zeros_like(psi0);want[1]=np.exp(-1j*mu*T)
output={
 'parameters':dict(T=T,tau=tau,alpha=alpha,eta=eta,cutoff=cutoff,mu=float(mu),N=N),
 'active_internal_modes':4,
 'storage_emitter_link_controls':4,
 'emitter_emitter_link_controls':1,
 'emitter_energy_control':1,
 'max_controls':dict(max_storage_hopping=float(records[:,4].max()),max_reactive_coupling=float(records[:,5].max()),max_internal_correction_norm=float(records[:,6].max())),
 'checks':dict(min_sampled_schur_margin=float(records[:,1].min()),max_equation_residual=float(records[:,2].max()),max_compatibility_error=float(abs(records[:,3]).max()),max_transient_radiation_norm=float(records[:,7].max()),max_emitter_norm=float(records[:,8].max()),final_radiation_norm=float(np.linalg.norm(rad_sol.sol(T))),full_transfer_error=float(np.linalg.norm(sol.y[:,-1]-want)),norm_final=float(np.linalg.norm(sol.y[:,-1]))),
 'interval_endpoints': {str(t):{'C':state_controls(t)[3].tolist(),'Q':state_controls(t)[4].tolist()} for t in [0,.01,.5,1.,3.,6.,9.,11.5,11.99,12.]}
}
with open(os.environ.get('ASTRA_ECHO_OUT','/mnt/data/astra_spatiotemporal_sparse_echo_results.json'),'w') as f:json.dump(output,f,indent=2)
print(json.dumps({k:v for k,v in output.items() if k!='interval_endpoints'},indent=2))

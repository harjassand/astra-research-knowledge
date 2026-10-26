#!/usr/bin/env python3
"""Constructive 3-emitter time-delayed echo with purely real symmetric internal H.
Full waveguide (two outgoing ports) remains complex due to propagation phases.
Includes 2 storage modes, no direct storage-to-storage hopping.
Source real-envelope carrier mu*tau is an odd multiple of pi.
"""
import json,numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre,betainc,beta
T=12.;tau=.5;alpha=.16; eta=.01;cutoff=12.;mu=2*np.pi;N=40
x=np.array([-tau,0,tau]);wn,wt=roots_legendre(N);w=.5*cutoff*(wn+1); wt=.5*cutoff*wt
v=eta*np.sqrt(w)*(1-w/cutoff)**2
W=np.vstack([np.sqrt(wt)[:,None]*v[:,None]*np.exp(1j*sgn*w[:,None]*x[None,:]) for sgn in (+1,-1)])
freq=np.tile(w,2)
start=tau;end=T-tau;width=end-start

def bump(t):
    if t<=start or t>=end: return 0.,0.
    z=(t-start)/width; p=4*z*(1-z)
    return p**3, (12/width)*p*p*(1-2*z)

def h_hprime(t):
    f,fp=bump(t);l,lp=bump(t-tau);r,rp=bump(t+tau)
    # mu*tau=15*pi, so q2=-q1(t-tau)-q1(t+tau)=+i*alpha*carrier*(l+r)
    return (alpha*np.array([f,l+r,f]),alpha*np.array([fp,lp+rp,fp]))

def q_qdot(t):
    h,hp=h_hprime(t); phase=np.exp(-1j*mu*t)
    return 1j*phase*h,phase*(mu*h+1j*hp)

def rad_rhs(t,z):
    q,_=q_qdot(t)
    return -1j*(freq*z+W@q)
rad_sol=solve_ivp(rad_rhs,(0,T),np.zeros(len(freq),complex),method='DOP853',atol=1e-14,rtol=1e-12,max_step=.035,dense_output=True)
assert rad_sol.success
I=width*4**6*beta(7,7)
def theta(t):
    if t<=start:return 0.,0.
    if t>=end:return np.pi/2,0.
    z=(t-start)/width;f,_=bump(t)
    return np.pi/2*betainc(7,7,z), np.pi/2*f*f/I

def controls(t):
    rad=rad_sol.sol(t).reshape(-1); rd=rad_rhs(t,rad)
    h,hp=h_hprime(t)
    q,qd=q_qdot(t)
    norm2=1-np.vdot(rad,rad).real-np.dot(h,h)
    assert norm2>0.8
    rho=np.sqrt(norm2)
    rhodot=-(np.vdot(rad,rd).real+np.dot(h,hp))/rho
    th,td=theta(t)
    r=rho*np.array([np.cos(th),np.sin(th)])
    rprime=rhodot*np.array([np.cos(th),np.sin(th)])+rho*td*np.array([-np.sin(th),np.cos(th)])
    g=np.exp(1j*mu*t)*(W.conj().T@rad)
    # H_int=mu I + [[0,C],[C.T,Q]] with real C,Q and no a-b edge.
    y=-hp-g.real
    z=-g.imag
    Hcor=np.zeros((5,5),float)
    nh=np.linalg.norm(h)
    nr=np.linalg.norm(r)
    if nh>1e-15:
        # Required symmetric compatibility r.T @ rprime == h.T @ y.
        compat=float(np.dot(r,rprime)-np.dot(h,y))
        assert abs(compat)<3e-10, (t,compat)
        C=(np.outer(rprime,h)/nh**2
           +np.outer(r,y)/nr**2
           -(np.dot(r,rprime)/(nr**2*nh**2))*np.outer(r,h))
        Q=(np.outer(z,h)+np.outer(h,z))/nh**2 -np.dot(h,z)*np.outer(h,h)/(nh**4)
        Hcor[:2,2:]=C;Hcor[2:,:2]=C.T;Hcor[2:,2:]=Q
    H=mu*np.eye(5)+Hcor
    u=np.r_[np.exp(-1j*mu*t)*r,q]
    udot=np.r_[np.exp(-1j*mu*t)*(rprime-1j*mu*r),qd]
    source=np.r_[np.zeros(2,complex),W.conj().T@rad]
    residual=np.linalg.norm(H@u+source-1j*udot)
    return u,rad,H,residual,np.linalg.norm(Hcor,2),np.linalg.norm(Hcor[:2,2:],2)

Schur=W.conj().T@(W/freq[:,None]); posadd=np.zeros((5,5),complex);posadd[2:,2:]=Schur
checks=[]
for t in np.linspace(0,T,601):
    u,rad,H,res,Kn,Cn=controls(t)
    checks.append([t,np.linalg.eigvalsh(H-posadd)[0],res,Kn,Cn,np.linalg.norm(rad),np.linalg.norm(u[2:]),np.max(abs(H.imag)),abs(H[0,1])])
checks=np.array(checks)

def rhs(t,psi):
    u=psi[:5]; rad=psi[5:]
    _,_,H,*_=controls(t)
    return np.r_[-1j*(H@u+np.r_[np.zeros(2,complex),W.conj().T@rad]),-1j*(freq*rad+W@u[2:])]
psi0=np.zeros(5+len(freq),complex);psi0[0]=1
solution=solve_ivp(rhs,(0,T),psi0,method='DOP853',rtol=1e-11,atol=1e-13,max_step=.028)
assert solution.success
wanted=np.zeros(len(psi0),complex);wanted[1]=np.exp(-1j*mu*T)
results={'parameters':{'mu':mu,'tau':tau,'alpha':alpha,'eta':eta,'T':T,'each_waveguide_direction_modes':N},
'checks':{'max_internal_control_residual':float(max(checks[:,2])),'min_sampled_full_schur_margin':float(min(checks[:,1])),'max_internal_correction_norm':float(max(checks[:,3])),'max_storage_emitter_hopping':float(max(checks[:,4])),'max_radiative_amplitude':float(max(checks[:,5])),'final_radiation_norm':float(np.linalg.norm(rad_sol.sol(T))),'direct_storage_hopping_max':float(max(checks[:,-1])),'imag_internal_H_max':float(max(checks[:,-2])),'full_state_transfer_error':float(np.linalg.norm(solution.y[:,-1]-wanted)),'full_final_norm':float(np.linalg.norm(solution.y[:,-1]))},
'interpretation':'Constructed time-dependent real symmetric 5-mode internal H, no direct storage-storage edge; source coupling to continuum remains phase-dependent and frequency-dependent. Positivity sampled here; existence of uniform positive family for sufficiently large carrier follows if controls bounded with carrier. No physically local sparse implementation certified.'}
open('/mnt/data/astra_temporal_dark_inband_certified_20261027.json','w').write(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))

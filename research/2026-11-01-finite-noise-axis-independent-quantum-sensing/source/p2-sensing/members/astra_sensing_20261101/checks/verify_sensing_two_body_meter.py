"""Exact three-qubit verification of the finite two-body meter construction."""
import json
import numpy as np
from scipy.linalg import expm

I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.diag([1,-1]).astype(complex)

def kron3(a,b,c):
    return np.kron(np.kron(a,b),c)

ZS = kron3(Z,I,I)
ZA_XM = kron3(I,Z,X)
ZS_XM = kron3(Z,I,X)
CZ = np.diag([1,1,1,-1,1,1,1,-1]).astype(complex)

def liouvillian(h,j,gamma):
    return (-1j*(np.kron(np.eye(8),h)-np.kron(h.T,np.eye(8)))
            +gamma*(np.kron(j.conj(),j)-np.eye(64)))

def basis_data(r,z):
    a = 0 if z==1 else 1
    s = a if r==1 else 1-a
    return 2*s+a

def evolve_matrix(superop,rho):
    return (superop@rho.reshape(-1,order="F")).reshape((8,8),order="F")

def exact_kernel(gamma,theta,tau,dead,A,eps,omega=0.0,coherent_erase=True):
    j=kron3(np.cos(theta)*X+np.sin(theta)*Y,I,I)
    h=(A/tau)*ZS_XM+(np.pi/(4*tau))*ZA_XM+omega*ZS/2
    ea=expm(tau*liouvillian(h,j,gamma))
    ed=expm(dead*liouvillian(omega*ZS/2,j,gamma))
    # CZ can be performed over any nonzero part of 'dead': its generator
    # commutes with sensor signal/noise, so this ordering includes all deadtime.
    probabilities=np.zeros((2,2,2),complex) # observed u (+,-), final r, initial r
    coherences=np.zeros_like(probabilities)
    for ri,r in enumerate((1,-1)):
        dp,dn=basis_data(r,1),basis_data(r,-1)
        state=np.zeros((8,8),complex);state[2*dp,2*dp]=1
        cross=np.zeros((8,8),complex);cross[2*dp,2*dn]=1
        state=evolve_matrix(ea,state);cross=evolve_matrix(ea,cross)
        if coherent_erase:
            state=CZ@state@CZ
            cross=CZ@cross@CZ
        state=evolve_matrix(ed,state)
        cross=evolve_matrix(ed,cross)
        for rpi,rp in enumerate((1,-1)):
            fp,fn=basis_data(rp,1),basis_data(rp,-1)
            for ui,u in enumerate((1,-1)):
                for actual_m in (0,1):
                    actual_u=1 if actual_m==1 else -1
                    weight=1-eps if actual_u==u else eps
                    probabilities[ui,rpi,ri]+=weight*state[2*fp+actual_m,2*fp+actual_m]
                    frame=1 if coherent_erase else (-1)**actual_m
                    coherences[ui,rpi,ri]+=weight*frame*cross[2*fp+actual_m,2*fn+actual_m]
    return probabilities,coherences

def pmat(gamma,t):
    a=np.exp(-2*gamma*t)
    return np.array([[(1+a)/2,(1-a)/2],[(1-a)/2,(1+a)/2]])

def svalue(gamma,tau,A):
    lam=2*A/tau
    d=np.sqrt(complex(gamma*gamma-lam*lam))
    sh=tau if abs(d)<1e-12 else np.sinh(d*tau)/d
    return float(np.real(lam*np.exp(-gamma*tau)*sh))

def formula_kernel(gamma,tau,dead,A,eps):
    eta=1-2*eps
    s=svalue(gamma,tau,A)
    return np.stack([(pmat(gamma,tau+dead)+u*eta*s*pmat(gamma,dead)@np.diag([1,-1]))/2
                     for u in (1,-1)])

def coherence_formula(gamma,omega,tau,dead,A,eps):
    def tilted(w,t):
        return expm(t*np.array([[-gamma-1j*w,gamma],[gamma,-gamma+1j*w]]))
    lam=2*A/tau
    sine=(tilted(omega-lam,tau)-tilted(omega+lam,tau))/(2j)
    return np.stack([tilted(omega,dead)@(tilted(omega,tau)+u*(1-2*eps)*sine)/2
                     for u in (1,-1)])

def main():
    gl,gh,tau,dead,A,eps=.3,1.2,.5,.17,.6,.13
    errs=[];coherence_errs=[];deferred_errs=[]
    for gamma in (gl,gh):
        for theta in (.17,.88):
            for omega in (0.0,.73):
                actual,coh=exact_kernel(gamma,theta,tau,dead,A,eps,omega)
                expected=formula_kernel(gamma,tau,dead,A,eps)
                expected_coh=coherence_formula(gamma,omega,tau,dead,A,eps)
                delayed_p,delayed_c=exact_kernel(gamma,theta,tau,dead,A,eps,omega,coherent_erase=False)
                deferred_errs.extend([np.max(np.abs(delayed_p-actual)),np.max(np.abs(delayed_c-coh))])
                errs.append(np.max(np.abs(actual-expected)))
                for ri,r in enumerate((1,-1)):
                    for rpi,rp in enumerate((1,-1)):
                        phase=np.exp(1j*theta*(r-rp))
                        coherence_errs.append(np.max(np.abs(coh[:,rpi,ri]-expected_coh[:,rpi,ri]*phase)))
    transition=np.zeros((4,4))
    for j,gamma in enumerate((gl,gh)):
        kernels=formula_kernel(gamma,tau,dead,A,eps)
        for uj in (0,1):
            transition[2*uj:2*uj+2,2*j:2*j+2]=kernels[uj]
    system=np.vstack([transition-np.eye(4),np.ones(4)])
    rhs=np.array([0,0,0,0,1.])
    pi=np.linalg.lstsq(system,rhs,rcond=None)[0]
    duration=tau+dead
    ql,qh=[(1-np.exp(-2*g*duration))/2 for g in (gl,gh)]
    sl,sh=[svalue(g,tau,A) for g in (gl,gh)]
    bl,bh=[np.exp(-2*g*dead) for g in (gl,gh)]
    eta=1-2*eps
    Q=ql+qh
    D=eta*(sl*bl+sh*bh)/(2-eta**2*(sl*bl-sh*bh)*(sl*qh-sh*ql)/Q)
    ml,mh=pi[0]-pi[1],pi[2]-pi[3]
    v_numeric=(ml*ql/gl+mh*qh/gh)/duration
    v_formula=D*ql*qh*(1/gl-1/gh)/(duration*Q)
    pe_formula=(1+D*(qh-ql)/Q)/2
    report={
        "three_qubit_kernel_max_error":float(max(errs)),
        "reference_preserving_coherence_max_error":float(max(coherence_errs)),
        "deferred_frame_vs_coherent_erasure_max_error":float(max(deferred_errs)),
        "stationary_m_l_error":float(abs(ml-qh*D/Q)),
        "stationary_m_h_error":float(abs(mh+ql*D/Q)),
        "stationary_velocity_error":float(abs(v_numeric-v_formula)),
        "stationary_even_probability_error":float(abs(pi[0]+pi[2]-pe_formula)),
        "parameters":{"gamma_l":gl,"gamma_h":gh,"tau":tau,"deadtime":dead,"A":A,"readout_error":eps},
        "effective_D":float(D),"velocity":float(v_formula),"pi_even":float(pe_formula),
        "unheralded_local_information_coefficient":float((pe_formula*v_formula)**2),
    }
    error_keys=[k for k in report if "error" in k and isinstance(report[k],float)]
    report["passed"]=max(report[k] for k in error_keys)<1e-10
    print(json.dumps(report,indent=2))
    if not report["passed"]:raise SystemExit(1)

if __name__=="__main__":main()

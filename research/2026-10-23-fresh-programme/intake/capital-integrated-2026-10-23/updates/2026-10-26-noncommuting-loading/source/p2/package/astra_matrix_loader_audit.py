#!/usr/bin/env python3
"""Executed finite-dimensional checks of exact noncommuting matrix-valued loading,
scalar common-amplitude arc-length schedule, and failure of uniform gap after
adding a bare penalty. Nothing here proves a physical endpoint interface.
"""
import numpy as np, json
from scipy.linalg import qr, eigh, expm
from scipy.integrate import solve_ivp
from math import atan, tan, pi, sqrt

rng=np.random.default_rng(20261026)
def unitary(n):
    z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    q,r=qr(z)
    return q@np.diag(np.diag(r)/np.abs(np.diag(r)))

def model(n=6,d=3):
    B=1.5
    q=unitary(n)
    Q=q@np.diag(np.array([B*1.0,2.,3.5,6.,10.,16.][:n]))@q.conj().T
    u=unitary(n)[:,:d]
    w=unitary(d)
    lam=np.array([.025,1.5,60.][:d])
    L=w@np.diag(lam)@w.conj().T
    W=u@w@np.diag(np.sqrt(lam))@w.conj().T
    G=Q@W
    return B,Q,G,W,L,u,lam

def ramp(lam):
    """Exact schedule from integral of max_j sqrt(lambda)/(1+eta²lambda).
    Crossings for sorted positive lambda are at eta=(lambda_i*lambda_{i+1})^(-1/4).
    """
    ll=sorted([float(x) for x in lam if x>0],reverse=True)
    breaks=[0.]
    for i in range(len(ll)-1):
        cross=(ll[i]*ll[i+1])**(-.25)
        if 0 < cross < 1: breaks.append(cross)
    breaks.append(1.)
    breaks=sorted(set(breaks))
    seg=[];cum=[0.]
    for a,b in zip(breaks[:-1],breaks[1:]):
        m=(a+b)/2
        active=max(ll,key=lambda l:np.sqrt(l)/(1+l*m*m))
        delta=atan(b*sqrt(active))-atan(a*sqrt(active))
        seg.append((a,b,active,delta))
        cum.append(cum[-1]+delta)
    ell=cum[-1]
    def eta_at(s):
        if s<=0:return 0.
        if s>=1:return 1.
        target=s*ell
        idx=min(len(seg)-1,int(np.searchsorted(cum,target,side='right')-1))
        a,b,l,delta=seg[idx]
        return min(1.,max(0.,tan(atan(a*sqrt(l))+(target-cum[idx]))/sqrt(l)))
    return ell,eta_at,seg

def calculate():
    B,Q,G,W,L,U,lam=model()
    n,d=W.shape
    evals,S=eigh(L)
    J=U.conj().T@np.linalg.solve(Q,U)
    # U from model is a polar isometry; W columns rotate with eigenvectors of L.
    # check U U* polar: W=U sqrt(L)
    sq=S@np.diag(np.sqrt(evals))@S.conj().T
    polar=W@S@np.diag(1/np.sqrt(evals))@S.conj().T
    assert np.linalg.norm(polar.conj().T@polar-np.eye(d))<1e-12
    U=polar
    J=U.conj().T@np.linalg.solve(Q,U)
    noncomm=float(np.linalg.norm(J@L-L@J))
    ell,eta_at,seg=ramp(lam)
    sample=[]
    for s in [.01,.2,.5,.82,1.]:
        eta=eta_at(s)
        theta=np.arctan(eta*np.sqrt(evals))
        C=S@np.diag(np.cos(theta))@S.conj().T
        Sin=S@np.diag(np.sin(theta))@S.conj().T
        Tan=S@np.diag(np.tan(theta))@S.conj().T
        R=np.column_stack((U@Tan,np.eye(n)))
        AA=R.conj().T@Q@R
        V=np.vstack((C,-U@Sin))
        E=np.vstack((Sin,U@C))
        chiu=Sin@C@J@C
        chil=np.linalg.solve(Q,U)@C-U@Sin@Sin@J@C
        chi=np.vstack((chiu,chil))
        eig=eigh(AA,eigvals_only=True)
        sample.append(dict(s=s,eta=eta,kernel_residual=float(np.linalg.norm(AA@V)),
            isometry_residual=float(np.linalg.norm(V.conj().T@V-np.eye(d))),
            reduced_inverse_residual=float(np.linalg.norm(AA@chi-E)),
            orthogonality_residual=float(np.linalg.norm(V.conj().T@chi)),
            chi_norm=float(np.linalg.norm(chi,2)),positive_gap=float(eig[d])))

    # Exact coherent transport via finite-step midpoint unitary evolution for
    # first sub-block with moderate spectrum and a controlled ramp.
    B1,Q1,G1,W1,L1,U1,lam1=model(n=6,d=3)
    e,S=eigh(L1); ell1,eta1,segs=ramp(lam1)
    def H_eta(eta):
        DD=G1.conj().T@np.linalg.solve(Q1,G1)
        return np.block([[eta*eta*DD,eta*G1.conj().T],[eta*G1,Q1]])
    target=np.vstack((S@np.diag(1/np.sqrt(1+e))@S.conj().T,-W1@(S@np.diag(1/np.sqrt(1+e))@S.conj().T)))
    V0=np.vstack((np.eye(3),np.zeros((6,3)))).astype(complex)
    # ODE solve for multiple T; stiff-ish due max spectrum ~ 1000
    propagation=[]
    for T in [2.,6.,15.,30.]:
        sol=solve_ivp(lambda s,y:(-1j*T*H_eta(eta1(s))@y.reshape(9,3)).reshape(-1),
            (0,1),V0.reshape(-1),rtol=1e-9,atol=1e-10,method='DOP853')
        error=float(np.linalg.norm(sol.y[:,-1].reshape(9,3)-target,2))
        bound=(2*ell1+5*ell1**2+2*len(lam1)*ell1)/(B1*T)
        propagation.append({'T':T,'operator_norm_error':error,'theorem_bound':bound,'integration_rhs_calls':sol.nfev})

    # Absolute counterexample to a cutoff-uniform gap when an undressed
    # positive penalty lives on the non-code bare impurity space.
    a=0.7; Btest=1.2; examples=[]
    for lam2 in [10.,100.,1e3,1e4,1e5]:
        D=np.array([[0.,0.],[0.,a]])
        W2=np.sqrt(lam2)*np.eye(2)
        AA=np.block([[Btest*lam2*np.eye(2)+D,Btest*W2],[Btest*W2,Btest*np.eye(2)]])
        spectra=eigh(AA,eigvals_only=True)
        examples.append({'L_eigenvalue':lam2,'first_positive_gap':float(spectra[1]),
          'variational_gap_upper_bound':float(a/(1+lam2))})

    result={'noncommutation_norm_J_L':noncomm,'geometric_arc_length':ell,
            'arc_length_upper_bound':len(lam)*pi/2,'general_matrix_samples':sample,
            'transport':propagation,'bare_penalty_gap_collapse':examples,
            'scope':'exact finite-band self-adjoint matrix model; common-amplitude scalar loading; no endpoint-only Jacobi interface'}
    with open('/mnt/data/astra_matrix_loader_audit.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
if __name__=='__main__':calculate()

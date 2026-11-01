"""Ordinary finite-source photon parity instruments; diagnostics are not certificates.
Column-major density vectorization. No source trajectories are sampled.
"""
import numpy as np
from scipy.linalg import expm
I=np.eye(2); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]); SM=np.array([[0,1],[0,0]],complex)

def source_parts(c,loss,up=0):
    H=-1j*c*(np.kron(I,X)-np.kron(X.T,I))
    Jm=np.kron(SM.conj(),SM); Jp=np.kron(SM.T,SM.T)
    Q=SM.T@SM; P=I-Q
    A=H-.5*loss*(np.kron(I,Q)+np.kron(Q.T,I))-.5*up*(np.kron(I,P)+np.kron(P.T,I))
    return A,loss*Jm,up*Jp

def instruments(c,loss,up,eta_m,eta_p,dt,dark=0):
    """One click per bin, blind after first captured jump; source keeps running.
    Returns (positive instrument, missed-parity signed instrument), each (no,click).
    Both transition maps include continuing Hamiltonian and both jump channels.
    """
    A,Jm,Jp=source_parts(c,loss,up)
    C=eta_m*Jm+eta_p*Jp
    out=[]
    for z in [1,-1]:
        active=A+z*((1-eta_m)*Jm+(1-eta_p)*Jp)-dark*np.eye(4)
        inactive=A+z*(Jm+Jp)
        M=np.block([[active,np.zeros((4,4))],[C+z*dark*np.eye(4),inactive]])
        E=expm(dt*M)
        out.append((E[:4,:4],E[4:,:4]))
    return tuple(out)

def raw_error(c,loss,up,T,pulses=0):
    """Exact ordinary telegraph reduction; pulses is number of sign reversals."""
    r=(loss+up)/2
    v=np.array([1,0],complex)
    dt=T/(pulses+1)
    for j in range(pulses+1):
        c0=c*(-1)**j
        v=expm(dt*np.array([[0,-2j*c0],[-2j*c0,-r]]))@v
    return float((1-v[0].real)/2)

def blind_error(c,loss,up,eta_m,eta_p,T,bins,q0=0,readout=0,dark=0):
    plus,minus=instruments(c,loss,up,eta_m,eta_p,T/bins,dark)
    v=np.zeros(4);v[0 if q0==0 else 3]=1
    d=np.linalg.matrix_power(sum(minus),bins)@v
    parity=float((d[0]+d[3]).real)
    # Known initial source bit, final source outcome's independent bit error.
    return (1-(1-2*readout)*parity)/2

def bayes_error(c,loss,up,eta_m,eta_p,T,bins,q0=0,readout=0,dark=0):
    """Exact ordinary optimal terminal Pauli decoder, numerically evaluated.
    Exponential offline enumeration; online filter is constant-memory per source.
    q0 is actually known. The noisy terminal report is the only endpoint defect.
    """
    plus,minus=instruments(c,loss,up,eta_m,eta_p,T/bins,dark)
    v=np.zeros(4);v[0 if q0==0 else 3]=1
    branches=[v.astype(complex)]
    for _ in range(bins):branches=[M@v for v in branches for M in minus]
    score=0
    for v in branches:
        # Residual after correcting click parity and reported final source bit.
        score+=abs(((1-readout)*v[0]-readout*v[3]).real)
        score+=abs(((1-readout)*v[3]-readout*v[0]).real)
    return float((1-score)/2)

def photon_only_error(c,loss,up,eta_m,eta_p,T,bins,q0=0,dark=0,opt=True):
    """No source measurement or noisy report exists in this operation."""
    _,minus=instruments(c,loss,up,eta_m,eta_p,T/bins,dark)
    v=np.zeros(4);v[0 if q0==0 else 3]=1
    if opt:
        branches=[v.astype(complex)]
        for _ in range(bins):branches=[M@v for v in branches for M in minus]
        score=sum(abs((d[0]-d[3]).real) for d in branches)
    else:
        d=np.linalg.matrix_power(sum(minus),bins)@v
        score=float((d[0]-d[3]).real)
    return float((1-score)/2)

def count_moments(c,loss,up,T,q0=0):
    A,Jm,Jp=source_parts(c,loss,up);G=A+Jm+Jp;J=Jm+Jp
    M=np.block([[G,np.zeros((4,4))],[J,G]])
    v=np.zeros(8);v[0 if q0==0 else 3]=1
    x=expm(T*M)@v
    return float((x[4]+x[7]).real)

if __name__=='__main__':
    import json
    rows=[]
    for loss in [1,4,16,64,256,1024,4096]:
        for eta in [0,.9,.99,1]:
            for bins in [1,4,16,64]:
                row=dict(c=1,loss=loss,up=0,T=1,eta_m=eta,eta_p=0,bins=bins,readout=.001)
                row.update(raw=raw_error(1,loss,0,1),raw_best_pauli=min(raw_error(1,loss,0,1),1-raw_error(1,loss,0,1)),echo=raw_error(1,loss,0,1,bins-1),blind_cold=blind_error(1,loss,0,eta,0,1,bins,readout=.001),blind_hot=blind_error(1,loss,0,eta,0,1,bins,q0=1,readout=.001),expected_emissions=count_moments(1,loss,0,1))
                if bins<=4:row['bayes_cold']=bayes_error(1,loss,0,eta,0,1,bins,readout=.001)
                rows.append(row)
    for r in rows:
        if 'bayes_cold' in r:assert r['bayes_cold']<=min(r['raw'],r['blind_cold'])+1e-10
    print(json.dumps({'scope':'Floating diagnostics only; exact structural proof separate','rows':rows},indent=2))

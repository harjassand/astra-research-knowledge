"""Finite-matrix sign/factor audits of the analytic operator inequalities.
These checks are independent numerical audits, not replacements for the proof.
"""
from pathlib import Path
import json
import numpy as np

rng=np.random.default_rng(20261101)
D=32;dd=3
ann=np.diag(np.sqrt(np.arange(1,D)),1);n=ann.conj().T@ann
I=np.eye(D);Id=np.eye(dd)
A=np.kron(Id,ann);N=np.kron(Id,n)

def dissipator_adjoint(L,V):
    Q=L.conj().T@L
    return L.conj().T@V@L-(Q@V+V@Q)/2

rows=[]
for theta,kappa,nb,eps,u in [(.2,.0001,.1,.12,3.),(.5,1.,.1,1.,1e-6),(.1,.3,.01,.3,.8)]:
    F=rng.normal(size=(dd,dd))+1j*rng.normal(size=(dd,dd));F*=u/np.linalg.norm(F,2)
    H=np.kron(F,ann.conj().T)+np.kron(F.conj().T,ann)
    V=np.kron(Id,np.diag(np.exp(theta*np.arange(D))))
    LV=1j*(H@V-V@H)+dissipator_adjoint(np.sqrt(kappa*(nb+1))*A,V)+dissipator_adjoint(np.sqrt(kappa*nb)*A.conj().T,V)
    c=-kappa*(1-np.exp(-theta))*(1-nb*np.expm1(theta))+2*u*eps*np.sinh(theta/2)
    b=kappa*nb*np.expm1(theta)+2*u/eps*np.sinh(theta/2)
    gap=(c*N+b*np.eye(D*dd))@V-LV
    eig=np.linalg.eigvalsh((gap+gap.conj().T)/2)
    assert eig[0]>-1e-6
    rows.append(dict(theta=theta,kappa=kappa,nbar=nb,epsilon=eps,force_norm=u,minimum_Lyapunov_gap=float(eig[0])))
caprows=[]
for L in [3,8,16]:
    F=rng.normal(size=(dd,dd))+1j*rng.normal(size=(dd,dd));F/=np.linalg.norm(F,2)
    H=np.kron(F,ann.conj().T)+np.kron(F.conj().T,ann)
    P=np.kron(Id,np.diag(np.arange(D)<=L));B=H-P@H@P
    RHS=np.kron(Id,np.diag(4*(np.arange(D)+1)*(np.arange(D)>=L)))
    eig=np.linalg.eigvalsh((RHS-B@B+(RHS-B@B).conj().T)/2)
    assert eig[0]>-1e-10
    caprows.append(dict(L=L,minimum_cutoff_gap=float(eig[0]),bounded_perturbation_norm=float(np.linalg.norm(P@H@P,2)),claimed_upper_norm=2*np.sqrt(L)))
out=dict(operator_Lyapunov=rows,force_cap=caprows)
Path(__file__).with_name('lyapunov_operator_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

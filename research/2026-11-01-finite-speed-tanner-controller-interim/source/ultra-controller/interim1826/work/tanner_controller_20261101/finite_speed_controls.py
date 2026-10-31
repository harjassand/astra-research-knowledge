"""Finite-speed positive-moment controls for two overlapping CSS centers.

The finite fixture has no logical qubits. It tests the full joint generator,
its dressed moment, noncommuting center couplings, and persistent-bath noise.
Numerical eigensolves are diagnostics, not interval certificates or a proof
of the all-size result.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/tanner_controller_20261101'
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex)
down=np.array([[0,1],[0,0]],complex);up=down.conj().T;number=up@down


def ten(*args):
    out=np.array([[1]],complex)
    for a in args:out=np.kron(out,a)
    return out


def diss(j,x):
    a=j.conj().T@j
    return j.conj().T@x@j-(a@x+x@a)/2


def fixture():
    # Tensor order: two DATA qubits, two RECORD qubits, one common BATH.
    pz=(np.eye(4)-ten(Z,Z))/2;px=(np.eye(4)-ten(X,X))/2
    js=[ten(X,I)@pz,ten(Z,I)@px]
    ts=[];gs=[];loss=[]
    for v,j in enumerate(js):
        flag=ten(up,I) if v==0 else ten(I,up)
        a=ten(j,flag,I)
        ts.append(a+a.conj().T)
        gs.append((1+1j)*a+(1-1j)*a.conj().T)
        loss.append(ten(np.eye(4),flag.conj().T,I))
    n=ten(np.eye(4),ten(number,I)+ten(I,number),I)
    u=ten(pz+px,np.eye(4),I)
    return ts,gs,loss,n,u


def main():
    ts,gs,loss,n,u=fixture();ident=np.eye(32)
    beta=np.log(2);rows=[]
    for A in (16,64,256,1024):
        for eps in (2.**-8,2.**-10,2.**-12):
            lam=A*eps**2
            kappa=2*eps**2  # one flag bit per center, nu=1/2, Gamma=1
            W=expm(-1j*eps*gs[1])@expm(-1j*eps*gs[0])
            F=expm(beta*u+lam*n)
            inv=expm(-(beta*u+lam*n)/2)
            h=n/2+eps*sum(ts)
            physical=W.conj().T@F@W
            raw=1j*(h@physical-physical@h)+sum(diss(j,physical) for j in loss)
            dressed=W@raw@W.conj().T
            relative=inv@dressed@inv
            gamma=kappa*(1-np.exp(-beta))
            mu=(1-np.exp(-lam))/2
            diagnostic=relative+gamma*u+mu*n
            diagnostic=(diagnostic+diagnostic.conj().T)/2
            a=float(np.linalg.eigvalsh(diagnostic)[-1])
            # Preserve the actual result, even if it is not small.
            rows.append({'A':A,'epsilon':eps,'lambda':lam,'kappa':kappa,
                         'positive_source_over_kappa':max(0,a)/kappa,
                         'largest_certificate_eigenvalue':a,
                         'hermiticity_residual':float(np.max(np.abs(relative-relative.conj().T)))})
    # Include thermal excitation plus two unconditional coherent couplings
    # through ONE bath, and a mixed jump that is not syndrome scalar.
    eps=2.**-12;A=256;lam=A*eps**2;kappa=2*eps**2
    W=expm(-1j*eps*gs[1])@expm(-1j*eps*gs[0])
    F=expm(beta*u+lam*n);inv=expm(-(beta*u+lam*n)/2)
    h=n/2+eps*sum(ts)
    hn=kappa/4096*(ten(X,I,I,I,X)+ten(Z,I,I,I,Z))
    mixed=np.sqrt(kappa/65536)*(ten(I,I,I,I,(I+Z)/2)+1j*ten(X,I,I,I,X))/4
    gain=[np.sqrt(kappa/65536)*j.conj().T for j in loss]
    physical=W.conj().T@F@W
    raw=1j*((h+hn)@physical-physical@(h+hn))+sum(diss(j,physical) for j in loss+gain+[mixed])
    rel=inv@W@raw@W.conj().T@inv
    gamma=kappa/2;mu=(1-np.exp(-lam))/2
    a=max(0,float(np.linalg.eigvalsh((rel+rel.conj().T)/2+gamma*u+mu*n)[-1]))
    # A separately computed conservative weighted-locality norm charge:
    # each perturbation touches <=3 dressed system qubits in this fixture;
    # use the FULL finite fixture norm, rather than claiming a small cone.
    noise_diamond=2*np.linalg.norm(hn,2)+2*np.linalg.norm(mixed,2)**2+sum(2*np.linalg.norm(j,2)**2 for j in gain)
    noise_weight=np.linalg.norm(F,2)*np.linalg.norm(inv,2)**2
    noiseless=next(x for x in rows if x['A']==A and x['epsilon']==eps)
    upper=noiseless['largest_certificate_eigenvalue']+noise_weight*noise_diamond
    assert a<=upper+1e-13
    assert max(x['hermiticity_residual'] for x in rows)<1e-12
    # At fixed small epsilon, increasing the flag penalty should suppress
    # the residual source in this actual finite generator.
    atsmall=[x for x in rows if x['epsilon']==eps]
    assert all(x['positive_source_over_kappa']>y['positive_source_over_kappa'] for x,y in zip(atsmall,atsmall[1:]))
    out={'fixture':'two data, two record qubits, one common bath; both CSS checks; no logical qubits',
         'dimension':32,'Gamma':1,'detuning':.5,'beta':beta,'rows':rows,
         'noisy_control':{'A':A,'epsilon':eps,'actual_source':a,'source_upper_from_noise_norm':upper,
                          'perturbation_diamond_upper':noise_diamond,
                          'unconditional_common_bath_H':True,'thermal_gain':True,'nonscalar_mixed_jump':True},
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Floating finite operator controls of the full generator; no interval certificate, asymptotic memory, novelty, or hardware claim'}
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/'finite_speed_controls.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'passed':True,'small_epsilon_sources_over_kappa':[x['positive_source_over_kappa'] for x in atsmall]}))


if __name__=='__main__':main()

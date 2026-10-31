"""Finite controls for the charge and remainder claims with multiple modes.

One degree-two data center, two neighbors, two lossy auxiliaries. Complex
couplings and static calibration shifts are retained. This tests the local
normal form, not the degree-18 expander memory or a hardware noise model.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/spectral_memory_20261101'
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex)
down=np.array([[0,1],[0,0]],complex);up=down.conj().T;num=up@down
def ten(*args):
    a=np.array([[1]],complex)
    for b in args:a=np.kron(a,b)
    return a
def at(a,i,n):return ten(*(a if j==i else I for j in range(n)))
def comm(a,b):return a@b-b@a
def diss(j,a):
    b=j.conj().T@j
    return j.conj().T@a@j-(b@a+a@b)/2
def norm(a):return float(np.linalg.norm(a,2))


def main():
    beta=.12;rows=[];algebra=[]
    iso=ten(np.eye(8),np.array([[1],[0],[0],[0]],complex))
    p0=iso@iso.conj().T;pe=np.eye(32)-p0
    xi=at(X,0,3);full_x=ten(xi,np.eye(4))
    nz=sum(at(num,3+r,5) for r in range(2))
    u=ten((2*np.eye(8)-at(Z,0,3)@at(Z,1,3)-at(Z,0,3)@at(Z,2,3))/2,np.eye(4))
    Udata=iso.conj().T@u@iso
    ki=at(Z,0,5)@at(Z,3,5)@at(Z,4,5)
    symmetry=at(X,0,5)@at(X,1,5)@at(X,2,5)
    gammas=(.7,1.6)
    amplitudes=(np.sqrt(.8)*np.exp(.37j),np.sqrt(1.3)*np.exp(-.52j))
    losses=[at(down,3+r,5) for r in range(2)]
    for K in (2.,8.,32.):
        hd=-(K+.025)*at(Z,0,3)@at(Z,1,3)-(K-.017)*at(Z,0,3)@at(Z,2,3)
        frequencies=(4*K+.11,8*K-.09)
        h0=ten(hd,np.eye(4))+sum(frequencies[r]*at(num,3+r,5) for r in range(2))
        v=sum(full_x@(amplitudes[r]*at(up,3+r,5)+amplitudes[r].conjugate()*losses[r]) for r in range(2))
        delta=np.real(np.diag(xi@hd@xi-hd));cs=[];G=np.zeros((32,32),complex)
        for r in range(2):
            values=amplitudes[r]/(gammas[r]/2-1j*(frequencies[r]+delta))
            c=xi@np.diag(values);cs.append(c)
            b=ten(c,at(up,r,2));G+=b+b.conj().T
        def d0(a):return 1j*comm(h0,a)+sum(gammas[r]*diss(losses[r],a) for r in range(2))
        poisson=norm(d0(G)+v)
        fast=norm(1j*comm(h0,G)+v-sum((gammas[r]/2)*(ten(cs[r],at(up,r,2))+ten(cs[r],at(up,r,2)).conj().T) for r in range(2)))
        # Full first-order transformed adjoint, checked on all data matrix units.
        c1=0.
        for i in range(8):
            for j in range(8):
                a=np.zeros((8,8),complex);a[i,j]=1;a=ten(a,np.eye(4))
                ag=1j*comm(G,a)
                value=d0(ag)-1j*comm(G,d0(a))+1j*comm(v,a)
                c1=max(c1,norm(value))
        assert max(poisson,fast,c1,norm(comm(G,ki)),norm(comm(v,symmetry)))<1e-10
        algebra.append({'K':K,'poisson':poisson,'uniform_fast_identity':fast,'full_data_C1':c1,'G_norm':norm(G)})
        for eps in (.1,.05,.025,.0125):
            lam=beta*eps;W=expm(-1j*eps*G)
            H=W@(h0+eps*v)@W.conj().T
            js=[W@j@W.conj().T for j in losses]
            F=expm(beta*u+lam*nz);inv=expm(-(beta*u+lam*nz)/2)
            raw=1j*comm(H,F)+sum(gammas[r]*diss(js[r],F) for r in range(2))
            fast_drift=-sum(gammas[r]*(1-np.exp(-lam))*at(num,3+r,5) for r in range(2))
            fd=expm(beta*Udata);idhalf=expm(-beta*Udata/2)
            leading=sum(eps**2*gammas[r]*idhalf@diss(cs[r],fd)@idhalf for r in range(2))
            rem=inv@raw@inv-fast_drift-ten(leading,np.eye(4))
            rem=(rem+rem.conj().T)/2
            ground=iso.conj().T@rem@iso
            hground=iso.conj().T@H@iso
            ground_diag=norm(hground-np.diag(np.diag(hground)))
            block_wrong=0.;excited=0.;linear=0.
            for r,j in enumerate(js):
                b=iso.conj().T@j@iso
                forbidden=np.array([[b[i,jj] if (i^jj)!=4 else 0 for jj in range(8)] for i in range(8)])
                block_wrong=max(block_wrong,norm(forbidden))
                excited=max(excited,norm(pe@j@iso)/eps**2)
                linear=max(linear,norm(b-1j*eps*cs[r])/eps**3)
            assert max(ground_diag,block_wrong)<1e-10
            rows.append({'K':K,'epsilon':eps,
                         'full_residual_over_beta_epsilon_squared':norm(rem)/(beta*eps**2),
                         'ground_residual_over_beta_epsilon_fourth':norm(ground)/(beta*eps**4),
                         'ground_H_offdiagonal':ground_diag,'wrong_data_flip_block':block_wrong,
                         'ground_loss_cubic_remainder_coefficient':linear,
                         'loss_to_excited_quadratic_coefficient':excited})
    assert max(r['ground_residual_over_beta_epsilon_fourth'] for r in rows)<30
    out={'fixture':'degree-two center, two neighbors, two finite auxiliary qubits, complex couplings and shifted energies/linewidths',
         'beta':beta,'Gamma':1.,'gammas':gammas,
         'coupling_squared_moduli':[abs(a)**2 for a in amplitudes],
         'algebra':algebra,'rows':rows,
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Finite calibrated multimode charge identities and predicted local remainder orders; no degree-18 dynamics, interval positivity, or asymptotic proof inferred from samples'}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'calibrated_multimode_controls.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'passed':True,'output':str(path),'algebra':algebra,
                      'ground_scaled_remainders':[r['ground_residual_over_beta_epsilon_fourth'] for r in rows]}))


if __name__=='__main__':main()

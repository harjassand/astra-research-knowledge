"""Stable full-generator moment diagnostics for damped arity reduction.

Four data qubits, two gadget mediators; optional one common bath. The
target has two noncommuting weight-four Hamiltonian terms and one-body
loss. The physical compiler uses only <=3-body Pauli Hamiltonians and
one-body loss. This fixture has NO logical code or memory advantage.

Huge mediator gaps commute exactly with the moment after changing frame.
The remaining Hamiltonian is evaluated by a stable Taylor expansion with
an explicit analytic tail bound, rather than subtracting two ~eps^-2
floating matrices. Eigensolves remain floating diagnostics, not intervals.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/arity_transfer_20261101'
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
down=np.array([[0,1],[0,0]],complex);num=down.conj().T@down


def ten(*args):
    a=np.array([[1]],complex)
    for b in args:a=np.kron(a,b)
    return a
def comm(a,b):return a@b-b@a
def diss(j,a):
    b=j.conj().T@j
    return j.conj().T@a@j-(b@a+a@b)/2
def pauli_at(m,j,total):return ten(*(m if k==j else I for k in range(total)))


def main():
    hs=[.005,-.003]
    aa=[ten(X,X,I,I),ten(Z,X,I,I)];bb=ten(I,I,X,X)
    pp=[a@bb for a in aa]
    kk=[math.sqrt(abs(h)/2)*(a-np.sign(h)*bb) for h,a in zip(hs,aa)]
    gg=[ten(kk[0],Y,I),ten(kk[1],I,Y)]
    vv=ten(kk[0],X,I)+ten(kk[1],I,X)
    ng=pauli_at(num,4,6)+pauli_at(num,5,6)
    nd=sum(pauli_at(num,j,6) for j in range(4))
    htarget=sum(h*p for h,p in zip(hs,pp))
    data_loss=[pauli_at(down,j,6) for j in range(4)]
    record_loss=[pauli_at(down,j,6) for j in (4,5)]
    beta=np.log(2)/4;lam=.01;gamma=(1-np.exp(-beta))/2
    F=expm(beta*nd+lam*ng);inv=expm(-(beta*nd+lam*ng)/2)
    fd=np.diag([np.exp(beta*j.bit_count()) for j in range(16)])
    idata=np.diag(1/np.sqrt(np.diag(fd)))
    nddata=np.diag([j.bit_count() for j in range(16)])
    dl=[pauli_at(down,j,4) for j in range(4)]
    target_rel=idata@(1j*comm(htarget,fd)+sum(diss(j,fd) for j in dl))@idata+gamma*nddata
    target_source=max(0,float(np.linalg.eigvalsh((target_rel+target_rel.conj().T)/2)[-1]))
    # Formal matrix coefficients of Ad_R(N+eps V), through degree eight.
    degree=8;zero=np.zeros((64,64),complex)
    coeff=[ng,vv]+[zero.copy() for _ in range(degree-1)]
    for g in gg:
        newer=[]
        for k in range(degree+1):
            val=zero.copy()
            for j in range(k+1):
                a=coeff[k-j]
                for _ in range(j):a=-1j*comm(g,a)
                val=val+a/math.factorial(j)
            newer.append(val)
        coeff=newer
    assert np.max(np.abs(coeff[0]-ng))<1e-14
    assert np.max(np.abs(coeff[1]))<1e-14
    summ=2*sum(np.linalg.norm(g,2) for g in gg)
    rows=[];saved=None
    for rate in (16.,64.,256.,1024.):
        for eps in (2.**-10,2.**-14,2.**-18):
            R=expm(-1j*eps*gg[1])@expm(-1j*eps*gg[0])
            # Degree 0 (N/eps^2) commutes with F; degree 1 is EXACTLY zero.
            hrot=sum(eps**(k-2)*coeff[k] for k in range(2,degree+1))
            htail=np.exp(eps*summ)*(np.linalg.norm(ng,2)*(eps*summ)**(degree+1)/math.factorial(degree+1)
                    +eps*np.linalg.norm(vv,2)*(eps*summ)**degree/math.factorial(degree))/eps**2
            jumps=[R@j@R.conj().T for j in data_loss]
            jumps.extend(np.sqrt(rate)*(R@j@R.conj().T) for j in record_loss)
            raw=1j*comm(hrot,F)+sum(diss(j,F) for j in jumps)
            mu=rate*(1-np.exp(-lam))/4
            rel=inv@raw@inv+gamma*nd+mu*ng
            rel=(rel+rel.conj().T)/2
            source=max(0,float(np.linalg.eigvalsh(rel)[-1]))
            weighted_tail=2*np.linalg.norm(F,2)*np.linalg.norm(inv,2)**2*htail
            row={'mediator_loss_rate':rate,'epsilon':eps,'mediator_gap':eps**-2,
                 'coupler_strengths':[math.sqrt(abs(h)/2)/eps for h in hs],
                 'source':source,'source_minus_target':source-target_source,
                 'Hamiltonian_Taylor_tail_norm_upper':float(htail),
                 'weighted_Taylor_tail_upper':float(weighted_tail)}
            rows.append(row)
            if rate==1024. and eps==2.**-18:saved=(R,hrot,jumps,source,weighted_tail,mu)
    # Common-bath controller and data errors, upward jumps, and a mixed
    # dissipator. The bound charges their FULL finite-fixture diamond norm.
    R,hrot,jumps,source,tail,mu=saved
    scale=1e-7
    hn=scale*(ten(pauli_at(X,0,6),X)+ten(pauli_at(X,4,6),Z))
    jm=np.sqrt(scale)*(ten(np.eye(64),(I+Z)/2)+1j*ten(pauli_at(Z,1,6),X))/4
    gains=[np.sqrt(scale)*ten(j.conj().T,I) for j in record_loss]
    RR=ten(R,I);hn=RR@hn@RR.conj().T;jm=RR@jm@RR.conj().T
    gains=[RR@j@RR.conj().T for j in gains]
    ff=ten(F,I);ii=ten(inv,I)
    raw=1j*comm(ten(hrot,I)+hn,ff)+sum(diss(ten(j,I),ff) for j in jumps)+diss(jm,ff)+sum(diss(j,ff) for j in gains)
    rel=ii@raw@ii+gamma*ten(nd,I)+mu*ten(ng,I)
    actual=max(0,float(np.linalg.eigvalsh((rel+rel.conj().T)/2)[-1]))
    delta=2*np.linalg.norm(hn,2)+2*np.linalg.norm(jm,2)**2+sum(2*np.linalg.norm(j,2)**2 for j in gains)
    weight=np.linalg.norm(F,2)*np.linalg.norm(inv,2)**2
    upper=source+tail+weight*delta
    assert actual<=upper+1e-11
    out={'fixture':'four data, two lossy mediators; optional one shared bath; NO logical code',
         'target_max_H_arity':4,'physical_max_H_arity':3,'physical_dissipation_arity':1,
         'target_terms':'0.005 XXXX - 0.003 ZXXX','beta':float(beta),'new_excitation_weight':lam,
         'target_source':target_source,'rows':rows,
         'shared_bath_noise':{'source':actual,'source_upper':float(upper),'diamond_noise_upper':float(delta),
                               'coherent_data_and_mediator_faults':True,'thermal_gain':True,'mixed_jump':True},
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Finite floating full-generator moment controls with analytical series tail; no interval eigencertificate, logical memory, all-size theorem, or device validation'}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'finite_generator_controls.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'passed':True,'target_source':target_source,
                     'small_epsilon_extra_sources':[r['source_minus_target'] for r in rows if r['epsilon']==2.**-18]}))


if __name__=='__main__':main()

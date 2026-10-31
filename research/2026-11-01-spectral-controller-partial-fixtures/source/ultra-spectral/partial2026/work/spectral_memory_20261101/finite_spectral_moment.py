"""Full finite spectral-controller moment, including occupied flags/bath.

Three repetition DATA qubits on a triangle, one resonant auxiliary per
site. This is not the degree-18 bipartite expander family. Numerical
operator inequalities retain all controller states. No asymptotic memory
claim or hardware validation is inferred from this fixture.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/spectral_memory_20261101'
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
down=np.array([[0,1],[0,0]],complex);up=down.conj().T;num=up@down
def ten(*args):
    a=np.array([[1]],complex)
    for b in args:a=np.kron(a,b)
    return a
def at(m,q,total):return ten(*(m if j==q else I for j in range(total)))
def comm(a,b):return a@b-b@a
def diss(j,a):
    b=j.conj().T@j;return j.conj().T@a@j-(b@a+a@b)/2


def main():
    beta=.25;rows=[];saved=None
    for K in (2.,4.,8.,16.):
        J=K;hd=-J*(ten(Z,Z,I)+ten(I,Z,Z)+ten(Z,I,Z))
        u=(3*np.eye(8)+hd/J)/2
        U=ten(u,np.eye(8));N=sum(at(num,3+i,6) for i in range(3))
        hf=ten(hd,np.eye(8))+4*J*N
        losses=[at(down,3+i,6) for i in range(3)];vs=[];gs=[]
        for i in range(3):
            xi=at(X,i,3);delta=xi@hd@xi-hd;flag=at(up,i,3)
            gs_i=np.zeros((64,64),complex)
            for d in (-4*J,0.,4*J):
                pi=np.diag(np.isclose(np.diag(delta),d).astype(float))
                c=1/(.5-1j*(4*J+d));a=c*ten(xi@pi,flag)
                gs_i+=a+a.conj().T
            gs.append(gs_i);vs.append(at(X,i,6)@at(X,3+i,6))
        for eps in (.025,.05,.1):
            lam=beta*eps;kappa=4*eps**2
            W=np.eye(64,dtype=complex)
            for g in gs:W=expm(-1j*eps*g)@W
            F=expm(beta*U+lam*N);inv=expm(-(beta*U+lam*N)/2)
            physical=W.conj().T@F@W
            H=hf+eps*sum(vs)
            raw=1j*comm(H,physical)+sum(diss(j,physical) for j in losses)
            relative=inv@W@raw@W.conj().T@inv
            gamma=kappa*(1-np.exp(-2*beta))/2
            mu=(1-np.exp(-lam))/4
            cert=(relative+relative.conj().T)/2+gamma*U+mu*N
            source=max(0,float(np.linalg.eigvalsh(cert)[-1]))
            # Ground restriction isolates the remaining quantum
            # controller contribution; it is not used as a substitute.
            iso=ten(np.eye(8),np.array([[1],[0],[0],[0],[0],[0],[0],[0]],complex))
            ground=iso.conj().T@cert@iso
            aground=max(0,float(np.linalg.eigvalsh((ground+ground.conj().T)/2)[-1]))
            rows.append({'J_over_Gamma':K,'g_over_Gamma':eps,'lambda':lam,'kappa':kappa,
                         'full_source':source,'full_source_over_kappa_beta':source/(kappa*beta),
                         'ground_source':aground,'full_minus_ground_source':source-aground,
                         'hermiticity_residual':float(np.max(np.abs(relative-relative.conj().T)))})
            if K==8. and eps==.05:saved=(W,F,inv,H,losses,U,N,gamma,mu,source,kappa)
    W,F,inv,H,losses,U,N,gamma,mu,source,kappa=saved
    scale=kappa/4096
    hn=scale*(ten(at(X,0,6),X)+ten(at(Z,0,6)@at(Z,1,6),Z)+ten(at(X,3,6),Y))
    mixed=np.sqrt(scale)*(ten(np.eye(64),(I+Z)/2)+1j*ten(at(X,1,6),X))/4
    gain=[np.sqrt(scale)*ten(j.conj().T,I) for j in losses]
    FF=ten(F,I);II=ten(inv,I);WW=ten(W,I)
    ph=WW.conj().T@FF@WW
    raw=1j*comm(ten(H,I)+hn,ph)+sum(diss(ten(j,I),ph) for j in losses)+diss(mixed,ph)+sum(diss(j,ph) for j in gain)
    rel=II@WW@raw@WW.conj().T@II+gamma*ten(U,I)+mu*ten(N,I)
    noisy=max(0,float(np.linalg.eigvalsh((rel+rel.conj().T)/2)[-1]))
    delta=2*np.linalg.norm(hn,2)+2*np.linalg.norm(mixed,2)**2+sum(2*np.linalg.norm(j,2)**2 for j in gain)
    upper=source+np.linalg.norm(F,2)*np.linalg.norm(inv,2)**2*delta
    assert noisy<=upper+1e-11
    assert max(r['hermiticity_residual'] for r in rows)<1e-11
    # Exact algebraic countermodel: in the ideal syndrome corrector a
    # Z_i phase flip has no syndrome, acts as logical Z, and leaves all
    # classical populations unchanged. Its exact logical diamond error
    # is 1-exp(-2 n eta T), never suppressed by the repetition length.
    n=3;eta=.001;times=[1.,10.,100.]
    failure=[{'T':t,'logical_diamond_error':1-np.exp(-2*n*eta*t),'classical_population_error':0.} for t in times]
    out={'fixture':'three data on triangle, three auxiliary qubits, optional one common bath; not the expander family',
         'physical_H_max_arity':2,'loss_arity':1,'Gamma':1,'beta':beta,'rows':rows,
         'noise_control':{'coherent_X_and_ZZ_data_faults':True,'coherent_controller_fault':True,
                          'thermal_gain':True,'mixed_jump':True,'actual_source':noisy,'source_upper':float(upper),
                          'diamond_noise_upper':float(delta)},
         'symmetry_breaking_countermodel':{'model':'ideal syndrome corrector plus eta sum_i D[Z_i]',
                                          'n':n,'eta':eta,'rows':failure},
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Floating full-controller operator diagnostics plus an analytic symmetry-breaking countermodel; no scalable encoded-memory simulation or interval positivity certificate'}
    OUT.mkdir(parents=True,exist_ok=True);p=OUT/'finite_spectral_moment.json';p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(p),'passed':True,'full_source_over_kappa_beta':[r['full_source_over_kappa_beta'] for r in rows]}))


if __name__=='__main__':main()

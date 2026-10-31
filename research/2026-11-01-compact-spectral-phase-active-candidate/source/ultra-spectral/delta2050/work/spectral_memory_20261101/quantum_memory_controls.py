"""Exact finite Markov-model channels for the known three-spin shadow code.

This is a finite quantum-control fixture, not the expander-family proof.
An exact local-charge block reduction retains controller coherences and
an unknown input entangled with a reference. It is checked against the
full six-qubit Lindbladian at one time before being used for longer times.
No experiment, shared-bath theorem, or asymptotic advantage is inferred.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.sparse import bmat,block_diag,csr_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/spectral_memory_20261101'
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex);down=np.array([[0,1],[0,0]],complex);up=down.conj().T;num=up@down
def ten(*a):
    b=np.array([[1]],complex)
    for c in a:b=np.kron(b,c)
    return b
def at(m,i,n):return ten(*(m if j==i else I for j in range(n)))
def vec(a):return a.reshape(-1,order='F')
def matrix(a,d):return a.reshape((d,d),order='F')


def generators(J,g,gamma,gain,eta):
    d=8;iden=np.eye(d);zz=[at(Z,i,3) for i in range(3)]
    xx=[at(X,i,3) for i in range(3)];dd=[at(down,i,3) for i in range(3)]
    nn=sum(at(num,i,3) for i in range(3));blocks=[];offblocks=[]
    for k in range(8):
        signs=[1-2*int(bool(k&(1<<(2-i)))) for i in range(3)]
        h=-J*sum(signs[i]*signs[j]*(zz[i]@zz[j]) for i,j in ((0,1),(1,2),(0,2)))+4*J*nn+g*sum(xx)
        common=-1j*(np.kron(iden,h)-np.kron(h.T,iden))
        for a in dd:
            b=a.conj().T@a;common-=.5*(np.kron(iden,b)+np.kron(b.T,iden))
            a=a.conj().T;b=a.conj().T@a;common-=gain/2*(np.kron(iden,b)+np.kron(b.T,iden))
        common-=3*gamma*np.eye(64)
        diag=common.copy();off=common.copy()
        for z in zz:
            diag+=eta*(np.kron(z,z)-np.eye(64))
            off-=eta*(np.kron(z,z)+np.eye(64))
        blocks.append(csr_matrix(diag));offblocks.append(csr_matrix(off))
    layout=[[None]*8 for _ in range(8)];layout_off=[[None]*8 for _ in range(8)]
    for k in range(8):
        layout[k][k]=blocks[k];layout_off[k][k]=offblocks[k]
        for i,a in enumerate(dd):
            target=k^(1<<(2-i))
            jump=np.kron(a.conj(),a)+gain*np.kron(a.T,a.conj().T)+gamma*np.eye(64)
            layout[target][k]=csr_matrix(jump);layout_off[target][k]=csr_matrix(jump)
    return bmat(layout,format='csr'),bmat(layout_off,format='csr')


def syndrome(d):return d if d.bit_count()<=1 else 7^d
def logical(d):return int(d.bit_count()>1)


def choi_from_blocks(diag,off):
    jj=np.zeros((32,32),complex)
    for k in range(8):
        rd=matrix(diag[k*64:(k+1)*64],8);ro=matrix(off[k*64:(k+1)*64],8)
        for f in range(8):
            for h in range(8):
                da=k^f;db=k^h
                if syndrome(da)!=syndrome(db):continue
                for a in range(2):
                    for b in range(2):
                        v=(rd if a==b else ro)[f,h]/2
                        row=((logical(da)^a)*8+f)*2+a
                        col=((logical(db)^b)*8+h)*2+b
                        jj[row,col]+=v
    return jj


def metrics(jj):
    assert np.max(np.abs(jj-jj.conj().T))<1e-9
    assert abs(np.trace(jj)-1)<1e-9
    assert np.linalg.eigvalsh((jj+jj.conj().T)/2)[0]>-1e-9
    aux=np.zeros((8,8),complex);jqr=np.zeros((4,4),complex)
    for q in range(2):
        for r in range(2):
            for c in range(8):
                for d in range(8):aux[c,d]+=jj[(q*8+c)*2+r,(q*8+d)*2+r]
    for q in range(2):
        for v in range(2):
            for r in range(2):
                for s in range(2):jqr[q*2+r,v*2+s]=sum(jj[(q*8+c)*2+r,(v*8+c)*2+s] for c in range(8))
    target=np.zeros_like(jj)
    for q in range(2):
        for v in range(2):
            for c in range(8):
                for d in range(8):target[(q*8+c)*2+q,(v*8+d)*2+v]=aux[c,d]/2
    dist=float(np.sum(np.abs(np.linalg.eigvalsh((jj-target+jj.conj().T-target.conj().T)/2))))
    bell=np.array([[1,1,0,0],[0,0,1,1],[0,0,1,-1],[1,-1,0,0]],complex)/np.sqrt(2)
    bj=bell.conj().T@jqr@bell
    assert np.max(np.abs(bj-np.diag(np.diag(bj))))<1e-8
    pI=float(np.real(bj[0,0]));mxx=float(np.real(np.trace(ten(X,X)@jqr)))
    return {'decoded_logical_diamond':max(0,2*(1-pI)),
            'joint_controller_comparison_choi_norm':dist,
            'joint_controller_comparison_diamond_upper':min(2,2*dist),
            'logical_X_retention':mxx,'controller_output_trace':float(np.real(np.trace(aux)))}


def full_check(J,g,gamma,gain,eta,diag_state,off_state):
    # Full Hilbert-space six-qubit GKSL calculation, independent of the
    # charge-block assembly, for ground controllers at T=1.
    D=64;idn=eye(D,format='csr',dtype=complex)
    H=-J*sum(at(Z,i,6)@at(Z,j,6) for i,j in ((0,1),(1,2),(0,2)))
    H+=4*J*sum(at(num,3+i,6) for i in range(3))+g*sum(at(X,i,6)@at(X,3+i,6) for i in range(3))
    HH=csr_matrix(H);L=-1j*(kron(idn,HH)-kron(HH.T,idn))
    js=[]
    for i in range(3):
        js.extend([at(down,3+i,6),np.sqrt(gain)*at(up,3+i,6),np.sqrt(gamma)*at(X,i,6),np.sqrt(eta)*at(Z,i,6)])
    for a in js:
        a=csr_matrix(a);b=a.conj().T@a
        L+=kron(a.conj(),a)-.5*(kron(idn,b)+kron(b.T,idn))
    init=[]
    for a in range(2):
        for b in range(2):
            rho=np.zeros((64,64),complex);rho[(7*a)*8,(7*b)*8]=1
            init.append(vec(rho))
    states=expm_multiply(L,np.stack(init,axis=1))
    jf=np.zeros((32,32),complex)
    for a in range(2):
        for b in range(2):
            rho=matrix(states[:,2*a+b],64);out=np.zeros((16,16),complex)
            for e in (0,1,2,4):
                kd=np.zeros((2,8),complex);kd[0,e]=1;kd[1,7^e]=1
                k=ten(kd,np.eye(8));out+=k@rho@k.conj().T
            inds_a=np.arange(16)*2+a;inds_b=np.arange(16)*2+b
            jf[np.ix_(inds_a,inds_b)]+=out/2
    reduced=choi_from_blocks(diag_state,off_state)
    err=float(np.max(np.abs(jf-reduced)))
    assert err<1e-10
    return err


def comparison(T,gamma,eta,kappa):
    px=(1-np.exp(-2*gamma*T))/2;pz1=(1-np.exp(-2*eta*T))/2;pz3=(1-np.exp(-6*eta*T))/2
    bad=3*px**2-2*px**3
    tau=1/kappa;cycles=int(np.floor(T/tau+1e-10));rest=max(0,T-cycles*tau)
    pcycle=(1-np.exp(-2*gamma*tau))/2;qcycle=3*pcycle**2-2*pcycle**3
    prest=(1-np.exp(-2*gamma*rest))/2;qrest=3*prest**2-2*prest**3
    psched=(1-(1-2*qcycle)**cycles*(1-2*qrest))/2
    # Ideal active minority-flip generator, with matched nominal kappa.
    Q=np.zeros((8,8))
    for d in range(8):
        for i in range(3):
            other=[j for j in range(3) if j!=i]
            bit=(d>>(2-i))&1
            active=all(((d>>(2-j))&1)!=bit for j in other)
            rate=gamma+kappa*active;t=d^(1<<(2-i));Q[t,d]+=rate;Q[d,d]-=rate
    p=expm(T*Q)[:,0];pideal=sum(p[d] for d in range(8) if logical(d))
    return {'bare_qubit_diamond':2*(1-(1-px)*(1-pz1)),
            'three_data_final_decode_only_diamond':2*(1-(1-bad)*(1-pz3)),
            'ideal_scheduled_recovery_diamond':2*(1-(1-psched)*(1-pz3)),
            'ideal_active_repair_diamond':2*(1-(1-pideal)*(1-pz3)),
            'ideal_schedule_period':tau}


def activity(ld,initial,T,gamma,gain,eta):
    # Integrate the actual auxiliary occupation alongside the finite
    # quantum master equation, retaining all local charge blocks.
    nrow=np.zeros((1,512),complex)
    for k in range(8):
        for f in range(8):nrow[0,k*64+9*f]=f.bit_count()
    aug=bmat([[ld,csr_matrix((512,1))],
              [csr_matrix(nrow),csr_matrix((1,1))]],format='csr')
    start=np.vstack((initial,np.zeros((1,2),complex)))
    end=expm_multiply(T*aug,start)
    rows=[]
    for c,label in enumerate(('ground','all_excited')):
        integ=float(np.real(end[-1,c]))
        rows.append({'T':T,'initial_controllers':label,
                     'symmetry_breaking_rate_per_data':eta,
                     'nominal_loss_events':integ,
                     'controller_gain_events':gain*(3*T-integ),
                     'data_X_noise_events':3*gamma*T,
                     'data_Z_noise_events':3*eta*T,
                     'physical_qubits':6,'Hamiltonian_pair_couplers':6,
                     'maximum_coupling_degree':3,
                     'auxiliary_bare_gap':16.,
                     'summed_absolute_Hamiltonian_coefficient_times_T':60.3*T,
                     'ideal_comparator_recovery_rounds':8,
                     'scope':'Expected jump counts for the specified finite Markov model and fixed initial controllers, not acquired power, bath bandwidth, hardware noise, or latency costs of ideal comparator recovery'})
    return rows


def main():
    J=4.;g=.1;gamma=.0004;gain=.000004;kappa=4*g*g
    initial=np.zeros((512,2),complex)
    initial[0,0]=1
    initial[7*64+63,1]=1  # |111> flags, K=data XOR flags=111
    rows=[];validation=None;activity_rows=[]
    for eta in (0.,.00001):
        ld,lo=generators(J,g,gamma,gain,eta)
        atone_d=expm_multiply(ld,initial[:,0]);atone_o=atone_d if eta==0 else expm_multiply(lo,initial[:,0])
        if eta>0:validation=full_check(J,g,gamma,gain,eta,atone_d,atone_o)
        rd=expm_multiply(ld,initial,start=0,stop=200,num=9,endpoint=True)
        ro=rd if eta==0 else expm_multiply(lo,initial,start=0,stop=200,num=9,endpoint=True)
        for index in (0,1,2,4,8):
            T=25.*index
            for col,state in enumerate(('ground','all_excited')):
                jj=choi_from_blocks(rd[index,:,col],ro[index,:,col]);m=metrics(jj)
                expected=np.exp(-6*eta*T)
                assert abs(m['logical_X_retention']-expected)<1e-8
                rows.append({'T':T,'symmetry_breaking_rate_per_data':eta,'initial_controllers':state,
                             **m,**comparison(T,gamma,eta,kappa)})
        activity_rows.extend(activity(ld,initial,200.,gamma,gain,eta))
        print(json.dumps({'eta_complete':eta,'last_ground_row':rows[-2]}),flush=True)
    out={'fixture':'known three-spin shadow-code warmup, full six-qubit Markov dynamics; no persistent bath in this finite channel control',
         'J':J,'Gamma':1,'g':g,'kappa_reference':kappa,'data_X_noise':gamma,'controller_gain':gain,
         'full_Lindbladian_vs_charge_reduction_max_residual':validation,
         'rows':rows,'actual_model_activity':activity_rows,
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Finite unknown-input/reference channels with controllers kept; exact invariant reduction verified at T=1, then floating semigroup controls; no expander-family verification, general-bath simulation, hardware claim, or cost advantage over real scheduled hardware',
         'comparator_scope':'Bare and final-decode-only channels have the same data Pauli noise; scheduled and active-repair references are IDEAL operations and have no controller/hardware fault costs. They are mathematical benchmarks, not acquired devices.'}
    OUT.mkdir(parents=True,exist_ok=True);p=OUT/'quantum_memory_controls.json';p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(p),'passed':True,'independent_full_model_residual':validation}))


if __name__=='__main__':main()

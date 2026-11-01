"""Full quantum finite-controller/flag/bath operator controls.

Five physical qubits: DATA A,B, old lossy controller C, flag F, retained B.
There is no asymptotic code in this diagnostic. It checks exact conjugation,
one-body nominal losses, signed calibration, nonunital faults, and the
positive flag-moment inequality including complete-loss killing.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/latched_gate_20261101'
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
down=np.array([[0,1],[0,0]],complex);num=down.conj().T@down
def ten(*aa):
    a=np.ones((1,1),complex)
    for b in aa:a=np.kron(a,b)
    return a
def at(a,i):return ten(*(a if j==i else I for j in range(5)))
def diss(j,a):
    n=j.conj().T@j
    return j.conj().T@a@j-(n@a+a@n)/2
def adj(h,jj,a):return 1j*(h@a-a@h)+sum((diss(j,a) for j in jj),np.zeros_like(a))
def opnorm(a):return float(np.linalg.norm(a,2))
def liouv(h,jj):
    h=csr_matrix(h);ii=eye(32,format='csr',dtype=complex)
    out=-1j*(kron(ii,h)-kron(h.T,ii))
    for j in jj:
        j=csr_matrix(j);n=j.conj().T@j
        out+=kron(j.conj(),j)-(kron(ii,n)+kron(n.T,ii))/2
    return out.tocsr()

def main():
    xa,za=at(X,0),at(Z,0);xb,zb=at(X,1),at(Z,1)
    xc,zc=at(X,2),at(Z,2);xf,nf=at(X,3),at(num,3)
    # CNOT and its flag-controlled frame. No pulse W is physically applied.
    u=((np.eye(32)+za)+(np.eye(32)-za)@xb)/2
    w=np.eye(32)-nf+nf@u
    assert opnorm(w@w-np.eye(32))<1e-14
    hmem=.31*xa@xc+.23*zb@zc+.41*at(num,2)+.17*at(Y,4)
    oldj=np.sqrt(.7)*at(down,2);flagj=at(down,3)
    gamma=.19;hphysical=w@hmem@w
    assert opnorm(hphysical@nf-nf@hphysical)<1e-14
    assert opnorm(w@oldj@w-oldj)<1e-14
    assert opnorm(w@flagj@w-u@flagj)<1e-14
    # Actual perturbations break reference balance: coherent flag/coupler
    # fault, controller loss-basis error, thermal flag pump, all DATA axes,
    # a common-bath interaction, and a SIGNED negative loss-rate correction.
    eps=2e-5;up=1e-5;dg=-2e-5;angle=1e-5
    dh=eps*(xf@xc+za@at(X,4))
    oldj_actual=np.sqrt(.7)*(at(down,2)+angle*zc)
    noise_j=[np.sqrt(up)*at(down,3).conj().T]
    noise_j += [np.sqrt(eps/3)*at(p,i) for i in (0,1) for p in (X,Y,Z)]
    actual_j=[oldj_actual,np.sqrt(gamma+dg)*flagj]+noise_j
    actual_h=hphysical+dh
    nominal_j=[oldj,np.sqrt(gamma)*flagj]
    f=ten(I,I,I,np.diag([1,np.e]),I)
    finv=ten(I,I,I,np.diag([1,np.exp(-.5)]),I)
    zeta=gamma*(1-np.exp(-1))
    nominal_res=opnorm(adj(hphysical,nominal_j,f)+zeta*nf@f)
    assert nominal_res<1e-13
    # Sum of full-generator diamond-norm upper bounds. Negative dg is paid.
    budget=(2*opnorm(dh)+2*abs(dg)+.7*(4*angle+2*angle**2)
            +2*sum(opnorm(j)**2 for j in noise_j))
    # Every perturbation touches <=2 flag qubits (here actually at most 1).
    cflag=np.e**2
    rel=finv@(adj(actual_h,actual_j,f)+zeta*nf@f)@finv
    highest=float(np.linalg.eigvalsh((rel+rel.conj().T)/2)[-1])
    assert highest<=cflag*budget+1e-12
    # A noncommuting DATA basin; only [P,F]=0 is required for this identity.
    pdata=(np.eye(32)+za@zb)/2
    kill=pdata@adj(actual_h,actual_j,pdata@f@pdata)@pdata
    full=pdata@adj(actual_h,actual_j,f)@pdata
    outgoing=sum((pdata@j.conj().T@(np.eye(32)-pdata)@f@(np.eye(32)-pdata)@j@pdata
                  for j in actual_j),np.zeros((32,32),complex))
    kill_res=opnorm(full-kill-outgoing)
    out_min=float(np.linalg.eigvalsh((outgoing+outgoing.conj().T)/2)[0])
    assert kill_res<1e-13 and out_min>-1e-13
    # Whole-superoperator physical/frame equality, including the SAME bath.
    lp=liouv(actual_h,actual_j);lf=liouv(w@actual_h@w,[w@j@w for j in actual_j])
    adw=kron(csr_matrix(w.conj()),csr_matrix(w),format='csr')
    frame_res=float(np.max(np.abs((lf-adw@lp@adw).data),initial=0))
    assert frame_res<1e-12
    # Entangled DATA/controller/bath input, flag initially |1>. An external
    # reference is unnecessary for an operator-order certificate.
    psi=np.zeros(32,complex);psi[2]=psi[31]=1/np.sqrt(2)
    rho=np.outer(psi,psi.conj());assert abs(np.trace(nf@rho)-1)<1e-14
    times=np.array([0.,2.,8.,24.,60.])
    values=[]
    for t in times:
        rr=expm_multiply(t*lp,rho.reshape(-1,order='F')).reshape(32,32,order='F')
        moment=float(np.trace(f@rr).real)
        log_upper=np.exp(-zeta*t)+cflag*budget/zeta*(1-np.exp(-zeta*t))
        assert np.log(moment)<=log_upper+1e-10
        assert abs(np.trace(rr)-1)<1e-10
        values.append({'time':float(t),'flag_population':float(np.trace(nf@rr).real),
                       'log_flag_moment':float(np.log(moment)),'log_moment_upper':float(log_upper)})
    result={'scope':'full finite quantum operator/dynamics checks, not a code-family simulation',
            'nominal_flag_moment_residual':nominal_res,'signed_total_fault_norm_upper':budget,
            'weighted_fault_source_largest_eigenvalue':highest,'weighted_source_upper':cflag*budget,
            'complete_loss_outgoing_identity_residual':kill_res,'outgoing_min_eigenvalue':out_min,
            'full_physical_to_frame_superoperator_residual':frame_res,
            'actual_controller_nonunitality_norm':opnorm(sum((j@j.conj().T-j.conj().T@j for j in actual_j),np.zeros((32,32),complex))),
            'flag_dynamics':values,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'quantum_flag_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()

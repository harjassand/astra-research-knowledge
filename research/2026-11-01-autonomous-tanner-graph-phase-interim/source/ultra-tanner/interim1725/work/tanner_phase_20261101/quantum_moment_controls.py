"""Full continuously driven finite ferromagnetic control of the moment proof.

Five spins on K5, local majority jumps, all-site unconditional coherent and
mixed Lindblad memory/bath faults. This controls the new quantum estimate;
it is not a quantum Tanner family or an all-Pauli memory construction.
"""
from __future__ import annotations
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
from scipy.linalg import eigvalsh
from scipy.sparse import csr_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/tanner_global_phase_20261101'
N=5;dm=1<<N;db=2;D=dm*db
I=np.eye(2);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]);Pb=(I+Z)/2
h=Q(1,1024);g=Q(1,65536)
Gtotal=N*g/4;Htotal=N*h
gamma=Q(15,64)
source=Q(15,4)*Htotal+272*Gtotal
ratio=source/gamma
Mcert=1/(1-ratio)
pcert=Mcert/16
assert ratio==Q(77,768) and Mcert==Q(768,691) and pcert<Q(4,15)**2


def superop(H,jumps,escapes=None):
    dim=len(H);ident=eye(dim,format='csr',dtype=complex)
    G=-1j*(kron(ident,csr_matrix(H))-kron(csr_matrix(H.T),ident))
    for j,J in enumerate(jumps):
        A=J.conj().T@J if escapes is None else escapes[j]
        G+=kron(csr_matrix(J.conj()),csr_matrix(J))
        G-=(kron(ident,csr_matrix(A))+kron(csr_matrix(A.T),ident))/2
    return G.tocsr(),G.diagonal().sum()


def choi(phi):
    J=np.zeros((16,16),complex)
    for a in range(4):
        for b in range(4):
            J[4*a:4*a+4,4*b:4*b+4]=phi[:,a+4*b].reshape(4,4,order='F')
    return (J+J.conj().T)/2


def build(model):
    H=np.kron(np.eye(dm),X/8+Z/16)
    js=[];native=[]
    U=np.array([s.bit_count()*(N-s.bit_count()) for s in range(dm)])
    for i in range(N):
        F=np.zeros((dm,dm));J=np.zeros((dm,dm));P=np.zeros((dm,dm))
        for s in range(dm):
            F[s^(1<<i),s]=1
            neighbors=N-1
            opposite=sum(((s>>i)^(s>>j))&1 for j in range(N) if j!=i)
            if 2*opposite>neighbors:J[s^(1<<i),s]=1;P[s,s]=1
        B=[Pb,X,Y,Z,(X+Z)/np.sqrt(2)][i]
        H+=float(h)*np.kron(F,B)
        native.append(np.kron(J,I))
        js.append(np.kron(J,I))
        if model=='completed':js.append(np.kron(np.eye(dm)-P,I))
        # ||L_i|| <= sqrt(g)/2. L_i^dagger L_i has off-diagonal
        # memory components: the no-jump evolution is not syndrome scalar.
        js.append(np.sqrt(float(g))*(np.kron(np.eye(dm),Pb)+1j*np.kron(F,X))/4)
    safe=[s for s in range(dm) if min(s.bit_count(),N-s.bit_count())<2]
    inds=[s*db+b for s in safe for b in range(db)]
    unsafe=[i for i in range(D) if i not in inds]
    assert all(np.linalg.norm(J[np.ix_(unsafe,inds)])==0 for J in native)
    HP=H[np.ix_(inds,inds)]
    jp=[J[np.ix_(inds,inds)] for J in js]
    ap=[(J.conj().T@J)[np.ix_(inds,inds)] for J in js]
    F=np.diag([2.**U[s] for s in safe for b in range(db)])
    up=np.diag([U[s] for s in safe for b in range(db)])
    adj=1j*(HP@F-F@HP)
    for J,A in zip(jp,ap):adj+=J.conj().T@F@J-(A@F+F@A)/2
    inv=np.diag(1/np.sqrt(np.diag(F)))
    residual=inv@(adj-float(source)*F+float(gamma)*up@F)@inv
    largest=float(eigvalsh((residual+residual.conj().T)/2)[-1])
    assert largest<1e-10
    loss=sum(ap)-sum(J.conj().T@J for J in jp)
    assert eigvalsh((loss+loss.conj().T)/2)[0]>-1e-10
    G,tG=superop(H,js);K,tK=superop(HP,jp,ap)
    # Fixed complement-pair decoder and encoding, before T is selected.
    ds=[]
    for s in range(dm):
        if s.bit_count()<N/2:
            d=np.zeros((2,dm));d[0,s]=1;d[1,s^(dm-1)]=1
            ds.append(np.kron(d,I))
    dsp=[d[:,inds] for d in ds]
    enc=np.zeros((D,4),complex)
    for q,s in [(0,0),(1,dm-1)]:
        for b in range(db):enc[s*db+b,q*db+b]=1
    ep=enc[inds,:]
    Gglobal=np.zeros((dm,dm))
    for s in range(dm):Gglobal[s^(dm-1),s]=1
    symmetry=np.kron(Gglobal,I)
    assert np.linalg.norm(H@symmetry-symmetry@H)<1e-12
    assert all(np.linalg.norm(J@symmetry-symmetry@J)<1e-12 for J in js)
    return G,tG,K,tK,enc,ep,ds,dsp,F,largest


def inputs(E):
    return np.array([np.outer(E[:,a],E[:,b].conj()).reshape(-1,order='F')
                     for b in range(4) for a in range(4)]).T


def decoded(v,dim,ds):
    phi=np.empty((16,16),complex)
    for col in range(16):
        A=v[:,col].reshape(dim,dim,order='F')
        phi[:,col]=sum(d@A@d.conj().T for d in ds).reshape(-1,order='F')
    return phi


def run():
    rows=[]
    for model in ['active','completed']:
        G,tG,K,tK,E,EP,ds,dsp,F,residual=build(model)
        ip=inputs(E);ik=inputs(EP);dimk=EP.shape[0]
        for T in [1.,10.,100.]:
            full=expm_multiply(G*T,ip,traceA=tG*T)
            kept=expm_multiply(K*T,ik,traceA=tK*T)
            phi=decoded(full,D,ds);sub=decoded(kept,dimk,dsp)
            # Actual bath marginal of the compressed process; trace loss is
            # completed as a CP bath map, not postselected or renormalized.
            lamb=np.empty((4,4),complex);M=np.zeros((2,2),complex);TE=np.zeros((2,2),complex)
            for a in range(2):
                for b in range(2):
                    col=a+4*b
                    A=sub[:,col].reshape(4,4,order='F')
                    lamb[:,a+2*b]=A[:2,:2].reshape(-1,order='F')
                    R=kept[:,col].reshape(dimk,dimk,order='F')
                    M[b,a]=np.trace(F@R);TE[b,a]=np.trace(R)
            M=(M+M.conj().T)/2;TE=(TE+TE.conj().T)/2
            assert eigvalsh(M)[-1]<float(Mcert)+1e-10
            defect=(I-TE+I-TE.conj().T)/2
            ev,V=np.linalg.eigh(defect)
            assert ev[0]>-1e-10
            C=(V*np.sqrt(np.maximum(ev,0)))@V.conj().T
            lcomp=lamb+np.kron(C.conj(),C)
            cmp=np.zeros((16,16),complex);csub=np.zeros_like(cmp)
            for a in range(4):
                for b in range(4):
                    out=np.zeros((4,4),complex);outsub=np.zeros_like(out)
                    unit=np.zeros((2,2));unit[a%2,b%2]=1
                    out[2*(a//2):2*(a//2+1),2*(b//2):2*(b//2+1)]=(lcomp@unit.reshape(-1,order='F')).reshape(2,2,order='F')
                    outsub[2*(a//2):2*(a//2+1),2*(b//2):2*(b//2+1)]=(lamb@unit.reshape(-1,order='F')).reshape(2,2,order='F')
                    cmp[:,a+4*b]=out.reshape(-1,order='F')
                    csub[:,a+4*b]=outsub.reshape(-1,order='F')
            factor=np.linalg.norm(csub-sub)
            assert factor<1e-9
            assert eigvalsh(choi(phi))[0]>-1e-10 and eigvalsh(choi(cmp))[0]>-1e-10
            trace_error=max(abs(np.trace(phi[:,a+4*b].reshape(4,4,order='F'))-(a==b)) for a in range(4) for b in range(4))
            assert trace_error<1e-9
            # For an unnormalised Choi matrix, ||Delta||_diamond<=||J_Delta||_1.
            numerical_upper=float(np.linalg.svd(choi(phi-cmp),compute_uv=False).sum())
            analytic=float((5*Gtotal+2*Htotal)*Q(4,15))*T
            assert numerical_upper<analytic+1e-8
            effect=np.zeros((2,2),complex)
            for a in range(2):
                for b in range(2):
                    effect[b,a]=np.trace(phi[:,a+4*b].reshape(4,4,order='F')[2:,2:])
            effect=(effect+effect.conj().T)/2
            rows.append(dict(model=model,T=T,moment_operator_max_preview=float(eigvalsh(M)[-1]),
                             exact_uniform_moment_upper=str(Mcert),
                             operator_drift_largest_residual=residual,
                             compressed_logical_factorization_residual=float(factor),
                             trace_residual=float(trace_error),
                             actual_error_effect_max_preview=float(eigvalsh(effect)[-1]),
                             comparison_choi_trace_norm_upper_preview=numerical_upper,
                             proved_joint_upper=min(2.,analytic)))
    return rows


def main():
    data=dict(N=N,graph='K5',h_per_face=str(h),mixed_jump_g=str(g),
              generic_jump_has_nonscalar_no_jump=True,common_bath_dimension=2,
              exact_moment_certificate=str(Mcert),exact_boundary_probability_upper=str(pcert),
              exact_joint_upper_at_T100=str((5*Gtotal+2*Htotal)*Q(4,15)*100),
              controls=run(),
              scope='Full global continuously driven finite control, arbitrary joint bath input covered by analytic bound; this repetition fixture only admits X-type memory faults, not a both-CSS Tanner family')
    data['program_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'quantum_moment_controls.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(output=str(OUT/'quantum_moment_controls.json'),checks=len(data['controls']))))


if __name__=='__main__':main()

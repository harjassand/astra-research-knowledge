#!/usr/bin/env python3
"""Native quantum-conditioned baths: exact code algebra and finite GKSL control.

Gaussian integer code algebra and rational probability bounds are exact.
Sparse exponentials are floating controls. The global five-qubit reset is a
conventional test receiver, not a scalable memory. No random draws or hardware.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time
import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import expm_multiply

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/autonomous_memory'
sys.path.insert(0,str(ROOT/'work'))
from ctmc_reflection_control import exp_negative_bounds,dyadic_enclose


def gauss(A):
    A=np.asarray(A)
    assert np.array_equal(A.real,np.rint(A.real)) and np.array_equal(A.imag,np.rint(A.imag))
    return A.real.astype(np.int64),A.imag.astype(np.int64)


def gm(A,B):
    a,b=A;c,d=B
    assert max(np.max(abs(x)) for x in (a,b,c,d))<2**20
    return a@c-b@d,a@d+b@c


def gd(A):return A[0].T,-A[1].T
def geq(A,B):return all(np.array_equal(a,b) for a,b in zip(A,B))
def cx(A):return A[0].astype(float)+1j*A[1]


def pauli(word):
    one={'I':np.eye(2,dtype=complex),'X':np.array([[0,1],[1,0]],complex),
        'Y':np.array([[0,-1j],[1j,0]],complex),'Z':np.diag([1,-1]).astype(complex)}
    P=np.ones((1,1),complex)
    for c in word:P=np.kron(P,one[c])
    return gauss(P)


def syndrome(word,stabilizers):
    return sum((sum(a!='I' and b!='I' and a!=b for a,b in zip(word,g))%2)<<j
        for j,g in enumerate(stabilizers))


def code_basis():
    stabilizers=['XZZXI','IXZZX','XIXZZ','ZXIXZ']
    eye=gauss(np.eye(32));projector=eye
    for g in stabilizers:
        P=pauli(g);projector=gm(projector,(eye[0]+P[0],eye[1]+P[1]))
    w0=(projector[0][:,0:1],projector[1][:,0:1])
    w1=gm(pauli('XXXXX'),w0)
    V=(np.hstack([w0[0],w1[0]]),np.hstack([w0[1],w1[1]]))
    assert geq(gm(gd(V),V),gauss(16*np.eye(2)))
    for g in stabilizers:assert geq(gm(pauli(g),V),V)
    words={0:'IIIII'}
    for i in range(5):
        for p in 'XYZ':
            w='I'*i+p+'I'*(4-i);s=syndrome(w,stabilizers)
            assert s and s not in words;words[s]=w
    assert len(words)==16
    cols=[gm(pauli(words[s]),V) for s in range(16)]
    W=(np.hstack([c[0] for c in cols]),np.hstack([c[1] for c in cols]))
    assert geq(gm(gd(W),W),gauss(16*np.eye(32)))
    def frame(word):
        numerator=gm(gm(gd(W),pauli(word)),W)
        assert all(np.all(a%16==0) for a in numerator)
        result=(numerator[0]//16,numerator[1]//16)
        assert max(np.max(abs(a)) for a in result)<=1
        return cx(result)
    for s,w in words.items():
        expected=np.zeros((32,2),complex);expected[2*s:2*s+2]=np.eye(2)
        assert np.array_equal(frame(w)[:,:2],expected)
    assert np.array_equal(frame('IYYIX')[:2,:2],-np.array([[0,1],[1,0]],complex))
    return frame,{'stabilizers':stabilizers,'logical_X':'XXXXX','logical_Z':'ZZZZZ',
        'code':'[[5,1,3]]','syndrome_representatives':words,'basis_orthonormal_exact':True,
        'all_15_single_Paulis_corrected_exact':True,'IYYIX_is_minus_logical_X_exact':True,
        'arithmetic':'Gaussian integer matrices, bounded intermediates, exact division by 16'}


def maps():
    # Hilbert order syndrome(16), logical(2), bath(2). Column-major vectorization.
    rows=[];cols=[]
    for a in range(4):
        for b in range(4):rows.append(a+64*b);cols.append(a+4*b)
    enc=sp.csc_matrix((np.ones(16),(rows,cols)),shape=(4096,16),dtype=complex)
    rows=[];cols=[]
    for s in range(16):
        for a in range(4):
            for b in range(4):
                rows.append(a+4*b);cols.append((4*s+a)+64*(4*s+b))
    dec=sp.csc_matrix((np.ones(len(rows)),(rows,cols)),shape=(16,4096),dtype=complex)
    recovery=enc@dec
    assert (dec@enc-sp.eye(16)).nnz==0
    assert (recovery@recovery-recovery).nnz==0
    return enc,dec,recovery


def probability_bad(r,kappa,T,order=180):
    # Absorbing event: >=2 potential faults in one recovery gap.
    cap=kappa+r
    Q=[[-r,r,F(0)],[kappa,-(kappa+r),r],[F(0),F(0),F(0)]]
    P=[[F(i==j)+Q[i][j]/cap for j in range(3)] for i in range(3)]
    assert all(sum(row)==1 and min(row)>=0 for row in P)
    mu=cap*T;lo,hi=exp_negative_bounds(mu,260)
    current=[F(1),F(0),F(0)];term=F(1);mass=total=F(0)
    for k in range(order+1):
        total+=term*current[2];mass+=term
        current=[sum((current[i]*P[i][j] for i in range(3)),F(0)) for j in range(3)]
        term*=mu/(k+1)
    tail=1-lo*mass
    assert 0<=tail<F(1,2**100)
    return dyadic_enclose(lo*total,min(F(1),hi*total+tail))


def choi(S,d):
    J=np.zeros((d*d,d*d),complex)
    for i in range(d):
        for j in range(d):
            output=S[:,i+d*j].reshape((d,d),order='F')
            for a in range(d):
                for b in range(d):J[a*d+i,b*d+j]=output[a,b]/d
    return (J+J.conj().T)/2


def bath_projection(S):
    # CP superchannel Phi -> Id_L tensor Tr_L Phi(I_L/2 tensor .).
    bath=np.zeros((4,4),complex)
    for b in range(2):
        for bp in range(2):
            E=np.zeros((2,2),complex);E[b,bp]=1
            output=(S@np.kron(np.eye(2)/2,E).reshape(-1,order='F')).reshape((4,4),order='F').reshape((2,2,2,2))
            bath[:,b+2*bp]=np.einsum('abad->bd',output).reshape(-1,order='F')
    joint=np.zeros((16,16),complex)
    for i in range(4):
        for j in range(4):
            l,b=divmod(i,2);lp,bp=divmod(j,2)
            E=np.zeros((2,2),complex);E[l,lp]=1
            result=np.kron(E,bath[:,b+2*bp].reshape((2,2),order='F'))
            joint[:,i+4*j]=result.reshape(-1,order='F')
    return joint,bath


def reduced_logical(S,rhoB):
    out=np.zeros((4,4),complex)
    for i in range(2):
        for j in range(2):
            E=np.zeros((2,2),complex);E[i,j]=1
            output=(S@np.kron(E,rhoB).reshape(-1,order='F')).reshape((4,4),order='F').reshape((2,2,2,2))
            out[:,i+2*j]=np.einsum('abcb->ac',output).reshape(-1,order='F')
    return out


def main():
    start=time.perf_counter();OUT.mkdir(parents=True,exist_ok=True)
    frame,exact=code_basis();enc,dec,recovery=maps()
    I2=np.eye(2,dtype=complex);X=cx(pauli('X'));Y=cx(pauli('Y'));Z=cx(pauli('Z'))
    bath_ops=[(I2+Z)/2,(I2+X)/2,(I2+Y)/2]
    words=['IYIII','IIYII','IIIIX']
    gamma=F(1,100);h=F(1,2000);kappa=F(1);T=F(10)
    sqrt_gamma=F(1,10);offset=h/sqrt_gamma
    rate=gamma+h*h/gamma;r=3*rate
    assert sqrt_gamma*sqrt_gamma==gamma
    eye=sp.eye(64,format='csc',dtype=complex);eye_super=sp.eye(4096,format='csc',dtype=complex)
    jumps=[];G=np.zeros((64,64),complex)
    for word,B in zip(words,bath_ops):
        K=np.kron(frame(word),B)
        assert np.array_equal(K,K.conj().T) and np.array_equal(K@K,np.kron(np.eye(32),B))
        J=float(sqrt_gamma)*K+1j*float(offset)*np.eye(64)
        target=float(gamma)*np.kron(np.eye(32),B)+float(h*h/gamma)*np.eye(64)
        assert np.max(abs(J.conj().T@J-target))<1e-16
        assert np.linalg.eigvalsh(target).max()<=float(rate)+1e-16
        jumps.append(sp.csc_matrix(J));G+=target
    bath_G=float(gamma)*sum(bath_ops)+3*float(h*h/gamma)*I2
    assert np.max(abs(G-np.kron(np.eye(32),bath_G)))<1e-16
    HB=sp.csc_matrix(np.kron(np.eye(32),X/3+Z/5))
    Jsuper=sum((sp.kron(J.conjugate(),J,format='csc') for J in jumps),
        sp.csc_matrix((4096,4096),dtype=complex))
    Gsp=sp.csc_matrix(G)
    quiet=-1j*(sp.kron(eye,HB)-sp.kron(HB.T,eye))-(sp.kron(eye,Gsp)+sp.kron(Gsp.T,eye))/2-float(kappa)*eye_super
    C=float(kappa)*recovery;zero=sp.csc_matrix((4096,4096),dtype=complex)
    tracker=sp.bmat([[quiet+C,C,zero],[Jsuper,quiet,zero],[zero,Jsuper,quiet+C+Jsuper]],format='csc')
    initial=sp.vstack([enc,sp.csc_matrix((8192,16),dtype=complex)],format='csc').toarray()
    states=expm_multiply(float(T)*tracker,initial,traceA=float(T)*tracker.diagonal().sum())
    recovered=[dec@states[j*4096:(j+1)*4096] for j in range(3)]
    good=recovered[0]+recovered[1];bad=recovered[2];total=good+bad
    projected,bath_good=bath_projection(good)
    factorization_error=float(np.max(abs(good-projected)))
    assert factorization_error<5e-12
    trace=np.eye(4).reshape(-1,order='F')
    assert np.max(abs(trace@total-trace))<5e-12
    effect=(bad.conj().T@trace).reshape((4,4),order='F');effect=(effect+effect.conj().T)/2
    actual_bad=float(np.linalg.eigvalsh(effect).max())
    cap_interval=probability_bad(r,kappa,T)
    assert actual_bad<=float(cap_interval[1])+1e-11
    CPmins={name:float(np.linalg.eigvalsh(choi(S,4)).min()) for name,S in [('total',total),('good',good),('bad',bad)]}
    assert min(CPmins.values())>-5e-12
    # Stronger ordinary global-count bound uses total escape, not separate caps.
    stronger_r=F(3,125)
    a=stronger_r-F(3,2)*gamma-3*h*h/gamma
    assert a>0 and a*a>3*(gamma/2)**2
    stronger_interval=probability_bad(stronger_r,kappa,T)
    assert actual_bad<=float(stronger_interval[1])+1e-11
    bath_states={'zero':np.diag([1,0]),'one':np.diag([0,1]),'plus':np.ones((2,2))/2,'mixed':I2/2}
    fidelities={};omega=np.array([1,0,0,1],complex)/np.sqrt(2)
    for name,rhoB in bath_states.items():
        channel=reduced_logical(total,rhoB)
        fidelities[name]=float(np.real(omega.conj()@choi(channel,2)@omega))
    result={'status':'NATIVE_BATH_FIVE_QUBIT_TRANSFER_CONTROL_PASSED',
        'exact_code_algebra':exact,'native_generator':{'gamma_each':str(gamma),'coherent_h_each':str(h),
            'K_memory_Paulis':words,'K_bath_operators':['(I+Z)/2','(I+X)/2','(I+Y)/2'],
            'bath_Hamiltonian':'X/3+Z/5','one_shared_persistent_bath_qubit':True,
            'bath_preparation_or_reset_assumed':False,'escape_is_bath_only':True,
            'jump_rate_cap_each':str(rate),'dominating_total_rate':str(r),
            'global_recovery_rate':str(kappa),'time':str(T),'added_noise_floor':0},
        'dominating_bad_probability_rational_enclosure':list(map(str,cap_interval)),
        'joint_diamond_error_bound':str(min(F(2),2*cap_interval[1])),
        'joint_diamond_error_bound_preview':float(min(F(2),2*cap_interval[1])),
        'stronger_ordinary_total_hazard_cap':str(stronger_r),
        'stronger_ordinary_joint_diamond_bound_preview':float(2*stronger_interval[1]),
        'same_information_incumbent':'ordinary quantum-jump instrument and GKSL propagation; no algorithmic advantage',
        'finite_numerical_diagnostics':{'good_map_factorization_max_entry_residual':factorization_error,
            'bad_effect_operator_norm':actual_bad,'twice_actual_bad_effect':2*actual_bad,
            'joint_bad_effect_eigenvalues':np.linalg.eigvalsh(effect).tolist(),
            'normalized_Choi_min_eigenvalues':CPmins,'logical_entanglement_fidelities':fidelities,
            'linear_generator_dimension':tracker.shape[0],'input_basis_columns':16,
            'sparse_generator_nonzeros':tracker.nnz,
            'precision_scope':'floating sparse expm; no interval-certified channel or diamond norm'},
        'not_scalable_memory':'global five-qubit reset is ideal supplied correction; no size/locality scaling',
        'new_random_draws':0,'physical_experiments':0,'external_audit':'NOT_PERFORMED',
        'code_SHA256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'CPU_wall_seconds':time.perf_counter()-start}
    (OUT/'native_bath_control.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(OUT/'native_bath_channels.npz',good=good,bad=bad,total=total,bath_good=bath_good)
    print(json.dumps({'status':result['status'],'seconds':result['CPU_wall_seconds'],
        'joint_bound':result['joint_diamond_error_bound_preview'],
        'stronger_ordinary_bound':result['stronger_ordinary_joint_diamond_bound_preview'],
        'actual_bad_effect':actual_bad,'good_factorization_error':factorization_error,
        'entanglement_fidelities':fidelities,'new_random_draws':0},indent=2))


if __name__=='__main__':main()

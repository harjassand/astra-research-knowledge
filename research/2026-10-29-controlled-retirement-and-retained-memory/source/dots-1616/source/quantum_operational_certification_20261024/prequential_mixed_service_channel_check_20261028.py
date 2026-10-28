"""Deterministic complete-channel fixture, not sampled acquisition.

Two arbitrary logical inputs are represented by their FULL four-qubit Choi
reference. A coherent source memory is reused through random TEST/USE roles.
Every branch is summed, not sampled. Floating residuals are explicitly reported.
"""
from pathlib import Path
import hashlib,itertools,json
import numpy as np

I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex)
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2);S=np.diag([1,1j])
P=[I,X,Y,Z]; phi=np.array([1,0,0,1],complex)/np.sqrt(2)
PHI=np.outer(phi,phi.conj());global_phi=np.kron(phi,phi)
GPHI=np.outer(global_phi,global_phi.conj())
sig=(I+Y)/2
source=np.kron(I,H)@(4*np.eye(4)+3j*np.kron(Z,Z))/5
assert np.max(np.abs(source.conj().T@source-np.eye(4)))<1e-14

def embed(g,targets,n):
    out=np.zeros((2**n,2**n),complex)
    for x in range(2**n):
        col=sum(((x>>(n-1-t))&1)<<(len(targets)-1-j) for j,t in enumerate(targets))
        for row in range(2**len(targets)):
            xx=x
            for j,t in enumerate(targets):
                bit=(row>>(len(targets)-1-j))&1
                xx=(xx&~(1<<(n-1-t)))|(bit<<(n-1-t))
            out[xx,x]=g[row,col]
    return out

def partial(r,n,keep):
    keep=list(keep);gone=[i for i in range(n) if i not in keep]
    order=keep+gone+[n+i for i in keep]+[n+i for i in gone]
    t=r.reshape([2]*(2*n)).transpose(order)
    a,b=2**len(keep),2**len(gone)
    return np.einsum('abcb->ac',t.reshape(a,b,a,b))

vectors={
 (0,1):np.array([1,1])/np.sqrt(2),(0,-1):np.array([1,-1])/np.sqrt(2),
 (1,1):np.array([1,1j])/np.sqrt(2),(1,-1):np.array([1,-1j])/np.sqrt(2),
 (2,1):np.array([1,0]),(2,-1):np.array([0,1])}
dec=[I,S]
instrument={}
for parity in (0,1):
    allk=[]
    for y in (0,1):
        ks=[]
        for j,sign in itertools.product(range(3),(-1,1)):
            inp=vectors[j,sign]; out=vectors[j,sign*(1-2*y)]
            a=np.vdot(out,dec[parity]@inp)
            b=np.vdot(out,dec[parity]@Z@inp)
            K=H@(4*a*I+3j*b*Z)/(5*np.sqrt(6))
            ks.append(K);allk.append(K)
        instrument[parity,y]=ks
    assert np.max(np.abs(sum(k.conj().T@k for k in allk)-I))<1e-14

source_full=[embed(source,(1,4),5),embed(source,(3,4),5)]
probe_full={(p,y):[embed(k,(4,),5) for k in ks] for (p,y),ks in instrument.items()}
reset=[np.array([[1,0],[0,0]],complex),np.array([[0,1],[0,0]],complex)]
max_independence=0.; max_current_channel=0.

def simulate(N,keys=(0,0)):
    global max_independence,max_current_channel
    input_frames=embed(P[keys[0]],(1,),5)@embed(P[keys[1]],(3,),5)
    initial=input_frames@np.kron(GPHI,sig)@input_frames.conj().T
    states={(0,0):initial}; risk=0.; q=2;r=.5
    for t in range(N):
        new={}
        def add(key,state):new[key]=new.get(key,np.zeros((32,32),complex))+state
        for (used,parity),state in states.items():
            prob=np.trace(state).real
            if used==q:
                add((used,parity),state);continue
            # Global Choi premise: untouched next Bell pair is product with rest.
            target=(2*used,2*used+1)
            pair=partial(state,5,target)
            expected_pair=embed(P[keys[used]],(1,),2)@PHI@embed(P[keys[used]],(1,),2).conj().T
            max_independence=max(max_independence,float(np.max(np.abs(pair-prob*expected_pair))))
            for y in (0,1):
                post=sum(k@state@k.conj().T for k in probe_full[parity,y])
                add((used,parity^y),(1-r)*post)
            U=source_full[used]
            dd=embed(dec[parity],(2*used+1,),5)
            frame=embed(P[keys[used]].conj().T,(2*used+1,),5)
            post=frame@dd@U@state@U.conj().T@dd.conj().T@frame.conj().T
            current=partial(post,5,target)
            this_risk=prob-np.trace(PHI@current).real
            risk+=r*this_risk
            # Independently construct the conditional fresh-Bell channel from M.
            mem=partial(state,5,(4,))
            binput=embed(P[keys[used]],(1,),3)
            b=np.kron(PHI,mem);b=binput@b@binput.conj().T
            uu=embed(source,(1,2),3)
            dd3=embed(P[keys[used]].conj().T@dec[parity],(1,),3)
            b=dd3@uu@b@uu.conj().T@dd3.conj().T
            max_current_channel=max(max_current_channel,float(np.max(np.abs(current-partial(b,3,(0,1))))))
            add((used+1,parity),r*post)
        states=new
        assert abs(sum(np.trace(s).real for s in states.values())-1)<1e-12
    out=np.zeros((16,16),complex);shortfall=0.;delivered_risk=0.
    for (used,parity),state in states.items():
        prob=np.trace(state).real
        for j in range(used):
            delivered_risk+=prob-np.trace(PHI@partial(state,5,(2*j,2*j+1))).real
        if used<q:shortfall+=prob
        for j in range(used,q):
            ks=[embed(k,(2*j+1,),5) for k in reset]
            state=sum(k@state@k.conj().T for k in ks)
            frame=embed(P[keys[j]].conj().T,(2*j+1,),5)
            state=frame@state@frame.conj().T
        out+=partial(state,5,(0,1,2,3))
    ell=1-np.trace(GPHI@out).real
    assert abs(risk-delivered_risk)<1e-12
    assert ell<=risk+shortfall+1e-12
    assert np.max(np.abs(partial(out,4,(0,2))-np.eye(4)/4))<1e-12
    assert np.min(np.linalg.eigvalsh(out))>-1e-12
    return out,{'N':N,'payloads':2,'role_use_probability':.5,'shortfall':shortfall,
                'summed_delivered_bell_risk':risk,'global_bell_loss':ell,
                'delivered_marginal_identity_residual':abs(risk-delivered_risk)}

reports=[];twirl_residual=0.;offdiag=0.;fe_residual=0.
for N in (3,6):
    base,report=simulate(N);reports.append(report)
    actual=np.zeros((16,16),complex);theory=np.zeros((16,16),complex)
    for keys in itertools.product(range(4),repeat=2):
        got,_=simulate(N,keys);actual+=got/16
        U=np.eye(16,dtype=complex)
        for j in range(2):U=embed(P[keys[j]].T,(2*j,),4)@embed(P[keys[j]].conj().T,(2*j+1,),4)@U
        theory+=U@base@U.conj().T/16
        twirl_residual=max(twirl_residual,float(np.max(np.abs(got-U@base@U.conj().T))))
    bellbasis=np.column_stack([np.kron(np.kron(I,a)@phi,np.kron(I,b)@phi) for a,b in itertools.product(P,repeat=2)])
    diag=bellbasis.conj().T@actual@bellbasis
    offdiag=max(offdiag,float(np.max(np.abs(diag-np.diag(np.diag(diag))))))
    fe_residual=max(fe_residual,float(abs(np.trace(GPHI@actual)-np.trace(GPHI@base))))
    assert np.max(np.abs(actual-theory))<1e-12
assert max(max_independence,max_current_channel,twirl_residual,offdiag,fe_residual)<1e-12

p=Path(__file__)
result={'status':'PASS_DETERMINISTIC_COMPLETE_CHANNEL_ENUMERATION','source_calls':0,'rng_draws':0,
 'source_memory_qubits':1,'joint_payload_qubits':2,'full_reference_qubits':2,
 'retained_record':'mismatch parity only; axes/signs retired after their actual instruments',
 'fixtures':reports,'actual_frame_schedules':32,
 'next_untouched_bell_pair_marginal_residual':max_independence,
 'conditional_current_channel_residual':max_current_channel,
 'actual_adaptive_global_frame_identity_residual':twirl_residual,
 'global_pauli_choi_offdiagonal_residual':offdiag,
 'twirl_bell_fidelity_residual':fe_residual,
 'scope':'generic coherent memory process; not common-algebra oracle or bandit learning performance; finite complete-channel diagnostic',
 'script_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
p.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

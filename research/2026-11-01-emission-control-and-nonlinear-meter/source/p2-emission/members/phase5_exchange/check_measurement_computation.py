"""Exact checks for the measurement-based competitor, not a hardware simulation.

Checks finite-strength Bell discrimination, forced S/T teleportation,
the failed four-spin encoded-singlet teleport retry, and verified cat faults.
"""
from pathlib import Path
from itertools import product
import json
import numpy as np
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
S=np.array([0,1,-1,0],complex)/np.sqrt(2)
SP=np.outer(S,S.conj());TP=np.eye(4)-SP

def tensor(xs):
    a=np.array([[1]],complex)
    for x in xs:a=np.kron(a,x)
    return a

def pair_projector(n,i,j):
    spin=[X/2,Y/2,Z/2]
    return np.eye(2**n)/4-sum(tensor([p if k in [i,j] else I for k in range(n)]) for p in spin)

def bell_measurement():
    bells=np.column_stack([S,np.array([0,1,1,0])/np.sqrt(2),
                           np.array([1,0,0,1])/np.sqrt(2),np.array([1,0,0,-1])/np.sqrt(2)])
    XA=np.kron(X,I);ZA=np.kron(Z,I)
    q=2.43723761742892e-5
    rows=[]
    for n in [1,2,3]:
        a=q**(n/2)*np.exp(.713j)
        N=a*SP+TP; C=np.sqrt(1-q**n)*SP
        ks=[C,C@ZA@N,C@XA@N@ZA@N,N@XA@N@ZA@N]
        effects=[k.conj().T@k for k in ks]
        target=[(1-q**n)*np.outer(bells[:,i],bells[:,i].conj()) for i in range(3)]
        target.append(np.outer(bells[:,3],bells[:,3].conj())+q**n*(np.eye(4)-np.outer(bells[:,3],bells[:,3].conj())))
        residual=max(np.linalg.norm(e-t,2) for e,t in zip(effects,target))
        assert residual<3e-15
        x=q**(n/2)
        f=lambda p:.5*(x*x*p+np.sqrt(x**4*p*p+4*x*x*p*(1-p)))
        opt=minimize_scalar(lambda p:-f(p),bounds=(0,1),method='bounded')
        exact=x/(2-x)
        assert abs(-opt.fun-exact)<1e-10
        rows.append(dict(repeated_tries=n,one_singlet_miss=q,
                         destructive_bell_half_diamond=q**n,
                         nondestructive_ST_half_diamond=exact,
                         max_effect_residual=residual,
                         optimal_ST_singlet_weight=1/(2-x)))
    # Any sequence of sector-scalar Kraus operators and exact Pauli permutations
    # has Bell-diagonal effects, regardless of its reported classical labels.
    rng=np.random.default_rng(119)
    mx=0.
    for trial in range(100):
        k=np.eye(4,dtype=complex)
        for _ in range(12):
            a,b=rng.normal(size=2)+1j*rng.normal(size=2)
            a/=max(1,abs(a));b/=max(1,abs(b))
            k=(a*SP+b*TP)@k
            k=[np.eye(4),XA,ZA,XA@ZA][rng.integers(4)]@k
        e=bells.conj().T@k.conj().T@k@bells
        mx=max(mx,float(np.linalg.norm(e-np.diag(np.diag(e)),2)))
    assert mx<1e-14
    return dict(finite_strength=rows,arbitrary_history_bell_off_diagonal_residual=mx)

def forced_teleportation():
    p=pair_projector(3,1,2);q=pair_projector(3,0,1);eye=np.eye(8)
    win=np.column_stack([np.kron(np.array([1,0]),S),np.kron(np.array([0,1]),S)])
    wout=np.column_stack([np.kron(S,np.array([1,0])),np.kron(S,np.array([0,1]))])
    pending=[(eye-q)@win]
    passed=[q@win]
    rows=[]
    mx=0.
    for cycles in range(7):
        for v in passed:
            c=np.trace(wout.conj().T@v)/2
            mx=max(mx,float(np.linalg.norm(v-c*wout,2)))
        failure=sum(v.conj().T@v for v in pending)
        want=.75*(.625**cycles)
        residual=float(np.linalg.norm(failure-want*np.eye(2),2))
        assert residual<1e-14
        rows.append(dict(recovery_cycles=cycles,failure_probability=want,
                         max_pair_measurements=1+2*cycles,
                         failure_effect_residual=residual))
        following=[];passed=[]
        for v in pending:
            for r in [p,eye-p]:
                passed.append(q@r@v)
                following.append((eye-q)@r@v)
        pending=following
    assert mx<1e-14
    return dict(cases=rows,max_success_channel_residual=mx,
                initial_success_probability=.25,recovery_cycle_success_probability=.375)

def encoded_retry_failure():
    up=np.array([1,0]);down=np.array([0,1]);tp=np.kron(up,up);tm=np.kron(down,down)
    t0=(np.kron(up,down)+np.kron(down,up))/np.sqrt(2)
    code=np.column_stack([np.kron(S,S),(np.kron(tp,tm)+np.kron(tm,tp)-np.kron(t0,t0))/np.sqrt(3)])
    rho_b=code@code.conj().T/2
    m=pair_projector(8,0,4)@pair_projector(8,1,5)
    # E_A=Tr_B[(I_A tensor rho_B)M], tested on the code.
    e=np.einsum('abcb->ac',(np.kron(np.eye(16),rho_b)@m).reshape(16,16,16,16))
    logical=code.conj().T@e@code
    assert np.linalg.norm(logical-np.diag([1/8,1/24]))<1e-14
    return dict(two_cross_singlet_prefix_effect=logical.real.tolist(),
                logical_information_ratio=3.,
                all_four_cross_singlets_teleport_success_probability=1/32,
                conclusion='Fine failure/prefix records reveal the logical state; harmless forced retries do not follow.')

def propagate(x,z,gate):
    typ,*qs=gate
    if typ=='H':
        a=qs[0];x[a],z[a]=z[a],x[a]
    elif typ=='CX':
        c,t=qs;x[t]^=x[c];z[c]^=z[t]
    return x,z

def cat_faults():
    gates=[('H',0),('CX',0,1),('CX',1,2),('CX',2,3),('CX',0,4),('CX',3,4)]
    locations=[(-1,(i,),f'prepare_{i}') for i in range(5)]
    locations += [(k,tuple(g[1:]),f'gate_{k}_{g[0]}') for k,g in enumerate(gates)]
    counts=dict(total=0,accepted=0,rejected=0)
    bad=[];maxweight=0
    paulis=[(0,0),(1,0),(0,1),(1,1)]
    for after,qubits,name in locations:
        for ps in product(paulis,repeat=len(qubits)):
            if not any(x or z for x,z in ps):continue
            x=np.zeros(5,dtype=int);z=x.copy()
            for a,(xx,zz) in zip(qubits,ps):x[a]=xx;z[a]=zz
            for g in gates[after+1:]:propagate(x,z,g)
            counts['total']+=1
            if x[4]:counts['rejected']+=1;continue
            counts['accepted']+=1
            weight=min(int(x[:4].sum()),4-int(x[:4].sum()))
            maxweight=max(maxweight,weight)
            if weight>1:bad.append((name,ps,x.tolist(),z.tolist()))
    # A lone flipped verifier bit rejects a clean cat, never admits a bad one.
    counts['total']+=1;counts['rejected']+=1
    assert not bad
    return dict(counts=counts,max_data_error_weight_from_accepted_single_cat_fault=maxweight,
                cat_graph='CNOT chain0-1-2-3; verify Z0 Z3 with a fifth spin',
                note='X patterns are taken modulo the harmless XXXX cat stabilizer; cat Z errors affect syndrome records.',
                coarse_EC_locations=914,coarse_two_block_CNOT_exrec_locations=3663,
                coarse_pair_bound=3663*3662//2,
                inverse_coarse_pair_count_not_a_complete_threshold=1/(3663*3662//2),
                counting_exclusions='Routing, factory waiting, idle locations, leakage-reduction additions and classical control are not in the coarse3663 count.')

if __name__=='__main__':
    result=dict(bell=bell_measurement(),routing=forced_teleportation(),
                failed_encoded_retry=encoded_retry_failure(),cat=cat_faults())
    (ROOT/'measurement_computation_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

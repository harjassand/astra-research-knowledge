"""Independent quantum-process check, not a calibration/bandit or source-sampling run.
q=2,N=3; partial-SWAP retained memory; deliberately non-2-design TEST instruments.
Tests only global Choi, mixed occupation, isolated marginals, shortfall and twirling.
"""
import numpy as np, json, hashlib
from pathlib import Path
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
paulis=[I,X,Y,Z];plus=np.array([1,1],complex)/np.sqrt(2)
SWAP=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
U=(15*np.eye(4)+8j*SWAP)/17
assert np.max(abs(U.conj().T@U-np.eye(4)))<1e-14
bell=np.array([1,0,0,1],complex)/np.sqrt(2);Phi=np.outer(bell,bell.conj())
# Fixed order R0,Q0,R1,Q1,M. Actual delivered Q wires become isolated output wires.
vec=np.kron(np.kron(bell,bell),plus);rho_init=np.outer(vec,vec.conj())
F0=np.eye(32)-np.kron(np.kron(Phi,np.eye(4)),I)
F1=np.eye(32)-np.kron(np.kron(np.eye(4),Phi),I)
G=np.kron(Phi,Phi)
def apply(rho,K,targets):
    n=int(round(np.log2(rho.shape[0])));other=[i for i in range(n) if i not in targets];order=targets+other
    perm=order+[i+n for i in order];inv=np.argsort(perm);a=2**len(targets);b=2**len(other)
    x=rho.reshape([2]*(2*n)).transpose(perm).reshape(a,b,a,b)
    y=np.einsum('ij,jbkc,lk->iblc',K,x,K.conj(),optimize=True)
    return y.reshape([2]*(2*n)).transpose(inv).reshape(2**n,2**n)
def reset0(rho,target):
    return sum((apply(rho,np.array([[1,0],[0,0]],complex) if j==0 else np.array([[0,1],[0,0]],complex),[target]) for j in (0,1)),np.zeros_like(rho))
def trace_memory(rho):return np.trace(rho.reshape(16,2,16,2),axis1=1,axis2=3)
def run(keys,r=0.5):
    branches=[(rho_init.copy(),0,0,'')];delivered_current=0.;finished=[]
    for t in range(3):
        nxt=[]
        for rho,j,parity,h in branches:
            if j==2:finished.append((rho,j,h));continue
            D=I if parity==0 else (15*I+8j*X)/17
            # USE: same port U, same pre-frozen decoder. Keys never enter control law.
            z=apply(rho,keys[j],[2*j+1]);z=apply(z,U,[2*j+1,4]);z=apply(z,D,[2*j+1]);z=apply(z,keys[j].conj().T,[2*j+1]);z*=r
            delivered_current+=float(np.trace((F0 if j==0 else F1)@z).real)
            nxt.append((z,j+1,parity,h+'U'))
            # TEST: fixed |+>, Z readout after the same D; two actual memory Kraus branches.
            DU=np.kron(D,I)@U
            for b in (0,1):
                K=np.einsum('mij,i->mj',DU.reshape(2,2,2,2)[b],plus)
                z=apply(rho,K,[4])*(1-r)
                nxt.append((z,j,parity^b,h+'T'+str(b)))
        branches=nxt
    finished.extend((rho,j,h) for rho,j,parity,h in branches)
    final=np.zeros((32,32),complex);shortfall=0.;delivered_final=0.;record={}
    for rho,j,h in finished:
        if j<2:shortfall+=float(np.trace(rho).real)
        for i in range(j):delivered_final+=float(np.trace((F0 if i==0 else F1)@rho).real)
        for i in range(j,2):
            rho=reset0(rho,2*i+1)
            rho=apply(rho,keys[i].conj().T,[2*i+1])
        final+=rho;record[h]=float(np.trace(rho).real)
    J=trace_memory(final);loss=1-float(np.trace(G@J).real)
    assert abs(np.trace(J)-1)<1e-12 and np.linalg.eigvalsh(J).min()>-1e-12
    assert abs(delivered_current-delivered_final)<1e-12
    assert loss<=delivered_current+shortfall+1e-12
    # Role shortfall must be binomial, despite source/record adaptation.
    theory=(1-r)**3+3*r*(1-r)**2
    assert abs(shortfall-theory)<1e-12
    return J,loss,shortfall,delivered_current,record
J0,loss,beta,cost,rec0=run([I,I])
framed=np.zeros_like(J0);twirled=np.zeros_like(J0);record_gap=0.;all_stats=[]
for P in paulis:
    for Q in paulis:
        J,l,b,c,record=run([P,Q]);framed+=J/16
        V=np.kron(np.kron(np.kron(P.T,P.conj().T),Q.T),Q.conj().T)
        twirled+=V@J0@V.conj().T/16
        record_gap=max(record_gap,max(abs(record[k]-rec0[k]) for k in rec0))
        all_stats.append([l,b,c])
twirl_gap=float(np.max(abs(framed-twirled)));assert twirl_gap<1e-12
assert record_gap<1e-12
assert abs(float(np.trace(G@framed).real)-float(np.trace(G@J0).real))<1e-12
# Bell-Pauli basis diagonalization gives exact half-diamond = total nonidentity weight.
Bells=np.column_stack([np.kron(np.kron(I,P),np.kron(I,Q))@np.kron(bell,bell) for P in paulis for Q in paulis])
BP=Bells.conj().T@framed@Bells;offdiag=float(np.max(abs(BP-np.diag(np.diag(BP)))))
assert offdiag<1e-12 and min(np.diag(BP).real)>-1e-12
out={'status':'PASS','kind':'deterministic independent global-Choi algebra; zero source samples',
     'q':2,'cap':3,'role_probability':0.5,'test_is_2design':False,'bandit_claims_checked':False,
     'untwirled_global_Bell_loss':loss,'delivered_marginal_Bell_cost':cost,'shortfall_probability':beta,
     'union_plus_single_shortfall_bound':cost+beta,'actual_framing_global_twirl_max_residual':twirl_gap,
     'Choi_role_record_key_dependence':record_gap,'twirled_Bell_basis_offdiagonal':offdiag,
     'private_keys_discarded':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
root=Path(__file__).parent;source=root/'ordinary_prequential_mixed_payload_memory_service_20261028.md'
if source.exists():out['reviewed_source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
(root/'prequential_mixed_service_quantum_independent_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

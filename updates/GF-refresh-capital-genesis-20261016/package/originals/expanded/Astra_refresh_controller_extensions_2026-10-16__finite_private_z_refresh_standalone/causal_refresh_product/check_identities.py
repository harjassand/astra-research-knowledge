"""Original deterministic algebra diagnostic. Not an optimizer or proof substitute."""
import json
import numpy as np

rng = np.random.default_rng(20261016)
def herm(n):
    a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    return (a+a.conj().T)/2

def unitary(n):
    w,v=np.linalg.eigh(herm(n))
    return (v*np.exp(1j*w))@v.conj().T

def norm(a): return float(np.linalg.norm(a,2))

# Joint A has two private parity bits; joint message M copies both; bath E dim 2.
q,d=4,2
C=np.zeros((q*q*d,q*q*d),complex)
for a in range(q):
    for m in range(q):
        for e in range(d):
            C[(a*q+(m^a))*d+e,(a*q+m)*d+e]=1
U=unitary(q*d)
W=C@np.kron(np.eye(q),U)@C
K=[]
for b in range(q):
    kb=np.zeros((q*d,q*d),complex)
    for a in range(q):
        for ap in range(q):
            kb[a*d:(a+1)*d,ap*d:(ap+1)*d]=W[(a*q+b)*d:(a*q+b+1)*d,(ap*q)*d:(ap*q+1)*d]
    K.append(kb)
Zs=[np.diag([(-1)**((a>>i)&1) for a in range(q)]) for i in range(2)]
comm=max(norm(k@np.kron(z,np.eye(d))-np.kron(z,np.eye(d))@k) for k in K for z in Zs)
tp=norm(sum(k.conj().T@k for k in K)-np.eye(q*d))

# Lossless simulation of a genuinely joint-parity-dependent bath unitary.
blocks=[unitary(d) for _ in range(q)]
D=np.zeros((q*d,q*d),complex)
for a in range(q): D[a*d:(a+1)*d,a*d:(a+1)*d]=blocks[a]
WD=C@np.kron(np.eye(q),D)@C
sim=np.zeros_like(D)
leak=0
for a in range(q):
    for ap in range(q):
        sim[a*d:(a+1)*d,ap*d:(ap+1)*d]=WD[(a*q)*d:(a*q+1)*d,(ap*q)*d:(ap*q+1)*d]
        for b in range(1,q):
            leak=max(leak,norm(WD[(a*q+b)*d:(a*q+b+1)*d,(ap*q)*d:(ap*q+1)*d]))

# Contraction decomposition, including singular values 0 and 1.
n=4
L,R=unitary(n),unitary(n)
s=np.array([0.,0.23,0.71,1.])
K0=L@np.diag(s)@R.conj().T
Up=L@np.diag(s+1j*np.sqrt(1-s*s))@R.conj().T
Um=L@np.diag(s-1j*np.sqrt(1-s*s))@R.conj().T
X=np.kron(np.array([[0,1],[1,0]]),np.eye(n))
Dp=np.block([[Up,np.zeros((n,n))],[np.zeros((n,n)),np.eye(n)]])
Dm=np.block([[Um,np.zeros((n,n))],[np.zeros((n,n)),np.eye(n)]])
B=np.block([[np.zeros((n,n)),K0],[K0.conj().T,np.zeros((n,n))]])
result={
    'joint_prover_private_parity_commutator':comm,
    'induced_channel_trace_preservation':tp,
    'lossless_joint_diagonal_simulation':norm(sim-D),
    'lossless_message_reset_leakage':leak,
    'contraction_mean_identity':norm((Up+Um)/2-K0),
    'unitary_factors':max(norm(Up.conj().T@Up-np.eye(n)),norm(Um.conj().T@Um-np.eye(n))),
    'odd_generator_conjugation_identity':norm((Dp@X@Dp.conj().T+Dm@X@Dm.conj().T)/2-B),
}
assert max(result.values())<1e-12,result
print(json.dumps(result,indent=2))

#!/usr/bin/env python3
"""Independent all-operator-basis audit of two role-sealed instruments.

Compares direct private-Pauli encrypted probes with entanglement-first,
post-transport role choice, including the entire quantum memory and a
nonunitary (mixture-of-unitaries) physical channel. No hardware.
"""
import numpy as np
import json
from pathlib import Path
from scipy.linalg import expm
HERE=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
P=[I,X,Y,Z]
K0=np.array([1,0],complex);K1=np.array([0,1],complex)
phi=(np.kron(K0,K0)+np.kron(K1,K1))/np.sqrt(2)
R0=np.outer(phi,phi.conj())
probes={
    'X':[(K0+K1)/np.sqrt(2),(K0-K1)/np.sqrt(2)],
    'Y':[(K0+1j*K1)/np.sqrt(2),(K0-1j*K1)/np.sqrt(2)],
    'Z':[K0,K1]
}
Sj={'X':np.kron(X,X),'Y':-np.kron(Y,Y),'Z':np.kron(Z,Z)}
U0=expm(-1j*(.61*np.kron(Z,(I+Z)/2)+.31*np.kron(X,X)+.17*np.kron(I,Y)))
U1=expm(-1j*(.38*np.kron(X,(I+Y)/2)+.37*np.kron(Y,Z)+.11*np.kron(I,X)))
Kraus=[np.sqrt(.65)*U0,np.sqrt(.35)*U1]
B=[[] for _ in range(4)]
for A in Kraus:
    for s,p in enumerate(P):
        B[s].append(.5*np.einsum('ab,biaj->ij',p,A.reshape(2,2,2,2)))

def phys(Xi):
    return sum(A@Xi@A.conj().T for A in Kraus)

def phi_s(s,sigma):
    return sum(b@sigma@b.conj().T for b in B[s])

def direct_test(setting,sigma):
    fail=np.zeros((2,2),complex); pas=np.zeros((2,2),complex)
    for psi in probes[setting]:
        Pi=np.outer(psi,psi.conj())
        bra=np.kron(psi.conj()[None,:],I)
        for pk in P:
            frame=np.kron(pk,I)
            prepared=frame@np.kron(Pi,sigma)@frame
            output=frame@phys(prepared)@frame
            passM=bra@output@bra.conj().T
            totM=np.einsum('aiaj->ij',output.reshape(2,2,2,2))
            fail+=(totM-passM)/8
            pas+=passM/8
    return pas,fail

# Apply arbitrary complete physical Kraus to the second resource half and bath.
def candidate(sigma):
    z=np.kron(R0,sigma) # order R C M
    total=np.zeros_like(z)
    for A in Kraus:
        V=np.kron(I,A)
        total+=V@z@V.conj().T
    return total

def trace_RB(Xi):
    return np.einsum('aiaj->ij',Xi.reshape(4,2,4,2))

def ebit_test(setting,sigma):
    candidate_state=candidate(sigma)
    plus=(np.eye(4)+Sj[setting])/2
    minus=(np.eye(4)-Sj[setting])/2
    return (trace_RB(np.kron(plus,I)@candidate_state),
            trace_RB(np.kron(minus,I)@candidate_state))

def ideal_test(setting,sigma):
    target={"X":1,"Y":2,"Z":3}[setting]
    fail=sum((phi_s(s,sigma) for s,p in enumerate(P) if s and
             np.linalg.norm(p@P[target]+P[target]@p)<1e-12),np.zeros((2,2),complex))
    tot=sum((phi_s(s,sigma) for s in range(4)),np.zeros((2,2),complex))
    return tot-fail,fail

basis=[np.eye(2,dtype=complex)[i:i+1,:].conj().T@np.eye(2,dtype=complex)[j:j+1,:] for i in range(2) for j in range(2)]
# Correct basis: |i><j| as outer products.
basis=[np.outer(np.eye(2,dtype=complex)[:,i],np.eye(2,dtype=complex)[:,j].conj()) for i in range(2) for j in range(2)]
max_direct_ebit=0.;max_direct_ideal=0.;max_ebit_ideal=0.
per_setting={}
for setting in probes:
    local=[]
    for sigma in basis:
        direct=direct_test(setting,sigma)
        ebit=ebit_test(setting,sigma)
        ideal=ideal_test(setting,sigma)
        d=max(np.linalg.norm(direct[v]-ebit[v]) for v in [0,1]);
        e=max(np.linalg.norm(direct[v]-ideal[v]) for v in [0,1]);
        f=max(np.linalg.norm(ebit[v]-ideal[v]) for v in [0,1]);
        local.append((d,e,f))
        max_direct_ebit=max(max_direct_ebit,d)
        max_direct_ideal=max(max_direct_ideal,e)
        max_ebit_ideal=max(max_ebit_ideal,f)
    per_setting[setting]={'max_entanglement_first_vs_direct':max(v[0] for v in local),
                          'max_direct_vs_positive':max(v[1] for v in local),
                          'max_entanglement_first_vs_positive':max(v[2] for v in local)}
assert max(max_direct_ebit,max_direct_ideal,max_ebit_ideal)<2e-13

# The same bath CP map for every hidden fault label s, in both USE variants.
# EPR Bell projection on RB before teleportation returns Phi_s.
max_bellmap=0.
for s,p in enumerate(P):
    beta=np.kron(I,p)@phi
    bra=np.kron(beta.conj()[None,:],I)
    for sigma in basis:
        sampled=bra@candidate(sigma)@bra.conj().T
        max_bellmap=max(max_bellmap,np.linalg.norm(sampled-phi_s(s,sigma)))
assert max_bellmap<2e-13

# Joint CP map for TEST after hiding the setting: bad test weight exactly 2/3 W.
W=sum((b.conj().T@b for group in B[1:] for b in group),np.zeros((2,2),complex))
W_effect=0.0
for target in [np.eye(2), np.outer(K0,K0.conj()), np.outer(K1,K1.conj())]:
    f_3=sum(np.trace(ebit_test(j,target)[1]) for j in probes)/3
    w_expect=(2/3)*np.trace(W@target)
    W_effect=max(W_effect,abs(f_3-w_expect))
assert W_effect<1e-12

res={
 'physical_channel':'mixture of two noncommuting quantum system-memory unitaries (two Kraus maps)',
 'resource_type':'one perfect local ebit; one half through identical unknown channel',
 'fully_retired_fine_test_records':True,
 'per_public_test_axis_all_matrix_unit_operator_residuals':per_setting,
 'max_complete_memory_instrument_direct_vs_ebit':max_direct_ebit,
 'max_direct_vs_positive_Pauli_fault_instrument':max_direct_ideal,
 'max_ebit_vs_positive_Pauli_fault_instrument':max_ebit_ideal,
 'ebit_Bell_sector_effect_and_memory_CP_map_residual':max_bellmap,
 'three_setting_fault_effect_residual':float(W_effect),
 'bad_bath_effect_eigenvalues':np.linalg.eigvalsh(W).tolist(),
 'scope':'TEST both pass/fail CP memory instruments; USE Bell-sector maps. Correlation/past-memory state arbitrary by linearity.'
}
(HERE/'ebit_vs_encrypted_instrument_results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))

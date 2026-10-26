#!/usr/bin/env python3
"""Executable complete-system checks for ASTRA's causal-role-sealed service.

No hardware data. All memory is represented in this VALIDATION script,
never presumed visible to the hypothetical received-record controller.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1.0, -1.0]).astype(complex)
P = [I, X, Y, Z]
ket0 = np.array([1.,0.], dtype=complex)
ket1 = np.array([0.,1.], dtype=complex)
ketplus = (ket0 + ket1) / np.sqrt(2)
ketminus = (ket0 - ket1) / np.sqrt(2)
ketplusy = (ket0 + 1j *ket1)/np.sqrt(2)
ketminusy = (ket0 - 1j*ket1)/np.sqrt(2)
STATES = [ket0,ket1,ketplus,ketminus,ketplusy,ketminusy]
BELL = (np.kron(ket0,ket0)+np.kron(ket1,ket1))/np.sqrt(2)
rho_bell = np.outer(BELL,BELL.conj())

def htrace(A):
    return float(np.real(np.trace(A)))

def dtrace(A,B):
    return float(0.5*np.sum(np.abs(np.linalg.eigvalsh((A-B+(A-B).conj().T)/2))))

def adj(U, rho):
    return U @ rho @ U.conj().T

def ptrace_qubit(M, dim=2):
    return np.einsum('aiaj->ij', M.reshape(2,dim,2,dim))

def coeffs(U, dim=2):
    Ut=U.reshape(2,dim,2,dim)
    return [0.5*np.einsum('ab,biaj->ij', p,Ut) for p in P]

def full_twirl(U, rho):
    return sum(adj(np.kron(p,I)@U@np.kron(p,I),rho) for p in P)/4

def diag_twirl(B, rho):
    return sum(adj(np.kron(p,b),rho) for p,b in zip(P,B))

def test_effect(U, keys=range(4)):
    F=np.zeros((2,2), dtype=complex)
    for psi in STATES:
        proj=np.outer(psi,psi.conj())
        prep=np.kron(psi[:,None],I) # 4x2 isometry
        q=np.kron(I-proj,I)
        for k in keys:
            V=np.kron(P[k],I)@U@np.kron(P[k],I)
            A=V@prep
            F+= A.conj().T@q@A
    return F/(6*len(keys))

def weighted_input(weights,rho):
    return sum(w*adj(np.kron(p,I),rho) for w,p in zip(weights,P))

rng=np.random.default_rng(261026)
H=0.60*np.kron(Z,(I+Z)/2)+0.30*np.kron(X,X)+0.11*np.kron(I,Y)
U=expm(-1j*H)
B=coeffs(U)
recon=sum(np.kron(p,b) for p,b in zip(P,B))
W=sum(b.conj().T@b for b in B[1:])
F=test_effect(U)
assert np.linalg.norm(U-recon) < 1e-13
assert np.linalg.norm(F-(2/3)*W) < 1e-13
assert abs(np.linalg.eigvalsh(W)[0])<1.01

states=[]
for _ in range(25):
    T=rng.standard_normal((4,4))+1j*rng.standard_normal((4,4))
    rho=T@T.conj().T/np.trace(T@T.conj().T)
    states.append(rho)
states += [rho_bell, np.kron(np.outer(ketplus,ketplus),np.outer(ket0,ket0))]
max_twirl=max(dtrace(full_twirl(U,rho),diag_twirl(B,rho)) for rho in states)
# Same coherent input-bath state in USE versus memory marginal in TEST.
use_full=weighted_input([.25]*4, rho_bell)
test_in=np.kron(I/2,I/2)
use_one_bit=(rho_bell+adj(np.kron(X,I),rho_bell))/2
one_bit_adv=dtrace(use_one_bit,test_in)
full_adv=dtrace(use_full,test_in)
# Full-information bath makes total-variation role leakage tight for biased keys.
p=[0.4,0.3,0.2,0.1]
tv=.5*sum(abs(pk-.25) for pk in p)
bias_input=weighted_input(p,rho_bell)
bias_adv=dtrace(bias_input,test_in)
assert abs(bias_adv-tv)<1e-12
assert abs(one_bit_adv-.5)<1e-12
assert full_adv<1e-12
assert max_twirl<1e-12

# Decoherence witness: if two-input branches are indistinguishable before
# the call, no quantum instrument applied to that joint input can distinguish.
max_output_diff=0.
for _ in range(12):
    HH=rng.standard_normal((4,4))+1j*rng.standard_normal((4,4))
    HH=(HH+HH.conj().T)/2
    V=expm(-1j*HH*.1)
    max_output_diff=max(max_output_diff,dtrace(adj(V,use_full),adj(V,test_in)))
assert max_output_diff<1e-12

# For a biased key, one channel comparison has complete-boundary half-distance
# at most the key's TV from uniform, even on an entangled input/bath.
max_actual_vs_ideal=0.
for rho in states:
    bad=sum(w*adj(np.kron(P[k],I)@U@np.kron(P[k],I),rho) for k,w in enumerate(p))
    good=full_twirl(U,rho)
    max_actual_vs_ideal=max(max_actual_vs_ideal,dtrace(bad,good))
assert max_actual_vs_ideal<=tv+1e-12

# A fixed key reused on two uses is not a two-use Pauli twirl.
# Coherent X and Z rotations create interference between different uses.
Uone=expm(-1j*.23*Z)
Utwo=np.kron(Uone,Uone)
P2=[np.kron(p,q) for p in P for q in P]
mixture_independent=sum(adj(k@Utwo@k,rho_bell) for k in P2)/16 # arbitrary 2-qubit state
mixture_same=sum(adj(np.kron(p,p)@Utwo@np.kron(p,p),rho_bell) for p in P)/4
reuse_discrepancy=dtrace(mixture_same,mixture_independent)
# This particular Bell state can be a symmetry; also test product input.
rho_pp=np.outer(np.kron(ketplus,ketplus),np.kron(ketplus,ketplus).conj())
ind_pp=sum(adj(k@Utwo@k,rho_pp) for k in P2)/16
same_pp=sum(adj(np.kron(p,p)@Utwo@np.kron(p,p),rho_pp) for p in P)/4
reuse_discrepancy=max(reuse_discrepancy,dtrace(same_pp,ind_pp))
assert reuse_discrepancy>1e-4

# Calibration of mismatch effect, algebraic one-step e-process inequality.
nu=2/3
p_test=.35
z=1.12
a=1-(1-p_test)*(z-1)/(p_test*nu)
assert 0<a<1
# Perturb ideal TEST mismatch effect toward zero by 7% loss of reporting.
F_actual=.93*F
EPS=float(max(0.,np.linalg.eigvalsh(F-F_actual)[-1]))
c=1+p_test*(1-a)*EPS
LHS=(1-p_test)*(I+(z-1)*W)+p_test*(I-(1-a)*F_actual)
max_eig=float(np.linalg.eigvalsh((LHS+LHS.conj().T)/2)[-1])
assert max_eig<=c+1e-12

results={
    'scope': 'Finite-dimensional reference; arbitrary future-accessible bath memory is retained in every checked channel',
    'complete_Pauli_expansion_residual_frobenius': float(np.linalg.norm(U-recon)),
    'full_memory_positive_twirl_max_half_trace_residual': max_twirl,
    'full_memory_three_basis_test_effect_residual_operator': float(np.linalg.norm(F-(2/3)*W)),
    'hidden_bath_bad_effect_eigenvalues': np.linalg.eigvalsh(W).tolist(),
    'full_pad_test_use_advantage': full_adv,
    'one_bit_pad_role_distinguishing_trace_distance':one_bit_adv,
    'one_bit_pad_role_guess_success':(1+one_bit_adv)/2,
    'biased_pad_TV_from_uniform':tv,
    'biased_pad_role_distinguishing_trace_distance':bias_adv,
    'biased_pad_max_full_boundary_output_distance':max_actual_vs_ideal,
    'max_role_distinguishing_after_unknown_memory_unitaries':max_output_diff,
    'two_round_reused_key_failure_half_trace_distance':reuse_discrepancy,
    'mismatched_test_effect_epsilon':EPS,
    'weighted_effect_supermartingale_constant_c':c,
    'weighted_effect_max_eigenvalue':max_eig,
    'weighted_effect_slack':c-max_eig,
    'fixed_test_parameters':{'p':p_test,'z':z,'a':a,'nu':nu}
}
(HERE/'causal_role_sealing_exact_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))

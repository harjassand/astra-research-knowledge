"""Verify the root's gap-free three-query singlet projector on all six spins.

Includes the complete final helper instrument, concurrent noncommuting logical
controls, and insertions of single physical active-coupler faults throughout
the positive-exchange implementation.  No effective Hamiltonian is used.
"""
from functools import reduce
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh, expm

I2 = np.eye(2)
paulis = [np.array([[0,1],[1,0]])/2,
          np.array([[0,-1j],[1j,0]])/2,
          np.diag([1,-1])/2]


def kron(xs):
    return reduce(np.kron, xs)


def spins(n):
    return [[kron([p if k==i else I2 for k in range(n)])
             for p in paulis] for i in range(n)]


sd, s = spins(4), spins(6)
JD = [sum(sd[i][a] for i in range(4)) for a in range(3)]
JD2 = sum(A@A for A in JD)
ev, vec = eigh(JD2)
bases = [vec[:, np.abs(ev-j*(j+1))<1e-8] for j in range(3)]
P0, P1, P2 = [q@q.conj().T for q in bases]
C0 = bases[0]
singlet = np.array([0,1,-1,0])/np.sqrt(2)
triplets = [np.array([1,0,0,0]), np.array([0,1,1,0])/np.sqrt(2), np.array([0,0,0,1])]
V = np.kron(np.eye(16), singlet[:,None])
P = V@V.conj().T
phi = np.arccos(1/3)
Rp = np.eye(64)+(np.exp(1j*phi)-1)*P
Rm = Rp.conj().T
helper_exchange = sum(s[4][a]@s[5][a] for a in range(3))
rest_controls = [sum(s[i][a]@s[j][a] for a in range(3))
                 for i,j in [(1,2),(2,3),(1,3)]]
rest_controls_d = [sum(sd[i][a]@sd[j][a] for a in range(3))
                   for i,j in [(1,2),(2,3),(1,3)]]


def star(site):
    es = [sum(s[i][a]@s[4][a] for a in range(3))
          for i in range(4) if i!=site]
    es.append(sum(s[site][a]@s[5][a] for a in range(3)))
    return sum(es), es


H, edges = star(0)
U = expm(-1j*np.pi*H)
Uinverse_positive = expm(-3j*np.pi*H)
R = [sum(sd[i][a] for i in [1,2,3]) for a in range(3)]
R2 = sum(A@A for A in R)
D = P1@(R2-.75*np.eye(16))/3
K = V.conj().T@U@V
C = U@Rp@Uinverse_positive@Rm@U
KC = V.conj().T@C@V
expected_K = -1j*P0-(D+P2)/2
results = dict(
    query_operator_error=float(np.linalg.norm(K-expected_K,2)),
    positive_inverse_error=float(np.linalg.norm(Uinverse_positive-U.conj().T,2)),
    query_period_error=float(np.linalg.norm(expm(-4j*np.pi*H)-np.eye(64),2)),
    composite_projector_error=float(np.linalg.norm(KC+1j*P0,2)),
    composite_leakage_amplitude=float(np.linalg.norm(KC@(P1+P2),2)),
    phi=float(phi), star_exchange_time=float(5*np.pi),
    helper_exchange_time=float(2*np.pi))
assert max(results[x] for x in ["query_operator_error", "positive_inverse_error",
                               "query_period_error", "composite_projector_error"])<1e-12

# Physical helper exchange pulses implement R's up to an irrelevant overall phase.
Hp = expm(-1j*phi*helper_exchange)
Hm = expm(-1j*(2*np.pi-phi)*helper_exchange)
Cphys = U@Hp@Uinverse_positive@Hm@U
overlap = np.trace(C.conj().T@Cphys)/64
results["physical_pulse_implementation_error"] = float(np.linalg.norm(Cphys-overlap*C,2))
assert results["physical_pulse_implementation_error"]<1e-12

outcomes = [singlet]+triplets
kraus = []
for t in outcomes:
    Vt = np.kron(np.eye(16), t[:,None])
    kraus.append(Vt.conj().T@C@V)
triplet_effect = sum(k.conj().T@k for k in kraus[1:])
results["fine_instrument_completeness_error"] = float(np.linalg.norm(sum(k.conj().T@k for k in kraus)-np.eye(16),2))
results["triplet_effect_projector_error"] = float(np.linalg.norm(triplet_effect-(np.eye(16)-P0),2))
results["max_code_to_triplet_amplitude"] = float(max(np.linalg.norm(k@C0,2) for k in kraus[1:]))
assert max(results[x] for x in ["fine_instrument_completeness_error", "triplet_effect_projector_error", "max_code_to_triplet_amplitude"])<1e-12

# Every untouched-three exchange commutes with every filtering primitive.
results["commutator_norms"] = [float(np.linalg.norm(H@h-h@H,2)) for h in rest_controls]
results["control_algebra_commutator"] = float(np.linalg.norm(C0.conj().T@(rest_controls_d[0]@rest_controls_d[1]-rest_controls_d[1]@rest_controls_d[0])@C0,2))
assert max(results["commutator_norms"])<1e-14
assert results["control_algebra_commutator"]>.1

# Noncommuting local controls at different times while filtering is active.
durations = [np.pi, 2*np.pi-phi, 3*np.pi, phi, np.pi]
generators = [H, helper_exchange, H, helper_exchange, H]
coefficients = [[.13, .21, .08], [.3,.1,.04], [.17,.05,.31], [.03,.14,.28], [.19,.12,.07]]
total = np.eye(64,dtype=complex)
local_d = np.eye(16,dtype=complex)
for t,G,c in zip(durations,generators,coefficients):
    h = sum(x*A for x,A in zip(c,rest_controls))
    hd = sum(x*A for x,A in zip(c,rest_controls_d))
    total = expm(-1j*t*(G+h))@total
    local_d = expm(-1j*t*hd)@local_d
controlled_k = V.conj().T@total@V
physical_alpha = np.trace(P0@(V.conj().T@Cphys@V))/2
results["concurrent_gate_full_pass_error"] = float(np.linalg.norm(controlled_k-physical_alpha*local_d@P0,2))
assert results["concurrent_gate_full_pass_error"]<1e-12

# Single active-edge exchange errors, including arbitrary occurrence times.
# These have exactly zero accepted logical amplitude for pure S_r dot s_a.
sequence = [U,Rm,Uinverse_positive,Rp,U]
max_code_edge = 0.
max_scalar_edge = 0.
count = 0
for seg in [0,2,4]:
    duration = np.pi if seg!=2 else 3*np.pi
    pre, post = np.eye(64,dtype=complex), np.eye(64,dtype=complex)
    for q in range(seg): pre=sequence[q]@pre
    for q in range(seg+1,5): post=sequence[q]@post
    for tau in np.linspace(0,duration,9):
        before,after = expm(-1j*tau*H)@pre,post@expm(-1j*(duration-tau)*H)
        for e in edges:
            L=C0.conj().T@V.conj().T@after@e@before@V@C0
            max_code_edge=max(max_code_edge,float(np.linalg.norm(L,2)))
            theta=.371
            fault=expm(-1j*theta*e)
            Lunitary=C0.conj().T@V.conj().T@after@fault@before@V@C0
            max_scalar_edge=max(max_scalar_edge,float(np.linalg.norm(Lunitary-np.trace(Lunitary)*np.eye(2)/2,2)))
            count+=1
results["active_coupler_error_insertions"]=count
results["max_accepted_pure_coupler_error"] = max_code_edge
results["max_accepted_exchange_rotation_traceless"] = max_scalar_edge
assert max(max_code_edge,max_scalar_edge)<1e-12

# A continuous mismatch supplies repeated insertions, and has a second-order
# accepted logical error. This is not exact tolerance of arbitrary calibration.
results["continuous_mismatch"] = []
for eps in [1e-4,1e-3,1e-2,.1]:
    Hbad=H+eps*edges[0]
    Ubad=expm(-1j*np.pi*Hbad)
    Ubad_inv=expm(-3j*np.pi*Hbad)
    Cbad=Ubad@Rp@Ubad_inv@Rm@Ubad
    Kbad=C0.conj().T@V.conj().T@Cbad@V@C0
    traceless=np.linalg.norm(Kbad-np.trace(Kbad)*np.eye(2)/2,2)
    results["continuous_mismatch"].append(dict(epsilon=eps,accepted_logical_traceless=float(traceless),over_epsilon_squared=float(traceless/eps**2)))

# Essential contrast: an intra-data exchange error is not erased by the filter.
F=np.kron(rest_controls_d[0],np.eye(4))
L=C0.conj().T@V.conj().T@C@F@V@C0
results["undetected_intra_data_exchange_traceless"] = float(np.linalg.norm(L-np.trace(L)*np.eye(2)/2,2))
assert results["undetected_intra_data_exchange_traceless"]>.4

# Magnetic faults during the verifier cannot become code-space logical faults,
# but a late fault can survive as unflagged leakage. This is an explicit boundary.
results["late_magnetic_faults"] = []
prefix = Rp@Uinverse_positive@Rm@U
max_vector_code = 0.
for remaining in [np.pi, np.pi/2, .1, .01, .001, 0.]:
    tau = np.pi-remaining
    before = expm(-1j*tau*H)@prefix
    after = expm(-1j*remaining*H)
    z_error = 2*s[0][2]  # unitary Pauli Z on the singled-out data spin
    F = after@z_error@before
    Kfault = V.conj().T@F@V@C0
    code = np.linalg.norm(C0.conj().T@Kfault,2)
    leak = np.linalg.norm(P1@Kfault,2)
    max_vector_code=max(max_vector_code,float(code))
    results["late_magnetic_faults"].append(dict(
        remaining_star_time=float(remaining),
        worst_unflagged_leakage_probability=float(leak**2),
        accepted_code_amplitude=float(code)))
assert max_vector_code<1e-12
assert results["late_magnetic_faults"][-1]["worst_unflagged_leakage_probability"]>1-1e-12

out=Path(__file__).with_name("exact_star_projector_results.json")
out.write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))

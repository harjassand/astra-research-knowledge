"""Full finite-Hubbard entangler followed by two physical singlet verifiers.

The full4900-state eight-site charge evolution independently verifies a
two-parameter gate calibration. An explicit all-data charge check then joins
the propagated gate to the exact SU(2),S3 reconstruction of the separately
computed400-state physical verifier. Both use U=1 and40/U ramps. This is a
complete flagged gate cell in the stated Hubbard/ideal-charge-read model.
"""
import sys,json,time
from pathlib import Path
from itertools import combinations
from math import sqrt,pi
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from phase4_hubbard.check_finite_hubbard import fock_basis,hopping_matrix,ramp
from phase4_exact_spin.check_hubbard_entangler import code

ROOT=Path(__file__).resolve().parent.parent
def tensor(xs):
    a=np.array([[1]],complex)
    for x in xs:a=np.kron(a,x)
    return a
def filter_matrix(row):
    pauli=[np.array([[0,1],[1,0]])/2,np.array([[0,-1j],[1j,0]])/2,np.diag([1,-1])/2]
    s=[[tensor([p if k==i else np.eye(2) for k in range(4)]) for p in pauli] for i in range(4)]
    total=[sum(s[i][a] for i in range(4)) for a in range(3)]
    rest=[sum(s[i][a] for i in range(3)) for a in range(3)]
    S2=sum(x@x for x in total);R2=sum(x@x for x in rest);I=np.eye(16)
    P0=(S2-2*I)@(S2-6*I)/12;P1=S2@(6*I-S2)/8;P2=S2@(S2-2*I)/24
    Rh=(3.75*I-R2)/3
    ps={'code':P0,'j1_rest_half':P1@Rh,'j1_rest_threehalf':P1@(I-Rh),'j2':P2}
    K=sum(complex(*row['sector_stats'][k]['accepted_amplitude'])*p for k,p in ps.items())
    return K

def main():
    started=time.time()
    cal=json.loads((ROOT/'phase4_exact_spin/hubbard_entangler_calibration_results.json').read_text())
    filt=json.loads((ROOT/'phase4_hubbard/refined_charge_closure_results.json').read_text())['selected_point_fine']
    pair=json.loads((ROOT/'phase4_hubbard/fourth_order_and_pair_cycle_results.json').read_text())
    q_read=pair['helper_pair_cycle']['read_singlet_false_triplet_probability']
    basis=fock_basis(8,4,4);lookup={w:k for k,w in enumerate(basis)}
    doubles=np.array([sum(((w>>(2*i))&3)==3 for i in range(8)) for w in basis])
    H0=diags(doubles,dtype=complex).tocsr()
    hi=hopping_matrix(basis,list(combinations(range(4),2))+list(combinations(range(4,8),2)))
    hx=hopping_matrix(basis,[(i,j) for i in [0,1] for j in [4,5]])
    V=cal['t_intra_over_U']*hi+cal['t_cross_over_U']*hx
    B=code();load=np.zeros((len(basis),4),complex);extract=[]
    for n in range(256):
        if n.bit_count()!=4:continue
        w=sum(1<<(2*i+((n>>(7-i))&1)) for i in range(8))
        load[lookup[w]]=B[n];extract.append((n,lookup[w]))
    cases=[];prev=None
    for steps in [80,160]:
        state=ramp(load.copy(),H0,V,40.,steps,False)
        state=expm_multiply(-1j*cal['optimized_plateau']*(H0+V),state)
        state=ramp(state,H0,V,40.,steps,True)
        G=np.zeros((256,4),complex)
        for n,k in extract:G[n]=state[k]
        L=B.conj().T@G
        phases=np.angle(np.diag(L))
        Ulogical=np.diag(np.exp(1j*phases))
        cp_phase=np.angle(L[3,3]*L[0,0]/(L[1,1]*L[2,2]))
        KF=filter_matrix(filt)
        A=np.kron(KF,KF)@G
        alpha=filt['accepted_code_scalar']
        filter_phase=complex(*alpha)**2/abs(complex(*alpha))**2
        target=filter_phase*(B@Ulogical)
        accepted_gate_error=float(np.linalg.norm(A-target,2))
        reject=float(np.linalg.eigvalsh(np.eye(4)-A.conj().T@A)[-1])
        A_read=(1-q_read)*A
        delta_read=float(np.linalg.norm(A_read-target,2))
        reject_read=float(np.linalg.eigvalsh(np.eye(4)-A_read.conj().T@A_read)[-1])
        row=dict(ramp_steps=steps,
                 gate_norm_preservation=float(np.linalg.norm(state.conj().T@state-np.eye(4),2)),
                 gate_worst_code_rejection=float(np.linalg.eigvalsh(np.eye(4)-L.conj().T@L)[-1]),
                 gate_worst_charge_probability=float(np.linalg.eigvalsh(np.eye(4)-G.conj().T@G)[-1]),
                 gate_accepted_code_offdiagonal=float(np.linalg.norm(L-np.diag(np.diag(L)),2)),
                 gate_phase_angles=phases.tolist(),actual_conditional_phase=float(cp_phase),
                 joint_pass_operator_deviation=accepted_gate_error,
                 joint_worst_reject_probability=reject,
                 joint_residual_spin_leakage_amplitude=float(np.linalg.norm(A-B@(B.conj().T@A),2)),
                 ideal_read_half_diamond_upper_bound=accepted_gate_error+reject/2,
                 conversion_included_pass_deviation=delta_read,
                 conversion_included_worst_reject_probability=reject_read,
                 conversion_included_half_diamond_upper_bound=delta_read+reject_read/2)
        if prev is not None:row['full_gate_refinement_operator_difference']=float(np.linalg.norm(G-prev,2))
        prev=G;cases.append(row)
    report=dict(full_gate_dimension=len(basis),filter_dimension=400,
                U_over_J_nominal=50.,t_intra_over_U=cal['t_intra_over_U'],
                t_cross_over_U=cal['t_cross_over_U'],cross_J_nominal_ratio=cal['optimized_cross_J_ratio'],
                gate_full_duration_U_units=cal['total_gate_duration'],
                filter_full_duration_U_units=filt['total_duration_U_units'],
                helper_preparation_duration_U_units=480.,read_conversion_duration_U_units=480.,
                successful_preparation_control_duration_parallel_filters_U_units=cal['total_gate_duration']+filt['total_duration_U_units']+960.,
                read_conversion_false_negative=q_read,
                assumptions=['Heralded successful helper singlet preparation',
                             'Ideal spin-blind charge check after entangler and after each verifier',
                             'Two helper pairs and independent verifier controls operated in parallel',
                             'Ideal final charge detectors after the specified finite read conversion',
                             'Flagged data discarded/replaced by an erasure symbol; no recovery implied',
                             'No spin anisotropy, magnetic noise, uncontrolled OFF hopping, or extra orbitals',
                             'Calibrated target phase of actual accepted gate, not uncorrected sqrt7 phase'],
                cases=cases,wall_seconds=time.time()-started)
    (ROOT/'phase4_exact_spin/joint_hubbard_cell_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

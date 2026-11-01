"""Exact physical CNOT recompilation and explicit sufficient lifetime ledger.

This consumes the new common-scattering force loop in the inherited b=0
7x7 boundary proof. It does NOT claim a new persistent-defect CNOT theorem,
hardware benchmark, or a tight logical-error estimate.
"""
from pathlib import Path
import json, math
import numpy as np
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent

def main():
    I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
    Z=np.diag([1,-1]).astype(complex);H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2)
    S=np.diag([1,1j]);Ht=np.kron(I,H);SS=np.kron(S,S)
    zz=np.kron(Z,Z);U=np.diag(np.exp(1j*math.pi/4*np.diag(zz)))
    C=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
    got=Ht@SS@U@Ht
    residual=float(np.linalg.norm(got-np.exp(1j*math.pi/4)*C,ord=2))
    post=Ht@SS
    zc=np.kron(Z,I);zt=np.kron(I,Z);xt=np.kron(I,X)
    propagation=[float(np.linalg.norm(post@zc@post.conj().T-zc,ord=2)),
                 float(np.linalg.norm(post@zt@post.conj().T-xt,ord=2))]
    assert residual<1e-14 and max(propagation)<1e-14
    pulse=json.loads((HERE.parent/'physical_mechanisms/one_bus_parity_results.json').read_text())['optimized_safe']
    Gx=pulse['gram_real'][0][0];Gy=pulse['gram_real'][1][1]
    nb=.1;pd=-math.expm1(-8*(2*nb+1)*Gx)/2;pa=-math.expm1(-2*(2*nb+1)*Gy)/2
    p1=-math.expm1(-2*(2*nb+1)*Gx)/2;p2=pa
    er=9.701352053304095e-7
    Tmeter=10.984;Tgate=pulse['T']+.15
    Trec_base=8*Tmeter+.1
    Ttxn_base=Tgate+Trec_base
    modules=217;calls=672;entanglers=49;L=320;vres=1e-7
    # T_outer is a symbolic actual latency. We print affine coefficients,
    # not an acquired controller throughput or a vanishing time assumption.
    force_coefficient=4*math.sqrt(L)*vres
    force_base=modules*force_coefficient*Ttxn_base
    force_latency_coefficient=modules*force_coefficient
    Bcp=calls*(pd+pa+2*er)+entanglers*(p1+p2)
    Rcp=math.expm1(Bcp)-Bcp
    Bwithforce=Bcp+force_base
    Rwithforce=math.expm1(Bwithforce)-Bwithforce
    targets=[]
    for rectangles,goal in [(1,1e-3),(1000,1e-2),(6250,1e-2)]:
        rhs=math.log1p(goal)/rectangles
        required=brentq(lambda B:math.expm1(B)-B-rhs,1e-12,1)
        targets.append({'rectangles':rectangles,'target_half_logical_distance':goal,
              'required_uniform_B_before_global_startup_tail_and_strong_terms':required})
    force_cap_coeff=2*math.sqrt(L+1)*math.exp((64-.4*L)/2)
    out={
      'exact_matrix_checks':{'cnot_residual_operator_norm':residual,
           'postgate_Pauli_propagation_residuals':propagation},
      'single_physical_gate':{'order':['H_target','common_scattering_loop','S_control_and_S_target_parallel','H_target'],
           'interaction_time':pulse['T'],'each_local_slot_time':.05,
           'total_time':Tgate,'peak_shared_force':pulse['peak_total_force_gate'],
           'derived_p_Z_control':p1,'derived_p_X_target':p2,
           'channel':'CNOT followed by derived independent Z_control and X_target channels, tensor free bus channel'},
      'inherited_consumer_scope':{'code':'two7x7 Bacon-Shor blocks, no persistent strongD',
           'incoming_component_maxima':[1,1,1,1],'after_ideal_cnot':[1,2,2,1],
           'with_one_fresh_event_whole_transaction':[2,3,3,2],
           'recovery_restores_incoming_boundary':True,
           'persistent_defect_CNOT_claimed':False},
      'hard_capped_transaction':{'data_qubits':98,'gauge_bus_modules':168,
           'bounded_gauge_ancillas':168,'interblock_gate_buses':49,'total_bus_modes':217,
           'parity_calls_at_hard_cap':calls,'physical_interblock_loops':entanglers,
           'recovery_calendar_excluding_outer_latency':Trec_base,
           'transaction_calendar_excluding_outer_latency':Ttxn_base,
           'actual_total_calendar':'89.962/g + T_outer; every actual decoder/refresh/wait latency belongs to T_outer unless already in meter slots',
           'gate_bus_passive_cooling':'4.472/g including.1/g ramps during first recovery period; forces physically off except admitted residuals; no added serial time',
           'all_buses_exposed_through_entire_calendar':True},
      'partial_bound_ledger':{'nominal_CP_weight_sum':Bcp,
           'residual_force_uniform_norm_at_zero_extra_latency':force_base,
           'residual_force_norm_per_extra_gT_outer':force_latency_coefficient,
           'per_rectangle_degree2_majorant_CP_only':Rcp,
           'per_rectangle_degree2_majorant_CP_plus_force_at_zero_extra_latency':Rwithforce,
           'force_cap_global_remainder_coefficient_times_total_force_action':force_cap_coeff,
           'unknown_additions':['actual_T_outer','data_relaxation_and_dephasing','local_control_and_leakage','microscopic_chi_Kerr_and_other_nonlinearity','uniform_gate_calibration','ADC_detector_and_controller_faults','strong_domain_onsets_or_common_events'],
           'interpretation':'These are components of a conservative UPPER bound, not lower bounds on device error. They already fail to certify the illustrative long computation target; tighter analysis could improve them.'},
      'illustrative_accuracy_conditions':targets,
      'provenance':'Exact gate/channel from Phase8; deterministic boundary consumed from unmodifiedPhase7. No resource advantage over other encodings is inferred.'}
    (HERE/'consumed_cnot_and_lifetime_ledger_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()

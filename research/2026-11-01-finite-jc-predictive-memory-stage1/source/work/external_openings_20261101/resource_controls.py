"""Collector alternatives, finite control precision and coherent-probe control.

All values are required model budgets or algebraic diagnostics, not measured
component specifications. The balanced tree is ordinary passive optics.
"""
import hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.special import gammaln
from receiver_frontier import block,finite_count_test
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/external_openings_20261101'
def main():
    selected=json.loads((OUT/'receiver_bounds.json').read_text())['best'];r=selected['block'];t=selected['test']
    ell=r['ell'];depth=int(math.log2(ell));zeta=r['selector_transmission'];sb=r['heterodyne_transmission']*(r['eta']*r['n']+r['b'])
    delta=1e-8;cap=math.sqrt((1+sb)*math.log(2*ell/delta));bits=12;step=2*cap/(2**bits-1)
    relative_error=step/math.sqrt(1+sb)
    adc_alignment=((1-relative_error)/(1+relative_error))**2
    norm_failure=math.exp(-ell*(math.log(2)-.5))
    # A unitary error e moves a normalized selected row by <=e. Then
    # inner-product magnitude >=sqrt(A_ADC)-e and squared alignment is
    # at least its square. Product-unitary errors add along the circuit.
    remaining_error=math.sqrt(adc_alignment)-math.sqrt(r['alignment'])
    assert remaining_error>0
    # Full independent 32-mode balanced network. The first layer contains
    # observed phases; each subsequent combiner uses child norms.
    rng=np.random.default_rng(2026110113);zs=rng.normal(size=32)+1j*rng.normal(size=32)
    u=np.diag(zs/abs(zs));nodes=[(i,abs(zs[i])) for i in range(32)]
    while len(nodes)>1:
        new=[]
        for (left,a),(right,b) in zip(nodes[::2],nodes[1::2]):
            norm=math.hypot(a,b);co=a/norm;si=b/norm
            old=u[left].copy();incoming=u[right].copy()
            u[left]=co*old+si*incoming;u[right]=-si*old+co*incoming
            new.append((left,norm))
        nodes=new
    row_error=float(np.max(abs(u[0]-zs/np.linalg.norm(zs))))
    unitary_error=float(np.linalg.norm(u.conj().T@u-np.eye(32),2))
    assert row_error<1e-13 and unitary_error<1e-13
    # Phase-only prior: use an exact finite lower-tail bound for a sum of
    # independent Rayleigh amplitudes via Gaussian concentration. This
    # only tests this sufficient bound; it is not a no-go for that receiver.
    y=r['retention']*r['n'];ym=r['memory_transmission']*y
    a=r['heterodyne_transmission']*r['eta']*r['retention']*r['memory_transmission']*r['n']*(1+r['n'])/(1+sb)
    v=zeta*(ym-a)+r['added_occupation'];p_tail=(y/(1+y))**2
    phase_rows=[]
    for fail in (1e-3,1e-5,1e-7):
        rayleigh_lower=math.sqrt(math.pi)/2-math.sqrt(math.log(1/fail)/ell)
        miss=min(1.,fail+(1-r['dark_probability'])/(1+v)*math.exp(-zeta*a*ell*rayleigh_lower**2/(1+v)))
        rr=dict(r);rr['actual_click_H0_lower']=max(0.,1-miss-2*math.sqrt(ell*p_tail))
        test=finite_count_test(rr,t['blocks'])
        phase_rows.append({'concentration_failure':fail,'H0_click_lower':rr['actual_click_H0_lower'],'finite_test':test})
    # Coherent channel-certification adversary: phase flip of Fock level N.
    # A rare fixed-brightness component beats a fixed mean-one Gaussian
    # schedule on THIS channel, while preserving total expected brightness.
    probes=[];budget=1.;es=1.
    for N in (8,32,128,512):
        prob=math.exp(-N+N*math.log(N)-gammaln(N+1))
        rare=budget/N*4*prob*(1-prob)
        log_ep=N*math.log(budget)-(N+1)*math.log1p(budget)
        log_ep2=gammaln(2*N+1)-2*gammaln(N+1)+2*N*math.log(budget)-(2*N+1)*math.log1p(2*budget)
        gauss=4*(math.exp(log_ep)-math.exp(log_ep2))
        probes.append({'Fock_level':N,'energy_constrained_full_trace_witness':4*math.sqrt(es/N*(1-es/N)),
                       'Gaussian_mean_one_detection_probability':gauss,
                       'rare_brightness_N_detection_probability':rare,
                       'scope':'one adversarial family, not a new minimax theorem or general JC-channel qualification'})
    pairs=t['total_source_pairs']
    result={'status':'PASS model-resource and circuit controls',
            'tree_32_mode_row_residual':row_error,'tree_unitarity_residual':unitary_error,
            'selected_collectors':{'pairs_per_block':ell,'balanced_tree_depth':depth,
                 'tree_combiners':ell-1,'parallel_read_modes':ell,
                 'max_equal_loss_per_tree_stage_if_entire_budget_allocated_here':1-zeta**(1/depth),
                 'max_equal_bus_loss_per_step_for_record_uniform_transmission':1-zeta**(1/ell),
                 'warning':'detector, propagation and switching losses share zeta; numbers cannot each be spent again'},
            'illustrative_finite_ADC':{'bits_per_real_quadrature':bits,'quadrature_absolute_clip':cap,
                 'clip_probability_per_block_upper':delta/2,'small_norm_failure_upper_float':norm_failure,
                 'log_small_norm_failure_upper':-ell*(math.log(2)-.5),
                 'squared_alignment_from_rounding_lower':adc_alignment,
                 'remaining_total_unitary_row_error_budget':remaining_error,
                 'sufficient_uniform_gate_error_for_entire_tree':remaining_error/(ell-1+ell),
                 'scope':'ADC and gate error are separate sufficient budgets; rare overflow and actuator faults still need explicit accounting'},
            'phase_only_prior_at_selected_point':phase_rows,
            'photon_and_operation_ledger':{'source_pairs':pairs,'sent_signal_photons':pairs*r['n'],
                 'initial_purifier_photons':pairs*r['n'],'retained_optical_photons_before_JC':pairs*y,
                 'mean_B_photons_including_noise':pairs*(r['eta']*r['n']+r['b']),
                 'JC_write_interactions':pairs,'JC_read_interactions':pairs,
                 'fresh_ground_qubit_uses':pairs,'fresh_vacuum_read_port_uses':pairs,
                 'on_off_detector_uses':t['blocks'],
                 'excluded_from_photon_totals':'pump, local oscillator, refrigeration, reset work, controller and discarded-output collection'},
            'coherent_probe_phase_flip_controls':probes,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'resource_controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

"""Receiver certificate allowing a retained, unprepared quantum gain source.

Uses the new binary nonvacuum-read lemma and collective Casimir, instead of
assuming a classical controller can be traced as a Gibbs-preserving map.
Source preparation/write is inherited at its explicit driven Markov scope.
"""
import json,math,hashlib
from pathlib import Path
from phase_spin_receiver import finite_test
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'
def certify(source,delta_gain=.1,shape_error=.001,read_ramp_duration=None,do_test=True):
    p=source['parameters'];ell=p['ell'];up=p['gamma']*p['cold_spin']/(1-p['cold_spin'])
    pb=source['spin_population_upper'];pm=source['spin_population_lower'];nu=p['cold_cavity']
    M=ell*pb+nu;F2=ell*(ell-1)*pb*pb+2*ell*pb*nu+2*nu*nu;N2=M+F2
    if read_ramp_duration is None:read_ramp_duration=.05/p['G']
    theta=(1+delta_gain)*math.pi/2;T=math.pi/(2*p['G'])+read_ramp_duration
    bright=ell*source['single_spin_coherence_lower']**2/(1+pb+ell*source['single_spin_coherence_upper']**2)
    gain=math.cos(math.pi*delta_gain/2)**2
    ideal=gain*bright/(1+nu)
    eps_sat=theta*math.sqrt(F2/ell)
    eps_shape=shape_error*theta*math.sqrt(N2)
    eps_det=p['read_detuning']*T*math.sqrt(N2)
    kp=p['read_kappa']*p['bath_thermal'];km=p['read_kappa']*(1+p['bath_thermal'])
    rate=max(km+kp,p['gamma']+2*p['dephase']);offset=kp+ell*up
    eps_nojump=T/2*math.sqrt(rate*rate*N2+2*rate*offset*M+offset*offset)
    good=max(0.,math.sqrt(ideal)-eps_sat-eps_shape-eps_det-eps_nojump)**2
    release=p['release_kappa']/(p['release_kappa']+p['read_kappa'])*(1-math.exp(-(p['release_kappa']+p['read_kappa'])*p['release_T']))
    transmission=p['detector_QE']*release
    added=p['detector_QE']*(1-release)*p['bath_thermal']+(1-p['detector_QE'])*p['detector_thermal']
    p0=(1-p['control_failure'])*transmission/(1+added)**2*good
    R=math.exp(ell*(pb-pm)/(1-pb))
    initial_K=nu+R*pb/(1-2*pb)
    dephasing_drift=4*p['dephase']*T*M/ell
    symmetric_false=initial_K+dephasing_drift
    first_up=T*(kp*(M+1)+ell*up)
    high_log_spin=ell/8*math.log(8*math.e*pb)
    high_log_cavity=ell/8*math.log(nu/(1+nu)) if nu else float('-inf')
    high=math.exp(high_log_spin)+math.exp(high_log_cavity)
    false_cavity=min(1.,(math.sqrt(symmetric_false)+eps_shape)**2+first_up+high)
    # A phase-insensitive thermal attenuator can add at most its vacuum
    # background click to an arbitrary incoming nonvacuum probability.
    p1=min(1.,false_cavity+added+p['detector_dark'])
    test=finite_test(p0,p1,ell,source['actual_signal_mean'],p['eta'],p['b']) if do_test else None
    return {'physical_source':source,'gain_relative_uncertainty':delta_gain,'coupling_shape_error':shape_error,
       'read_ramp_duration':read_ramp_duration,'actual_read_duration':T,
       'actual_gain_source':'arbitrary retained finite quantum system, noncommuting and arbitrarily fast dynamics, positive bounded common gain on good blocks',
       'common_bad_block_scope':'independent/conditional-CP mixture <=5%; any collective N-and-Casimir-preserving Hamiltonian with the same bounded shape perturbation',
       'bright_nonvacuum_lower':bright,'warm_gain_efficiency_lower':gain,
       'ideal_bosonic_quantum_source_nonvac_lower':ideal,
       'saturation_vector_error':eps_sat,'shape_vector_error':eps_shape,
       'detuning_vector_error':eps_det,'no_jump_vector_error':eps_nojump,
       'H1_accessible_charge_initial_upper':initial_K,'H1_local_dephasing_charge_growth':dephasing_drift,
       'H1_first_upward_event_probability':first_up,'H1_high_number_log_bounds':[high_log_spin,high_log_cavity],
       'H1_symmetric_nonvacuum_upper':symmetric_false,
       'actual_H0_click_lower':p0,'actual_H1_click_upper':p1,'finite_test':test}
def main():
    sources=json.loads((OUT/'phase_spin_receiver.json').read_text())['qualifying_points']
    rows=[]
    for s in sources:
        row=certify(s)
        if row['finite_test']:rows.append(row)
    rows.sort(key=lambda r:r['finite_test']['source_pairs'])
    assert rows
    chosen=next((r for r in rows if r['physical_source']['parameters']['gamma']==1e-4),rows[0])
    result={'status':'new conditional warm-controller analytic receiver certificate, floating evaluation',
       'selected':chosen,'qualifying_points':rows,
       'scope':'binary photon-presence read, not a coherent SWAP, universal fault tolerance or a measured device',
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'warm_controller_receiver.json').write_text(json.dumps(result,indent=2)+'\n')
    out={k:v for k,v in chosen.items() if k!='physical_source'}
    out['physical_parameters']=chosen['physical_source']['parameters']
    print(json.dumps({'qualified':len(rows),'selected':out},indent=2))
if __name__=='__main__':main()

"""Physical spin-cavity collector bounds for energy-only quantum illumination.

The write coherence is derived from an input-output capture kernel; the
read transfer from a damped two-mode propagator. Nonlinear saturation is
bounded by a charge-sector Duhamel estimate. The absent-target false click
uses an operator Gibbs supersolution for the actual nonlinear open receiver.
All rates are declared model parameters, not measured component values.
"""
from __future__ import annotations
import json,math,hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
from scipy.special import xlogy
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'

def binary_d(p,q):return float(xlogy(p,p/q)+xlogy(1-p,(1-p)/(1-q)))
def capture(kappa=1.,g=.5,gamma=1e-7,dephase=1e-7,duration=30.,ramp=1.):
    A=np.array([[-kappa/2,-1j*g],[-1j*g,-gamma/2-dephase]],complex)
    def kernel(t):return math.sqrt(kappa)*expm(A*t)[1,0]
    eta,error=quad(lambda t:abs(kernel(t))**2,0,duration,epsabs=1e-13)
    h=kappa/2+gamma/2+dephase;om2=g*g-((kappa/2-gamma/2-dephase)/2)**2
    # Smooth the tiny leading source tail; the photon-generator coupling
    # remains finite by leaving a fixed residual fraction in its source.
    early_mass_upper=kappa*g*g/om2*ramp*math.exp(-h*(duration-ramp))
    beta2_lower=max(0.,eta-2*early_mass_upper)
    def taper(t):return math.sin(math.pi*t/(2*ramp))**2 if t<ramp else 1.
    norm=quad(lambda t:abs(kernel(duration-t)*taper(t))**2,0,duration,epsabs=1e-13)[0]
    overlap=quad(lambda t:abs(kernel(duration-t))**2*taper(t),0,duration,epsabs=1e-13)[0]
    actual_beta2=overlap**2/norm
    assert beta2_lower<=actual_beta2+1e-13
    return {'kappa':kappa,'g':g,'gamma':gamma,'dephase':dephase,'duration':duration,'ramp':ramp,
            'matched_coherence_efficiency':eta,'smoothed_coherence_efficiency':actual_beta2,
            'coherence_efficiency_lower':beta2_lower,'smoothing_loss_charge':2*early_mass_upper,
            'quadrature_error_report':error,
            'source_max_release_rate_bound_at_residual_01':99*kappa*g*g/om2/norm}

def evaluate(n,ell,blocks=3000,write=None,source_residual=.01,source_thermal=1e-12,
             cold_qubit=1e-12,cold_write_cavity=1e-12,storage_time=100.,gamma=1e-7,
             storage_dephase=1e-5,G=1.,read_kappa=.02,read_dephase=1e-5,
             bath_occupation=1e-12,detector_efficiency=.95,dark=1e-7,
             extra_detector_occupation=1e-8,delta_record=1e-6,delta_phase=1e-4,
             row_error=.003,control_failure=.05,eta=.5,b=.5,eta_H=.9):
    write=write or capture();ret=1-source_residual;y=ret*n
    # Squeezing two independent equally warm modes preserves a thermal
    # signal marginal, with this actual mean. The pure-state source is
    # used only as an H0 reference; H1 uses the actual occupation.
    n_actual=n+(2*n+1)*source_thermal
    beta=math.sqrt(write['coherence_efficiency_lower'])*math.exp(-(gamma/2+storage_dephase)*storage_time)
    kplus=read_kappa*bath_occupation;kminus=read_kappa*(1+bath_occupation)
    gplus=gamma*cold_qubit;gminus=gamma*(1-cold_qubit)
    T=math.pi/(2*G)
    # Nominal vacuum loss is solved inside the Gaussian reference; it is
    # not an additive chance of a failure on the whole experiment.
    Ar=np.array([[-read_kappa/2,-1j*G],[-1j*G,-gamma/2]],complex)
    read=expm(Ar*T);read_eta=float(abs(read[0,1])**2)
    initial_cavity_coefficient=float(abs(read[0,0])**2)
    local_warm_charge=cold_qubit+cold_write_cavity
    # Warm incoming write-field/upward-event charge; a conservative local
    # first-event bound. It is paid in H0, and separately in H1 occupation.
    write_warm_charge=write['duration']*(write['kappa']+write['gamma'])*bath_occupation
    prep_charge=ell*(local_warm_charge+write_warm_charge+2*source_thermal)
    tail=(y/(1+y))**2;head_charge=2*math.sqrt(ell*tail)
    pbar=min(.1,ret*n_actual+local_warm_charge+write_warm_charge+gamma*cold_qubit*storage_time)
    pmin=max(0.,ret*n_actual/(1+ret*n_actual)**2*beta**2-local_warm_charge-write_warm_charge)
    qbar=pbar/(1-pbar);qmin=pmin/(1-pmin)
    # Cavity and thermal baths must be colder than even the guaranteed
    # signal-induced spin occupation. This is a real low-noise constraint.
    if min(qmin-qbar*0+kplus/kminus*0, qmin)>0:
        assert bath_occupation/(1+bath_occupation)<=qmin
    else:return None
    # Normalized heterodyne row is diffuse on the good classical record.
    w2=2*math.log(2*ell/delta_record)/ell
    wmax=min(1.,math.sqrt(w2)+row_error)
    # A phase-covariant vacuum-stable write on the head is loss followed
    # by phase diffusion. Without knowing its population a, a<=1 and its
    # coherence >=beta give this uniform variance bound for the real drive.
    V=(1-beta*beta)**2*w2/2
    logp=math.log(1/delta_phase)
    phase_charge=math.sqrt(2*V*logp)+(4/3)*w2*logp
    coherent_amplitude=max(0.,beta-phase_charge-row_error)
    M=ell*pbar;M2=M+ell*(ell-1)*pbar*pbar
    saturation=G*T*wmax*math.sqrt(ell*(ell-1))*pbar
    # Number-diagonal dephasing is cone-preserving for H1. The H0 charge
    # is excitation-weighted, rather than one error per empty spin.
    phase_read_charge=math.sqrt(2*read_dephase*T*M+(read_dephase*T)**2*M2)
    heat_read_charge=T*(kplus*(M+1)+ell*gplus)
    sb=eta_H*(eta*n+b);a0=eta_H*eta*ret*n*(n+1)/(1+sb)
    # Discard the helpful no-click prefactor for a bound uniform over the
    # unknown head population a in [beta^2,1].
    variance_upper=detector_efficiency*(read_eta*y+initial_cavity_coefficient*bath_occupation)+extra_detector_occupation
    drive=detector_efficiency*read_eta*coherent_amplitude**2*a0
    miss=(1-dark)*math.exp(-ell*math.log1p(drive/(1+variance_upper)))
    p0=max(0.,1-miss-head_charge-prep_charge-delta_record-delta_phase-saturation-phase_read_charge-heat_read_charge)
    p0*=1-control_failure
    # Gibbs cone: actual p can be unknown in [pmin,pbar]; choose its own
    # fugacity, cancel the spin normalization, then maximize at qbar.
    cone_exponent=T*(ell*(gminus*qbar-gplus)+kminus*qbar-kplus)
    cone=math.exp(max(0.,cone_exponent))
    cavity_mean_upper=cone*qbar/((1+bath_occupation)*(1-qbar)**2)
    p1=min(1.,dark+detector_efficiency*cavity_mean_upper+extra_detector_occupation)
    # All probes with only a classical retained record: arbitrary input
    # states and correlations, energy <=K*n_actual. No source-info cap.
    incumbent_per_pair=eta*n_actual*math.log1p(1/b)
    result={'n_ideal':n,'n_actual':n_actual,'ell':ell,'blocks':blocks,'source_retention':ret,
            'write':write,'storage_time':storage_time,'gamma':gamma,'storage_dephase':storage_dephase,
            'G':G,'read_kappa':read_kappa,'read_dephase':read_dephase,'read_duration':T,
            'bath_occupation':bath_occupation,'cold_qubit':cold_qubit,'cold_write_cavity':cold_write_cavity,
            'detector_efficiency':detector_efficiency,'dark':dark,'extra_detector_occupation':extra_detector_occupation,
            'source_thermal':source_thermal,'eta':eta,'b':b,'eta_H':eta_H,'control_failure':control_failure,
            'delta_record':delta_record,'delta_phase':delta_phase,'row_error':row_error,
            'head_coherence_lower':beta,'nominal_read_population_transfer':read_eta,
            'pmin':pmin,'pbar':pbar,'phase_concentration_charge':phase_charge,
            'saturation_charge':saturation,'H0_head_tail_charge':head_charge,'H0_preparation_charge':prep_charge,
            'H0_read_dephasing_charge':phase_read_charge,'H0_thermal_read_charge':heat_read_charge,
            'max_spin_weight':wmax,'Gibbs_cone_exponent':cone_exponent,
            'actual_click_H0_lower':p0,'actual_click_H1_upper':p1,
            'all_classical_energy_only_relative_entropy_per_pair_upper':incumbent_per_pair}
    if p0>p1:
        mu=blocks*p0;h=math.floor(mu-math.sqrt(2*mu*math.log(10)))
        if h>blocks*p1:
            logq=-blocks*binary_d(h/blocks,p1)
            logc=-(blocks*ell*incumbent_per_pair+math.log(2))/.9
            result.update({'total_pairs':blocks*ell,'threshold':h,
                    'miss_upper':math.exp(-(mu-h)**2/(2*mu)),
                    'log_quantum_false_upper':logq,'log_all_classical_false_lower':logc,
                    'strict_log_margin':logc-logq})
    return result

def main():
    write=capture();rows=[];allrows=[]
    for n in (1e-4,3e-5,1e-5,3e-6):
      for ell in (4096,8192,16384,32768,65536):
       for blocks in (1000,3000,10000,30000):
        r=evaluate(n,ell,blocks,write=write);allrows.append(r)
        if r and r.get('strict_log_margin',0)>5:rows.append(r);break
    assert rows,'no complete-model point survives these sufficient bounds'
    rows.sort(key=lambda r:r['total_pairs'])
    result={'status':'conditional analytic physical-model construction, floating evaluation',
            'selected':rows[0],'qualifying_points':rows,
            'scope':'no imposed information cap; all parallel source probes with classical retained records at equal signal energy, including non-Gaussian inputs',
            'not_claimed':'new illumination principle, measured device, generic fault tolerance or practical advantage',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'collective_model.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'qualified':len(rows),'selected':rows[0]},indent=2))
if __name__=='__main__':main()

"""Observable-based certificate for a nonlinear phase-only spin receiver.

All primitive channels come from a declared driven quantum-optical Markov
model. This is a conditional mathematical construction, not device validation.
The finite-count expressions use the actual per-block conditional bounds.
"""
from __future__ import annotations
import json,math,hashlib
from pathlib import Path
from scipy.special import gammaln
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'

def capture_lower(kappa,g,gamma,dephase,T,ramp,internal_fraction):
    alpha=kappa/2;beta=gamma/2+dephase;h=alpha+beta;d=(alpha-beta)/2
    om=math.sqrt(g*g-d*d)
    residual=math.exp(-h*(T-2*ramp))*(1+(g+abs(d))/om)**2
    lower=(1-internal_fraction)*(1-(gamma+2*dephase)*T-(1+2*kappa*ramp)*residual)
    assert lower>0
    source_peak=99*kappa/(lower-residual*kappa*ramp)
    return lower,residual,source_peak

def finite_test(p0,p1,ell,n_actual,eta,b,miss=.1,target_beta=1e-8):
    candidates=[]
    for blocks in range(3,1001):
        # Largest integer threshold satisfying the exact binomial miss
        # expression. Floating screening only; interval check is separate.
        h=int(binom.ppf(miss,blocks,p0))
        while h>0 and binom.cdf(h-1,blocks,p0)>miss:h-=1
        while h<blocks and binom.cdf(h,blocks,p0)<=miss:h+=1
        if h<1:continue
        logq=gammaln(blocks+1)-gammaln(h+1)-gammaln(blocks-h+1)+h*math.log(p1)
        logc=-(blocks*ell*eta*n_actual*math.log1p(1/b)+math.log(2))/(1-miss)
        if logq<min(math.log(target_beta),logc):
            candidates.append({'blocks':blocks,'threshold':h,'source_pairs':ell*blocks,
               'mean_signal_photons':ell*blocks*n_actual,
               'miss_upper_float':float(binom.cdf(h-1,blocks,p0)),
               'log_quantum_false_upper':float(logq),'log_all_classical_false_lower':logc,
               'strict_log_margin':logc-logq,'target_beta':target_beta})
            break
    return candidates[0] if candidates else None

def evaluate(n=3e-5,ell=32768,ports=1024,gamma=1e-4,dephase=1e-5,
             write_kappa=1.,write_g=.5,write_T=40.,ramp=1.,write_internal_fraction=.01,
             G=1.,read_kappa=.02,read_gain_spread=.1,read_detuning=.0001,
             source_A_residual=.01,source_C_residual=.01,source_thermal=1e-12,
             bath_thermal=1e-12,cold_spin=1e-12,cold_cavity=1e-12,
             return_delay=100.,reset_g=1.,source_chi=.1,
             phase_bins=64,phase_duration=1.,phase_pump_angle=1e-4,
             phase_actuator_error=.001,control_failure=.05,
             release_kappa=1.,release_T=7.,detector_QE=.95,
             detector_dark=1e-7,detector_thermal=1e-8,eta=.5,b=.5,eta_H=.9,do_test=True):
    source_mean=n+(2*n+1)*source_thermal
    A_trans=1-source_A_residual;C_trans=1-source_C_residual
    # Transmitted temporal modes propagate in vacuum. Nonzero thermal
    # occupation belongs to explicitly separate internal loss ports.
    nA=A_trans*source_mean
    # The C source oscillator is the actual Gaussian input to the whole
    # cascaded emitter/capture channel, so its release is part of beta.
    y=source_mean
    s=eta_H*(eta*nA+b)
    cross2=eta_H*eta*A_trans*(2*source_thermal+1)**2*n*(n+1)
    a=cross2/(1+s);conditional=y-a
    assert conditional>=0
    eta_write,residual,source_peak=capture_lower(write_kappa,write_g,gamma,dephase,write_T,ramp,write_internal_fraction)
    spin_up=gamma*cold_spin/(1-cold_spin)
    exposure=write_kappa*write_T+math.log(1/source_C_residual)
    beta_warm_charge=20*bath_thermal*write_internal_fraction*write_kappa*write_T+4*(cold_spin+cold_cavity)+4*spin_up*write_T
    beta_write=max(0.,math.sqrt(C_trans*eta_write)-beta_warm_charge)
    source_prepare_T=math.asinh(math.sqrt(n))/source_chi
    thermal_swap_T=math.pi/(2*reset_g)
    cycle=thermal_swap_T+source_prepare_T+write_T
    rounds=math.ceil(ell/ports)
    hold_max=return_delay+(rounds-1)*cycle+phase_duration
    hold_min=return_delay+phase_duration
    # Actual thermally populated qubits and cavities are replaced by fresh
    # thermal ancillas using finite swaps; no asymptotic reset is invoked.
    beta_head=beta_write*math.exp(-((gamma+spin_up)/2+dephase)*hold_max)
    qsource=y/(1+y);qbath=bath_thermal/(1+bath_thermal)
    qspin=cold_spin/(1-cold_spin)
    if min(qsource-qbath,qsource-qspin,qsource-cold_cavity/(1+cold_cavity))<=0:return None
    Awrite=qsource*exposure+write_internal_fraction*write_kappa*bath_thermal*(qsource-1)*write_T+(gamma*qsource-spin_up)*write_T
    pwrite_upper=math.exp(Awrite)*(1-cold_spin)/(1+cold_cavity)*qsource/(1-qsource)
    pbar=min(.2,pwrite_upper+spin_up*hold_max)
    pmin=y/(1+y)**2*beta_write**2*math.exp(-(gamma+spin_up)*hold_max)
    qbar=pbar/(1-pbar);qmin=pmin/(1-pmin)
    if max(qbath,qspin,cold_cavity/(1+cold_cavity))>=qmin:return None
    # Exact heterodyne phase-bin first harmonic and a finite coherent
    # cross-Kerr phase pulse. The outgoing pump never returns as memory.
    sinc=math.sin(math.pi/phase_bins)/(math.pi/phase_bins)
    phase_visibility=math.exp(-2*math.pi*math.tan(phase_pump_angle/2))
    phase_gain=sinc*phase_visibility*math.cos(phase_actuator_error)
    total_first=math.sqrt(math.pi)/2*math.sqrt(a)
    head_first=total_first/(math.sqrt(1+conditional)*(1+y)**1.5)
    tail_first=max(0.,(total_first-head_first)/math.sqrt(2))
    s_lower=max(0.,phase_gain*beta_head*head_first-tail_first)
    s_upper=total_first
    # Read pulse: common smooth envelope, static positive coupling spread.
    T=math.pi/G;theta_max=math.pi/2*(1+read_gain_spread)
    coherent_gain=math.sqrt(1-read_gain_spread**2)
    wmax2=((1+read_gain_spread)/(1-read_gain_spread))**2/ell
    gamma_coh=(gamma+spin_up)/2+dephase
    linear_perturbation=(max(read_kappa/2,gamma_coh)+read_detuning)*T
    sin_lower=math.cos(math.pi*read_gain_spread/2)
    M=ell*pbar;cold=cold_cavity
    F2=M*M+2*M*cold+2*cold*cold
    F3=M**3+3*M*M*cold+6*M*cold*cold+6*cold**3
    # Upper bound for thermal birth during the actual nonlinear read.
    kplus=read_kappa*bath_thermal;kminus=read_kappa*(1+bath_thermal)
    birth_u=kplus;birth_v=kplus+ell*spin_up
    mean_upper=(M+cold+birth_v*T)*math.exp(birth_u*T)
    factorial_upper=(F2+F3+2*(birth_v+birth_u)*mean_upper*T)*math.exp((8*birth_u+3*birth_v)*T)
    nonlinear=2*(math.cosh(theta_max)-1)*wmax2*math.sqrt(factorial_upper)
    mean_amplitude=max(0.,math.sqrt(ell)*(sin_lower*coherent_gain*s_lower-linear_perturbation*s_upper)-nonlinear)
    noise_norm=math.sqrt(T*(2*dephase*math.sinh(theta_max)**2*wmax2*mean_upper+spin_up+kplus))
    linear_number_upper=cold+pbar+ell*s_upper*s_upper
    cavity_number_upper=min(mean_upper,(math.sqrt(linear_number_upper)+nonlinear+noise_norm)**2)
    # The internal loss port remains open during release.
    eta_release=release_kappa/(release_kappa+read_kappa)*(1-math.exp(-(release_kappa+read_kappa)*release_T))
    det_trans=detector_QE*eta_release
    added=detector_QE*(1-eta_release)*bath_thermal+(1-detector_QE)*detector_thermal
    p0=(1-control_failure)*det_trans*mean_amplitude**2/(1+det_trans*cavity_number_upper+added)
    # Full H1 cone, with an explicit correction for nonidentical aged spins.
    population_spread=ell*(pbar-pmin)/(1-pbar)
    read_A=T*(ell*(gamma*qbar-spin_up)+kminus*qbar-kplus)
    cone=math.exp(population_spread+max(0.,read_A))
    false_mean=cone/(1+cold_cavity)*qbar/(1-qbar)**2
    p1=min(1.,detector_dark+det_trans*false_mean+added)
    test=finite_test(p0,p1,ell,nA,eta,b) if do_test else None
    result={'parameters':{k:v for k,v in locals().copy().items() if k in (
       'n','ell','ports','gamma','dephase','write_kappa','write_g','write_T','ramp','write_internal_fraction','G','read_kappa',
       'read_gain_spread','read_detuning','source_A_residual','source_C_residual','source_thermal',
       'bath_thermal','cold_spin','cold_cavity','return_delay','reset_g','source_chi','phase_bins',
       'phase_duration','phase_pump_angle','phase_actuator_error','control_failure','release_kappa',
       'release_T','detector_QE','detector_dark','detector_thermal','eta','b','eta_H')},
       'actual_signal_mean':nA,'actual_C_source_mean':y,'conditional_optical_mean':conditional,
       'write_coherence_efficiency_lower':eta_write,'write_residual_bound':residual,
       'source_release_peak_rate_bound':source_peak,'source_release_integrated_rate':math.log(1/source_C_residual),
       'write_cooperativity_g2_over_kappa_gamma':write_g**2/(write_kappa*gamma),
       'capture_cycle_duration':cycle,'capture_rounds':rounds,'maximum_spin_hold':hold_max,
       'minimum_spin_hold':hold_min,'thermal_swap_duration':thermal_swap_T,
       'head_coherence_write_lower':beta_write,'head_coherence_after_storage_lower':beta_head,
       'spin_population_upper':pbar,'spin_population_lower':pmin,
       'optical_tail_first_moment_charge':tail_first,'single_spin_coherence_lower':s_lower,
       'single_spin_coherence_upper':s_upper,'phase_visibility_lower':phase_visibility,
       'max_phase_pump_photons':2*math.pi/math.sin(phase_pump_angle),
       'mean_phase_pump_photons':math.pi/math.sin(phase_pump_angle),
       'read_duration':T,'read_area_upper':theta_max,'read_one_particle_diagonal_error_bound':linear_perturbation,
       'nonlinear_amplitude_charge':nonlinear,'read_noise_vector_norm_upper':noise_norm,
       'cavity_coherent_amplitude_lower':mean_amplitude,'cavity_population_upper':cavity_number_upper,
       'total_initial_read_excitations_upper':M+cold,'read_thermal_birth_mean_upper':mean_upper,
       'H1_population_inhomogeneity_log_factor':population_spread,'H1_read_Gibbs_log_factor':read_A,
       'H1_cavity_mean_upper':false_mean,'actual_block_click_H0_lower':p0,
       'actual_block_click_H1_upper':p1,'finite_test':test}
    return result

def main():
    rows=[]
    for gamma in (1e-4,1e-5):
     for ports in (256,1024):
      for n in (1e-4,3e-5,1e-5,3e-6):
       for ell in (2048,8192,32768):
        r=evaluate(n,ell,ports,gamma)
        if r and r['finite_test']:rows.append(r)
    assert rows
    rows.sort(key=lambda r:(r['finite_test']['source_pairs'],r['parameters']['ports']))
    selected=next((r for r in rows if r['parameters']['gamma']==1e-4),rows[0])
    result={'status':'conditional finite dynamics and observable inequalities; floating screening',
       'selected':selected,'qualifying_points':rows,
       'classical_scope':'all parallel probes with arbitrary classical retained records, arbitrary input states and correlations across sent modes, same actual mean signal photons; no imposed information budget',
       'physical_scope':'driven rotating-wave Markov model, fresh stated thermal inputs; detector budgets still qualified assumptions',
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'phase_spin_receiver.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'qualified':len(rows),'selected':selected},indent=2))
if __name__=='__main__':main()

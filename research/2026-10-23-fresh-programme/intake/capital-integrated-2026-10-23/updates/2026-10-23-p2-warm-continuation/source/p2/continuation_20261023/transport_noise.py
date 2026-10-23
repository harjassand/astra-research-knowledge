"""Thermal-current noise, distinct from converter-added noise.

Analytic moment proof is in TRANSPORT_NOISE_BOUND.txt. All outputs here are
calculation/simulation, not acquired measurements. The measured device tuple
is read from the single-record Josephson input file; its 80/100 mK use is a
proposed reassignment, not a reported operating point.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent
H = 6.62607015e-34
KB = 1.380649e-23


def moments_two_mode(na, nb, transmission):
    delta = na - nb
    return transmission*delta, (
        transmission*(na*(1+nb)+nb*(1+na))
        + transmission**2*delta**2
    )


def finite_fock_check(na, nb, transmission, cutoff):
    """Two-projective-number-measurement distribution in exact N blocks.

    Omit entire total-number sectors >= cutoff, with the omitted probability
    and moments documented. This preserves unitarity in every retained block.
    No truncated annihilation operator at the top of a rectangular basis.
    """
    ra, rb = na/(1+na), nb/(1+nb)
    theta = math.asin(math.sqrt(transmission))
    mass = mean = second = 0.
    unitarity = 0.
    for total in range(cutoff):
        dimension = total+1
        # Basis k = initial/final occupation of mode b, a = total-k.
        generator = np.zeros((dimension, dimension))
        for k in range(total):
            value = math.sqrt((total-k)*(k+1))
            generator[k+1, k] = value
            generator[k, k+1] = -value
        unitary = expm(theta*generator)
        unitarity = max(unitarity, float(np.max(abs(unitary.T@unitary-np.eye(dimension)))))
        probabilities = unitary**2
        for k in range(dimension):
            initial_p = (1-ra)*(1-rb)*ra**(total-k)*rb**k
            q = np.arange(dimension)-k
            mass += initial_p
            mean += initial_p*float(q@probabilities[:, k])
            second += initial_p*float((q*q)@probabilities[:, k])
    return dict(cutoff_total_occupation=cutoff,
                retained_mass=mass, omitted_mass=max(0.,1-mass),
                raw_mean=mean, raw_variance=second-mean**2,
                block_unitarity_max_error=unitarity)


def device_noise(device, cooperativity=1., tc=.080, th=.100):
    fa, fb = [device['modes'][j]['frequency_Hz'] for j in ('a','b')]
    ka, kb = [2*math.pi*device['modes'][j]['kappa_over_2pi_Hz'] for j in ('a','b')]
    ea, eb = [device['modes'][j]['external_fraction'] for j in ('a','b')]
    n = np.array([1/math.expm1(H*f/(KB*t))
                  for f,t in ((fa,tc),(fa,th),(fb,th),(fb,th))])
    # Use dimensionless detuning u = delta/ka. All four loss/external ports
    # are retained, so this scattering matrix is photon-number unitary.
    coupling = np.array([[math.sqrt(ea),math.sqrt(1-ea),0.,0.],
                        [0.,0.,math.sqrt(kb*eb/ka),math.sqrt(kb*(1-eb)/ka)]])
    g = math.sqrt(cooperativity*ka*kb)/2/ka
    pc = np.diag([1.,0.,0.,0.])
    pw = np.diag([0.,0.,1.,1.])  # upper photons = net pump quanta
    nn = np.diag(n)
    nplus = np.diag(1+n)

    def at(u):
        denominator = np.array([[.5-1j*u,1j*g],
                                [1j*g,kb/(2*ka)-1j*u]])
        scattering = np.eye(4)-coupling.T@np.linalg.solve(denominator,coupling)
        kc = pc-scattering.conj().T@pc@scattering
        kw = scattering.conj().T@pw@scattering-pw
        means = [np.trace(k@nn).real for k in (kc,kw)]
        variances = [np.trace(k@nn@k@nplus).real for k in (kc,kw)]
        cross = np.trace(kc@nn@kw@nplus).real
        return np.array(means+variances+[cross])

    # Even spectra, integrals d(delta)/(2 pi) = ka/pi int_0^infty du.
    integrals = np.array([quad(lambda u:at(u)[j],0.,np.inf,
                        epsabs=2e-12,epsrel=2e-10,limit=200)[0]
                        *ka/math.pi for j in range(5)])
    jc, jp, vc, vp, cv = map(float,integrals)
    # Peak normally-ordered internal added noise, output b referred to a.
    added_internal = ((1-ea)/ea*n[1]
                      +(1-eb)/(ea*cooperativity)*n[3])
    eta_peak = 4*ea*eb*cooperativity/(1+cooperativity)**2
    s0_den = np.array([[.5,1j*g],[1j*g,kb/(2*ka)]])
    s0 = np.eye(4)-coupling.T@np.linalg.solve(s0_den,coupling)
    return {
        'status':'MODEL ONLY; temperatures proposed, rates conditionally retained',
        'C':cooperativity,'Tc_K':tc,'Th_K':th,
        'cold_net_photons_per_s':jc,
        'net_conversion_work_quanta_per_s':jp,
        'cold_heat_W':H*fa*jc,
        'conversion_work_W':H*(fb-fa)*jp,
        'cold_count_variance_per_s':vc,
        'conversion_work_count_variance_per_s':vp,
        'cold_conversion_work_count_covariance_per_s':cv,
        'cold_Fano_variance_rate_over_mean_rate':vc/jc,
        'conversion_work_Fano_variance_rate_over_mean_rate':vp/jp,
        'work_count_convention':'Net upper-band signal count times hbar*Omega; semiclassical work inference, NOT a TPM measurement on a coherent pump.',
        'cold_one_second_rms_energy_J':H*fa*math.sqrt(vc),
        'ideal_only_averaging_time_for_one_percent_relative_heat_noise_s':vc/(jc**2*.01**2),
        'averaging_time_warning':'Long-time intrinsic stationary transport variance only; no detector, thermometer, technical pump or calibration noise included.',
        'resonant_external_conversion_probability':eta_peak,
        'normal_ordered_internal_added_noise_input_referred_photons':added_internal,
        'resonant_full_port_unitarity_error':float(np.max(abs(s0@s0.conj().T-np.eye(4)))),
        'omitted_physics':'Frequency variation of bath occupations/rates, pump depletion and excess noise, off-resonant mode c, non-RWA pair creation and all controller/source costs.'
    }


def main():
    device = json.loads((ROOT/'josephson_inputs.json').read_text())
    fa, fb = [device['modes'][j]['frequency_Hz'] for j in ('a','b')]
    tc, th = .080,.100
    na, nb = [1/math.expm1(H*f/(KB*t)) for f,t in ((fa,tc),(fb,th))]
    affinity = H*fb/(KB*th)-H*fa/(KB*tc)
    ideal = {
        'status':'IDEAL TWO-PORT COMPARATOR AT THE SAME FREQUENCIES; NOT THE MEASURED LOSSY DEVICE',
        'nc':na,'nh':nb,'affinity_dimensionless':affinity,
        'minimum_count_Fano':1/math.tanh(affinity/2),
        'full_transmission_single_temporal_mode_Fano':1/math.tanh(affinity/2)+na-nb,
        'ideal_conversion_COP':fa/(fb-fa),
        'Carnot_COP':tc/(th-tc),
        'entropy_uncertainty_product_lower_bound':affinity/math.tanh(affinity/2),
        'virtual_pump_bath_occupation_weak_conversion':nb*(1+na)/(na-nb),
        'virtual_pump_bath_temperature_K_weak_conversion':H*(fb-fa)/(KB*affinity),
    }
    # Independent exact Fock-basis check at appreciable occupation, so both
    # reverse events and bunching contribute to the second cumulant.
    qa,qb,tr=.4,.2,.63
    analytic = moments_two_mode(qa,qb,tr)
    checks=[]
    for cutoff in (20,32):
        out=finite_fock_check(qa,qb,tr,cutoff)
        out['mean_abs_error']=abs(out['raw_mean']-analytic[0])
        out['variance_abs_error']=abs(out['raw_variance']-analytic[1])
        checks.append(out)
    assert checks[-1]['mean_abs_error']<1e-12
    assert checks[-1]['variance_abs_error']<1e-12
    actual=device_noise(device)
    assert actual['cold_heat_W']>0
    assert actual['resonant_full_port_unitarity_error']<1e-12
    result={
        'classification':'ANALYTIC THEOREM + NUMERICAL VERIFICATION; NO ACQUIRED MEASUREMENT',
        'variance_convention':'lim_{tau->infinity} Var[N(tau)]/tau; no extra spectral-density factor of 2',
        'ideal_pair':ideal,
        'single_record_four_port_proposed_model':actual,
        'independent_Fock_verification':{
            'na':qa,'nb':qb,'transmission':tr,
            'analytic_mean':analytic[0],'analytic_variance':analytic[1],
            'checks':checks
        },
        'novelty':'UNKNOWN; thermal bosonic FCS and fluctuation relations are established. This is a scoped derivation/application, not a new physical law.'
    }
    (ROOT/'transport_noise_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()

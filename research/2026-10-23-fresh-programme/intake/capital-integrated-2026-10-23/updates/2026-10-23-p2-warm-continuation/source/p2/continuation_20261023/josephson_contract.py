"""Single-record Josephson conversion contract; not device refrigeration data.

Primary basis: Lecocq et al., Phys. Rev. Applied 7,024028 (2017),
DOI 10.1103/PhysRevApplied.7.024028, accepted manuscript dated 2017-01-18.
All device inputs below are from that record. No GaAs inputs enter this model.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.integrate import quad

H = 6.62607015e-34
HBAR = H/(2*math.pi)
KB = 1.380649e-23
OUT = Path(__file__).resolve().parent

inputs = {
    "source": {
        "doi": "10.1103/PhysRevApplied.7.024028",
        "title": "Nonreciprocal Microwave Signal Processing with a Field-Programmable Josephson Amplifier",
        "accepted_manuscript_date": "2017-01-18",
        "accepted_manuscript_url": "https://link.aps.org/accepted/10.1103/PhysRevApplied.7.024028",
        "supplemented_arxiv_version_read": "1612.01438v1",
        "arxiv_pdf_url": "https://arxiv.org/pdf/1612.01438v1",
        "retrieval_date": "2026-10-23",
        "pdf_byte_sha256": "UNKNOWN; direct download disallowed, web reader accessed source",
    },
    "modes": {
        "a": {"frequency_Hz": 4.155e9, "kappa_over_2pi_Hz": 29.8e6, "external_fraction": .96},
        "b": {"frequency_Hz": 5.756e9, "kappa_over_2pi_Hz": 29.5e6, "external_fraction": .96},
        "c": {"frequency_Hz": 7.915e9, "kappa_over_2pi_Hz": 59.3e6, "external_fraction": .97},
    },
    "flux_bias_over_flux_quantum": .29,
    "conversion_beta_magnitude_approx": .5,
    "conversion_insertion_loss_dB_approx": .5,
    "conversion_return_loss_dB_approx": 30.,
    "noise_context": {
        "reported_added_noise_photons_approx": 1.,
        "reported_uncertainty_photons_approx": .1,
        "operating_mode": "SUM-FREQUENCY AMPLIFICATION; NOT DIFFERENCE-FREQUENCY CONVERSION",
        "conversion_added_noise_photons": "UNKNOWN",
        "cryostat_stage_temperature_K": .020,
        "actual_converter_bath_temperatures_K": "UNKNOWN",
        "separate_noise_calibration_cooldown_sample_temperature_K": .100,
        "temperature_caution": "The separate 100 mK calibration is not assigned to converter operation.",
    },
    "absolute_pump_incident_power_W": "UNKNOWN",
    "pump_absorption_W": "UNKNOWN",
    "pump_outgoing_recovery_W": "UNKNOWN",
    "flux_control_and_cryogenic_wall_power_W": "UNKNOWN",
}

fa, fb, fc = [inputs["modes"][j]["frequency_Hz"] for j in ("a", "b", "c")]
ka, kb, kc = [2*math.pi*inputs["modes"][j]["kappa_over_2pi_Hz"] for j in ("a", "b", "c")]
ea, eb, ec = [inputs["modes"][j]["external_fraction"] for j in ("a", "b", "c")]
beta = inputs["conversion_beta_magnitude_approx"]
g = beta*math.sqrt(ka*kb)  # Hamiltonian/RWA coupling, half paper's modulation amplitude
C = 4*g*g/(ka*kb)
Keff = ka*kb/(ka+kb)*C/(1+C)
fp = fb-fa

# Resonant external scattering and internal bath branches at C=1.
tau = ea*eb
reflection = (1-ea)**2
loss_a = ea*(1-ea)
loss_b = ea*(1-eb)
assert abs(tau+reflection+loss_a+loss_b-1) < 1e-14
converted_total = tau+loss_b
input_energy = H*fa
output_energy = H*(fa*(reflection+loss_a)+fb*(tau+loss_b))
work_per_input_photon = H*fp*converted_total
assert abs(output_energy-input_energy-work_per_input_photon) < 1e-37

headline_tau = 10**(-inputs["conversion_insertion_loss_dB_approx"]/10)
headline_reflection = 10**(-inputs["conversion_return_loss_dB_approx"]/10)

derived = {
    "status": "DERIVED_MODEL_COEFFICIENTS_FROM_ONE_EXPERIMENT; NO THERMAL PERFORMANCE MEASUREMENT",
    "frequency_ratio_b_over_a": fb/fa,
    "pump_frequency_Hz": fp,
    "pump_over_cold_frequency": fp/fa,
    "ideal_conversion_COP_if_two_thermal_baths": fa/fp,
    "necessary_ideal_temperature_ratio_Th_over_Tc_less_than": fb/fa,
    "C": C,
    "g_RWA_over_2pi_Hz": g/(2*math.pi),
    "g_RWA_over_omega_a": g/(2*math.pi*fa),
    "g_RWA_over_pump_omega": g/(2*math.pi*fp),
    "nearest_other_difference_frequency_detuning_Hz": abs((fc-fb)-fp),
    "nearest_other_difference_detuning_over_largest_linewidth": abs((fc-fb)-fp)/(kc/(2*math.pi)),
    "number_current_coefficient_per_occupation_difference_per_s": Keff,
    "cold_external_heat_coefficient_per_mixed_occupation_difference_W": H*fa*ea*Keff,
    "cold_internal_contact_heat_coefficient_per_occupation_difference_W": H*fa*ka*ea*(1-ea),
    "conversion_work_coefficient_per_mixed_occupation_difference_W": H*fp*Keff,
    "external_a_to_external_b_thermal_transmission_area_Hz": ea*eb*Keff,
    "linewidths": {
        j: {
            "internal_over_2pi_Hz": inputs["modes"][j]["kappa_over_2pi_Hz"]*(1-inputs["modes"][j]["external_fraction"]),
            "external_over_2pi_Hz": inputs["modes"][j]["kappa_over_2pi_Hz"]*inputs["modes"][j]["external_fraction"],
        }
        for j in ("a", "b", "c")
    },
    "rounded_parameter_model_on_resonance": {
        "photon_conversion_external_probability": tau,
        "reflection_probability": reflection,
        "internal_a_absorption_probability_per_a_incident_photon": loss_a,
        "internal_b_absorption_probability_per_a_incident_photon": loss_b,
        "total_upconverted_probability_including_b_internal_bath": converted_total,
        "conversion_insertion_loss_dB": -10*math.log10(tau),
        "work_J_per_a_incident_photon": work_per_input_photon,
        "pump_energy_quanta_consumed_per_a_incident_photon": converted_total,
        "signal_induced_internal_heat_J_per_a_incident_photon": H*(fa*loss_a+fb*loss_b),
        "vacuum_symmetrized_input_referred_added_noise_quanta": (1-tau)/(2*tau),
        "normal_ordered_vacuum_added_heat": 0.,
    },
    "headline_conversion_numbers_separate_from_rounded_parameter_fit": {
        "photon_conversion_external_probability_approx": headline_tau,
        "reflection_probability_approx": headline_reflection,
        "unobserved_passive_port_probability_approx": 1-headline_tau-headline_reflection,
        "vacuum_symmetrized_input_referred_added_noise_quanta_approx": (1-headline_tau)/(2*headline_tau),
        "caution": "Approximate headline values do not exactly equal the rounded parameter model; no fitted correction is invented.",
    },
    "noise_warning": "Symmetrized vacuum attenuation noise is not thermal photons or pump heating. Conversion-specific excess noise remains UNKNOWN.",
    "wall_COP": "UNKNOWN",
    "cold_pump_load_normalized_to_g_squared": "UNKNOWN",
    "receipts": {"new_workers": 0, "provider_model_id": "UNKNOWN", "token_usage": "UNKNOWN", "billing": "UNKNOWN"},
}

# Proposed reservoir reassignment requested by root. The measured rates are
# retained CONDITIONALLY; their invariance under this reassignment is not data.
tc, th = .080, .100
bose = lambda f,t: 1/math.expm1(H*f/(KB*t))
nac, nah, nbh = bose(fa,tc), bose(fa,th), bose(fb,th)
nbara = ea*nac+(1-ea)*nah
nbarb = nbh
dbar = nbara-nbarb
da = nah-nac
K0 = ka*kb/(ka+kb)
gain = H*fa*ea*K0*dbar
leak = H*fa*ka*ea*(1-ea)*da
ell = leak/gain
cthresh = ell/(1-ell)

def thermal_case(cooperativity):
    current = K0*cooperativity/(1+cooperativity)*dbar
    pop_a = nbara-current/ka
    pop_b = nbarb+current/kb
    heat = np.array([
        H*fa*ka*ea*(nac-pop_a),
        H*fa*ka*(1-ea)*(nah-pop_a),
        H*fb*kb*eb*(nbh-pop_b),
        H*fb*kb*(1-eb)*(nbh-pop_b),
    ])
    work = H*fp*current
    assert abs(sum(heat)+work)<1e-29
    entropy = -heat[0]/tc-sum(heat[1:])/th
    assert entropy > -1e-28
    return {
        "C":cooperativity,
        "g_RWA_over_2pi_Hz": math.sqrt(cooperativity*ka*kb)/2/(2*math.pi),
        "number_current_per_s":current,
        "populations": {"a":pop_a,"b":pop_b},
        "heat_W_positive_out_of_reservoir":dict(zip(
            ["lower_external_cold","lower_internal_hot","upper_external_hot","upper_internal_hot"],
            map(float,heat))),
        "conversion_work_W":work,
        "cold_heat_over_conversion_work":float(heat[0]/work) if work>0 else None,
        "additional_cold_deposition_margin_W":max(0.,float(heat[0])),
        "entropy_production_W_per_K":float(entropy),
    }

case1=thermal_case(1.)
# Independent integration of the full four-port Markov scattering spectrum.
# Frequencies/occupations are frozen at mode centers, as required by this
# local Markov model. No rectangular bandwidth approximation is used.
rate_scale=ka
M=np.array([[math.sqrt(ka*ea/rate_scale),math.sqrt(ka*(1-ea)/rate_scale),0.,0.],
            [0.,0.,math.sqrt(kb*eb/rate_scale),math.sqrt(kb*(1-eb)/rate_scale)]])
ns=np.array([nac,nah,nbh,nbh])
fr=np.array([1.,1.,fb/fa,fb/fa])
gg=math.sqrt(ka*kb)/2/rate_scale
def spectral_heat(u,port):
    D=np.array([[ka/(2*rate_scale)-1j*u,1j*gg],
                [1j*gg,kb/(2*rate_scale)-1j*u]],dtype=complex)
    S=np.eye(4)-M.T@np.linalg.solve(D,M)
    return float(fr[port]*sum(abs(S[port,k])**2*(ns[port]-ns[k]) for k in range(4))/math.pi)
spectral=np.array([quad(lambda u:spectral_heat(u,p),0.,np.inf,
                        epsabs=1e-12,epsrel=1e-11,limit=200)[0]
                   *H*fa*rate_scale for p in range(4)])
analytic=np.array(list(case1["heat_W_positive_out_of_reservoir"].values()))
residual=max(abs(spectral-analytic))/max(abs(analytic))
assert residual<1e-10

derived["proposed_80mK_100mK_reservoir_model"]={
    "status":"PROPOSED MODEL ONLY; NOT THE PAPER'S EXPERIMENT",
    "assumption":"Retain measured linewidths and external fractions while assigning lower external bath 80mK and all other baths 100mK. Actual rates/noise at these temperatures are unmeasured here.",
    "Tc_K":tc,"Th_K":th,
    "bath_occupations":{"lower_external_cold":nac,"lower_internal_hot":nah,"upper_baths_hot":nbh},
    "mixed_occupation_difference":dbar,
    "Qc_form":"G*C/(1+C)-L; excludes pump deposition and extra driven noise",
    "G_W":gain,"L_W":leak,"ell":ell,
    "minimum_C_for_strictly_positive_cold_heat":cthresh,
    "cold_heat_supremum_W_unlimited_C_model":gain-leak,
    "linear_cold_pump_heat_slope_W_per_C_threshold":gain*(1-math.sqrt(ell))**2,
    "C_at_linear_loss_threshold_tangency":math.sqrt(ell)/(1-math.sqrt(ell)),
    "Carnot_COP":tc/(th-tc),
    "cases":[thermal_case(c) for c in [0.,cthresh,1.,2.,5.]],
    "four_port_spectral_integral_C1_W":list(map(float,spectral)),
    "max_relative_spectral_vs_covariance_residual":float(residual),
    "spectral_scope":"Exact within the local Markov/RWA model over the full resonance spectrum, with Bose occupations frozen at centers. It is not a full frequency-dependent circuit calculation.",
}

(OUT/'josephson_inputs.json').write_text(json.dumps(inputs, indent=2)+'\n')
(OUT/'josephson_results.json').write_text(json.dumps(derived, indent=2)+'\n')
print(json.dumps(derived, indent=2))

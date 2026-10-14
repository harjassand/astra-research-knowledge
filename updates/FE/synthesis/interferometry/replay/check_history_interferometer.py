#!/usr/bin/env python3
"""Finite-wavepacket checks for a proposed two-history molecular interferometer.

This is an idealized two-level, impulsive calculation, NOT a simulation of
CaOH+ rovibrational dynamics and NOT experimental data. It keeps the spatial
dependence of the pulse unitary, including its recoil/backaction, but neglects
trap evolution DURING the ultrafast sequence. Radiation, spectator modes,
molecular anharmonicity, atomic IR Stark dynamics, pulse-shape distortion and drift must be measured or
included for experimental prediction. Gaussian quadrature is deterministic.

Published reference scales (Wu et al., Nature 657, 364-368, 2026;
arXiv:2511.19687v2): alpha ~6.5, eta_IR ~0.03, reference contrast ~0.52,
nu=3703.3 cm^-1, mean laser intensity 1.1e4 W/cm^2, laser rate 1e5 Hz.
The pulse probabilities and experimental cycle rate used below are scenarios,
NOT reported performance of the proposed apparatus.

Run: python check_history_interferometer.py --output results.json
Dependencies: Python >=3.10, numpy, scipy.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.hermite import hermgauss
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq


def compile_fields(EA: complex, EB: complex, separation_phase: float) -> np.ndarray:
    """Return amplitudes of +k/-k beams for fields EA,EB at kx=+/-s/2."""
    s = float(separation_phase)
    if abs(math.sin(s)) < 1e-10:
        raise ValueError("The two-point field map is singular or ill conditioned.")
    matrix = np.array([[np.exp(0.5j*s), np.exp(-0.5j*s)],
                       [np.exp(-0.5j*s), np.exp(0.5j*s)]])
    return np.linalg.solve(matrix, np.array([EA, EB], complex))


def field_at(coefficients: np.ndarray, kx: float) -> complex:
    return coefficients[0]*np.exp(1j*kx)+coefficients[1]*np.exp(-1j*kx)


def rotation(area: float, phase: float) -> np.ndarray:
    """Resonant two-level rotation, basis (g,e); signed area is permitted."""
    c, s = math.cos(area/2), math.sin(area/2)
    return np.array([[c, -1j*np.exp(-1j*phase)*s],
                     [-1j*np.exp(1j*phase)*s, c]], complex)


def pulse(area: float, field: complex) -> np.ndarray:
    return rotation(area*abs(field), float(np.angle(field)))


def gaussian_nodes(sigma: float, order: int = 36):
    if sigma < 0:
        raise ValueError("sigma must be nonnegative")
    if sigma == 0:
        return np.array([0.]), np.array([1.])
    x, w = hermgauss(order)
    return math.sqrt(2)*sigma*x, w/math.sqrt(math.pi)


def orientation_nodes(frozen_isotropic: bool, order: int = 36):
    if not frozen_isotropic:
        return np.array([1.]), np.array([1.])
    x, w = leggauss(order)
    return x, w/2


def calibrated_area(p: float, frozen_isotropic: bool = False) -> float:
    """Choose model area for stated single-pulse probability; not a laser model."""
    if not 0 < p < .49:
        raise ValueError("Require 0 < p < 0.49 for the chosen monotone branch.")
    if not frozen_isotropic:
        return 2*math.asin(math.sqrt(p))
    # Uniform frozen dipole orientation: <sin^2(theta*u/2)>=(1-sin(theta)/theta)/2.
    return brentq(lambda a: .5*(1-np.sinc(a/np.pi))-p, 1e-8, np.pi)


def signal(p: float, s: float, width_phase: float = 0., node_jitter: float = 0.,
           phase: float = np.pi/2, frozen_isotropic: bool = False,
           swap: bool = False) -> dict:
    """Compute integral <psi_B(q)|psi_A(q)> after conditional recombination.

    Both pulses address branch A, with branch B nominally at a node. The common
    fluctuation q accounts for wavepacket width after undoing the cat translation.
    Node jitter is static across the ultrafast two-pulse sequence; it combines
    with Gaussian spatial width in this specific model. No detuning or intervening
    internal evolution is assumed here, so only the calibration limit is tested.
    """
    area = calibrated_area(p, frozen_isotropic)
    nodes, weights = gaussian_nodes(math.hypot(width_phase, node_jitter))
    us, uw = orientation_nodes(frozen_isotropic)
    coeff = compile_fields(0., 1., s) if swap else compile_fields(1., 0., s)
    ground = np.array([1., 0.], complex)
    L = 0j
    excitation = 0.
    pA = pB = 0.
    for q, w in zip(nodes, weights):
        a = field_at(coeff, s/2+q)
        b = field_at(coeff, -s/2+q)
        for u, wu in zip(us, uw):
            firstA, firstB = pulse(area*u, a), pulse(area*u, b)
            psiA = pulse(area*u, np.exp(1j*phase)*a) @ firstA @ ground
            psiB = pulse(area*u, np.exp(1j*phase)*b) @ firstB @ ground
            weight = float(w*wu)
            L += weight*np.vdot(psiB, psiA)
            excitation += weight*(abs(psiA[1])**2+abs(psiB[1])**2)/2
            pA += weight*abs((firstA@ground)[1])**2
            pB += weight*abs((firstB@ground)[1])**2
    return {'L_real': float(L.real), 'L_imag': float(L.imag),
            'excitation_total': float(excitation),
            'single_pulse_A': float(pA), 'single_pulse_B': float(pB),
            'area': float(area)}



def order_signal(p: float, s: float, width_phase: float = 0.,
                 frozen_isotropic: bool = False, swap: bool = False) -> dict:
    """Opposite-order Rx/Ry pulses on the two branches, zero detuning limit.

    At the first time the branch fields are (1,i); at the second (i,1).
    Exchanging the two branch programmes conjugates the desired overlap.
    """
    first = compile_fields(1j, 1., s) if swap else compile_fields(1., 1j, s)
    second = compile_fields(1., 1j, s) if swap else compile_fields(1j, 1., s)
    area = calibrated_area(p, frozen_isotropic)
    nodes, weights = gaussian_nodes(width_phase)
    us, uw = orientation_nodes(frozen_isotropic)
    ground = np.array([1.,0.], complex)
    L, pA, pB = 0j, 0., 0.
    for q,w in zip(nodes,weights):
        for u,wu in zip(us,uw):
            xa, xb = s/2+q, -s/2+q
            psiA = pulse(area*u,field_at(second,xa)) @ pulse(area*u,field_at(first,xa)) @ ground
            psiB = pulse(area*u,field_at(second,xb)) @ pulse(area*u,field_at(first,xb)) @ ground
            weight = float(w*wu)
            L += weight*np.vdot(psiB,psiA)
            pA += weight*abs(psiA[1])**2
            pB += weight*abs(psiB[1])**2
    return {'L_real':float(L.real),'L_imag':float(L.imag),
            'excited_probability_A':float(pA),'excited_probability_B':float(pB)}


def leakage_ratio(s: float, total_phase_sigma: float) -> float:
    """Ratio of averaged dark/bright INTENSITIES; not a general gate error."""
    q = math.exp(-2*total_phase_sigma**2)
    return (1-q)/(1-q*math.cos(2*s))


def run_checks() -> dict:
    alpha, eta, C, nu, f_laser, Iavg = 6.5, .03, .52, 3703.3, 1e5, 1.1e4
    s = 4*alpha*eta
    wavelength = 1e-2/nu
    kz_assumed = 2*np.pi/wavelength
    # Physical distances below assume the probe wavevector is along the cat axis.
    # The dimensionless s and compiler energy do not require that assumption.
    x0 = eta/kz_assumed
    d = 4*alpha*x0
    rng = np.random.default_rng(7)
    residual = 0.
    energy_error = 0.
    for _ in range(100):
        EA, EB = rng.normal(size=2)+1j*rng.normal(size=2)
        coef = compile_fields(EA, EB, s)
        residual = max(residual, abs(field_at(coef,s/2)-EA), abs(field_at(coef,-s/2)-EB))
        norm = float(np.vdot(coef,coef).real)
        formula = (abs(EA)**2+abs(EB)**2-2*np.cos(s)*np.real(EA*np.conj(EB)))/(2*np.sin(s)**2)
        energy_error = max(energy_error, abs(norm-formula))
    assert residual < 1e-12 and energy_error < 1e-12
    # Opposite-order waveforms have identical intensity at EVERY position,
    # so instantaneous intensity-only shifts receive the same exposure.
    # This identity does NOT imply that all atomic Stark-induced cat errors cancel.
    f1, f2 = compile_fields(1.,1j,s), compile_fields(1j,1.,s)
    intensity_identity_error = max(abs(abs(field_at(f1,x))**2 - abs(field_at(f2,x))**2)
                                   for x in np.linspace(-8*np.pi,8*np.pi,1001))
    assert intensity_identity_error < 1e-12
    # Illustrative STATIC-polarizability scale only, not a measured dynamic
    # 2.7-micron Ca+ Stark shift. Real local fluence at the atom must be calibrated.
    eps0, c_light, hbar, au_alpha = 8.8541878128e-12, 299792458., 1.054571817e-34, 1.64877727436e-41
    static_delta_alpha_au = -44.32  # Huang et al., arXiv:2202.07828
    illustrative_stark_phase = static_delta_alpha_au*au_alpha*(Iavg/f_laser*1e4)/(2*eps0*c_light*hbar)
    check_rows = []
    for p in [.01, .03, .10, .30]:
        plus = signal(p,s)
        minus = signal(p,s,phase=-np.pi/2)
        assert abs(plus['L_real']-(1-p)) < 1e-12
        assert abs(plus['L_imag']-p) < 1e-12
        assert abs(plus['excitation_total']-p*(1-p)) < 1e-12
        assert abs(plus['excitation_total']-minus['excitation_total']) < 1e-12
        finite = signal(p,s,width_phase=eta)
        swapped = signal(p,s,width_phase=eta,swap=True)
        assert abs(finite['L_real']-swapped['L_real']) < 1e-12
        assert abs(finite['L_imag']+swapped['L_imag']) < 1e-12
        finite_iso = signal(p,s,width_phase=eta,frozen_isotropic=True)
        jitter = signal(p,s,width_phase=eta,node_jitter=.06)
        check_rows.append({'scenario_single_pulse_p':p,'point_packet':plus,
                           'finite_width':finite,'finite_width_frozen_isotropic':finite_iso,
                           'finite_width_node_jitter_0p06':jitter})
    # Two noncommuting rotations: normalized trace of B^dag A^dag B A.
    order_rows = []
    for p in [.01,.03,.1,.3]:
        theta = calibrated_area(p)
        A,B = rotation(theta,0),rotation(theta,np.pi/2)
        overlap = np.trace((A@B).conj().T @ (B@A))/2
        target = 1-2*p*p
        assert abs(overlap-target) < 1e-12
        pure = order_signal(p,s)
        finite = order_signal(p,s,width_phase=eta)
        swapped = order_signal(p,s,width_phase=eta,swap=True)
        assert abs(pure['L_real']-(1-2*p*p))<1e-12
        assert abs(pure['L_imag']-2*p*(1-p))<1e-12
        assert abs(pure['excited_probability_A']-pure['excited_probability_B'])<1e-12
        assert abs(finite['L_imag']+swapped['L_imag'])<1e-12
        phase_randomized = 0j
        g = np.array([1.,0.],complex)
        for phi in np.linspace(0,2*np.pi,128,endpoint=False):
            UA = rotation(theta,phi+np.pi/2) @ rotation(theta,0)
            UB = rotation(theta,phi) @ rotation(theta,np.pi/2)
            phase_randomized += np.vdot(UB@g,UA@g)/128
        assert abs(phase_randomized-(1-2*p)) < 1e-12
        order_rows.append({'phase_randomized_real':float(phase_randomized.real),
                           'phase_randomized_imag':float(phase_randomized.imag),'scenario_p':p,'mixed_state_order_overlap':float(overlap.real),
                           'point_packet_formula':target, 'pure_ground_point':pure,
                           'pure_ground_finite_width':finite,
                           'pure_ground_finite_width_frozen_isotropic':order_signal(p,s,width_phase=eta,frozen_isotropic=True)})
    # Isotropic power leakage exact integral check.
    qx,qw=gaussian_nodes(eta)
    ratio_num=np.dot(qw,np.sin(qx)**2)/np.dot(qw,np.sin(s+qx)**2)
    assert abs(ratio_num-leakage_ratio(s,eta)) < 1e-12
    # Five-sigma, two phase settings, total independent Bernoulli trials N.
    sample_rows=[]
    for pgamma in [.01,.03,.1]:
        probability_difference = C*pgamma
        N=math.ceil((5/probability_difference)**2)
        sample_rows.append({'scenario_overlap_imaginary_amplitude_R':pgamma,
                            'probability_difference':probability_difference,
                            'N_total_two_settings_5sigma':N,
                            'minutes_at_assumed_50_completed_trials_per_second':N/50/60,
                            'loss_per_trial_for_90pct_survival':-math.log(.9)/N})
    gamma_intensity_half = math.sin(s)**2
    # A 1% leakage bound under the Gaussian static-noise model.
    def objective(jitter):
        return leakage_ratio(s,math.hypot(eta,jitter))-.01
    max_jitter=brentq(objective,0,.2)
    return {'status':'DERIVED IDEALIZED MODEL; NOT OBSERVED PERFORMANCE',
      'reference':{'paper':'Wu et al., Nature 657, 364-368 (2026); arXiv:2511.19687v2',
                   'alpha':alpha,'eta_approx':eta,'reference_contrast_not_guaranteed_for_new_protocol':C,
                   'wavenumber_cm_inverse':nu,'laser_repetition_Hz':f_laser,
                   'mean_intensity_W_per_cm2':Iavg},
      'geometry':{'s_kd':s,'wavelength_m':wavelength,
                   'x_zero_point_m_assuming_axial_beam':x0,
                   'branch_separation_m_assuming_axial_beam':d,
                   'incident_energy_ratio_one_addressed_branch':1/(2*np.sin(s)**2),
                   'per_pulse_local_fluence_fraction_two_pulses_fixed_energy':gamma_intensity_half,
                   'reference_incident_fluence_J_per_cm2':Iavg/f_laser,
                   'each_target_pulse_fluence_J_per_cm2_fixed_energy':Iavg/f_laser*gamma_intensity_half,
                   'opposite_order_each_local_pulse_fluence_fraction_fixed_total_energy':gamma_intensity_half/2,
                   'opposite_order_each_local_pulse_fluence_J_per_cm2_fixed_total_energy':Iavg/f_laser*gamma_intensity_half/2,
                   'width_only_dark_to_bright_intensity':leakage_ratio(s,eta),
                   'node_phase_sigma_for_1pct_leakage':max_jitter,
                   'node_position_sigma_m_assuming_axial_beam':max_jitter/kz_assumed},
      'tests':{'field_compilation_max_error':residual,'energy_identity_max_error':energy_error,
                'global_intensity_identity_max_error':intensity_identity_error,
                'exact_unitary_and_symmetry_assertions':'passed'},
      'atomic_Stark_scale_NOT_a_dynamic_prediction':{'static_differential_polarizability_au':static_delta_alpha_au,
        'illustrative_phase_rad_at_reference_local_fluence':illustrative_stark_phase,
        'warning':'Dynamic/tensor polarizability, local atomic fluence and resulting qubit-motion errors are not modeled.'},
      'two_pulse_scenarios':check_rows,'noncommuting_control_scenarios':order_rows,
      'acquisition_scenarios':sample_rows,
      'exclusions':['No measured molecular coherent response is supplied.',
                    'No internal dephasing time is assigned.',
                    'Atomic IR Stark dynamics and correction errors are not included.',
                    'No photochemical loss rate is assigned.',
                    'No full molecule spectrum or reaction model is simulated.',
                    'No proof of scientific or economic advantage is supplied.',
                    'No claim of novelty or external validation is established.']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('results.json'))
    args=parser.parse_args()
    result=run_checks()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'geometry':result['geometry'],'tests':result['tests'],
                     'acquisition_scenarios':result['acquisition_scenarios'],
                     'p0p03_finite_width':result['two_pulse_scenarios'][1]['finite_width']},indent=2))

if __name__=='__main__':
    main()

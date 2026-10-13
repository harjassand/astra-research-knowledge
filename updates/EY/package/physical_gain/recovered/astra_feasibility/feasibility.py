#!/usr/bin/env python3
"""Reproduce the scoped ASTRA feasibility calculations.

No quantities computed here are new measurements. This program differentiates a
published vibronic rate fit, checks coupled kinetic-response identities, and
calculates explicitly hypothetical measurement budgets. It is not a materials
simulation, an experimentally validated device model, or a novelty certificate.

Run: python feasibility.py --output results
Requires: Python 3.10+, NumPy, SciPy.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
from typing import Any

import numpy as np
import scipy
from scipy.constants import Boltzmann as KB, elementary_charge as E, epsilon_0 as EPS0
from scipy.constants import Avogadro as NA, Planck as H, speed_of_light as C
from scipy.integrate import solve_ivp
from scipy.special import gammaln, logsumexp

T = 298.15
KT_EV = KB * T / E


def mlj_log_rate_and_slope(
    gap_ev: float, temperature_k: float = T,
    lambda_s_ev: float = 0.15, vibration_ev: float = 0.186,
    huang_rhys: float = 2.7, terms: int = 100,
) -> tuple[float, float]:
    """Return log(rate/common prefactor) and -d log k/d gap [1/eV].

    Electronic coupling and all reorganization parameters are held fixed.
    Therefore the slope is NOT automatically a measured electric-field slope.
    """
    if temperature_k <= 0 or lambda_s_ev <= 0 or vibration_ev <= 0:
        raise ValueError("Temperature and energies must be positive")
    if huang_rhys <= 0 or terms < 20:
        raise ValueError("Require a positive Huang-Rhys factor and >=20 terms")
    w = np.arange(terms, dtype=float)
    kt_ev = KB * temperature_k / E
    z = lambda_s_ev + w * vibration_ev - gap_ev
    logs = -huang_rhys + w * np.log(huang_rhys) - gammaln(w + 1)
    logs -= z**2 / (4 * lambda_s_ev * kt_ev)
    logsum = float(logsumexp(logs))
    weights = np.exp(logs - logsum)
    slope = -float(np.dot(weights, z)) / (2 * lambda_s_ev * kt_ev)
    return logsum, slope


def marcus_rates(
    voltage: float, q_e: float, drive_ev: float, reorg_ev: float,
    prefactor_s: float, temperature_k: float,
) -> np.ndarray:
    """[a+, a-, b+, b-] for the symmetric chemical cycle; all rates in 1/s.

    q_e is charge in units of e, so q_e * voltage is an energy in eV.
    The four Marcus barriers implement local detailed balance together.
    """
    if reorg_ev <= 0 or prefactor_s <= 0 or temperature_k <= 0:
        raise ValueError("Positive reorganization, prefactor and T required")
    kt = KB * temperature_k / E
    d = drive_ev / 2
    z = np.array([reorg_ev-d-q_e*voltage,
                  reorg_ev+d+q_e*voltage,
                  reorg_ev-d+q_e*voltage,
                  reorg_ev+d-q_e*voltage])
    return prefactor_s * np.exp(-z*z/(4*reorg_ev*kt))


def immobile_chi(s: complex | np.ndarray, rho: float, mu: float,
                 occupation: float, recombination_s: float,
                 slope_per_joule: float) -> complex | np.ndarray:
    """Polarization susceptibility P/E [F/m], fixed isotropic dipoles.

    Population changes only; ground-state dipole is taken to be zero.
    Instantaneous electronic polarization and passive losses are separate.
    """
    if not 0 <= occupation < 1 or recombination_s <= 0:
        raise ValueError("Require 0<=p<1 and positive recombination rate")
    relaxation = recombination_s/(1-occupation)
    return -(rho*mu*mu/3)*occupation*(1-occupation)*slope_per_joule \
           * relaxation/(s+relaxation)


def rotating_chi(s: complex | np.ndarray, rho: float, mu: float,
                 occupation: float, recombination_s: float,
                 slope_per_joule: float, rotation_s: float,
                 temperature_k: float = T) -> complex | np.ndarray:
    """Two orientational-moment reduction, ground dipole zero.

    Both states have the same rotational diffusion rate b=1/tau_r. Optical
    pumping is orientation-isotropic, with no first-order field dependence.
    A nonzero pump slope can be used in a_eff only when the associated angular
    forcing remains this model's forcing. More general pumps require a new
    generator. Intramolecular charge hopping is not identical to this rotation.
    """
    p, k, b = occupation, recombination_s, rotation_s
    if not 0 <= p < 1 or k <= 0 or b < 0 or temperature_k <= 0:
        raise ValueError("Invalid kinetic inputs")
    if b == 0:
        return immobile_chi(s, rho, mu, p, k, slope_per_joule)
    pump = k*p/(1-p)
    beta = 1/(KB*temperature_k)
    numerator = b*beta*(1+pump/(s+b))-k*slope_per_joule
    return rho*mu*mu*p/3 * numerator/(s+pump+k+b)


def rotating_chi_matrix(s: complex, rho: float, mu: float,
                        p: float, k: float, a: float,
                        b: float, temperature_k: float = T) -> complex:
    """Independent 2x2 resolvent calculation of the same linear model."""
    pump = k*p/(1-p)
    beta = 1/(KB*temperature_k)
    matrix = np.array([[-k-b, pump], [k, -pump-b]], dtype=complex)
    force = mu*p/3*np.array([b*beta-k*a, k*a], dtype=complex)
    response = np.linalg.solve(s*np.eye(2)-matrix, force)
    return rho*mu*response[0]


def reaction_current_noise(omega: float, molecule_number: float,
                           q2_mean: float, p: float, k: float) -> float:
    """One-sided current noise PSD [A^2/Hz] for independent Markov sites.

    Convention: one-sided frequency f>=0, omega=2*pi*f; variance of Q is the
    integral S_Q(f) df. Pump and recombination jumps are stochastic.
    """
    relaxation = k/(1-p)
    return 4*molecule_number*q2_mean*p*(1-p)*relaxation*omega**2 \
           /(relaxation**2+omega**2)


def measurement_budget() -> dict[str, Any]:
    """One instrument-design example, NOT a qualified material prediction."""
    _, a_ev = mlj_log_rate_and_slope(1.5)
    a = a_ev/E
    rho = NA * 1.0  # 1 mol/m^3 = 1 millimolar; design assumption, not measured
    area, thickness, epsr = 1e-8, 1e-6, 2.0
    mu = 1.5e-9*E  # measured effective dipole target, NOT raw charge separation
    p, k = .01, .56e9
    pump = k*p/(1-p)
    relaxation = pump+k
    capacitance = EPS0*epsr*area/thickness
    cr = -area/thickness*rho*mu**2/3*p*(1-p)*a
    omega = relaxation
    y = 1j*omega*area/thickness*immobile_chi(1j*omega,rho,mu,p,k,a)
    gain = -float(y.real)
    number = rho*area*thickness
    photon_j = H*C/600e-9
    absorbed_minimum = number*p*k*photon_j
    voltage_peak = .01
    output_small_signal = .5*gain*voltage_peak**2
    noise = reaction_current_noise(omega, number, mu**2/(3*thickness**2), p, k)
    noise_temperature_ratio = 1/(KB*a)
    return {
        "status": "UNMEASURED instrument-design budget; no device performance claim",
        "inputs": {
            "k_s": {"value":k,"status":"published amplitude-average at source conditions"},
            "gap_ev": {"value":1.5,"status":"selected nominal point near low end of source CR1 range; not a precise same-device energy measurement"},
            "slope_per_ev": {"value":a_ev,"status":"derivative of published MLJ fit at fixed coupling and reorganization; field-slope transfer unverified"},
            "temperature_k": {"value":T,"status":"chosen room-temperature evaluation"},
            "density_m3": {"value":rho,"status":"design concentration target, not source measurement"},
            "effective_dipole_Cm": {"value":mu,"status":"required measurable target; not established for CdS-AZ in the proposed cell"},
            "occupation": {"value":p,"status":"pump-occupation target, not measured"},
            "area_m2": {"value":area,"status":"proposed geometry"},
            "thickness_m": {"value":thickness,"status":"proposed active thickness; extra interfaces omitted from this ideal budget"},
            "relative_background_permittivity": {"value":epsr,"status":"design assumption, must measure at RF under illumination"},
            "rotation": {"value":"immobile","status":"ideal comparison; actual orientation persistence not acquired"},
        },
        "derived": {
            "pump_creation_rate_s":pump,
            "kinetic_relaxation_s":relaxation,
            "corner_frequency_hz":omega/(2*np.pi),
            "background_capacitance_F":capacitance,
            "population_capacitance_F":cr,
            "population_gain_S":gain,
            "background_susceptance_S":omega*capacitance,
            "loss_tangent_upper_limit_if_no_other_losses":gain/(omega*capacitance),
            "probe_voltage_peak_V":voltage_peak,
            "in_phase_current_peak_A":gain*voltage_peak,
            "available_small_signal_output_W":output_small_signal,
            "minimum_absorbed_pump_W":absorbed_minimum,
            "small_signal_output_to_absorbed_ratio":output_small_signal/absorbed_minimum,
            "ideal_population_current_noise_A_per_sqrtHz":math.sqrt(noise),
            "noise_to_gain_equivalent_temperature_K":noise_temperature_ratio,
            "rotation_time_critical_s":1/(k*a*KB*T),
            "free_carrier_escape_lifetime_mobility_product_max_m2_per_V":mu**2*a/(6*E),
            "ratio_abs_Cr_to_C0":-cr/capacitance,
            "resonator_Q_min_if_Ctotal_equals_C0":omega*capacitance/gain,
            "molecule_number":number,
            "mean_center_spacing_m":rho**(-1/3),
            "productive_cycles_per_molecule_s":p*k,
            "destruction_probability_per_cycle_max_for_90pct_retention_1000s":-math.log(.9)/(p*k*1000),
            "heat_density_W_m3_if_output_negligible":absorbed_minimum/(area*thickness),
        },
    }


def checks() -> list[dict[str, Any]]:
    out: list[dict[str,Any]]=[]
    def record(name: str, passed: bool, detail: str) -> None:
        out.append({"name":name,"passed":bool(passed),"detail":detail})
        if not passed:
            raise AssertionError(name+": "+detail)

    # Finite differences of the published MLJ fit, no experimental refit.
    slopes=[]
    for d in np.linspace(.2,2.0,91):
        _, a=mlj_log_rate_and_slope(float(d))
        h=1e-6
        fd=-(mlj_log_rate_and_slope(float(d+h))[0]-mlj_log_rate_and_slope(float(d-h))[0])/(2*h)
        slopes.append(abs(a-fd))
    record("MLJ analytic derivative versus centered differences",max(slopes)<1e-7,
           f"91 gaps; max absolute error {max(slopes):.4g} per eV")
    err=max(abs(mlj_log_rate_and_slope(float(d),terms=100)[1]-mlj_log_rate_and_slope(float(d),terms=200)[1]) for d in np.linspace(.2,2.,91))
    record("MLJ truncation convergence",err<1e-12,f"100 vs 200 terms; max slope change {err:.4g}")

    # Marcus reciprocal kinetics: input rate sensitivities are not independent.
    q, drive, reorg, pref, temp=.3,.4374,.0729,1e9,423.
    kt=KB*temp/E
    errors=[]
    for v in np.linspace(-.2,.2,41):
        ap,am,bp,bm=marcus_rates(float(v),q,drive,reorg,pref,temp)
        errors.extend([abs(math.log(ap/am)-(drive/2+q*v)/kt),
                       abs(math.log(bp/bm)-(drive/2-q*v)/kt),
                       abs(math.log(ap*bp/(am*bm))-drive/kt)])
    record("Marcus local detailed balance and voltage-independent affinity",max(errors)<1e-12,
           f"41 voltages; max log-ratio error {max(errors):.4g}")
    def stationary(v: float) -> float:
        ap,am,bp,bm=marcus_rates(v,q,drive,reorg,pref,temp)
        return (ap+bm)/(ap+am+bp+bm)
    h=1e-6
    derivative=(stationary(h)-stationary(-h))/(2*h)
    gamma=drive/(2*reorg)
    expected=q/(4*kt)*(1-gamma*math.tanh(drive/(4*kt)))
    record("Marcus coupled gamma reproduces chemical response",abs(derivative-expected)<1e-8,
           f"gamma={gamma:.8g}; derivative={derivative:.8g} /V")
    delta=math.sqrt(2*reorg*kt)
    objective=lambda x:x/reorg*math.exp(-x*x/(4*reorg*kt))
    record("Strong-drive negative-conductance optimum",objective(delta)>max(objective(.99*delta),objective(1.01*delta)),
           "Scoped constant-prefactor, strong-drive Marcus expression; not a materials optimization")

    # Analytic orientational response compared with direct linear algebra.
    rho=NA; mu=1.5e-9*E; p=.01; k=.56e9
    a=mlj_log_rate_and_slope(1.5)[1]/E
    errs=[]
    for b in [1e5,1e7,1e8,1e9]:
        for omega in np.geomspace(1e5,1e12,81):
            analytic=rotating_chi(1j*omega,rho,mu,p,k,a,b)
            direct=rotating_chi_matrix(1j*omega,rho,mu,p,k,a,b)
            errs.append(abs(analytic-direct)/max(abs(direct),1e-30))
    record("Rotation closed form versus 2x2 resolvent",max(errs)<1e-10,
           f"324 complex evaluations; max relative discrepancy {max(errs):.4g}")
    s=1j*k
    limit=rotating_chi(s,rho,mu,p,k,a,1e-3)
    fixed=immobile_chi(s,rho,mu,p,k,a)
    record("Immobile limit",abs(limit-fixed)/abs(fixed)<1e-9,
           f"relative discrepancy {abs(limit-fixed)/abs(fixed):.4g}")
    grid=np.geomspace(1e4,1e13,2001)
    bcrit=k*a*KB*T
    no_gain=np.real(1j*grid*rotating_chi(1j*grid,rho,mu,p,k,a,2*bcrit))
    has_gain=np.real(1j*grid*rotating_chi(1j*grid,rho,mu,p,k,a,.5*bcrit))
    record("Fast rotation no-gain control",bool(np.all(no_gain>0)),
           "b=2 bcrit; positive population+rotation absorption throughout finite test grid")
    record("Slow rotation gain case",bool(np.any(has_gain<0)),
           "b=0.5 bcrit; negative absorption exists in finite test grid, before other device losses")
    normal=np.real(1j*grid*rotating_chi(1j*grid,rho,mu,p,k,-a,1e8))
    record("Normal-region slope control",bool(np.all(normal>0)),
           "Negative a produces positive absorption on test grid")
    dark=rotating_chi(1j*grid,rho,mu,0.,k,a,1e8)
    record("No-pump population-response control",bool(np.all(dark==0)),
           "Does not include passive background dielectric response")

    # Independent time-domain integration of the linear angular equations.
    b=.5*bcrit; pump=k*p/(1-p); rate=pump+k
    omega=rate; ef=1e3; beta=1/(KB*T)
    mat=np.array([[-k-b,pump],[k,-pump-b]])
    forcing=mu*p/3*np.array([b*beta-k*a,k*a])*ef
    # Normalize time by rate and moment by forcing/rate to avoid small atol.
    scale=float(np.linalg.norm(forcing)/rate)
    matn=mat/rate; fn=forcing/(rate*scale)
    period=2*np.pi
    def fun(tau: float, moment: np.ndarray) -> np.ndarray:
        return matn@moment+fn*np.cos(tau)
    sol=solve_ivp(fun,[0,100*period],np.zeros(2),method="DOP853",rtol=1e-10,atol=1e-12,dense_output=True,max_step=.1)
    if not sol.success:
        raise RuntimeError(sol.message)
    tau=np.linspace(80*period,100*period,20001)
    m=sol.sol(tau)[0]*scale
    phasor=(np.trapezoid(m*np.cos(tau),tau)-1j*np.trapezoid(m*np.sin(tau),tau))*2/(20*period)
    theory=rotating_chi(1j*omega,rho,mu,p,k,a,b)*ef/(rho*mu)
    record("Rotation frequency response versus time-domain integration",abs(phasor-theory)/abs(theory)<1e-7,
           f"100 cycles integrated; relative phasor error {abs(phasor-theory)/abs(theory):.4g}; same model, no physical validation")

    # The optical preparation state is not part of the two-state model.
    # Compare a three-state G->X->C->G response with its fast-X reduction,
    # with constant injection and pump rates and zero X dipole, just for this
    # limiting calculation. No injection yield or X dipole is measured here.
    inj=.038e12
    W=k*p/(1-p)  # unit-yield limiting case; actual pump rate needs measurement
    J=np.array([[-W-inj,-W],[inj,-k]])
    g=1/(1+W/inj+W/k)
    x=W*g/inj
    pc=inj*x/k
    field_force=np.array([0.,-k*a*mu*pc])
    om=k/(1-p)
    c_resp=np.linalg.solve(1j*om*np.eye(2)-J,field_force)[1]
    approximate=-mu*p*(1-p)*a*(k/(1-p))/(1j*om+k/(1-p))
    three_error=abs(c_resp-approximate)/abs(approximate)
    record("Fast optical-intermediate reduction",three_error<1e-3,
           f"G-X-C generator vs two-state limit; relative error {three_error:.4g}; zero X dipole and unit yield assumed only in this test")

    # Geometry cancellation and stochastic noise-to-gain identity.
    ratios=[]; noise_ratios=[]
    for d in [1e-7,1e-6,1e-5]:
        area=1e-8
        q2=mu*mu/(3*d*d); num=rho*area*d
        cr=-num*q2*p*(1-p)*a
        c0=EPS0*2*area/d
        ratios.append(-cr/c0)
        om=k/(1-p)
        gain=-float(np.real(1j*om*area/d*immobile_chi(1j*om,rho,mu,p,k,a)))
        noise_ratios.append(reaction_current_noise(om,num,q2,p,k)/(4*gain))
    record("Filled-gap reciprocal geometry cancellation",np.ptp(ratios)<1e-15,
           f"|Cr|/C0={ratios[0]:.8g} at all 3 thicknesses; fixed density and material response")
    record("Population shot-noise to gain identity",np.max(np.abs(np.array(noise_ratios)*a-1))<1e-12,
           "S_I/(4 |Re Y_population|)=1/a for independent fixed isotropic two-state sites")
    bd=measurement_budget(); der=bd["derived"]
    ratio_formula=a*(mu*.01/1e-6)**2/(12*H*C/600e-9)
    record("Small-signal optical energy-ratio identity",abs(ratio_formula/der["small_signal_output_to_absorbed_ratio"]-1)<1e-12,
           "Ideal productive absorption and omega=R+k; no total system-efficiency claim")
    # Mobile escaped charges introduce real conductivity even with blocking
    # electrodes at frequencies where a bulk mobility description applies.
    mobile_mu=1e-8; mobile_lifetime=1e-3  # illustrative only, not measurements
    threshold=mu**2*a/(6*E)
    escape=threshold/(mobile_mu*mobile_lifetime)
    sigma_mobile=E*rho*p*k*escape*mobile_lifetime*mobile_mu
    sigma_gain=rho*mu**2*p*k*a/6
    record("Escaped-carrier leakage product bound",abs(sigma_mobile/sigma_gain-1)<1e-12,
           "At omega=R+k: f_escape*tau_free*mobility_sum < mu_dipole^2*a/(6e); no mobility or escape fraction acquired")
    return out


def write_results(outdir: Path) -> dict[str,Any]:
    outdir.mkdir(parents=True,exist_ok=True)
    test_results=checks()
    budget=measurement_budget()
    _, aev=mlj_log_rate_and_slope(1.5)
    k=.56e9; p=.01; a=aev/E
    critical=1/(k*a*KB*T)
    rotation=[]
    frequencies=np.geomspace(1e5,5e8,701)
    for tau_ns in [2.,5.,8.,12.,20.,50.,100.,1e9]:
        b=1/(tau_ns*1e-9)
        adm=1j*(2*np.pi*frequencies)*1e-2*rotating_chi(1j*2*np.pi*frequencies,NA,1.5e-9*E,p,k,a,b)
        idx=int(np.argmin(adm.real))
        rotation.append({"tau_ns":tau_ns,"any_negative_on_grid":bool(np.min(adm.real)<0),
                         "minimum_population_and_rotation_ReY_S":float(adm.real[idx]),
                         "frequency_at_grid_minimum_Hz":float(frequencies[idx]),
                         "population_and_rotation_ReY_at_90MHz_S":float(np.real(1j*2*np.pi*90e6*1e-2*rotating_chi(1j*2*np.pi*90e6,NA,1.5e-9*E,p,k,a,b)))})
    with (outdir/'mlj_slope.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['gap_eV','log_relative_rate','minus_dlogk_dgap_per_eV'])
        for d in np.linspace(.2,2.,181):
            z=mlj_log_rate_and_slope(float(d));writer.writerow([d,*z])
    with (outdir/'rotation_response.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['frequency_Hz','tau_rotation_ns','population_plus_rotation_real_Y_S','population_plus_rotation_imag_Y_S'])
        for tau_ns in [5.,8.,20.,50.,100.]:
            yy=1j*2*np.pi*frequencies*1e-2*rotating_chi(1j*2*np.pi*frequencies,NA,1.5e-9*E,p,k,a,1/(tau_ns*1e-9))
            for ff,v in zip(frequencies,yy):writer.writerow([ff,tau_ns,v.real,v.imag])
    results={"scope":"Analytic feasibility and instrument-budget calculations; no measured gain or qualified material",
             "measured_source":"Wang et al., Nature Communications 12,6333 (2021), DOI 10.1038/s41467-021-26705-x",
             "budget":budget,"rotation_critical_time_s":critical,"rotation_grid":rotation,
             "checks":test_results,
             "counts":{"test_groups":len(test_results),"passed":sum(r['passed'] for r in test_results)},
             "environment":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__}}
    (outdir/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    return results


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).parent/'results')
    args=parser.parse_args()
    r=write_results(args.output)
    print(json.dumps({"counts":r['counts'],"budget":r['budget']['derived'],"rotation_grid":r['rotation_grid']},indent=2))


if __name__=='__main__':
    main()

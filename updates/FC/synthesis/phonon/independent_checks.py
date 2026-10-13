#!/usr/bin/env python3
"""Independent kinematics and conditional probability checks, not a Te simulator."""
from __future__ import annotations

from fractions import Fraction
from functools import reduce
from pathlib import Path
import json
import math
import platform

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import log_ndtr, ndtr, ndtri

EV = 1.602176634e-19
C = 299792458.0
U = 1.66053906892e-27
ME = 9.1093837139e-31
KB = 1.380649e-23
M = 127.60 * U
FREQ = 3.24e12
OMEGA = math.tau * FREQ


def momentum(energy_ev):
    e = energy_ev * EV
    return math.sqrt(e * (e + 2 * ME * C * C)) / C


def recoil(energy_ev):
    p = momentum(energy_ev)
    return 2 * p * p / (M * EV)


def recoil_slope(energy_ev):
    return 4 * (energy_ev * EV + ME * C * C) / (M * C * C)


def optimal_rate_log10(d, ratio):
    """Largest target event probability compatible with Gaussian ROC and ratio."""
    z = brentq(lambda z: log_ndtr(z) - log_ndtr(z-d) - math.log(ratio), -1000, 30)
    return {"normal_quantile": z, "target_probability": float(ndtr(z)),
            "log10_target_probability": float(log_ndtr(z) / math.log(10)),
            "unwanted_probability": float(ndtr(z-d)),
            "ratio": ratio, "separation": d}


def write_success(n, m, ratio):
    return reduce(lambda x, k: x * Fraction(k * ratio, k * ratio + m),
                  range(1, n+1), Fraction(1))


def write_log_success(n, m, ratio):
    return -math.fsum(math.log1p(m/(k*ratio)) for k in range(1, n+1))


def main():
    tables = []
    pm_speed = OMEGA * 1e-12
    for e in (100000, 200000, 300000, 500000):
        shift = 2 * momentum(e) * pm_speed / EV
        numerical = (recoil(e+0.5)-recoil(e-0.5))
        assert math.isclose(numerical, recoil_slope(e), rel_tol=2e-10)
        tables.append({"beam_keV": e/1000, "stationary_recoil_eV": recoil(e),
                       "shift_eV_per_pm": shift, "basis_splitting_eV_per_pm": 1.5*shift,
                       "equivalent_beam_shift_keV_per_pm": shift/recoil_slope(e)/1000})

    # Number density from the primary paper's three-atom hexagonal cell, not RSC density.
    a, cc = 4.456e-10, 5.927e-10
    number_density = 3 / (math.sqrt(3) * a*a*cc / 2)
    absorbed_ev = 1.4e27 * 1.57 / number_density
    speed_literal = OMEGA * 0.24e-10
    literal_ev = M * speed_literal**2 / (2*EV)
    ceiling_speed = math.sqrt(2*EV*absorbed_ev/M)
    sigma300 = math.sqrt(KB * 300 / M)
    energy = {"primary_lattice_atom_density_cm3": number_density/1e6,
              "absorbed_estimate_eV_atom": absorbed_ev,
              "literal_amplitude_speed_m_s": speed_literal,
              "literal_amplitude_energy_eV_atom": literal_ev,
              "literal_over_absorbed": literal_ev/absorbed_ev,
              "all_absorbed_coherent_speed_ceiling_m_s": ceiling_speed,
              "assumptions": "Equal per-atom radial amplitudes, same volume, no other energy reservoir; ceiling is not an operating point"}

    moment_count = 0
    for theta in np.linspace(0, math.tau, 81):
        cs = np.cos(theta - math.tau*np.arange(3)/3)
        assert abs(cs.sum()) < 3e-15
        assert abs(cs @ cs - 1.5) < 4e-15
        assert abs(np.sum(cs**3) - .75*math.cos(3*theta)) < 4e-15
        moment_count += 1

    # Exact analytic dual formula for two contrast rows; the written proof covers
    # any finite number of rows. This is supplied-subspace geometry, not Te modes.
    geometry_count = 0
    rng = np.random.default_rng(20261013)
    for dim in (1,2,3,7):
        for _ in range(75):
            g1,g2 = rng.normal(size=(2,dim))
            difference = g1-g2
            lam = float(np.clip(-g2 @ difference/(difference @ difference),0,1))
            nearest = lam*g1+(1-lam)*g2
            distance = float(np.linalg.norm(nearest))
            if distance > 1e-12:
                u = math.sqrt(2)*nearest/distance
                assert abs(min(g1@u,g2@u)-math.sqrt(2)*distance) < 2e-12
            else:
                assert distance < 1e-12
            for _ in range(4):
                trial = rng.normal(size=dim)
                trial *= math.sqrt(2)*rng.random()/np.linalg.norm(trial)
                assert min(g1@trial,g2@trial) <= math.sqrt(2)*distance+2e-12
            geometry_count += 1
    # Dimensionless q=M=E_cell=1; compare native radial and supplied collinear modes.
    native_g = 1.5/math.sqrt(3)
    collinear_nearest = np.array([1,-.5,-.5])
    native_margin = math.sqrt(2)*native_g
    collinear_margin = math.sqrt(2)*np.linalg.norm(collinear_nearest)
    assert math.isclose(collinear_margin/native_margin, math.sqrt(2), rel_tol=1e-14)

    # Integrating over outgoing azimuth cancels the transverse impulse at first order.
    angle_count = 0
    azimuth = math.tau * np.arange(1024)/1024
    for chi in np.linspace(.05, math.pi, 32):
        p = momentum(300000)
        q = p * np.vstack((-math.sin(chi)*np.cos(azimuth),
                          -math.sin(chi)*np.sin(azimuth),
                          np.full_like(azimuth, 1-math.cos(chi)))).T
        assert np.max(abs(np.sum(q*q, axis=1)-4*p*p*math.sin(chi/2)**2)) < 1e-55
        for velocity in ((10, 20, 30), (-50, 8, 0), (0, 0, 21)):
            average = float(np.mean(q @ velocity))
            expected = p*(1-math.cos(chi))*velocity[2]
            assert abs(average-expected) < 2e-34
            angle_count += 1

    # The exact Gaussian extremizer is a likelihood-ratio half-space. Check both
    # the analytic threshold equality and smooth common response functions.
    roc_equalities = 0
    smooth_roc = 0
    for d in (.1, .25, .5, 1, 2, 4):
        for pt in (.001, .01, .25, .75, .99):
            cutoff = d/2-ndtri(pt)
            pu = float(ndtr(-d/2-cutoff))
            bound = float(ndtr(ndtri(pt)-d))
            assert abs(pu-bound) < 8e-16
            roc_equalities += 1
        for slope in (.2, 1, 5):
            for cut in (-2, 0, 2):
                g = lambda x: .5 + .5*math.tanh(slope*(x-cut)/2)
                density = lambda x, mu: math.exp(-.5*(x-mu)**2)/math.sqrt(math.tau)
                pt = quad(lambda x: g(x)*density(x,d/2), -14, 14, epsabs=1e-12)[0]
                pu = quad(lambda x: g(x)*density(x,-d/2), -14, 14, epsabs=1e-12)[0]
                assert pu + 2e-11 >= ndtr(ndtri(pt)-d)
                smooth_roc += 1

    Rfixed = math.log(.01)/math.log(.99)
    thermal_table = []
    for A in (1, 2, 5, 10):
        d = 1.5 * pm_speed * A / sigma300
        row = {"hypothetical_measured_amplitude_pm": A,
               "classical_temperature_K": 300, "projected_noise_m_s": sigma300,
               "d": d, "fixed_dose_458_ratio_probability_ceiling": optimal_rate_log10(d, Rfixed)}
        thermal_table.append(row)
    d_ceiling = 1.5*ceiling_speed/sigma300
    critical_d = 2*float(ndtri(.99))
    thermal = {"scope": "Scalar recoil-only Gaussian model; no acquired Te covariance/kernel and no physical no-go claim",
               "classical_sigma_300K_m_s": sigma300,
               "all_coherent_d_ceiling_300K": d_ceiling,
               "minimum_unwanted_if_single_collision_target_99pct": float(ndtr(ndtri(.99)-d_ceiling)),
               "single_collision_99_1_separation_required": critical_d,
               "single_collision_99_1_energy_eV_atom_300K": (2/9)*critical_d**2*KB*300/EV,
               "fixed_dose_hazard_ratio_required": Rfixed,
               "table": thermal_table}

    # Exact finite rational Bellman and superharmonic checks under legal global
    # hazard controls. No random material rates or quantum trajectories imported.
    adaptive_count = 0
    for n in range(1,9):
        for m in range(1,6):
            for R in (1,2,5,99,458,1000):
                previous = Fraction(1)
                value = Fraction(1)
                for k in range(1,n+1):
                    optimum = max(Fraction(k*r, k*r+m)*previous
                                  for r in (Fraction(R,3),Fraction(R,2),Fraction(R)))
                    value *= Fraction(k*R, k*R+m)
                    assert optimum == value
                    # Generator of the claimed upper potential for each control.
                    for r in (Fraction(R,3), Fraction(R,2), Fraction(R)):
                        residual = k*r*(previous-value) - m*value
                        assert residual <= 0
                    previous = optimum
                assert value == write_success(n,m,R)
                adaptive_count += 1

    parallel_examples = []
    for n,m in ((1,1),(10,20),(100,200),(1000,2000)):
        root = brentq(lambda R: write_log_success(n,m,R)-math.log(.99), 1e-3, 1e9)
        harmonic = math.fsum(1/k for k in range(1,n+1))
        parallel_examples.append({"target_sites":n,"unwanted_sites":m,
                                  "success_at_R458_2106": math.exp(write_log_success(n,m,Rfixed)),
                                  "minimum_R_for_99pct_global_success":root,
                                  "simple_sufficient_R":m*harmonic/(-math.log(.99)),
                                  "mean_mobility_dose_to_complete_at_unit_target_rate":harmonic})
    assert write_success(1,1,99) == Fraction(99,100)
    assert write_success(2,1,99) == Fraction(99,100)*Fraction(198,199)

    out = {"status":"Independent exact/finite/floating mathematical diagnostics; no atomistic or experimental validation",
           "python":platform.python_version(), "recoil_table":tables,
           "energy_consistency":energy,
           "linear_gaussian_pulse_attenuation":{
               str(w): math.exp(-.5*OMEGA**2*(w*1e-15/math.sqrt(8*math.log(2)))**2)
               for w in (28,50,100,200)},
           "conditional_gaussian_bound":thermal,
           "adaptive_parallel_write":parallel_examples,
           "checks":{"three_site_moments":moment_count,
                     "supplied_subspace_geometry_fixtures":geometry_count,
                     "finite_angle_azimuth_average":angle_count,
                     "gaussian_optimal_threshold_equalities":roc_equalities,
                     "gaussian_smooth_response_inequalities":smooth_roc,
                     "exact_rational_adaptive_Bellman_fixtures":adaptive_count,
                     "passed":True}}
    rendered = json.dumps(out,indent=2,allow_nan=False)+"\n"
    Path(__file__).with_name("independent_results.json").write_text(rendered)
    print(rendered,end="")


if __name__ == "__main__":
    main()

"""Exact rational resonance screening and a thermal-detector objection.

This is a new diagnostic, not a physical full-channel error certificate.
The resonance screen is infinite-duration, pure single-harmonic perturbation
theory. The thermal calculation is an independent ideal direct detector of a
stationary blackbody traveling field, with a rectangular frequency passband.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.constants import h, k
from scipy.linalg import eigvalsh
from numpy.polynomial.legendre import leggauss
from math import factorial, pi, prod


def first_band_event(fa, fp, flo, fhi, max_order=80, require_source=False):
    fa, fp, flo, fhi = map(F, (fa, fp, flo, fhi))
    if fp == 0:
        return None
    for order in range(1, max_order + 1):
        # r cannot exceed available energy / lowest detected frequency.
        for m in range(order % 2, order + 1, 2):
            if m == 0:
                continue
            for ns in range(order % 2, int(m * fp / fa) + 1, 2):
                if require_source and ns == 0:
                    continue
                rem = m * fp - ns * fa
                for photons in range(1 + (order + 1) % 2, int(rem / flo) + 1, 2):
                    # Strict inequalities demand nonzero continuum phase space;
                    # all photons exactly at a hard band edge has zero measure.
                    if photons * flo < rem < photons * fhi:
                        return {"order": order, "net_pump_quanta": m,
                                "source_photons": ns, "bath_photons": photons,
                                "total_bath_energy_GHz": str(rem)}
    return None


def first_any_detected_with_soft_bath(fa, fp, flo, max_order=80):
    """Permit extra unobserved bath photons at arbitrary positive frequency."""
    fa, fp, flo = map(F, (fa, fp, flo))
    for order in range(1, max_order+1):
        # Odd order needs an odd source occupation (at least one). Even order
        # may leave the source empty and emit one detected plus one soft photon.
        minimum = (order % 2)*fa + flo
        for m in range(1 + (order+1)%2, order+1, 2):
            if m*fp > minimum:
                return {"order":order,"net_pump_quanta":m,
                        "minimum_source_photons":order%2,
                        "available_bath_energy_GHz":str(m*fp-(order%2)*fa)}
    return None


def first_weak_seed(fa, fp, max_order=80):
    fa, fp = map(F, (fa, fp))
    for order in range(1, max_order + 1, 2):
        for m in range(1, order + 1, 2):
            # Strictly positive emitted frequency: f=0 is not a positive mode.
            if m * fp > fa:
                return {"order": order, "net_pump_quanta": m,
                        "source_photons": 1, "weak_frequency_GHz": str(m * fp-fa)}
    return None


def thermal_detector(center_GHz, bandwidth_GHz, duration_ns, temp_mK, eta, N):
    """Nyström covariance spectrum on a time and frequency window.

    Eigenvalues of sqrt(wt) C(t,s) sqrt(wt) give thermal detector mode means
    after efficiency loss. Vacuum probability is det(1+C)^-1. The propagating
    field has [b(f), b†(f')]=delta(f-f'); GHz*ns=1.
    """
    u, w = leggauss(N)
    ts = duration_ns * (u + 1) / 2
    wt = duration_ns * w / 2
    fs = center_GHz + bandwidth_GHz * u / 2
    wf = bandwidth_GHz * w / 2
    occ = 1 / np.expm1(h * (fs * 1e9) / (k * temp_mK * 1e-3))
    # Removing the center-frequency phase is a unitary and helps conditioning.
    A = (np.sqrt(wt)[:, None] * np.exp(2j*np.pi*np.outer(ts, fs-center_GHz))
         * np.sqrt(wf * eta * occ)[None, :])
    cov = A @ A.conj().T
    raw_lams = eigvalsh(cov)
    # Numerical negative eigenvalues are recorded, then clipped for probability.
    lams = np.maximum(raw_lams, 0)
    logp0 = -np.log1p(lams).sum()
    p0 = float(np.exp(logp0))
    r = lams / (1+lams)
    p1 = float(p0 * r.sum())
    p2 = float(p0 * (r.sum()**2 + (r*r).sum())/2)
    return {"frequency_GHz": center_GHz, "bandwidth_GHz": bandwidth_GHz,
            "duration_ns": duration_ns, "temperature_mK": temp_mK,
            "efficiency": eta, "quadrature_order": N,
            "mean_count": float(lams.sum()),
            "q_at_least_1": float(-np.expm1(logp0)),
            "q_at_least_2": float(-np.expm1(logp0)-p1),
            "q_at_least_3": float(-np.expm1(logp0)-p1-p2),
            "min_raw_eigenvalue": float(raw_lams.min()),
            "buffer_nonvacuum_equilibrium": float(np.exp(-h*center_GHz*1e9/(k*temp_mK*1e-3)))}


def main():
    cases = [
        ("baseline_up", "5", "16", "6", "8"),
        ("low_up", "5", "1", "1.86", "2.14"),
        ("low_down", "5", ".5", "1.36", "1.64"),
        ("still_lower_down", "5", ".25", "1.44", "1.72"),
        ("passive", "5", "0", "1.52", "1.82"),
    ]
    screens = {}
    for name, fa, fp, lo, hi in cases:
        screens[name] = {"fa": fa, "fp": fp, "band": [lo,hi],
                        "first_all_bath_photons_in_band_event": first_band_event(fa,fp,lo,hi),
                        "first_source_and_all_bath_photons_in_band_seed": first_band_event(fa,fp,lo,hi,require_source=True),
                        "first_any_detected_event_with_soft_bath":first_any_detected_with_soft_bath(fa,fp,lo),
                        "first_source_and_arbitrary_positive_weak_seed": first_weak_seed(fa,fp)}
    thermal = []
    for freq in [1.5, 2.0, 5/3, 7.0]:
        for temp in [5,10,20,30]:
            fine = thermal_detector(freq,.28,7,temp,.9,96)
            coarse = thermal_detector(freq,.28,7,temp,.9,48)
            fine['coarse_fine_max_probability_difference'] = max(
                abs(fine[key]-coarse[key]) for key in ['q_at_least_1','q_at_least_2','q_at_least_3'])
            thermal.append(fine)
    smooth_bound = []
    # Analytic uniform bound for Fourier transform of sin^(2p)(pi t/T).
    # The floating evaluations below are not outward interval enclosures.
    for pump in [0,.5,1]:
        duration, power, A = 7, 2, 6
        gap = 5-pump
        fourier_bound = factorial(2*power)/(2**(2*power)*pi*gap
                          * prod((gap*duration)**2-j*j for j in range(1,power+1)))
        smooth_bound.append({"source_GHz":5,"pump_GHz":pump,
            "duration_ns":duration,"envelope_power":2*power,
            "A_rad_per_ns":A,"fourier_uniform_bound_ns":fourier_bound,
            "first_Dyson_vector_squared_bound":A*A*fourier_bound**2/4,
            "scope":"first Dyson vector only, vacuum positive-frequency bath, arbitrary finite phase variance; no all-orders remainder"})
    pi_lower = F(314159,100000)
    delta, duration, amplitude = F(9,2), F(7), F(6)
    transform_upper = F(3,2)/(pi_lower*delta*((delta*duration)**2-1)*((delta*duration)**2-4))
    coefficient_upper = amplitude**2*transform_upper**2/4
    first_vertex_exact_check = {"pi_lower":"314159/100000",
        "fourier_upper_rational":str(transform_upper),
        "coefficient_upper_rational":str(coefficient_upper),
        "claim":"first Dyson vector squared norm < 1.056e-13",
        "strict_rational_comparison":coefficient_upper < F(1056,10**16)}
    assert first_vertex_exact_check['strict_rational_comparison']
    data = {"status":"diagnostic_only; quadrature convergence is not interval certification",
            "resonance_screen":screens,"thermal_detector":thermal,
            "smooth_pulse_first_vertex_bound":smooth_bound,
            "first_vertex_exact_arithmetic":first_vertex_exact_check,
            "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = Path(__file__).with_suffix('.json')
    out.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({"output":str(out),"resonance_screen":screens,
                      "smooth_pulse_first_vertex_bound":smooth_bound,
                      "thermal_20mK":[x for x in thermal if x['temperature_mK']==20]},indent=2))


if __name__ == '__main__':
    main()

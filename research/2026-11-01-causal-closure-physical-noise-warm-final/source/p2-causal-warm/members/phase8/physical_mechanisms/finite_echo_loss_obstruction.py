"""Exact old-mode loss response of finite dispersive echoes.

No optimized forced gate is claimed. Ideal sign reversals are deliberately
granted; real pulse/control exposure is an additional physical requirement.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq


def old_column_overlap(kappa, chi, durations, signs):
    """<v_-|v_+>, including the retained endpoint and all output times."""
    elapsed = 0.0
    theta = 0.0
    q = 0.0j
    for duration, sign in zip(durations, signs):
        rate = kappa + 2j * chi * sign
        integral = -np.expm1(-rate * duration) / rate
        q += kappa * np.exp(-kappa * elapsed - 2j * theta) * integral
        elapsed += duration
        theta += chi * sign * duration
    q += np.exp(-kappa * elapsed - 2j * theta)
    return complex(q), theta


def positive_mismatch(kappa, chi, durations, signs):
    """Compute 1-Re(q) without subtracting nearly equal numbers."""
    elapsed = 0.0
    theta = 0.0
    value = 0.0
    for duration, sign in zip(durations, signs):
        integrand = lambda s: 2 * kappa * math.exp(-kappa * (elapsed+s)) * math.sin(theta+chi*sign*s)**2
        value += quad(integrand, 0, duration, epsabs=1e-24, epsrel=1e-12)[0]
        elapsed += duration
        theta += chi * sign * duration
    value += 2 * math.exp(-kappa * elapsed) * math.sin(theta)**2
    return value


def echo_entry(kappa, chi, T, N, durations, signs):
    q, final_theta = old_column_overlap(kappa, chi, durations, signs)
    nu = positive_mismatch(kappa, chi, durations, signs)
    # The positive integral is more accurate than 1-q.real at weak loss.
    q = complex(1-nu, q.imag)
    multiplier = np.exp(N * complex(-nu, q.imag))
    return {
        "durations": list(durations), "signs": list(signs),
        "q_real": q.real, "q_imag": q.imag,
        "final_theta": final_theta,
        "one_minus_real_q_positive_integral": nu,
        "coherent_mean_occupation": N,
        "coherent_magnitude_loss_probability": -np.expm1(-N*nu)/2,
        "coherent_phase_radians": N*q.imag,
        "coherent_half_trace_distance_from_ideal_plus": abs(1-multiplier)/2,
        "mean_occupation_for_half_coherence_magnitude": math.log(2)/nu,
        "fock_N_magnitude_loss_probability": (1-abs(q)**N)/2,
        "fock_N_phase_radians": N*np.angle(q),
    }


def independent_lindblad_check():
    # Off-diagonal data block sigma obeys dot sigma = -i chi*y{n,sigma}
    # +kappa D[a](sigma). Its initial trace is normalized to one.
    kappa, chi, T, alpha, cutoff = 0.7, 1.3, 2.4, 0.8+0.35j, 32
    amplitudes = np.empty(cutoff, complex)
    amplitudes[0] = np.exp(-abs(alpha)**2/2)
    for n in range(1, cutoff):
        amplitudes[n] = amplitudes[n-1]*alpha/math.sqrt(n)
    norm = float(np.vdot(amplitudes, amplitudes).real)
    amplitudes /= math.sqrt(norm)
    sigma = np.outer(amplitudes, amplitudes.conj())
    nums = np.arange(cutoff)
    nsum = nums[:, None] + nums[None, :]
    ladder = np.sqrt((nums[:-1, None]+1)*(nums[None, :-1]+1))
    durations, signs = [T/2, T/2], [1, -1]
    for duration, sign in zip(durations, signs):
        def rhs(_, vector):
            matrix = vector.reshape(cutoff, cutoff)
            out = -(kappa/2+1j*chi*sign)*nsum*matrix
            out[:-1, :-1] += kappa*ladder*matrix[1:, 1:]
            return out.ravel()
        solution = solve_ivp(rhs, (0, duration), sigma.ravel(), method="DOP853", rtol=2e-11, atol=2e-13)
        if not solution.success:
            raise RuntimeError(solution.message)
        sigma = solution.y[:, -1].reshape(cutoff, cutoff)
    q, _ = old_column_overlap(kappa, chi, durations, signs)
    exact = np.exp(abs(alpha)**2*(q-1))
    numerical = np.trace(sigma)
    return {
        "kappa": kappa, "chi": chi, "T": T,
        "alpha": [alpha.real, alpha.imag], "cutoff": cutoff,
        "coherent_cutoff_normalization": norm,
        "exact_multiplier": [exact.real, exact.imag],
        "lindblad_multiplier": [numerical.real, numerical.imag],
        "absolute_error": abs(numerical-exact),
    }


def main():
    kappa, chi, T, N = 1e-4, .01, 1.84, 320
    symmetric = [T/4, T/2, T/4]
    first = brentq(lambda p: old_column_overlap(kappa, chi, [p,T/2,T/2-p], [1,-1,1])[0].imag,
                   T/8, 3*T/8, xtol=1e-15)
    phase_balanced = [first, T/2, T/2-first]
    results = {
        "scope": "Force-free ideal finite echoes; vacuum input ports; not a complete forced parity gate or finite-pulse schedule.",
        "parameters": {"kappa": kappa, "chi": chi, "T": T, "N_or_coherent_mean": N},
        "Hahn": echo_entry(kappa,chi,T,N,[T/2,T/2],[1,-1]),
        "symmetric_three_segments": echo_entry(kappa,chi,T,N,symmetric,[1,-1,1]),
        "phase_balanced_three_segments": echo_entry(kappa,chi,T,N,phase_balanced,[1,-1,1]),
        "phase_balance_timing_shift": first-T/4,
        "small_parameter_Hahn_prediction": {
            "one_minus_real_q": kappa*chi**2*T**3/6,
            "imag_q": -kappa*chi*T**2/2,
        },
        "independent_lindblad_check": independent_lindblad_check(),
    }
    out = Path(__file__).with_name("finite_echo_loss_obstruction_results.json")
    out.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

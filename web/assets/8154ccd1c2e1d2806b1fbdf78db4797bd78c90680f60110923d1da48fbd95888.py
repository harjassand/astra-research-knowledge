"""Exact rational audit of a covariance-quantized thermal-loss instance.

The trace-distance continuity inequality is imported from Mele et al.,
arXiv:2405.01431v4, Theorem 10. This script checks only the exact covariance,
energy, physicality, and rational reset-bound arithmetic for the fixture; it
does not certify either that imported inequality or the N72 reset theorem.
"""

from fractions import Fraction as F
import json
from pathlib import Path


def main():
    modes = 10_000
    eta = F(1, 1_000)
    delta = F(1, 100_000_000)

    # One mode of a stable quadratic Gibbs state at beta*w_tilde=log(4),
    # with q/p squeezing factors 2 and 1/2.
    vq, vp = F(5, 3), F(5, 12)
    xq, xp = vq - F(1, 2), vp - F(1, 2)
    assert (vq, vp, xq, xp) == (F(5, 3), F(5, 12), F(7, 6), -F(1, 12))

    # A rational raw covariance has spectral-norm error delta, then the
    # rational delta*I slack makes it physical by V+i*Omega/2 >= 0.
    # For this exact fixture the raw errors are (-delta, delta/2), so after
    # slack the q variance is exact and p grows by 3*delta/2.
    raw_q, raw_p = vq - delta, vp + delta / 2
    hat_q, hat_p = raw_q + delta, raw_p + delta
    assert hat_q == vq
    assert hat_p == vp + 3 * delta / 2
    assert hat_q * hat_p >= F(1, 4)  # one-mode uncertainty relation

    # Input and output total mean photon numbers. Uniform vacuum loss scales
    # centered input energy by eta; a passive circuit preserves it.
    energy_per_mode = (vq + vp - 1) / 2
    hat_energy_per_mode = (hat_q + hat_p - 1) / 2
    energy_in = modes * energy_per_mode
    hat_energy_in = modes * hat_energy_per_mode
    energy_out = eta * energy_in
    hat_energy_out = eta * hat_energy_in
    assert energy_out == F(65, 12)
    assert hat_energy_out < 6

    # Output covariance difference has one changed quadrature per mode.
    cov_error_in_trace = modes * (hat_q - vq + hat_p - vp)
    cov_error_out_trace = eta * cov_error_in_trace
    assert cov_error_in_trace == F(3, 2) * modes * delta
    assert cov_error_out_trace == F(3, 20_000_000)

    # Mele et al. Theorem 10 uses V_paper=2*V_here and
    # d_tr=||rho-sigma||_1/2. For zero means it implies
    # d_tr <= 2 f(N) sqrt(||V_here-Vhat_here||_1).
    # With N=6, f(N)^2=6.5+sqrt(42)<13. Hence d_tr^2<52*tau.
    # The rational 7/2500 bound squares to 7.84e-6 > 52*tau=7.8e-6.
    cov_tv_bound = F(7, 2_500)
    assert cov_tv_bound**2 > 52 * cov_error_out_trace

    # N72 ideal-reset bound, evaluated on the rational physical covariance.
    hat_xq = hat_q - F(1, 2)
    hat_xp = hat_p - F(1, 2)
    inv_one_minus_eta = 1 / (1 - eta)
    phi_per_mode = eta**3 * (
        hat_xq**2 * (hat_xq + inv_one_minus_eta)
        + hat_xp**2 * (hat_xp + inv_one_minus_eta)
    )
    phi_total = modes * phi_per_mode
    reset_tv_bound = F(5_184, 25) * phi_total
    total_bound = cov_tv_bound + reset_tv_bound
    assert total_bound < F(9, 1_000)  # < 0.009

    result = {
        "modes": modes,
        "eta": str(eta),
        "raw_entrywise_slack_delta": str(delta),
        "exact_input_covariance_diagonal": [str(vq), str(vp)],
        "rational_physical_approx_covariance_diagonal": [str(hat_q), str(hat_p)],
        "physicality_determinant": str(hat_q * hat_p),
        "input_covariance_trace_error": str(cov_error_in_trace),
        "output_covariance_trace_error": str(cov_error_out_trace),
        "exact_output_mean_photon_number": str(energy_out),
        "approx_output_mean_photon_number": str(hat_energy_out),
        "energy_cap_used_for_continuity": 6,
        "continuity_tv_bound_rational": str(cov_tv_bound),
        "phi_total_for_approx_covariance": str(phi_total),
        "ideal_reset_tv_bound_rational": str(reset_tv_bound),
        "combined_tv_bound_rational": str(total_bound),
        "combined_tv_bound_decimal": float(total_bound),
        "status": "PASS_EXACT_RATIONAL_INSTANCE; imported inequalities remain conditional",
    }
    out = Path(__file__).with_name("covariance_precision_checks.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

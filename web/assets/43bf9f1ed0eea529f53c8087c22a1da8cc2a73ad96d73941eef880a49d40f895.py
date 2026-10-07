"""Exact rational checks for the one-mode quadratic-Gibbs transfer.

This checks the covariance/purification algebra and a finite family budget.
It does not replay or certify the imported centered-reset theorem.
"""

from fractions import Fraction as F


def check_one_mode(q: F, eta: F, squeeze_scale: F):
    # TFD purification: tanh(r_beta)=q; its reduced thermal mean is n.
    n = q * q / (1 - q * q)
    anomalous = q / (1 - q * q)
    assert n == F(1, 3) if q == F(1, 2) else n >= 0

    # Choose the q quadrature covariance scale to be squeeze_scale (2 here);
    # the conjugate p scale is its reciprocal. K_beta=V_beta-I/2.
    vq = (n + F(1, 2)) * squeeze_scale
    vp = (n + F(1, 2)) / squeeze_scale
    xq, xp = vq - F(1, 2), vp - F(1, 2)

    # Passive/odd decomposition and covariance-only D certificate.
    r = (xq + xp) / 2
    x = (xq - xp) / 2
    d_pre = x * x / r - r
    d_after_loss = eta * d_pre
    assert 0 <= d_after_loss <= eta

    # With a uniform vacuum loss, C=eta I and B=eta/(1-eta) I.
    b = eta / (1 - eta)
    phi = eta**3 * (xq * xq * (xq + 1 / (1 - eta))
                    + xp * xp * (xp + 1 / (1 - eta)))
    phi_from_output_covariance = sum(
        (eta * z + b) * (eta * z) ** 2 for z in (xq, xp)
    )
    assert phi == phi_from_output_covariance
    mean_out = eta * (xq + xp) / 2
    s3 = eta**3  # T=sqrt(eta) times a unit row from the TFD passive network.
    assert mean_out >= 0 and s3 >= 0
    return {
        "thermal_mean_before_loss": n,
        "anomalous_moment": anomalous,
        "covariance_eigenvalues": (vq, vp),
        "K_beta_eigenvalues": (xq, xp),
        "D_before_loss": d_pre,
        "D_after_loss": d_after_loss,
        "B": b,
        "Phi_one_mode": phi,
        "mean_count_after_loss": mean_out,
        "S3": s3,
    }


def main():
    # H = omega a†a + g(a²+a†²)/2 with omega=1, g=-3/5.
    # Then |tanh(2s)|=3/5, so one covariance axis has scale 2 and
    # the conjugate axis scale 1/2. Choosing
    # beta*sqrt(omega²-g²)=log(4) gives n_beta=1/3 (q=1/2).
    result = check_one_mode(F(1, 2), F(1, 1000), F(2))
    assert result["covariance_eigenvalues"] == (F(5, 3), F(5, 12))
    assert result["K_beta_eigenvalues"] == (F(7, 6), F(-1, 12))
    assert result["D_before_loss"] == F(7, 39)

    modes = 10_000
    total_phi = modes * result["Phi_one_mode"]
    ideal_tv_bound = min(F(1), F(5184, 25) * total_phi)
    bit_tv_bound_without_additive_rounding = min(F(1), F(10125, 16) * total_phi)
    total_mean = modes * result["mean_count_after_loss"]
    assert ideal_tv_bound < F(1, 100)
    assert bit_tv_bound_without_additive_rounding < F(1, 50)

    print("one_mode:")
    for key, value in result.items():
        if isinstance(value, tuple):
            rendered = tuple(f"{x} ({float(x):.12g})" for x in value)
        else:
            rendered = f"{value} ({float(value):.12g})"
        print(f"  {key}: {rendered}")
    print(f"modes: {modes}")
    print(f"total_Phi: {total_phi} ({float(total_phi):.12g})")
    print(f"ideal_reset_TV_bound: {ideal_tv_bound} ({float(ideal_tv_bound):.12g})")
    print(f"bit_candidate_TV_bound_before_additive_epsilon: {bit_tv_bound_without_additive_rounding} ({float(bit_tv_bound_without_additive_rounding):.12g})")
    print(f"total_mean_output_count: {total_mean} ({float(total_mean):.12g})")


if __name__ == "__main__":
    main()

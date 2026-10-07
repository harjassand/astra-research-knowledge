"""Exact finite checks for the fixed-flow/fixed-volume metric sequence.

This verifies arithmetic instances, not the imported smooth-volume entropy
formula. The all-n formulas are proved in the adjacent text artifact.
"""
from fractions import Fraction as Q
import json


def one_case(n: int) -> dict:
    if n < 1:
        raise ValueError("n must be positive")
    a = Q(1, n)
    beta = Q(n * n)
    v = Q(n)
    nu = Q(3, 7)

    # Coefficients of H,e,f in E0,E+,E-.
    E0 = (Q(-1, 2 * n), Q(0), Q(0))
    Ep = (Q(0), Q(1), Q(0))
    Em = (Q(0), Q(0), Q(-n, 2))

    # Structure constants of [H,e]=2e, [H,f]=-2f, [e,f]=H.
    def bracket(u, w):
        H, e, f = u
        K, p, q = w
        return (
            e * q - f * p,
            2 * H * p - 2 * e * K,
            -2 * H * q + 2 * f * K,
        )

    def sub(x, y):
        return tuple(a0 - b0 for a0, b0 in zip(x, y))

    def scale(c, x):
        return tuple(c * z for z in x)

    brackets = {
        "[E0,Ep]=-a Ep": sub(bracket(E0, Ep), scale(-a, Ep)) == (0, 0, 0),
        "[E0,Em]=a Em": sub(bracket(E0, Em), scale(a, Em)) == (0, 0, 0),
        "[Ep,Em]=beta E0": sub(bracket(Ep, Em), scale(beta, E0)) == (0, 0, 0),
    }

    generator = scale(v, E0)
    fixed_generator = (Q(-1, 2), Q(0), Q(0))
    volume_determinant = E0[0] * Ep[1] * Em[2]
    entropy_rate = a * v
    strain_sq = 2 * entropy_rate**2
    power_density = 2 * nu * strain_sq
    equality_rhs = 4 * nu * entropy_rate**2
    scalar = -2 * a**2 - beta**2 / 2

    checks = {
        **brackets,
        "same_flow_generator": generator == fixed_generator,
        "same_volume_form_factor_4": volume_determinant == Q(1, 4),
        "entropy_rate_one": entropy_rate == 1,
        "strain_norm_sq_two": strain_sq == 2,
        "exact_work_equality": power_density == equality_rhs,
        "work_density_12_over_7": power_density == Q(12, 7),
    }
    return {
        "n": n,
        "a": str(a),
        "beta": str(beta),
        "v": str(v),
        "generator_H_e_f_coefficients": [str(x) for x in generator],
        "volume_form_factor_relative_to_mu0": "4",
        "entropy_rate": str(entropy_rate),
        "strain_norm_squared": str(strain_sq),
        "viscosity": str(nu),
        "work_density": str(power_density),
        "scalar_curvature": str(scalar),
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }


if __name__ == "__main__":
    rows = [one_case(n) for n in range(1, 13)]
    print(json.dumps({"status": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
                      "all_n_formulas": {
                          "a": "1/n", "beta": "n^2", "v": "n",
                          "X": "-H/2", "dvol/dmu0": "4",
                          "entropy_rate": "1", "strain_norm_sq": "2",
                          "nu": "3/7", "work_density": "12/7",
                          "scalar_curvature": "-2/n^2-n^4/2",
                      },
                      "cases": rows}, indent=2))

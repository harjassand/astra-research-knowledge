"""Independent coarse rational certificate for the declared elastic fixture.

No owner code is imported and no owner data is written. This proves the
two sign inequalities of the frozen-Eulerian, unstressed-incremental model;
it does not certify a loaded material tangent or a nonlinear skin basin.
"""

from fractions import Fraction as F
import json
from pathlib import Path


def fraction_record(value):
    return {"numerator": str(value.numerator), "denominator": str(value.denominator),
            "decimal_diagnostic": float(value)}


def construct_certificate():
    # All values below are supplied design parameters, not measurements.
    b = F(1, 50000)
    ce = F(91, 2 * 10**12)
    kn, rho = F(13, 250), F(10)
    G = F(2500, 13)
    nu = F(13, 10**6 * 96485)
    gamma = F(1, 2 * 10**10)
    kw, rv = F(158300000000), F(80)
    R = F(1, 4500)
    depth, bulk_kappa = b, F(1, 2)
    Lmax = R + depth / bulk_kappa
    Bplate = b**3 / (12 * ce)
    km0 = 2 / (b * ce)
    qbar = F(22500)
    ell = qbar * b / 2
    assert ell == F(9, 40)

    # k_plus(q)<=Bplate*q^4/2 follows by integrating tanh(t)<=t.
    kp_upper = Bplate * qbar**4 / 2
    m_lower = (km0 - kp_upper) / (km0 + kp_upper + 2 * kw)
    assert m_lower > F(99, 100)

    # Bound cosh(ell) by the first nonconstant term and a geometric tail.
    cosh_ell_upper = 1 + (ell**2 / 2) / (1 - ell**2 / 12)
    assert cosh_ell_upper < F(103, 100)
    # sinh(t)/t>=1 and cosh(t)<=cosh(ell) on 0<=t<=ell imply
    # k_plus(qbar)>=(Bplate*qbar^4/2)*(100/103)^3.
    chi_high_lower = gamma * qbar**2 + nu * kp_upper * F(100, 103)**3
    assert chi_high_lower > G

    beta2 = rho * b**2 * qbar**2
    assert beta2 == F(81, 40)
    cosh_beta_upper = 1 + (beta2 / 2) / (1 - beta2 / 12)
    sinhc_beta_upper = 1 + (beta2 / 6) / (1 - beta2 / 20)
    assert cosh_beta_upper < F(9, 4)
    assert sinhc_beta_upper < F(7, 5)
    H_coefficient = Lmax * kn * rho * b * qbar**2
    assert H_coefficient == F(6903, 5000) < F(7, 5)
    Hbar_upper = F(9, 4) + F(7, 5)**2
    feedback_lower = F(99, 100) * (1 + kn * rv)
    assert Hbar_upper == F(421, 100)
    assert feedback_lower == F(12771, 2500)
    assert feedback_lower > Hbar_upper

    # Independent same-skin, same-foundation R_v=0 instability witness.
    q = F(10000)
    chi_upper = gamma * q**2 + nu * (Bplate * q**4 + kw)
    assert chi_upper < G
    zbulk_lower = depth / bulk_kappa * (1 - (q * depth)**2 / 3)
    Llower = R + zbulk_lower
    t = rho * b**2 * q**2
    cosh_lower = 1 + t / 2 + t**2 / 24
    sinhc_lower = 1 + t / 6 + t**2 / 120
    Hlower = cosh_lower + Llower * kn * rho * b * q**2 * sinhc_lower
    ordinary_lower = (1 - chi_upper / G) * Hlower - 1
    assert ordinary_lower > F(1, 10)

    return {
        "scope": "exact rational certificate for declared frozen constitutive model only",
        "owner_code_imported": False,
        "all_q_certificate_pass": True,
        "qbar_per_m": int(qbar),
        "m_uniform_lower": fraction_record(m_lower),
        "chi_high_lower_over_G": fraction_record(chi_high_lower / G),
        "cosh_ell_upper": fraction_record(cosh_ell_upper),
        "cosh_beta_upper": fraction_record(cosh_beta_upper),
        "sinhc_beta_upper": fraction_record(sinhc_beta_upper),
        "Hbar_coarse_upper": fraction_record(Hbar_upper),
        "feedback_coarse_lower": fraction_record(feedback_lower),
        "ordinary_q10000_N_over_G_lower": fraction_record(ordinary_lower),
        "ordinary_identical_skin_instability_pass": True,
        "loaded_material_tangent_acquired": False,
        "nonlinear_spreading_skin_basin_proved": False,
    }


if __name__ == "__main__":
    result = construct_certificate()
    rendered = json.dumps(result, indent=2) + "\n"
    target = Path(__file__).with_name("INDEPENDENT_FIXTURE_CERTIFICATE.json")
    if target.exists():
        if target.read_text() != rendered:
            raise RuntimeError("Preserved certificate differs; refusing to replace it")
    else:
        target.write_text(rendered)
    print(rendered, end="")

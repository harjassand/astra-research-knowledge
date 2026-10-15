#!/usr/bin/env python3
"""Finite supplementary checks only; the analytic proof is in the adjacent file."""
import json
import platform
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import sympy as sp


def main():
    mp.mp.dps = 55
    g, n = sp.symbols("g n", real=True, positive=True)
    signed_numerator = sp.exp(2*g)/16 + sp.exp(-2*g) - sp.Rational(1, 2)
    strict_countermodel_identity = sp.simplify(
        sp.expand_trig(sp.sinh(g-sp.log(2))**2).rewrite(sp.exp)
        - signed_numerator
    ) == 0
    s, radius = sp.symbols("s radius", positive=True)
    u = radius*s
    k1_squared = sp.sinh(u)**2 / s**2
    k2_plus = radius/s - sp.exp(-u)*sp.sinh(u)/s**2
    k2_minus = -radius/s + sp.exp(u)*sp.sinh(u)/s**2
    defect = (sp.sinh(2*u)-2*u)/(2*s**2)
    pauli_plus_identity = sp.simplify((k2_plus-k1_squared+defect).rewrite(sp.exp)) == 0
    pauli_minus_identity = sp.simplify((k2_minus-k1_squared-defect).rewrite(sp.exp)) == 0

    ed, vd = Fraction(1, 2), Fraction(1, 4)
    ey, vy = Fraction(1), Fraction(1, 6)
    ec, vc = Fraction(1, 4), Fraction(5, 48)
    er = 2*(ed+ey)
    er2 = 4*(vd+vy)+er**2
    es = 1+2*(ed+ec)
    es2 = 4*(vd+vc)+es**2
    exact_moments = {
        "E_R": str(er), "E_R2": str(er2), "E_S2": str(es2),
        "coordinate_noise_variance": str(es2/3),
        "raw_score_second_moment_ratio": str((er2/3)/3),
    }
    moments_ok = (er, er2, es2, es2/3) == (
        Fraction(3), Fraction(32, 3), Fraction(23, 3), Fraction(23, 9)
    )

    def F(z):
        # Entire series is independent of the quadrature identities checked below.
        return mp.exp(mp.mpf("0.5") * mp.nsum(
            lambda j: z**j/(j*mp.factorial(j)), [1, mp.inf]
        ))

    def H(k):
        return mp.exp(1j*k)*F(2j*k)

    def G(k):
        z = 2j*k
        ratio = mp.mpf(1) if not k else mp.expm1(z)/z
        return mp.exp(1j*k)*F(z)*(1+ratio)/2

    def J(k):
        if not k:
            return mp.mpf(1)
        return F(2j*k)*(mp.expm1(4j*k)/(8j*k)+mp.exp(2j*k)/2)

    transform_checks = []
    for k in map(mp.mpf, ["0.125", "0.5", "1", "1.57079632679489661923", "2.5"]):
        phi = mp.im(H(k))/(2*k)
        scalar_noise_quad = mp.quad(lambda q: mp.re(G(q)), [0, k])/k
        covariant_scalar_quad = mp.quad(lambda q: mp.re(J(q)), [0, k])/k
        covariant_vector_quad = mp.quad(lambda q: q*mp.im(J(q)), [0, k])/k**2
        errors = {
            "scalar_noise_transform_error": abs(phi-scalar_noise_quad),
            "covariant_scalar_error": abs(covariant_scalar_quad-phi*mp.cos(k)),
            "covariant_vector_error": abs(covariant_vector_quad-phi*mp.sin(k)),
        }
        transform_checks.append({
            "frequency": mp.nstr(k, 25),
            "phi": mp.nstr(phi, 45),
            **{name: mp.nstr(value, 6) for name, value in errors.items()},
            "passes_1e_minus_45": all(e < mp.mpf("1e-45") for e in errors.values()),
        })

    result = {
        "scope": "Finite symbolic/rational/55-decimal diagnostics; no certification of analytic all-tail, infinite-dimensional, priority, or implementation claims.",
        "versions": {"python": platform.python_version(), "sympy": sp.__version__, "mpmath": mp.__version__},
        "strict_countermodel_identity": strict_countermodel_identity,
        "pauli_plus_identity": pauli_plus_identity,
        "pauli_minus_identity": pauli_minus_identity,
        "exact_moments": exact_moments,
        "exact_moments_ok": moments_ok,
        "new_trace_covariance_lower_bound_unit_pauli": mp.nstr(6+16/mp.pi**3, 35),
        "new_radial_coordinate_variance_lower_bound_unit_pauli": mp.nstr(2+16/(3*mp.pi**3), 35),
        "superseded_first_pass_radial_bound": mp.nstr(2+64/(27*mp.pi**4), 35),
        "transform_checks": transform_checks,
    }
    result["all_finite_checks_pass"] = all([
        strict_countermodel_identity, pauli_plus_identity, pauli_minus_identity,
        moments_ok, *[item["passes_1e_minus_45"] for item in transform_checks],
    ])
    output = Path(__file__).with_name("checks.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"all_finite_checks_pass": result["all_finite_checks_pass"], "saved": str(output)}))
    if not result["all_finite_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

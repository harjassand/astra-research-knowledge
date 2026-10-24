"""Finite diagnostics and rational certificates for ELASTIC_INTERFACE.txt.

No material data are acquired by this program. The all-q certificate and the
ordinary-skin instability witness use exact Fraction inequalities for the
declared model parameters; floating comparisons are separately labeled.
"""

from fractions import Fraction as F
import json
import math
from pathlib import Path

import numpy as np


def hyperbolic_bounds(x2, order=14):
    """Rational bounds for cosh(sqrt(x2)) and sinh(sqrt(x2))/sqrt(x2)."""
    assert x2 >= 0
    c = ct = F(1)
    s = st = F(1)
    for n in range(1, order + 1):
        ct *= x2 / ((2 * n - 1) * (2 * n))
        st *= x2 / ((2 * n) * (2 * n + 1))
        c += ct
        s += st
    rc = x2 / ((2 * order + 1) * (2 * order + 2))
    rs = x2 / ((2 * order + 2) * (2 * order + 3))
    assert rc < 1 and rs < 1
    return (c, c + ct * rc / (1 - rc)), (s, s + st * rs / (1 - rs))


def kp_bounds(q, b, ce):
    ell = q * b / 2
    (cl, cu), (slx, sux) = hyperbolic_bounds(ell * ell)
    sl, su = ell * slx, ell * sux
    lo = q / (2 * ce) * (sl * cl - ell) / (cu * cu)
    hi = q / (2 * ce) * (su * cu - ell) / (cl * cl)
    assert 0 < lo <= hi
    return lo, hi, (sl, su, cl, cu)


def bernstein_upper(coefficients, upper, bins=128):
    """Exact cubic upper bound from its Bernstein coefficients on each bin."""
    a0, a1, a2, a3 = coefficients
    answer = None
    for i in range(bins):
        left = upper * i / bins
        width = upper / bins
        p0 = a0 + a1 * left + a2 * left**2 + a3 * left**3
        p1 = width * (a1 + 2 * a2 * left + 3 * a3 * left**2)
        p2 = width**2 * (a2 + 3 * a3 * left)
        p3 = width**3 * a3
        beta = (p0, p0 + p1 / 3, p0 + 2 * p1 / 3 + p2 / 3,
                p0 + p1 + p2 + p3)
        bound = max(beta)
        answer = bound if answer is None else max(answer, bound)
    return answer


def ratio_record(x):
    return {"value": float(x), "numerator": str(x.numerator),
            "denominator": str(x.denominator)}


def declared_parameters():
    s = F(20, 10**6)
    d = s / F(9, 10)
    dref = 2 * s
    lam = d / dref
    mu = F(10**6)
    b = F(20, 10**6)
    young = F(20 * 10**9)
    poisson = F(3, 10)
    kn = F(52, 1000)
    rho = F(10)
    ce = (1 - poisson**2) / young
    nu_m = F(13, 10**6) / 96485
    gamma = F(5, 10**11)
    j0 = F(10)
    resistance = d**2 / (d - s)  # k_l=1 S/m
    rv = s**2 / (d - s)**2 - 1
    kw = s * mu / dref**2 * (2 * lam**-3 + 1)
    p0 = s / dref * mu * (lam**-2 - lam)
    bulk_depth, bulk_kappa = F(20, 10**6), F(1, 2)
    lmax = resistance + bulk_depth / bulk_kappa
    return dict(s=s, d=d, dref=dref, mu=mu, b=b, young=young,
                poisson=poisson, kn=kn, rho=rho, ce=ce, nu_m=nu_m,
                gamma=gamma, j0=j0, resistance=resistance, rv=rv,
                kw=kw, p0=p0, bulk_depth=bulk_depth,
                bulk_kappa=bulk_kappa, lmax=lmax, r=F(1, 10000))


def rational_certificate(p):
    qbar = F(22500)
    ybar = qbar**2
    g = p["j0"] / p["kn"]
    kpl, kpu, hbounds = kp_bounds(qbar, p["b"], p["ce"])
    km0 = 2 / (p["b"] * p["ce"])
    mmin = (km0 - kpu) / (km0 + kpu + 2 * p["kw"])
    sl, _, _, cu = hbounds
    ell = qbar * p["b"] / 2
    cb = sl / (ell * cu**3) / (1 + kpu / km0)
    plate_b = p["young"] * p["b"]**3 / (12 * (1 - p["poisson"]**2))
    high_q_lower = p["gamma"] * ybar + p["nu_m"] * kpl
    (_, ch), (_, sh) = hyperbolic_bounds(p["rho"] * p["b"]**2 * ybar)
    hu = ch + p["lmax"] * p["kn"] * p["rho"] * p["b"] * ybar * sh
    chord = (hu - 1) / ybar
    w0 = 1 - p["nu_m"] * p["kw"] * mmin**2 / g
    a0 = p["gamma"] / g
    c0 = p["nu_m"] * cb * plate_b / g
    polynomial = (w0, w0 * chord - a0, -(c0 + a0 * chord), -c0 * chord)
    rhs = bernstein_upper(polynomial, ybar)
    lhs = mmin * (1 + p["kn"] * p["rv"])
    assert high_q_lower > g
    assert km0 > kpu and mmin > 0 and cb > 0
    assert lhs > rhs
    return {
        "scope": "exact rational sufficient certificate for E1-E4, unstressed model",
        "qbar_per_m": int(qbar), "high_q_chi_lower_V_per_m": ratio_record(high_q_lower),
        "G_V_per_m": ratio_record(g), "m_lower": ratio_record(mmin),
        "plate_fraction_lower": ratio_record(cb),
        "left": ratio_record(lhs), "cubic_Bernstein_upper": ratio_record(rhs),
        "Bernstein_bins": 128, "all_q_certificate_pass": True,
    }


def ordinary_instability_witness(p):
    """A single exact positive-numerator lower bound, same support, R_v=0."""
    q = F(10000)
    _, kpu, _ = kp_bounds(q, p["b"], p["ce"])
    # k_eff(Kw) <= k_eff(0)+Kw <= 2 k_plus+Kw, since dk_eff/dKw=m^2<=1.
    chi_upper = p["gamma"] * q**2 + p["nu_m"] * (2 * kpu + p["kw"])
    g = p["j0"] / p["kn"]
    # tanh(x)>=x-x^3/3, so the actual finite bulk impedance has this lower bound.
    x = q * p["bulk_depth"]
    zb_lower = p["bulk_depth"] / p["bulk_kappa"] * (1 - x**2 / 3)
    llower = p["resistance"] + zb_lower
    (cl, _), (sl, _) = hyperbolic_bounds(p["rho"] * p["b"]**2 * q**2)
    hlower = cl + llower * p["kn"] * p["rho"] * p["b"] * q**2 * sl
    witness = (1 - chi_upper / g) * hlower - 1  # m<=1
    assert chi_upper < g and witness > 0
    return {"scope": "exact rational instability witness, identical support and skin, R_v=0",
            "q_per_m": int(q), "N_over_G_lower": ratio_record(witness),
            "positive_witness_pass": True}


def elastic_twoport(q, b, young, poisson, kw):
    ell = q * b / 2
    ce = (1 - poisson**2) / young
    kp = q / (2 * ce) * (math.tanh(ell) - ell / math.cosh(ell)**2)
    km = q / (2 * ce) * (1 / math.tanh(ell) + ell / math.sinh(ell)**2)
    aa, cc = (kp + km) / 2, (kp - km) / 2
    m = -cc / (aa + kw)
    # This equivalent positive form avoids subtractive cancellation at small q.
    ke = (kp * km + aa * kw) / (aa + kw)
    return np.array([[aa, cc], [cc, aa]]), m, ke


def airy_independent(q, b, young, poisson):
    """Independent 4x4 boundary solve in the Airy basis, no k+/- formulas."""
    def rows(z):
        # Phi=(a+b*t)exp(t)+(c+d*t)exp(-t), t=q*z.
        t = q * z
        ep, em = math.exp(t), math.exp(-t)
        val = np.array([ep, t * ep, em, t * em])
        first = np.array([ep, (t + 1) * ep, -em, (1 - t) * em]) * q
        third = np.array([ep, (t + 3) * ep, -em, (3 - t) * em]) * q**3
        return val, first, third
    v0, f0, t0 = rows(0)
    vb, fb, tb = rows(b)
    ce = (1 - poisson**2) / young
    mat = np.stack([f0, fb, ce * t0 / q**2, ce * tb / q**2])
    answer = np.empty((2, 2))
    for column in range(2):
        rhs = np.array([0., 0., float(column == 0), float(column == 1)])
        coeff = np.linalg.solve(mat, rhs)
        answer[:, column] = [q**2 * (v0 @ coeff), -q**2 * (vb @ coeff)]
    return answer


def float_diagnostics(p):
    x = {k: float(v) for k, v in p.items()}
    rng = np.random.default_rng(20261024)
    relative_errors = []
    moving_errors = []
    for _ in range(24):
        qb = float(rng.uniform(.15, 3.))
        q, b, young, poisson = qb, 1., 3., .27
        target, m, ke = elastic_twoport(q, b, young, poisson, .3)
        direct = airy_independent(q, b, young, poisson)
        relative_errors.append(float(np.max(abs(target - direct)) / np.max(abs(target))))
        rho, kn = float(rng.uniform(.2, 12)), .7
        jj, rr, ll, rv, nu_m, gamma = .8, .4, .6, .9, .2, .03
        g = jj / kn
        ch = math.cosh(q * b * math.sqrt(rho))
        sh = math.sinh(q * b * math.sqrt(rho))
        pp = kn * q * math.sqrt(rho)
        chi = gamma * q*q + nu_m * ke
        # Unknown bottom potential u0 and bottom current jb, with h=1 and top=m.
        mat = np.array([[1., -rr], [ch + ll * pp * sh, sh / pp + ll * ch]])
        rhs = np.array([chi - g, -m * (g + jj * rv)])
        _, jb = np.linalg.solve(mat, rhs)
        numerator = (g - chi) * (ch + ll * pp * sh) - m * (g + jj * rv)
        denominator = rr * ch + sh / pp + ll * (ch + rr * pp * sh)
        moving_errors.append(float(abs(jb - numerator / denominator)))
    q = 10000.
    _, m, ke = elastic_twoport(q, x["b"], x["young"], x["poisson"], x["kw"])
    ll = x["resistance"] + math.tanh(q*x["bulk_depth"])/(x["bulk_kappa"]*q)
    g = x["j0"] / x["kn"]
    chi = x["gamma"] * q*q + x["nu_m"] * ke
    qs = q * x["b"] * math.sqrt(x["rho"])
    hh = math.cosh(qs) + ll * x["kn"] * q * math.sqrt(x["rho"]) * math.sinh(qs)
    ordinary = (1 - chi/g) * hh - m
    responsive = ordinary - m * x["kn"] * x["rv"]
    m0 = 1 / (1 + x["kw"]*x["b"]*float(p["ce"]))
    n0 = g*(1-m0) - x["nu_m"]*x["kw"]*m0 - m0*x["j0"]*x["rv"]
    d0 = x["r"] + x["b"]/x["kn"] + x["lmax"]
    level = x["j0"]*d0/(-n0)
    return {
        "scope": "floating independent finite diagnostics, not continuum validation",
        "Airy_boundary_solves": len(relative_errors),
        "Airy_max_relative_matrix_error": max(relative_errors),
        "moving_face_max_current_residual": max(moving_errors),
        "q10000_m": m, "q10000_chi_V_per_m": chi,
        "q10000_ordinary_N_over_G_actual_bulk": ordinary,
        "q10000_responsive_N_over_G_actual_bulk": responsive,
        "longwave_leveling_length_m_mean_deposition": level,
        "mean_plating_time_one_efold_seconds": level/(x["nu_m"]*x["j0"]),
        "skin_ohmic_drop_V": x["j0"]*x["b"]/x["kn"],
        "pore_ohmic_drop_V": x["j0"]*x["resistance"],
        "preload_Pa_design_model": x["p0"],
        "mechanical_foundation_Pa_per_m_design_model": x["kw"],
        "current_rate_A_per_m2": x["j0"],
        "material_conjunction_acquired": False,
        "residual_stress_included_in_this_fixture": False,
        "nonlinear_skin_basin_proved": False,
        "rechargeable_cycle_proved": False,
    }


def main():
    p = declared_parameters()
    out = {"rational_all_q_certificate": rational_certificate(p),
           "rational_identical_skin_instability": ordinary_instability_witness(p),
           "diagnostics": float_diagnostics(p)}
    target = Path(__file__).with_name("ELASTIC_INTERFACE_RESULTS.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"all_q_pass": out["rational_all_q_certificate"]["all_q_certificate_pass"],
                      "certificate_left": out["rational_all_q_certificate"]["left"]["value"],
                      "certificate_right": out["rational_all_q_certificate"]["cubic_Bernstein_upper"]["value"],
                      "ordinary_instability_lower": out["rational_identical_skin_instability"]["N_over_G_lower"]["value"],
                      "diagnostics": out["diagnostics"]}, indent=2))


if __name__ == "__main__":
    main()
